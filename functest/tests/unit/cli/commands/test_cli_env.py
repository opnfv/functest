#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

from git.exc import NoSuchPathError
import mock

from functest.cli.commands import cli_env
from functest.utils.constants import CONST
from functest.tests.unit import test_utils


class CliEnvTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.cli_environ = cli_env.CliEnv()

    @mock.patch('functest.cli.commands.cli_testcase.os.path.isfile',
                return_value=False)
    @mock.patch('functest.cli.commands.cli_testcase.ft_utils.execute_command')
    def test_prepare_default(self, mock_ft_utils, mock_os):
        cmd = ("python %s/functest/ci/prepare_env.py start" %
               CONST.dir_repo_functest)
        self.cli_environ.prepare()
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.cli.commands.cli_testcase.os.path.isfile',
                return_value=True)
    @mock.patch('functest.cli.commands.cli_testcase.ft_utils.execute_command')
    def test_prepare_missing_status(self, mock_ft_utils, mock_os):
        with mock.patch('__builtin__.raw_input', return_value="y"), \
                mock.patch('functest.cli.commands.cli_testcase.os.remove') \
                as mock_os_remove:
            cmd = ("python %s/functest/ci/prepare_env.py start" %
                   CONST.dir_repo_functest)
            self.cli_environ.prepare()
            mock_os_remove.assert_called_once_with(CONST.env_active)
            mock_ft_utils.assert_called_with(cmd)

    def _test_show_missing_env_var(self, var, *args):
        if var == 'INSTALLER_TYPE':
            CONST.INSTALLER_TYPE = None
            reg_string = "|  INSTALLER: Unknown, \S+\s*|"
        elif var == 'INSTALLER_IP':
            CONST.INSTALLER_IP = None
            reg_string = "|  INSTALLER: \S+, Unknown\s*|"
        elif var == 'SCENARIO':
            CONST.DEPLOY_SCENARIO = None
            reg_string = "|   SCENARIO: Unknown\s*|"
        elif var == 'NODE':
            CONST.NODE_NAME = None
            reg_string = "|        POD: Unknown\s*|"
        elif var == 'BUILD_TAG':
            CONST.BUILD_TAG = None
            reg_string = "|  BUILD TAG: None|"
        elif var == 'DEBUG':
            CONST.CI_DEBUG = None
            reg_string = "| DEBUG FLAG: false\s*|"
        elif var == 'STATUS':
            reg_string = "|     STATUS: not ready\s*|"

        with mock.patch('functest.cli.commands.cli_env.click.echo') \
                as mock_click_echo:
            self.cli_environ.show()
            mock_click_echo.assert_called_with(test_utils.
                                               RegexMatch(reg_string))

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_installer_type(self, *args):
        self._test_show_missing_env_var('INSTALLER_TYPE', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_installer_ip(self, *args):
        self._test_show_missing_env_var('INSTALLER_IP', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_scenario(self, *args):
        self._test_show_missing_env_var('SCENARIO', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_node(self, *args):
        self._test_show_missing_env_var('NODE', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_build_tag(self, *args):
        self._test_show_missing_env_var('BUILD_TAG', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_debug(self, *args):
        self._test_show_missing_env_var('DEBUG', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    @mock.patch('functest.cli.commands.cli_env.os.path.isfile',
                return_value=False)
    def test_show_missing_environment(self, *args):
        self._test_show_missing_env_var('STATUS', *args)

    @mock.patch('functest.cli.commands.cli_env.os.path.exists',
                return_value=False)
    def test_show_missing_git_repo_dir(self, *args):
        CONST.dir_repo_functest = None
        self.assertRaises(NoSuchPathError, lambda: self.cli_environ.show())

    @mock.patch('functest.cli.commands.cli_env.click.echo')
    @mock.patch('functest.cli.commands.cli_env.os.path.isfile',
                return_value=True)
    def test_status_environment_present(self, mock_path, mock_click_echo):
        self.assertEqual(self.cli_environ.status(), 0)
        mock_click_echo.assert_called_with("Functest environment"
                                           " ready to run tests.\n")

    @mock.patch('functest.cli.commands.cli_env.click.echo')
    @mock.patch('functest.cli.commands.cli_env.os.path.isfile',
                return_value=False)
    def test_status_environment_absent(self, mock_path, mock_click_echo):
        self.assertEqual(self.cli_environ.status(), 1)
        mock_click_echo.assert_called_with("Functest environment"
                                           " is not installed.\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
