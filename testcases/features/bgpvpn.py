#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Execute BGPVPN Tempest test cases
#
import argparse
import os
import re
import time
import yaml
import ConfigParser

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)

""" tests configuration """
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug",
                    help="Debug mode",
                    action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
args = parser.parse_args()

dirs = functest_yaml.get('general').get('directories')
FUNCTEST_REPO = dirs.get('dir_repo_functest')
BGPVPN_REPO = dirs.get('dir_repo_bgpvpn')
TEST_DB_URL = functest_yaml.get('results').get('test_db_url')

logger = ft_logger.Logger("bgpvpn").getLogger()


def main():
    logger.info("Running BGPVPN Tempest test case...")
    start_time = time.time()

    cmd = 'cd ' + BGPVPN_REPO + ';pip install --no-deps -e .'
    ft_utils.execute_command(cmd, logger, exit_on_error=False)

    src_tempest_dir = ft_utils.get_deployment_dir(logger)
    if not src_tempest_dir:
        logger.error("Rally deployment not found.")
        exit(-1)

    src_tempest_conf = src_tempest_dir + '/tempest.conf'
    dst_tempest_conf = src_tempest_dir + '/etc/tempest.conf'

    config = ConfigParser.RawConfigParser()
    config.read(src_tempest_conf)
    config.set('service_available', 'bgpvpn', 'True')
    with open(dst_tempest_conf, 'wb') as config_file:
        config.write(config_file)

    cmd_line = (src_tempest_dir +
                '/run_tempest.sh -t -N -- networking_bgpvpn_tempest;'
                'rm -rf ' + dst_tempest_conf)
    cmd = os.popen(cmd_line)
    output = cmd.read()
    # Results parsing
    error_logs = ""
    duration = 0
    tests = 0
    failed = 0
    try:
        # Look For errors
        error_logs = ""
        for match in re.findall('(.*?)[. ]*FAILED', output):
            error_logs += match
        # look for duration
        m = re.search('tests in(.*)sec', output)
        duration = m.group(1)
        # Look for tests run
        m = re.search('Ran:(.*)tests', output)
        tests = m.group(1)
        # Look for tests failed
        m = re.search('Failed:(.*)', output)
        failed = m.group(1)
    except:
        logger.error("Impossible to parse the result file")

    # Generate json results for DB
    json_results = {"duration": float(duration),
                    "tests": int(tests),
                    "failures": int(failed),
                    "errors": error_logs}

    logger.info("Results: " + str(json_results))
    criteria = "FAIL"
    # criteria = success rate = 100% (i.e all tests passed)
    # TODO use criteria defined in config file
    criteria_run = int(tests)
    if not failed:
        criteria_failed = 0
    else:
        criteria_failed = int(failed)

    if criteria_run > 0 and criteria_failed < 1:
        criteria = "PASS"

    # Push results in payload of testcase
    if args.report:
        logger.debug("Push bgpvpn results into DB")
        stop_time = time.time()
        ft_utils.push_results_to_db("sdnvpn",
                                    "bgpvpn_api",
                                    logger,
                                    start_time,
                                    stop_time,
                                    criteria,
                                    json_results)

if __name__ == '__main__':
    main()
