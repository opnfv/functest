#!/usr/bin/python -u
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
import enum
import importlib
import logging
import logging.config
import os
import re
import sys

import functest.ci.generate_report as generate_report
import functest.ci.tier_builder as tb
import functest.core.testcase as testcase
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_clean as os_clean
import functest.utils.openstack_snapshot as os_snapshot
import functest.utils.openstack_utils as os_utils
from functest.utils.constants import CONST

# __name__ cannot be used here
logger = logging.getLogger('functest.ci.run_tests')


class Result(enum.Enum):
    EX_OK = os.EX_OK
    EX_ERROR = -1


class BlockingTestFailed(Exception):
    pass


class RunTestsParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-t", "--test", dest="test", action='store',
                                 help="Test case or tier (group of tests) "
                                 "to be executed. It will run all the test "
                                 "if not specified.")
        self.parser.add_argument("-n", "--noclean", help="Do not clean "
                                 "OpenStack resources after running each "
                                 "test (default=false).",
                                 action="store_true")
        self.parser.add_argument("-r", "--report", help="Push results to "
                                 "database (default=false).",
                                 action="store_true")

    def parse_args(self, argv=[]):
        return vars(self.parser.parse_args(argv))


class GlobalVariables:
    EXECUTED_TEST_CASES = []
    OVERALL_RESULT = Result.EX_OK
    CLEAN_FLAG = True
    REPORT_FLAG = False


def print_separator(str, count=45):
    line = ""
    for i in range(0, count - 1):
        line += str
    logger.info("%s" % line)


def source_rc_file():
    rc_file = CONST.__getattribute__('openstack_creds')
    if not os.path.isfile(rc_file):
        raise Exception("RC file %s does not exist..." % rc_file)
    logger.debug("Sourcing the OpenStack RC file...")
    os_utils.source_credentials(rc_file)
    for key, value in os.environ.iteritems():
        if re.search("OS_", key):
            if key == 'OS_AUTH_URL':
                CONST.__setattr__('OS_AUTH_URL', value)
            elif key == 'OS_USERNAME':
                CONST.__setattr__('OS_USERNAME', value)
            elif key == 'OS_TENANT_NAME':
                CONST.__setattr__('OS_TENANT_NAME', value)
            elif key == 'OS_PASSWORD':
                CONST.__setattr__('OS_PASSWORD', value)


def generate_os_snapshot():
    os_snapshot.main()


def cleanup():
    os_clean.main()


def update_test_info(test_name, result, duration):
    for test in GlobalVariables.EXECUTED_TEST_CASES:
        if test['test_name'] == test_name:
            test.update({"result": result,
                         "duration": duration})


def get_run_dict(testname):
    try:
        dict = ft_utils.get_dict_by_test(testname)
        if not dict:
            logger.error("Cannot get {}'s config options".format(testname))
        elif 'run' in dict:
            return dict['run']
        return None
    except Exception:
        logger.exception("Cannot get {}'s config options".format(testname))
        return None


def run_test(test, tier_name, testcases=None):
    result_str = "PASS"
    start = datetime.datetime.now()
    test_name = test.get_name()
    logger.info("\n")  # blank line
    print_separator("=")
    logger.info("Running test case '%s'..." % test_name)
    print_separator("=")
    logger.debug("\n%s" % test)
    source_rc_file()

    if test.needs_clean() and GlobalVariables.CLEAN_FLAG:
        generate_os_snapshot()

    flags = (" -t %s" % (test_name))
    if GlobalVariables.REPORT_FLAG:
        flags += " -r"

    result = testcase.TestCase.EX_RUN_ERROR
    run_dict = get_run_dict(test_name)
    if run_dict:
        try:
            module = importlib.import_module(run_dict['module'])
            cls = getattr(module, run_dict['class'])
            test_dict = ft_utils.get_dict_by_test(test_name)
            test_case = cls(**test_dict)

            try:
                kwargs = run_dict['args']
                result = test_case.run(**kwargs)
            except KeyError:
                result = test_case.run()
            if result == testcase.TestCase.EX_OK:
                if GlobalVariables.REPORT_FLAG:
                    test_case.push_to_db()
                result = test_case.check_result()
        except ImportError:
            logger.exception("Cannot import module {}".format(
                run_dict['module']))
        except AttributeError:
            logger.exception("Cannot get class {}".format(
                run_dict['class']))
    else:
        raise Exception("Cannot import the class for the test case.")

    if test.needs_clean() and GlobalVariables.CLEAN_FLAG:
        cleanup()

    end = datetime.datetime.now()
    duration = (end - start).seconds
    duration_str = ("%02d:%02d" % divmod(duration, 60))
    logger.info("Test execution time: %s" % duration_str)

    if result != 0:
        logger.error("The test case '%s' failed. " % test_name)
        GlobalVariables.OVERALL_RESULT = Result.EX_ERROR
        result_str = "FAIL"

        if test.is_blocking():
            if not testcases or testcases == "all":
                # if it is a single test we don't print the whole results table
                update_test_info(test_name, result_str, duration_str)
                generate_report.main(GlobalVariables.EXECUTED_TEST_CASES)
            raise BlockingTestFailed("The test case {} failed and is blocking"
                                     .format(test.get_name()))

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
    summary = ""
    tiers_to_run = []

    for tier in tiers.get_tiers():
        if (len(tier.get_tests()) != 0 and
                re.search(CONST.__getattribute__('CI_LOOP'),
                          tier.get_ci_loop()) is not None):
            tiers_to_run.append(tier)
            summary += ("\n    - %s:\n\t   %s"
                        % (tier.get_name(),
                           tier.get_test_names()))

    logger.info("Tests to be executed:%s" % summary)
    GlobalVariables.EXECUTED_TEST_CASES = generate_report.init(tiers_to_run)
    for tier in tiers_to_run:
        run_tier(tier)

    generate_report.main(GlobalVariables.EXECUTED_TEST_CASES)


def main(**kwargs):

    file = CONST.functest_testcases_yaml
    _tiers = tb.TierBuilder(CONST.__getattribute__('INSTALLER_TYPE'),
                            CONST.__getattribute__('DEPLOY_SCENARIO'),
                            file)

    if kwargs['noclean']:
        GlobalVariables.CLEAN_FLAG = False

    if kwargs['report']:
        GlobalVariables.REPORT_FLAG = True

    try:
        if kwargs['test']:
            source_rc_file()
            if _tiers.get_tier(kwargs['test']):
                GlobalVariables.EXECUTED_TEST_CASES = generate_report.init(
                    [_tiers.get_tier(kwargs['test'])])
                run_tier(_tiers.get_tier(kwargs['test']))
            elif _tiers.get_test(kwargs['test']):
                run_test(_tiers.get_test(kwargs['test']),
                         _tiers.get_tier(kwargs['test']),
                         kwargs['test'])
            elif kwargs['test'] == "all":
                run_all(_tiers)
            else:
                logger.error("Unknown test case or tier '%s', "
                             "or not supported by "
                             "the given scenario '%s'."
                             % (kwargs['test'],
                                CONST.__getattribute__('DEPLOY_SCENARIO')))
                logger.debug("Available tiers are:\n\n%s"
                             % _tiers)
                return Result.EX_ERROR
        else:
            run_all(_tiers)
    except Exception as e:
        logger.error(e)
        GlobalVariables.OVERALL_RESULT = Result.EX_ERROR
    logger.info("Execution exit value: %s" % GlobalVariables.OVERALL_RESULT)
    return GlobalVariables.OVERALL_RESULT


if __name__ == '__main__':
    logging.config.fileConfig(
        CONST.__getattribute__('dir_functest_logging_cfg'))
    parser = RunTestsParser()
    args = parser.parse_args(sys.argv[1:])
    sys.exit(main(**args).value)
