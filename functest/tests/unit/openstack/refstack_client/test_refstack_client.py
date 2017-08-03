#!/usr/bin/env python
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# matthew.lijun@huawei.com wangwulin@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import pkg_resources
import unittest

from functest.core import testcase
from functest.opnfv_tests.openstack.refstack_client import refstack_client
from functest.utils.constants import CONST


class OSRefstackClientTesting(unittest.TestCase):

    _config = pkg_resources.resource_filename(
        'functest',
        'opnfv_tests/openstack/refstack_client/refstack_tempest.conf')
    _testlist = pkg_resources.resource_filename(
        'functest', 'opnfv_tests/openstack/refstack_client/defcore.txt')

    def setUp(self):
        self.defaultargs = {'config': self._config,
                            'testlist': self._testlist}
        CONST.__setattr__('OS_AUTH_URL', 'https://ip:5000/v3')
        CONST.__setattr__('OS_INSECURE', 'true')
        self.refstackclient = refstack_client.RefstackClient()

    def test_run_defcore_insecure(self):
        insecure = '-k'
        config = 'tempest.conf'
        testlist = 'testlist'
        with mock.patch('functest.opnfv_tests.openstack.refstack_client.'
                        'refstack_client.ft_utils.execute_command') as m:
            cmd = ("refstack-client test {0} -c {1} -v --test-list {2}"
                   .format(insecure, config, testlist))
            self.refstackclient.run_defcore(config, testlist)
            m.assert_any_call(cmd)

    def test_run_defcore(self):
        CONST.__setattr__('OS_AUTH_URL', 'http://ip:5000/v3')
        refstackclient = refstack_client.RefstackClient()
        insecure = ''
        config = 'tempest.conf'
        testlist = 'testlist'
        with mock.patch('functest.opnfv_tests.openstack.refstack_client.'
                        'refstack_client.ft_utils.execute_command') as m:
            cmd = ("refstack-client test {0} -c {1} -v --test-list {2}"
                   .format(insecure, config, testlist))
            refstackclient.run_defcore(config, testlist)
            m.assert_any_call(cmd)

    @mock.patch('functest.opnfv_tests.openstack.refstack_client.'
                'refstack_client.LOGGER.info')
    @mock.patch('__builtin__.open', side_effect=Exception)
    def test_parse_refstack_result_missing_log_file(self, mock_open,
                                                    mock_logger_info):
        self.case_name = 'refstack_defcore'
        self.result = 0
        self.refstackclient.parse_refstack_result()
        mock_logger_info.assert_called_once_with(
            "Testcase %s success_rate is %s%%",
            self.case_name, self.result)

    def test_parse_refstack_result_default(self):
        log_file = ('''
                    {0} tempest.api.compute [18.464988s] ... ok
                    {0} tempest.api.volume [0.230334s] ... FAILED
                    {0} tempest.api.network [1.265828s] ... SKIPPED:
                    Ran: 3 tests in 1259.0000 sec.
                    - Passed: 1
                    - Skipped: 1
                    - Failed: 1
                   ''')
        self.details = {"tests": 3,
                        "failures": 1,
                        "success": [' tempest.api.compute [18.464988s]'],
                        "errors": [' tempest.api.volume [0.230334s]'],
                        "skipped": [' tempest.api.network [1.265828s]']}
        with mock.patch('__builtin__.open',
                        mock.mock_open(read_data=log_file)):
            self.refstackclient.parse_refstack_result()
            self.assertEqual(self.refstackclient.details, self.details)

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
                         testcase.TestCase.EX_RUN_ERROR)

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
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
