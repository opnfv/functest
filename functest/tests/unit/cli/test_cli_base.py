#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock
from click.testing import CliRunner

with mock.patch('functest.cli.commands.cli_testcase.CliTestcase.__init__',
                mock.Mock(return_value=None)), \
    mock.patch('functest.cli.commands.cli_tier.CliTier.__init__',
               mock.Mock(return_value=None)):
    from functest.cli import cli_base


class CliBaseTesting(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self._openstack = cli_base._openstack
        self._env = cli_base._env
        self._testcase = cli_base._testcase
        self._tier = cli_base._tier

    def test_os_check(self):
        with mock.patch.object(self._openstack, 'check') as mock_method:
            result = self.runner.invoke(cli_base.os_check)
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(mock_method.called)

    def test_os_show_credentials(self):
        with mock.patch.object(self._openstack, 'show_credentials') \
                as mock_method:
            result = self.runner.invoke(cli_base.os_show_credentials)
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(mock_method.called)

    def test_env_show(self):
        with mock.patch.object(self._env, 'show') as mock_method:
            result = self.runner.invoke(cli_base.env_show)
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(mock_method.called)

    def test_testcase_list(self):
        with mock.patch.object(self._testcase, 'list') as mock_method:
            result = self.runner.invoke(cli_base.testcase_list)
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(mock_method.called)

    def test_testcase_show(self):
        with mock.patch.object(self._testcase, 'show') as mock_method:
            result = self.runner.invoke(cli_base.testcase_show, ['testname'])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(mock_method.called)

    def test_testcase_run(self):
        with mock.patch.object(self._testcase, 'run') as mock_method:
            result = self.runner.invoke(cli_base.testcase_run,
                                        ['testname', '--noclean'])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(mock_method.called)

    def test_tier_list(self):
        with mock.patch.object(self._tier, 'list') as mock_method:
            result = self.runner.invoke(cli_base.tier_list)
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(mock_method.called)

    def test_tier_show(self):
        with mock.patch.object(self._tier, 'show') as mock_method:
            result = self.runner.invoke(cli_base.tier_show, ['tiername'])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(mock_method.called)

    def test_tier_gettests(self):
        with mock.patch.object(self._tier, 'gettests') as mock_method:
            result = self.runner.invoke(cli_base.tier_gettests, ['tiername'])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(mock_method.called)

    def test_tier_run(self):
        with mock.patch.object(self._tier, 'run') as mock_method:
            result = self.runner.invoke(cli_base.tier_run,
                                        ['tiername', '--noclean'])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(mock_method.called)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
