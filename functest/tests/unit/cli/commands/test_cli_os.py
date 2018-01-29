#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest
import os

import mock

from functest.cli.commands import cli_os


class CliOpenStackTesting(unittest.TestCase):

    def setUp(self):
        self.endpoint_ip = 'test_ip'
        self.os_auth_url = 'http://test_ip:test_port/v2.0'
        self.installer_type = 'test_installer_type'
        self.installer_ip = 'test_installer_ip'
        self.openstack_creds = 'test_env_file'
        self.snapshot_file = 'test_snapshot_file'
        self.cli_os = cli_os.CliOpenStack()

    def test_ping_endpoint_default(self):
        self.cli_os.os_auth_url = self.os_auth_url
        self.cli_os.endpoint_ip = self.endpoint_ip
        with mock.patch('functest.cli.commands.cli_os.os.system',
                        return_value=0):
            self.assertEqual(self.cli_os.ping_endpoint(), 0)

    @mock.patch('functest.cli.commands.cli_os.exit', side_effect=Exception)
    @mock.patch('functest.cli.commands.cli_os.click.echo')
    def test_ping_endpoint_auth_url_ko(self, mock_click_echo, mock_exit):
        with self.assertRaises(Exception):
            self.cli_os.os_auth_url = None
            self.cli_os.ping_endpoint()
        mock_click_echo.assert_called_once_with(
            "Source the OpenStack credentials first '. $creds'")
        mock_exit.assert_called_once_with(0)

    @mock.patch('functest.cli.commands.cli_os.exit')
    @mock.patch('functest.cli.commands.cli_os.click.echo')
    def test_ping_endpoint_system_fails(self, mock_click_echo, mock_exit):
        self.cli_os.os_auth_url = self.os_auth_url
        self.cli_os.endpoint_ip = self.endpoint_ip
        with mock.patch('functest.cli.commands.cli_os.os.system',
                        return_value=1):
            self.cli_os.ping_endpoint()
            mock_click_echo.assert_called_once_with(
                "Cannot talk to the endpoint %s\n" % self.endpoint_ip)
            mock_exit.assert_called_once_with(0)

    def test_check(self):
        with mock.patch.object(self.cli_os, 'ping_endpoint'), \
            mock.patch('functest.cli.commands.cli_os.check_deployment.'
                       'CheckDeployment') as mock_check_deployment:
            self.cli_os.check()
            self.assertTrue(mock_check_deployment.called)

    @mock.patch('functest.cli.commands.cli_os.click.echo')
    def test_show_credentials(self, mock_click_echo):
        key = 'OS_KEY'
        value = 'OS_VALUE'
        with mock.patch.dict(os.environ, {key: value}):
            self.cli_os.show_credentials()
            mock_click_echo.assert_any_call("{}={}".format(key, value))


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
