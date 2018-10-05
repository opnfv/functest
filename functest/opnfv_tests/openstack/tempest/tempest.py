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


class TempestCommon(singlevm.VmReady2):
    # pylint: disable=too-many-instance-attributes
    """TempestCommon testcases implementation class."""

    visibility = 'public'
    shared_network = True
    filename_alt = '/home/opnfv/functest/images/cirros-0.4.0-x86_64-disk.img'

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest'
        super(TempestCommon, self).__init__(**kwargs)
        assert self.orig_cloud
        assert self.cloud
        assert self.project
        if self.orig_cloud.get_role("admin"):
            role_name = "admin"
        elif self.orig_cloud.get_role("Admin"):
            role_name = "Admin"
        else:
            raise Exception("Cannot detect neither admin nor Admin")
        self.orig_cloud.grant_role(
            role_name, user=self.project.user.id,
            project=self.project.project.id,
            domain=self.project.domain.id)
        environ = dict(
            os.environ,
            OS_USERNAME=self.project.user.name,
            OS_PROJECT_NAME=self.project.project.name,
            OS_PROJECT_ID=self.project.project.id,
            OS_PASSWORD=self.project.password)
        conf_utils.create_rally_deployment(environ=environ)
        conf_utils.create_verifier()
        self.verifier_id = conf_utils.get_verifier_id()
        self.verifier_repo_dir = conf_utils.get_verifier_repo_dir(
            self.verifier_id)
        self.deployment_id = conf_utils.get_verifier_deployment_id()
        self.deployment_dir = conf_utils.get_verifier_deployment_dir(
            self.verifier_id, self.deployment_id)
        self.verification_id = None
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), self.case_name)
        self.raw_list = os.path.join(self.res_dir, 'test_raw_list.txt')
        self.list = os.path.join(self.res_dir, 'test_list.txt')
        self.conf_file = None
        self.image_alt = None
        self.flavor_alt = None
        self.services = []
        try:
            self.services = kwargs['run']['args']['services']
        except Exception:  # pylint: disable=broad-except
            pass
        self.neutron_extensions = []
        try:
            self.neutron_extensions = kwargs['run']['args'][
                'neutron_extensions']
        except Exception:  # pylint: disable=broad-except
            pass

    def check_services(self):
        """Check the mandatory services."""
        for service in self.services:
            try:
                self.cloud.search_services(service)[0]
            except Exception:  # pylint: disable=broad-except
                self.is_skipped = True
                break

    def check_extensions(self):
        """Check the mandatory network extensions."""
        extensions = self.cloud.get_network_extensions()
        for network_extension in self.neutron_extensions:
            if network_extension not in extensions:
                LOGGER.warning(
                    "Cannot find Neutron extension: %s", network_extension)
                self.is_skipped = True
                break

    def check_requirements(self):
        self.check_services()
        self.check_extensions()

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
            LOGGER.info(line.rstrip())
            new_line = line.replace(' ', '').split('|')
            if 'Tests' in new_line:
                break
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

    def generate_test_list(self, **kwargs):
        """Generate test list based on the test mode."""
        LOGGER.debug("Generating test case list...")
        self.backup_tempest_config(self.conf_file, '/etc')
        if kwargs.get('mode') == 'custom':
            if os.path.isfile(conf_utils.TEMPEST_CUSTOM):
                shutil.copyfile(
                    conf_utils.TEMPEST_CUSTOM, self.list)
            else:
                raise Exception("Tempest test list file %s NOT found."
                                % conf_utils.TEMPEST_CUSTOM)
        else:
            testr_mode = kwargs.get(
                'mode', r'^tempest\.(api|scenario).*\[.*\bsmoke\b.*\]$')
            cmd = "(cd {0}; stestr list '{1}' >{2} 2>/dev/null)".format(
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
            deploy_scenario = env.get('DEPLOY_SCENARIO')
            if bool(deploy_scenario):
                # if DEPLOY_SCENARIO is set we read the file
                black_list_file = open(conf_utils.TEMPEST_BLACKLIST)
                black_list_yaml = yaml.safe_load(black_list_file)
                black_list_file.close()
                for item in black_list_yaml:
                    scenarios = item['scenarios']
                    if deploy_scenario in scenarios:
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

    def run_verifier_tests(self, **kwargs):
        """Execute tempest test cases."""
        cmd = ["rally", "verify", "start", "--load-list",
               self.list]
        cmd.extend(kwargs.get('option', []))
        LOGGER.info("Starting Tempest test suite: '%s'.", cmd)

        f_stdout = open(
            os.path.join(self.res_dir, "tempest.log"), 'w+')

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1)

        with proc.stdout:
            for line in iter(proc.stdout.readline, b''):
                if re.search(r"\} tempest\.", line):
                    LOGGER.info(line.rstrip())
                elif re.search(r'(?=\(UUID=(.*)\))', line):
                    self.verification_id = re.search(
                        r'(?=\(UUID=(.*)\))', line).group(1)
                f_stdout.write(line)
        proc.wait()
        f_stdout.close()

        if self.verification_id is None:
            raise Exception('Verification UUID not found')
        LOGGER.info('Verification UUID: %s', self.verification_id)

        shutil.copy(
            "{}/tempest.log".format(self.deployment_dir),
            "{}/tempest.debug.log".format(self.res_dir))

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
                                   "tempest.log"), 'r') as logfile:
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

    def update_rally_regex(self, rally_conf='/etc/rally/rally.conf'):
        """Set image name as tempest img_name_regex"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(rally_conf)
        if not rconfig.has_section('openstack'):
            rconfig.add_section('openstack')
        rconfig.set('openstack', 'img_name_regex', '^{}$'.format(
            self.image.name))
        with open(rally_conf, 'wb') as config_file:
            rconfig.write(config_file)

    def update_default_role(self, rally_conf='/etc/rally/rally.conf'):
        """Detect and update the default role if required"""
        role = self.get_default_role(self.cloud)
        if not role:
            return
        rconfig = configparser.RawConfigParser()
        rconfig.read(rally_conf)
        if not rconfig.has_section('openstack'):
            rconfig.add_section('openstack')
        rconfig.set('openstack', 'swift_operator_role', role.name)
        with open(rally_conf, 'wb') as config_file:
            rconfig.write(config_file)

    def update_rally_logs(self, rally_conf='/etc/rally/rally.conf'):
        """Print rally logs in res dir"""
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)
        rconfig = configparser.RawConfigParser()
        rconfig.read(rally_conf)
        rconfig.set('DEFAULT', 'log-file', 'rally.log')
        rconfig.set('DEFAULT', 'log_dir', self.res_dir)
        with open(rally_conf, 'wb') as config_file:
            rconfig.write(config_file)

    @staticmethod
    def clean_rally_conf(rally_conf='/etc/rally/rally.conf'):
        """Clean Rally config"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(rally_conf)
        if rconfig.has_option('openstack', 'img_name_regex'):
            rconfig.remove_option('openstack', 'img_name_regex')
        if rconfig.has_option('openstack', 'swift_operator_role'):
            rconfig.remove_option('openstack', 'swift_operator_role')
        if rconfig.has_option('DEFAULT', 'log-file'):
            rconfig.remove_option('DEFAULT', 'log-file')
        if rconfig.has_option('DEFAULT', 'log_dir'):
            rconfig.remove_option('DEFAULT', 'log_dir')
        with open(rally_conf, 'wb') as config_file:
            rconfig.write(config_file)

    def update_scenario_section(self):
        """Update scenario section in tempest.conf"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        filename = getattr(
            config.CONF, '{}_image'.format(self.case_name), self.filename)
        if not rconfig.has_section('scenario'):
            rconfig.add_section('scenario')
        rconfig.set('scenario', 'img_file', os.path.basename(filename))
        rconfig.set('scenario', 'img_dir', os.path.dirname(filename))
        rconfig.set('scenario', 'img_disk_format', getattr(
            config.CONF, '{}_image_format'.format(self.case_name),
            self.image_format))
        extra_properties = self.extra_properties.copy()
        if env.get('IMG_PROP'):
            extra_properties.update(dict((k.strip(), v.strip()) for k, v in
                                         (item.split(': ') for item in
                                          env.get('IMG_PROP').split(','))))
        extra_properties.update(
            getattr(config.CONF, '{}_extra_properties'.format(
                self.case_name), {}))
        rconfig.set(
            'scenario', 'img_properties',
            conf_utils.convert_dict_to_ini(extra_properties))
        with open(self.conf_file, 'wb') as config_file:
            rconfig.write(config_file)

    def configure(self, **kwargs):  # pylint: disable=unused-argument
        """
        Create all openstack resources for tempest-based testcases and write
        tempest.conf.
        """
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)
        compute_cnt = len(self.cloud.list_hypervisors())

        self.image_alt = self.publish_image_alt()
        self.flavor_alt = self.create_flavor_alt()
        LOGGER.debug("flavor: %s", self.flavor_alt)

        self.conf_file = conf_utils.configure_verifier(self.deployment_dir)
        conf_utils.configure_tempest_update_params(
            self.conf_file, network_name=self.network.name,
            image_id=self.image.id,
            flavor_id=self.flavor.id,
            compute_cnt=compute_cnt,
            image_alt_id=self.image_alt.id,
            flavor_alt_id=self.flavor_alt.id,
            domain_name=self.cloud.auth.get("project_domain_name", "Default"))
        self.update_scenario_section()
        self.backup_tempest_config(self.conf_file, self.res_dir)

    def run(self, **kwargs):
        self.start_time = time.time()
        try:
            assert super(TempestCommon, self).run(
                **kwargs) == testcase.TestCase.EX_OK
            if not os.path.exists(self.res_dir):
                os.makedirs(self.res_dir)
            self.update_rally_regex()
            self.update_default_role()
            self.update_rally_logs()
            shutil.copy("/etc/rally/rally.conf", self.res_dir)
            self.configure(**kwargs)
            self.generate_test_list(**kwargs)
            self.apply_tempest_blacklist()
            self.run_verifier_tests(**kwargs)
            self.parse_verifier_result()
            self.generate_report()
            res = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            LOGGER.exception('Error with run')
            self.result = 0
            res = testcase.TestCase.EX_RUN_ERROR
        self.stop_time = time.time()
        return res

    def clean(self):
        """
        Cleanup all OpenStack objects. Should be called on completion.
        """
        self.clean_rally_conf()
        if self.image_alt:
            self.cloud.delete_image(self.image_alt)
        if self.flavor_alt:
            self.orig_cloud.delete_flavor(self.flavor_alt.id)
        super(TempestCommon, self).clean()
