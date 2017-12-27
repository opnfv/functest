#!/usr/bin/env python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

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


""" logging configuration """
logger = logging.getLogger(__name__)


class TempestCommon(testcase.TestCase):

    def __init__(self, **kwargs):
        super(TempestCommon, self).__init__(**kwargs)
        self.resources = TempestResourcesManager(**kwargs)
        self.MODE = ""
        self.OPTION = ""
        self.VERIFIER_ID = conf_utils.get_verifier_id()
        self.VERIFIER_REPO_DIR = conf_utils.get_verifier_repo_dir(
            self.VERIFIER_ID)
        self.DEPLOYMENT_ID = conf_utils.get_verifier_deployment_id()
        self.DEPLOYMENT_DIR = conf_utils.get_verifier_deployment_dir(
            self.VERIFIER_ID, self.DEPLOYMENT_ID)
        self.VERIFICATION_ID = None

    @staticmethod
    def read_file(filename):
        with open(filename) as src:
            return [line.strip() for line in src.readlines()]

    def generate_test_list(self, verifier_repo_dir):
        logger.debug("Generating test case list...")
        if self.MODE == 'defcore':
            shutil.copyfile(
                conf_utils.TEMPEST_DEFCORE, conf_utils.TEMPEST_RAW_LIST)
        elif self.MODE == 'custom':
            if os.path.isfile(conf_utils.TEMPEST_CUSTOM):
                shutil.copyfile(
                    conf_utils.TEMPEST_CUSTOM, conf_utils.TEMPEST_RAW_LIST)
            else:
                raise Exception("Tempest test list file %s NOT found."
                                % conf_utils.TEMPEST_CUSTOM)
        else:
            if self.MODE == 'smoke':
                testr_mode = "smoke"
            elif self.MODE == 'full':
                testr_mode = ""
            else:
                testr_mode = 'tempest.api.' + self.MODE
            cmd = ("cd {0};"
                   "testr list-tests {1} > {2};"
                   "cd -;".format(verifier_repo_dir,
                                  testr_mode,
                                  conf_utils.TEMPEST_RAW_LIST))
            ft_utils.execute_command(cmd)

    def apply_tempest_blacklist(self):
        logger.debug("Applying tempest blacklist...")
        cases_file = self.read_file(conf_utils.TEMPEST_RAW_LIST)
        result_file = open(conf_utils.TEMPEST_LIST, 'w')
        black_tests = []
        try:
            installer_type = CONST.__getattribute__('INSTALLER_TYPE')
            deploy_scenario = CONST.__getattribute__('DEPLOY_SCENARIO')
            if (bool(installer_type) * bool(deploy_scenario)):
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
        except Exception:
            black_tests = []
            logger.debug("Tempest blacklist file does not exist.")

        for cases_line in cases_file:
            for black_tests_line in black_tests:
                if black_tests_line in cases_line:
                    break
            else:
                result_file.write(str(cases_line) + '\n')
        result_file.close()

    def run_verifier_tests(self):
        self.OPTION += (" --load-list {} --detailed"
                        .format(conf_utils.TEMPEST_LIST))

        cmd_line = "rally verify start " + self.OPTION
        logger.info("Starting Tempest test suite: '%s'." % cmd_line)

        header = ("Tempest environment:\n"
                  "  SUT: %s\n  Scenario: %s\n  Node: %s\n  Date: %s\n" %
                  (CONST.__getattribute__('INSTALLER_TYPE'),
                   CONST.__getattribute__('DEPLOY_SCENARIO'),
                   CONST.__getattribute__('NODE_NAME'),
                   time.strftime("%a %b %d %H:%M:%S %Z %Y")))

        f_stdout = open(
            os.path.join(conf_utils.TEMPEST_RESULTS_DIR, "tempest.log"), 'w+')
        f_stderr = open(
            os.path.join(conf_utils.TEMPEST_RESULTS_DIR,
                         "tempest-error.log"), 'w+')
        f_env = open(os.path.join(conf_utils.TEMPEST_RESULTS_DIR,
                                  "environment.log"), 'w+')
        f_env.write(header)

        p = subprocess.Popen(
            cmd_line, shell=True,
            stdout=subprocess.PIPE,
            stderr=f_stderr,
            bufsize=1)

        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                if re.search("\} tempest\.", line):
                    logger.info(line.replace('\n', ''))
                elif re.search('Starting verification', line):
                    logger.info(line.replace('\n', ''))
                    first_pos = line.index("UUID=") + len("UUID=")
                    last_pos = line.index(") for deployment")
                    self.VERIFICATION_ID = line[first_pos:last_pos]
                    logger.debug('Verification UUID: %s', self.VERIFICATION_ID)
                f_stdout.write(line)
        p.wait()

        f_stdout.close()
        f_stderr.close()
        f_env.close()

    def parse_verifier_result(self):
        if self.VERIFICATION_ID is None:
            raise Exception('Verification UUID not found')

        cmd_line = "rally verify show --uuid {}".format(self.VERIFICATION_ID)
        logger.info("Showing result for a verification: '%s'." % cmd_line)
        p = subprocess.Popen(cmd_line,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        for line in p.stdout:
            new_line = line.replace(' ', '').split('|')
            if 'Tests' in new_line:
                break

            logger.info(line)
            if 'Testscount' in new_line:
                num_tests = new_line[2]
            elif 'Success' in new_line:
                num_success = new_line[2]
            elif 'Skipped' in new_line:
                num_skipped = new_line[2]
            elif 'Failures' in new_line:
                num_failures = new_line[2]

        try:
            num_executed = int(num_tests) - int(num_skipped)
            try:
                self.result = 100 * int(num_success) / int(num_executed)
            except ZeroDivisionError:
                self.result = 0
                if int(num_tests) > 0:
                    logger.info("All tests have been skipped")
                else:
                    logger.error("No test has been executed")
                    return

            with open(os.path.join(conf_utils.TEMPEST_RESULTS_DIR,
                                   "tempest.log"), 'r') as logfile:
                output = logfile.read()

            success_testcases = []
            for match in re.findall('.*\{0\} (.*?)[. ]*success ', output):
                success_testcases.append(match)
            failed_testcases = []
            for match in re.findall('.*\{0\} (.*?)[. ]*fail ', output):
                failed_testcases.append(match)
            skipped_testcases = []
            for match in re.findall('.*\{0\} (.*?)[. ]*skip:', output):
                skipped_testcases.append(match)

            self.details = {"tests": int(num_tests),
                            "failures": int(num_failures),
                            "success": success_testcases,
                            "errors": failed_testcases,
                            "skipped": skipped_testcases}
        except Exception:
            self.result = 0

        logger.info("Tempest %s success_rate is %s%%"
                    % (self.case_name, self.result))

    def run(self):

        self.start_time = time.time()
        try:
            if not os.path.exists(conf_utils.TEMPEST_RESULTS_DIR):
                os.makedirs(conf_utils.TEMPEST_RESULTS_DIR)
            resources = self.resources.create()
            compute_cnt = snaps_utils.get_active_compute_cnt(
                self.resources.os_creds)
            conf_utils.configure_tempest(
                self.DEPLOYMENT_DIR,
                image_id=resources.get("image_id"),
                flavor_id=resources.get("flavor_id"),
                compute_cnt=compute_cnt)
            self.generate_test_list(self.VERIFIER_REPO_DIR)
            self.apply_tempest_blacklist()
            self.run_verifier_tests()
            self.parse_verifier_result()
            res = testcase.TestCase.EX_OK
        except Exception as e:
            logger.error('Error with run: %s' % e)
            res = testcase.TestCase.EX_RUN_ERROR
        finally:
            self.resources.cleanup()

        self.stop_time = time.time()
        return res


class TempestSmokeSerial(TempestCommon):

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest_smoke_serial'
        TempestCommon.__init__(self, **kwargs)
        self.MODE = "smoke"
        self.OPTION = "--concurrency 1"


class TempestSmokeParallel(TempestCommon):

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest_smoke_parallel'
        TempestCommon.__init__(self, **kwargs)
        self.MODE = "smoke"
        self.OPTION = ""


class TempestFullParallel(TempestCommon):

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest_full_parallel'
        TempestCommon.__init__(self, **kwargs)
        self.MODE = "full"


class TempestCustom(TempestCommon):

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest_custom'
        TempestCommon.__init__(self, **kwargs)
        self.MODE = "custom"
        self.OPTION = "--concurrency 1"


class TempestDefcore(TempestCommon):

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tempest_defcore'
        TempestCommon.__init__(self, **kwargs)
        self.MODE = "defcore"
        self.OPTION = "--concurrency 1"


class TempestResourcesManager(object):

    def __init__(self, **kwargs):
        self.os_creds = None
        if 'os_creds' in kwargs:
            self.os_creds = kwargs['os_creds']
        else:
            self.os_creds = openstack_tests.get_credentials(
                os_env_file=CONST.__getattribute__('openstack_creds'))

        self.guid = '-' + str(uuid.uuid4())

        self.creators = list()

        if hasattr(CONST, 'snaps_images_cirros'):
            self.cirros_image_config = CONST.__getattribute__(
                'snaps_images_cirros')
        else:
            self.cirros_image_config = None

    def create(self, use_custom_images=False, use_custom_flavors=False,
               create_project=False):
        if create_project:
            logger.debug("Creating project (tenant) for Tempest suite")
            project_name = CONST.__getattribute__(
                'tempest_identity_tenant_name') + self.guid
            project_creator = deploy_utils.create_project(
                self.os_creds, ProjectConfig(
                    name=project_name,
                    description=CONST.__getattribute__(
                        'tempest_identity_tenant_description')))
            if (project_creator is None or
                    project_creator.get_project() is None):
                raise Exception("Failed to create tenant")
            project_id = project_creator.get_project().id
            self.creators.append(project_creator)

            logger.debug("Creating user for Tempest suite")
            user_creator = deploy_utils.create_user(
                self.os_creds, UserConfig(
                    name=CONST.__getattribute__(
                        'tempest_identity_user_name') + self.guid,
                    password=CONST.__getattribute__(
                        'tempest_identity_user_password'),
                    project_name=project_name))
            if user_creator is None or user_creator.get_user() is None:
                raise Exception("Failed to create user")
            user_id = user_creator.get_user().id
            self.creators.append(user_creator)
        else:
            project_name = None
            project_id = None
            user_id = None

        logger.debug("Creating private network for Tempest suite")

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

        network_creator = deploy_utils.create_network(
            self.os_creds, NetworkConfig(
                name=CONST.__getattribute__(
                    'tempest_private_net_name') + self.guid,
                project_name=project_name,
                network_type=tempest_network_type,
                physical_network=tempest_physical_network,
                segmentation_id=tempest_segmentation_id,
                subnet_settings=[SubnetConfig(
                    name=CONST.__getattribute__(
                        'tempest_private_subnet_name') + self.guid,
                    cidr=CONST.__getattribute__('tempest_private_subnet_cidr'))
                ]))
        if network_creator is None or network_creator.get_network() is None:
            raise Exception("Failed to create private network")
        self.creators.append(network_creator)

        image_id = None
        image_id_alt = None
        flavor_id = None
        flavor_id_alt = None

        logger.debug("Creating image for Tempest suite")
        image_base_name = CONST.__getattribute__(
            'openstack_image_name') + self.guid
        os_image_settings = openstack_tests.cirros_image_settings(
            image_base_name, public=True,
            image_metadata=self.cirros_image_config)
        logger.debug("Creating image for Tempest suite")
        image_creator = deploy_utils.create_image(
            self.os_creds, os_image_settings)
        if image_creator is None:
            raise Exception('Failed to create image')
        self.creators.append(image_creator)
        image_id = image_creator.get_image().id

        if use_custom_images:
            logger.debug("Creating 2nd image for Tempest suite")
            image_base_name_alt = CONST.__getattribute__(
                'openstack_image_name_alt') + self.guid
            os_image_settings_alt = openstack_tests.cirros_image_settings(
                image_base_name_alt, public=True,
                image_metadata=self.cirros_image_config)
            logger.debug("Creating 2nd image for Tempest suite")
            image_creator_alt = deploy_utils.create_image(
                self.os_creds, os_image_settings_alt)
            if image_creator_alt is None:
                raise Exception('Failed to create image')
            self.creators.append(image_creator_alt)
            image_id_alt = image_creator_alt.get_image().id

        if (CONST.__getattribute__('tempest_use_custom_flavors') == 'True' or
           use_custom_flavors):
            logger.info("Creating flavor for Tempest suite")
            scenario = CONST.__getattribute__('DEPLOY_SCENARIO')
            flavor_metadata = None
            if 'ovs' in scenario or 'fdio' in scenario:
                flavor_metadata = create_flavor.MEM_PAGE_SIZE_LARGE
            flavor_creator = OpenStackFlavor(
                self.os_creds, FlavorConfig(
                    name=CONST.__getattribute__(
                        'openstack_flavor_name') + self.guid,
                    ram=CONST.__getattribute__('openstack_flavor_ram'),
                    disk=CONST.__getattribute__('openstack_flavor_disk'),
                    vcpus=CONST.__getattribute__('openstack_flavor_vcpus'),
                    metadata=flavor_metadata))
            flavor = flavor_creator.create()
            if flavor is None:
                raise Exception('Failed to create flavor')
            self.creators.append(flavor_creator)
            flavor_id = flavor.id

        if use_custom_flavors:
            logger.info("Creating 2nd flavor for Tempest suite")
            scenario = CONST.__getattribute__('DEPLOY_SCENARIO')
            flavor_metadata_alt = None
            if 'ovs' in scenario or 'fdio' in scenario:
                flavor_metadata_alt = create_flavor.MEM_PAGE_SIZE_LARGE
                CONST.__setattr__('openstack_flavor_ram', 1024)
            flavor_creator_alt = OpenStackFlavor(
                self.os_creds, FlavorConfig(
                    name=CONST.__getattribute__(
                        'openstack_flavor_name_alt') + self.guid,
                    ram=CONST.__getattribute__('openstack_flavor_ram'),
                    disk=CONST.__getattribute__('openstack_flavor_disk'),
                    vcpus=CONST.__getattribute__('openstack_flavor_vcpus'),
                    metadata=flavor_metadata_alt))
            flavor_alt = flavor_creator_alt.create()
            if flavor_alt is None:
                raise Exception('Failed to create flavor')
            self.creators.append(flavor_creator_alt)
            flavor_id_alt = flavor_alt.id

        print("RESOURCES CREATE: image_id: %s, image_id_alt: %s, "
              "flavor_id: %s, flavor_id_alt: %s" % (
                  image_id, image_id_alt, flavor_id, flavor_id_alt,))

        result = {
            'image_id': image_id,
            'image_id_alt': image_id_alt,
            'flavor_id': flavor_id,
            'flavor_id_alt': flavor_id_alt
        }

        if create_project:
            result['project_id'] = project_id
            result['tenant_id'] = project_id  # for compatibility
            result['user_id'] = user_id

        return result

    def cleanup(self):
        """
        Cleanup all OpenStack objects. Should be called on completion.
        """
        for creator in reversed(self.creators):
            try:
                creator.clean()
            except Exception as e:
                logger.error('Unexpected error cleaning - %s', e)
