#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0


import unittest
import logging

import mock

from functest.ci import run_tests
from functest.utils.constants import CONST


class RunTestsTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.sep = 'test_sep'
        self.creds = {'OS_AUTH_URL': 'test_os_auth_url',
                      'OS_USERNAME': 'test_os_username',
                      'OS_TENANT_NAME': 'test_tenant',
                      'OS_PASSWORD': 'test_password'}
        self.test = {'test_name': 'test_name'}
        self.tier = mock.Mock()
        attrs = {'get_name.return_value': 'test_tier',
                 'get_tests.return_value': ['test1', 'test2'],
                 'get_ci_loop.return_value': 'test_ci_loop',
                 'get_test_names.return_value': ['test1', 'test2']}
        self.tier.configure_mock(**attrs)

        self.tiers = mock.Mock()
        attrs = {'get_tiers.return_value': [self.tier]}
        self.tiers.configure_mock(**attrs)

    @mock.patch('functest.ci.run_tests.logger.info')
    def test_print_separator(self, mock_logger_info):
        run_tests.print_separator(self.sep)
        mock_logger_info.assert_called_once_with(self.sep * 44)

    @mock.patch('functest.ci.run_tests.logger.error')
    def test_source_rc_file_missing_file(self, mock_logger_error):
        with mock.patch('functest.ci.run_tests.os.path.isfile',
                        return_value=False), \
                self.assertRaises(SystemExit) as m:
            run_tests.source_rc_file()
            mock_logger_error.assert_called_once_with("RC file %s does"
                                                      " not exist..."
                                                      % CONST.openstack_creds)
            self.assertEqual(m.exception.code, 1)

    @mock.patch('functest.ci.run_tests.logger.debug')
    def test_source_rc_file_default(self, mock_logger_debug):
        with mock.patch('functest.ci.run_tests.os.path.isfile',
                        return_value=True), \
            mock.patch('functest.ci.run_tests.os_utils.source_credentials',
                       return_value=self.creds):
            run_tests.source_rc_file()

    @mock.patch('functest.ci.run_tests.os_snapshot.main')
    def test_generate_os_snapshot(self, mock_os_snap):
            run_tests.generate_os_snapshot()
            self.assertTrue(mock_os_snap.called)

    @mock.patch('functest.ci.run_tests.os_clean.main')
    def test_cleanup(self, mock_os_clean):
            run_tests.cleanup()
            self.assertTrue(mock_os_clean.called)

    def test_update_test_info(self):
        run_tests.GlobalVariables.EXECUTED_TEST_CASES = [self.test]
        run_tests.update_test_info('test_name',
                                   'test_result',
                                   'test_duration')
        exp = self.test
        exp.update({"result": 'test_result',
                    "duration": 'test_duration'})
        self.assertEqual(run_tests.GlobalVariables.EXECUTED_TEST_CASES,
                         [exp])

    def test_get_run_dict_if_defined_default(self):
        mock_obj = mock.Mock()
        with mock.patch('functest.ci.run_tests.'
                        'ft_utils.get_dict_by_test',
                        return_value={'run': mock_obj}):
            self.assertEqual(run_tests.get_run_dict_if_defined('test_name'),
                             mock_obj)

    @mock.patch('functest.ci.run_tests.logger.error')
    def test_get_run_dict_if_defined_missing_config_option(self,
                                                           mock_logger_error):
        with mock.patch('functest.ci.run_tests.'
                        'ft_utils.get_dict_by_test',
                        return_value=None):
            testname = 'test_name'
            self.assertEqual(run_tests.get_run_dict_if_defined(testname),
                             None)
            mock_logger_error.assert_called_once_with("Cannot get {}'s config "
                                                      "options"
                                                      .format(testname))

        with mock.patch('functest.ci.run_tests.'
                        'ft_utils.get_dict_by_test',
                        return_value={}):
            testname = 'test_name'
            self.assertEqual(run_tests.get_run_dict_if_defined(testname),
                             None)

    @mock.patch('functest.ci.run_tests.logger.exception')
    def test_get_run_dict_if_defined_exception(self,
                                               mock_logger_except):
        with mock.patch('functest.ci.run_tests.'
                        'ft_utils.get_dict_by_test',
                        side_effect=Exception):
            testname = 'test_name'
            self.assertEqual(run_tests.get_run_dict_if_defined(testname),
                             None)
            mock_logger_except.assert_called_once_with("Cannot get {}'s config"
                                                       " options"
                                                       .format(testname))
    # TODO: run_test

    @mock.patch('functest.ci.run_tests.logger.info')
    def test_run_tier_default(self, mock_logger_info):
        with mock.patch('functest.ci.run_tests.print_separator'), \
                mock.patch('functest.ci.run_tests.run_test') as mock_method:
            run_tests.run_tier(self.tier)
            mock_method.assert_any_call('test1', 'test_tier')
            mock_method.assert_any_call('test2', 'test_tier')
            self.assertTrue(mock_logger_info.called)

    @mock.patch('functest.ci.run_tests.logger.info')
    def test_run_tier_missing_test(self, mock_logger_info):
        with mock.patch('functest.ci.run_tests.print_separator'):
            self.tier.get_tests.return_value = None
            self.assertEqual(run_tests.run_tier(self.tier), 0)
            self.assertTrue(mock_logger_info.called)

    @mock.patch('functest.ci.run_tests.logger.info')
    def test_run_all_default(self, mock_logger_info):
        with mock.patch('functest.ci.run_tests.run_tier') as mock_method, \
            mock.patch('functest.ci.run_tests.generate_report.init'), \
                mock.patch('functest.ci.run_tests.generate_report.main'):
            CONST.CI_LOOP = 'test_ci_loop'
            run_tests.run_all(self.tiers)
            mock_method.assert_any_call(self.tier)
            self.assertTrue(mock_logger_info.called)

    @mock.patch('functest.ci.run_tests.logger.info')
    def test_run_all__missing_tier(self, mock_logger_info):
        with mock.patch('functest.ci.run_tests.generate_report.init'), \
                mock.patch('functest.ci.run_tests.generate_report.main'):
            CONST.CI_LOOP = 'loop_re_not_available'
            run_tests.run_all(self.tiers)
            self.assertTrue(mock_logger_info.called)

    # TODO: main


if __name__ == "__main__":
    unittest.main(verbosity=2)
