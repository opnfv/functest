#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import os
import re
import unittest

import mock

from functest.cli.commands import cli_env


class RegexMatch(object):  # pylint: disable=too-few-public-methods
    def __init__(self, msg):
        self.msg = msg

    def __eq__(self, other):
        match = re.search(self.msg, other)
        return match is not None


class CliEnvTesting(unittest.TestCase):

    def setUp(self):
        self.cli_environ = cli_env.CliEnv()

    def _test_show_missing_env_var(self, var, *args):
        # pylint: disable=unused-argument
        if var == 'INSTALLER_TYPE':
            os.environ['INSTALLER_TYPE'] = ''
            reg_string = r"|  INSTALLER: Unknown, \S+\s*|"
        elif var == 'SCENARIO':
            os.environ['DEPLOY_SCENARIO'] = ''
            reg_string = r"|   SCENARIO: Unknown\s*|"
        elif var == 'NODE':
            os.environ['NODE_NAME'] = ''
            reg_string = r"|        POD: Unknown\s*|"
        elif var == 'BUILD_TAG':
            os.environ['BUILD_TAG'] = ''
            reg_string = r"|  BUILD TAG: None|"

        with mock.patch('functest.cli.commands.cli_env.click.echo') \
                as mock_click_echo:
            self.cli_environ.show()
            mock_click_echo.assert_called_with(RegexMatch(reg_string))

    def test_show_ci_installer_type_ko(self, *args):
        self._test_show_missing_env_var('INSTALLER_TYPE', *args)

    def test_show_missing_ci_scenario(self, *args):
        self._test_show_missing_env_var('SCENARIO', *args)

    def test_show_missing_ci_node(self, *args):
        self._test_show_missing_env_var('NODE', *args)

    def test_show_missing_ci_build_tag(self, *args):
        self._test_show_missing_env_var('BUILD_TAG', *args)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
