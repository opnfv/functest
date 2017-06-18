#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import logging
import pkg_resources
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
        self.openstack_creds = 'test_openstack_creds'
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
    def test_ping_endpoint_missing_auth_url(self, mock_click_echo,
                                            mock_exit):
        with self.assertRaises(Exception):
            self.cli_os.os_auth_url = None
            self.cli_os.ping_endpoint()
            mock_click_echo.assert_called_once_with("Source the OpenStack "
                                                    "credentials first '. "
                                                    "$creds'")

    @mock.patch('functest.cli.commands.cli_os.exit')
    @mock.patch('functest.cli.commands.cli_os.click.echo')
    def test_ping_endpoint_os_system_fails(self, mock_click_echo,
                                           mock_exit):
        self.cli_os.os_auth_url = self.os_auth_url
        self.cli_os.endpoint_ip = self.endpoint_ip
        with mock.patch('functest.cli.commands.cli_os.os.system',
                        return_value=1):
            self.cli_os.ping_endpoint()
            mock_click_echo.assert_called_once_with("Cannot talk to the "
                                                    "endpoint %s\n" %
                                                    self.endpoint_ip)
            mock_exit.assert_called_once_with(0)

    @mock.patch('functest.cli.commands.cli_os.ft_utils.execute_command')
    def test_check(self, mock_ftutils_execute):
        with mock.patch.object(self.cli_os, 'ping_endpoint'):
            self.cli_os.check()
            mock_ftutils_execute.assert_called_once_with(
                "sh %s" % pkg_resources.resource_filename(
                    'functest', 'ci/check_os.sh'), verbose=False)

    @mock.patch('functest.cli.commands.cli_os.os.path.isfile',
                return_value=False)
    @mock.patch('functest.cli.commands.cli_os.click.echo')
    def test_snapshot_create(self, mock_click_echo, mock_os_path):
        with mock.patch.object(self.cli_os, 'ping_endpoint'), \
                mock.patch('functest.cli.commands.cli_os.os_snapshot.main') \
                as mock_os_snapshot:
            self.cli_os.snapshot_create()
            mock_click_echo.assert_called_once_with("Generating Openstack "
                                                    "snapshot...")
            self.assertTrue(mock_os_snapshot.called)

    @mock.patch('functest.cli.commands.cli_os.os.path.isfile',
                return_value=True)
    @mock.patch('functest.cli.commands.cli_os.click.echo')
    def test_snapshot_create_overwrite(self, mock_click_echo, mock_os_path):
        with mock.patch('__builtin__.raw_input', return_value="y") \
                as mock_raw_input, \
                mock.patch.object(self.cli_os, 'ping_endpoint'), \
                mock.patch('functest.cli.commands.cli_os.os_snapshot.main') \
                as mock_os_snapshot:
            self.cli_os.snapshot_create()
            mock_click_echo.assert_called_once_with("Generating Openstack "
                                                    "snapshot...")
            mock_raw_input.assert_any_call("It seems there is already an "
                                           "OpenStack snapshot. Do you want "
                                           "to overwrite it with the current "
                                           "OpenStack status? [y|n]\n")
            self.assertTrue(mock_os_snapshot.called)

    @mock.patch('functest.cli.commands.cli_os.os.path.isfile',
                return_value=False)
    @mock.patch('functest.cli.commands.cli_os.click.echo')
    def test_snapshot_show_missing_snap(self, mock_click_echo, mock_os_path):
        self.cli_os.snapshot_show()
        mock_click_echo.assert_called_once_with("There is no OpenStack "
                                                "snapshot created. To create "
                                                "one run the command "
                                                "'functest openstack "
                                                "snapshot-create'")

    @mock.patch('functest.cli.commands.cli_os.os.path.isfile',
                return_value=True)
    @mock.patch('functest.cli.commands.cli_os.click.echo')
    def test_snapshot_show_default(self, mock_click_echo, mock_os_path):
        with mock.patch('__builtin__.open', mock.mock_open(read_data='0')) \
                as m:
            self.cli_os.snapshot_file = self.snapshot_file
            self.cli_os.snapshot_show()
            m.assert_called_once_with(self.snapshot_file, 'r')
            mock_click_echo.assert_called_once_with("\n0")

    @mock.patch('functest.cli.commands.cli_os.os.path.isfile',
                return_value=True)
    @mock.patch('functest.cli.commands.cli_os.click.echo')
    def test_clean(self, mock_click_echo, mock_os_path):
        with mock.patch.object(self.cli_os, 'ping_endpoint'), \
                mock.patch('functest.cli.commands.cli_os.os_clean.main') \
                as mock_os_clean:
            self.cli_os.clean()
            self.assertTrue(mock_os_clean.called)

    @mock.patch('functest.cli.commands.cli_os.os.path.isfile',
                return_value=False)
    @mock.patch('functest.cli.commands.cli_os.click.echo')
    def test_clean_missing_file(self, mock_click_echo, mock_os_path):
        with mock.patch.object(self.cli_os, 'ping_endpoint'):
            self.cli_os.clean()
            mock_click_echo.assert_called_once_with("Not possible to clean "
                                                    "OpenStack without a "
                                                    "snapshot. This could "
                                                    "cause problems. "
                                                    "Run first the command "
                                                    "'functest openstack "
                                                    "snapshot-create'")

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
