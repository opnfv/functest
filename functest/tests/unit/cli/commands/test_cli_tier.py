#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0


import logging
import mock
import unittest

from functest.cli.commands import cli_tier
from functest.utils import functest_constants as ft_constants


class CliTierTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.tiername = 'tiername'
        with mock.patch('functest.cli.commands.cli_tier.tb'):
            self.cli_tier = cli_tier.CliTier()

    @mock.patch('functest.cli.commands.cli_tier.click.echo')
    def test_list(self, mock_click_echo):
        with mock.patch.object(self.cli_tier.tiers, 'get_tiers',
                               return_value=[]):
            self.cli_tier.list()
            mock_click_echo.assert_called_with("")

    @mock.patch('functest.cli.commands.cli_tier.click.echo')
    def test_show_missing_tier(self, mock_click_echo):
        with mock.patch.object(self.cli_tier.tiers, 'get_tier',
                               return_value=None):
            self.cli_tier.show(self.tiername)
            tier_names = self.cli_tier.tiers.get_tier_names()
            mock_click_echo.assert_called_with("The tier with name '%s' does "
                                               "not exist. Available tiers are"
                                               ":\n  %s\n" % (self.tiername,
                                                              tier_names))

    @mock.patch('functest.cli.commands.cli_tier.click.echo')
    def test_gettests_missing_tier(self, mock_click_echo):
        with mock.patch.object(self.cli_tier.tiers, 'get_tier',
                               return_value=None):
            self.cli_tier.show(self.tiername)
            tier_names = self.cli_tier.tiers.get_tier_names()
            mock_click_echo.assert_called_with("The tier with name '%s' does"
                                               " not exist. Available tiers "
                                               "are:\n  %s\n" % (self.tiername,
                                                                 tier_names))

    @mock.patch('functest.cli.commands.cli_tier.os.path.isfile',
                return_value=False)
    @mock.patch('functest.cli.commands.cli_tier.click.echo')
    def test_run_missing_env_file(self, mock_click_echo, mock_os):
        self.cli_tier.run(self.tiername)
        mock_click_echo.assert_called_with("Functest environment is not ready."
                                           " Run first 'functest env prepare'")

    @mock.patch('functest.cli.commands.cli_tier.os.path.isfile',
                return_value=True)
    @mock.patch('functest.cli.commands.cli_tier.ft_utils.execute_command')
    def test_run_noclean(self, mock_ft_utils, mock_os):
        cmd = ("python %s/functest/ci/run_tests.py "
               "-n -t %s" % (ft_constants.FUNCTEST_REPO_DIR, self.tiername))
        self.cli_tier.run(self.tiername, noclean=True)
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.cli.commands.cli_tier.os.path.isfile',
                return_value=True)
    @mock.patch('functest.cli.commands.cli_tier.ft_utils.execute_command')
    def test_run_without_noclean(self, mock_ft_utils, mock_os):
        cmd = ("python %s/functest/ci/run_tests.py "
               "-t %s" % (ft_constants.FUNCTEST_REPO_DIR, self.tiername))
        self.cli_tier.run(self.tiername, noclean=False)
        mock_ft_utils.assert_called_with(cmd)


if __name__ == "__main__":
    unittest.main(verbosity=2)
