#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import time
import unittest

import mock
import pkg_resources

from functest.utils import functest_utils


class FunctestUtilsTesting(unittest.TestCase):
    # pylint: disable=too-many-instance-attributes,too-many-public-methods

    readline = 0
    test_ip = ['10.1.23.4', '10.1.14.15', '10.1.16.15']

    def setUp(self):
        self.url = 'http://www.opnfv.org/'
        self.timeout = 5
        self.dest_path = 'test_path'
        self.repo_path = 'test_repo_path'
        self.installer = 'test_installer'
        self.scenario = 'test_scenario'
        self.build_tag = 'jenkins-functest-fuel-opnfv-jump-2-daily-master-190'
        self.build_tag_week = 'jenkins-functest-fuel-baremetal-weekly-master-8'
        self.version = 'master'
        self.node_name = 'test_node_name'
        self.project = 'test_project'
        self.case_name = 'test_case_name'
        self.status = 'test_status'
        self.details = 'test_details'
        self.db_url = 'test_db_url'
        self.criteria = 50
        self.result = 75
        self.start_date = 1482624000
        self.stop_date = 1482624000
        self.start_time = time.time()
        self.stop_time = time.time()
        self.readline = -1
        self.test_ip = ['10.1.23.4', '10.1.14.15', '10.1.16.15']
        self.test_file = 'test_file'
        self.error_msg = 'test_error_msg'
        self.cmd = 'test_cmd'
        self.output_file = 'test_output_file'
        self.testname = 'testname'
        self.parameter = 'general.openstack.image_name'
        self.config_yaml = pkg_resources.resource_filename(
            'functest', 'ci/config_functest.yaml')
        self.db_url_env = 'http://foo/testdb'
        self.testcases_yaml = "test_testcases_yaml"
        self.file_yaml = {'general': {'openstack': {'image_name':
                                                    'test_image_name'}}}

    def _get_env_dict(self, var):
        dic = {'INSTALLER_TYPE': self.installer,
               'DEPLOY_SCENARIO': self.scenario,
               'NODE_NAME': self.node_name,
               'BUILD_TAG': self.build_tag}
        dic.pop(var, None)
        return dic

    @staticmethod
    def readline_side():
        if FunctestUtilsTesting.readline == \
                len(FunctestUtilsTesting.test_ip) - 1:
            return False
        FunctestUtilsTesting.readline += 1
        return FunctestUtilsTesting.test_ip[FunctestUtilsTesting.readline]

    def _get_environ(self, var, *args):  # pylint: disable=unused-argument
        if var == 'INSTALLER_TYPE':
            return self.installer
        elif var == 'DEPLOY_SCENARIO':
            return self.scenario
        return var

    @staticmethod
    def cmd_readline():
        return 'test_value\n'

    @mock.patch('functest.utils.functest_utils.LOGGER.error')
    @mock.patch('functest.utils.functest_utils.LOGGER.info')
    def test_exec_cmd_args_present_ko(self, mock_logger_info,
                                      mock_logger_error):
        with mock.patch('functest.utils.functest_utils.subprocess.Popen') \
                as mock_subproc_open, \
                mock.patch('six.moves.builtins.open',
                           mock.mock_open()) as mopen:

            FunctestUtilsTesting.readline = 0

            mock_obj = mock.Mock()
            attrs = {'readline.side_effect': self.cmd_readline()}
            mock_obj.configure_mock(**attrs)

            mock_obj2 = mock.Mock()
            attrs = {'stdout': mock_obj, 'wait.return_value': 1}
            mock_obj2.configure_mock(**attrs)

            mock_subproc_open.return_value = mock_obj2

            resp = functest_utils.execute_command(self.cmd, info=True,
                                                  error_msg=self.error_msg,
                                                  verbose=True,
                                                  output_file=self.output_file)
            self.assertEqual(resp, 1)
            msg_exec = ("Executing command: '%s'" % self.cmd)
            mock_logger_info.assert_called_once_with(msg_exec)
            mopen.assert_called_once_with(self.output_file, "w")
            mock_logger_error.assert_called_once_with(self.error_msg)

    @mock.patch('functest.utils.functest_utils.LOGGER.info')
    def test_exec_cmd_args_present_ok(self, mock_logger_info):
        with mock.patch('functest.utils.functest_utils.subprocess.Popen') \
                as mock_subproc_open, \
                mock.patch('six.moves.builtins.open',
                           mock.mock_open()) as mopen:

            FunctestUtilsTesting.readline = 0

            mock_obj = mock.Mock()
            attrs = {'readline.side_effect': self.cmd_readline()}
            mock_obj.configure_mock(**attrs)

            mock_obj2 = mock.Mock()
            attrs = {'stdout': mock_obj, 'wait.return_value': 0}
            mock_obj2.configure_mock(**attrs)

            mock_subproc_open.return_value = mock_obj2

            resp = functest_utils.execute_command(self.cmd, info=True,
                                                  error_msg=self.error_msg,
                                                  verbose=True,
                                                  output_file=self.output_file)
            self.assertEqual(resp, 0)
            msg_exec = ("Executing command: '%s'" % self.cmd)
            mock_logger_info.assert_called_once_with(msg_exec)
            mopen.assert_called_once_with(self.output_file, "w")

    @mock.patch('sys.stdout')
    def test_exec_cmd_args_missing_ok(self, stdout=None):
        # pylint: disable=unused-argument
        with mock.patch('functest.utils.functest_utils.subprocess.Popen') \
                as mock_subproc_open:

            FunctestUtilsTesting.readline = 2

            mock_obj = mock.Mock()
            attrs = {'readline.side_effect': self.cmd_readline()}
            mock_obj.configure_mock(**attrs)

            mock_obj2 = mock.Mock()
            attrs = {'stdout': mock_obj, 'wait.return_value': 0}
            mock_obj2.configure_mock(**attrs)

            mock_subproc_open.return_value = mock_obj2

            resp = functest_utils.execute_command(self.cmd, info=False,
                                                  error_msg="",
                                                  verbose=False,
                                                  output_file=None)
            self.assertEqual(resp, 0)

    @mock.patch('sys.stdout')
    def test_exec_cmd_args_missing_ko(self, stdout=None):
        # pylint: disable=unused-argument
        with mock.patch('functest.utils.functest_utils.subprocess.Popen') \
                as mock_subproc_open:

            FunctestUtilsTesting.readline = 2
            mock_obj = mock.Mock()
            attrs = {'readline.side_effect': self.cmd_readline()}
            mock_obj.configure_mock(**attrs)

            mock_obj2 = mock.Mock()
            attrs = {'stdout': mock_obj, 'wait.return_value': 1}
            mock_obj2.configure_mock(**attrs)

            mock_subproc_open.return_value = mock_obj2

            resp = functest_utils.execute_command(self.cmd, info=False,
                                                  error_msg="",
                                                  verbose=False,
                                                  output_file=None)
            self.assertEqual(resp, 1)

    def test_get_param_from_yaml_failed(self):
        self.file_yaml['general'] = None
        with mock.patch('six.moves.builtins.open', mock.mock_open()), \
                mock.patch('functest.utils.functest_utils.yaml.safe_load') \
                as mock_yaml, \
                self.assertRaises(ValueError) as excep:
            mock_yaml.return_value = self.file_yaml
            functest_utils.get_parameter_from_yaml(self.parameter,
                                                   self.test_file)
            self.assertTrue(("The parameter %s is not"
                             " defined in config_functest.yaml" %
                             self.parameter) in excep.exception)

    def test_get_param_from_yaml_def(self):
        with mock.patch('six.moves.builtins.open', mock.mock_open()), \
                mock.patch('functest.utils.functest_utils.yaml.safe_load') \
                as mock_yaml:
            mock_yaml.return_value = self.file_yaml
            self.assertEqual(functest_utils.
                             get_parameter_from_yaml(self.parameter,
                                                     self.test_file),
                             'test_image_name')

    def test_nova_version_exc1(self):
        # pylint: disable=protected-access
        cloud = mock.Mock()
        cloud._compute_client.request.return_value = None
        self.assertEqual(functest_utils.get_nova_version(cloud), None)
        cloud._compute_client.request.assert_called_once_with('/', 'GET')

    def test_nova_version_exc2(self):
        # pylint: disable=protected-access
        cloud = mock.Mock()
        cloud._compute_client.request.return_value = {"version": None}
        self.assertEqual(functest_utils.get_nova_version(cloud), None)
        cloud._compute_client.request.assert_called_once_with('/', 'GET')

    def test_nova_version_exc3(self):
        # pylint: disable=protected-access
        cloud = mock.Mock()
        cloud._compute_client.request.return_value = {
            "version": {"version": None}}
        self.assertEqual(functest_utils.get_nova_version(cloud), None)
        cloud._compute_client.request.assert_called_once_with('/', 'GET')

    def test_nova_version_exc4(self):
        # pylint: disable=protected-access
        cloud = mock.Mock()
        cloud._compute_client.request.return_value = {
            "version": {"version": "a.b"}}
        self.assertEqual(functest_utils.get_nova_version(cloud), None)
        cloud._compute_client.request.assert_called_once_with('/', 'GET')

    def test_nova_version(self):
        # pylint: disable=protected-access
        cloud = mock.Mock()
        cloud._compute_client.request.return_value = {
            "version": {"version": "2.1"}}
        self.assertEqual(functest_utils.get_nova_version(cloud), (2, 1))
        cloud._compute_client.request.assert_called_once_with('/', 'GET')

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=(2, 61))
    def test_openstack_version1(self, *args):
        cloud = mock.Mock()
        self.assertEqual(functest_utils.get_openstack_version(
            cloud), "Rocky or newer")
        args[0].assert_called_once_with(cloud)

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=(2, 60))
    def test_openstack_version2(self, *args):
        cloud = mock.Mock()
        self.assertEqual(functest_utils.get_openstack_version(cloud), "Queens")
        args[0].assert_called_once_with(cloud)

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=(2, 43))
    def test_openstack_version3(self, *args):
        cloud = mock.Mock()
        self.assertEqual(functest_utils.get_openstack_version(cloud), "Pike")
        args[0].assert_called_once_with(cloud)

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=(2, 39))
    def test_openstack_version4(self, *args):
        cloud = mock.Mock()
        self.assertEqual(functest_utils.get_openstack_version(cloud), "Ocata")
        args[0].assert_called_once_with(cloud)

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=(2, 26))
    def test_openstack_version5(self, *args):
        cloud = mock.Mock()
        self.assertEqual(functest_utils.get_openstack_version(cloud), "Newton")
        args[0].assert_called_once_with(cloud)

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=(2, 13))
    def test_openstack_version6(self, *args):
        cloud = mock.Mock()
        self.assertEqual(functest_utils.get_openstack_version(cloud), "Mitaka")
        args[0].assert_called_once_with(cloud)

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=(2, 4))
    def test_openstack_version7(self, *args):
        cloud = mock.Mock()
        self.assertEqual(
            functest_utils.get_openstack_version(cloud), "Liberty")
        args[0].assert_called_once_with(cloud)

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=(2, 1))
    def test_openstack_version8(self, *args):
        cloud = mock.Mock()
        self.assertEqual(functest_utils.get_openstack_version(cloud), "Kilo")
        args[0].assert_called_once_with(cloud)

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=(1, 9))
    def test_openstack_version9(self, *args):
        cloud = mock.Mock()
        self.assertEqual(
            functest_utils.get_openstack_version(cloud), "Unknown")
        args[0].assert_called_once_with(cloud)

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=(3, 1))
    def test_openstack_version10(self, *args):
        cloud = mock.Mock()
        self.assertEqual(
            functest_utils.get_openstack_version(cloud), "Rocky or newer")
        args[0].assert_called_once_with(cloud)

    @mock.patch('functest.utils.functest_utils.get_nova_version',
                return_value=None)
    def test_openstack_version_exc(self, *args):
        cloud = mock.Mock()
        self.assertEqual(
            functest_utils.get_openstack_version(cloud), "Unknown")
        args[0].assert_called_once_with(cloud)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
