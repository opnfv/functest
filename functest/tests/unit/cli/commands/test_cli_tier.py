#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0


import logging
import unittest

import mock

from functest.cli.commands import cli_tier


class CliTierTesting(unittest.TestCase):

    def setUp(self):
        self.tiername = 'tiername'
        self.testnames = 'testnames'
        with mock.patch('functest.cli.commands.cli_tier.tb'):
            self.cli_tier = cli_tier.CliTier()

    @mock.patch('functest.cli.commands.cli_tier.click.echo')
    def test_list(self, mock_click_echo):
        with mock.patch.object(self.cli_tier.tiers, 'get_tiers',
                               return_value=[]):
            self.cli_tier.list()
            mock_click_echo.assert_called_with("")

    @mock.patch('functest.cli.commands.cli_tier.click.echo')
    def test_show_default(self, mock_click_echo):
        with mock.patch.object(self.cli_tier.tiers, 'get_tier',
                               return_value=self.tiername):
            self.cli_tier.show(self.tiername)
            mock_click_echo.assert_called_with(self.tiername)

    @mock.patch('functest.cli.commands.cli_tier.click.echo')
    def test_show_missing_tier(self, mock_click_echo):
        with mock.patch.object(self.cli_tier.tiers, 'get_tier',
                               return_value=None), \
            mock.patch.object(self.cli_tier.tiers, 'get_tier_names',
                              return_value='tiernames'):
            self.cli_tier.show(self.tiername)
            mock_click_echo.assert_called_with("The tier with name '%s' does "
                                               "not exist. Available tiers are"
                                               ":\n  %s\n" % (self.tiername,
                                                              'tiernames'))

    @mock.patch('functest.cli.commands.cli_tier.click.echo')
    def test_gettests_default(self, mock_click_echo):
        mock_obj = mock.Mock()
        attrs = {'get_test_names.return_value': self.testnames}
        mock_obj.configure_mock(**attrs)

        with mock.patch.object(self.cli_tier.tiers, 'get_tier',
                               return_value=mock_obj):
            self.cli_tier.gettests(self.tiername)
            mock_click_echo.assert_called_with("Test cases in tier "
                                               "'%s':\n %s\n" % (self.tiername,
                                                                 self.testnames
                                                                 ))

    @mock.patch('functest.cli.commands.cli_tier.click.echo')
    def test_gettests_missing_tier(self, mock_click_echo):
        with mock.patch.object(self.cli_tier.tiers, 'get_tier',
                               return_value=None), \
            mock.patch.object(self.cli_tier.tiers, 'get_tier_names',
                              return_value='tiernames'):
            self.cli_tier.gettests(self.tiername)
            mock_click_echo.assert_called_with("The tier with name '%s' does "
                                               "not exist. Available tiers are"
                                               ":\n  %s\n" % (self.tiername,
                                                              'tiernames'))

    @mock.patch('functest.cli.commands.cli_tier.os.path.isfile',
                return_value=True)
    @mock.patch('functest.cli.commands.cli_tier.ft_utils.execute_command')
    def test_run_default(self, mock_ft_utils, mock_os):
        cmd = "run_tests -n -r -t {}".format(self.tiername)
        self.cli_tier.run(self.tiername, noclean=True, report=True)
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.cli.commands.cli_tier.os.path.isfile',
                return_value=True)
    @mock.patch('functest.cli.commands.cli_tier.ft_utils.execute_command')
    def test_run_report_missing_noclean(self, mock_ft_utils, mock_os):
        cmd = "run_tests -r -t {}".format(self.tiername)
        self.cli_tier.run(self.tiername, noclean=False, report=True)
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.cli.commands.cli_tier.os.path.isfile',
                return_value=True)
    @mock.patch('functest.cli.commands.cli_tier.ft_utils.execute_command')
    def test_run_noclean_missing_report(self, mock_ft_utils, mock_os):
        cmd = "run_tests -n -t {}".format(self.tiername)
        self.cli_tier.run(self.tiername, noclean=True, report=False)
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.cli.commands.cli_tier.os.path.isfile',
                return_value=True)
    @mock.patch('functest.cli.commands.cli_tier.ft_utils.execute_command')
    def test_run_missing_noclean_report(self, mock_ft_utils, mock_os):
        cmd = "run_tests -t {}".format(self.tiername)
        self.cli_tier.run(self.tiername, noclean=False, report=False)
        mock_ft_utils.assert_called_with(cmd)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
