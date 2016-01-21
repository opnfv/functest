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

import re
import json
import os
import argparse
import logging
import yaml
import requests
import subprocess
import sys
from novaclient import client as novaclient
from glanceclient import client as glanceclient
from keystoneclient.v2_0 import client as keystoneclient
from neutronclient.v2_0 import client as neutronclient

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

REPO_PATH=os.environ['repos_dir']+'/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)
sys.path.append(REPO_PATH + "testcases/")
import functest_utils

with open("/home/opnfv/functest/conf/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

HOME = os.environ['HOME']+"/"
####todo:
#SCENARIOS_DIR = REPO_PATH + functest_yaml.get("general"). \
#    get("directories").get("dir_rally_scn")
SCENARIOS_DIR = REPO_PATH + "testcases/VIM/OpenStack/CI/rally_cert/"
###
TEMPLATE_DIR = SCENARIOS_DIR + "scenario/templates"
SUPPORT_DIR = SCENARIOS_DIR + "scenario/support"
###todo:
FLAVOR_NAME = "m1.tiny"
USERS_AMOUNT = 2
TENANTS_AMOUNT = 3
CONTROLLERS_AMOUNT = 2
###
RESULTS_DIR = functest_yaml.get("general").get("directories"). \
    get("dir_rally_res")
TEST_DB = functest_yaml.get("results").get("test_db_url")
FLOATING_NETWORK = functest_yaml.get("general"). \
    get("openstack").get("neutron_public_net_name")
FLOATING_SUBNET_CIDR = functest_yaml.get("general"). \
    get("openstack").get("neutron_public_subnet_cidr")
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


def push_results_to_db(payload):

    url = TEST_DB + "/results"
    installer = functest_utils.get_installer_type(logger)
    git_version = functest_utils.get_git_branch(REPO_PATH)
    pod_name = functest_utils.get_pod_name(logger)
    # TODO pod_name hardcoded, info shall come from Jenkins
    params = {"project_name": "functest", "case_name": "Rally",
              "pod_name": pod_name, "installer": installer,
              "version": git_version, "details": payload}

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
    rally_report = rally_report[0]
    if rally_report is None:
        return False
    if rally_report.get('result') is None:
        return False

    for result in rally_report.get('result'):
        if len(result.get('error')) > 0:
            return False

    return True


def build_task_args(test_file_name):
    task_args = {'service_list': [test_file_name]}
    task_args['smoke'] = args.smoke
    task_args['image_name'] = GLANCE_IMAGE_NAME
    task_args['flavor_name'] = FLAVOR_NAME
    task_args['glance_image_location'] = GLANCE_IMAGE_PATH
    task_args['floating_network'] = FLOATING_NETWORK
    task_args['floating_subnet_cidr'] = FLOATING_SUBNET_CIDR
    task_args['netid'] = functest_utils.get_network_id(client_dict['neutron'],
                                    PRIVATE_NETWORK).encode('ascii', 'ignore')
    task_args['tmpl_dir'] = TEMPLATE_DIR
    task_args['sup_dir'] = SUPPORT_DIR
    task_args['users_amount'] = USERS_AMOUNT
    task_args['tenants_amount'] = TENANTS_AMOUNT
    task_args['controllers_amount'] = CONTROLLERS_AMOUNT

    return task_args


def run_task(test_name):
    #
    # the "main" function of the script who launch rally for a task
    # :param test_name: name for the rally test
    # :return: void
    #

    logger.info('starting {} test ...'.format(test_name))

    task_file = '{}task.yaml'.format(SCENARIOS_DIR)
    if not os.path.exists(task_file):
        logger.error("Task file '%s' does not exist." % task_file)
        exit(-1)

    test_file_name = '{}opnfv-{}.yaml'.format(SCENARIOS_DIR + "scenario/", test_name)
    if not os.path.exists(test_file_name):
        logger.error("The scenario '%s' does not exist." % test_file_name)
        exit(-1)

    logger.debug('Scenario fetched from : {}'.format(test_file_name))

    cmd_line = "rally task start --abort-on-sla-failure " + \
               "--task {} ".format(task_file) + \
               "--task-args \"{}\" ".format(build_task_args(test_name))
    logger.debug('running command line : {}'.format(cmd_line))

    p = subprocess.Popen(cmd_line, stdout=subprocess.PIPE, stderr=RALLY_STDERR, shell=True)
    result = ""
    while p.poll() is None:
        l = p.stdout.readline()
        print l.replace('\n', '')
        result += l

    task_id = get_task_id(result)
    logger.debug('task_id : {}'.format(task_id))

    if task_id is None:
        logger.error("failed to retrieve task_id")
        exit(-1)

    # check for result directory and create it otherwise
    if not os.path.exists(RESULTS_DIR):
        logger.debug('does not exists, we create it'.format(RESULTS_DIR))
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

    # Push results in payload of testcase
    if args.report:
        logger.debug("Push result into DB")
        push_results_to_db(json_data)

    """ parse JSON operation result """
    if task_succeed(json_results):
        print 'Test OK'
    else:
        print 'Test KO'


def main():
    # configure script
    if not (args.test_name in tests):
        logger.error('argument not valid')
        exit(-1)

    creds_nova = functest_utils.get_credentials("nova")
    nova_client = novaclient.Client('2',**creds_nova)
    creds_neutron = functest_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)
    creds_keystone = functest_utils.get_credentials("keystone")
    keystone_client = keystoneclient.Client(**creds_keystone)
    glance_endpoint = keystone_client.service_catalog.url_for(service_type='image',
                                                   endpoint_type='publicURL')
    glance_client = glanceclient.Client(1, glance_endpoint,
                                        token=keystone_client.auth_token)

    client_dict['neutron'] = neutron_client

    image_id = functest_utils.get_image_id(glance_client, GLANCE_IMAGE_NAME)

    if image_id == '':
        logger.debug("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME, \
                                                           GLANCE_IMAGE_PATH))
        image_id = functest_utils.create_glance_image(glance_client,\
                                                GLANCE_IMAGE_NAME,GLANCE_IMAGE_PATH)
        if not image_id:
            logger.error("Failed to create the Glance image...")
            exit(-1)
        else:
            logger.debug("Image '%s' with ID '%s' created succesfully ." \
                         % (GLANCE_IMAGE_NAME, image_id))
    else:
        logger.debug("Using existing image '%s' with ID '%s'..." \
                     % (GLANCE_IMAGE_NAME,image_id))

    if args.test_name == "all":
        for test_name in tests:
            if not (test_name == 'all' or
                    test_name == 'vm'):
                print(test_name)
                run_task(test_name)
    else:
        print(args.test_name)
        run_task(args.test_name)

    logger.debug("Deleting image '%s' with ID '%s'..." \
                         % (GLANCE_IMAGE_NAME, image_id))
    if not functest_utils.delete_glance_image(nova_client, image_id):
        logger.error("Error deleting the glance image")

if __name__ == '__main__':
    main()
