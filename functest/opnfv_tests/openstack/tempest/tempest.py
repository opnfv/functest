#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

import os
import re
import shutil
import subprocess
import time

import yaml

from functest.core import testcase_base
from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils

""" logging configuration """
logger = ft_logger.Logger("Tempest").getLogger()


class TempestCommon(testcase_base.TestcaseBase):

    def __init__(self):
        super(TempestCommon, self).__init__()
        self.MODE = ""
        self.OPTION = ""
        self.FLAVOR_ID = None
        self.IMAGE_ID = None
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

    def create_tempest_resources(self):
        keystone_client = os_utils.get_keystone_client()

        logger.debug("Creating tenant and user for Tempest suite")
        tenant_id = os_utils.create_tenant(
            keystone_client,
            CONST.tempest_identity_tenant_name,
            CONST.tempest_identity_tenant_description)
        if not tenant_id:
            logger.error("Error : Failed to create %s tenant"
                         % CONST.tempest_identity_tenant_name)

        user_id = os_utils.create_user(keystone_client,
                                       CONST.tempest_identity_user_name,
                                       CONST.tempest_identity_user_password,
                                       None, tenant_id)
        if not user_id:
            logger.error("Error : Failed to create %s user" %
                         CONST.tempest_identity_user_name)

        logger.debug("Creating private network for Tempest suite")
        network_dic = os_utils.create_shared_network_full(
            CONST.tempest_private_net_name,
            CONST.tempest_private_subnet_name,
            CONST.tempest_router_name,
            CONST.tempest_private_subnet_cidr)
        if not network_dic:
            return testcase_base.TestcaseBase.EX_RUN_ERROR

        if CONST.tempest_use_custom_images:
            # adding alternative image should be trivial should we need it
            logger.debug("Creating image for Tempest suite")
            _, self.IMAGE_ID = os_utils.get_or_create_image(
                CONST.openstack_image_name, conf_utils.GLANCE_IMAGE_PATH,
                CONST.openstack_image_disk_format)
            if not self.IMAGE_ID:
                return testcase_base.TestcaseBase.EX_RUN_ERROR

        if CONST.tempest_use_custom_flavors:
            # adding alternative flavor should be trivial should we need it
            logger.debug("Creating flavor for Tempest suite")
            _, self.FLAVOR_ID = os_utils.get_or_create_flavor(
                CONST.openstack_flavor_name,
                CONST.openstack_flavor_ram,
                CONST.openstack_flavor_disk,
                CONST.openstack_flavor_vcpus)
            if not self.FLAVOR_ID:
                return testcase_base.TestcaseBase.EX_RUN_ERROR

        return testcase_base.TestcaseBase.EX_OK

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
                logger.error("Tempest test list file %s NOT found."
                             % conf_utils.TEMPEST_CUSTOM)
                return testcase_base.TestcaseBase.EX_RUN_ERROR
        else:
            if self.MODE == 'smoke':
                testr_mode = "smoke"
            elif self.MODE == 'feature_multisite':
                testr_mode = " | grep -i kingbird "
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

        return testcase_base.TestcaseBase.EX_OK

    def apply_tempest_blacklist(self):
        logger.debug("Applying tempest blacklist...")
        cases_file = self.read_file(conf_utils.TEMPEST_RAW_LIST)
        result_file = open(conf_utils.TEMPEST_LIST, 'w')
        black_tests = []
        try:
            installer_type = CONST.INSTALLER_TYPE
            deploy_scenario = CONST.DEPLOY_SCENARIO
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
        return testcase_base.TestcaseBase.EX_OK

    def run_verifier_tests(self):
        self.OPTION += (" --load-list {}".format(conf_utils.TEMPEST_LIST))

        cmd_line = "rally verify start " + self.OPTION
        logger.info("Starting Tempest test suite: '%s'." % cmd_line)

        header = ("Tempest environment:\n"
                  "  Installer: %s\n  Scenario: %s\n  Node: %s\n  Date: %s\n" %
                  (CONST.INSTALLER_TYPE,
                   CONST.DEPLOY_SCENARIO,
                   CONST.NODE_NAME,
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
                    logger.debug('Verication UUID: %s' % self.VERIFICATION_ID)
                f_stdout.write(line)
        p.wait()

        f_stdout.close()
        f_stderr.close()
        f_env.close()

    def parse_verifier_result(self):
        if not self.VERIFICATION_ID:
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
            success_rate = 100 * int(num_success) / int(num_executed)
            with open(os.path.join(conf_utils.TEMPEST_RESULTS_DIR,
                                   "tempest.log"), 'r') as logfile:
                output = logfile.read()

            error_logs = ""
            for match in re.findall('(.*?)[. ]*FAILED', output):
                error_logs += match

            self.details = {"tests": int(num_tests),
                            "failures": int(num_failures),
                            "errors": error_logs}
        except Exception:
            success_rate = 0

        self.criteria = ft_utils.check_success_rate(
            self.case_name, success_rate)
        logger.info("Tempest %s success_rate is %s%%, is marked as %s"
                    % (self.case_name, success_rate, self.criteria))

    def run(self):

        self.start_time = time.time()

        if not os.path.exists(conf_utils.TEMPEST_RESULTS_DIR):
            os.makedirs(conf_utils.TEMPEST_RESULTS_DIR)

        # Pre-configuration
        res = self.create_tempest_resources()
        if res != testcase_base.TestcaseBase.EX_OK:
            return res

        res = conf_utils.configure_tempest(self.DEPLOYMENT_DIR,
                                           self.IMAGE_ID,
                                           self.FLAVOR_ID)
        if res != testcase_base.TestcaseBase.EX_OK:
            return res

        res = self.generate_test_list(self.VERIFIER_REPO_DIR)
        if res != testcase_base.TestcaseBase.EX_OK:
            return res

        res = self.apply_tempest_blacklist()
        if res != testcase_base.TestcaseBase.EX_OK:
            return res

        self.run_verifier_tests()
        self.parse_verifier_result()

        self.stop_time = time.time()

        # If we are here, it means that the test case was successfully executed
        # criteria is managed by the criteria Field
        return testcase_base.TestcaseBase.EX_OK


class TempestSmokeSerial(TempestCommon):

    def __init__(self):
        TempestCommon.__init__(self)
        self.case_name = "tempest_smoke_serial"
        self.MODE = "smoke"
        self.OPTION = "--concurrency 1"


class TempestSmokeParallel(TempestCommon):

    def __init__(self):
        TempestCommon.__init__(self)
        self.case_name = "tempest_smoke_parallel"
        self.MODE = "smoke"
        self.OPTION = ""


class TempestFullParallel(TempestCommon):

    def __init__(self):
        TempestCommon.__init__(self)
        self.case_name = "tempest_full_parallel"
        self.MODE = "full"


class TempestMultisite(TempestCommon):

    def __init__(self):
        TempestCommon.__init__(self)
        self.case_name = "multisite"
        self.MODE = "feature_multisite"
        self.OPTION = "--concurrency 1"
        conf_utils.configure_tempest_multisite(self.DEPLOYMENT_DIR)


class TempestCustom(TempestCommon):

    def __init__(self, mode, option):
        TempestCommon.__init__(self)
        self.case_name = "tempest_custom"
        self.MODE = mode
        self.OPTION = option
