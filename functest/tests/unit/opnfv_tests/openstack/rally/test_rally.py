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

from functest.core import testcase_base
from functest.opnfv_tests.openstack.rally import rally
from functest.utils.constants import CONST


class OSRallyTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.nova_client = mock.Mock()
        self.neutron_client = mock.Mock()
        self.cinder_client = mock.Mock()
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os_utils.get_nova_client',
                        return_value=self.nova_client), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os_utils.get_neutron_client',
                       return_value=self.neutron_client), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os_utils.get_cinder_client',
                       return_value=self.cinder_client):
            self.rally_base = rally.RallyBase()
            self.rally_base.network_dict['net_id'] = 'test_net_id'
            self.polling_iter = 2

    def test_build_task_args_missing_floating_network(self):
        CONST.OS_AUTH_URL = None
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os_utils.get_external_net',
                        return_value=None):
            task_args = self.rally_base._build_task_args('test_file_name')
            self.assertEqual(task_args['floating_network'], '')

    def test_build_task_args_missing_net_id(self):
        CONST.OS_AUTH_URL = None
        self.rally_base.network_dict['net_id'] = ''
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os_utils.get_external_net',
                        return_value='test_floating_network'):
            task_args = self.rally_base._build_task_args('test_file_name')
            self.assertEqual(task_args['netid'], '')

    def test_build_task_args_missing_auth_url(self):
        CONST.OS_AUTH_URL = None
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os_utils.get_external_net',
                        return_value='test_floating_network'):
            task_args = self.rally_base._build_task_args('test_file_name')
            self.assertEqual(task_args['request_url'], '')

    def check_scenario_file(self, value):
        yaml_file = 'opnfv-{}.yaml'.format('test_file_name')
        if yaml_file in value:
            return False
        return True

    def test_prepare_test_list_missing_scenario_file(self):
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os.path.exists',
                        side_effect=self.check_scenario_file), \
                self.assertRaises(Exception):
            self.rally_base._prepare_test_list('test_file_name')

    def check_temp_dir(self, value):
        yaml_file = 'opnfv-{}.yaml'.format('test_file_name')
        if yaml_file in value:
            return True
        return False

    def test_prepare_test_list_missing_temp_dir(self):
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os.path.exists',
                        side_effect=self.check_temp_dir), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os.makedirs') as mock_os_makedir, \
            mock.patch.object(self.rally_base, 'apply_blacklist',
                              return_value=mock.Mock()) as mock_method:
            yaml_file = 'opnfv-{}.yaml'.format('test_file_name')
            ret_val = os.path.join(self.rally_base.TEMP_DIR, yaml_file)
            self.assertEqual(self.rally_base.
                             _prepare_test_list('test_file_name'),
                             ret_val)
            self.assertTrue(mock_method.called)
            self.assertTrue(mock_os_makedir.called)

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

    def test_excl_scenario_default(self):
        CONST.INSTALLER_TYPE = 'test_installer'
        CONST.DEPLOY_SCENARIO = 'test_scenario'
        dic = {'scenario': [{'scenarios': ['test_scenario'],
                             'installers': ['test_installer'],
                             'tests': ['test']}]}
        with mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'yaml.safe_load',
                       return_value=dic):
                self.assertEqual(self.rally_base.excl_scenario(),
                                 ['test'])

    def test_excl_scenario_exception(self):
        with mock.patch('__builtin__.open', side_effect=Exception):
                self.assertEqual(self.rally_base.excl_scenario(),
                                 [])

    def test_excl_func_default(self):
        CONST.INSTALLER_TYPE = 'test_installer'
        CONST.DEPLOY_SCENARIO = 'test_scenario'
        dic = {'functionality': [{'functions': ['no_live_migration'],
                                  'tests': ['test']}]}
        with mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'yaml.safe_load',
                       return_value=dic), \
            mock.patch.object(self.rally_base, 'live_migration_supported',
                              return_value=False):
                self.assertEqual(self.rally_base.excl_func(),
                                 ['test'])

    def test_excl_func_exception(self):
        with mock.patch('__builtin__.open', side_effect=Exception):
                self.assertEqual(self.rally_base.excl_func(),
                                 [])

    def test_file_is_empty_default(self):
        mock_obj = mock.Mock()
        attrs = {'st_size': 10}
        mock_obj.configure_mock(**attrs)
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os.stat',
                        return_value=mock_obj):
            self.assertEqual(self.rally_base.file_is_empty('test_file_name'),
                             False)

    def test_file_is_empty_exception(self):
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os.stat',
                        side_effect=Exception):
            self.assertEqual(self.rally_base.file_is_empty('test_file_name'),
                             True)

    def test_run_task_missing_task_file(self):
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os.path.exists',
                        return_value=False), \
                self.assertRaises(Exception):
            self.rally_base._run_task('test_name')

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.logger.info')
    def test_run_task_no_tests_for_scenario(self, mock_logger_info):
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os.path.exists',
                        return_value=True), \
            mock.patch.object(self.rally_base, '_prepare_test_list',
                              return_value='test_file_name'), \
            mock.patch.object(self.rally_base, 'file_is_empty',
                              return_value=True):
            self.rally_base._run_task('test_name')
            str = 'No tests for scenario "test_name"'
            mock_logger_info.assert_any_call(str)

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.logger.error')
    def test_run_task_taskid_missing(self, mock_logger_error):
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os.path.exists',
                        return_value=True), \
            mock.patch.object(self.rally_base, '_prepare_test_list',
                              return_value='test_file_name'), \
            mock.patch.object(self.rally_base, 'file_is_empty',
                              return_value=False), \
            mock.patch.object(self.rally_base, '_build_task_args',
                              return_value={}), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'subprocess.Popen'), \
            mock.patch.object(self.rally_base, '_get_output',
                              return_value=mock.Mock()), \
            mock.patch.object(self.rally_base, 'get_task_id',
                              return_value=None), \
            mock.patch.object(self.rally_base, 'get_cmd_output',
                              return_value=''):
            self.rally_base._run_task('test_name')
            str = 'Failed to retrieve task_id, validating task...'
            mock_logger_error.assert_any_call(str)

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.logger.info')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.logger.error')
    def test_run_task_default(self, mock_logger_error,
                              mock_logger_info):
        popen = mock.Mock()
        attrs = {'read.return_value': 'json_result'}
        popen.configure_mock(**attrs)

        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os.path.exists',
                        return_value=True), \
            mock.patch.object(self.rally_base, '_prepare_test_list',
                              return_value='test_file_name'), \
            mock.patch.object(self.rally_base, 'file_is_empty',
                              return_value=False), \
            mock.patch.object(self.rally_base, '_build_task_args',
                              return_value={}), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'subprocess.Popen'), \
            mock.patch.object(self.rally_base, '_get_output',
                              return_value=mock.Mock()), \
            mock.patch.object(self.rally_base, 'get_task_id',
                              return_value='1'), \
            mock.patch.object(self.rally_base, 'get_cmd_output',
                              return_value=''), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os.makedirs'), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os.popen',
                       return_value=popen), \
            mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch.object(self.rally_base, 'task_succeed',
                              return_value=True):
            self.rally_base._run_task('test_name')
            str = 'Test scenario: "test_name" OK.\n'
            mock_logger_info.assert_any_call(str)

    def test_prepare_env_testname_invalid(self):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test'
        with self.assertRaises(Exception):
            self.rally_base._prepare_env()

    def test_prepare_env_volume_creation_failed(self):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test1'
        volume_type = None
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os_utils.list_volume_types',
                        return_value=None), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os_utils.create_volume_type',
                       return_value=volume_type), \
                self.assertRaises(Exception):
            self.rally_base._prepare_env()

    def test_prepare_env_image_missing(self):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test1'
        volume_type = mock.Mock()
        image_id = None
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os_utils.list_volume_types',
                        return_value=None), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os_utils.create_volume_type',
                       return_value=volume_type), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os_utils.get_or_create_image',
                       return_value=(True, image_id)), \
                self.assertRaises(Exception):
            self.rally_base._prepare_env()

    def test_prepare_env_image_shared_network_creation_failed(self):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test1'
        volume_type = mock.Mock()
        image_id = 'image_id'
        network_dict = None
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os_utils.list_volume_types',
                        return_value=None), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os_utils.create_volume_type',
                       return_value=volume_type), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os_utils.get_or_create_image',
                       return_value=(True, image_id)), \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os_utils.create_shared_network_full',
                       return_value=network_dict), \
                self.assertRaises(Exception):
            self.rally_base._prepare_env()

    def test_run_tests_all(self):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'all'
        with mock.patch.object(self.rally_base, '_run_task',
                               return_value=mock.Mock()):
            self.rally_base._run_tests()
            self.rally_base._run_task.assert_any_call('test1')
            self.rally_base._run_task.assert_any_call('test2')

    def test_run_tests_default(self):
        self.rally_base.TESTS = ['test1', 'test2']
        self.rally_base.test_name = 'test1'
        with mock.patch.object(self.rally_base, '_run_task',
                               return_value=mock.Mock()):
            self.rally_base._run_tests()
            self.rally_base._run_task.assert_any_call('test1')

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.logger.info')
    def test_generate_report(self, mock_logger_info):
        summary = [{'test_name': 'test_name',
                    'overall_duration': 5,
                    'nb_tests': 3,
                    'success': 5}]
        self.rally_base.summary = summary
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'ft_utils.check_success_rate',
                        return_value='criteria'):
            self.rally_base._generate_report()
            self.assertTrue(mock_logger_info.called)

    def test_clean_up_default(self):
        self.rally_base.volume_type = mock.Mock()
        self.rally_base.cinder_client = mock.Mock()
        self.rally_base.image_exists = False
        self.rally_base.image_id = 1
        self.rally_base.nova_client = mock.Mock()
        with mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                        'os_utils.delete_volume_type') as mock_vol_method, \
            mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                       'os_utils.delete_glance_image') as mock_glance_method:
            self.rally_base._clean_up()
            mock_vol_method.assert_any_call(self.rally_base.cinder_client,
                                            self.rally_base.volume_type)
            mock_glance_method.assert_any_call(self.rally_base.nova_client,
                                               1)

    def test_run_default(self):
        with mock.patch.object(self.rally_base, '_prepare_env'), \
            mock.patch.object(self.rally_base, '_run_tests'), \
            mock.patch.object(self.rally_base, '_generate_report'), \
                mock.patch.object(self.rally_base, '_clean_up'):
            self.assertEqual(self.rally_base.run(),
                             testcase_base.TestCase.EX_OK)

    def test_run_exception(self):
        with mock.patch.object(self.rally_base, '_prepare_env',
                               side_effect=Exception):
            self.assertEqual(self.rally_base.run(),
                             testcase_base.TestCase.EX_RUN_ERROR)


if __name__ == "__main__":
    unittest.main(verbosity=2)
