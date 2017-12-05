#!/usr/bin/env python

# Copyright (c) 2016 Ericsson AB and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
import enum
import importlib
import logging
import logging.config
import os
import pkg_resources
import re
import sys
import textwrap

import prettytable
import six
import yaml

import functest
import functest.ci.tier_builder as tb
import functest.core.testcase as testcase
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
from functest.utils.constants import CONST

# __name__ cannot be used here
logger = logging.getLogger('functest.ci.run_tests')

CONFIG_FUNCTEST_PATH = pkg_resources.resource_filename(
    'functest', 'ci/config_functest.yaml')


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
        self.executed_test_cases = {}
        self.overall_result = Result.EX_OK
        self.clean_flag = True
        self.report_flag = False
        self._tiers = tb.TierBuilder(
            CONST.__getattribute__('INSTALLER_TYPE'),
            CONST.__getattribute__('DEPLOY_SCENARIO'),
            pkg_resources.resource_filename('functest', 'ci/testcases.yaml'))

    @staticmethod
    def source_rc_file():
        rc_file = CONST.__getattribute__('openstack_creds')
        if not os.path.isfile(rc_file):
            raise Exception("RC file %s does not exist..." % rc_file)
        logger.debug("Sourcing the OpenStack RC file...")
        os_utils.source_credentials(rc_file)
        for key, value in six.iteritems(os.environ):
            if re.search("OS_", key):
                if key == 'OS_AUTH_URL':
                    CONST.__setattr__('OS_AUTH_URL', value)
                elif key == 'OS_USERNAME':
                    CONST.__setattr__('OS_USERNAME', value)
                elif key == 'OS_TENANT_NAME':
                    CONST.__setattr__('OS_TENANT_NAME', value)
                elif key == 'OS_PASSWORD':
                    CONST.__setattr__('OS_PASSWORD', value)
                elif key == "OS_PROJECT_DOMAIN_NAME":
                    CONST.__setattr__('OS_PROJECT_DOMAIN_NAME', value)

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

    def run_test(self, test):
        if not test.is_enabled():
            raise TestNotEnabled(
                "The test case {} is not enabled".format(test.get_name()))
        logger.info("Running test case '%s'...", test.get_name())
        result = testcase.TestCase.EX_RUN_ERROR
        run_dict = self.get_run_dict(test.get_name())
        if run_dict:
            try:
                module = importlib.import_module(run_dict['module'])
                cls = getattr(module, run_dict['class'])
                test_dict = ft_utils.get_dict_by_test(test.get_name())
                test_case = cls(**test_dict)
                self.executed_test_cases[test.get_name()] = test_case
                if self.clean_flag:
                    if test_case.create_snapshot() != test_case.EX_OK:
                        return testcase.TestCase.EX_RUN_ERROR
                try:
                    kwargs = run_dict['args']
                    test_case.run(**kwargs)
                except KeyError:
                    test_case.run()
                if self.report_flag:
                    test_case.push_to_db()
                if test.get_project() == "functest":
                    result = test_case.is_successful()
                else:
                    result = testcase.TestCase.EX_OK
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
            self.overall_result = Result.EX_ERROR
        else:
            logger.info("Running tier '%s'" % tier_name)
            for test in tests:
                self.run_test(test)
                test_case = self.executed_test_cases[test.get_name()]
                if test_case.is_successful() != testcase.TestCase.EX_OK:
                    logger.error("The test case '%s' failed.", test.get_name())
                    if test.get_project() == "functest":
                        self.overall_result = Result.EX_ERROR
                    if test.is_blocking():
                        raise BlockingTestFailed(
                            "The test case {} failed and is blocking".format(
                                test.get_name()))
        return self.overall_result

    def run_all(self):
        tiers_to_run = []
        msg = prettytable.PrettyTable(
            header_style='upper', padding_width=5,
            field_names=['tiers', 'order', 'CI Loop', 'description',
                         'testcases'])
        for tier in self._tiers.get_tiers():
            if (len(tier.get_tests()) != 0 and
                    re.search(CONST.__getattribute__('CI_LOOP'),
                              tier.get_ci_loop()) is not None):
                tiers_to_run.append(tier)
                msg.add_row([tier.get_name(), tier.get_order(),
                             tier.get_ci_loop(),
                             textwrap.fill(tier.description, width=40),
                             textwrap.fill(' '.join([str(x.get_name(
                                 )) for x in tier.get_tests()]), width=40)])
        logger.info("TESTS TO BE EXECUTED:\n\n%s\n", msg)
        for tier in tiers_to_run:
            self.run_tier(tier)

    def main(self, **kwargs):
        if 'noclean' in kwargs:
            self.clean_flag = not kwargs['noclean']
        if 'report' in kwargs:
            self.report_flag = kwargs['report']
        try:
            if 'test' in kwargs:
                self.source_rc_file()
                logger.debug("Test args: %s", kwargs['test'])
                if self._tiers.get_tier(kwargs['test']):
                    self.run_tier(self._tiers.get_tier(kwargs['test']))
                elif self._tiers.get_test(kwargs['test']):
                    result = self.run_test(
                        self._tiers.get_test(kwargs['test']))
                    if result != testcase.TestCase.EX_OK:
                        logger.error("The test case '%s' failed.",
                                     kwargs['test'])
                        self.overall_result = Result.EX_ERROR
                elif kwargs['test'] == "all":
                    self.run_all()
                else:
                    logger.error("Unknown test case or tier '%s', "
                                 "or not supported by "
                                 "the given scenario '%s'."
                                 % (kwargs['test'],
                                    CONST.__getattribute__('DEPLOY_SCENARIO')))
                    logger.debug("Available tiers are:\n\n%s",
                                 self._tiers)
                    return Result.EX_ERROR
            else:
                self.run_all()
        except BlockingTestFailed:
            pass
        except Exception:
            logger.exception("Failures when running testcase(s)")
            self.overall_result = Result.EX_ERROR
        if not self._tiers.get_test(kwargs['test']):
            self.summary(self._tiers.get_tier(kwargs['test']))
        logger.info("Execution exit value: %s" % self.overall_result)
        return self.overall_result

    def summary(self, tier=None):
        msg = prettytable.PrettyTable(
            header_style='upper', padding_width=5,
            field_names=['env var', 'value'])
        for env_var in ['INSTALLER_TYPE', 'DEPLOY_SCENARIO', 'BUILD_TAG',
                        'CI_LOOP']:
            msg.add_row([env_var, CONST.__getattribute__(env_var)])
        logger.info("Deployment description:\n\n%s\n", msg)
        msg = prettytable.PrettyTable(
            header_style='upper', padding_width=5,
            field_names=['test case', 'project', 'tier',
                         'duration', 'result'])
        tiers = [tier] if tier else self._tiers.get_tiers()
        for tier in tiers:
            for test in tier.get_tests():
                try:
                    test_case = self.executed_test_cases[test.get_name()]
                except KeyError:
                    msg.add_row([test.get_name(), test.get_project(),
                                 tier.get_name(), "00:00", "SKIP"])
                else:
                    result = 'PASS' if(test_case.is_successful(
                        ) == test_case.EX_OK) else 'FAIL'
                    msg.add_row(
                        [test_case.case_name, test_case.project_name,
                         self._tiers.get_tier_name(test_case.case_name),
                         test_case.get_duration(), result])
            for test in tier.get_skipped_test():
                msg.add_row([test.get_name(), test.get_project(),
                             tier.get_name(), "00:00", "SKIP"])
        logger.info("FUNCTEST REPORT:\n\n%s\n", msg)


def main():
    logging.config.fileConfig(pkg_resources.resource_filename(
        'functest', 'ci/logging.ini'))
    logging.captureWarnings(True)
    parser = RunTestsParser()
    args = parser.parse_args(sys.argv[1:])
    runner = Runner()
    return runner.main(**args).value
