#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock

from functest.ci import run_tests
from functest.utils.constants import CONST
from functest.core.testcase import TestCase


class FakeModule(TestCase):

    def run(self, **kwargs):
        return TestCase.EX_OK


class RunTestsTesting(unittest.TestCase):

    def setUp(self):
        self.runner = run_tests.Runner()
        mock_test_case = mock.Mock()
        mock_test_case.is_successful.return_value = TestCase.EX_OK
        self.runner.executed_test_cases['test1'] = mock_test_case
        self.runner.executed_test_cases['test2'] = mock_test_case
        self.sep = 'test_sep'
        self.creds = {'OS_AUTH_URL': 'http://test_ip:test_port/v2.0',
                      'OS_USERNAME': 'test_os_username',
                      'OS_TENANT_NAME': 'test_tenant',
                      'OS_PASSWORD': 'test_password'}
        self.test = {'test_name': 'test_name'}
        self.tier = mock.Mock()
        test1 = mock.Mock()
        test1.get_name.return_value = 'test1'
        test2 = mock.Mock()
        test2.get_name.return_value = 'test2'
        attrs = {'get_name.return_value': 'test_tier',
                 'get_tests.return_value': [test1, test2],
                 'get_ci_loop.return_value': 'test_ci_loop',
                 'get_test_names.return_value': ['test1', 'test2']}
        self.tier.configure_mock(**attrs)

        self.tiers = mock.Mock()
        attrs = {'get_tiers.return_value': [self.tier]}
        self.tiers.configure_mock(**attrs)

        self.run_tests_parser = run_tests.RunTestsParser()

    @mock.patch('functest.ci.run_tests.ft_utils.get_dict_by_test')
    def test_get_run_dict(self, *args):
        retval = {'run': mock.Mock()}
        args[0].return_value = retval
        self.assertEqual(self.runner.get_run_dict('test_name'), retval['run'])
        args[0].assert_called_once_with('test_name')

    @mock.patch('functest.ci.run_tests.LOGGER.error')
    @mock.patch('functest.ci.run_tests.ft_utils.get_dict_by_test',
                return_value=None)
    def test_get_run_dict_config_ko(self, *args):
        testname = 'test_name'
        self.assertEqual(self.runner.get_run_dict(testname), None)
        args[0].return_value = {}
        self.assertEqual(self.runner.get_run_dict(testname), None)
        calls = [mock.call(testname), mock.call(testname)]
        args[0].assert_has_calls(calls)
        calls = [mock.call("Cannot get %s's config options", testname),
                 mock.call("Cannot get %s's config options", testname)]
        args[1].assert_has_calls(calls)

    @mock.patch('functest.ci.run_tests.LOGGER.exception')
    @mock.patch('functest.ci.run_tests.ft_utils.get_dict_by_test',
                side_effect=Exception)
    def test_get_run_dict_exception(self, *args):
        testname = 'test_name'
        self.assertEqual(self.runner.get_run_dict(testname), None)
        args[1].assert_called_once_with(
            "Cannot get %s's config options", testname)

    @mock.patch('functest.ci.run_tests.Runner.get_run_dict',
                return_value=None)
    def test_run_tests_import_exception(self, *args):
        mock_test = mock.Mock()
        kwargs = {'get_name.return_value': 'test_name',
                  'needs_clean.return_value': False}
        mock_test.configure_mock(**kwargs)
        with self.assertRaises(Exception) as context:
            self.runner.run_test(mock_test)
        args[0].assert_called_with('test_name')
        msg = "Cannot import the class for the test case."
        self.assertTrue(msg in str(context.exception))

    @mock.patch('importlib.import_module', name="module",
                return_value=mock.Mock(test_class=mock.Mock(
                    side_effect=FakeModule)))
    @mock.patch('functest.utils.functest_utils.get_dict_by_test')
    def test_run_tests_default(self, *args):
        mock_test = mock.Mock()
        kwargs = {'get_name.return_value': 'test_name',
                  'needs_clean.return_value': True}
        mock_test.configure_mock(**kwargs)
        test_run_dict = {'module': 'test_module',
                         'class': 'test_class'}
        with mock.patch('functest.ci.run_tests.Runner.get_run_dict',
                        return_value=test_run_dict):
            self.runner.clean_flag = True
            self.runner.run_test(mock_test)
        args[0].assert_called_with('test_name')
        args[1].assert_called_with('test_module')
        self.assertEqual(self.runner.overall_result,
                         run_tests.Result.EX_OK)

    @mock.patch('functest.ci.run_tests.Runner.run_test',
                return_value=TestCase.EX_OK)
    def test_run_tier_default(self, *mock_methods):
        self.assertEqual(self.runner.run_tier(self.tier),
                         run_tests.Result.EX_OK)
        mock_methods[0].assert_called_with(mock.ANY)

    @mock.patch('functest.ci.run_tests.LOGGER.info')
    def test_run_tier_missing_test(self, mock_logger_info):
        self.tier.get_tests.return_value = None
        self.assertEqual(self.runner.run_tier(self.tier),
                         run_tests.Result.EX_ERROR)
        self.assertTrue(mock_logger_info.called)

    @mock.patch('functest.ci.run_tests.LOGGER.info')
    @mock.patch('functest.ci.run_tests.Runner.run_tier')
    @mock.patch('functest.ci.run_tests.Runner.summary')
    def test_run_all_default(self, *mock_methods):
        CONST.__setattr__('CI_LOOP', 'test_ci_loop')
        self.runner.run_all()
        mock_methods[1].assert_not_called()
        self.assertTrue(mock_methods[2].called)

    @mock.patch('functest.ci.run_tests.LOGGER.info')
    @mock.patch('functest.ci.run_tests.Runner.summary')
    def test_run_all_missing_tier(self, *mock_methods):
        CONST.__setattr__('CI_LOOP', 'loop_re_not_available')
        self.runner.run_all()
        self.assertTrue(mock_methods[1].called)

    @mock.patch('functest.utils.openstack_utils.source_credentials',
                side_effect=Exception)
    @mock.patch('functest.ci.run_tests.Runner.summary')
    def test_main_failed(self, *mock_methods):
        kwargs = {'test': 'test_name', 'noclean': True, 'report': True}
        args = {'get_tier.return_value': False,
                'get_test.return_value': False}
        self.runner.tiers = mock.Mock()
        self.runner.tiers.configure_mock(**args)
        self.assertEqual(self.runner.main(**kwargs),
                         run_tests.Result.EX_ERROR)
        mock_methods[1].assert_called_once_with(
            '/home/opnfv/functest/conf/env_file')

    @mock.patch('functest.utils.openstack_utils.source_credentials')
    @mock.patch('functest.ci.run_tests.Runner.run_test',
                return_value=TestCase.EX_OK)
    @mock.patch('functest.ci.run_tests.Runner.summary')
    def test_main_tier(self, *mock_methods):
        mock_tier = mock.Mock()
        test_mock = mock.Mock()
        test_mock.get_name.return_value = 'test1'
        args = {'get_name.return_value': 'tier_name',
                'get_tests.return_value': [test_mock]}
        mock_tier.configure_mock(**args)
        kwargs = {'test': 'tier_name', 'noclean': True, 'report': True}
        args = {'get_tier.return_value': mock_tier,
                'get_test.return_value': None}
        self.runner.tiers = mock.Mock()
        self.runner.tiers.configure_mock(**args)
        self.assertEqual(self.runner.main(**kwargs),
                         run_tests.Result.EX_OK)
        mock_methods[1].assert_called()

    @mock.patch('functest.utils.openstack_utils.source_credentials')
    @mock.patch('functest.ci.run_tests.Runner.run_test',
                return_value=TestCase.EX_OK)
    def test_main_test(self, *mock_methods):
        kwargs = {'test': 'test_name', 'noclean': True, 'report': True}
        args = {'get_tier.return_value': None,
                'get_test.return_value': 'test_name'}
        self.runner.tiers = mock.Mock()
        mock_methods[1].return_value = self.creds
        self.runner.tiers.configure_mock(**args)
        self.assertEqual(self.runner.main(**kwargs),
                         run_tests.Result.EX_OK)
        mock_methods[0].assert_called_once_with('test_name')

    @mock.patch('functest.utils.openstack_utils.source_credentials')
    @mock.patch('functest.ci.run_tests.Runner.run_all')
    @mock.patch('functest.ci.run_tests.Runner.summary')
    def test_main_all_tier(self, *args):
        kwargs = {'get_tier.return_value': None,
                  'get_test.return_value': None}
        self.runner.tiers = mock.Mock()
        self.runner.tiers.configure_mock(**kwargs)
        self.assertEqual(
            self.runner.main(test='all', noclean=True, report=True),
            run_tests.Result.EX_OK)
        args[0].assert_called_once_with(None)
        args[1].assert_called_once_with()
        args[2].assert_called_once_with('/home/opnfv/functest/conf/env_file')

    @mock.patch('functest.utils.openstack_utils.source_credentials')
    def test_main_any_tier_test_ko(self, *args):
        kwargs = {'get_tier.return_value': None,
                  'get_test.return_value': None}
        self.runner.tiers = mock.Mock()
        self.runner.tiers.configure_mock(**kwargs)
        self.assertEqual(
            self.runner.main(test='any', noclean=True, report=True),
            run_tests.Result.EX_ERROR)
        args[0].assert_called_once_with('/home/opnfv/functest/conf/env_file')


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
