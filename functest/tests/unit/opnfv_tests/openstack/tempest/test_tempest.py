#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.core import testcase
from functest.opnfv_tests.openstack.tempest import tempest
from functest.opnfv_tests.openstack.tempest import conf_utils


class OSTempestTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'conf_utils.get_verifier_id',
                        return_value='test_deploy_id'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.get_verifier_deployment_id',
                       return_value='test_deploy_id'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.get_verifier_repo_dir',
                       return_value='test_verifier_repo_dir'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.get_verifier_deployment_dir',
                       return_value='test_verifier_deploy_dir'):
            self.tempestcommon = tempest.TempestCommon()

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.logger.debug')
    def test_generate_test_list_defcore_mode(self, mock_logger_debug):
        self.tempestcommon.MODE = 'defcore'
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'shutil.copyfile') as m:
            self.tempestcommon.generate_test_list('test_verifier_repo_dir')
            self.assertTrue(m.called)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.logger.error')
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.logger.debug')
    def test_generate_test_list_custom_mode_missing_file(self,
                                                         mock_logger_debug,
                                                         mock_logger_error):
        self.tempestcommon.MODE = 'custom'
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'os.path.isfile', return_value=False), \
                self.assertRaises(Exception) as context:
            msg = "Tempest test list file %s NOT found."
            self.tempestcommon.generate_test_list('test_verifier_repo_dir')
            self.assertTrue((msg % conf_utils.TEMPEST_CUSTOM) in context)

    def test_generate_test_list_custom_mode_default(self):
        self.tempestcommon.MODE = 'custom'
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'shutil.copyfile') as m, \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'os.path.isfile', return_value=True):
            self.tempestcommon.generate_test_list('test_verifier_repo_dir')
            self.assertTrue(m.called)

    def _test_generate_test_list_mode_default(self, mode):
        self.tempestcommon.MODE = mode
        if self.tempestcommon.MODE == 'smoke':
            testr_mode = "smoke"
        elif self.tempestcommon.MODE == 'feature_multisite':
            testr_mode = "'[Kk]ingbird'"
        elif self.tempestcommon.MODE == 'full':
            testr_mode = ""
        else:
            testr_mode = 'tempest.api.' + self.tempestcommon.MODE
        conf_utils.TEMPEST_RAW_LIST = 'raw_list'
        verifier_repo_dir = 'test_verifier_repo_dir'
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'ft_utils.execute_command') as m:
            cmd = ("cd {0};"
                   "testr list-tests {1} > {2};"
                   "cd -;".format(verifier_repo_dir,
                                  testr_mode,
                                  conf_utils.TEMPEST_RAW_LIST))
            self.tempestcommon.generate_test_list('test_verifier_repo_dir')
            m.assert_any_call(cmd)

    def test_generate_test_list_smoke_mode(self):
        self._test_generate_test_list_mode_default('smoke')

    def test_generate_test_list_feature_multisite_mode(self):
        self._test_generate_test_list_mode_default('feature_multisite')

    def test_generate_test_list_full_mode(self):
        self._test_generate_test_list_mode_default('full')

    def test_parse_verifier_result_missing_verification_uuid(self):
        self.tempestcommon.VERIFICATION_ID = ''
        with self.assertRaises(Exception):
            self.tempestcommon.parse_verifier_result()

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.logger.info')
    def test_parse_verifier_result_default(self, mock_logger_info):
        self.tempestcommon.VERIFICATION_ID = 'test_uuid'
        self.tempestcommon.case_name = 'test_case_name'
        stdout = ['Testscount||2', 'Success||2', 'Skipped||0', 'Failures||0']
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'subprocess.Popen') as mock_popen, \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'ft_utils.check_success_rate') as mock_method, \
                mock.patch('__builtin__.open', mock.mock_open()):
            mock_stdout = mock.Mock()
            attrs = {'stdout': stdout}
            mock_stdout.configure_mock(**attrs)
            mock_popen.return_value = mock_stdout

            self.tempestcommon.parse_verifier_result()
            mock_method.assert_any_call('test_case_name', 100)

    def test_run_missing_create_tempest_dir(self):
        ret = testcase.TestCase.EX_RUN_ERROR
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'os.path.exists', return_value=False), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'os.makedirs') as mock_os_makedirs, \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.create_tempest_resources',
                       return_value="image_and_flavor"):
            self.assertEqual(self.tempestcommon.run(),
                             ret)
            self.assertTrue(mock_os_makedirs.called)

    def test_run_missing_configure_tempest(self):
        ret = testcase.TestCase.EX_RUN_ERROR
        ret_ok = testcase.TestCase.EX_OK
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'os.path.exists', return_value=False), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'os.makedirs') as mock_os_makedirs, \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.create_tempest_resources',
                       return_value=ret_ok), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.configure_tempest',
                       return_value=ret):
            self.assertEqual(self.tempestcommon.run(),
                             ret)
            self.assertTrue(mock_os_makedirs.called)

    def test_run_missing_generate_test_list(self):
        ret = testcase.TestCase.EX_RUN_ERROR
        ret_ok = testcase.TestCase.EX_OK
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'os.path.exists', return_value=False), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'os.makedirs') as mock_os_makedirs, \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.create_tempest_resources',
                       return_value=ret_ok), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.configure_tempest',
                       return_value=ret_ok), \
            mock.patch.object(self.tempestcommon, 'generate_test_list',
                              return_value=ret):
            self.assertEqual(self.tempestcommon.run(),
                             ret)
            self.assertTrue(mock_os_makedirs.called)

    def test_run_missing_apply_tempest_blacklist(self):
        ret = testcase.TestCase.EX_RUN_ERROR
        ret_ok = testcase.TestCase.EX_OK
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'os.path.exists', return_value=False), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'os.makedirs') as mock_os_makedirs, \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.create_tempest_resources',
                       return_value=ret_ok), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.configure_tempest',
                       return_value=ret_ok), \
            mock.patch.object(self.tempestcommon, 'generate_test_list',
                              return_value=ret_ok), \
            mock.patch.object(self.tempestcommon, 'apply_tempest_blacklist',
                              return_value=ret):
            self.assertEqual(self.tempestcommon.run(),
                             ret)
            self.assertTrue(mock_os_makedirs.called)

    def test_run_missing_parse_verifier_result(self):
        ret = testcase.TestCase.EX_RUN_ERROR
        ret_ok = testcase.TestCase.EX_OK
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'os.path.exists', return_value=False), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'os.makedirs') as mock_os_makedirs, \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.create_tempest_resources',
                       return_value=ret_ok), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'conf_utils.configure_tempest',
                       return_value=ret_ok), \
            mock.patch.object(self.tempestcommon, 'generate_test_list',
                              return_value=ret_ok), \
            mock.patch.object(self.tempestcommon, 'apply_tempest_blacklist',
                              return_value=ret_ok), \
            mock.patch.object(self.tempestcommon, 'run_verifier_tests',
                              return_value=ret_ok), \
            mock.patch.object(self.tempestcommon, 'parse_verifier_result',
                              return_value=ret):
            self.assertEqual(self.tempestcommon.run(),
                             ret)
            self.assertTrue(mock_os_makedirs.called)


if __name__ == "__main__":
    unittest.main(verbosity=2)
