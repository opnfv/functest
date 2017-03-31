#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.ci import prepare_env
from functest.tests.unit import test_utils
from functest.utils.constants import CONST
from opnfv.utils import constants as opnfv_constants


class PrepareEnvTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.prepare_envparser = prepare_env.PrepareEnvParser()
        self.db_url_env = 'http://foo/testdb'

    @mock.patch('functest.ci.prepare_env.logger.info')
    def test_print_separator(self, mock_logger_info):
        str = "=============================================="
        prepare_env.print_separator()
        mock_logger_info.assert_called_once_with(str)

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_missing_inst_type(self, mock_logger_warn,
                                                   mock_logger_info):
        CONST.INSTALLER_TYPE = None
        prepare_env.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_warn.assert_any_call("The env variable 'INSTALLER_TYPE'"
                                         " is not defined.")

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_missing_inst_ip(self, mock_logger_warn,
                                                 mock_logger_info):
        CONST.INSTALLER_IP = None
        prepare_env.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_warn.assert_any_call("The env variable 'INSTALLER_IP'"
                                         " is not defined. It is needed to"
                                         " fetch the OpenStack credentials."
                                         " If the credentials are not"
                                         " provided to the container as a"
                                         " volume, please add this env"
                                         " variable to the 'docker run'"
                                         " command.")

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_inst_ip(self, mock_logger_warn,
                                              mock_logger_info):
        CONST.INSTALLER_IP = mock.Mock()
        prepare_env.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_info.assert_any_call(test_utils.
                                         SubstrMatch("    INSTALLER_IP="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_missing_scenario(self, mock_logger_warn,
                                                  mock_logger_info):
        CONST.DEPLOY_SCENARIO = None
        prepare_env.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_warn.assert_any_call("The env variable"
                                         " 'DEPLOY_SCENARIO' is not defined"
                                         ". Setting CI_SCENARIO=undefined.")

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_scenario(self, mock_logger_warn,
                                               mock_logger_info):
        CONST.DEPLOY_SCENARIO = 'test_scenario'
        prepare_env.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_info.assert_any_call(test_utils.
                                         SubstrMatch("DEPLOY_SCENARIO="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_ci_debug(self, mock_logger_warn,
                                               mock_logger_info):
        CONST.CI_DEBUG = mock.Mock()
        prepare_env.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_info.assert_any_call(test_utils.
                                         SubstrMatch("    CI_DEBUG="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_node(self, mock_logger_warn,
                                           mock_logger_info):
        CONST.NODE_NAME = mock.Mock()
        prepare_env.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_info.assert_any_call(test_utils.
                                         SubstrMatch("    NODE_NAME="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_build_tag(self, mock_logger_warn,
                                                mock_logger_info):
        CONST.BUILD_TAG = mock.Mock()
        prepare_env.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")

        mock_logger_info.assert_any_call(test_utils.
                                         SubstrMatch("    BUILD_TAG="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_is_ci_run(self, mock_logger_warn,
                                                mock_logger_info):
        CONST.IS_CI_RUN = mock.Mock()
        prepare_env.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")

        mock_logger_info.assert_any_call(test_utils.
                                         SubstrMatch("    IS_CI_RUN="))

    def test_get_deployment_handler_missing_const_vars(self):
        with mock.patch('functest.ci.prepare_env.'
                        'factory.Factory.get_handler') as m:
            CONST.INSTALLER_IP = None
            prepare_env.get_deployment_handler()
            self.assertFalse(m.called)

            CONST.INSTALLER_TYPE = None
            prepare_env.get_deployment_handler()
            self.assertFalse(m.called)

    @mock.patch('functest.ci.prepare_env.logger.debug')
    def test_get_deployment_handler_missing_print_deploy_info(self,
                                                              mock_debug):
        with mock.patch('functest.ci.prepare_env.'
                        'factory.Factory.get_handler') as m, \
            mock.patch('functest.ci.prepare_env.'
                       'ft_utils.get_parameter_from_yaml',
                       side_effect=ValueError):
            CONST.INSTALLER_IP = 'test_ip'
            CONST.INSTALLER_TYPE = 'test_inst_type'
            opnfv_constants.INSTALLERS = ['test_inst_type']
            prepare_env.get_deployment_handler()
            msg = ('Printing deployment info is not supported for '
                   'test_inst_type')
            mock_debug.assert_any_call(msg)
            self.assertFalse(m.called)

    @mock.patch('functest.ci.prepare_env.logger.debug')
    def test_get_deployment_handler_exception(self, mock_debug):
        with mock.patch('functest.ci.prepare_env.'
                        'factory.Factory.get_handler',
                        side_effect=Exception), \
            mock.patch('functest.ci.prepare_env.'
                       'ft_utils.get_parameter_from_yaml'):
            CONST.INSTALLER_IP = 'test_ip'
            CONST.INSTALLER_TYPE = 'test_inst_type'
            opnfv_constants.INSTALLERS = ['test_inst_type']
            prepare_env.get_deployment_handler()
            self.assertTrue(mock_debug.called)

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.debug')
    def test_create_directories_missing_dir(self, mock_logger_debug,
                                            mock_logger_info):
        with mock.patch('functest.ci.prepare_env.os.path.exists',
                        return_value=False), \
                mock.patch('functest.ci.prepare_env.os.makedirs') \
                as mock_method:
            prepare_env.create_directories()
            mock_logger_info.assert_any_call("Creating needed directories...")
            mock_method.assert_any_call(CONST.dir_functest_conf)
            mock_method.assert_any_call(CONST.dir_functest_data)
            mock_logger_info.assert_any_call("    %s created." %
                                             CONST.dir_functest_conf)
            mock_logger_info.assert_any_call("    %s created." %
                                             CONST.dir_functest_data)

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.debug')
    def test_create_directories_with_dir(self, mock_logger_debug,
                                         mock_logger_info):
        with mock.patch('functest.ci.prepare_env.os.path.exists',
                        return_value=True):
            prepare_env.create_directories()
            mock_logger_info.assert_any_call("Creating needed directories...")
            mock_logger_debug.assert_any_call("   %s already exists." %
                                              CONST.dir_functest_conf)
            mock_logger_debug.assert_any_call("   %s already exists." %
                                              CONST.dir_functest_data)

    def _get_env_cred_dict(self, os_prefix=''):
        return {'OS_USERNAME': os_prefix + 'username',
                'OS_PASSWORD': os_prefix + 'password',
                'OS_AUTH_URL': 'http://test_ip:test_port/v2.0',
                'OS_TENANT_NAME': os_prefix + 'tenant_name',
                'OS_USER_DOMAIN_NAME': os_prefix + 'user_domain_name',
                'OS_PROJECT_DOMAIN_NAME': os_prefix + 'project_domain_name',
                'OS_PROJECT_NAME': os_prefix + 'project_name',
                'OS_ENDPOINT_TYPE': os_prefix + 'endpoint_type',
                'OS_REGION_NAME': os_prefix + 'region_name'}

    @mock.patch('functest.ci.prepare_env.logger.error')
    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_source_rc_missing_rc_file(self, mock_logger_warn,
                                       mock_logger_info,
                                       mock_logger_error):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=True), \
                mock.patch('functest.ci.prepare_env.os.path.getsize',
                           return_value=0), \
                self.assertRaises(Exception):
            CONST.openstack_creds = 'test_creds'
            prepare_env.source_rc_file()

    def test_source_rc_missing_installer_ip(self):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=False), \
                self.assertRaises(Exception):
            CONST.INSTALLER_IP = None
            CONST.openstack_creds = 'test_creds'
            prepare_env.source_rc_file()

    def test_source_rc_missing_installer_type(self):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=False), \
                self.assertRaises(Exception):
            CONST.INSTALLER_IP = 'test_ip'
            CONST.openstack_creds = 'test_creds'
            CONST.INSTALLER_TYPE = 'test_type'
            opnfv_constants.INSTALLERS = []
            prepare_env.source_rc_file()

    def test_source_rc_missing_os_credfile_ci_inst(self):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=False), \
                mock.patch('functest.ci.prepare_env.os.path.getsize'), \
                mock.patch('functest.ci.prepare_env.os.path.join'), \
                mock.patch('functest.ci.prepare_env.subprocess.Popen') \
                as mock_subproc_popen, \
                self.assertRaises(Exception):
            CONST.openstack_creds = 'test_creds'
            CONST.INSTALLER_IP = None
            CONST.INSTALLER_TYPE = 'test_type'
            opnfv_constants.INSTALLERS = ['test_type']

            process_mock = mock.Mock()
            attrs = {'communicate.return_value': ('output', 'error'),
                     'return_code': 1}
            process_mock.configure_mock(**attrs)
            mock_subproc_popen.return_value = process_mock

            prepare_env.source_rc_file()

    @mock.patch('functest.ci.prepare_env.logger.debug')
    def test_patch_file(self, mock_logger_debug):
        with mock.patch("__builtin__.open", mock.mock_open()), \
            mock.patch('functest.ci.prepare_env.yaml.safe_load',
                       return_value={'test_scenario': {'tkey': 'tvalue'}}), \
            mock.patch('functest.ci.prepare_env.ft_utils.get_functest_yaml',
                       return_value={'tkey1': 'tvalue1'}), \
            mock.patch('functest.ci.prepare_env.os.remove') as m, \
                mock.patch('functest.ci.prepare_env.yaml.dump'):
            CONST.DEPLOY_SCENARIO = 'test_scenario'
            prepare_env.patch_file('test_file')
            self.assertTrue(m.called)

    @mock.patch('functest.ci.prepare_env.update_db_url')
    def test_update_db_url(self, mock_db_url):
        with mock.patch("__builtin__.open", mock.mock_open()), \
            mock.patch('functest.ci.prepare_env.yaml.safe_load',
                       return_value={'test_scenario': {'tkey': 'tvalue'}}), \
            mock.patch('functest.ci.prepare_env.ft_utils.get_functest_yaml',
                       return_value={'tkey1': 'tvalue1'}), \
            mock.patch('functest.ci.prepare_env.yaml.dump'), \
                mock.patch.dict('functest.ci.prepare_env.os.environ',
                                {'TEST_DB_URL': self.db_url_env},
                                clear=True):
            prepare_env.update_config_file()
            self.assertTrue(mock_db_url.called)

    @mock.patch('functest.ci.prepare_env.logger.info')
    def test_verify_deployment_error(self, mock_logger_error):
        mock_popen = mock.Mock()
        attrs = {'poll.return_value': None,
                 'stdout.readline.return_value': 'ERROR'}
        mock_popen.configure_mock(**attrs)

        with mock.patch('functest.ci.prepare_env.print_separator') as m, \
            mock.patch('functest.ci.prepare_env.subprocess.Popen',
                       return_value=mock_popen), \
                self.assertRaises(Exception) as context:
            prepare_env.verify_deployment()
            self.assertTrue(m.called)
            msg = "Problem while running 'check_os.sh'."
            mock_logger_error.assert_called_once_with('ERROR')
            self.assertTrue(msg in context)

    def _get_rally_creds(self):
        return {"type": "ExistingCloud",
                "admin": {"username": 'test_user_name',
                          "password": 'test_password',
                          "tenant": 'test_tenant'}}

    @mock.patch('functest.ci.prepare_env.os_utils.get_credentials_for_rally')
    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.ft_utils.execute_command_raise')
    @mock.patch('functest.ci.prepare_env.ft_utils.execute_command')
    def test_install_rally(self, mock_exec, mock_exec_raise, mock_logger_info,
                           mock_os_utils):

        mock_os_utils.return_value = self._get_rally_creds()

        prepare_env.install_rally()

        cmd = "rally deployment destroy opnfv-rally"
        error_msg = "Deployment %s does not exist." % \
                    CONST.rally_deployment_name
        mock_logger_info.assert_any_call("Creating Rally environment...")
        mock_exec.assert_any_call(cmd, error_msg=error_msg, verbose=False)

        cmd = "rally deployment create --file=rally_conf.json --name="
        cmd += CONST.rally_deployment_name
        error_msg = "Problem while creating Rally deployment"
        mock_exec_raise.assert_any_call(cmd, error_msg=error_msg)

        cmd = "rally deployment check"
        error_msg = ("OpenStack not responding or "
                     "faulty Rally deployment.")
        mock_exec_raise.assert_any_call(cmd, error_msg=error_msg)

        cmd = "rally deployment list"
        error_msg = ("Problem while listing "
                     "Rally deployment.")
        mock_exec.assert_any_call(cmd, error_msg=error_msg)

        cmd = "rally plugin list | head -5"
        error_msg = ("Problem while showing "
                     "Rally plugins.")
        mock_exec.assert_any_call(cmd, error_msg=error_msg)

    @mock.patch('functest.ci.prepare_env.logger.debug')
    def test_install_tempest(self, mock_logger_debug):
        mock_popen = mock.Mock()
        attrs = {'poll.return_value': None,
                 'stdout.readline.return_value': '0'}
        mock_popen.configure_mock(**attrs)

        CONST.tempest_deployment_name = 'test_dep_name'
        with mock.patch('functest.ci.prepare_env.'
                        'ft_utils.execute_command_raise',
                        side_effect=Exception), \
            mock.patch('functest.ci.prepare_env.subprocess.Popen',
                       return_value=mock_popen), \
                self.assertRaises(Exception):
            prepare_env.install_tempest()
            mock_logger_debug.assert_any_call("Tempest test_dep_name"
                                              " does not exist")

    def test_create_flavor(self):
        with mock.patch('functest.ci.prepare_env.'
                        'os_utils.get_or_create_flavor',
                        return_value=('test_', None)), \
                self.assertRaises(Exception) as context:
            prepare_env.create_flavor()
            msg = 'Failed to create flavor'
            self.assertTrue(msg in context)

    @mock.patch('functest.ci.prepare_env.sys.exit')
    @mock.patch('functest.ci.prepare_env.logger.error')
    def test_check_environment_missing_file(self, mock_logger_error,
                                            mock_sys_exit):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=False), \
                self.assertRaises(Exception):
                prepare_env.check_environment()

    @mock.patch('functest.ci.prepare_env.sys.exit')
    @mock.patch('functest.ci.prepare_env.logger.error')
    def test_check_environment_with_error(self, mock_logger_error,
                                          mock_sys_exit):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=True), \
            mock.patch("__builtin__.open", mock.mock_open(read_data='0')), \
                self.assertRaises(Exception):
            prepare_env.check_environment()

    @mock.patch('functest.ci.prepare_env.logger.info')
    def test_check_environment_default(self, mock_logger_info):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=True):
            with mock.patch("__builtin__.open", mock.mock_open(read_data='1')):
                prepare_env.check_environment()
                mock_logger_info.assert_any_call("Functest environment"
                                                 " is installed.")

    @mock.patch('functest.ci.prepare_env.print_deployment_info')
    @mock.patch('functest.ci.prepare_env.check_environment')
    @mock.patch('functest.ci.prepare_env.create_flavor')
    @mock.patch('functest.ci.prepare_env.install_tempest')
    @mock.patch('functest.ci.prepare_env.install_rally')
    @mock.patch('functest.ci.prepare_env.verify_deployment')
    @mock.patch('functest.ci.prepare_env.update_config_file')
    @mock.patch('functest.ci.prepare_env.source_rc_file')
    @mock.patch('functest.ci.prepare_env.create_directories')
    @mock.patch('functest.ci.prepare_env.get_deployment_handler')
    @mock.patch('functest.ci.prepare_env.check_env_variables')
    @mock.patch('functest.ci.prepare_env.logger.info')
    def test_main_start(self, mock_logger_info, mock_env_var, mock_dep_handler,
                        mock_create_dir, mock_source_rc, mock_update_config,
                        mock_verify_depl, mock_install_rally,
                        mock_install_temp, mock_create_flavor,
                        mock_check_env, mock_print_info):
        with mock.patch("__builtin__.open", mock.mock_open()) as m:
            args = {'action': 'start'}
            self.assertEqual(prepare_env.main(**args), 0)
            mock_logger_info.assert_any_call("######### Preparing Functest "
                                             "environment #########\n")
            self.assertTrue(mock_env_var.called)
            self.assertTrue(mock_dep_handler.called)
            self.assertTrue(mock_create_dir.called)
            self.assertTrue(mock_source_rc.called)
            self.assertTrue(mock_update_config.called)
            self.assertTrue(mock_verify_depl.called)
            self.assertTrue(mock_install_rally.called)
            self.assertTrue(mock_install_temp.called)
            self.assertTrue(mock_create_flavor.called)
            m.assert_called_once_with(CONST.env_active, "w")
            self.assertTrue(mock_check_env.called)
            self.assertTrue(mock_print_info.called)

    @mock.patch('functest.ci.prepare_env.check_environment')
    def test_main_check(self, mock_check_env):
        args = {'action': 'check'}
        self.assertEqual(prepare_env.main(**args), 0)
        self.assertTrue(mock_check_env.called)

    @mock.patch('functest.ci.prepare_env.logger.error')
    def test_main_no_arg(self, mock_logger_error):
        args = {'action': 'not_valid'}
        self.assertEqual(prepare_env.main(**args), -1)
        mock_logger_error.assert_called_once_with('Argument not valid.')


if __name__ == "__main__":
    unittest.main(verbosity=2)
