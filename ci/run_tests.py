#!/bin/bash
#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import argparse
import os
import sys

import functest.ci.tier_builder as tb
import functest.utils.functest_logger as ft_logger
import functest.utils.clean_openstack as clean_os


""" arguments """
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
logger = ft_logger.Logger("run_test").getLogger()


""" global variables """
REPOS_DIR = os.getenv('repos_dir')
FUNCTEST_REPO = ("%s/functest/" % REPOS_DIR)
EXEC_SCRIPT = ("%sci/exec_test.sh" % FUNCTEST_REPO)
CLEAN_FLAG = True
REPORT_FLAG = False


def print_separator(str, count=45):
    line = ""
    for i in range(0, count - 1):
        line += str

    logger.info("%s" % line)


def cleanup():
    print_separator("+")
    logger.info("Cleaning OpenStack resources...")
    print_separator("+")
    clean_os.main()
    print_separator("")


def run_test(test):
    test_name = test.get_name()
    print_separator("")
    print_separator("=")
    logger.info("Running test case '%s'..." % test_name)
    print_separator("=")
    logger.debug("\n%s" % test)
    flags = (" -t %s" % (test_name))
    if REPORT_FLAG:
        flags += " -r"

    cmd = ("%s%s" % (EXEC_SCRIPT, flags))
    logger.debug("Executing command %s" % cmd)

    print_separator("")

    if CLEAN_FLAG:
        cleanup()


def run_tier(tier):
    print_separator("#")
    logger.info("Running tier '%s'" % tier.get_name())
    print_separator("#")
    logger.debug("\n%s" % tier)
    for test in tier.get_tests():
        run_test(test)


def run_all(tiers):
    logger.debug("Tiers to be executed:\n\n%s" % tiers)
    for tier in tiers.get_tiers():
        run_tier(tier)


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
        if _tiers.get_tier(args.test):
            run_tier(_tiers.get_tier(args.test))

        elif _tiers.get_test(args.test):
            run_test(_tiers.get_test(args.test))

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

    sys.exit(0)

if __name__ == '__main__':
    main()
