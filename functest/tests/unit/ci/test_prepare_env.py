#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest

from functest.ci import prepare_env as pe
from functest.utils import functest_constants as ft_constants

from nose.tools import raises


class AnyStringWith(str):
    def __eq__(self, other):
        if self in other:
            return True
        return False


class PrepareEnvTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.parser = pe.parser

    @mock.patch('functest.ci.prepare_env.logger.info')
    def test_print_separator(self, mock_logger_info):
        str = "=============================================="
        pe.print_separator()
        mock_logger_info.assert_called_once_with(str)

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_missing_ci_inst_type(self, mock_logger_warn,
                                                      mock_logger_info):
        ft_constants.CI_INSTALLER_TYPE = None
        pe.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_warn.assert_any_call("The env variable 'INSTALLER_TYPE'"
                                         " is not defined.")

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_missing_ci_inst_ip(self, mock_logger_warn,
                                                    mock_logger_info):
        ft_constants.CI_INSTALLER_IP = None
        pe.check_env_variables()
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
    def test_check_env_variables_with_ci_inst_ip(self, mock_logger_warn,
                                                 mock_logger_info):
        ft_constants.CI_INSTALLER_IP = mock.Mock()
        pe.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_info.assert_any_call(AnyStringWith("    INSTALLER_IP="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_missing_ci_scenario(self, mock_logger_warn,
                                                     mock_logger_info):
        ft_constants.CI_SCENARIO = None
        pe.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_warn.assert_any_call("The env variable"
                                         " 'DEPLOY_SCENARIO' is not defined"
                                         ". Setting CI_SCENARIO=undefined.")

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_ci_scenario(self, mock_logger_warn,
                                                  mock_logger_info):
        ft_constants.CI_SCENARIO = mock.Mock()
        pe.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_info.assert_any_call(AnyStringWith("DEPLOY_SCENARIO="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_ci_debug(self, mock_logger_warn,
                                               mock_logger_info):
        ft_constants.CI_DEBUG = mock.Mock()
        pe.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_info.assert_any_call(AnyStringWith("    CI_DEBUG="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_ci_node(self, mock_logger_warn,
                                              mock_logger_info):
        ft_constants.CI_NODE = mock.Mock()
        pe.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")
        mock_logger_info.assert_any_call(AnyStringWith("    NODE_NAME="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_ci_build_tag(self, mock_logger_warn,
                                                   mock_logger_info):
        ft_constants.CI_BUILD_TAG = mock.Mock()
        pe.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")

        mock_logger_info.assert_any_call(AnyStringWith("    BUILD_TAG="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_check_env_variables_with_is_ci_run(self, mock_logger_warn,
                                                mock_logger_info):
        ft_constants.IS_CI_RUN = mock.Mock()
        pe.check_env_variables()
        mock_logger_info.assert_any_call("Checking environment variables"
                                         "...")

        mock_logger_info.assert_any_call(AnyStringWith("    IS_CI_RUN="))

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.debug')
    def test_create_directories_missing_dir(self, mock_logger_debug,
                                            mock_logger_info):
        with mock.patch('functest.ci.prepare_env.os.path.exists',
                        return_value=False), \
                mock.patch('functest.ci.prepare_env.os.makedirs') \
                as mock_method:
            pe.create_directories()
            mock_logger_info.assert_any_call("Creating needed directories...")
            mock_method.assert_any_call(ft_constants.FUNCTEST_CONF_DIR)
            mock_method.assert_any_call(ft_constants.FUNCTEST_DATA_DIR)
            mock_logger_info.assert_any_call("    %s created." %
                                             ft_constants.FUNCTEST_CONF_DIR)
            mock_logger_info.assert_any_call("    %s created." %
                                             ft_constants.FUNCTEST_DATA_DIR)

    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.debug')
    def test_create_directories_with_dir(self, mock_logger_debug,
                                         mock_logger_info):
        with mock.patch('functest.ci.prepare_env.os.path.exists',
                        return_value=True):
            pe.create_directories()
            mock_logger_info.assert_any_call("Creating needed directories...")
            mock_logger_debug.assert_any_call("   %s already exists." %
                                              ft_constants.FUNCTEST_CONF_DIR)
            mock_logger_debug.assert_any_call("   %s already exists." %
                                              ft_constants.FUNCTEST_DATA_DIR)

    @mock.patch('functest.ci.prepare_env.logger.error')
    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_source_rc_missing_os_cred(self, mock_logger_warn,
                                       mock_logger_info,
                                       mock_logger_error):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=True), \
                mock.patch('functest.ci.prepare_env.os.path.getsize',
                           return_value=0), \
                mock.patch('functest.ci.prepare_env.os.path.join') \
                as mock_method, \
                mock.patch('functest.ci.prepare_env.sys.exit') \
                as mock_sys_exit:
            ft_constants.OPENSTACK_CREDS = None
            pe.source_rc_file()
            mock_logger_info.assert_any_call("Fetching RC file...")
            mock_logger_warn.assert_any_call("The environment variable 'creds'"
                                             " must be set andpointing to the "
                                             "local RC file. Using default: "
                                             "/home/opnfv/functest/conf/"
                                             "openstack.creds ...")
            mock_method.assert_called_once_with(ft_constants.FUNCTEST_CONF_DIR,
                                                'openstack.creds')
            mock_logger_info.assert_any_call("RC file provided in %s."
                                             % ft_constants.OPENSTACK_CREDS)
            mock_logger_error.assert_any_call("The file %s is empty."
                                              % ft_constants.OPENSTACK_CREDS)
            mock_sys_exit.assert_any_call(1)

    @mock.patch('functest.ci.prepare_env.os_utils.source_credentials')
    @mock.patch('functest.ci.prepare_env.logger.debug')
    @mock.patch('functest.ci.prepare_env.logger.error')
    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.logger.warning')
    def test_source_rc_missing_os_credfile_ci_inst(self, mock_logger_warn,
                                                   mock_logger_info,
                                                   mock_logger_error,
                                                   mock_logger_debug,
                                                   mock_os_utils):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=False), \
                mock.patch('functest.ci.prepare_env.os.path.getsize'), \
                mock.patch('functest.ci.prepare_env.os.path.join'), \
                mock.patch('functest.ci.prepare_env.subprocess.Popen') \
                as mock_subproc_popen, \
                mock.patch('functest.ci.prepare_env.sys.exit') \
                as mock_sys_exit:

            ft_constants.CI_INSTALLER_IP = None
            ft_constants.CI_INSTALLER_TYPE = 'test_type'
            ft_constants.INSTALLERS = ['test_type']

            process_mock = mock.Mock()
            attrs = {'communicate.return_value': ('output', 'error'),
                     'return_code': 1}
            process_mock.configure_mock(**attrs)
            mock_subproc_popen.return_value = process_mock

            pe.source_rc_file()

            mock_logger_info.assert_any_call("RC file not provided. Fetching"
                                             " it from the installer...")
            mock_logger_error.assert_any_call("The env variable CI_INSTALLER"
                                              "_IP must be provided in order"
                                              " to fetch the credentials from"
                                              " the installer.")
            mock_sys_exit.assert_any_call("Missing CI_INSTALLER_IP.")
            cmd = ("/home/opnfv/repos/releng/utils/fetch_os_creds.sh "
                   "-d %s -i %s -a %s"
                   % (ft_constants.OPENSTACK_CREDS,
                      ft_constants.CI_INSTALLER_TYPE,
                      ft_constants.CI_INSTALLER_IP))
            mock_logger_debug.assert_any_call("Executing command: %s" % cmd)
            mock_sys_exit.assert_any_call(1)

    def _get_rally_creds(self):
        return {"type": "ExistingCloud",
                "admin": {"username": 'test_user_name',
                          "password": 'test_password',
                          "tenant": 'test_tenant'}}

    @mock.patch('functest.ci.prepare_env.os_utils.get_credentials_for_rally')
    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.ft_utils.execute_command')
    def test_install_rally(self, mock_exec, mock_logger_info, mock_os_utils):

        mock_os_utils.return_value = self._get_rally_creds()

        pe.install_rally()

        cmd = "rally deployment destroy opnfv-rally"
        error_msg = "Deployment %s does not exist." % \
                    ft_constants.RALLY_DEPLOYMENT_NAME
        mock_logger_info.assert_any_call("Creating Rally environment...")
        mock_exec.assert_any_call(cmd, error_msg=error_msg, verbose=False)

        cmd = "rally deployment create --file=rally_conf.json --name="
        cmd += ft_constants.RALLY_DEPLOYMENT_NAME
        error_msg = "Problem creating Rally deployment"
        mock_exec.assert_any_call(cmd, error_msg=error_msg)

        mock_logger_info.assert_any_call("Installing tempest from existing"
                                         " repo...")
        cmd = ("rally verify install --source " +
               ft_constants.TEMPEST_REPO_DIR +
               " --system-wide")
        error_msg = "Problem installing Tempest."
        mock_exec.assert_any_call(cmd, error_msg=error_msg)

        cmd = "rally deployment check"
        error_msg = ("OpenStack not responding or "
                     "faulty Rally deployment.")
        mock_exec.assert_any_call(cmd, error_msg=error_msg)

        cmd = "rally show images"
        error_msg = ("Problem while listing "
                     "OpenStack images.")
        mock_exec.assert_any_call(cmd, error_msg=error_msg)

        cmd = "rally show flavors"
        error_msg = ("Problem while showing "
                     "OpenStack flavors.")
        mock_exec.assert_any_call(cmd, error_msg=error_msg)

    @mock.patch('functest.ci.prepare_env.sys.exit')
    @mock.patch('functest.ci.prepare_env.logger.error')
    def test_check_environment_missing_file(self, mock_logger_error,
                                            mock_sys_exit):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=False):
            with mock.patch("__builtin__.open", mock.mock_open(read_data='1')):
                pe.check_environment()
                msg_not_active = "The Functest environment is not installed."
                mock_logger_error.assert_any_call(msg_not_active)
                mock_sys_exit.assert_any_call(1)

    @mock.patch('functest.ci.prepare_env.sys.exit')
    @mock.patch('functest.ci.prepare_env.logger.error')
    def test_check_environment_with_error(self, mock_logger_error,
                                          mock_sys_exit):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=True):
            with mock.patch("__builtin__.open", mock.mock_open(read_data='0')):
                pe.check_environment()
                msg_not_active = "The Functest environment is not installed."
                mock_logger_error.assert_any_call(msg_not_active)
                mock_sys_exit.assert_any_call(1)

    @mock.patch('functest.ci.prepare_env.logger.info')
    def test_check_environment_default(self, mock_logger_info):
        with mock.patch('functest.ci.prepare_env.os.path.isfile',
                        return_value=True):
            with mock.patch("__builtin__.open", mock.mock_open(read_data='1')):
                pe.check_environment()
                mock_logger_info.assert_any_call("Functest environment"
                                                 " installed.")

    @raises(SystemExit)
    @mock.patch('functest.ci.prepare_env.check_environment')
    @mock.patch('functest.ci.prepare_env.install_rally')
    @mock.patch('functest.ci.prepare_env.verify_deployment')
    @mock.patch('functest.ci.prepare_env.patch_config_file')
    @mock.patch('functest.ci.prepare_env.source_rc_file')
    @mock.patch('functest.ci.prepare_env.create_directories')
    @mock.patch('functest.ci.prepare_env.check_env_variables')
    @mock.patch('functest.ci.prepare_env.logger.info')
    def test_main_start(self, mock_logger_info, mock_env_var,
                        mock_create_dir, mock_source_rc, mock_patch_config,
                        mock_verify_depl, mock_install_rally, mock_check_env):
        args = self.parser.parse_args(['start', '-d'])
        pe.args = args
        with mock.patch("__builtin__.open", mock.mock_open()) as m:
            pe.main()
            mock_logger_info.assert_any_call("######### Preparing Functest "
                                             "environment #########\n")
            self.assertTrue(mock_env_var.called)
            self.assertTrue(mock_create_dir.called)
            self.assertTrue(mock_source_rc.called)
            self.assertTrue(mock_patch_config.called)
            self.assertTrue(mock_verify_depl.called)
            self.assertTrue(mock_install_rally.called)
            m.assert_called_once_with(ft_constants.ENV_FILE, "w")
            handle = m()
            handle.assert_called_once_with("1")
            self.assertTrue(mock_check_env.called)

    @raises(SystemExit)
    @mock.patch('functest.ci.prepare_env.check_environment')
    def test_main_check(self, mock_check_env):
        args = self.parser.parse_args(['check', '-d'])
        pe.args = args
        pe.main()
        self.assertTrue(mock_check_env.called)

    @raises(SystemExit)
    @mock.patch('functest.ci.prepare_env.sys.exit')
    @mock.patch('functest.ci.prepare_env.logger.error')
    def test_main_no_arg(self, mock_logger_error, mock_sys_exit):
        args = self.parser.parse_args(['test_no', '-d'])
        pe.args = args
        pe.main()
        mock_logger_error.assert_called_once_with('Argument not valid.')
        self.assertTrue(mock_sys_exit)


if __name__ == "__main__":
    unittest.main(verbosity=2)
