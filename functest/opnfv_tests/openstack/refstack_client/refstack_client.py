#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Refstack client testcase implemenation."""

from __future__ import division

import argparse
import logging
import os
import re
import sys
import subprocess
import time

import pkg_resources

from functest.core import testcase
from functest.energy import energy
from functest.opnfv_tests.openstack.refstack_client.tempest_conf \
    import TempestConf
from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils import constants
from functest.utils import functest_utils


__author__ = ("Matthew Li <matthew.lijun@huawei.com>,"
              "Linda Wang <wangwulin@huawei.com>")

# logging configuration """
LOGGER = logging.getLogger(__name__)


class RefstackClient(testcase.TestCase):
    """RefstackClient testcase implementation class."""
    # pylint: disable=too-many-instance-attributes

    def __init__(self, **kwargs):
        """Initialize RefstackClient testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "refstack_defcore"
        super(RefstackClient, self).__init__(**kwargs)
        self.resdir = os.path.join(
            getattr(constants.CONST, 'dir_results'), 'refstack')
        self.conf_path = os.path.join(self.resdir, 'refstack_tempest.conf')
        self.tempestconf = TempestConf()
        self.defcorelist = os.path.join(
            getattr(constants.CONST, 'dir_refstack_data'), 'defcore.txt')
        self.testlist = None
        self.insecure = ''
        if ('https' in os.environ['OS_AUTH_URL'] and
                os.getenv('OS_INSECURE', '').lower() == 'true'):
            self.insecure = '-k'

    def run_defcore(self, conf, testlist):
        """Run defcore sys command."""
        cmd = ("refstack-client test {0} -c {1} -v --test-list {2}"
               .format(self.insecure, conf, testlist))
        LOGGER.info("Starting Refstack_defcore test case: '%s'.", cmd)
        functest_utils.execute_command(cmd)

    def run_defcore_default(self):
        """Run default defcore sys command."""
        options = ["-v"] if not self.insecure else ["-v", self.insecure]
        cmd = (["refstack-client", "test", "-c", self.conf_path] +
               options + ["--test-list", self.defcorelist])
        LOGGER.info("Starting Refstack_defcore test case: '%s'.", cmd)

        with open(os.path.join(self.resdir, "refstack.log"), 'w+') as f_stdout:
            subprocess.call(cmd, shell=False, stdout=f_stdout,
                            stderr=subprocess.STDOUT)

    def parse_refstack_result(self):
        """Parse Refstack results."""
        try:
            with open(os.path.join(self.resdir,
                                   "refstack.log"), 'r') as logfile:
                for line in logfile.readlines():
                    if 'Tests' in line:
                        break
                    if re.search(r"\} tempest\.", line):
                        LOGGER.info(line.replace('\n', ''))

            with open(os.path.join(self.resdir,
                                   "refstack.log"), 'r') as logfile:
                output = logfile.read()

            for match in re.findall(r"Ran: (\d+) tests in (\d+\.\d{4}) sec.",
                                    output):
                num_tests = match[0]
                LOGGER.info("Ran: %s tests in %s sec.", num_tests, match[1])
            for match in re.findall(r"(- Passed: )(\d+)", output):
                num_success = match[1]
                LOGGER.info("".join(match))
            for match in re.findall(r"(- Skipped: )(\d+)", output):
                num_skipped = match[1]
                LOGGER.info("".join(match))
            for match in re.findall(r"(- Failed: )(\d+)", output):
                num_failures = match[1]
                LOGGER.info("".join(match))
            success_testcases = []
            for match in re.findall(r"\{0\} (.*?) \.{3} ok", output):
                success_testcases.append(match)
            failed_testcases = []
            for match in re.findall(r"\{0\} (.*?) \.{3} FAILED", output):
                failed_testcases.append(match)
            skipped_testcases = []
            for match in re.findall(r"\{0\} (.*?) \.{3} SKIPPED:", output):
                skipped_testcases.append(match)

            num_executed = int(num_tests) - int(num_skipped)

            try:
                self.result = 100 * int(num_success) / int(num_executed)
            except ZeroDivisionError:
                LOGGER.error("No test has been executed")

            self.details = {"tests": int(num_tests),
                            "failures": int(num_failures),
                            "success": success_testcases,
                            "errors": failed_testcases,
                            "skipped": skipped_testcases}
        except Exception:  # pylint: disable=broad-except
            self.result = 0

        LOGGER.info("Testcase %s success_rate is %s%%",
                    self.case_name, self.result)

    @energy.enable_recording
    def run(self, **kwargs):
        """
        Start RefstackClient testcase.

        used for functest command line,
        functest testcase run refstack_defcore
        """
        self.start_time = time.time()

        try:
            # Make sure that Tempest is configured
            if not self.conf_path:
                tempestconf = TempestConf()
                tempestconf.main()
            self.run_defcore_default()
            self.parse_refstack_result()
            res = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            LOGGER.exception("Error with run")
            res = testcase.TestCase.EX_RUN_ERROR
        finally:
            self.tempestconf.clean()

        self.stop_time = time.time()
        return res

    def _prep_test(self):
        """Check that the config file exists."""
        if not os.path.isfile(self.conf_path):
            LOGGER.error("Conf file not valid: %s", self.conf_path)
        if not os.path.isfile(self.testlist):
            LOGGER.error("testlist file not valid: %s", self.testlist)

    def main(self, **kwargs):
        """
        Execute RefstackClient testcase manually.

        used for manually running,
           python refstack_client.py -c <tempest_conf_path>
           --testlist <testlist_path>
           can generate a reference refstack_tempest.conf by
           python tempest_conf.py
        """
        try:
            conf_path = kwargs['config']
            defcorelist = kwargs['testlist']
        except KeyError as exc:
            LOGGER.error("Cannot run refstack client. Please check "
                         "%s", exc)
            return self.EX_RUN_ERROR
        try:
            self._prep_test()
            self.run_defcore(conf_path, defcorelist)
            res = testcase.TestCase.EX_OK
        except Exception as exc:  # pylint: disable=broad-except
            LOGGER.error('Error with run: %s', exc)
            res = testcase.TestCase.EX_RUN_ERROR

        return res


class RefstackClientParser(object):  # pylint: disable=too-few-public-methods
    """Command line argument parser helper."""

    def __init__(self):
        """Initialize helper object."""
        self.functest_test = pkg_resources.resource_filename(
            'functest', 'opnfv_tests')
        self.conf_path = pkg_resources.resource_filename(
            'functest',
            'opnfv_tests/openstack/refstack_client/refstack_tempest.conf')
        self.defcore_list = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/openstack/refstack_client/defcore.txt')
        self.confpath = os.path.join(self.functest_test,
                                     self.conf_path)
        self.defcorelist = os.path.join(self.functest_test,
                                        self.defcore_list)
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-c', '--config',
            help='the file path of refstack_tempest.conf',
            default=self.confpath)
        self.parser.add_argument(
            '-t', '--testlist',
            help='Specify the file path or URL of a test list text file. '
                 'This test list will contain specific test cases that '
                 'should be tested.',
            default=self.defcorelist)

    def parse_args(self, argv=None):
        """Parse command line arguments."""
        return vars(self.parser.parse_args(argv))


def main():
    """Run RefstackClient testcase with CLI."""
    logging.basicConfig()
    refstackclient = RefstackClient()
    parser = RefstackClientParser()
    args = parser.parse_args(sys.argv[1:])
    try:
        result = refstackclient.main(**args)
        if result != testcase.TestCase.EX_OK:
            return result
    except Exception:  # pylint: disable=broad-except
        return testcase.TestCase.EX_RUN_ERROR
