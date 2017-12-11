#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest

from functest.utils import openstack_snapshot


class OSSnapshotTesting(unittest.TestCase):

    def _get_instance(self, key):
        mock_obj = mock.Mock()
        attrs = {'id': 'id' + str(key), 'name': 'name' + str(key),
                 'ip': 'ip' + str(key)}
        mock_obj.configure_mock(**attrs)
        return mock_obj

    def setUp(self):
        self.client = mock.Mock()
        self.test_list = [self._get_instance(1), self._get_instance(2)]
        self.update_list = {'id1': 'name1', 'id2': 'name2'}
        self.update_floatingips = {'id1': 'ip1', 'id2': 'ip2'}
        self.floatingips_list = [{'id': 'id1', 'floating_ip_address': 'ip1'},
                                 {'id': 'id2', 'floating_ip_address': 'ip2'}]
        self.test_dict_list = [{'id': 'id1', 'name': 'name1', 'ip': 'ip1'},
                               {'id': 'id2', 'name': 'name2', 'ip': 'ip2'}]

    @mock.patch('functest.utils.openstack_snapshot.logger.info')
    def test_separator(self, mock_logger_info):
        openstack_snapshot.separator()
        mock_logger_info.assert_called_once_with("-----------------"
                                                 "-----------------"
                                                 "---------")

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_instances(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_instances', return_value=self.test_list):
            resp = openstack_snapshot.get_instances(self.client)
            mock_logger_debug.assert_called_once_with("Getting instances...")
            self.assertDictEqual(resp, {'instances': self.update_list})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_instances_missing_instances(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_instances', return_value=[]):
            resp = openstack_snapshot.get_instances(self.client)
            mock_logger_debug.assert_called_once_with("Getting instances...")
            self.assertDictEqual(resp, {'instances': {}})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_images(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_images', return_value=self.test_list):
            resp = openstack_snapshot.get_images(self.client)
            mock_logger_debug.assert_called_once_with("Getting images...")
            self.assertDictEqual(resp, {'images': self.update_list})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_images_missing_images(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_images', return_value=[]):
            resp = openstack_snapshot.get_images(self.client)
            mock_logger_debug.assert_called_once_with("Getting images...")
            self.assertDictEqual(resp, {'images': {}})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_volumes(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_volumes', return_value=self.test_list):
            resp = openstack_snapshot.get_volumes(self.client)
            mock_logger_debug.assert_called_once_with("Getting volumes...")
            self.assertDictEqual(resp, {'volumes': self.update_list})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_volumes_missing_volumes(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_volumes', return_value=[]):
            resp = openstack_snapshot.get_volumes(self.client)
            mock_logger_debug.assert_called_once_with("Getting volumes...")
            self.assertDictEqual(resp, {'volumes': {}})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_networks(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_network_list', return_value=self.test_dict_list):
            resp = openstack_snapshot.get_networks(self.client)
            mock_logger_debug.assert_called_once_with("Getting networks")
            self.assertDictEqual(resp, {'networks': self.update_list})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_networks_missing_networks(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_network_list', return_value=[]):
            resp = openstack_snapshot.get_networks(self.client)
            mock_logger_debug.assert_called_once_with("Getting networks")
            self.assertDictEqual(resp, {'networks': {}})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_routers(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_router_list', return_value=self.test_dict_list):
            resp = openstack_snapshot.get_routers(self.client)
            mock_logger_debug.assert_called_once_with("Getting routers")
            self.assertDictEqual(resp, {'routers': self.update_list})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_routers_missing_routers(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_router_list', return_value=[]):
            resp = openstack_snapshot.get_routers(self.client)
            mock_logger_debug.assert_called_once_with("Getting routers")
            self.assertDictEqual(resp, {'routers': {}})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_secgroups(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_security_groups',
                        return_value=self.test_dict_list):
            resp = openstack_snapshot.get_security_groups(self.client)
            mock_logger_debug.assert_called_once_with("Getting Security "
                                                      "groups...")
            self.assertDictEqual(resp, {'secgroups': self.update_list})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_secgroups_missing_secgroups(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_security_groups', return_value=[]):
            resp = openstack_snapshot.get_security_groups(self.client)
            mock_logger_debug.assert_called_once_with("Getting Security "
                                                      "groups...")
            self.assertDictEqual(resp, {'secgroups': {}})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_floatingips(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_floating_ips',
                        return_value=self.floatingips_list):
            resp = openstack_snapshot.get_floatingips(self.client)
            mock_logger_debug.assert_called_once_with("Getting Floating "
                                                      "IPs...")
            self.assertDictEqual(resp, {'floatingips':
                                        self.update_floatingips})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_floatingips_missing_floatingips(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_floating_ips', return_value=[]):
            resp = openstack_snapshot.get_floatingips(self.client)
            mock_logger_debug.assert_called_once_with("Getting Floating "
                                                      "IPs...")
            self.assertDictEqual(resp, {'floatingips': {}})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_users(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_users', return_value=self.test_list):
            resp = openstack_snapshot.get_users(self.client)
            mock_logger_debug.assert_called_once_with("Getting users...")
            self.assertDictEqual(resp, {'users': self.update_list})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_users_missing_users(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_users', return_value=[]):
            resp = openstack_snapshot.get_users(self.client)
            mock_logger_debug.assert_called_once_with("Getting users...")
            self.assertDictEqual(resp, {'users': {}})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_tenants(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_tenants', return_value=self.test_list):
            resp = openstack_snapshot.get_tenants(self.client)
            mock_logger_debug.assert_called_once_with("Getting tenants...")
            self.assertDictEqual(resp, {'tenants': self.update_list})

    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_get_tenants_missing_tenants(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_snapshot.os_utils'
                        '.get_tenants', return_value=[]):
            resp = openstack_snapshot.get_tenants(self.client)
            mock_logger_debug.assert_called_once_with("Getting tenants...")
            self.assertDictEqual(resp, {'tenants': {}})

    @mock.patch('functest.utils.openstack_clean.os_utils.get_glance_client')
    @mock.patch('functest.utils.openstack_snapshot.os_utils.get_cinder_client')
    @mock.patch('functest.utils.openstack_snapshot.os_utils'
                '.get_keystone_client')
    @mock.patch('functest.utils.openstack_snapshot.os_utils'
                '.get_neutron_client')
    @mock.patch('functest.utils.openstack_snapshot.os_utils.get_nova_client')
    @mock.patch('functest.utils.openstack_snapshot.os_utils.check_credentials')
    @mock.patch('functest.utils.openstack_snapshot.logger.info')
    @mock.patch('functest.utils.openstack_snapshot.logger.debug')
    def test_main_default(self, mock_logger_debug, mock_logger_info,
                          mock_creds, mock_nova, mock_neutron,
                          mock_keystone, mock_cinder, mock_glance):
        with mock.patch('functest.utils.openstack_snapshot.get_instances',
                        return_value=self.update_list), \
            mock.patch('functest.utils.openstack_snapshot.get_images',
                       return_value=self.update_list), \
            mock.patch('functest.utils.openstack_snapshot.get_images',
                       return_value=self.update_list), \
            mock.patch('functest.utils.openstack_snapshot.get_volumes',
                       return_value=self.update_list), \
            mock.patch('functest.utils.openstack_snapshot.get_networks',
                       return_value=self.update_list), \
            mock.patch('functest.utils.openstack_snapshot.get_routers',
                       return_value=self.update_list), \
            mock.patch('functest.utils.openstack_snapshot.get_security_groups',
                       return_value=self.update_list), \
            mock.patch('functest.utils.openstack_snapshot.get_floatingips',
                       return_value=self.update_floatingips), \
            mock.patch('functest.utils.openstack_snapshot.get_users',
                       return_value=self.update_list), \
            mock.patch('functest.utils.openstack_snapshot.get_tenants',
                       return_value=self.update_list), \
                mock.patch('six.moves.builtins.open', mock.mock_open()) as m:
            openstack_snapshot.main()
            mock_logger_info.assert_called_once_with("Generating OpenStack "
                                                     "snapshot...")
            m.assert_called_once_with(openstack_snapshot.OS_SNAPSHOT_FILE,
                                      'w+')
            mock_logger_debug.assert_any_call("NOTE: These objects will "
                                              "NOT be deleted after " +
                                              "running the test.")


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
