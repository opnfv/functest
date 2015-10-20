#!/usr/bin/env python
#
# Description:
#    Runs tempest and pushes the results to the DB
#
# Authors:
#    morgan.richomme@orange.com
#    jose.lausuch@ericsson.com
#

import argparse
import json
import logging
import os
import re
import requests
import subprocess
import sys
import yaml

modes = ['full', 'smoke', 'baremetal', 'compute', 'data_processing',
         'identity', 'image', 'network', 'object_storage', 'orchestration',
         'telemetry', 'volume']

""" tests configuration """
parser = argparse.ArgumentParser()
parser.add_argument("repo_path", help="Path to the Functest repository")
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
parser.add_argument("-m", "--mode", help="Tempest test mode [smoke, all]",
                    default="smoke")

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

with open(args.repo_path+"/testcases/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

REPO_PATH = args.repo_path
TEST_DB = functest_yaml.get("results").get("test_db_url")
sys.path.append(args.repo_path + "/testcases/")
import functest_utils

MODE = "smoke"


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
    git_version = functest_utils.get_git_branch(REPO_PATH)
    logger.info("Pushing results to DB: '%s'." % url)

    params = {"project_name": "functest", "case_name": "Tempest",
              "pod_name": str(pod_name), 'installer': installer,
              "version": git_version, 'details': payload}
    headers = {'Content-Type': 'application/json'}

    r = requests.post(url, data=json.dumps(params), headers=headers)
    logger.debug(r)


def run_tempest(OPTION):
    #
    # the "main" function of the script which launches Rally to run Tempest
    # :param option: tempest option (smoke, ..)
    # :return: void
    #
    logger.info("Starting Tempest test suite: '%s'." % OPTION)
    cmd_line = "rally verify start "+OPTION
    logger.debug('Executing command : {}'.format(cmd_line))
    subprocess.call(cmd_line, shell=True, stderr=subprocess.STDOUT)

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
    if dur_min > 0:
        dur_sec_int = dur_sec_int + 60 * dur_min

    # Generate json results for DB
    json_results = {"timestart": time_start, "duration": dur_sec_int,
                    "tests": int(num_tests), "failures": int(num_failures)}
    logger.info("Results: "+str(json_results))
    push_results_to_db(json_results, MODE, "opnfv-jump-2")


def main():
    global MODE
    if not (args.mode):
        MODE = "smoke"
    elif not (args.mode in modes):
        logger.error("Tempest mode not valid. Possible values are:\n"
                     + str(modes))
        exit(-1)
    else:
        MODE = args.mode

    run_tempest(MODE)


if __name__ == '__main__':
    main()
