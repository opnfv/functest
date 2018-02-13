#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock

from functest.core import testcase
from functest.opnfv_tests.openstack.tempest import tempest
from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils.constants import CONST

from snaps.openstack.os_credentials import OSCreds


class OSTempestTesting(unittest.TestCase):

    def setUp(self):
        os_creds = OSCreds(
            username='user', password='pass',
            auth_url='http://foo.com:5000/v3', project_name='bar')

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
                       return_value='test_verifier_deploy_dir'), \
            mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                       'get_credentials',
                       return_value=os_creds):
            self.tempestcommon = tempest.TempestCommon()
            self.tempestsmoke_serial = tempest.TempestSmokeSerial()
            self.tempestsmoke_parallel = tempest.TempestSmokeParallel()
            self.tempestfull_parallel = tempest.TempestFullParallel()
            self.tempestcustom = tempest.TempestCustom()
            self.tempestdefcore = tempest.TempestDefcore()

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.LOGGER.debug')
    def test_gen_tl_defcore_mode(self, mock_logger_debug):
        # pylint: disable=unused-argument
        self.tempestcommon.mode = 'defcore'
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'shutil.copyfile') as mock_copyfile:
            self.tempestcommon.generate_test_list('test_verifier_repo_dir')
            self.assertTrue(mock_copyfile.called)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.LOGGER.error')
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.LOGGER.debug')
    def test_gen_tl_cm_missing_file(self, mock_logger_debug,
                                    mock_logger_error):
        # pylint: disable=unused-argument
        self.tempestcommon.mode = 'custom'
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'os.path.isfile', return_value=False), \
                self.assertRaises(Exception) as context:
            msg = "Tempest test list file %s NOT found."
            self.tempestcommon.generate_test_list('test_verifier_repo_dir')
            self.assertTrue((msg % conf_utils.TEMPEST_CUSTOM) in context)

    def test_gen_tl_cm_default(self):
        self.tempestcommon.mode = 'custom'
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'shutil.copyfile') as mock_copyfile, \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'os.path.isfile', return_value=True):
            self.tempestcommon.generate_test_list('test_verifier_repo_dir')
            self.assertTrue(mock_copyfile.called)

    def _test_gen_tl_mode_default(self, mode):
        self.tempestcommon.mode = mode
        if self.tempestcommon.mode == 'smoke':
            testr_mode = "smoke"
        elif self.tempestcommon.mode == 'full':
            testr_mode = ""
        else:
            testr_mode = 'tempest.api.' + self.tempestcommon.mode
        conf_utils.TEMPEST_RAW_LIST = 'raw_list'
        verifier_repo_dir = 'test_verifier_repo_dir'
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'ft_utils.execute_command') as mock_exec:
            cmd = ("cd {0};"
                   "testr list-tests {1} > {2};"
                   "cd -;".format(verifier_repo_dir, testr_mode,
                                  conf_utils.TEMPEST_RAW_LIST))
            self.tempestcommon.generate_test_list('test_verifier_repo_dir')
            mock_exec.assert_any_call(cmd)

    def test_gen_tl_smoke_mode(self):
        self._test_gen_tl_mode_default('smoke')

    def test_gen_tl_full_mode(self):
        self._test_gen_tl_mode_default('full')

    def test_verif_res_missing_verif_id(self):
        self.tempestcommon.verification_id = None
        with self.assertRaises(Exception):
            self.tempestcommon.parse_verifier_result()

    def test_apply_missing_blacklist(self):
        with mock.patch('__builtin__.open', mock.mock_open()) as mock_open, \
            mock.patch.object(self.tempestcommon, 'read_file',
                              return_value=['test1', 'test2']):
            conf_utils.TEMPEST_BLACKLIST = Exception
            CONST.__setattr__('INSTALLER_TYPE', 'installer_type')
            CONST.__setattr__('DEPLOY_SCENARIO', 'deploy_scenario')
            self.tempestcommon.apply_tempest_blacklist()
            obj = mock_open()
            obj.write.assert_any_call('test1\n')
            obj.write.assert_any_call('test2\n')

    def test_apply_blacklist_default(self):
        item_dict = {'scenarios': ['deploy_scenario'],
                     'installers': ['installer_type'],
                     'tests': ['test2']}
        with mock.patch('__builtin__.open', mock.mock_open()) as mock_open, \
            mock.patch.object(self.tempestcommon, 'read_file',
                              return_value=['test1', 'test2']), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'yaml.safe_load', return_value=item_dict):
            CONST.__setattr__('INSTALLER_TYPE', 'installer_type')
            CONST.__setattr__('DEPLOY_SCENARIO', 'deploy_scenario')
            self.tempestcommon.apply_tempest_blacklist()
            obj = mock_open()
            obj.write.assert_any_call('test1\n')
            self.assertFalse(obj.write.assert_any_call('test2\n'))

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.LOGGER.info')
    def test_run_verifier_tests_default(self, mock_logger_info):
        with mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch('__builtin__.iter', return_value=[r'\} tempest\.']), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'subprocess.Popen'):
            conf_utils.TEMPEST_LIST = 'test_tempest_list'
            cmd = ["rally", "verify", "start", "--load-list",
                   conf_utils.TEMPEST_LIST]
            self.tempestcommon.run_verifier_tests()
            mock_logger_info. \
                assert_any_call("Starting Tempest test suite: '%s'.", cmd)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'os.path.exists', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.os.makedirs',
                side_effect=Exception)
    def test_run_makedirs_ko(self, *args):
        # pylint: disable=unused-argument
        self.assertEqual(self.tempestcommon.run(),
                         testcase.TestCase.EX_RUN_ERROR)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'os.path.exists', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'TempestResourcesManager.create', side_effect=Exception)
    def test_run_create_resources_ko(self, *args):
        # pylint: disable=unused-argument
        self.assertEqual(self.tempestcommon.run(),
                         testcase.TestCase.EX_RUN_ERROR)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'os.path.exists', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'TempestResourcesManager.create', return_value={})
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_active_compute_cnt', side_effect=Exception)
    def test_run_get_active_comp_cnt_ko(self, *args):
        # pylint: disable=unused-argument
        self.assertEqual(self.tempestcommon.run(),
                         testcase.TestCase.EX_RUN_ERROR)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'os.path.exists', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'TempestResourcesManager.create', return_value={})
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_active_compute_cnt', return_value=2)
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'conf_utils.configure_tempest', side_effect=Exception)
    def test_run_configure_tempest_ko(self, *args):
        # pylint: disable=unused-argument
        self.assertEqual(self.tempestcommon.run(),
                         testcase.TestCase.EX_RUN_ERROR)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'os.path.exists', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'TempestResourcesManager.create', return_value={})
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_active_compute_cnt', return_value=2)
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'conf_utils.configure_tempest')
    def _test_run(self, status, *args):
        # pylint: disable=unused-argument
        self.assertEqual(self.tempestcommon.run(), status)

    def test_run_missing_gen_test_list(self):
        with mock.patch.object(self.tempestcommon, 'generate_test_list',
                               side_effect=Exception):
            self._test_run(testcase.TestCase.EX_RUN_ERROR)

    def test_run_apply_blacklist_ko(self):
        with mock.patch.object(self.tempestcommon, 'generate_test_list'), \
                    mock.patch.object(self.tempestcommon,
                                      'apply_tempest_blacklist',
                                      side_effect=Exception()):
            self._test_run(testcase.TestCase.EX_RUN_ERROR)

    def test_run_verifier_tests_ko(self):
        with mock.patch.object(self.tempestcommon, 'generate_test_list'), \
                mock.patch.object(self.tempestcommon,
                                  'apply_tempest_blacklist'), \
                mock.patch.object(self.tempestcommon, 'run_verifier_tests',
                                  side_effect=Exception()), \
                mock.patch.object(self.tempestcommon, 'parse_verifier_result',
                                  side_effect=Exception):
            self._test_run(testcase.TestCase.EX_RUN_ERROR)

    def test_run_verif_result_ko(self):
        with mock.patch.object(self.tempestcommon, 'generate_test_list'), \
                mock.patch.object(self.tempestcommon,
                                  'apply_tempest_blacklist'), \
                mock.patch.object(self.tempestcommon, 'run_verifier_tests'), \
                mock.patch.object(self.tempestcommon, 'parse_verifier_result',
                                  side_effect=Exception):
            self._test_run(testcase.TestCase.EX_RUN_ERROR)

    def test_run(self):
        with mock.patch.object(self.tempestcommon, 'generate_test_list'), \
                mock.patch.object(self.tempestcommon,
                                  'apply_tempest_blacklist'), \
                mock.patch.object(self.tempestcommon, 'run_verifier_tests'), \
                mock.patch.object(self.tempestcommon, 'parse_verifier_result'):
            self._test_run(testcase.TestCase.EX_OK)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
