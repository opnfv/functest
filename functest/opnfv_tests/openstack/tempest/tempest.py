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

import functest.core.testcase_base as testcase_base
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
import functest.utils.functest_constants as ft_constants
import conf_utils

modes = ['full', 'smoke', 'baremetal', 'compute', 'data_processing',
         'identity', 'image', 'network', 'object_storage', 'orchestration',
         'telemetry', 'volume', 'custom', 'defcore', 'feature_multisite']


""" logging configuration """
logger = ft_logger.Logger("Tempest").getLogger()


class TempestCommon(testcase_base.TestcaseBase):

    def __init__(self):
        self.MODE = "smoke"
        self.CASE_NAME = ""
        self.FLAVOR_ID = None
        self.IMAGE_ID = None
        self.DEPLOYMENT_DIR = ft_utils.get_deployment_dir()

    def read_file(self, filename):
        with open(filename) as src:
            return [line.strip() for line in src.readlines()]

    def create_tempest_resources(self):
        keystone_client = os_utils.get_keystone_client()

        logger.debug("Creating tenant and user for Tempest suite")
        tenant_id = os_utils.create_tenant(
            keystone_client,
            ft_constants.TEMPEST_TENANT_NAME,
            ft_constants.TEMPEST_TENANT_DESCRIPTION)
        if not tenant_id:
            logger.error("Error : Failed to create %s tenant"
                         % ft_constants.TEMPEST_TENANT_NAME)

        user_id = os_utils.create_user(keystone_client,
                                       ft_constants.TEMPEST_USER_NAME,
                                       ft_constants.TEMPEST_USER_PASSWORD,
                                       None, tenant_id)
        if not user_id:
            logger.error("Error : Failed to create %s user" %
                         ft_constants.TEMPEST_USER_NAME)

        logger.debug("Creating private network for Tempest suite")
        network_dic = \
            os_utils.create_shared_network_full(
                ft_constants.TEMPEST_PRIVATE_NET_NAME,
                ft_constants.TEMPEST_PRIVATE_SUBNET_NAME,
                ft_constants.TEMPEST_ROUTER_NAME,
                ft_constants.TEMPEST_PRIVATE_SUBNET_CIDR)
        if not network_dic:
            exit(1)

        if ft_constants.TEMPEST_USE_CUSTOM_IMAGES:
            # adding alternative image should be trivial should we need it
            logger.debug("Creating image for Tempest suite")
            _, self.IMAGE_ID = os_utils.get_or_create_image(
                ft_constants.GLANCE_IMAGE_NAME, conf_utils.GLANCE_IMAGE_PATH,
                ft_constants.GLANCE_IMAGE_FORMAT)
            if not self.IMAGE_ID:
                exit(-1)

        if ft_constants.TEMPEST_USE_CUSTOM_FLAVORS:
            # adding alternative flavor should be trivial should we need it
            logger.debug("Creating flavor for Tempest suite")
            _, self.FLAVOR_ID = os_utils.get_or_create_flavor(
                ft_constants.FLAVOR_NAME,
                ft_constants.FLAVOR_RAM,
                ft_constants.FLAVOR_DISK,
                ft_constants.FLAVOR_VCPUS)
            if not self.FLAVOR_ID:
                exit(-1)

    def generate_test_list(self, deployment_dir):
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
                exit(-1)
        else:
            if self.MODE == 'smoke':
                testr_mode = "smoke"
            elif self.MODE == 'feature_multisite':
                testr_mode = " | grep -i kingbird "
            elif self.MODE == 'full':
                testr_mode = ""
            else:
                testr_mode = 'tempest.api.' + self.MODE
            cmd = ("cd " + deployment_dir + ";" + "testr list-tests " +
                   testr_mode + ">" + conf_utils.TEMPEST_RAW_LIST + ";cd")
            ft_utils.execute_command(cmd)

    def apply_tempest_blacklist(self):
        logger.debug("Applying tempest blacklist...")
        cases_file = self.read_file(conf_utils.TEMPEST_RAW_LIST)
        result_file = open(conf_utils.TEMPEST_LIST, 'w')
        black_tests = []
        try:
            installer_type = ft_constants.CI_INSTALLER_TYPE
            deploy_scenario = ft_constants.CI_SCENARIO
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
        except:
            black_tests = []
            logger.debug("Tempest blacklist file does not exist.")

        for cases_line in cases_file:
            for black_tests_line in black_tests:
                if black_tests_line in cases_line:
                    break
            else:
                result_file.write(str(cases_line) + '\n')
        result_file.close()

    def run(self, OPTION):
        if not os.path.exists(conf_utils.TEMPEST_RESULTS_DIR):
            os.makedirs(conf_utils.TEMPEST_RESULTS_DIR)

        # Pre-configuration
        self.create_tempest_resources()
        conf_utils.configure_tempest(logger,
                                     self.deployment_dir,
                                     self.IMAGE_ID,
                                     self.FLAVOR_ID)
        self.generate_test_list(self.deployment_dir)
        self.apply_tempest_blacklist()

        # Execute suite
        ret_val = self.run_tempest(self.MODE)

        if ret_val != 0:
            return testcase_base.TestcaseBase.EX_RUN_ERROR

        logger.info("Starting Tempest test suite: '%s'." % OPTION)
        cmd_line = "rally verify start " + OPTION + " --system-wide"

        header = ("Tempest environment:\n"
                  "  Installer: %s\n  Scenario: %s\n  Node: %s\n  Date: %s\n" %
                  (ft_constants.CI_INSTALLER_TYPE,
                   ft_constants.CI_SCENARIO,
                   ft_constants.CI_NODE,
                   time.strftime("%a %b %d %H:%M:%S %Z %Y")))

        f_stdout = open(conf_utils.TEMPEST_RESULTS_DIR + "/tempest.log", 'w+')
        f_stderr = open(
            conf_utils.TEMPEST_RESULTS_DIR + "/tempest-error.log", 'w+')
        f_env = open(conf_utils.TEMPEST_RESULTS_DIR + "/environment.log", 'w+')
        f_env.write(header)

        # subprocess.call(cmd_line, shell=True,
        # stdout=f_stdout, stderr=f_stderr)
        p = subprocess.Popen(
            cmd_line, shell=True,
            stdout=subprocess.PIPE,
            stderr=f_stderr,
            bufsize=1)

        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                if re.search("\} tempest\.", line):
                    logger.info(line.replace('\n', ''))
                f_stdout.write(line)
        p.wait()

        f_stdout.close()
        f_stderr.close()
        f_env.close()

        cmd_line = "rally verify show"
        output = ""
        p = subprocess.Popen(cmd_line,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        for line in p.stdout:
            if re.search("Tests\:", line):
                break
            output += line
        logger.info(output)

        cmd_line = "rally verify list"
        cmd = os.popen(cmd_line)
        output = (((cmd.read()).splitlines()[-2]).replace(" ", "")).split("|")
        # Format:
        # | UUID | Deployment UUID | smoke | tests | failures | Created at |
        # Duration | Status  |
        num_tests = output[4]
        num_failures = output[5]
        duration = output[7]
        # Compute duration (lets assume it does not take more than 60 min)
        dur_min = int(duration.split(':')[1])
        dur_sec_float = float(duration.split(':')[2])
        dur_sec_int = int(round(dur_sec_float, 0))
        dur_sec_int = dur_sec_int + 60 * dur_min

        try:
            diff = (int(num_tests) - int(num_failures))
            success_rate = 100 * diff / int(num_tests)
        except:
            success_rate = 0

        if 'smoke' in self.MODE:
            self.CASE_NAME = 'tempest_smoke_serial'
        elif 'feature' in self.MODE:
            self.CASE_NAME = self.MODE.replace(
                "feature_", "")
        else:
            self.CASE_NAME = 'tempest_full_parallel'

        status = ft_utils.check_success_rate(
            self.CASE_NAME, success_rate)
        logger.info("Tempest %s success_rate is %s%%, is marked as %s"
                    % (self.CASE_NAME, success_rate, status))

        if status == "PASS":
            return 0
        else:
            return -1


class TempestSmoke(TempestCommon):

    def __init__(self):
        TempestCommon.__init__(self)
        self.MODE = "smoke --concur 1"
        self.CASE_NAME = "tempest_smoke_serial"

    def run(self):
        ret_val = super(TempestSmoke, self).run("smoke")
        if ret_val != 0:
            return -1


class TempestFull(TempestCommon):

    def __init__(self):
        TempestCommon.__init__(self)
        self.CASE_NAME = "tempest_full_parallel"

    def run(self):
        ret_val = super(TempestFull, self).run("full")
        if ret_val != 0:
            return -1


class TempestMultisite(TempestCommon):

    def __init__(self):
        TempestCommon.__init__(self)
        self.CASE_NAME = "multisite"
        self.MODE = " --concur 1"

    def run(self):
        ret_val = super(TempestMultisite, self).run("feature_multisite")
        if ret_val != 0:
            return -1
