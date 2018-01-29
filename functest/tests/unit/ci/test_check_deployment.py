#!/usr/bin/env python

# Copyright (c) 2017 Ericsson and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import socket
import unittest

import logging
import mock

from functest.ci import check_deployment

__author__ = "Jose Lausuch <jose.lausuch@ericsson.com>"


class CheckDeploymentTesting(unittest.TestCase):
    """The super class which testing classes could inherit."""
    # pylint: disable=missing-docstring,too-many-public-methods

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.client_test = mock.Mock()
        self.deployment = check_deployment.CheckDeployment()
        self.service_test = 'compute'
        self.rc_file = self.deployment.rc_file
        self.endpoint_test = 'http://192.168.0.6:5000/v3'
        creds_attr = {'auth_url': self.endpoint_test,
                      'proxy_settings': ''}
        proxy_attr = {'host': '192.168.0.1', 'port': '5000'}
        proxy_settings = mock.Mock()
        proxy_settings.configure_mock(**proxy_attr)
        self.os_creds = mock.Mock()
        self.os_creds.configure_mock(**creds_attr)
        self.os_creds.proxy_settings = proxy_settings
        self.deployment.os_creds = self.os_creds

    @mock.patch('socket.socket.connect', side_effect=TypeError)
    def test_verify_connectivity_ko1(self, *args):
        self.assertFalse(check_deployment.verify_connectivity("127.0.0.1"))
        args[0].assert_called_once_with((None, 80))

    @mock.patch('socket.socket.connect', side_effect=socket.error)
    def test_verify_connectivity_ko2(self, *args):
        self.assertFalse(
            check_deployment.verify_connectivity("http://127.0.0.1"))
        args[0].assert_called_once_with(("127.0.0.1", 80))

    @mock.patch('socket.socket.connect', side_effect=socket.error)
    def test_verify_connectivity_ko3(self, *args):
        self.assertFalse(
            check_deployment.verify_connectivity("https://127.0.0.1"))
        args[0].assert_called_once_with(("127.0.0.1", 443))

    @mock.patch('socket.socket.connect')
    def test_verify_connectivity(self, *args):
        self.assertTrue(
            check_deployment.verify_connectivity("https://127.0.0.1"))
        args[0].assert_called_once_with(("127.0.0.1", 443))

    @mock.patch('snaps.openstack.utils.keystone_utils.keystone_session',
                return_value=mock.Mock(
                    get_token=mock.Mock(side_effect=Exception)))
    def test_get_auth_token_ko(self, *args):
        with self.assertRaises(Exception):
            check_deployment.get_auth_token(self.os_creds)
        args[0].assert_called_once_with(self.os_creds)

    @mock.patch('snaps.openstack.utils.keystone_utils.keystone_session',
                return_value=mock.Mock(
                    get_token=mock.Mock(return_value="foo")))
    def test_get_auth_token(self, *args):
        self.assertEqual(check_deployment.get_auth_token(self.os_creds), "foo")
        args[0].assert_called_once_with(self.os_creds)

    @mock.patch('six.moves.builtins.open',
                mock.mock_open(read_data='OS_AUTH_URL'))
    @mock.patch('functest.ci.check_deployment.os.path.isfile', returns=True)
    def test_check_rc(self, *args):
        self.deployment.check_rc()
        args[0].assert_called_once_with(self.rc_file)

    @mock.patch('functest.ci.check_deployment.os.path.isfile',
                return_value=False)
    def test_check_rc_missing_file(self, *args):
        with self.assertRaises(Exception) as context:
            self.deployment.check_rc()
        args[0].assert_called_once_with(self.rc_file)
        msg = 'RC file {} does not exist!'.format(self.rc_file)
        self.assertTrue(msg in str(context.exception))

    @mock.patch('six.moves.builtins.open',
                mock.mock_open(read_data='test'))
    @mock.patch('functest.ci.check_deployment.os.path.isfile',
                return_value=True)
    def test_check_rc_missing_os_auth(self, *args):
        with self.assertRaises(Exception) as context:
            self.deployment.check_rc()
        args[0].assert_called_once_with(self.rc_file)
        msg = 'OS_AUTH_URL not defined in {}.'.format(self.rc_file)
        self.assertTrue(msg in str(context.exception))

    @mock.patch('functest.ci.check_deployment.get_auth_token',
                return_value='gAAAAABaOhXGS')
    @mock.patch('functest.ci.check_deployment.verify_connectivity',
                return_value=True)
    def test_check_auth_endpoint(self, *args):
        self.deployment.check_auth_endpoint()
        args[0].assert_called_once_with(self.endpoint_test)
        args[1].assert_called_once_with(mock.ANY)

    @mock.patch('functest.ci.check_deployment.verify_connectivity',
                return_value=False)
    def test_check_auth_endpoint_ko(self, *args):
        with self.assertRaises(Exception) as context:
            self.deployment.check_auth_endpoint()
        msg = "OS_AUTH_URL {} is not reachable.".format(self.os_creds.auth_url)
        args[0].assert_called_once_with(self.os_creds.auth_url)
        self.assertTrue(msg in str(context.exception))

    @mock.patch('functest.ci.check_deployment.verify_connectivity',
                return_value=True)
    @mock.patch('functest.ci.check_deployment.keystone_utils.get_endpoint')
    def test_check_public_endpoint(self, *args):
        args[0].return_value = self.endpoint_test
        self.deployment.check_public_endpoint()
        args[0].assert_called_once_with(
            mock.ANY, 'identity', interface='public')
        args[1].assert_called_once_with(self.endpoint_test)

    @mock.patch('functest.ci.check_deployment.verify_connectivity',
                return_value=False)
    @mock.patch('functest.ci.check_deployment.keystone_utils.get_endpoint')
    def test_check_public_endpoint_ko(self, *args):
        args[0].return_value = self.endpoint_test
        with self.assertRaises(Exception) as context:
            self.deployment.check_public_endpoint()
        args[0].assert_called_once_with(
            mock.ANY, 'identity', interface='public')
        args[1].assert_called_once_with(self.endpoint_test)
        msg = "Public endpoint {} is not reachable.".format(self.endpoint_test)
        self.assertTrue(msg in str(context.exception))

    @mock.patch('functest.ci.check_deployment.verify_connectivity',
                return_value=True)
    @mock.patch('functest.ci.check_deployment.keystone_utils.get_endpoint')
    def test_check_service_endpoint(self, *args):
        self.deployment.check_service_endpoint(self.service_test)
        args[0].assert_called_once_with(
            mock.ANY, self.service_test, interface='public')
        args[1].assert_called_once_with(args[0].return_value)

    @mock.patch('functest.ci.check_deployment.verify_connectivity',
                return_value=False)
    @mock.patch('functest.ci.check_deployment.keystone_utils.get_endpoint')
    def test_check_service_endpoint_ko(self, *args):
        args[0].return_value = self.endpoint_test
        with self.assertRaises(Exception) as context:
            self.deployment.check_service_endpoint(self.service_test)
        msg = "{} endpoint {} is not reachable.".format(
            self.service_test, self.endpoint_test)
        self.assertTrue(msg in str(context.exception))
        args[0].assert_called_once_with(
            mock.ANY, self.service_test, interface='public')
        args[1].assert_called_once_with(args[0].return_value)

    @mock.patch('functest.ci.check_deployment.nova_utils.nova_client')
    def test_check_nova(self, mock_method):
        self.deployment.check_nova()
        mock_method.assert_called_once_with(mock.ANY)

    @mock.patch('functest.ci.check_deployment.nova_utils.nova_client',
                return_value=mock.Mock(
                    servers=mock.Mock(list=mock.Mock(side_effect=Exception))))
    def test_check_nova_fail(self, mock_method):
        with self.assertRaises(Exception):
            self.deployment.check_nova()
        mock_method.assert_called_once_with(mock.ANY)

    @mock.patch('functest.ci.check_deployment.neutron_utils.neutron_client')
    def test_check_neutron(self, mock_method):
        self.deployment.check_neutron()
        mock_method.assert_called_once_with(mock.ANY)

    @mock.patch('functest.ci.check_deployment.neutron_utils.neutron_client',
                return_value=mock.Mock(
                    list_networks=mock.Mock(side_effect=Exception)))
    def test_check_neutron_fail(self, mock_method):
        with self.assertRaises(Exception):
            self.deployment.check_neutron()
        mock_method.assert_called_once_with(mock.ANY)

    @mock.patch('functest.ci.check_deployment.glance_utils.glance_client')
    def test_check_glance(self, mock_method):
        self.deployment.check_glance()
        mock_method.assert_called_once_with(mock.ANY)

    @mock.patch('functest.ci.check_deployment.glance_utils.glance_client',
                return_value=mock.Mock(
                    images=mock.Mock(list=mock.Mock(side_effect=Exception))))
    def test_check_glance_fail(self, mock_method):
        with self.assertRaises(Exception):
            self.deployment.check_glance()
        mock_method.assert_called_once_with(mock.ANY)

    @mock.patch('functest.ci.check_deployment.LOGGER.info')
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name', return_value='ext-net')
    def test_check_extnet(self, *args):
        self.deployment.check_ext_net()
        args[0].assert_called_once_with(mock.ANY)
        args[1].assert_called_once_with(
            "External network found: %s", "ext-net")

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name', return_value='')
    def test_check_extnet_none(self, mock_getext):
        with self.assertRaises(Exception) as context:
            self.deployment.check_ext_net()
        self.assertTrue(mock_getext.called)
        msg = 'ERROR: No external networks in the deployment.'
        self.assertTrue(msg in str(context.exception))

    @mock.patch('functest.ci.check_deployment.CheckDeployment.check_rc',
                side_effect=Exception)
    def test_check_all_exc1(self, *args):
        with self.assertRaises(Exception):
            self.deployment.check_all()
        args[0].assert_called_once_with()

    @mock.patch('snaps.openstack.tests.openstack_tests.get_credentials',
                side_effect=Exception)
    @mock.patch('functest.ci.check_deployment.CheckDeployment.check_rc')
    def test_check_all_exc2(self, *args):
        with self.assertRaises(Exception):
            self.deployment.check_all()
        args[0].assert_called_once_with()
        args[1].assert_called_once_with(
            os_env_file=self.rc_file, proxy_settings_str=None,
            ssh_proxy_cmd=None)

    @mock.patch('snaps.openstack.tests.openstack_tests.get_credentials',
                return_value=None)
    @mock.patch('functest.ci.check_deployment.CheckDeployment.check_rc')
    def test_check_all_exc3(self, *args):
        with self.assertRaises(Exception):
            self.deployment.check_all()
        args[0].assert_called_once_with()
        args[1].assert_called_once_with(
            os_env_file=self.rc_file, proxy_settings_str=None,
            ssh_proxy_cmd=None)

    @mock.patch('functest.ci.check_deployment.CheckDeployment.check_ext_net')
    @mock.patch('functest.ci.check_deployment.CheckDeployment.check_glance')
    @mock.patch('functest.ci.check_deployment.CheckDeployment.check_neutron')
    @mock.patch('functest.ci.check_deployment.CheckDeployment.check_nova')
    @mock.patch(
        'functest.ci.check_deployment.CheckDeployment.check_service_endpoint')
    @mock.patch(
        'functest.ci.check_deployment.CheckDeployment.check_public_endpoint')
    @mock.patch(
        'functest.ci.check_deployment.CheckDeployment.check_auth_endpoint')
    @mock.patch('snaps.openstack.tests.openstack_tests.get_credentials')
    @mock.patch('functest.ci.check_deployment.CheckDeployment.check_rc')
    def test_check_all(self, *args):
        self.assertEqual(self.deployment.check_all(), 0)
        for i in [0, 2, 3, 5, 6, 7, 8]:
            args[i].assert_called_once_with()
        args[1].assert_called_once_with(
            os_env_file=self.rc_file, proxy_settings_str=None,
            ssh_proxy_cmd=None)
        calls = [mock.call('compute'), mock.call('network'),
                 mock.call('image')]
        args[4].assert_has_calls(calls)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
