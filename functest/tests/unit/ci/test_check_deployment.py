#!/usr/bin/env python

# Copyright (c) 2017 Ericsson and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest

from functest.ci import check_deployment

__author__ = "Jose Lausuch <jose.lausuch@ericsson.com>"


class CheckDeploymentTesting(unittest.TestCase):
    """The super class which testing classes could inherit."""
    # pylint: disable=missing-docstring

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

    def test_check_rc(self):
        with mock.patch('functest.ci.check_deployment.os.path.isfile',
                        returns=True) as m, \
                mock.patch('__builtin__.open',
                           mock.mock_open(read_data='OS_AUTH_URL')):
            self.deployment.check_rc()
            self.assertTrue(m.called)

    def test_check_rc_missing_file(self):
        with mock.patch('functest.ci.check_deployment.os.path.isfile',
                        return_value=False), \
                self.assertRaises(Exception) as context:
            msg = 'RC file {} does not exist!'.format(self.rc_file)
            self.deployment.check_rc(self.rc_file)
            self.assertTrue(msg in context)

    def test_check_rc_missing_os_auth(self):
        with mock.patch('__builtin__.open',
                        mock.mock_open(read_data='test')), \
                self.assertRaises(Exception) as context:
            msg = 'OS_AUTH_URL not defined in {}.'.format(self.rc_file)
            self.assertTrue(msg in context)

    def test_check_auth_endpoint(self):
        with mock.patch('functest.ci.check_deployment.verify_connectivity',
                        return_value=True) as m:
            self.deployment.check_auth_endpoint()
            self.assertTrue(m.called)

    def test_check_auth_endpoint_not_reachable(self):
        with mock.patch('functest.ci.check_deployment.verify_connectivity',
                        return_value=False) as m, \
                self.assertRaises(Exception) as context:
            endpoint = self.os_creds.auth_url
            self.deployment.check_auth_endpoint()
            msg = "OS_AUTH_URL {} is not reachable.".format(endpoint)
            self.assertTrue(m.called)
            self.assertTrue(msg in context)

    def test_check_public_endpoint(self):
        with mock.patch('functest.ci.check_deployment.verify_connectivity',
                        return_value=True) as m, \
                mock.patch('functest.ci.check_deployment.keystone_utils.'
                           'get_endpoint') as n:
            self.deployment.check_public_endpoint()
            self.assertTrue(m.called)
            self.assertTrue(n.called)

    def test_check_public_endpoint_not_reachable(self):
        with mock.patch('functest.ci.check_deployment.verify_connectivity',
                        return_value=False) as m, \
                mock.patch('functest.ci.check_deployment.keystone_utils.'
                           'get_endpoint',
                           return_value=self.endpoint_test) as n, \
                self.assertRaises(Exception) as context:
            self.deployment.check_public_endpoint()
            msg = ("Public endpoint {} is not reachable."
                   .format(self.mock_endpoint))
            self.assertTrue(m.called)
            self.assertTrue(n.called)
            self.assertTrue(msg in context)

    def test_check_service_endpoint(self):
        with mock.patch('functest.ci.check_deployment.verify_connectivity',
                        return_value=True) as m, \
                mock.patch('functest.ci.check_deployment.keystone_utils.'
                           'get_endpoint') as n:
            self.deployment.check_service_endpoint(self.service_test)
            self.assertTrue(m.called)
            self.assertTrue(n.called)

    def test_check_service_endpoint_not_reachable(self):
        with mock.patch('functest.ci.check_deployment.verify_connectivity',
                        return_value=False) as m, \
                mock.patch('functest.ci.check_deployment.keystone_utils.'
                           'get_endpoint',
                           return_value=self.endpoint_test) as n, \
                self.assertRaises(Exception) as context:
            self.deployment.check_service_endpoint(self.service_test)
            msg = "{} endpoint {} is not reachable.".format(self.service_test,
                                                            self.endpoint_test)
            self.assertTrue(m.called)
            self.assertTrue(n.called)
            self.assertTrue(msg in context)

    def test_check_nova(self):
        with mock.patch('functest.ci.check_deployment.nova_utils.nova_client',
                        return_value=self.client_test) as m:
            self.deployment.check_nova()
            self.assertTrue(m.called)

    def test_check_nova_fail(self):
        with mock.patch('functest.ci.check_deployment.nova_utils.nova_client',
                        return_value=self.client_test) as m, \
                mock.patch.object(self.client_test, 'servers.list',
                                  side_effect=Exception):
            self.deployment.check_nova()
            self.assertTrue(m.called)
            self.assertRaises(Exception)

    def test_check_neutron(self):
        with mock.patch('functest.ci.check_deployment.neutron_utils.'
                        'neutron_client', return_value=self.client_test) as m:
            self.deployment.check_neutron()
            self.assertTrue(m.called)

    def test_check_neutron_fail(self):
        with mock.patch('functest.ci.check_deployment.neutron_utils.'
                        'neutron_client',
                        return_value=self.client_test) as m, \
                mock.patch.object(self.client_test, 'list_networks',
                                  side_effect=Exception), \
                self.assertRaises(Exception):
            self.deployment.check_neutron()
            self.assertRaises(Exception)
            self.assertTrue(m.called)

    def test_check_glance(self):
        with mock.patch('functest.ci.check_deployment.glance_utils.'
                        'glance_client', return_value=self.client_test) as m:
            self.deployment.check_glance()
            self.assertTrue(m.called)

    def test_check_glance_fail(self):
        with mock.patch('functest.ci.check_deployment.glance_utils.'
                        'glance_client', return_value=self.client_test) as m, \
                mock.patch.object(self.client_test, 'images.list',
                                  side_effect=Exception):
            self.deployment.check_glance()
            self.assertRaises(Exception)
            self.assertTrue(m.called)

    @mock.patch('functest.ci.check_deployment.LOGGER.info')
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name')
    def test_check_extnet(self, mock_getext, mock_loginfo):
        test_network = 'ext-net'
        mock_getext.return_value = test_network
        self.deployment.check_ext_net()
        self.assertTrue(mock_getext.called)
        mock_loginfo.assert_called_once_with(
            "External network found: %s", test_network)

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name', return_value='')
    def test_check_extnet_None(self, mock_getext):
        with self.assertRaises(Exception) as context:
            self.deployment.check_ext_net()
            self.assertTrue(mock_getext.called)
            msg = 'ERROR: No external networks in the deployment.'
            self.assertTrue(msg in context)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
