#!/usr/bin/env python
#
# Description:
#    Runs tempest and pushes the results to the DB
#
# Authors:
#    morgan.richomme@orange.com
#    jose.lausuch@ericsson.com
#


import re
import json
import os
import argparse
import logging
import yaml
import requests

""" tests configuration """
parser = argparse.ArgumentParser()
parser.add_argument("repo_path", help="Path to the repository")
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
parser.add_argument("test_mode",
                    help="Tempest test mode", nargs='?', default="smoke")

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

with open(args.repo_path+"testcases/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

HOME = os.environ['HOME']+"/"
REPO_PATH = args.repo_path
TEST_DB = functest_yaml.get("results").get("test_db_url")

def get_info(file_result):
    test_run = ""
    duration = ""
    test_failed = ""

    p = subprocess.Popen('cat tempest.log', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        # print line,
        if (len(test_run) < 1): test_run = re.findall("[0-9]*\.[0-9]*s", line)
        if (len(duration) < 1): duration = re.findall("[0-9]*\ tests", line)
        regexp = r"(failures=[0-9]+)"
        if (len(test_failed) < 1): test_failed = re.findall(regexp, line)

    retval = p.wait()

    print "test_run:"
    print test_run
    print "duration:"
    print duration


def push_results_to_db(payload, module, pod_id):

    # TODO move DB creds into config file
    url = TEST_DB + "/results"
    params = {"project_name": "functest", "case_name": "Tempest",
              "pod_id": pod_id, "details": payload}
    headers = {'Content-Type': 'application/json'}

    # print url
    # print " ----- "
    # print params
    # print " ----- "

    r = requests.post(url, data=json.dumps(params), headers=headers)
    logger.debug(r)


def run_tempest(option):
    #
    # the "main" function of the script who lunch rally to run tempest
    # :param option: tempest option (smoke, ..)
    # :return: void
    #

    logger.info('starting Tempest test suite {}...'.format(option))

    cmd_line = 'rally verify start {}'.format(option)
    logger.debug('running command line : {}'.format(cmd_line))
    cmd = os.popen(cmd_line)

    cmd_line = "rally verify list"
    logger.debug('running command line : {}'.format(cmd_line))
    cmd = os.popen(cmd_line)

    # Push results in payload of testcase
    # push_results_to_db(json_results, test_name)


def main():
    # configure script

    run_tempest(args.test_mode)



if __name__ == '__main__':
    main()

