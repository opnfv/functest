#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock

from functest.cli.commands import cli_testcase


class CliTestCasesTesting(unittest.TestCase):

    def setUp(self):
        self.testname = 'testname'
        with mock.patch('functest.ci.tier_builder'):
            self.cli_tests = cli_testcase.CliTestcase()

    @mock.patch('functest.utils.functest_utils.execute_command')
    def test_run_default(self, mock_ft_utils):
        cmd = "run_tests -n -r -t {}".format(self.testname)
        self.cli_tests.run(self.testname, noclean=True, report=True)
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.utils.functest_utils.execute_command')
    def test_run_noclean_missing_report(self, mock_ft_utils):
        cmd = "run_tests -n -t {}".format(self.testname)
        self.cli_tests.run(self.testname, noclean=True, report=False)
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.utils.functest_utils.execute_command')
    def test_run_report_missing_noclean(self, mock_ft_utils):
        cmd = "run_tests -r -t {}".format(self.testname)
        self.cli_tests.run(self.testname, noclean=False, report=True)
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.utils.functest_utils.execute_command')
    def test_run_missing_noclean_report(self, mock_ft_utils):
        cmd = "run_tests -t {}".format(self.testname)
        self.cli_tests.run(self.testname, noclean=False, report=False)
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.cli.commands.cli_testcase.click.echo')
    def test_list(self, mock_click_echo):
        with mock.patch.object(self.cli_tests.tiers, 'get_tiers',
                               return_value=[]):
            self.cli_tests.list()
            mock_click_echo.assert_called_with("")

    @mock.patch('functest.cli.commands.cli_testcase.click.echo')
    def test_show_default_desc_none(self, mock_click_echo):
        with mock.patch.object(self.cli_tests.tiers, 'get_test',
                               return_value=None):
            self.cli_tests.show(self.testname)
            mock_click_echo.assert_any_call("The test case '%s' "
                                            "does not exist or is"
                                            " not supported."
                                            % self.testname)

    @mock.patch('functest.cli.commands.cli_testcase.click.echo')
    def test_show_default(self, mock_click_echo):
        mock_obj = mock.Mock()
        with mock.patch.object(self.cli_tests.tiers, 'get_test',
                               return_value=mock_obj):
            self.cli_tests.show(self.testname)
            mock_click_echo.assert_called_with(mock_obj)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
