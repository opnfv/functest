#!/usr/bin/env python
#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import argparse
import datetime
import os
import re
import sys
import functest.ci.generate_report as generate_report
import functest.ci.tier_builder as tb
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_clean as os_clean
import functest.utils.openstack_snapshot as os_snapshot
import functest.utils.openstack_utils as os_utils


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", dest="test", action='store',
                    help="Test case or tier (group of tests) to be executed. "
                    "It will run all the test if not specified.")
parser.add_argument("-n", "--noclean", help="Do not clean OpenStack resources"
                    " after running each test (default=false).",
                    action="store_true")
parser.add_argument("-r", "--report", help="Push results to database "
                    "(default=false).", action="store_true")
args = parser.parse_args()


""" logging configuration """
logger = ft_logger.Logger("run_tests").getLogger()


""" global variables """
REPOS_DIR = os.getenv('repos_dir')
FUNCTEST_REPO = ("%s/functest/" % REPOS_DIR)
EXEC_SCRIPT = ("%sci/exec_test.sh" % FUNCTEST_REPO)
CLEAN_FLAG = True
REPORT_FLAG = False
EXECUTED_TEST_CASES = []

# This will be the return code of this script. If any of the tests fails,
# this variable will change to -1
OVERALL_RESULT = 0


def print_separator(str, count=45):
    line = ""
    for i in range(0, count - 1):
        line += str
    logger.info("%s" % line)


def source_rc_file():
    rc_file = os.getenv('creds')
    if not os.path.isfile(rc_file):
        logger.error("RC file %s does not exist..." % rc_file)
        sys.exit(1)
    logger.debug("Sourcing the OpenStack RC file...")
    os_utils.source_credentials(rc_file)


def generate_os_snapshot():
    os_snapshot.main()


def cleanup():
    os_clean.main()


def update_test_info(test_name, result, duration):
    for test in EXECUTED_TEST_CASES:
        if test['test_name'] == test_name:
            test.update({"result": result,
                         "duration": duration})


def run_test(test, tier_name):
    global OVERALL_RESULT, EXECUTED_TEST_CASES
    result_str = "PASS"
    start = datetime.datetime.now()
    test_name = test.get_name()
    logger.info("\n")  # blank line
    print_separator("=")
    logger.info("Running test case '%s'..." % test_name)
    print_separator("=")
    logger.debug("\n%s" % test)

    if CLEAN_FLAG:
        generate_os_snapshot()

    flags = (" -t %s" % (test_name))
    if REPORT_FLAG:
        flags += " -r"

    cmd = ("%s%s" % (EXEC_SCRIPT, flags))
    logger.debug("Executing command '%s'" % cmd)
    result = ft_utils.execute_command(cmd, logger, exit_on_error=False)

    if CLEAN_FLAG:
        cleanup()
    end = datetime.datetime.now()
    duration = (end - start).seconds
    duration_str = ("%02d:%02d" % divmod(duration, 60))
    logger.info("Test execution time: %s" % duration_str)

    if result != 0:
        logger.error("The test case '%s' failed. " % test_name)
        OVERALL_RESULT = -1
        result_str = "FAIL"

        if test.is_blocking():
            if not args.test or args.test == "all":
                logger.info("This test case is blocking. Aborting overall "
                            "execution.")
                # if it is a single test we don't print the whole results table
                update_test_info(test_name, result_str, duration_str)
                generate_report.main(EXECUTED_TEST_CASES)
            logger.info("Execution exit value: %s" % OVERALL_RESULT)
            sys.exit(OVERALL_RESULT)

    update_test_info(test_name, result_str, duration_str)


def run_tier(tier):
    tier_name = tier.get_name()
    tests = tier.get_tests()
    if tests is None or len(tests) == 0:
        logger.info("There are no supported test cases in this tier "
                    "for the given scenario")
        return 0
    logger.info("\n\n")  # blank line
    print_separator("#")
    logger.info("Running tier '%s'" % tier_name)
    print_separator("#")
    logger.debug("\n%s" % tier)
    for test in tests:
        run_test(test, tier_name)


def run_all(tiers):
    global EXECUTED_TEST_CASES
    summary = ""
    BUILD_TAG = os.getenv('BUILD_TAG')
    if BUILD_TAG is not None and re.search("daily", BUILD_TAG) is not None:
        CI_LOOP = "daily"
    else:
        CI_LOOP = "weekly"

    tiers_to_run = []

    for tier in tiers.get_tiers():
        if (len(tier.get_tests()) != 0 and
                re.search(CI_LOOP, tier.get_ci_loop()) is not None):
            tiers_to_run.append(tier)
            summary += ("\n    - %s:\n\t   %s"
                        % (tier.get_name(),
                           tier.get_test_names()))

    logger.info("Tests to be executed:%s" % summary)
    EXECUTED_TEST_CASES = generate_report.init(tiers_to_run)
    for tier in tiers_to_run:
        run_tier(tier)

    generate_report.main(EXECUTED_TEST_CASES)


def main():
    global CLEAN_FLAG
    global REPORT_FLAG

    CI_INSTALLER_TYPE = os.getenv('INSTALLER_TYPE')
    CI_SCENARIO = os.getenv('DEPLOY_SCENARIO')

    file = FUNCTEST_REPO + "/ci/testcases.yaml"
    _tiers = tb.TierBuilder(CI_INSTALLER_TYPE, CI_SCENARIO, file)

    if args.noclean:
        CLEAN_FLAG = False

    if args.report:
        REPORT_FLAG = True

    if args.test:
        source_rc_file()
        if _tiers.get_tier(args.test):
            run_tier(_tiers.get_tier(args.test))

        elif _tiers.get_test(args.test):
            run_test(_tiers.get_test(args.test), _tiers.get_tier(args.test))

        elif args.test == "all":
            run_all(_tiers)

        else:
            logger.error("Unknown test case or tier '%s', or not supported by "
                         "the given scenario '%s'."
                         % (args.test, CI_SCENARIO))
            logger.debug("Available tiers are:\n\n%s"
                         % _tiers)
    else:
        run_all(_tiers)

    logger.info("Execution exit value: %s" % OVERALL_RESULT)
    sys.exit(OVERALL_RESULT)

if __name__ == '__main__':
    main()
