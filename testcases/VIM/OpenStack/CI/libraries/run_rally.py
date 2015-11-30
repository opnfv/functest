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
import sys
import novaclient.v2.client as novaclient

""" tests configuration """
tests = ['authenticate', 'glance', 'cinder', 'ceilometer', 'heat', 'keystone',
         'neutron', 'nova', 'quotas', 'requests', 'vm', 'all']
parser = argparse.ArgumentParser()
parser.add_argument("repo_path", help="Path to the repository")
parser.add_argument("test_name",
                    help="Module name to be tested"
                         "Possible values are : "
                         "[ {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} | "
                         "{d[5]} | {d[6]} | {d[7]} | {d[8]} | {d[9]} | "
                         "{d[10]} | {d[11]}]. The 'all' value "
                         "performs all the  possible tests scenarios"
                         .format(d=tests))

parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")

args = parser.parse_args()

sys.path.append(args.repo_path + "testcases/")
import functest_utils

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

with open(args.repo_path+"testcases/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

HOME = os.environ['HOME']+"/"
REPO_PATH = args.repo_path
SCENARIOS_DIR = REPO_PATH + functest_yaml.get("general"). \
    get("directories").get("dir_rally_scn")
RESULTS_DIR = HOME + functest_yaml.get("general").get("directories"). \
    get("dir_rally_res") + "/rally/"
TEST_DB = functest_yaml.get("results").get("test_db_url")

GLANCE_IMAGE_NAME = "functest-img-rally"
GLANCE_IMAGE_FILENAME = functest_yaml.get("general"). \
    get("openstack").get("image_file_name")
GLANCE_IMAGE_FORMAT = functest_yaml.get("general"). \
    get("openstack").get("image_disk_format")
GLANCE_IMAGE_PATH = functest_yaml.get("general"). \
    get("directories").get("dir_functest_data") + "/" + GLANCE_IMAGE_FILENAME


def push_results_to_db(payload):

    url = TEST_DB + "/results"
    installer = functest_utils.get_installer_type(logger)
    git_version = functest_utils.get_git_branch(args.repo_path)
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


def create_glance_image(path, name, disk_format):
    """
    Create a glance image given the absolute path of the image, its name and the disk format
    """
    cmd = ("glance image-create --name " + name + "  --visibility public "
           "--disk-format " + disk_format + " --container-format bare --file " + path)
    functest_utils.execute_command(cmd, logger)
    return True


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


def run_task(test_name):
    #
    # the "main" function of the script who lunch rally for a task
    # :param test_name: name for the rally test
    # :return: void
    #

    logger.info('starting {} test ...'.format(test_name))

    # check directory for scenarios test files or retrieve from git otherwise
    proceed_test = True
    test_file_name = '{}opnfv-{}.json'.format(SCENARIOS_DIR, test_name)

    if not os.path.exists(test_file_name):
        logger.error("The scenario '%s' does not exist." % test_file_name)
        exit(-1)

    # we do the test only if we have a scenario test file
    if proceed_test:
        logger.debug('Scenario fetched from : {}'.format(test_file_name))
        cmd_line = "rally task start --abort-on-sla-failure {}".format(test_file_name)
        logger.debug('running command line : {}'.format(cmd_line))
        cmd = os.popen(cmd_line)
        task_id = get_task_id(cmd.read())
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
    else:
        logger.error('{} test failed, unable to fetch a scenario test file'
                     .format(test_name))


def delete_glance_image(name):
    cmd = ("glance image-delete $(glance image-list | grep %s "
           "| awk '{print $2}' | head -1)" % name)
    functest_utils.execute_command(cmd, logger)
    return True


def cleanup(nova):
    logger.info("Cleaning up...")
    logger.debug("Deleting image...")
    delete_glance_image(GLANCE_IMAGE_NAME)
    return True


def main():
    # configure script
    if not (args.test_name in tests):
        logger.error('argument not valid')
        exit(-1)

    creds_nova = functest_utils.get_credentials("nova")
    nova_client = novaclient.Client(**creds_nova)

    logger.debug("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME, GLANCE_IMAGE_PATH))
    create_glance_image(GLANCE_IMAGE_PATH, GLANCE_IMAGE_NAME, GLANCE_IMAGE_FORMAT)

    # Check if the given image exists
    try:
        nova_client.images.find(name=GLANCE_IMAGE_NAME)
        logger.info("Glance image found '%s'" % GLANCE_IMAGE_NAME)
    except:
        logger.error("ERROR: Glance image '%s' not found." % GLANCE_IMAGE_NAME)
        logger.info("Available images are: ")
        exit(-1)

    if args.test_name == "all":
        for test_name in tests:
            if not (test_name == 'all' or
                    test_name == 'heat' or
                    test_name == 'ceilometer' or
                    test_name == 'smoke' or
                    test_name == 'vm'):
                print(test_name)
                run_task(test_name)
    else:
        print(args.test_name)
        run_task(args.test_name)

    cleanup(nova_client)

if __name__ == '__main__':
    main()
