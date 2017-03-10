#!/usr/bin/env python

# matthew.lijun@huawei.com wangwulin@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
import argparse
import os
import sys

import refstack_conf

from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.core import testcase_base
from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.ci.run_tests as run_test

""" logging configuration """
logger = ft_logger.Logger("refstack_defcore").getLogger()


class RefstackClient(testcase_base.TestcaseBase):

    def __init__(self):
        super(RefstackClient, self).__init__()
        self.REPO_DIR = CONST.dir_refstack_client
        self.FUNCTEST_TEST = CONST.dir_functest_test
        self.CONF_PATH = CONST.refstack_tempest_conf_path
        self.DEFCORE_LIST = CONST.refstack_defcore_list
        self.confpath = os.path.join(self.FUNCTEST_TEST,
                                      self.CONF_PATH)
        self.defcorelist = os.path.join(self.FUNCTEST_TEST,
                                         self.DEFCORE_LIST)
        self.VERIFIER_ID = conf_utils.get_verifier_id()
        self.VERIFIER_REPO_DIR = conf_utils.get_verifier_repo_dir(
            self.VERIFIER_ID)
        self.DEPLOYMENT_ID = conf_utils.get_verifier_deployment_id()
        self.DEPLOYMENT_DIR = conf_utils.get_verifier_deployment_dir(
            self.VERIFIER_ID, self.DEPLOYMENT_ID)

    def source_venv(self):

        cmd = ("cd {0};"
               ". .venv/bin/activate;"
               "cd -;".format(self.REPO_DIR))
        ft_utils.execute_command(cmd)

    def run_defcore(self, conf, testlist):
        logger.debug("Generating test case list...")

        cmd = ("cd {0};"
               "./refstack-client test -c {1} -v --test-list {2};"
               "cd -;".format(self.REPO_DIR,
                              conf,
                              testlist))
        ft_utils.execute_command(cmd)

    def run_defcore_default(self):
        logger.debug("Generating test case list...")

        cmd = ("cd {0};"
               "./refstack-client test -c {1} -v --test-list {2};"
               "cd -;".format(self.REPO_DIR,
                              self.confpath,
                              self.defcorelist))
        ft_utils.execute_command(cmd)

    def run(self):
        try:
            run_test.source_rc_file()
            image_id, image_id_alt = refstack_conf.create_tempest_resources()
            refstack_conf.configure_tempest(
                self.DEPLOYMENT_DIR, image_id, image_id_alt)
        except KeyError as e:
            logger.error("Cannot run refstack client. Please check "
                              "%s", e)
            return self.EX_RUN_ERROR
        try:
            self.source_venv()
            self.run_defcore_default()
            res = testcase_base.TestcaseBase.EX_OK
        except Exception as e:
            logger.error('Error with run: %s', e)
            res = testcase_base.TestcaseBase.EX_RUN_ERROR

        return res

    def main(self, **kwargs):
        try:
            tempestconf = kwargs['config']
            testlist = kwargs['testlist']
        except KeyError as e:
            logger.error("Cannot run refstack client. Please check "
                              "%s", e)
            return self.EX_RUN_ERROR
        try:
            run_test.source_rc_file()
            image_id, image_id_alt = refstack_conf.create_tempest_resources()
            refstack_conf.configure_tempest(
                self.DEPLOYMENT_DIR, image_id, image_id_alt)
        except KeyError as e:
            logger.error("Cannot run refstack client. Please check "
                              "%s", e)
            return self.EX_RUN_ERROR
        try:
            self.source_venv()
            self.run_defcore(tempestconf, testlist)
            res = testcase_base.TestcaseBase.EX_OK
        except Exception as e:
            logger.error('Error with run: %s', e)
            res = testcase_base.TestcaseBase.EX_RUN_ERROR

        return res


class RefstackClientParser(testcase_base.TestcaseBase):

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
        if result != testcase_base.TestcaseBase.EX_OK:
            sys.exit(result)
    except Exception:
        sys.exit(testcase_base.TestcaseBase.EX_RUN_ERROR)
