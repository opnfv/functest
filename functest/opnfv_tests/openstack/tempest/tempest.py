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
import uuid

import os_client_config
from six.moves import configparser
from xtesting.core import testcase
import yaml

from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils import config
from functest.utils import env

LOGGER = logging.getLogger(__name__)


class TempestCommon(testcase.TestCase):
    # pylint: disable=too-many-instance-attributes
    """TempestCommon testcases implementation class."""

    TEMPEST_RESULTS_DIR = os.path.join(
        getattr(config.CONF, 'dir_results'), 'tempest')

    def __init__(self, **kwargs):
        super(TempestCommon, self).__init__(**kwargs)
        self.resources = TempestResourcesManager()
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
        self.resources.create()
        compute_cnt = len(self.resources.cloud.list_hypervisors())
        self.conf_file = conf_utils.configure_verifier(self.deployment_dir)
        conf_utils.configure_tempest_update_params(
            self.conf_file, network_name=self.resources.network.id,
            image_id=self.resources.image.id,
            flavor_id=self.resources.flavor.id,
            compute_cnt=compute_cnt,
            image_alt_id=self.resources.image_alt.id,
            flavor_alt_id=self.resources.flavor_alt.id)
        self.backup_tempest_config(self.conf_file, self.res_dir)

    def run(self, **kwargs):
        self.start_time = time.time()
        try:
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
        finally:
            self.resources.cleanup()
        self.stop_time = time.time()
        return res


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


class TempestResourcesManager(object):
    # pylint: disable=too-many-instance-attributes
    """Tempest resource manager."""
    def __init__(self):
        self.guid = '-' + str(uuid.uuid4())
        self.cloud = os_client_config.make_shade()
        LOGGER.debug("cloud: %s", self.cloud)
        self.domain = self.cloud.get_domain(
            name_or_id=self.cloud.auth.get(
                "project_domain_name", "Default"))
        LOGGER.debug("domain: %s", self.domain)
        self.project = None
        self.user = None
        self.network = None
        self.subnet = None
        self.image = None
        self.image_alt = None
        self.flavor = None
        self.flavor_alt = None

    def _create_project(self):
        """Create project for tests."""
        self.project = self.cloud.create_project(
            getattr(config.CONF, 'tempest_identity_tenant_name') + self.guid,
            description=getattr(
                config.CONF, 'tempest_identity_tenant_description'),
            domain_id=self.domain.id)
        LOGGER.debug("project: %s", self.project)

    def _create_user(self):
        """Create user for tests."""
        self.user = self.cloud.create_user(
            name=getattr(
                config.CONF, 'tempest_identity_user_name') + self.guid,
            password=getattr(config.CONF, 'tempest_identity_user_password'),
            default_project=getattr(
                config.CONF, 'tempest_identity_tenant_name') + self.guid,
            domain_id=self.domain.id)
        LOGGER.debug("user: %s", self.user)

    def _create_network(self):
        """Create network for tests."""
        tempest_net_name = getattr(
            config.CONF, 'tempest_private_net_name') + self.guid
        provider = {}
        if hasattr(config.CONF, 'tempest_network_type'):
            provider["network_type"] = getattr(
                config.CONF, 'tempest_network_type')
        if hasattr(config.CONF, 'tempest_physical_network'):
            provider["physical_network"] = getattr(
                config.CONF, 'tempest_physical_network')
        if hasattr(config.CONF, 'tempest_segmentation_id'):
            provider["segmentation_id"] = getattr(
                config.CONF, 'tempest_segmentation_id')
        LOGGER.info(
            "Creating network with name: '%s'", tempest_net_name)
        self.network = self.cloud.create_network(
            tempest_net_name, provider=provider)
        LOGGER.debug("network: %s", self.network)

        self.subnet = self.cloud.create_subnet(
            self.network.id,
            subnet_name=getattr(
                config.CONF, 'tempest_private_subnet_name') + self.guid,
            cidr=getattr(config.CONF, 'tempest_private_subnet_cidr'),
            enable_dhcp=True,
            dns_nameservers=[env.get('NAMESERVER')])
        LOGGER.debug("subnet: %s", self.subnet)

    def _create_image(self, name):
        """Create image for tests"""
        LOGGER.info("Creating image with name: '%s'", name)
        meta = getattr(config.CONF, 'openstack_extra_properties', None)
        image = self.cloud.create_image(
            name, filename=getattr(config.CONF, 'openstack_image_url'),
            is_public=True, meta=meta)
        LOGGER.debug("image: %s", image)
        return image

    def _create_flavor(self, name):
        """Create flavor for tests."""
        flavor = self.cloud.create_flavor(
            name, getattr(config.CONF, 'openstack_flavor_ram'),
            getattr(config.CONF, 'openstack_flavor_vcpus'),
            getattr(config.CONF, 'openstack_flavor_disk'))
        self.cloud.set_flavor_specs(
            flavor.id, getattr(config.CONF, 'flavor_extra_specs', {}))
        LOGGER.debug("flavor: %s", flavor)
        return flavor

    def create(self, create_project=False):
        """Create resources for Tempest test suite."""
        if create_project:
            self._create_project()
            self._create_user()
        self._create_network()

        LOGGER.debug("Creating two images for Tempest suite")
        self.image = self._create_image(
            getattr(config.CONF, 'openstack_image_name') + self.guid)
        self.image_alt = self._create_image(
            getattr(config.CONF, 'openstack_image_name_alt') + self.guid)

        LOGGER.info("Creating two flavors for Tempest suite")
        self.flavor = self._create_flavor(
            getattr(config.CONF, 'openstack_flavor_name') + self.guid)
        self.flavor_alt = self._create_flavor(
            getattr(config.CONF, 'openstack_flavor_name_alt') + self.guid)

    def cleanup(self):
        """
        Cleanup all OpenStack objects. Should be called on completion.
        """
        self.cloud.delete_image(self.image)
        self.cloud.delete_image(self.image_alt)
        self.cloud.delete_network(self.network.id)
        self.cloud.delete_flavor(self.flavor.id)
        self.cloud.delete_flavor(self.flavor_alt.id)
        if self.project:
            self.cloud.delete_user(self.user.id)
            self.cloud.delete_project(self.project.id)
