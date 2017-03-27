#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import os
import unittest

from functest.core import testcase_base
from functest.opnfv_tests.openstack.refstack_client import refstack_client
from functest.utils.constants import CONST


class OSRefstackClientTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)
    _config = \
        os.path.join(CONST.dir_functest_test, CONST.refstack_tempest_conf_path)
    _testlist = \
        os.path.join(CONST.dir_functest_test, CONST.refstack_defcore_list)

    def setUp(self):
        self.defaultargs = {'config': self._config,
                            'testlist': self._testlist}
        self.refstackclient = refstack_client.RefstackClient()

    def test_source_venv(self):
        CONST.dir_refstack_client = 'test_repo_dir'
        with mock.patch('functest.opnfv_tests.openstack.refstack_client.'
                        'refstack_client.ft_utils.execute_command') as m:
            cmd = ("cd {0};"
                   ". .venv/bin/activate;"
                   "cd -;".format(CONST.dir_refstack_client))
            self.refstackclient.source_venv()
            m.assert_any_call(cmd)

    def test_run_defcore(self):
        config = 'tempest.conf'
        testlist = 'testlist'
        with mock.patch('functest.opnfv_tests.openstack.refstack_client.'
                        'refstack_client.ft_utils.execute_command') as m:
            cmd = ("cd {0};"
                   "./refstack-client test -c {1} -v --test-list {2};"
                   "cd -;".format(CONST.dir_refstack_client,
                                  config,
                                  testlist))
            self.refstackclient.run_defcore(config, testlist)
            m.assert_any_call(cmd)

    def _get_main_kwargs(self, key=None):
        kwargs = {'config': self._config,
                  'testlist': self._testlist}
        if key:
            del kwargs[key]
        return kwargs

    def _test_main(self, status, *args):
        kwargs = self._get_main_kwargs()
        self.assertEqual(self.refstackclient.main(**kwargs), status)
        if len(args) > 0:
            args[0].assert_called_once_with(
                 refstack_client.RefstackClient.result_dir)
        if len(args) > 1:
            args

    def _test_main_missing_keyword(self, key):
        kwargs = self._get_main_kwargs(key)
        self.assertEqual(self.refstackclient.main(**kwargs),
                         testcase_base.TestCase.EX_RUN_ERROR)

    def test_main_missing_conf(self):
        self._test_main_missing_keyword('config')

    def test_main_missing_testlist(self):
        self._test_main_missing_keyword('testlist')

    def _test_argparser(self, arg, value):
        self.defaultargs[arg] = value
        parser = refstack_client.RefstackClientParser()
        self.assertEqual(parser.parse_args(["--{}={}".format(arg, value)]),
                         self.defaultargs)

    def test_argparser_conf(self):
        self._test_argparser('config', self._config)

    def test_argparser_testlist(self):
        self._test_argparser('testlist', self._testlist)

    def test_argparser_multiple_args(self):
        self.defaultargs['config'] = self._config
        self.defaultargs['testlist'] = self._testlist
        parser = refstack_client.RefstackClientParser()
        self.assertEqual(parser.parse_args(
            ["--config={}".format(self._config),
             "--testlist={}".format(self._testlist)
             ]), self.defaultargs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
