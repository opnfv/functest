#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0


import logging
import mock
import unittest

from functest.cli.commands import cli_testcase
from functest.utils import functest_constants as ft_constants

class CliTestCasesTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.testname = 'testname'
        with mock.patch('functest.cli.commands.cli_testcase.tb'):
            self.cli_tests = cli_testcase.CliTestcase()

    # TODO: Why is it failing?
    # @mock.patch('functest.cli.commands.cli_testcase.click.echo')
    # def test_show_without_description(self, mock_click_echo):
    #     with mock.patch.object(self.cli_tests.tiers, 'get_test', return_value=None)\
    #         as mock_tb_test:
    #         self.cli_tests.show('testname')
    #         mock_click_echo.assert_called_with("The test case '%s' does not exist \
    #             or is not supported." % 'testname')

    @mock.patch('functest.cli.commands.cli_testcase.vacation.main')
    def test_run_vacation(self, mock_method):
        self.cli_tests.run('vacation')
        self.assertTrue(mock_method.called)

    @mock.patch('functest.cli.commands.cli_testcase.os.path.isfile', return_value=False)
    @mock.patch('functest.cli.commands.cli_testcase.click.echo')
    def test_run_missing_env_file(self, mock_click_echo, mock_os):
        self.cli_tests.run(self.testname)
        mock_click_echo.assert_called_with("Functest environment is not ready. "
                       "Run first 'functest env prepare'")

    @mock.patch('functest.cli.commands.cli_testcase.os.path.isfile', return_value=True)
    @mock.patch('functest.cli.commands.cli_testcase.ft_utils.execute_command')
    def test_run_noclean(self, mock_ft_utils, mock_os):
        cmd = ("python %s/functest/ci/run_tests.py "
                       "-n -t %s" % (ft_constants.FUNCTEST_REPO_DIR, self.testname))
        self.cli_tests.run(self.testname, noclean=True)
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.cli.commands.cli_testcase.os.path.isfile', return_value=True)
    @mock.patch('functest.cli.commands.cli_testcase.ft_utils.execute_command')
    def test_run_without_noclean(self, mock_ft_utils, mock_os):
        cmd = ("python %s/functest/ci/run_tests.py "
                       "-t %s" % (ft_constants.FUNCTEST_REPO_DIR, self.testname))
        self.cli_tests.run(self.testname, noclean=False)
        mock_ft_utils.assert_called_with(cmd)

    @mock.patch('functest.cli.commands.cli_testcase.click.echo')
    def test_list(self, mock_click_echo):
        with mock.patch.object(self.cli_tests.tiers, 'get_tiers', return_value=[]) \
                               as mock_tb_tiers:
                self.cli_tests.list()
                mock_click_echo.assert_called_with("")

if __name__ == "__main__":
    unittest.main(verbosity=2)
