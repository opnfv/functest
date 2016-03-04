#!/usr/bin/env python
#
# Description:
#    Runs tempest and pushes the results to the DB
#
# Authors:
#    morgan.richomme@orange.com
#    jose.lausuch@ericsson.com
#    viktor.tikkanen@nokia.com
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import argparse
import json
import logging
import os
import re
import requests
import shutil
import subprocess
import sys
import time
import yaml
import keystoneclient.v2_0.client as ksclient
from neutronclient.v2_0 import client as neutronclient

modes = ['full', 'smoke', 'baremetal', 'compute', 'data_processing',
         'identity', 'image', 'network', 'object_storage', 'orchestration',
         'telemetry', 'volume', 'custom']

""" tests configuration """
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug",
                    help="Debug mode",
                    action="store_true")
parser.add_argument("-s", "--serial",
                    help="Run tests in one thread",
                    action="store_true")
parser.add_argument("-m", "--mode",
                    help="Tempest test mode [smoke, all]",
                    default="smoke")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
parser.add_argument("-n", "--noclean",
                    help="Don't clean the created resources for this test.",
                    action="store_true")

args = parser.parse_args()

""" logging configuration """
logger = logging.getLogger('run_tempest')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

REPO_PATH=os.environ['repos_dir']+'/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)
sys.path.append(REPO_PATH + "testcases/")
import functest_utils

with open("/home/opnfv/functest/conf/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()
TEST_DB = functest_yaml.get("results").get("test_db_url")

MODE = "smoke"
TENANT_NAME = functest_yaml.get("tempest").get("identity").get("tenant_name")
TENANT_DESCRIPTION = functest_yaml.get("tempest").get("identity").get("tenant_description")
USER_NAME = functest_yaml.get("tempest").get("identity").get("user_name")
USER_PASSWORD = functest_yaml.get("tempest").get("identity").get("user_password")
SSH_USER_REGEX = functest_yaml.get("tempest").get("input-scenario").get("ssh_user_regex")
DEPLOYMENT_MAME = functest_yaml.get("rally").get("deployment_name")
RALLY_INSTALLATION_DIR = functest_yaml.get("general").get("directories").get("dir_rally_inst")
RESULTS_DIR = functest_yaml.get("general").get("directories").get("dir_results")
TEMPEST_RESULTS_DIR = RESULTS_DIR + '/tempest'


def get_info(file_result):
    test_run = ""
    duration = ""
    test_failed = ""

    p = subprocess.Popen('cat tempest.log',
                         shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        # print line,
        if (len(test_run) < 1):
            test_run = re.findall("[0-9]*\.[0-9]*s", line)
        if (len(duration) < 1):
            duration = re.findall("[0-9]*\ tests", line)
        regexp = r"(failures=[0-9]+)"
        if (len(test_failed) < 1):
            test_failed = re.findall(regexp, line)

    retval = p.wait()

    logger.debug("test_run:"+test_run)
    logger.debug("duration:"+duration)


def push_results_to_db(payload, module, pod_name):

    # TODO move DB creds into config file
    url = TEST_DB + "/results"
    installer = functest_utils.get_installer_type(logger)
    scenario = functest_utils.get_scenario(logger)
    logger.info("Pushing results to DB: '%s'." % url)

    params = {"project_name": "functest", "case_name": "Tempest",
              "pod_name": str(pod_name), 'installer': installer,
              "version": scenario, 'details': payload}
    headers = {'Content-Type': 'application/json'}

    r = requests.post(url, data=json.dumps(params), headers=headers)
    logger.debug(r)


def create_tempest_resources():
    ks_creds = functest_utils.get_credentials("keystone")
    logger.info("Creating tenant and user for Tempest suite")
    keystone = ksclient.Client(**ks_creds)
    tenant_id = functest_utils.create_tenant(keystone, TENANT_NAME, TENANT_DESCRIPTION)
    if tenant_id == '':
        logger.error("Error : Failed to create %s tenant" %TENANT_NAME)

    user_id = functest_utils.create_user(keystone, USER_NAME, USER_PASSWORD, None, tenant_id)
    if user_id == '':
        logger.error("Error : Failed to create %s user" %USER_NAME)


def free_tempest_resources():
    ks_creds = functest_utils.get_credentials("keystone")
    logger.info("Deleting tenant and user for Tempest suite)")
    keystone = ksclient.Client(**ks_creds)

    user_id = functest_utils.get_user_id(keystone, USER_NAME)
    if user_id == '':
        logger.error("Error : Failed to get id of %s user" % USER_NAME)
    else:
        if not functest_utils.delete_user(keystone, user_id):
            logger.error("Error : Failed to delete %s user" % USER_NAME)

    tenant_id = functest_utils.get_tenant_id(keystone, TENANT_NAME)
    if tenant_id == '':
        logger.error("Error : Failed to get id of %s tenant" % TENANT_NAME)
    else:
        if not functest_utils.delete_tenant(keystone, tenant_id):
            logger.error("Error : Failed to delete %s tenant" % TENANT_NAME)


def configure_tempest():
    """
    Add/update needed parameters into tempest.conf file generated by Rally
    """

    logger.debug("Generating tempest.conf file...")
    cmd = "rally verify genconfig"
    functest_utils.execute_command(cmd,logger)

    logger.debug("Resolving deployment UUID...")
    cmd = "rally deployment list | awk '/"+DEPLOYMENT_MAME+"/ {print $2}'"
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT);
    deployment_uuid = p.stdout.readline().rstrip()
    if deployment_uuid == "":
        logger.debug("   Rally deployment NOT found")
        return False

    logger.debug("Finding tempest.conf file...")
    tempest_conf_file = RALLY_INSTALLATION_DIR+"/tempest/for-deployment-" \
                        +deployment_uuid+"/tempest.conf"
    if not os.path.isfile(tempest_conf_file):
        logger.error("   Tempest configuration file %s NOT found." % tempest_conf_file)
        return False

    logger.debug("  Updating fixed_network_name...")
    private_net_name = ""
    creds_neutron = functest_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)
    private_net = functest_utils.get_private_net(neutron_client)
    if private_net is None:
        logger.error("No shared private networks found.")
    else:
        private_net_name = private_net['name']
    cmd = "crudini --set "+tempest_conf_file+" compute fixed_network_name " \
          +private_net_name
    functest_utils.execute_command(cmd,logger)

    logger.debug("  Updating non-admin credentials...")
    cmd = "crudini --set "+tempest_conf_file+" identity tenant_name " \
          +TENANT_NAME
    functest_utils.execute_command(cmd,logger)
    cmd = "crudini --set "+tempest_conf_file+" identity username " \
          +USER_NAME
    functest_utils.execute_command(cmd,logger)
    cmd = "crudini --set "+tempest_conf_file+" identity password " \
          +USER_PASSWORD
    functest_utils.execute_command(cmd,logger)
    cmd = "sed -i 's/.*ssh_user_regex.*/ssh_user_regex = "+SSH_USER_REGEX+"/' "+tempest_conf_file
    functest_utils.execute_command(cmd,logger)


    # Copy tempest.conf to /home/opnfv/functest/results/tempest/
    shutil.copyfile(tempest_conf_file,TEMPEST_RESULTS_DIR+'/tempest.conf')
    return True


def run_tempest(OPTION):
    #
    # the "main" function of the script which launches Rally to run Tempest
    # :param option: tempest option (smoke, ..)
    # :return: void
    #
    logger.info("Starting Tempest test suite: '%s'." % OPTION)
    cmd_line = "rally verify start " + OPTION + " --system-wide"
    logger.debug('Executing command : {}'.format(cmd_line))

    CI_DEBUG = os.environ.get("CI_DEBUG")
    if CI_DEBUG == "true" or CI_DEBUG == "True":
        subprocess.call(cmd_line, shell=True, stderr=subprocess.STDOUT)
    else:
        header = "Tempest environment:\n"\
            "  Installer: %s\n  Scenario: %s\n  Node: %s\n  Date: %s\n" % \
            (os.getenv('INSTALLER_TYPE','Unknown'), \
             os.getenv('DEPLOY_SCENARIO','Unknown'), \
             os.getenv('NODE_NAME','Unknown'), \
             time.strftime("%a %b %d %H:%M:%S %Z %Y"))

        f_stdout = open(TEMPEST_RESULTS_DIR+"/tempest.log", 'w+')
        f_stderr = open(TEMPEST_RESULTS_DIR+"/tempest-error.log", 'w+')
        f_env = open(TEMPEST_RESULTS_DIR+"/environment.log", 'w+')
        f_env.write(header)

        subprocess.call(cmd_line, shell=True, stdout=f_stdout, stderr=f_stderr)

        f_stdout.close()
        f_stderr.close()
        f_env.close()

        cmd_line = "rally verify show"
        subprocess.call(cmd_line, shell=True)

    cmd_line = "rally verify list"
    logger.debug('Executing command : {}'.format(cmd_line))
    cmd = os.popen(cmd_line)
    output = (((cmd.read()).splitlines()[3]).replace(" ", "")).split("|")
    # Format:
    # | UUID | Deployment UUID | smoke | tests | failures | Created at |
    # Duration | Status  |
    num_tests = output[4]
    num_failures = output[5]
    time_start = output[6]
    duration = output[7]
    # Compute duration (lets assume it does not take more than 60 min)
    dur_min=int(duration.split(':')[1])
    dur_sec_float=float(duration.split(':')[2])
    dur_sec_int=int(round(dur_sec_float,0))
    dur_sec_int = dur_sec_int + 60 * dur_min

    # Generate json results for DB
    json_results = {"timestart": time_start, "duration": dur_sec_int,
                    "tests": int(num_tests), "failures": int(num_failures)}
    logger.info("Results: "+str(json_results))
    pod_name = functest_utils.get_pod_name(logger)

    # Push results in payload of testcase
    if args.report:
        logger.debug("Push result into DB")
        push_results_to_db(json_results, MODE, pod_name)


def main():
    global MODE
    if not (args.mode):
        MODE = "smoke"
    elif not (args.mode in modes):
        logger.error("Tempest mode not valid. Possible values are:\n"
                     + str(modes))
        exit(-1)
    elif (args.mode == 'custom'):
        MODE = "--tests-file "+REPO_PATH+"testcases/VIM/OpenStack/CI/custom_tests/test_list.txt"
    else:
        MODE = "--set "+args.mode

    if args.serial:
        MODE = "--concur 1 "+MODE

    if not os.path.exists(TEMPEST_RESULTS_DIR):
        os.makedirs(TEMPEST_RESULTS_DIR)

    create_tempest_resources()
    configure_tempest()
    run_tempest(MODE)

    if args.noclean:
        exit(0)

    free_tempest_resources()


if __name__ == '__main__':
    main()
