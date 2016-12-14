#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import os
import re
import unittest

from git.exc import NoSuchPathError
from functest.cli.commands import cli_env
from functest.utils import functest_constants as ft_constants
from functest.utils import functest_utils as ft_utils

class AnyStringWith(str):
    def __eq__(self, other):
        match = re.search(self, other)
        if match:
            return True
        return False

class CliEnvTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.cli_environ = cli_env.CliEnv()

    @mock.patch('functest.cli.commands.cli_testcase.os.path.isfile', return_value=False)
    @mock.patch('functest.cli.commands.cli_testcase.ft_utils.execute_command')
    def test_prepare(self, mock_ft_utils, mock_os):
        cmd = ("python %s/functest/ci/prepare_env.py start" %
               ft_constants.FUNCTEST_REPO_DIR)
        self.cli_environ.prepare()
        mock_ft_utils.assert_called_with(cmd)

    def _test_show_missing_env_var(self, var, *args):
        if var == 'CI_INSTALLER_TYPE':
            ft_constants.CI_INSTALLER_TYPE = None
            reg_string = "|  INSTALLER: Unknown, \S+\s*|"
        elif var == 'CI_INSTALLER_IP':
            ft_constants.CI_INSTALLER_TYPE = None
            reg_string = "|  INSTALLER: \S+, Unknown\s*|"
        elif var == 'CI_SCENARIO':
            ft_constants.CI_SCENARIO = None
            reg_string = "|   SCENARIO: Unknown\s*|"
        elif var == 'CI_NODE':
            ft_constants.CI_NODE = None
            reg_string = "|        POD: Unknown\s*|"
        elif var == 'CI_BUILD_TAG':
            ft_constants.CI_BUILD_TAG = None
            reg_string = "|  BUILD TAG: None|"
        elif var == 'CI_DEBUG':
            ft_constants.CI_DEBUG = None
            reg_string = "| DEBUG FLAG: false\s*|"
        elif var == 'STATUS':
            reg_string = "|     STATUS: not ready\s*|"

        with mock.patch('functest.cli.commands.cli_env.click.echo') as mock_click_echo:
            self.cli_environ.show()
            mock_click_echo.assert_called_with(AnyStringWith(reg_string))

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_installer_type(self, *args):
        self._test_show_missing_env_var('CI_INSTALLER_TYPE', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_installer_ip(self, *args):
        self._test_show_missing_env_var('CI_INSTALLER_IP', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_scenario(self, *args):
        self._test_show_missing_env_var('CI_SCENARIO', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_node(self, *args):
        self._test_show_missing_env_var('CI_NODE', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_build_tag(self, *args):
        self._test_show_missing_env_var('CI_BUILD_TAG', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    def test_show_missing_ci_debug(self, *args):
        self._test_show_missing_env_var('CI_DEBUG', *args)

    @mock.patch('functest.cli.commands.cli_env.git.Repo')
    @mock.patch('functest.cli.commands.cli_env.os.path.isfile', return_value=False)
    def test_show_missing_environment(self, *args):
        self._test_show_missing_env_var('STATUS', *args)

    @mock.patch('functest.cli.commands.cli_env.os.path.exists', return_value=False)
    def test_show_missing_git_repo_dir(self, *args):
        ft_constants.FUNCTEST_REPO_DIR = None
        self.assertRaises(NoSuchPathError, lambda: self.cli_environ.show())

    @mock.patch('functest.cli.commands.cli_env.click.echo')
    @mock.patch('functest.cli.commands.cli_env.os.path.isfile', return_value=True)
    def test_status_environment_present(self, mock_path, mock_click_echo):
        self.assertEqual(self.cli_environ.status(), 0)
        mock_click_echo.assert_called_with("Functest environment ready to run tests.\n")

    @mock.patch('functest.cli.commands.cli_env.click.echo')
    @mock.patch('functest.cli.commands.cli_env.os.path.isfile', return_value=False)
    def test_status_environment_absent(self, mock_path, mock_click_echo):
        self.assertEqual(self.cli_environ.status(), 1)
        mock_click_echo.assert_called_with("Functest environment is not installed.\n")

if __name__ == "__main__":
    unittest.main(verbosity=2)
