#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import pkg_resources
import os
import time
import unittest

import mock
from six.moves import urllib

from functest.utils import functest_utils


class FunctestUtilsTesting(unittest.TestCase):

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
        self.testcase_dict = {'case_name': 'testname',
                              'criteria': self.criteria}
        self.parameter = 'general.openstack.image_name'
        self.config_yaml = pkg_resources.resource_filename(
            'functest', 'ci/config_functest.yaml')
        self.db_url_env = 'http://foo/testdb'
        self.testcases_yaml = "test_testcases_yaml"
        self.file_yaml = {'general': {'openstack': {'image_name':
                                                    'test_image_name'}}}

    @mock.patch('six.moves.urllib.request.urlopen',
                side_effect=urllib.error.URLError('no host given'))
    def test_check_internet_connectivity_failed(self, mock_method):
        self.assertFalse(functest_utils.check_internet_connectivity())
        mock_method.assert_called_once_with(self.url, timeout=self.timeout)

    @mock.patch('six.moves.urllib.request.urlopen')
    def test_check_internet_connectivity_default(self, mock_method):
        self.assertTrue(functest_utils.check_internet_connectivity())
        mock_method.assert_called_once_with(self.url, timeout=self.timeout)

    @mock.patch('six.moves.urllib.request.urlopen')
    def test_check_internet_connectivity_debian(self, mock_method):
        self.url = "https://www.debian.org/"
        self.assertTrue(functest_utils.check_internet_connectivity(self.url))
        mock_method.assert_called_once_with(self.url, timeout=self.timeout)

    @mock.patch('six.moves.urllib.request.urlopen',
                side_effect=urllib.error.URLError('no host given'))
    def test_download_url_failed(self, mock_url):
        self.assertFalse(functest_utils.download_url(self.url, self.dest_path))

    @mock.patch('six.moves.urllib.request.urlopen')
    def test_download_url_default(self, mock_url):
        with mock.patch("six.moves.builtins.open", mock.mock_open()) as m, \
                mock.patch('functest.utils.functest_utils.shutil.copyfileobj')\
                as mock_sh:
            name = self.url.rsplit('/')[-1]
            dest = self.dest_path + "/" + name
            self.assertTrue(functest_utils.download_url(self.url,
                                                        self.dest_path))
            m.assert_called_once_with(dest, 'wb')
            self.assertTrue(mock_sh.called)

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

    # TODO: get_resolvconf_ns
    @mock.patch('functest.utils.functest_utils.dns.resolver.Resolver')
    def test_get_resolvconf_ns_default(self, mock_dns_resolve):
        attrs = {'query.return_value': ["test"]}
        mock_dns_resolve.configure_mock(**attrs)

        m = mock.Mock()
        attrs = {'readline.side_effect': self.readline_side}
        m.configure_mock(**attrs)

        with mock.patch("six.moves.builtins.open") as mo:
            mo.return_value = m
            self.assertEqual(functest_utils.get_resolvconf_ns(),
                             self.test_ip[1:])

    def _get_environ(self, var):
        if var == 'INSTALLER_TYPE':
            return self.installer
        elif var == 'DEPLOY_SCENARIO':
            return self.scenario
        return var

    def test_get_ci_envvars_default(self):
        with mock.patch('os.environ.get',
                        side_effect=self._get_environ):
            dic = {"installer": self.installer,
                   "scenario": self.scenario}
            self.assertDictEqual(functest_utils.get_ci_envvars(), dic)

    def cmd_readline(self):
        return 'test_value\n'

    @mock.patch('functest.utils.functest_utils.logger.error')
    @mock.patch('functest.utils.functest_utils.logger.info')
    def test_execute_command_args_present_with_error(self, mock_logger_info,
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

    @mock.patch('functest.utils.functest_utils.logger.info')
    def test_execute_command_args_present_with_success(self, mock_logger_info,
                                                       ):
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
    def test_execute_command_args_missing_with_success(self, stdout=None):
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
    def test_execute_command_args_missing_with_error(self, stdout=None):
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

    def _get_functest_config(self, var):
        return var

    @mock.patch('functest.utils.functest_utils.logger.error')
    def test_get_dict_by_test(self, mock_logger_error):
        with mock.patch('six.moves.builtins.open', mock.mock_open()), \
                mock.patch('functest.utils.functest_utils.yaml.safe_load') \
                as mock_yaml:
            mock_obj = mock.Mock()
            attrs = {'get.return_value': [{'testcases': [self.testcase_dict]}]}
            mock_obj.configure_mock(**attrs)

            mock_yaml.return_value = mock_obj

            self.assertDictEqual(functest_utils.
                                 get_dict_by_test(self.testname),
                                 self.testcase_dict)

    @mock.patch('functest.utils.functest_utils.get_dict_by_test')
    def test_get_criteria_by_test_default(self, mock_get_dict_by_test):
        mock_get_dict_by_test.return_value = self.testcase_dict
        self.assertEqual(functest_utils.get_criteria_by_test(self.testname),
                         self.criteria)

    @mock.patch('functest.utils.functest_utils.get_dict_by_test')
    def test_get_criteria_by_test_failed(self, mock_get_dict_by_test):
        mock_get_dict_by_test.return_value = None
        self.assertIsNone(functest_utils.get_criteria_by_test(self.testname))

    def test_get_parameter_from_yaml_failed(self):
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

    def test_get_parameter_from_yaml_default(self):
        with mock.patch('six.moves.builtins.open', mock.mock_open()), \
                mock.patch('functest.utils.functest_utils.yaml.safe_load') \
                as mock_yaml:
            mock_yaml.return_value = self.file_yaml
            self.assertEqual(functest_utils.
                             get_parameter_from_yaml(self.parameter,
                                                     self.test_file),
                             'test_image_name')

    @mock.patch('functest.utils.functest_utils.get_parameter_from_yaml')
    def test_get_functest_config_default(self, mock_get_parameter_from_yaml):
        with mock.patch.dict(os.environ,
                             {'CONFIG_FUNCTEST_YAML': self.config_yaml}):
            functest_utils.get_functest_config(self.parameter)
            mock_get_parameter_from_yaml. \
                assert_called_once_with(self.parameter,
                                        self.config_yaml)

    def test_get_functest_yaml(self):
        with mock.patch('six.moves.builtins.open', mock.mock_open()), \
                mock.patch('functest.utils.functest_utils.yaml.safe_load') \
                as mock_yaml:
            mock_yaml.return_value = self.file_yaml
            resp = functest_utils.get_functest_yaml()
            self.assertEqual(resp, self.file_yaml)

    @mock.patch('functest.utils.functest_utils.logger.info')
    def test_print_separator(self, mock_logger_info):
        functest_utils.print_separator()
        mock_logger_info.assert_called_once_with("======================="
                                                 "=======================")


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
