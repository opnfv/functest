#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import os
import unittest

import mock
import pkg_resources

from functest.core import testcase
from functest.opnfv_tests.openstack.refstack_client.refstack_client import \
    RefstackClient, RefstackClientParser

from snaps.openstack.os_credentials import OSCreds

__author__ = ("Matthew Li <matthew.lijun@huawei.com>,"
              "Linda Wang <wangwulin@huawei.com>")


class OSRefstackClientTesting(unittest.TestCase):
    """The class testing RefstackClient """
    # pylint: disable=missing-docstring, too-many-public-methods

    _config = pkg_resources.resource_filename(
        'functest',
        'opnfv_tests/openstack/refstack_client/refstack_tempest.conf')

    def setUp(self):
        self.default_args = {'config': None,
                             'testlist': RefstackClient.defcorelist}
        os.environ['OS_AUTH_URL'] = 'https://ip:5000/v3'
        os.environ['OS_INSECURE'] = 'true'
        self.case_name = 'refstack_defcore'
        self.result = 0
        self.os_creds = OSCreds(
            username='user', password='pass',
            auth_url='http://foo.com:5000/v3', project_name='bar')
        self.details = {"tests": 3,
                        "failures": 1,
                        "success": ['tempest.api.compute [18.464988s]'],
                        "errors": ['tempest.api.volume [0.230334s]'],
                        "skipped": ['tempest.api.network [1.265828s]']}

    def _create_client(self):
        with mock.patch('snaps.openstack.tests.openstack_tests.'
                        'get_credentials', return_value=self.os_creds):
            return RefstackClient()

    @mock.patch('functest.utils.functest_utils.execute_command')
    def test_run_defcore_insecure(self, m_cmd):
        insecure = '-k'
        config = 'tempest.conf'
        testlist = 'testlist'
        client = self._create_client()
        cmd = ("refstack-client test {0} -c {1} -v --test-list {2}".format(
            insecure, config, testlist))
        client.run_defcore(config, testlist)
        m_cmd.assert_any_call(cmd)

    @mock.patch('functest.utils.functest_utils.execute_command')
    def test_run_defcore(self, m_cmd):
        os.environ['OS_AUTH_URL'] = 'http://ip:5000/v3'
        insecure = ''
        config = 'tempest.conf'
        testlist = 'testlist'
        client = self._create_client()
        cmd = ("refstack-client test {0} -c {1} -v --test-list {2}".format(
            insecure, config, testlist))
        client.run_defcore(config, testlist)
        m_cmd.assert_any_call(cmd)

    @mock.patch('functest.opnfv_tests.openstack.refstack_client.'
                'refstack_client.LOGGER.info')
    @mock.patch('__builtin__.open', side_effect=Exception)
    def test_parse_refstack_result_fail(self, *args):
        self._create_client().parse_refstack_result()
        args[1].assert_called_once_with(
            "Testcase %s success_rate is %s%%",
            self.case_name, self.result)

    def test_parse_refstack_result_ok(self):
        log_file = ('''
                    {0} tempest.api.compute [18.464988s] ... ok
                    {0} tempest.api.volume [0.230334s] ... FAILED
                    {0} tempest.api.network [1.265828s] ... SKIPPED:
                    Ran: 3 tests in 1259.0000 sec.
                    - Passed: 1
                    - Skipped: 1
                    - Failed: 1
                   ''')
        client = self._create_client()
        with mock.patch('__builtin__.open',
                        mock.mock_open(read_data=log_file)):
            client.parse_refstack_result()
            self.assertEqual(client.details, self.details)

    def _get_main_kwargs(self, key=None):
        kwargs = {'config': self._config,
                  'testlist': RefstackClient.defcorelist}
        if key:
            del kwargs[key]
        return kwargs

    def _test_main_missing_keyword(self, key):
        kwargs = self._get_main_kwargs(key)
        client = self._create_client()
        self.assertEqual(client.main(**kwargs),
                         testcase.TestCase.EX_RUN_ERROR)

    def test_main_missing_conf(self):
        self._test_main_missing_keyword('config')

    def test_main_missing_testlist(self):
        self._test_main_missing_keyword('testlist')

    def _test_argparser(self, arg, value):
        self.default_args[arg] = value
        parser = RefstackClientParser()
        self.assertEqual(parser.parse_args(["--{}={}".format(arg, value)]),
                         self.default_args)

    def test_argparser_conf(self):
        self._test_argparser('config', self._config)

    def test_argparser_testlist(self):
        self._test_argparser('testlist', RefstackClient.defcorelist)

    def test_argparser_multiple_args(self):
        self.default_args['config'] = self._config
        self.default_args['testlist'] = RefstackClient.defcorelist
        parser = RefstackClientParser()
        self.assertEqual(parser.parse_args(
            ["--config={}".format(self._config),
             "--testlist={}".format(RefstackClient.defcorelist)]),
                         self.default_args)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
