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
import enum
import importlib
import logging
import logging.config
import os
import pkg_resources
import re
import sys

import prettytable

import functest.ci.tier_builder as tb
import functest.core.testcase as testcase
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
from functest.utils.constants import CONST

# __name__ cannot be used here
logger = logging.getLogger('functest.ci.run_tests')


class Result(enum.Enum):
    EX_OK = os.EX_OK
    EX_ERROR = -1


class BlockingTestFailed(Exception):
    pass


class TestNotEnabled(Exception):
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


class Runner(object):

    def __init__(self):
        self.executed_test_cases = []
        self.overall_result = Result.EX_OK
        self.clean_flag = True
        self.report_flag = False

    @staticmethod
    def print_separator(str, count=45):
        line = ""
        for i in range(0, count - 1):
            line += str
        logger.info("%s" % line)

    @staticmethod
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

    @staticmethod
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

    def run_test(self, test, tier_name, testcases=None):
        if not test.is_enabled():
            raise TestNotEnabled(
                "The test case {} is not enabled".format(test.get_name()))
        logger.info("\n")  # blank line
        self.print_separator("=")
        logger.info("Running test case '%s'...", test.get_name())
        self.print_separator("=")
        logger.debug("\n%s" % test)
        self.source_rc_file()

        flags = " -t %s" % test.get_name()
        if self.report_flag:
            flags += " -r"

        result = testcase.TestCase.EX_RUN_ERROR
        run_dict = self.get_run_dict(test.get_name())
        if run_dict:
            try:
                module = importlib.import_module(run_dict['module'])
                cls = getattr(module, run_dict['class'])
                test_dict = ft_utils.get_dict_by_test(test.get_name())
                test_case = cls(**test_dict)
                self.executed_test_cases.append(test_case)
                if self.clean_flag:
                    if test_case.create_snapshot() != test_case.EX_OK:
                        return result
                try:
                    kwargs = run_dict['args']
                    result = test_case.run(**kwargs)
                except KeyError:
                    result = test_case.run()
                if result == testcase.TestCase.EX_OK:
                    if self.report_flag:
                        test_case.push_to_db()
                    result = test_case.is_successful()
                logger.info("Test result:\n\n%s\n", test_case)
                if self.clean_flag:
                    test_case.clean()
            except ImportError:
                logger.exception("Cannot import module {}".format(
                    run_dict['module']))
            except AttributeError:
                logger.exception("Cannot get class {}".format(
                    run_dict['class']))
        else:
            raise Exception("Cannot import the class for the test case.")

        return result

    def run_tier(self, tier):
        tier_name = tier.get_name()
        tests = tier.get_tests()
        if tests is None or len(tests) == 0:
            logger.info("There are no supported test cases in this tier "
                        "for the given scenario")
            return 0
        logger.info("\n\n")  # blank line
        self.print_separator("#")
        logger.info("Running tier '%s'" % tier_name)
        self.print_separator("#")
        logger.debug("\n%s" % tier)
        for test in tests:
            result = self.run_test(test, tier_name)
            if result != testcase.TestCase.EX_OK:
                logger.error("The test case '%s' failed.", test.get_name())
                self.overall_result = Result.EX_ERROR
                if test.is_blocking():
                    raise BlockingTestFailed(
                        "The test case {} failed and is blocking".format(
                            test.get_name()))

    def run_all(self, tiers):
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
        for tier in tiers_to_run:
            self.run_tier(tier)

    def main(self, **kwargs):
        _tiers = tb.TierBuilder(
            CONST.__getattribute__('INSTALLER_TYPE'),
            CONST.__getattribute__('DEPLOY_SCENARIO'),
            pkg_resources.resource_filename('functest', 'ci/testcases.yaml'))

        if kwargs['noclean']:
            self.clean_flag = False

        if kwargs['report']:
            self.report_flag = True

        try:
            if kwargs['test']:
                self.source_rc_file()
                logger.debug("Test args: %s", kwargs['test'])
                if _tiers.get_tier(kwargs['test']):
                    self.run_tier(_tiers.get_tier(kwargs['test']))
                elif _tiers.get_test(kwargs['test']):
                    result = self.run_test(
                        _tiers.get_test(kwargs['test']),
                        _tiers.get_tier_name(kwargs['test']),
                        kwargs['test'])
                    if result != testcase.TestCase.EX_OK:
                        logger.error("The test case '%s' failed.",
                                     kwargs['test'])
                        self.overall_result = Result.EX_ERROR
                elif kwargs['test'] == "all":
                    self.run_all(_tiers)
                else:
                    logger.error("Unknown test case or tier '%s', "
                                 "or not supported by "
                                 "the given scenario '%s'."
                                 % (kwargs['test'],
                                    CONST.__getattribute__('DEPLOY_SCENARIO')))
                    logger.debug("Available tiers are:\n\n%s",
                                 _tiers)
                    return Result.EX_ERROR
            else:
                self.run_all(_tiers)
        except BlockingTestFailed:
            pass
        except Exception:
            logger.exception("Failures when running testcase(s)")
            self.overall_result = Result.EX_ERROR

        msg = prettytable.PrettyTable(
            header_style='upper', padding_width=5,
            field_names=['env var', 'value'])
        for env_var in ['INSTALLER_TYPE', 'DEPLOY_SCENARIO', 'BUILD_TAG',
                        'CI_LOOP']:
            msg.add_row([env_var, CONST.__getattribute__(env_var)])
        logger.info("Deployment description: \n\n%s\n", msg)

        if len(self.executed_test_cases) > 1:
            msg = prettytable.PrettyTable(
                header_style='upper', padding_width=5,
                field_names=['test case', 'project', 'tier',
                             'duration', 'result'])
            for test_case in self.executed_test_cases:
                result = 'PASS' if(test_case.is_successful(
                        ) == test_case.EX_OK) else 'FAIL'
                msg.add_row([test_case.case_name, test_case.project_name,
                             _tiers.get_tier_name(test_case.case_name),
                             test_case.get_duration(), result])
            logger.info("FUNCTEST REPORT: \n\n%s\n", msg)

        logger.info("Execution exit value: %s" % self.overall_result)
        return self.overall_result


def main():
    logging.config.fileConfig(pkg_resources.resource_filename(
        'functest', 'ci/logging.ini'))
    parser = RunTestsParser()
    args = parser.parse_args(sys.argv[1:])
    runner = Runner()
    return runner.main(**args).value
