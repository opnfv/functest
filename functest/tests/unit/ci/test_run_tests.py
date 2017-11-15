#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest
import os

import mock

from functest.ci import run_tests
from functest.utils.constants import CONST
from functest.core.testcase import TestCase


class FakeModule(TestCase):

    def run(self):
        return TestCase.EX_OK

    def push_to_db(self):
        return TestCase.EX_OK

    def is_successful(self):
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

    @mock.patch('functest.ci.run_tests.Runner.patch_file')
    @mock.patch('functest.ci.run_tests.Runner.update_db_url')
    @mock.patch.dict(os.environ, {'POD_ARCH': 'aarch64'})
    @mock.patch.dict(os.environ, {'TEST_DB_URL': 'somevalue'})
    def test_update_config_file_default(self, *mock_methods):
        self.runner.update_config_file()
        self.assertTrue(mock_methods[0].called)
        self.assertTrue(mock_methods[1].called)

    @mock.patch('functest.ci.run_tests.logger.error')
    def test_source_rc_file_missing_file(self, mock_logger_error):
        with mock.patch('functest.ci.run_tests.os.path.isfile',
                        return_value=False), \
                self.assertRaises(Exception):
            self.runner.source_rc_file()

    @mock.patch('functest.ci.run_tests.logger.debug')
    @mock.patch('functest.ci.run_tests.os.path.isfile',
                return_value=True)
    def test_source_rc_file_default(self, *args):
        with mock.patch('functest.ci.run_tests.os_utils.source_credentials',
                        return_value=self.creds):
            self.runner.source_rc_file()

    def test_get_run_dict_if_defined_default(self):
        mock_obj = mock.Mock()
        with mock.patch('functest.ci.run_tests.'
                        'ft_utils.get_dict_by_test',
                        return_value={'run': mock_obj}):
            self.assertEqual(self.runner.get_run_dict('test_name'),
                             mock_obj)

    @mock.patch('functest.ci.run_tests.logger.error')
    def test_get_run_dict_if_defined_missing_config_option(self,
                                                           mock_logger_error):
        with mock.patch('functest.ci.run_tests.'
                        'ft_utils.get_dict_by_test',
                        return_value=None):
            testname = 'test_name'
            self.assertEqual(self.runner.get_run_dict(testname),
                             None)
            mock_logger_error.assert_called_once_with("Cannot get {}'s config "
                                                      "options"
                                                      .format(testname))

        with mock.patch('functest.ci.run_tests.'
                        'ft_utils.get_dict_by_test',
                        return_value={}):
            testname = 'test_name'
            self.assertEqual(self.runner.get_run_dict(testname),
                             None)

    @mock.patch('functest.ci.run_tests.logger.exception')
    def test_get_run_dict_if_defined_exception(self,
                                               mock_logger_except):
        with mock.patch('functest.ci.run_tests.'
                        'ft_utils.get_dict_by_test',
                        side_effect=Exception):
            testname = 'test_name'
            self.assertEqual(self.runner.get_run_dict(testname),
                             None)
            mock_logger_except.assert_called_once_with("Cannot get {}'s config"
                                                       " options"
                                                       .format(testname))

    def test_run_tests_import_test_class_exception(self):
        mock_test = mock.Mock()
        args = {'get_name.return_value': 'test_name',
                'needs_clean.return_value': False}
        mock_test.configure_mock(**args)
        with mock.patch('functest.ci.run_tests.Runner.source_rc_file'), \
            mock.patch('functest.ci.run_tests.Runner.get_run_dict',
                       return_value=None), \
                self.assertRaises(Exception) as context:
            self.runner(mock_test, 'tier_name')
            msg = "Cannot import the class for the test case."
            self.assertTrue(msg in context)

    @mock.patch('functest.ci.run_tests.Runner.source_rc_file')
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
        self.assertEqual(self.runner.overall_result,
                         run_tests.Result.EX_OK)

    @mock.patch('functest.ci.run_tests.Runner.run_test',
                return_value=TestCase.EX_OK)
    def test_run_tier_default(self, *mock_methods):
        self.assertEqual(self.runner.run_tier(self.tier),
                         run_tests.Result.EX_OK)
        mock_methods[0].assert_called_with(mock.ANY)

    @mock.patch('functest.ci.run_tests.logger.info')
    def test_run_tier_missing_test(self, mock_logger_info):
        self.tier.get_tests.return_value = None
        self.assertEqual(self.runner.run_tier(self.tier),
                         run_tests.Result.EX_ERROR)
        self.assertTrue(mock_logger_info.called)

    @mock.patch('functest.ci.run_tests.logger.info')
    @mock.patch('functest.ci.run_tests.Runner.run_tier')
    @mock.patch('functest.ci.run_tests.Runner.summary')
    def test_run_all_default(self, *mock_methods):
        CONST.__setattr__('CI_LOOP', 'test_ci_loop')
        self.runner.run_all()
        mock_methods[1].assert_not_called()
        self.assertTrue(mock_methods[2].called)

    @mock.patch('functest.ci.run_tests.logger.info')
    @mock.patch('functest.ci.run_tests.Runner.summary')
    def test_run_all_missing_tier(self, *mock_methods):
        CONST.__setattr__('CI_LOOP', 'loop_re_not_available')
        self.runner.run_all()
        self.assertTrue(mock_methods[1].called)

    @mock.patch('functest.ci.run_tests.Runner.source_rc_file',
                side_effect=Exception)
    @mock.patch('functest.ci.run_tests.Runner.summary')
    def test_main_failed(self, *mock_methods):
        kwargs = {'test': 'test_name', 'noclean': True, 'report': True}
        args = {'get_tier.return_value': False,
                'get_test.return_value': False}
        self.runner._tiers = mock.Mock()
        self.runner._tiers.configure_mock(**args)
        self.assertEqual(self.runner.main(**kwargs),
                         run_tests.Result.EX_ERROR)
        mock_methods[1].assert_called_once_with()

    @mock.patch('functest.ci.run_tests.Runner.source_rc_file')
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
        self.runner._tiers = mock.Mock()
        self.runner._tiers.configure_mock(**args)
        self.assertEqual(self.runner.main(**kwargs),
                         run_tests.Result.EX_OK)
        mock_methods[1].assert_called()

    @mock.patch('functest.ci.run_tests.Runner.source_rc_file')
    @mock.patch('functest.ci.run_tests.Runner.run_test',
                return_value=TestCase.EX_OK)
    def test_main_test(self, *mock_methods):
        kwargs = {'test': 'test_name', 'noclean': True, 'report': True}
        args = {'get_tier.return_value': None,
                'get_test.return_value': 'test_name'}
        self.runner._tiers = mock.Mock()
        self.runner._tiers.configure_mock(**args)
        self.assertEqual(self.runner.main(**kwargs),
                         run_tests.Result.EX_OK)
        mock_methods[0].assert_called_once_with('test_name')

    @mock.patch('functest.ci.run_tests.Runner.source_rc_file')
    @mock.patch('functest.ci.run_tests.Runner.run_all')
    @mock.patch('functest.ci.run_tests.Runner.summary')
    def test_main_all_tier(self, *mock_methods):
        kwargs = {'test': 'all', 'noclean': True, 'report': True}
        args = {'get_tier.return_value': None,
                'get_test.return_value': None}
        self.runner._tiers = mock.Mock()
        self.runner._tiers.configure_mock(**args)
        self.assertEqual(self.runner.main(**kwargs),
                         run_tests.Result.EX_OK)
        mock_methods[1].assert_called_once_with()

    @mock.patch('functest.ci.run_tests.Runner.source_rc_file')
    @mock.patch('functest.ci.run_tests.Runner.summary')
    def test_main_any_tier_test_ko(self, *mock_methods):
        kwargs = {'test': 'any', 'noclean': True, 'report': True}
        args = {'get_tier.return_value': None,
                'get_test.return_value': None}
        self.runner._tiers = mock.Mock()
        self.runner._tiers.configure_mock(**args)
        self.assertEqual(self.runner.main(**kwargs),
                         run_tests.Result.EX_ERROR)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
