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

from functest.opnfv_tests.openstack.rally import rally
from functest.opnfv_tests.openstack.tempest import tempest
from functest.utils import config


class OSTempestTesting(unittest.TestCase):
    # pylint: disable=too-many-public-methods

    def setUp(self):
        with mock.patch('os_client_config.get_config'), \
                mock.patch('shade.OpenStackCloud'), \
                mock.patch('functest.core.tenantnetwork.NewProject'), \
                mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                           'RallyBase.create_rally_deployment'), \
                mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                           'TempestCommon.create_verifier'), \
                mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                           'TempestCommon.get_verifier_id',
                           return_value='test_deploy_id'), \
                mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                           'RallyBase.get_verifier_deployment_id',
                           return_value='test_deploy_id'), \
                mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                           'TempestCommon.get_verifier_repo_dir',
                           return_value='test_verifier_repo_dir'), \
                mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                           'TempestCommon.get_verifier_deployment_dir',
                           return_value='test_verifier_deploy_dir'), \
                mock.patch('os_client_config.make_shade'):
            self.tempestcommon = tempest.TempestCommon()

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
                (msg % self.tempestcommon.tempest_custom) in context.exception)

    @mock.patch('subprocess.check_output')
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
        if mode == 'smoke':
            testr_mode = r'^tempest\.(api|scenario).*\[.*\bsmoke\b.*\]$'
        elif mode == 'full':
            testr_mode = r'^tempest\.'
        else:
            testr_mode = self.tempestcommon.mode
        verifier_repo_dir = 'test_verifier_repo_dir'
        self.tempestcommon.verifier_repo_dir = verifier_repo_dir
        cmd = "(cd {0}; stestr list '{1}' >{2} 2>/dev/null)".format(
            verifier_repo_dir, testr_mode, self.tempestcommon.list)
        self.tempestcommon.generate_test_list(mode=testr_mode)
        args[0].assert_called_once_with(cmd, shell=True)
        args[2].assert_called_once_with('/etc/tempest.conf')

    def test_gen_tl_smoke_mode(self):
        self._test_gen_tl_mode_default('smoke')

    def test_gen_tl_full_mode(self):
        self._test_gen_tl_mode_default('full')

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
        with mock.patch('six.moves.builtins.open',
                        mock.mock_open()) as mock_open, \
            mock.patch.object(self.tempestcommon, 'read_file',
                              return_value=['test1', 'test2']):
            self.tempestcommon.tempest_blacklist = Exception
            os.environ['DEPLOY_SCENARIO'] = 'deploy_scenario'
            self.tempestcommon.apply_tempest_blacklist(
                self.tempestcommon.tempest_blacklist)
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
                     'tests': ['test2']}
        with mock.patch('six.moves.builtins.open',
                        mock.mock_open()) as mock_open, \
            mock.patch.object(self.tempestcommon, 'read_file',
                              return_value=['test1', 'test2']), \
            mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                       'yaml.safe_load', return_value=item_dict):
            os.environ['DEPLOY_SCENARIO'] = 'deploy_scenario'
            self.tempestcommon.apply_tempest_blacklist(
                self.tempestcommon.tempest_blacklist)
            obj = mock_open()
            obj.write.assert_any_call('test1\n')
            self.assertFalse(obj.write.assert_any_call('test2\n'))
            args[0].assert_called_once_with(self.tempestcommon.raw_list)
            args[1].assert_called_once_with(self.tempestcommon.raw_list)
            args[2].assert_called_once_with(
                self.tempestcommon.list, self.tempestcommon.raw_list)

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.'
                'subprocess.Popen')
    @mock.patch('six.moves.builtins.open', mock.mock_open())
    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.LOGGER.info')
    def test_run_verifier_tests_default(self, *args):
        self.tempestcommon.tempest_list = 'test_tempest_list'
        cmd = ["rally", "verify", "start", "--load-list",
               self.tempestcommon.tempest_list]
        with self.assertRaises(Exception):
            self.tempestcommon.run_verifier_tests()
            args[0].assert_any_call("Starting Tempest test suite: '%s'.", cmd)

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

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.TempestCommon.'
                'run', return_value=testcase.TestCase.EX_OK)
    def test_run(self, *args):
        with mock.patch.object(self.tempestcommon, 'update_rally_regex'), \
                mock.patch.object(self.tempestcommon, 'generate_test_list'), \
                mock.patch.object(self.tempestcommon,
                                  'apply_tempest_blacklist'), \
                mock.patch.object(self.tempestcommon, 'run_verifier_tests'), \
                mock.patch.object(self.tempestcommon,
                                  'parse_verifier_result'):
            self._test_run(testcase.TestCase.EX_OK)
            args[0].assert_called_once_with()

    @mock.patch('functest.opnfv_tests.openstack.tempest.tempest.LOGGER.debug')
    def test_create_verifier(self, mock_logger_debug):
        mock_popen = mock.Mock()
        attrs = {'poll.return_value': None,
                 'stdout.readline.return_value': '0'}
        mock_popen.configure_mock(**attrs)

        setattr(config.CONF, 'tempest_verifier_name', 'test_verifier_name')
        with mock.patch('subprocess.Popen', side_effect=Exception), \
                self.assertRaises(Exception):
            self.tempestcommon.create_verifier()
            mock_logger_debug.assert_any_call("Tempest test_verifier_name"
                                              " does not exist")

    def test_get_verifier_id_default(self):
        setattr(config.CONF, 'tempest_verifier_name', 'test_verifier_name')

        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'tempest.subprocess.Popen') as mock_popen:
            mock_stdout = mock.Mock()
            attrs = {'stdout.readline.return_value': b'test_deploy_id'}
            mock_stdout.configure_mock(**attrs)
            mock_popen.return_value = mock_stdout

            self.assertEqual(self.tempestcommon.get_verifier_id(),
                             'test_deploy_id')

    def test_get_depl_id_default(self):
        setattr(config.CONF, 'tempest_verifier_name', 'test_deploy_name')
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'tempest.subprocess.Popen') as mock_popen:
            mock_stdout = mock.Mock()
            attrs = {'stdout.readline.return_value': b'test_deploy_id'}
            mock_stdout.configure_mock(**attrs)
            mock_popen.return_value = mock_stdout

            self.assertEqual(rally.RallyBase.get_verifier_deployment_id(),
                             'test_deploy_id')

    def test_get_verif_repo_dir_default(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'tempest.os.path.join',
                        return_value='test_verifier_repo_dir'):
            self.assertEqual(self.tempestcommon.get_verifier_repo_dir(''),
                             'test_verifier_repo_dir')

    def test_get_depl_dir_default(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'tempest.os.path.join',
                        return_value='test_verifier_repo_dir'):
            self.assertEqual(
                self.tempestcommon.get_verifier_deployment_dir('', ''),
                'test_verifier_repo_dir')

    def _test_missing_param(self, params, image_id, flavor_id, alt=False):
        with mock.patch('six.moves.configparser.RawConfigParser.'
                        'set') as mset, \
            mock.patch('six.moves.configparser.RawConfigParser.'
                       'read') as mread, \
            mock.patch('six.moves.configparser.RawConfigParser.'
                       'write') as mwrite, \
            mock.patch('six.moves.builtins.open', mock.mock_open()), \
            mock.patch('functest.utils.functest_utils.yaml.safe_load',
                       return_value={'validation': {'ssh_timeout': 300}}):
            os.environ['OS_INTERFACE'] = ''
            if not alt:
                self.tempestcommon.configure_tempest_update_params(
                    'test_conf_file', image_id=image_id,
                    flavor_id=flavor_id)
                mset.assert_any_call(params[0], params[1], params[2])
            else:
                self.tempestcommon.configure_tempest_update_params(
                    'test_conf_file', image_alt_id=image_id,
                    flavor_alt_id=flavor_id)
                mset.assert_any_call(params[0], params[1], params[2])
            self.assertTrue(mread.called)
            self.assertTrue(mwrite.called)

    def test_upd_missing_image_id(self):
        self._test_missing_param(('compute', 'image_ref', 'test_image_id'),
                                 'test_image_id', None)

    def test_upd_missing_image_id_alt(self):
        self._test_missing_param(
            ('compute', 'image_ref_alt', 'test_image_id_alt'),
            'test_image_id_alt', None, alt=True)

    def test_upd_missing_flavor_id(self):
        self._test_missing_param(('compute', 'flavor_ref', 'test_flavor_id'),
                                 None, 'test_flavor_id')

    def test_upd_missing_flavor_id_alt(self):
        self._test_missing_param(
            ('compute', 'flavor_ref_alt', 'test_flavor_id_alt'),
            None, 'test_flavor_id_alt', alt=True)

    def test_verif_missing_conf_file(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'tempest.os.path.isfile',
                        return_value=False), \
                mock.patch('subprocess.check_output') as mexe, \
                self.assertRaises(Exception) as context:
            self.tempestcommon.configure_verifier('test_dep_dir')
            mexe.assert_called_once_with("rally verify configure-verifier")
            msg = ("Tempest configuration file 'test_dep_dir/tempest.conf'"
                   " NOT found.")
            self.assertTrue(msg in context.exception)

    def test_configure_verifier_default(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'tempest.os.path.isfile',
                        return_value=True), \
                mock.patch('subprocess.check_output') as mexe:
            self.assertEqual(
                self.tempestcommon.configure_verifier('test_dep_dir'),
                'test_dep_dir/tempest.conf')
            mexe.assert_called_once_with(
                ['rally', 'verify', 'configure-verifier', '--reconfigure',
                 '--id', str(getattr(config.CONF, 'tempest_verifier_name'))])

    def test_is_successful_false(self):
        with mock.patch('six.moves.builtins.super') as mock_super:
            self.tempestcommon.deny_skipping = True
            self.tempestcommon.details = {"skipped_number": 2}
            self.assertEqual(self.tempestcommon.is_successful(),
                             testcase.TestCase.EX_TESTCASE_FAILED)
            mock_super(tempest.TempestCommon,
                       self).is_successful.assert_not_called()

    def test_is_successful_true(self):
        with mock.patch('six.moves.builtins.super') as mock_super:
            self.tempestcommon.deny_skipping = False
            self.tempestcommon.details = {"skipped_number": 2}
            mock_super(tempest.TempestCommon,
                       self).is_successful.return_value = 567
            self.assertEqual(self.tempestcommon.is_successful(), 567)
            mock_super(tempest.TempestCommon,
                       self).is_successful.assert_called()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
