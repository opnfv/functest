#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import os
import unittest

import mock
from xtesting.core import testcase

from functest.opnfv_tests.openstack.tempest import tempest
from functest.opnfv_tests.openstack.tempest import conf_utils


class OSTempestTesting(unittest.TestCase):
    # pylint: disable=too-many-public-methods

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
                           return_value='test_verifier_deploy_dir'), \
                mock.patch('os_client_config.get_config'), \
                mock.patch('shade.OperatorCloud'):
            self.tempestcommon = tempest.TempestCommon()
            self.tempestsmoke_serial = tempest.TempestSmokeSerial()
            self.tempestsmoke_parallel = tempest.TempestSmokeParallel()
            self.tempestfull_parallel = tempest.TempestFullParallel()
            self.tempestcustom = tempest.TempestCustom()
            self.tempestdefcore = tempest.TempestDefcore()
            self.tempestneutrontrunk = tempest.TempestNeutronTrunk()

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
            self.tempestcommon.generate_test_list()
            self.assertTrue(
                (msg % conf_utils.TEMPEST_CUSTOM) in context.exception)

    @mock.patch('os.remove')
    def test_gen_tl_cm_default(self, *args):
        self.tempestcommon.mode = 'custom'
        with mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                        'shutil.copyfile') as mock_copyfile, \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'os.path.isfile', return_value=True):
            self.tempestcommon.generate_test_list()
            self.assertTrue(mock_copyfile.called)
        args[0].assert_called_once_with('/etc/tempest.conf')

    @mock.patch('os.remove')
    @mock.patch('shutil.copyfile')
    @mock.patch('subprocess.check_output')
    def _test_gen_tl_mode_default(self, mode, *args):
        self.tempestcommon.mode = mode
        if self.tempestcommon.mode == 'smoke':
            testr_mode = r"'^tempest\.(api|scenario).*\[.*\bsmoke\b.*\]$'"
        elif self.tempestcommon.mode == 'full':
            testr_mode = r"'^tempest\.'"
        else:
            testr_mode = self.tempestcommon.mode
        verifier_repo_dir = 'test_verifier_repo_dir'
        cmd = "(cd {0}; testr list-tests {1} >{2} 2>/dev/null)".format(
            verifier_repo_dir, testr_mode, self.tempestcommon.list)
        self.tempestcommon.generate_test_list()
        args[0].assert_called_once_with(cmd, shell=True)
        args[2].assert_called_once_with('/etc/tempest.conf')

    def test_gen_tl_smoke_mode(self):
        self._test_gen_tl_mode_default('smoke')

    def test_gen_tl_full_mode(self):
        self._test_gen_tl_mode_default('full')

    def test_gen_tl_neutron_trunk_mode(self):
        self._test_gen_tl_mode_default('neutron_trunk')

    def test_verif_res_missing_verif_id(self):
        self.tempestcommon.verification_id = None
        with self.assertRaises(Exception):
            self.tempestcommon.parse_verifier_result()

    def test_backup_config_default(self):
        with mock.patch('os.path.exists', return_value=False), \
                mock.patch('os.makedirs') as mock_makedirs, \
                mock.patch('shutil.copyfile') as mock_copyfile:
            self.tempestcommon.backup_tempest_config(
                'test_conf_file', res_dir='test_dir')
            self.assertTrue(mock_makedirs.called)
            self.assertTrue(mock_copyfile.called)

        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('shutil.copyfile') as mock_copyfile:
            self.tempestcommon.backup_tempest_config(
                'test_conf_file', res_dir='test_dir')
            self.assertTrue(mock_copyfile.called)

    @mock.patch("os.rename")
    @mock.patch("os.remove")
    @mock.patch("os.path.exists", return_value=True)
    def test_apply_missing_blacklist(self, *args):
        with mock.patch('__builtin__.open', mock.mock_open()) as mock_open, \
            mock.patch.object(self.tempestcommon, 'read_file',
                              return_value=['test1', 'test2']):
            conf_utils.TEMPEST_BLACKLIST = Exception
            os.environ['INSTALLER_TYPE'] = 'installer_type'
            os.environ['DEPLOY_SCENARIO'] = 'deploy_scenario'
            self.tempestcommon.apply_tempest_blacklist()
            obj = mock_open()
            obj.write.assert_any_call('test1\n')
            obj.write.assert_any_call('test2\n')
            args[0].assert_called_once_with(self.tempestcommon.raw_list)
            args[1].assert_called_once_with(self.tempestcommon.raw_list)
            args[2].assert_called_once_with(
                self.tempestcommon.list, self.tempestcommon.raw_list)

    @mock.patch("os.rename")
    @mock.patch("os.remove")
    @mock.patch("os.path.exists", return_value=True)
    def test_apply_blacklist_default(self, *args):
        item_dict = {'scenarios': ['deploy_scenario'],
                     'installers': ['installer_type'],
                     'tests': ['test2']}
        with mock.patch('__builtin__.open', mock.mock_open()) as mock_open, \
            mock.patch.object(self.tempestcommon, 'read_file',
                              return_value=['test1', 'test2']), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'yaml.safe_load', return_value=item_dict):
            os.environ['INSTALLER_TYPE'] = 'installer_type'
            os.environ['DEPLOY_SCENARIO'] = 'deploy_scenario'
            self.tempestcommon.apply_tempest_blacklist()
            obj = mock_open()
            obj.write.assert_any_call('test1\n')
            self.assertFalse(obj.write.assert_any_call('test2\n'))
            args[0].assert_called_once_with(self.tempestcommon.raw_list)
            args[1].assert_called_once_with(self.tempestcommon.raw_list)
            args[2].assert_called_once_with(
                self.tempestcommon.list, self.tempestcommon.raw_list)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.LOGGER.info')
    def test_run_verifier_tests_default(self, mock_logger_info):
        with mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch('__builtin__.iter', return_value=[r'\} tempest\.']), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'subprocess.Popen'):
            conf_utils.TEMPEST_LIST = 'test_tempest_list'
            cmd = ["rally", "verify", "start", "--load-list",
                   conf_utils.TEMPEST_LIST]
            with self.assertRaises(Exception):
                self.tempestcommon.run_verifier_tests()
                mock_logger_info. \
                    assert_any_call("Starting Tempest test suite: '%s'.", cmd)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'subprocess.Popen')
    def test_generate_report(self, mock_popen):
        self.tempestcommon.verification_id = "1234"
        html_file = os.path.join(tempest.TempestCommon.TEMPEST_RESULTS_DIR,
                                 "tempest-report.html")
        cmd = ["rally", "verify", "report", "--type", "html", "--uuid",
               "1234", "--to", html_file]
        self.tempestcommon.generate_report()
        mock_popen.assert_called_once_with(cmd, stdout=mock.ANY,
                                           stderr=mock.ANY)

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
    def test_run_create_resources_ko(self, *args):
        # pylint: disable=unused-argument
        self.assertEqual(self.tempestcommon.run(),
                         testcase.TestCase.EX_RUN_ERROR)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'os.path.exists', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'TempestCommon.configure', side_effect=Exception)
    def test_run_configure_tempest_ko(self, *args):
        # pylint: disable=unused-argument
        self.assertEqual(self.tempestcommon.run(),
                         testcase.TestCase.EX_RUN_ERROR)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'os.path.exists', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'TempestCommon.configure')
    def _test_run(self, status, *args):
        # pylint: disable=unused-argument
        self.assertEqual(self.tempestcommon.run(), status)

    def test_run_missing_gen_test_list(self):
        with mock.patch.object(self.tempestcommon, 'generate_test_list',
                               side_effect=Exception):
            self._test_run(testcase.TestCase.EX_RUN_ERROR)

    def test_run_apply_blacklist_ko(self):
        with mock.patch.object(self.tempestcommon, 'generate_test_list'), \
                mock.patch.object(
                    self.tempestcommon, 'apply_tempest_blacklist',
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

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.TempestCommon.'
                'run', return_value=testcase.TestCase.EX_OK)
    def test_run(self, *args):
        with mock.patch.object(self.tempestcommon, 'update_rally_regex'), \
                mock.patch.object(self.tempestcommon, 'generate_test_list'), \
                mock.patch.object(self.tempestcommon,
                                  'apply_tempest_blacklist'), \
                mock.patch.object(self.tempestcommon, 'run_verifier_tests'), \
                mock.patch.object(self.tempestcommon,
                                  'parse_verifier_result'), \
                mock.patch.object(self.tempestcommon, 'generate_report'):
            self._test_run(testcase.TestCase.EX_OK)
            args[0].assert_called_once_with()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
