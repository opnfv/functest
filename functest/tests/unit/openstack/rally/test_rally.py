#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring,protected-access,invalid-name

import json
import logging
import os
import subprocess
import unittest

import mock
import munch
from xtesting.core import testcase

from functest.opnfv_tests.openstack.rally import rally
from functest.utils import config


class OSRallyTesting(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    def setUp(self):
        with mock.patch('os_client_config.get_config') as mock_get_config, \
                mock.patch('shade.OpenStackCloud') as mock_shade, \
                mock.patch('functest.core.tenantnetwork.NewProject') \
                as mock_new_project:
            self.rally_base = rally.RallyBase()
            self.rally_base.image = munch.Munch(name='foo')
            self.rally_base.flavor = munch.Munch(name='foo')
            self.rally_base.flavor_alt = munch.Munch(name='bar')
        self.assertTrue(mock_get_config.called)
        self.assertTrue(mock_shade.called)
        self.assertTrue(mock_new_project.called)

    def test_build_task_args_missing_floating_network(self):
        os.environ['OS_AUTH_URL'] = ''
        self.rally_base.ext_net = None
        task_args = self.rally_base.build_task_args('test_name')
        self.assertEqual(task_args['floating_network'], '')

    def test_build_task_args_missing_net_id(self):
        os.environ['OS_AUTH_URL'] = ''
        self.rally_base.network = None
        task_args = self.rally_base.build_task_args('test_name')
        self.assertEqual(task_args['netid'], '')

    @staticmethod
    def check_scenario_file(value):
        yaml_file = 'opnfv-test_file_name.yaml'
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
        yaml_file = 'opnfv-test_file_name.yaml'
        if yaml_file in value:
            return True
        return False

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.'
                'RallyBase.get_verifier_deployment_id', return_value='foo')
    @mock.patch('subprocess.check_output')
    def test_create_rally_deployment(self, mock_exec, mock_get_id):
        # pylint: disable=unused-argument
        self.assertEqual(rally.RallyBase.create_rally_deployment(), 'foo')
        calls = [
            mock.call(['rally', 'deployment', 'destroy', '--deployment',
                       str(getattr(config.CONF, 'rally_deployment_name'))]),
            mock.call().decode("utf-8"),
            mock.call(['rally', 'deployment', 'create', '--fromenv', '--name',
                       str(getattr(config.CONF, 'rally_deployment_name'))],
                      env=None),
            mock.call().decode("utf-8"),
            mock.call(['rally', 'deployment', 'check']),
            mock.call().decode("utf-8")]
        mock_exec.assert_has_calls(calls)

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'apply_blacklist')
    def test_prepare_test_list_missing_temp_dir(
            self, mock_method, mock_os_makedirs, mock_path_exists):
        mock_path_exists.side_effect = self.check_temp_dir

        yaml_file = 'opnfv-test_file_name.yaml'
        ret_val = os.path.join(self.rally_base.temp_dir, yaml_file)
        self.assertEqual(self.rally_base._prepare_test_list('test_file_name'),
                         ret_val)
        mock_path_exists.assert_called()
        mock_method.assert_called()
        mock_os_makedirs.assert_called()

    @mock.patch('subprocess.check_output', return_value=b'1\n')
    def test_get_task_id_default(self, *args):
        tag = 'nova'
        self.assertEqual(self.rally_base.get_task_id(tag), '1')
        args[0].assert_called_with(
            ['rally', 'task', 'list', '--tag', tag, '--uuids-only'])

    @mock.patch('subprocess.check_output', return_value=b'\n')
    def test_get_task_id_missing_id(self, *args):
        tag = 'nova'
        self.assertEqual(self.rally_base.get_task_id(tag), '')
        args[0].assert_called_with(
            ['rally', 'task', 'list', '--tag', tag, '--uuids-only'])

    def test_task_succeed_fail(self):
        json_raw = json.dumps({})
        self.assertEqual(self.rally_base.task_succeed(json_raw),
                         False)
        json_raw = json.dumps({'tasks': [{'status': 'crashed'}]})
        self.assertEqual(self.rally_base.task_succeed(json_raw),
                         False)

    def test_task_succeed_success(self):
        json_raw = json.dumps({'tasks': [{'status': 'finished',
                                          'pass_sla': True}]})
        self.assertEqual(self.rally_base.task_succeed(json_raw),
                         True)

    @mock.patch('six.moves.builtins.open', mock.mock_open())
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.yaml.safe_load',
                return_value={'scenario': [
                    {'scenarios': ['test_scenario'],
                     'tests': ['test']},
                    {'scenarios': ['other_scenario'],
                     'tests': ['other_test']}]})
    def test_excl_scenario_default(self, mock_func):
        os.environ['INSTALLER_TYPE'] = 'test_installer'
        os.environ['DEPLOY_SCENARIO'] = 'test_scenario'
        self.assertEqual(self.rally_base.excl_scenario(), ['test'])
        mock_func.assert_called()

    @mock.patch('six.moves.builtins.open', mock.mock_open())
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.yaml.safe_load',
                return_value={'scenario': [
                    {'scenarios': ['^os-[^-]+-featT-modeT$'],
                     'tests': ['test1']},
                    {'scenarios': ['^os-ctrlT-[^-]+-modeT$'],
                     'tests': ['test2']},
                    {'scenarios': ['^os-ctrlT-featT-[^-]+$'],
                     'tests': ['test3']},
                    {'scenarios': ['^os-'],
                     'tests': ['test4']},
                    {'scenarios': ['other_scenario'],
                     'tests': ['test0a']},
                    {'scenarios': [''],  # empty scenario
                     'tests': ['test0b']}]})
    def test_excl_scenario_regex(self, mock_func):
        os.environ['DEPLOY_SCENARIO'] = 'os-ctrlT-featT-modeT'
        self.assertEqual(self.rally_base.excl_scenario(),
                         ['test1', 'test2', 'test3', 'test4'])
        mock_func.assert_called()

    @mock.patch('six.moves.builtins.open', side_effect=Exception)
    def test_excl_scenario_exception(self, mock_open):
        self.assertEqual(self.rally_base.excl_scenario(), [])
        mock_open.assert_called()

    @mock.patch('six.moves.builtins.open', mock.mock_open())
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.yaml.safe_load',
                return_value={'functionality': [
                    {'functions': ['no_migration'], 'tests': ['test']}]})
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_migration_supported', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_network_trunk_supported', return_value=False)
    def test_excl_func_default(self, mock_trunk, mock_func, mock_yaml_load):
        os.environ['DEPLOY_SCENARIO'] = 'test_scenario'
        self.assertEqual(self.rally_base.excl_func(), ['test'])
        mock_func.assert_called()
        mock_trunk.assert_called()
        mock_yaml_load.assert_called()

    @mock.patch('six.moves.builtins.open', side_effect=Exception)
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
            self.rally_base.prepare_run()
        mock_path_exists.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_prepare_test_list', return_value='test_file_name')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'file_is_empty', return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.LOGGER.info')
    def test_prepare_task_no_tests_for_scenario(
            self, mock_logger_info, mock_file_empty, mock_prep_list):
        self.rally_base.prepare_task('test_name')
        mock_logger_info.assert_any_call('No tests for scenario \"%s\"',
                                         'test_name')
        mock_file_empty.assert_called()
        mock_prep_list.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_prepare_test_list', return_value='test_file_name')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'file_is_empty', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'build_task_args', return_value={})
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'get_task_id', return_value=None)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists',
                return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.subprocess.Popen')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.LOGGER.error')
    def test_run_task_taskid_missing(self, mock_logger_error, *args):
        # pylint: disable=unused-argument
        with self.assertRaises(Exception):
            self.rally_base.run_task('test_name')
        text = 'Failed to retrieve task_id'
        mock_logger_error.assert_any_call(text)

    @mock.patch('six.moves.builtins.open', mock.mock_open())
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_prepare_test_list', return_value='test_file_name')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'file_is_empty', return_value=False)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'build_task_args', return_value={})
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'get_task_id', return_value='1')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'task_succeed', return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists',
                return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.subprocess.Popen')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.LOGGER.info')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.LOGGER.error')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_save_results')
    def test_run_task_default(self, mock_save_res, *args):
        # pylint: disable=unused-argument
        self.rally_base.run_task('test_name')
        mock_save_res.assert_called()

    @mock.patch('six.moves.builtins.open', mock.mock_open())
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'task_succeed', return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists',
                return_value=True)
    @mock.patch('subprocess.check_output')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.makedirs')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.LOGGER.info')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.LOGGER.debug')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_append_summary')
    def test_save_results(self, mock_summary, *args):
        # pylint: disable=unused-argument
        self.rally_base._save_results('test_name', '1234')
        mock_summary.assert_called()

    def test_prepare_run_testname_invalid(self):
        self.rally_base.stests = ['test1', 'test2']
        with self.assertRaises(Exception):
            self.rally_base.prepare_run(tests=['test'])

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.os.path.exists')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.shutil.copyfile')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.shutil.copytree')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.shutil.rmtree')
    def test_prepare_run_flavor_alt_creation_failed(self, *args):
        # pylint: disable=unused-argument
        self.rally_base.stests = ['test1', 'test2']
        with mock.patch.object(self.rally_base, 'count_hypervisors') \
            as mock_list_hyperv, \
            mock.patch.object(self.rally_base, 'create_flavor_alt',
                              side_effect=Exception) \
                as mock_create_flavor:
            with self.assertRaises(Exception):
                self.rally_base.prepare_run(tests=['test1'])
            mock_list_hyperv.assert_called_once()
            mock_create_flavor.assert_called_once()

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'prepare_task', return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'run_task')
    def test_run_tests_all(self, mock_run_task, mock_prepare_task):
        self.rally_base.tests = ['test1', 'test2']
        self.rally_base.run_tests()
        mock_prepare_task.assert_any_call('test1')
        mock_prepare_task.assert_any_call('test2')
        mock_run_task.assert_any_call('test1')
        mock_run_task.assert_any_call('test2')

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'prepare_task', return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'run_task')
    def test_run_tests_default(self, mock_run_task, mock_prepare_task):
        self.rally_base.tests = ['test1', 'test2']
        self.rally_base.run_tests()
        mock_prepare_task.assert_any_call('test1')
        mock_prepare_task.assert_any_call('test2')
        mock_run_task.assert_any_call('test1')
        mock_run_task.assert_any_call('test2')

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'clean_rally_logs')
    def test_clean_up_default(self, *args):
        with mock.patch.object(self.rally_base.orig_cloud,
                               'delete_flavor') as mock_delete_flavor:
            self.rally_base.flavor_alt = mock.Mock()
            self.rally_base.clean()
            self.assertEqual(mock_delete_flavor.call_count, 1)
            args[0].assert_called_once_with()

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'update_rally_logs')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'create_rally_deployment')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'prepare_run')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'run_tests')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                '_generate_report')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'export_task')
    def test_run_default(self, *args):
        self.assertEqual(self.rally_base.run(), testcase.TestCase.EX_OK)
        for func in args:
            func.assert_called()

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'update_rally_logs')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'create_rally_deployment', side_effect=Exception)
    def test_run_exception_create_rally_dep(self, *args):
        self.assertEqual(self.rally_base.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].assert_called()
        args[1].assert_called_once_with(self.rally_base.res_dir)

    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'update_rally_logs')
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'create_rally_deployment', return_value=mock.Mock())
    @mock.patch('functest.opnfv_tests.openstack.rally.rally.RallyBase.'
                'prepare_run', side_effect=Exception)
    def test_run_exception_prepare_run(self, mock_prep_env, *args):
        # pylint: disable=unused-argument
        self.assertEqual(self.rally_base.run(), testcase.TestCase.EX_RUN_ERROR)
        mock_prep_env.assert_called()
        args[1].assert_called_once_with(self.rally_base.res_dir)

    def test_append_summary(self):
        json_dict = {
            'tasks': [{
                'subtasks': [{
                    'title': 'sub_task',
                    'workloads': [{
                        'full_duration': 1.23,
                        'data': [{
                            'error': []
                        }]
                    }, {
                        'full_duration': 2.78,
                        'data': [{
                            'error': ['err']
                        }]
                    }]
                }]
            }]
        }
        self.rally_base._append_summary(json.dumps(json_dict), "foo_test")
        self.assertEqual(self.rally_base.summary[0]['test_name'], "foo_test")
        self.assertEqual(self.rally_base.summary[0]['overall_duration'], 4.01)
        self.assertEqual(self.rally_base.summary[0]['nb_tests'], 2)
        self.assertEqual(self.rally_base.summary[0]['nb_success'], 1)
        self.assertEqual(self.rally_base.summary[0]['success'], [])
        self.assertEqual(self.rally_base.summary[0]['failures'], ['sub_task'])

    def test_is_successful_false(self):
        with mock.patch('six.moves.builtins.super') as mock_super:
            self.rally_base.summary = [{"task_status": True},
                                       {"task_status": False}]
            self.assertEqual(self.rally_base.is_successful(),
                             testcase.TestCase.EX_TESTCASE_FAILED)
            mock_super(rally.RallyBase, self).is_successful.assert_not_called()

    def test_is_successful_true(self):
        with mock.patch('six.moves.builtins.super') as mock_super:
            mock_super(rally.RallyBase, self).is_successful.return_value = 424
            self.rally_base.summary = [{"task_status": True},
                                       {"task_status": True}]
            self.assertEqual(self.rally_base.is_successful(), 424)
            mock_super(rally.RallyBase, self).is_successful.assert_called()

    @mock.patch('subprocess.check_output',
                side_effect=subprocess.CalledProcessError('', ''))
    def test_export_task_ko(self, *args):
        file_name = (f"{self.rally_base.results_dir}/"
                     f"{self.rally_base.case_name}.html")
        with self.assertRaises(subprocess.CalledProcessError):
            self.rally_base.export_task(file_name)
        cmd = ["rally", "task", "export", "--type", "html", "--deployment",
               str(getattr(config.CONF, 'rally_deployment_name')),
               "--to", file_name]
        args[0].assert_called_with(cmd, stderr=subprocess.STDOUT)

    @mock.patch('subprocess.check_output', return_value=b'')
    def test_export_task(self, *args):
        file_name = (f"{self.rally_base.results_dir}/"
                     f"{self.rally_base.case_name}.html")
        self.assertEqual(self.rally_base.export_task(file_name), None)
        cmd = ["rally", "task", "export", "--type", "html", "--deployment",
               str(getattr(config.CONF, 'rally_deployment_name')),
               "--to", file_name]
        args[0].assert_called_with(cmd, stderr=subprocess.STDOUT)

    @mock.patch('subprocess.check_output',
                side_effect=subprocess.CalledProcessError('', ''))
    def test_verify_report_ko(self, *args):
        file_name = (f"{self.rally_base.results_dir}/"
                     f"{self.rally_base.case_name}.html")
        with self.assertRaises(subprocess.CalledProcessError):
            self.rally_base.verify_report(file_name, "1")
        cmd = ["rally", "verify", "report", "--type", "html", "--uuid", "1",
               "--to", file_name]
        args[0].assert_called_with(cmd, stderr=subprocess.STDOUT)

    @mock.patch('subprocess.check_output', return_value=b'')
    def test_verify_report(self, *args):
        file_name = (f"{self.rally_base.results_dir}/"
                     f"{self.rally_base.case_name}.html")
        self.assertEqual(self.rally_base.verify_report(file_name, "1"), None)
        cmd = ["rally", "verify", "report", "--type", "html", "--uuid", "1",
               "--to", file_name]
        args[0].assert_called_with(cmd, stderr=subprocess.STDOUT)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
