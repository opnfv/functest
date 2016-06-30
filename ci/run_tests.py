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
import os
import re
import sys

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
    logger.info("Sourcing the OpenStack RC file...")
    os_utils.source_credentials(rc_file)


def generate_os_snapshot():
    logger.debug("Generating OpenStack snapshot...")
    os_snapshot.main()


def cleanup():
    os_clean.main()


def run_test(test):
    test_name = test.get_name()
    print_separator("=")
    logger.info("Running test case '%s'..." % test_name)
    print_separator("=")
    logger.debug("\n%s" % test)

    generate_os_snapshot()

    flags = (" -t %s" % (test_name))
    if REPORT_FLAG:
        flags += " -r"

    cmd = ("%s%s" % (EXEC_SCRIPT, flags))
    logger.debug("Executing command '%s'" % cmd)

    result = ft_utils.execute_command(cmd, logger, exit_on_error=False)

    if result != 0:
        logger.error("The test case '%s' failed. Cleaning and exiting."
                     % test_name)
        if CLEAN_FLAG:
            cleanup()
        sys.exit(1)

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
    summary = ""
    BUILD_TAG = os.getenv('BUILD_TAG')
    if BUILD_TAG is not None and re.search("daily", BUILD_TAG) is not None:
        CI_LOOP = "daily"
    else:
        CI_LOOP = "weekly"

    tiers_to_run = []

    for tier in tiers.get_tiers():
        if re.search(CI_LOOP, tier.get_ci_loop()) is not None:
            tiers_to_run.append(tier)
            summary += ("\n    - %s. %s:\n\t   %s"
                        % (tier.get_order(),
                           tier.get_name(),
                           tier.get_test_names()))

    logger.info("Tiers to be executed:%s" % summary)

    for tier in tiers_to_run:
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
        source_rc_file()
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
