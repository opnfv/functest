#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import json
import logging
import os
import unittest

import mock

from functest.core import testcase
from functest.opnfv_tests.openstack.rally import rally
from functest.utils.constants import CONST

from snaps.openstack.os_credentials import OSCreds


class OSRallyTesting(unittest.TestCase):
    def setUp(self):
        os_creds = OSCreds(
            username='user', password='pass',
            auth_url='http://foo.com:5000/v3', project_name='bar')
        with mock.patch('snaps.openstack.tests.openstack_tests.'
                        'get_credentials', return_value=os_creds) as m:
            self.rally_base = rally.RallyBase()
            self.polling_iter = 2
        self.assertTrue(m.called)

    def test_build_task_args_missing_floating_network(self):
        CONST.__setattr__('OS_AUTH_URL', None)
        self.rally_base.ext_net_name = ''
        task_args = self.rally_base._build_task_args('test_file_name')
        self.assertEqual(task_args['floating_network'], '')

    def test_build_task_args_missing_net_id(self):
        CONST.__setattr__('OS_AUTH_URL', None)
        self.rally_base.priv_net_id = ''
        task_args = self.rally_base._build_task_args('test_file_name')
        self.assertEqual(task_args['netid'], '')

    @staticmethod
    def check_scenario_file(value):
        yaml_file = 'opnfv-{}.yaml'.format('test_file_name')
        if yaml_file in value:
            return False
        return True

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists')
    def test_prepare_test_list_missing_scenario_file(self, mock_func):
        mock_func.side_effect = self.check_scenario_file
        with self.assertRaises(Exception):
            self.rally_base._prepare_test_list('test_file_name')
        mock_func.assert_called()

    @staticmethod
    def check_temp_dir(value):
        yaml_file = 'opnfv-{}.yaml'.format('test_file_name')
        if yaml_file in value:
            return True
        return False

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_apply_blacklist')
    def test_prepare_test_list_missing_temp_dir(
            self, mock_method, mock_os_makedirs, mock_path_exists):
        mock_path_exists.side_effect = self.check_temp_dir

        yaml_file = 'opnfv-{}.yaml'.format('test_file_name')
        ret_val = os.path.join(self.rally_base.TEMP_DIR, yaml_file)
        self.assertEqual(self.rally_base._prepare_test_list('test_file_name'),
                         ret_val)
        mock_path_exists.assert_called()
        mock_method.assert_called()
        mock_os_makedirs.assert_called()

    def test_get_task_id_default(self):
        cmd_raw = 'Task 1: started'
        self.assertEqual(self.rally_base.get_task_id(cmd_raw),
                         '1')

    def test_get_task_id_missing_id(self):
        cmd_raw = ''
        self.assertEqual(self.rally_base.get_task_id(cmd_raw),
                         None)

    def test_task_succeed_fail(self):
        json_raw = json.dumps([None])
        self.assertEqual(self.rally_base.task_succeed(json_raw),
                         False)
        json_raw = json.dumps([{'result': [{'error': ['test_error']}]}])
        self.assertEqual(self.rally_base.task_succeed(json_raw),
                         False)

    def test_task_succeed_success(self):
        json_raw = json.dumps('')
        self.assertEqual(self.rally_base.task_succeed(json_raw),
                         True)

    def polling(self):
        if self.polling_iter == 0:
            return "something"
        self.polling_iter -= 1
        return None

    def test_get_cmd_output(self):
        proc = mock.Mock()
        attrs = {'poll.side_effect': self.polling,
                 'stdout.readline.return_value': 'line'}
        proc.configure_mock(**attrs)
        self.assertEqual(self.rally_base.get_cmd_output(proc),
                         'lineline')

    @mock.patch('__builtin__.open', mock.mock_open())
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.yaml.safe_load',
                return_value={'scenario': [
                    {'scenarios': ['test_scenario'],
                     'installers': ['test_installer'],
                     'tests': ['test']},
                    {'scenarios': ['other_scenario'],
                     'installers': ['test_installer'],
                     'tests': ['other_test']}]})
    def test_excl_scenario_default(self, mock_func):
        CONST.__setattr__('INSTALLER_TYPE', 'test_installer')
        CONST.__setattr__('DEPLOY_SCENARIO', 'test_scenario')
        self.assertEqual(self.rally_base.excl_scenario(), ['test'])
        mock_func.assert_called()

    @mock.patch('__builtin__.open', mock.mock_open())
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.yaml.safe_load',
                return_value={'scenario': [
                    {'scenarios': ['^os-[^-]+-featT-modeT$'],
                     'installers': ['test_installer'],
                     'tests': ['test1']},
                    {'scenarios': ['^os-ctrlT-[^-]+-modeT$'],
                     'installers': ['test_installer'],
                     'tests': ['test2']},
                    {'scenarios': ['^os-ctrlT-featT-[^-]+$'],
                     'installers': ['test_installer'],
                     'tests': ['test3']},
                    {'scenarios': ['^os-'],
                     'installers': ['test_installer'],
                     'tests': ['test4']},
                    {'scenarios': ['other_scenario'],
                     'installers': ['test_installer'],
                     'tests': ['test0a']},
                    {'scenarios': [''],  # empty scenario
                     'installers': ['test_installer'],
                     'tests': ['test0b']}]})
    def test_excl_scenario_regex(self, mock_func):
        CONST.__setattr__('INSTALLER_TYPE', 'test_installer')
        CONST.__setattr__('DEPLOY_SCENARIO', 'os-ctrlT-featT-modeT')
        self.assertEqual(self.rally_base.excl_scenario(),
                         ['test1', 'test2', 'test3', 'test4'])
        mock_func.assert_called()

    @mock.patch('__builtin__.open', side_effect=Exception)
    def test_excl_scenario_exception(self, mock_open):
        self.assertEqual(self.rally_base.excl_scenario(), [])
        mock_open.assert_called()

    @mock.patch('__builtin__.open', mock.mock_open())
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.yaml.safe_load',
                return_value={'functionality': [
                    {'functions': ['no_live_migration'], 'tests': ['test']}]})
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_live_migration_supported', return_value=False)
    def test_excl_func_default(self, mock_func, mock_yaml_load):
        CONST.__setattr__('INSTALLER_TYPE', 'test_installer')
        CONST.__setattr__('DEPLOY_SCENARIO', 'test_scenario')
        self.assertEqual(self.rally_base.excl_func(), ['test'])
        mock_func.assert_called()
        mock_yaml_load.assert_called()

    @mock.patch('__builtin__.open', side_effect=Exception)
    def test_excl_func_exception(self, mock_open):
        self.assertEqual(self.rally_base.excl_func(), [])
        mock_open.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.stat')
    def test_file_is_empty_default(self, mock_os_stat):
        attrs = {'st_size': 10}
        mock_os_stat.return_value.configure_mock(**attrs)
        self.assertEqual(self.rally_base.file_is_empty('test_file_name'),
                         False)
        mock_os_stat.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.stat',
                side_effect=Exception)
    def test_file_is_empty_exception(self, mock_os_stat):
        self.assertEqual(self.rally_base.file_is_empty('test_file_name'), True)
        mock_os_stat.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists',
                return_value=False)
    def test_run_task_missing_task_file(self, mock_path_exists):
        with self.assertRaises(Exception):
            self.rally_base._run_task('test_name')
        mock_path_exists.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists',
                return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_prepare_test_list', return_value='test_file_name')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'file_is_empty', return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.LOGGER.info')
    def test_run_task_no_tests_for_scenario(self, mock_logger_info,
                                            mock_file_empty, mock_prep_list,
                                            mock_path_exists):
        self.rally_base._run_task('test_name')
        mock_logger_info.assert_any_call('No tests for scenario \"%s\"',
                                         'test_name')
        mock_file_empty.assert_called()
        mock_prep_list.assert_called()
        mock_path_exists.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_prepare_test_list', return_value='test_file_name')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'file_is_empty', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_build_task_args', return_value={})
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_get_output')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'get_task_id', return_value=None)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'get_cmd_output', return_value='')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists',
                return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.subprocess.Popen')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.LOGGER.error')
    def test_run_task_taskid_missing(self, mock_logger_error, *args):
        self.rally_base._run_task('test_name')
        text = 'Failed to retrieve task_id, validating task...'
        mock_logger_error.assert_any_call(text)

    @mock.patch('__builtin__.open', mock.mock_open())
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_prepare_test_list', return_value='test_file_name')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'file_is_empty', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_build_task_args', return_value={})
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_get_output')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'get_task_id', return_value='1')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'get_cmd_output', return_value='')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'task_succeed', return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists',
                return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.subprocess.Popen')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.popen')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.LOGGER.info')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.LOGGER.error')
    def test_run_task_default(self, mock_logger_error, mock_logger_info,
                              mock_popen, *args):
        attrs = {'read.return_value': 'json_result'}
        mock_popen.return_value.configure_mock(**attrs)
        self.rally_base._run_task('test_name')
        text = 'Test scenario: "test_name" OK.\n'
        mock_logger_info.assert_any_call(text)
        mock_logger_error.assert_not_called()

    def test_prepare_env_testname_invalid(self):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test'
        with self.assertRaises(Exception):
            self.rally_base._prepare_env()

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_active_compute_cnt')
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name', return_value='test_net_name')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_image',
                return_value=None)
    def test_prepare_env_image_missing(
            self, mock_get_img, mock_get_net, mock_get_comp_cnt):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test1'
        with self.assertRaises(Exception):
            self.rally_base._prepare_env()
        mock_get_img.assert_called()
        mock_get_net.assert_called()
        mock_get_comp_cnt.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_active_compute_cnt')
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name', return_value='test_net_name')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_image')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_network',
                return_value=None)
    def test_prepare_env_network_creation_failed(
            self, mock_create_net, mock_get_img, mock_get_net,
            mock_get_comp_cnt):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test1'
        with self.assertRaises(Exception):
            self.rally_base._prepare_env()
        mock_create_net.assert_called()
        mock_get_img.assert_called()
        mock_get_net.assert_called()
        mock_get_comp_cnt.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_active_compute_cnt')
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name', return_value='test_net_name')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_image')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_network')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_router',
                return_value=None)
    def test_prepare_env_router_creation_failed(
            self, mock_create_router, mock_create_net, mock_get_img,
            mock_get_net, mock_get_comp_cnt):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test1'
        with self.assertRaises(Exception):
            self.rally_base._prepare_env()
        mock_create_net.assert_called()
        mock_get_img.assert_called()
        mock_get_net.assert_called()
        mock_create_router.assert_called()
        mock_get_comp_cnt.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_active_compute_cnt')
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name', return_value='test_net_name')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_image')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_network')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_router')
    @mock.patch('snaps.openstack.create_flavor.OpenStackFlavor.create',
                return_value=None)
    def test_prepare_env_flavor_creation_failed(
            self, mock_create_flavor, mock_create_router, mock_create_net,
            mock_get_img, mock_get_net, mock_get_comp_cnt):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test1'
        with self.assertRaises(Exception):
            self.rally_base._prepare_env()
        mock_create_net.assert_called()
        mock_get_img.assert_called()
        mock_get_net.assert_called()
        mock_create_router.assert_called()
        mock_get_comp_cnt.assert_called()
        mock_create_flavor.assert_called_once()

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_active_compute_cnt')
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name', return_value='test_net_name')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_image')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_network')
    @mock.patch('snaps.openstack.utils.deploy_utils.create_router')
    @mock.patch('snaps.openstack.create_flavor.OpenStackFlavor.create',
                side_effect=[mock.Mock, None])
    def test_prepare_env_flavor_alt_creation_failed(
            self, mock_create_flavor, mock_create_router, mock_create_net,
            mock_get_img, mock_get_net, mock_get_comp_cnt):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test1'
        with self.assertRaises(Exception):
            self.rally_base._prepare_env()
        mock_create_net.assert_called()
        mock_get_img.assert_called()
        mock_get_net.assert_called()
        mock_create_router.assert_called()
        mock_get_comp_cnt.assert_called()
        self.assertEqual(mock_create_flavor.call_count, 2)

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_run_task')
    def test_run_tests_all(self, mock_run_task):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'all'
        self.rally_base._run_tests()
        mock_run_task.assert_any_call('test1')
        mock_run_task.assert_any_call('test2')

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_run_task')
    def test_run_tests_default(self, mock_run_task):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test1'
        self.rally_base._run_tests()
        mock_run_task.assert_any_call('test1')

    def test_clean_up_default(self):
        creator1 = mock.Mock()
        creator2 = mock.Mock()
        self.rally_base.creators = [creator1, creator2]
        self.rally_base._clean_up()
        self.assertTrue(creator1.clean.called)
        self.assertTrue(creator2.clean.called)

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_prepare_env')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_run_tests')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_generate_report')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_clean_up')
    def test_run_default(self, *args):
        self.assertEqual(self.rally_base.run(), testcase.TestCase.EX_OK)
        map(lambda m: m.assert_called(), args)

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_prepare_env', side_effect=Exception)
    def test_run_exception(self, mock_prep_env):
        self.assertEqual(self.rally_base.run(), testcase.TestCase.EX_RUN_ERROR)
        mock_prep_env.assert_called()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
