#!/usr/bin/env python

# matthew.lijun@huawei.com wangwulin@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
import argparse
import os
import re
import sys
import subprocess
import time

from functest.core import testcase
from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
from tempest_conf import TempestConf

""" logging configuration """
logger = ft_logger.Logger("refstack_defcore").getLogger()


class RefstackClient(testcase.TestCase):

    def __init__(self):
        super(RefstackClient, self).__init__()
        self.case_name = "refstack_defcore"
        self.FUNCTEST_TEST = CONST.dir_functest_test
        self.CONF_PATH = CONST.refstack_tempest_conf_path
        self.DEFCORE_LIST = CONST.refstack_defcore_list
        self.confpath = os.path.join(self.FUNCTEST_TEST,
                                     self.CONF_PATH)
        self.defcorelist = os.path.join(self.FUNCTEST_TEST,
                                        self.DEFCORE_LIST)

    def source_venv(self):

        cmd = ("cd {0};"
               ". .venv/bin/activate;"
               "cd -;".format(CONST.dir_refstack_client))
        ft_utils.execute_command(cmd)

    def run_defcore(self, conf, testlist):
        logger.debug("Generating test case list...")

        cmd = ("cd {0};"
               "./refstack-client test -c {1} -v --test-list {2};"
               "cd -;".format(CONST.dir_refstack_client,
                              conf,
                              testlist))
        ft_utils.execute_command(cmd)

    def run_defcore_default(self):
        logger.debug("Generating test case list...")

        cmd = ("cd {0};"
               "./refstack-client test -c {1} -v --test-list {2};"
               "cd -;".format(CONST.dir_refstack_client,
                              self.confpath,
                              self.defcorelist))
        logger.info("Starting Refstack_defcore test case: '%s'." % cmd)

        header = ("Refstack environment:\n"
                  "  SUT: %s\n  Scenario: %s\n  Node: %s\n  Date: %s\n" %
                  (CONST.INSTALLER_TYPE,
                   CONST.DEPLOY_SCENARIO,
                   CONST.NODE_NAME,
                   time.strftime("%a %b %d %H:%M:%S %Z %Y")))

        f_stdout = open(
            os.path.join(conf_utils.REFSTACK_RESULTS_DIR,
                         "refstack.log"), 'w+')
        f_env = open(os.path.join(conf_utils.REFSTACK_RESULTS_DIR,
                                  "environment.log"), 'w+')
        f_env.write(header)

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, bufsize=1)

        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                if 'Tests' in line:
                    break
                if re.search("\} tempest\.", line):
                    logger.info(line.replace('\n', ''))
                f_stdout.write(line)
        p.wait()

        f_stdout.close()
        f_env.close()

    def parse_refstack_result(self):
        try:
            with open(os.path.join(conf_utils.REFSTACK_RESULTS_DIR,
                                   "refstack.log"), 'r') as logfile:
                output = logfile.read()

            for match in re.findall("Ran: (\d+) tests in (\d+\.\d{4}) sec.",
                                    output):
                num_tests = match[0]
                logger.info("Ran: %s tests in %s sec." % (num_tests, match[1]))
            for match in re.findall("(- Passed: )(\d+)", output):
                num_success = match[1]
                logger.info("".join(match))
            for match in re.findall("(- Skipped: )(\d+)", output):
                num_skipped = match[1]
                logger.info("".join(match))
            for match in re.findall("(- Failed: )(\d+)", output):
                num_failures = match[1]
                logger.info("".join(match))
            success_testcases = ""
            for match in re.findall(r"\{0\}(.*?)[. ]*ok", output):
                success_testcases += match + ", "
            failed_testcases = ""
            for match in re.findall(r"\{0\}(.*?)[. ]*FAILED", output):
                failed_testcases += match + ", "
            skipped_testcases = ""
            for match in re.findall(r"\{0\}(.*?)[. ]*SKIPPED:", output):
                skipped_testcases += match + ", "

            num_executed = int(num_tests) - int(num_skipped)
            success_rate = 100 * int(num_success) / int(num_executed)

            self.details = {"tests": int(num_tests),
                            "failures": int(num_failures),
                            "success": success_testcases,
                            "errors": failed_testcases,
                            "skipped": skipped_testcases}
        except Exception:
            success_rate = 0

        self.criteria = ft_utils.check_success_rate(
            self.case_name, success_rate)
        logger.info("Testcase %s success_rate is %s%%, is marked as %s"
                    % (self.case_name, success_rate, self.criteria))

    def run(self):
        '''used for functest command line,
           functest testcase run refstack_defcore'''
        self.start_time = time.time()

        if not os.path.exists(conf_utils.REFSTACK_RESULTS_DIR):
            os.makedirs(conf_utils.REFSTACK_RESULTS_DIR)

        try:
            tempestconf = TempestConf()
            tempestconf.generate_tempestconf()
            self.source_venv()
            self.run_defcore_default()
            self.parse_refstack_result()
            res = testcase.TestCase.EX_OK
        except Exception as e:
            logger.error('Error with run: %s', e)
            res = testcase.TestCase.EX_RUN_ERROR

        self.stop_time = time.time()
        return res

    def _prep_test(self):
        '''Check that the config file exists.'''
        if not os.path.isfile(self.confpath):
            logger.error("Conf file not valid: %s" % self.confpath)
        if not os.path.isfile(self.testlist):
            logger.error("testlist file not valid: %s" % self.testlist)

    def main(self, **kwargs):
        '''used for manually running,
           python refstack_client.py -c <tempest_conf_path>
           --testlist <testlist_path>
           can generate a reference tempest.conf by
           python tempest_conf.py
        '''
        try:
            self.confpath = kwargs['config']
            self.testlist = kwargs['testlist']
        except KeyError as e:
            logger.error("Cannot run refstack client. Please check "
                         "%s", e)
            return self.EX_RUN_ERROR
        try:
            self.source_venv()
            self._prep_test()
            self.run_defcore(self.confpath, self.testlist)
            res = testcase.TestcaseBase.EX_OK
        except Exception as e:
            logger.error('Error with run: %s', e)
            res = testcase.TestCase.EX_RUN_ERROR

        return res


class RefstackClientParser(testcase.TestCase):

    def __init__(self):
        super(RefstackClientParser, self).__init__()
        self.FUNCTEST_TEST = CONST.dir_functest_test
        self.CONF_PATH = CONST.refstack_tempest_conf_path
        self.DEFCORE_LIST = CONST.refstack_defcore_list
        self.confpath = os.path.join(self.FUNCTEST_TEST,
                                     self.CONF_PATH)
        self.defcorelist = os.path.join(self.FUNCTEST_TEST,
                                        self.DEFCORE_LIST)
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-c', '--config',
            help='the file path of tempest.conf',
            default=self.confpath)
        self.parser.add_argument(
            '-t', '--testlist',
            help='Specify the file path or URL of a test list text file. '
                 'This test list will contain specific test cases that '
                 'should be tested.',
            default=self.defcorelist)

    def parse_args(self, argv=[]):
        return vars(self.parser.parse_args(argv))


if __name__ == '__main__':
    refstackclient = RefstackClient()
    parser = RefstackClientParser()
    args = parser.parse_args(sys.argv[1:])
    try:
        result = refstackclient.main(**args)
        if result != testcase.TestCase.EX_OK:
            sys.exit(result)
    except Exception:
        sys.exit(testcase.TestCase.EX_RUN_ERROR)
