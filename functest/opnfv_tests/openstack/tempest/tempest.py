#!/usr/bin/env python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

"""Tempest testcases implementation."""

from __future__ import division

import logging
import os
import re
import shutil
import subprocess
import time

from six.moves import configparser
from xtesting.core import testcase
import yaml

from functest.core import singlevm
from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils import config
from functest.utils import env

LOGGER = logging.getLogger(__name__)


class TempestCommon(singlevm.VmReady1):
    # pylint: disable=too-many-instance-attributes
    """TempestCommon testcases implementation class."""

    TEMPEST_RESULTS_DIR = os.path.join(
        getattr(config.CONF, 'dir_results'), 'tempest')

    def __init__(self, **kwargs):
        super(TempestCommon, self).__init__(**kwargs)
        self.mode = ""
        self.option = []
        self.verifier_id = conf_utils.get_verifier_id()
        self.verifier_repo_dir = conf_utils.get_verifier_repo_dir(
            self.verifier_id)
        self.deployment_id = conf_utils.get_verifier_deployment_id()
        self.deployment_dir = conf_utils.get_verifier_deployment_dir(
            self.verifier_id, self.deployment_id)
        self.verification_id = None
        self.res_dir = TempestCommon.TEMPEST_RESULTS_DIR
        self.raw_list = os.path.join(self.res_dir, 'test_raw_list.txt')
        self.list = os.path.join(self.res_dir, 'test_list.txt')
        self.conf_file = None
        self.image_alt = None
        self.flavor_alt = None

    @staticmethod
    def read_file(filename):
        """Read file and return content as a stripped list."""
        with open(filename) as src:
            return [line.strip() for line in src.readlines()]

    @staticmethod
    def get_verifier_result(verif_id):
        """Retrieve verification results."""
        result = {
            'num_tests': 0,
            'num_success': 0,
            'num_failures': 0,
            'num_skipped': 0
        }
        cmd = ["rally", "verify", "show", "--uuid", verif_id]
        LOGGER.info("Showing result for a verification: '%s'.", cmd)
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        for line in proc.stdout:
            new_line = line.replace(' ', '').split('|')
            if 'Tests' in new_line:
                break
            LOGGER.info(line)
            if 'Testscount' in new_line:
                result['num_tests'] = int(new_line[2])
            elif 'Success' in new_line:
                result['num_success'] = int(new_line[2])
            elif 'Skipped' in new_line:
                result['num_skipped'] = int(new_line[2])
            elif 'Failures' in new_line:
                result['num_failures'] = int(new_line[2])
        return result

    @staticmethod
    def backup_tempest_config(conf_file, res_dir):
        """
        Copy config file to tempest results directory
        """
        if not os.path.exists(res_dir):
            os.makedirs(res_dir)
        shutil.copyfile(conf_file,
                        os.path.join(res_dir, 'tempest.conf'))

    def generate_test_list(self):
        """Generate test list based on the test mode."""
        LOGGER.debug("Generating test case list...")
        self.backup_tempest_config(self.conf_file, '/etc')
        if self.mode == 'custom':
            if os.path.isfile(conf_utils.TEMPEST_CUSTOM):
                shutil.copyfile(
                    conf_utils.TEMPEST_CUSTOM, self.list)
            else:
                raise Exception("Tempest test list file %s NOT found."
                                % conf_utils.TEMPEST_CUSTOM)
        else:
            if self.mode == 'smoke':
                testr_mode = r"'^tempest\.(api|scenario).*\[.*\bsmoke\b.*\]$'"
            elif self.mode == 'full':
                testr_mode = r"'^tempest\.'"
            else:
                testr_mode = self.mode
            cmd = "(cd {0}; stestr list {1} >{2} 2>/dev/null)".format(
                self.verifier_repo_dir, testr_mode, self.list)
            output = subprocess.check_output(cmd, shell=True)
            LOGGER.info("%s\n%s", cmd, output)
        os.remove('/etc/tempest.conf')

    def apply_tempest_blacklist(self):
        """Exclude blacklisted test cases."""
        LOGGER.debug("Applying tempest blacklist...")
        if os.path.exists(self.raw_list):
            os.remove(self.raw_list)
        os.rename(self.list, self.raw_list)
        cases_file = self.read_file(self.raw_list)
        result_file = open(self.list, 'w')
        black_tests = []
        try:
            installer_type = env.get('INSTALLER_TYPE')
            deploy_scenario = env.get('DEPLOY_SCENARIO')
            if bool(installer_type) * bool(deploy_scenario):
                # if INSTALLER_TYPE and DEPLOY_SCENARIO are set we read the
                # file
                black_list_file = open(conf_utils.TEMPEST_BLACKLIST)
                black_list_yaml = yaml.safe_load(black_list_file)
                black_list_file.close()
                for item in black_list_yaml:
                    scenarios = item['scenarios']
                    installers = item['installers']
                    if (deploy_scenario in scenarios and
                            installer_type in installers):
                        tests = item['tests']
                        for test in tests:
                            black_tests.append(test)
                        break
        except Exception:  # pylint: disable=broad-except
            black_tests = []
            LOGGER.debug("Tempest blacklist file does not exist.")

        for cases_line in cases_file:
            for black_tests_line in black_tests:
                if black_tests_line in cases_line:
                    break
            else:
                result_file.write(str(cases_line) + '\n')
        result_file.close()

    def run_verifier_tests(self):
        """Execute tempest test cases."""
        cmd = ["rally", "verify", "start", "--load-list",
               self.list]
        cmd.extend(self.option)
        LOGGER.info("Starting Tempest test suite: '%s'.", cmd)

        f_stdout = open(
            os.path.join(self.res_dir, "tempest.log"), 'w+')
        f_stderr = open(
            os.path.join(self.res_dir,
                         "tempest-error.log"), 'w+')

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=f_stderr,
            bufsize=1)

        with proc.stdout:
            for line in iter(proc.stdout.readline, b''):
                if re.search(r"\} tempest\.", line):
                    LOGGER.info(line.replace('\n', ''))
                elif re.search(r'(?=\(UUID=(.*)\))', line):
                    self.verification_id = re.search(
                        r'(?=\(UUID=(.*)\))', line).group(1)
                    LOGGER.info('Verification UUID: %s', self.verification_id)
                f_stdout.write(line)
        proc.wait()

        f_stdout.close()
        f_stderr.close()

        if self.verification_id is None:
            raise Exception('Verification UUID not found')

    def parse_verifier_result(self):
        """Parse and save test results."""
        stat = self.get_verifier_result(self.verification_id)
        try:
            num_executed = stat['num_tests'] - stat['num_skipped']
            try:
                self.result = 100 * stat['num_success'] / num_executed
            except ZeroDivisionError:
                self.result = 0
                if stat['num_tests'] > 0:
                    LOGGER.info("All tests have been skipped")
                else:
                    LOGGER.error("No test has been executed")
                    return

            with open(os.path.join(self.res_dir,
                                   "tempest-error.log"), 'r') as logfile:
                output = logfile.read()

            success_testcases = []
            for match in re.findall(r'.*\{\d{1,2}\} (.*?) \.{3} success ',
                                    output):
                success_testcases.append(match)
            failed_testcases = []
            for match in re.findall(r'.*\{\d{1,2}\} (.*?) \.{3} fail',
                                    output):
                failed_testcases.append(match)
            skipped_testcases = []
            for match in re.findall(r'.*\{\d{1,2}\} (.*?) \.{3} skip:',
                                    output):
                skipped_testcases.append(match)

            self.details = {"tests_number": stat['num_tests'],
                            "success_number": stat['num_success'],
                            "skipped_number": stat['num_skipped'],
                            "failures_number": stat['num_failures'],
                            "success": success_testcases,
                            "skipped": skipped_testcases,
                            "failures": failed_testcases}
        except Exception:  # pylint: disable=broad-except
            self.result = 0

        LOGGER.info("Tempest %s success_rate is %s%%",
                    self.case_name, self.result)

    def generate_report(self):
        """Generate verification report."""
        html_file = os.path.join(self.res_dir,
                                 "tempest-report.html")
        cmd = ["rally", "verify", "report", "--type", "html", "--uuid",
               self.verification_id, "--to", html_file]
        subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    def configure(self, **kwargs):  # pylint: disable=unused-argument
        """
        Create all openstack resources for tempest-based testcases and write
        tempest.conf.
        """
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)
        compute_cnt = len(self.cloud.list_hypervisors())

        LOGGER.info("Creating two images for Tempest suite")

        meta = getattr(
            config.CONF, '{}_extra_properties'.format(self.case_name), None)
        self.image_alt = self.cloud.create_image(
            '{}-img_alt_{}'.format(self.case_name, self.guid),
            filename=getattr(
                config.CONF, '{}_image'.format(self.case_name),
                self.filename),
            meta=meta)
        LOGGER.debug("image_alt: %s", self.image_alt)

        self.flavor_alt = self.orig_cloud.create_flavor(
            '{}-flavor_alt_{}'.format(self.case_name, self.guid),
            getattr(config.CONF, '{}_flavor_ram'.format(self.case_name),
                    self.flavor_ram),
            getattr(config.CONF, '{}_flavor_vcpus'.format(self.case_name),
                    self.flavor_vcpus),
            getattr(config.CONF, '{}_flavor_disk'.format(self.case_name),
                    self.flavor_disk))
        LOGGER.debug("flavor: %s", self.flavor_alt)
        self.orig_cloud.set_flavor_specs(
            self.flavor_alt.id, getattr(config.CONF, 'flavor_extra_specs', {}))

        self.conf_file = conf_utils.configure_verifier(self.deployment_dir)
        conf_utils.configure_tempest_update_params(
            self.conf_file, network_name=self.network.id,
            image_id=self.image.id,
            flavor_id=self.flavor.id,
            compute_cnt=compute_cnt,
            image_alt_id=self.image_alt.id,
            flavor_alt_id=self.flavor_alt.id)
        self.backup_tempest_config(self.conf_file, self.res_dir)

    def run(self, **kwargs):
        self.start_time = time.time()
        try:
            super(TempestCommon, self).run(**kwargs)
            self.configure(**kwargs)
            self.generate_test_list()
            self.apply_tempest_blacklist()
            self.run_verifier_tests()
            self.parse_verifier_result()
            self.generate_report()
            res = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            LOGGER.exception('Error with run')
            res = testcase.TestCase.EX_RUN_ERROR
        self.stop_time = time.time()
        return res

    def clean(self):
        """
        Cleanup all OpenStack objects. Should be called on completion.
        """
        super(TempestCommon, self).clean()
        self.cloud.delete_image(self.image_alt)
        self.orig_cloud.delete_flavor(self.flavor_alt.id)


class TempestSmokeSerial(TempestCommon):
    """Tempest smoke serial testcase implementation."""
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest_smoke_serial'
        TempestCommon.__init__(self, **kwargs)
        self.mode = "smoke"
        self.option = ["--concurrency", "1"]


class TempestNeutronTrunk(TempestCommon):
    """Tempest neutron trunk testcase implementation."""
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'neutron_trunk'
        TempestCommon.__init__(self, **kwargs)
        self.mode = "'neutron_tempest_plugin.(api|scenario).test_trunk'"
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), 'neutron_trunk')
        self.raw_list = os.path.join(self.res_dir, 'test_raw_list.txt')
        self.list = os.path.join(self.res_dir, 'test_list.txt')

    def configure(self, **kwargs):
        super(TempestNeutronTrunk, self).configure(**kwargs)
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        rconfig.set('network-feature-enabled', 'api_extensions', 'all')
        with open(self.conf_file, 'wb') as config_file:
            rconfig.write(config_file)


class TempestBarbican(TempestCommon):
    """Tempest Barbican testcase implementation."""
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'barbican'
        TempestCommon.__init__(self, **kwargs)
        self.mode = "'barbican_tempest_plugin.tests.(api|scenario)'"
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), 'barbican')
        self.raw_list = os.path.join(self.res_dir, 'test_raw_list.txt')
        self.list = os.path.join(self.res_dir, 'test_list.txt')


class TempestSmokeParallel(TempestCommon):
    """Tempest smoke parallel testcase implementation."""
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest_smoke_parallel'
        TempestCommon.__init__(self, **kwargs)
        self.mode = "smoke"


class TempestFullParallel(TempestCommon):
    """Tempest full parallel testcase implementation."""
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest_full_parallel'
        TempestCommon.__init__(self, **kwargs)
        self.mode = "full"


class TempestCustom(TempestCommon):
    """Tempest custom testcase implementation."""
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest_custom'
        TempestCommon.__init__(self, **kwargs)
        self.mode = "custom"
        self.option = ["--concurrency", "1"]


class TempestDefcore(TempestCommon):
    """Tempest Defcore testcase implementation."""
    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest_defcore'
        TempestCommon.__init__(self, **kwargs)
        self.mode = "defcore"
        self.option = ["--concurrency", "1"]
