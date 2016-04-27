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


""" arguments """
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", dest="test", action='store',
                    help="Test case or tier (group of tests) to be executed.")
args = parser.parse_args()


""" logging configuration """
logger = ft_logger.Logger("run_test").getLogger()

REPOS_DIR = os.getenv('repos_dir')
FUNCTEST_REPO = REPOS_DIR + '/functest/'


def run_test(test):
    # make the call here to run_tests.sh
    logger.info("Running test case '%s'..." % test.get_name())
    logger.debug("\n%s" % test)


def run_tier(tier):
    logger.info("Running tier\n\n'%s'..." % tier)


def run_all(tiers):
    logger.info("Tiers to be executed:\n\n%s" % tiers)


def main():
    CI_INSTALLER_TYPE = os.getenv('INSTALLER_TYPE')
    CI_SCENARIO = os.getenv('DEPLOY_SCENARIO')

    file = FUNCTEST_REPO + "/ci/testcases.yaml"
    _tiers = tb.TierBuilder(CI_INSTALLER_TYPE, CI_SCENARIO, file)

    if args.test:
        if _tiers.is_tier(args.test):
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
