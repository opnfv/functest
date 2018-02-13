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

import yaml

from functest.core import testcase
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils.constants import CONST
import functest.utils.functest_utils as ft_utils

from snaps.config.flavor import FlavorConfig
from snaps.config.network import NetworkConfig, SubnetConfig
from snaps.config.project import ProjectConfig
from snaps.config.user import UserConfig

from snaps.openstack import create_flavor
from snaps.openstack.create_flavor import OpenStackFlavor
from snaps.openstack.tests import openstack_tests
from snaps.openstack.utils import deploy_utils


LOGGER = logging.getLogger(__name__)


class TempestCommon(testcase.TestCase):
    # pylint: disable=too-many-instance-attributes
    """TempestCommon testcases implementation class."""

    def __init__(self, **kwargs):
        super(TempestCommon, self).__init__(**kwargs)
        self.resources = TempestResourcesManager(**kwargs)
        self.mode = ""
        self.option = []
        self.verifier_id = conf_utils.get_verifier_id()
        self.verifier_repo_dir = conf_utils.get_verifier_repo_dir(
            self.verifier_id)
        self.deployment_id = conf_utils.get_verifier_deployment_id()
        self.deployment_dir = conf_utils.get_verifier_deployment_dir(
            self.verifier_id, self.deployment_id)
        self.verification_id = None

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

    def generate_test_list(self, verifier_repo_dir):
        """Generate test list based on the test mode."""
        LOGGER.debug("Generating test case list...")
        if self.mode == 'defcore':
            shutil.copyfile(
                conf_utils.TEMPEST_DEFCORE, conf_utils.TEMPEST_RAW_LIST)
        elif self.mode == 'custom':
            if os.path.isfile(conf_utils.TEMPEST_CUSTOM):
                shutil.copyfile(
                    conf_utils.TEMPEST_CUSTOM, conf_utils.TEMPEST_RAW_LIST)
            else:
                raise Exception("Tempest test list file %s NOT found."
                                % conf_utils.TEMPEST_CUSTOM)
        else:
            if self.mode == 'smoke':
                testr_mode = "smoke"
            elif self.mode == 'full':
                testr_mode = ""
            else:
                testr_mode = 'tempest.api.' + self.mode
            cmd = ("cd {0};"
                   "testr list-tests {1} > {2};"
                   "cd -;".format(verifier_repo_dir,
                                  testr_mode,
                                  conf_utils.TEMPEST_RAW_LIST))
            ft_utils.execute_command(cmd)

    def apply_tempest_blacklist(self):
        """Exclude blacklisted test cases."""
        LOGGER.debug("Applying tempest blacklist...")
        cases_file = self.read_file(conf_utils.TEMPEST_RAW_LIST)
        result_file = open(conf_utils.TEMPEST_LIST, 'w')
        black_tests = []
        try:
            installer_type = CONST.__getattribute__('INSTALLER_TYPE')
            deploy_scenario = CONST.__getattribute__('DEPLOY_SCENARIO')
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
               conf_utils.TEMPEST_LIST]
        cmd.extend(self.option)
        LOGGER.info("Starting Tempest test suite: '%s'.", cmd)

        f_stdout = open(
            os.path.join(conf_utils.TEMPEST_RESULTS_DIR, "tempest.log"), 'w+')
        f_stderr = open(
            os.path.join(conf_utils.TEMPEST_RESULTS_DIR,
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
                elif re.search('Starting verification', line):
                    LOGGER.info(line.replace('\n', ''))
                    first_pos = line.index("UUID=") + len("UUID=")
                    last_pos = line.index(") for deployment")
                    self.verification_id = line[first_pos:last_pos]
                    LOGGER.debug('Verification UUID: %s', self.verification_id)
                f_stdout.write(line)
        proc.wait()

        f_stdout.close()
        f_stderr.close()

    def parse_verifier_result(self):
        """Parse and save test results."""
        if self.verification_id is None:
            raise Exception('Verification UUID not found')

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

            with open(os.path.join(conf_utils.TEMPEST_RESULTS_DIR,
                                   "tempest.log"), 'r') as logfile:
                output = logfile.read()

            success_testcases = []
            for match in re.findall(r'.*\{0\} (.*?)[. ]*success ', output):
                success_testcases.append(match)
            failed_testcases = []
            for match in re.findall(r'.*\{0\} (.*?)[. ]*fail ', output):
                failed_testcases.append(match)
            skipped_testcases = []
            for match in re.findall(r'.*\{0\} (.*?)[. ]*skip:', output):
                skipped_testcases.append(match)

            self.details = {"tests": stat['num_tests'],
                            "failures": stat['num_failures'],
                            "success": success_testcases,
                            "skipped": skipped_testcases,
                            "errors": failed_testcases}
        except Exception:  # pylint: disable=broad-except
            self.result = 0

        LOGGER.info("Tempest %s success_rate is %s%%",
                    self.case_name, self.result)

    def run(self, **kwargs):

        self.start_time = time.time()
        try:
            if not os.path.exists(conf_utils.TEMPEST_RESULTS_DIR):
                os.makedirs(conf_utils.TEMPEST_RESULTS_DIR)
            resources = self.resources.create()
            compute_cnt = snaps_utils.get_active_compute_cnt(
                self.resources.os_creds)
            conf_utils.configure_tempest(
                self.deployment_dir,
                network_name=resources.get("network_name"),
                image_id=resources.get("image_id"),
                flavor_id=resources.get("flavor_id"),
                compute_cnt=compute_cnt)
            self.generate_test_list(self.verifier_repo_dir)
            self.apply_tempest_blacklist()
            self.run_verifier_tests()
            self.parse_verifier_result()
            res = testcase.TestCase.EX_OK
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.error('Error with run: %s', err)
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
    """Tempest resource manager."""
    def __init__(self, **kwargs):
        self.os_creds = kwargs.get('os_creds') or snaps_utils.get_credentials()
        self.guid = '-' + str(uuid.uuid4())
        self.creators = list()

        if hasattr(CONST, 'snaps_images_cirros'):
            self.cirros_image_config = CONST.__getattribute__(
                'snaps_images_cirros')
        else:
            self.cirros_image_config = None

    def _create_project(self):
        """Create project for tests."""
        project_creator = deploy_utils.create_project(
            self.os_creds, ProjectConfig(
                name=CONST.__getattribute__(
                    'tempest_identity_tenant_name') + self.guid,
                description=CONST.__getattribute__(
                    'tempest_identity_tenant_description')))
        if project_creator is None or project_creator.get_project() is None:
            raise Exception("Failed to create tenant")
        self.creators.append(project_creator)
        return project_creator.get_project().id

    def _create_user(self):
        """Create user for tests."""
        user_creator = deploy_utils.create_user(
            self.os_creds, UserConfig(
                name=CONST.__getattribute__(
                    'tempest_identity_user_name') + self.guid,
                password=CONST.__getattribute__(
                    'tempest_identity_user_password'),
                project_name=CONST.__getattribute__(
                    'tempest_identity_tenant_name') + self.guid))
        if user_creator is None or user_creator.get_user() is None:
            raise Exception("Failed to create user")
        self.creators.append(user_creator)
        return user_creator.get_user().id

    def _create_network(self, project_name):
        """Create network for tests."""
        tempest_network_type = None
        tempest_physical_network = None
        tempest_segmentation_id = None

        if hasattr(CONST, 'tempest_network_type'):
            tempest_network_type = CONST.__getattribute__(
                'tempest_network_type')
        if hasattr(CONST, 'tempest_physical_network'):
            tempest_physical_network = CONST.__getattribute__(
                'tempest_physical_network')
        if hasattr(CONST, 'tempest_segmentation_id'):
            tempest_segmentation_id = CONST.__getattribute__(
                'tempest_segmentation_id')

        tempest_net_name = CONST.__getattribute__(
            'tempest_private_net_name') + self.guid

        network_creator = deploy_utils.create_network(
            self.os_creds, NetworkConfig(
                name=tempest_net_name,
                project_name=project_name,
                network_type=tempest_network_type,
                physical_network=tempest_physical_network,
                segmentation_id=tempest_segmentation_id,
                subnet_settings=[SubnetConfig(
                    name=CONST.__getattribute__(
                        'tempest_private_subnet_name') + self.guid,
                    project_name=project_name,
                    cidr=CONST.__getattribute__(
                        'tempest_private_subnet_cidr'))]))
        if network_creator is None or network_creator.get_network() is None:
            raise Exception("Failed to create private network")
        self.creators.append(network_creator)
        return tempest_net_name

    def _create_image(self, name):
        """Create image for tests"""
        os_image_settings = openstack_tests.cirros_image_settings(
            name, public=True,
            image_metadata=self.cirros_image_config)
        image_creator = deploy_utils.create_image(
            self.os_creds, os_image_settings)
        if image_creator is None:
            raise Exception('Failed to create image')
        self.creators.append(image_creator)
        return image_creator.get_image().id

    def _create_flavor(self, name):
        """Create flavor for tests."""
        scenario = CONST.__getattribute__('DEPLOY_SCENARIO')
        flavor_metadata = None
        if 'ovs' in scenario or 'fdio' in scenario:
            flavor_metadata = create_flavor.MEM_PAGE_SIZE_LARGE
        flavor_creator = OpenStackFlavor(
            self.os_creds, FlavorConfig(
                name=name,
                ram=CONST.__getattribute__('openstack_flavor_ram'),
                disk=CONST.__getattribute__('openstack_flavor_disk'),
                vcpus=CONST.__getattribute__('openstack_flavor_vcpus'),
                metadata=flavor_metadata))
        flavor = flavor_creator.create()
        if flavor is None:
            raise Exception('Failed to create flavor')
        self.creators.append(flavor_creator)
        return flavor.id

    def create(self, use_custom_images=False, use_custom_flavors=False,
               create_project=False):
        """Create resources for Tempest test suite."""
        result = {
            'tempest_net_name': None,
            'image_id': None,
            'image_id_alt': None,
            'flavor_id': None,
            'flavor_id_alt': None
        }
        project_name = None

        if create_project:
            LOGGER.debug("Creating project and user for Tempest suite")
            project_name = CONST.__getattribute__(
                'tempest_identity_tenant_name') + self.guid
            result['project_id'] = self._create_project()
            result['user_id'] = self._create_user()
            result['tenant_id'] = result['project_id']  # for compatibility

        LOGGER.debug("Creating private network for Tempest suite")
        result['tempest_net_name'] = self._create_network(project_name)

        LOGGER.debug("Creating image for Tempest suite")
        image_name = CONST.__getattribute__('openstack_image_name') + self.guid
        result['image_id'] = self._create_image(image_name)

        if use_custom_images:
            LOGGER.debug("Creating 2nd image for Tempest suite")
            image_name = CONST.__getattribute__(
                'openstack_image_name_alt') + self.guid
            result['image_id_alt'] = self._create_image(image_name)

        if (CONST.__getattribute__('tempest_use_custom_flavors') == 'True' or
                use_custom_flavors):
            LOGGER.info("Creating flavor for Tempest suite")
            name = CONST.__getattribute__('openstack_flavor_name') + self.guid
            result['flavor_id'] = self._create_flavor(name)

        if use_custom_flavors:
            LOGGER.info("Creating 2nd flavor for Tempest suite")
            scenario = CONST.__getattribute__('DEPLOY_SCENARIO')
            if 'ovs' in scenario or 'fdio' in scenario:
                CONST.__setattr__('openstack_flavor_ram', 1024)
            name = CONST.__getattribute__(
                'openstack_flavor_name_alt') + self.guid
            result['flavor_id_alt'] = self._create_flavor(name)

        return result

    def cleanup(self):
        """
        Cleanup all OpenStack objects. Should be called on completion.
        """
        for creator in reversed(self.creators):
            try:
                creator.clean()
            except Exception as err:  # pylint: disable=broad-except
                LOGGER.error('Unexpected error cleaning - %s', err)
