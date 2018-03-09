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
import ConfigParser
import logging
import os
import re
import sys
import subprocess
import time

from xtesting.core import testcase
from xtesting.energy import energy

from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.opnfv_tests.openstack.tempest import tempest
from functest.utils import config
from functest.utils import functest_utils


__author__ = ("Matthew Li <matthew.lijun@huawei.com>,"
              "Linda Wang <wangwulin@huawei.com>")

# logging configuration """
LOGGER = logging.getLogger(__name__)


class RefstackClient(testcase.TestCase):
    """RefstackClient testcase implementation class."""
    # pylint: disable=too-many-instance-attributes

    defcorelist = os.path.join(
        getattr(config.CONF, 'dir_refstack_data'), 'defcore.txt')

    def __init__(self, **kwargs):
        """Initialize RefstackClient testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "refstack_defcore"
        super(RefstackClient, self).__init__(**kwargs)
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), 'refstack')
        self.conf_path = os.path.join(self.res_dir, 'refstack_tempest.conf')

    @staticmethod
    def run_defcore(conf, testlist):
        """Run defcore sys command."""
        insecure = ''
        if ('https' in os.environ['OS_AUTH_URL'] and
                os.getenv('OS_INSECURE', '').lower() == 'true'):
            insecure = '-k'
        cmd = ("refstack-client test {0} -c {1} -v --test-list {2}"
               .format(insecure, conf, testlist))
        LOGGER.info("Starting Refstack_defcore test case: '%s'.", cmd)
        functest_utils.execute_command(cmd)

    def run_defcore_default(self):
        """Run default defcore sys command."""
        insecure = ''
        if ('https' in os.environ['OS_AUTH_URL'] and
                os.getenv('OS_INSECURE', '').lower() == 'true'):
            insecure = '-k'
        options = ["-v"] if not insecure else ["-v", insecure]
        cmd = (["refstack-client", "test", "-c", self.conf_path] +
               options + ["--test-list", self.defcorelist])
        LOGGER.info("Starting Refstack_defcore test case: '%s'.", cmd)
        with open(os.path.join(self.res_dir, "refstack.log"), 'w+') as fstdout:
            subprocess.call(cmd, shell=False, stdout=fstdout,
                            stderr=subprocess.STDOUT)

    def parse_refstack_result(self):
        """Parse Refstack results."""
        try:
            with open(os.path.join(self.res_dir,
                                   "refstack.log"), 'r') as logfile:
                for line in logfile.readlines():
                    if 'Tests' in line:
                        break
                    if re.search(r"\} tempest\.", line):
                        LOGGER.info(line.replace('\n', ''))

            with open(os.path.join(self.res_dir,
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

    def configure_tempest_defcore(self):
        # pylint: disable=too-many-arguments
        """
        Add/update needed parameters into tempest.conf file
        """
        resources = tempest.TempestResourcesManager().create(
            create_project=True, use_custom_images=True,
            use_custom_flavors=True)
        verifier_id = conf_utils.get_verifier_id()
        deployment_id = conf_utils.get_verifier_deployment_id()
        deployment_dir = conf_utils.get_verifier_deployment_dir(
            verifier_id, deployment_id)
        conf_file = conf_utils.configure_verifier(deployment_dir)
        conf_utils.configure_tempest_update_params(
            conf_file, self.res_dir, resources.get("network_name"),
            resources.get("image_id"), resources.get("flavor_id"))
        LOGGER.debug(
            "Updating selected tempest.conf parameters for defcore...")
        rconfig = ConfigParser.RawConfigParser()
        rconfig.read(conf_file)
        rconfig.set(
            'DEFAULT', 'log_file', '{}/tempest.log'.format(deployment_dir))
        rconfig.set('oslo_concurrency', 'lock_path',
                    '{}/lock_files'.format(deployment_dir))
        conf_utils.generate_test_accounts_file(
            tenant_id=resources.get("project_id"))
        rconfig.set('auth', 'test_accounts_file',
                    conf_utils.TEST_ACCOUNTS_FILE)
        rconfig.set('scenario', 'img_dir', '{}'.format(deployment_dir))
        rconfig.set('scenario', 'img_file', 'tempest-image')
        rconfig.set('compute', 'image_ref', resources.get("image_id"))
        rconfig.set('compute', 'image_ref_alt', resources.get("image_id_alt"))
        rconfig.set('compute', 'flavor_ref', resources.get("flavor_id"))
        rconfig.set('compute', 'flavor_ref_alt',
                    resources.get("flavor_id_alt"))
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)
        with open(self.conf_path, 'w') as config_fd:
            rconfig.write(config_fd)

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
            self.configure_tempest_defcore()
            self.run_defcore_default()
            self.parse_refstack_result()
            res = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            LOGGER.exception("Error with run")
            res = testcase.TestCase.EX_RUN_ERROR
        self.stop_time = time.time()
        return res

    @staticmethod
    def main(**kwargs):
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
            if not os.path.isfile(conf_path):
                LOGGER.error("Conf file not valid: %s", conf_path)
                return testcase.TestCase.EX_RUN_ERROR
            testlist = kwargs['testlist']
            if not os.path.isfile(testlist):
                LOGGER.error("testlist file not valid: %s", testlist)
                return testcase.TestCase.EX_RUN_ERROR
        except KeyError as exc:
            LOGGER.error("Cannot run refstack client. Please check "
                         "%s", exc)
            return testcase.TestCase.EX_RUN_ERROR
        try:
            RefstackClient.run_defcore(conf_path, testlist)
        except Exception as exc:  # pylint: disable=broad-except
            LOGGER.error('Error with run: %s', exc)
            return testcase.TestCase.EX_RUN_ERROR
        return testcase.TestCase.EX_OK


class RefstackClientParser(object):  # pylint: disable=too-few-public-methods
    """Command line argument parser helper."""

    def __init__(self):
        """Initialize helper object."""
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-c', '--config',
            help='the file path of refstack_tempest.conf')
        self.parser.add_argument(
            '-t', '--testlist',
            help='Specify the file path or URL of a test list text file. '
                 'This test list will contain specific test cases that '
                 'should be tested.',
            default=RefstackClient.defcorelist)

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
