#!/usr/bin/env python
#
# Copyright (c) 2015 Orange
# guyrodrigue.koffi@orange.com
# morgan.richomme@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# 0.1 (05/2015) initial commit
# 0.2 (28/09/2015) extract Tempest, format json result, add ceilometer suite
# 0.3 (19/10/2015) remove Tempest from run_rally
# and push result into test DB
#
import argparse
import iniparse
import json
import logging
import os
import re
import requests
import subprocess
import sys
import time
import yaml

from novaclient import client as novaclient
from glanceclient import client as glanceclient
from keystoneclient.v2_0 import client as keystoneclient
from neutronclient.v2_0 import client as neutronclient
from cinderclient import client as cinderclient

""" tests configuration """
tests = ['authenticate', 'glance', 'cinder', 'heat', 'keystone',
         'neutron', 'nova', 'quotas', 'requests', 'vm', 'all']
parser = argparse.ArgumentParser()
parser.add_argument("test_name",
                    help="Module name to be tested. "
                         "Possible values are : "
                         "[ {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} | "
                         "{d[5]} | {d[6]} | {d[7]} | {d[8]} | {d[9]} | "
                         "{d[10]} ] "
                         "The 'all' value "
                         "performs all possible test scenarios"
                         .format(d=tests))

parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
parser.add_argument("-s", "--smoke",
                    help="Smoke test mode",
                    action="store_true")
parser.add_argument("-v", "--verbose",
                    help="Print verbose info about the progress",
                    action="store_true")
parser.add_argument("-n", "--noclean",
                    help="Don't clean the created resources for this test.",
                    action="store_true")

args = parser.parse_args()

client_dict = {}

if args.verbose:
    RALLY_STDERR = subprocess.STDOUT
else:
    RALLY_STDERR = open(os.devnull, 'w')

""" logging configuration """
logger = logging.getLogger("run_rally")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - "
                              "%(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

REPO_PATH = os.environ['repos_dir']+'/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)
sys.path.append(REPO_PATH + "testcases/")
import functest_utils
import openstack_utils

with open("/home/opnfv/functest/conf/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

HOME = os.environ['HOME']+"/"
SCENARIOS_DIR = REPO_PATH + functest_yaml.get("general"). \
    get("directories").get("dir_rally_scn")
TEMPLATE_DIR = SCENARIOS_DIR + "scenario/templates"
SUPPORT_DIR = SCENARIOS_DIR + "scenario/support"
###todo:
FLAVOR_NAME = "m1.tiny"
USERS_AMOUNT = 2
TENANTS_AMOUNT = 3
ITERATIONS_AMOUNT = 10
CONCURRENCY = 4

###
RESULTS_DIR = functest_yaml.get("general").get("directories"). \
    get("dir_rally_res")
TEMPEST_CONF_FILE = functest_yaml.get("general").get("directories"). \
    get("dir_results") + '/tempest/tempest.conf'
TEST_DB = functest_yaml.get("results").get("test_db_url")
PRIVATE_NETWORK = functest_yaml.get("general"). \
    get("openstack").get("neutron_private_net_name")

GLANCE_IMAGE_NAME = functest_yaml.get("general"). \
    get("openstack").get("image_name")
GLANCE_IMAGE_FILENAME = functest_yaml.get("general"). \
    get("openstack").get("image_file_name")
GLANCE_IMAGE_FORMAT = functest_yaml.get("general"). \
    get("openstack").get("image_disk_format")
GLANCE_IMAGE_PATH = functest_yaml.get("general"). \
    get("directories").get("dir_functest_data") + "/" + GLANCE_IMAGE_FILENAME

CINDER_VOLUME_TYPE_NAME = "volume_test"


SUMMARY = []


def push_results_to_db(case, payload, criteria):

    url = TEST_DB + "/results"
    installer = functest_utils.get_installer_type(logger)
    scenario = functest_utils.get_scenario(logger)
    # Until we found a way to manage version, use scenario
    version = scenario
    pod_name = functest_utils.get_pod_name(logger)

    # evalutate success criteria

    params = {"project_name": "functest", "case_name": case,
              "pod_name": pod_name, "installer": installer,
              "version": version, "scenario": scenario,
              "criteria": criteria, "details": payload}

    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(params), headers=headers)
    logger.debug(r)


def get_task_id(cmd_raw):
    """
    get task id from command rally result
    :param cmd_raw:
    :return: task_id as string
    """
    taskid_re = re.compile('^Task +(.*): started$')
    for line in cmd_raw.splitlines(True):
        line = line.strip()
        match = taskid_re.match(line)
        if match:
            return match.group(1)
    return None


def task_succeed(json_raw):
    """
    Parse JSON from rally JSON results
    :param json_raw:
    :return: Bool
    """
    rally_report = json.loads(json_raw)
    for report in rally_report:
        if report is None or report.get('result') is None:
            return False

        for result in report.get('result'):
            if result is None or len(result.get('error')) > 0:
                return False

    return True


def live_migration_supported():
    config = iniparse.ConfigParser()
    if config.read(TEMPEST_CONF_FILE) and \
       config.has_section('compute-feature-enabled') and \
       config.has_option('compute-feature-enabled', 'live_migration'):
        return config.getboolean('compute-feature-enabled', 'live_migration')

    return False


def build_task_args(test_file_name):
    task_args = {'service_list': [test_file_name]}
    task_args['smoke'] = args.smoke
    task_args['image_name'] = GLANCE_IMAGE_NAME
    task_args['flavor_name'] = FLAVOR_NAME
    task_args['glance_image_location'] = GLANCE_IMAGE_PATH
    task_args['tmpl_dir'] = TEMPLATE_DIR
    task_args['sup_dir'] = SUPPORT_DIR
    task_args['users_amount'] = USERS_AMOUNT
    task_args['tenants_amount'] = TENANTS_AMOUNT
    task_args['iterations'] = ITERATIONS_AMOUNT
    task_args['concurrency'] = CONCURRENCY

    ext_net = openstack_utils.get_external_net(client_dict['neutron'])
    if ext_net:
        task_args['floating_network'] = str(ext_net)
    else:
        task_args['floating_network'] = ''

    net_id = openstack_utils.get_network_id(client_dict['neutron'],
                                           PRIVATE_NETWORK)
    task_args['netid'] = str(net_id)
    task_args['live_migration'] = live_migration_supported()

    return task_args


def get_output(proc, test_name):
    global SUMMARY
    result = ""
    nb_tests = 0
    overall_duration = 0.0
    success = 0.0
    nb_totals = 0

    while proc.poll() is None:
        line = proc.stdout.readline()
        if args.verbose:
            result += line
        else:
            if "Load duration" in line or \
               "started" in line or \
               "finished" in line or \
               " Preparing" in line or \
               "+-" in line or \
               "|" in line:
                result += line
            elif "test scenario" in line:
                result += "\n" + line
            elif "Full duration" in line:
                result += line + "\n\n"

        # parse output for summary report
        if "| " in line and \
           "| action" not in line and \
           "| Starting" not in line and \
           "| Completed" not in line and \
           "| ITER" not in line and \
           "|   " not in line and \
           "| total" not in line:
            nb_tests += 1
        elif "| total" in line:
            percentage = ((line.split('|')[8]).strip(' ')).strip('%')
            try:
                success += float(percentage)
            except ValueError:
                logger.info('Percentage error: %s, %s' % (percentage, line))
            nb_totals += 1
        elif "Full duration" in line:
            duration = line.split(': ')[1]
            try:
                overall_duration += float(duration)
            except ValueError:
                logger.info('Duration error: %s, %s' % (duration, line))

    overall_duration="{:10.2f}".format(overall_duration)
    if nb_totals == 0:
        success_avg = 0
    else:
        success_avg = "{:0.2f}".format(success / nb_totals)

    scenario_summary = {'test_name': test_name,
                        'overall_duration': overall_duration,
                        'nb_tests': nb_tests,
                        'success': success_avg}
    SUMMARY.append(scenario_summary)

    logger.info("\n" + result)

    return result


def run_task(test_name):
    #
    # the "main" function of the script who launch rally for a task
    # :param test_name: name for the rally test
    # :return: void
    #
    global SUMMARY
    logger.info('Starting test scenario "{}" ...'.format(test_name))

    task_file = '{}task.yaml'.format(SCENARIOS_DIR)
    if not os.path.exists(task_file):
        logger.error("Task file '%s' does not exist." % task_file)
        exit(-1)

    test_file_name = '{}opnfv-{}.yaml'.format(SCENARIOS_DIR + "scenario/",
                                              test_name)
    if not os.path.exists(test_file_name):
        logger.error("The scenario '%s' does not exist." % test_file_name)
        exit(-1)

    logger.debug('Scenario fetched from : {}'.format(test_file_name))

    cmd_line = "rally task start --abort-on-sla-failure " + \
               "--task {} ".format(task_file) + \
               "--task-args \"{}\" ".format(build_task_args(test_name))
    logger.debug('running command line : {}'.format(cmd_line))

    p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE,
                         stderr=RALLY_STDERR, shell=True)
    output = get_output(p, test_name)
    task_id = get_task_id(output)
    logger.debug('task_id : {}'.format(task_id))

    if task_id is None:
        logger.error("Failed to retrieve task_id.")
        exit(-1)

    # check for result directory and create it otherwise
    if not os.path.exists(RESULTS_DIR):
        logger.debug('%s does not exist, we create it.'.format(RESULTS_DIR))
        os.makedirs(RESULTS_DIR)

    # write html report file
    report_file_name = '{}opnfv-{}.html'.format(RESULTS_DIR, test_name)
    cmd_line = "rally task report {} --out {}".format(task_id,
                                                      report_file_name)

    logger.debug('running command line : {}'.format(cmd_line))
    os.popen(cmd_line)

    # get and save rally operation JSON result
    cmd_line = "rally task results %s" % task_id
    logger.debug('running command line : {}'.format(cmd_line))
    cmd = os.popen(cmd_line)
    json_results = cmd.read()
    with open('{}opnfv-{}.json'.format(RESULTS_DIR, test_name), 'w') as f:
        logger.debug('saving json file')
        f.write(json_results)

    with open('{}opnfv-{}.json'
              .format(RESULTS_DIR, test_name)) as json_file:
        json_data = json.load(json_file)

    """ parse JSON operation result """
    status = "failed"
    if task_succeed(json_results):
        logger.info('Test scenario: "{}" OK.'.format(test_name) + "\n")
        status = "passed"
    else:
        logger.info('Test scenario: "{}" Failed.'.format(test_name) + "\n")

    # Push results in payload of testcase
    if args.report:
        logger.debug("Push result into DB")
        push_results_to_db("Rally_details", json_data, status)


def main():
    global SUMMARY
    # configure script
    if not (args.test_name in tests):
        logger.error('argument not valid')
        exit(-1)

    SUMMARY = []
    creds_nova = openstack_utils.get_credentials("nova")
    nova_client = novaclient.Client('2', **creds_nova)
    creds_neutron = openstack_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)
    creds_keystone = openstack_utils.get_credentials("keystone")
    keystone_client = keystoneclient.Client(**creds_keystone)
    glance_endpoint = keystone_client.service_catalog.url_for(service_type='image',
                                                              endpoint_type='publicURL')
    glance_client = glanceclient.Client(1, glance_endpoint,
                                        token=keystone_client.auth_token)
    creds_cinder = openstack_utils.get_credentials("cinder")
    cinder_client = cinderclient.Client('2', creds_cinder['username'],
                                        creds_cinder['api_key'],
                                        creds_cinder['project_id'],
                                        creds_cinder['auth_url'],
                                        service_type="volume")

    client_dict['neutron'] = neutron_client

    volume_types = openstack_utils.list_volume_types(cinder_client,
                                                    private=False)
    if not volume_types:
        volume_type = openstack_utils.create_volume_type(cinder_client,
                                                        CINDER_VOLUME_TYPE_NAME)
        if not volume_type:
            logger.error("Failed to create volume type...")
            exit(-1)
        else:
            logger.debug("Volume type '%s' created succesfully..." \
                         % CINDER_VOLUME_TYPE_NAME)
    else:
        logger.debug("Using existing volume type(s)...")

    image_id = openstack_utils.get_image_id(glance_client, GLANCE_IMAGE_NAME)

    if image_id == '':
        logger.debug("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME,
                                                           GLANCE_IMAGE_PATH))
        image_id = openstack_utils.create_glance_image(glance_client,
                                                      GLANCE_IMAGE_NAME,
                                                      GLANCE_IMAGE_PATH)
        if not image_id:
            logger.error("Failed to create the Glance image...")
            exit(-1)
        else:
            logger.debug("Image '%s' with ID '%s' created succesfully ." \
                         % (GLANCE_IMAGE_NAME, image_id))
    else:
        logger.debug("Using existing image '%s' with ID '%s'..." \
                     % (GLANCE_IMAGE_NAME, image_id))

    if args.test_name == "all":
        for test_name in tests:
            if not (test_name == 'all' or
                    test_name == 'vm'):
                run_task(test_name)
    else:
        logger.debug("Test name: " + args.test_name)
        run_task(args.test_name)

    report = "\n"\
             "                                                              \n"\
             "                     Rally Summary Report\n"\
             "+===================+============+===============+===========+\n"\
             "| Module            | Duration   | nb. Test Run  | Success   |\n"\
             "+===================+============+===============+===========+\n"
    payload = []

    #for each scenario we draw a row for the table
    total_duration = 0.0
    total_nb_tests = 0
    total_success = 0.0
    for s in SUMMARY:
        name = "{0:<17}".format(s['test_name'])
        duration = float(s['overall_duration'])
        total_duration += duration
        duration = time.strftime("%M:%S", time.gmtime(duration))
        duration = "{0:<10}".format(duration)
        nb_tests = "{0:<13}".format(s['nb_tests'])
        total_nb_tests += int(s['nb_tests'])
        success = "{0:<10}".format(str(s['success'])+'%')
        total_success += float(s['success'])
        report += ""\
        "| " + name + " | " + duration + " | " + nb_tests + " | " + success + "|\n"\
        "+-------------------+------------+---------------+-----------+\n"
        payload.append({'module': name,
                        'details': {'duration': s['overall_duration'],
                                    'nb tests': s['nb_tests'],
                                    'success': s['success']}})

    total_duration_str = time.strftime("%H:%M:%S", time.gmtime(total_duration))
    total_duration_str2 = "{0:<10}".format(total_duration_str)
    total_nb_tests_str = "{0:<13}".format(total_nb_tests)
    total_success = "{:0.2f}".format(total_success / len(SUMMARY))
    total_success_str = "{0:<10}".format(str(total_success)+'%')
    report += "+===================+============+===============+===========+\n"
    report += "| TOTAL:            | " + total_duration_str2 + " | " + \
            total_nb_tests_str  + " | " + total_success_str + "|\n"
    report += "+===================+============+===============+===========+\n"

    logger.info("\n"+report)
    payload.append({'summary': {'duration': total_duration,
                               'nb tests': total_nb_tests,
                               'nb success': total_success}})

    # Generate json results for DB
    #json_results = {"timestart": time_start, "duration": total_duration,
    #                "tests": int(total_nb_tests), "success": int(total_success)}
    #logger.info("Results: "+str(json_results))

    # Evaluation of the success criteria
    status = "failed"
    # for Rally we decided that the overall success rate must be above 90%
    if total_success >= 90:
        status = "passed"

    if args.report:
        logger.debug("Pushing Rally summary into DB...")
        push_results_to_db("Rally", payload, status)

    if args.noclean:
        exit(0)

    logger.debug("Deleting image '%s' with ID '%s'..." \
                 % (GLANCE_IMAGE_NAME, image_id))
    if not openstack_utils.delete_glance_image(nova_client, image_id):
        logger.error("Error deleting the glance image")

    if not volume_types:
        logger.debug("Deleting volume type '%s'..." \
                     % CINDER_VOLUME_TYPE_NAME)
        if not openstack_utils.delete_volume_type(cinder_client, volume_type):
            logger.error("Error in deleting volume type...")


if __name__ == '__main__':
    main()
