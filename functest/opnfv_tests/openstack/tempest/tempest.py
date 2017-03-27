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

""" logging configuration """
logger = ft_logger.Logger("Tempest").getLogger()


class TempestCommon(testcase_base.TestCase):

    def __init__(self):
        super(TempestCommon, self).__init__()
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
            elif self.MODE == 'feature_multisite':
                testr_mode = "'[Kk]ingbird'"
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

    def run_verifier_tests(self):
        self.OPTION += (" --load-list {} --detailed"
                        .format(conf_utils.TEMPEST_LIST))

        cmd_line = "rally verify start " + self.OPTION
        logger.info("Starting Tempest test suite: '%s'." % cmd_line)

        header = ("Tempest environment:\n"
                  "  SUT: %s\n  Scenario: %s\n  Node: %s\n  Date: %s\n" %
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
            success_rate = 100 * int(num_success) / int(num_executed)
            with open(os.path.join(conf_utils.TEMPEST_RESULTS_DIR,
                                   "tempest.log"), 'r') as logfile:
                output = logfile.read()

            error_logs = ""
            for match in re.findall('(.*?)[. ]*fail ', output):
                error_logs += match
            skipped_testcase = ""
            for match in re.findall('(.*?)[. ]*skip:', output):
                skipped_testcase += match

            self.details = {"tests": int(num_tests),
                            "failures": int(num_failures),
                            "errors": error_logs,
                            "skipped": skipped_testcase}
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

        try:
            image_and_flavor = conf_utils.create_tempest_resources()
            conf_utils.configure_tempest(
                self.DEPLOYMENT_DIR,
                IMAGE_ID=image_and_flavor.get("image_id"),
                FLAVOR_ID=image_and_flavor.get("flavor_id"),
                MODE=self.MODE)
            self.generate_test_list(self.VERIFIER_REPO_DIR)
            self.apply_tempest_blacklist()
            self.run_verifier_tests()
            self.parse_verifier_result()
            res = testcase_base.TestCase.EX_OK
        except Exception as e:
            logger.error('Error with run: %s' % e)
            res = testcase_base.TestCase.EX_RUN_ERROR

        self.stop_time = time.time()
        return res


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
        conf_utils.install_verifier_ext(CONST.dir_repo_kingbird)


class TempestCustom(TempestCommon):

    def __init__(self):
        TempestCommon.__init__(self)
        self.case_name = "tempest_custom"
        self.MODE = "custom"
        self.OPTION = "--concurrency 1"


class TempestDefcore(TempestCommon):

    def __init__(self):
        TempestCommon.__init__(self)
        self.case_name = "tempest_defcore"
        self.MODE = "defcore"
        self.OPTION = "--concurrency 1"
