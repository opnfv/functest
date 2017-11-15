#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.cli.commands import cli_env
from functest.utils.constants import CONST
from functest.tests.unit import test_utils


class CliEnvTesting(unittest.TestCase):

    def setUp(self):
        self.cli_environ = cli_env.CliEnv()

    def _test_show_missing_env_var(self, var, *args):
        if var == 'INSTALLER_TYPE':
            CONST.__setattr__('INSTALLER_TYPE', None)
            reg_string = "|  INSTALLER: Unknown, \S+\s*|"
        elif var == 'INSTALLER_IP':
            CONST.__setattr__('INSTALLER_IP', None)
            reg_string = "|  INSTALLER: \S+, Unknown\s*|"
        elif var == 'SCENARIO':
            CONST.__setattr__('DEPLOY_SCENARIO', None)
            reg_string = "|   SCENARIO: Unknown\s*|"
        elif var == 'NODE':
            CONST.__setattr__('NODE_NAME', None)
            reg_string = "|        POD: Unknown\s*|"
        elif var == 'BUILD_TAG':
            CONST.__setattr__('BUILD_TAG', None)
            reg_string = "|  BUILD TAG: None|"
        elif var == 'DEBUG':
            CONST.__setattr__('CI_DEBUG', None)
            reg_string = "| DEBUG FLAG: false\s*|"
        elif var == 'STATUS':
            reg_string = "|     STATUS: not ready\s*|"

        with mock.patch('functest.cli.commands.cli_env.click.echo') \
                as mock_click_echo:
            self.cli_environ.show()
            mock_click_echo.assert_called_with(test_utils.
                                               RegexMatch(reg_string))

    def test_show_missing_ci_installer_type(self, *args):
        self._test_show_missing_env_var('INSTALLER_TYPE', *args)

    def test_show_missing_ci_installer_ip(self, *args):
        self._test_show_missing_env_var('INSTALLER_IP', *args)

    def test_show_missing_ci_scenario(self, *args):
        self._test_show_missing_env_var('SCENARIO', *args)

    def test_show_missing_ci_node(self, *args):
        self._test_show_missing_env_var('NODE', *args)

    def test_show_missing_ci_build_tag(self, *args):
        self._test_show_missing_env_var('BUILD_TAG', *args)

    def test_show_missing_ci_debug(self, *args):
        self._test_show_missing_env_var('DEBUG', *args)

    @mock.patch('functest.cli.commands.cli_env.os.path.isfile',
                return_value=False)
    def test_show_missing_environment(self, *args):
        self._test_show_missing_env_var('STATUS', *args)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
