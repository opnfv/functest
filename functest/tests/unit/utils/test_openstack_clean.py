#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest

from functest.utils import openstack_clean
from functest.tests.unit import test_utils


class OSCleanTesting(unittest.TestCase):

    def _get_instance(self, key):
        mock_obj = mock.Mock()
        attrs = {'id': 'id' + str(key), 'name': 'name' + str(key),
                 'ip': 'ip' + str(key), 'status': 'ACTIVE',
                 'OS-EXT-STS:task_state': '-'}
        mock_obj.configure_mock(**attrs)
        return mock_obj

    def _get_instance_deleted(self, key):
        mock_obj = mock.Mock()
        attrs = {'id': 'id' + str(key), 'name': 'name' + str(key),
                 'ip': 'ip' + str(key), 'status': 'DELETED',
                 'OS-EXT-STS:task_state': '-'}
        mock_obj.configure_mock(**attrs)
        return mock_obj

    def _get_instance_deleting(self, key):
        mock_obj = mock.Mock()
        attrs = {'id': 'id' + str(key), 'name': 'name' + str(key),
                 'ip': 'ip' + str(key), 'status': 'BUILD',
                 'OS-EXT-STS:task_state': 'deleting'}
        mock_obj.configure_mock(**attrs)
        return mock_obj

    def _get_instance_other(self, key):
        mock_obj = mock.Mock()
        attrs = {'id': 'id' + str(key), 'name': 'name' + str(key),
                 'ip': 'ip' + str(key), 'status': 'BUILD',
                 'OS-EXT-STS:task_state': 'networking'}
        mock_obj.configure_mock(**attrs)
        return mock_obj

    def setUp(self):
        self.client = mock.Mock()
        self.test_list = [self._get_instance(1), self._get_instance(2)]
        self.deleted_list = [self._get_instance_deleted(5),
                             self._get_instance_deleting(6)]
        self.other_list = [self._get_instance_other(7)]
        self.update_list = {'id1': 'name1', 'id2': 'name2'}
        self.remove_list = {'id3': 'name3', 'id4': 'name4'}
        self.test_dict_list = [{'id': 'id1', 'name': 'name1', 'ip': 'ip1',
                                'router:external': False,
                                'external_gateway_info': None},
                               {'id': 'id2', 'name': 'name2', 'ip': 'ip2',
                                'router:external': False,
                                'external_gateway_info': None}]
        self.floatingips_list = [{'id': 'id1', 'floating_ip_address': 'ip1'},
                                 {'id': 'id2', 'floating_ip_address': 'ip2'}]
        self.routers = [mock.Mock()]
        self.ports = [mock.Mock()]

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_separator(self, mock_logger_debug):
        openstack_clean.separator()
        mock_logger_debug.assert_called_once_with("-----------------"
                                                  "-----------------"
                                                  "---------")

    @mock.patch('time.sleep')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_instances(self, mock_logger_debug, *args):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_instances', return_value=self.test_list):
            openstack_clean.remove_instances(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing Nova instances...")
            mock_logger_debug.assert_any_call("   > this is a default "
                                              "instance and will "
                                              "NOT be deleted.")

    @mock.patch('time.sleep')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_instances_missing_instances(self, mock_logger_debug, *args):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_instances', return_value=[]):
            openstack_clean.remove_instances(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing Nova instances...")
            mock_logger_debug.assert_any_call("No instances found.")

    @mock.patch('time.sleep')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_instances_delete_success(self, mock_logger_debug, *args):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_instances', return_value=self.test_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_instance', return_value=True):
            openstack_clean.remove_instances(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Nova instances...")
            mock_logger_debug.assert_any_call("  > Request sent.")
            mock_logger_debug.assert_any_call(test_utils.RegexMatch("Removing"
                                                                    " instance"
                                                                    " '\s*\S+'"
                                                                    " ..."))

    @mock.patch('time.sleep')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_instances_pending_delete_success(self, mock_logger_debug,
                                                     *args):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_instances', return_value=self.deleted_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_instance', return_value=True):
            openstack_clean.remove_instances(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Nova instances...")
            mock_logger_debug.test_utils.RegexMatch("Removing"
                                                    " instance"
                                                    " '\s*\S+'"
                                                    " ...").assert_not_called()

    @mock.patch('time.sleep')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_instances_other_delete_success(self, mock_logger_debug,
                                                   *args):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_instances', return_value=self.other_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_instance', return_value=True):
            openstack_clean.remove_instances(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Nova instances...")
            mock_logger_debug.assert_any_call("  > Request sent.")
            mock_logger_debug.assert_any_call(test_utils.RegexMatch("Removing"
                                                                    " instance"
                                                                    " '\s*\S+'"
                                                                    " ..."))

    @mock.patch('time.sleep')
    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_instances_delete_failed(self, mock_logger_debug,
                                            mock_logger_error, *args):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_instances', return_value=self.test_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_instance', return_value=False):
            openstack_clean.remove_instances(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Nova instances...")
            mock_logger_error.assert_any_call(test_utils.
                                              RegexMatch("There has been a "
                                                         "problem removing "
                                                         "the instance \s*\S+"
                                                         "..."))
            mock_logger_debug.assert_any_call(test_utils.RegexMatch("Removing"
                                                                    " instance"
                                                                    " '\s*\S+'"
                                                                    " ..."))

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_images(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_images', return_value=self.test_list):
            openstack_clean.remove_images(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing Glance images...")
            mock_logger_debug.assert_any_call("   > this is a default "
                                              "image and will "
                                              "NOT be deleted.")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_images_missing_images(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_images', return_value=[]):
            openstack_clean.remove_images(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing Glance images...")
            mock_logger_debug.assert_any_call("No images found.")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_images_delete_success(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_images', return_value=self.test_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_glance_image', return_value=True):
            openstack_clean.remove_images(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Glance images...")
            mock_logger_debug.assert_any_call("  > Done!")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing image "
                                                         "\s*\S+,"
                                                         " ID=\s*\S+ ..."))

    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_images_delete_failed(self, mock_logger_debug,
                                         mock_logger_error):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_images', return_value=self.test_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_glance_image', return_value=False):
            openstack_clean.remove_images(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Glance images...")
            mock_logger_error.assert_any_call(test_utils.
                                              RegexMatch("There has been a "
                                                         "problem removing the"
                                                         "image \s*\S+..."))
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing image "
                                                         "\s*\S+,"
                                                         " ID=\s*\S+ ..."))

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_volumes(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_volumes', return_value=self.test_list):
            openstack_clean.remove_volumes(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing Cinder volumes...")
            mock_logger_debug.assert_any_call("   > this is a default "
                                              "volume and will "
                                              "NOT be deleted.")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_volumes_missing_volumes(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_volumes', return_value=[]):
            openstack_clean.remove_volumes(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing Cinder volumes...")
            mock_logger_debug.assert_any_call("No volumes found.")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_volumes_delete_success(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_volumes', return_value=self.test_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_volume', return_value=True):
            openstack_clean.remove_volumes(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Cinder volumes...")
            mock_logger_debug.assert_any_call("  > Done!")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing cinder "
                                                         "volume \s*\S+ ..."))

    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_volumes_delete_failed(self, mock_logger_debug,
                                          mock_logger_error):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_volumes', return_value=self.test_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_volume', return_value=False):
            openstack_clean.remove_volumes(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Cinder volumes...")
            mock_logger_error.assert_any_call(test_utils.
                                              RegexMatch("There has been a "
                                                         "problem removing "
                                                         "the "
                                                         "volume \s*\S+..."))
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing cinder "
                                                         "volume \s*\S+ ..."))

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_floatingips(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_floating_ips',
                        return_value=self.floatingips_list):
            openstack_clean.remove_floatingips(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing floating IPs...")
            mock_logger_debug.assert_any_call("   > this is a default "
                                              "floating IP and will "
                                              "NOT be deleted.")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_floatingips_missing_floatingips(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_floating_ips', return_value=[]):
            openstack_clean.remove_floatingips(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing floating IPs...")
            mock_logger_debug.assert_any_call("No floating IPs found.")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_floatingips_delete_success(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_floating_ips',
                        side_effect=[self.floatingips_list, None]), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_floating_ip', return_value=True):
            openstack_clean.remove_floatingips(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing floating IPs...")
            mock_logger_debug.assert_any_call("  > Done!")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing floating "
                                                         "IP \s*\S+ ..."))

    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_floatingips_delete_failed(self, mock_logger_debug,
                                              mock_logger_error):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_floating_ips',
                        return_value=self.floatingips_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_floating_ip', return_value=False):
            openstack_clean.remove_floatingips(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing floating IPs...")
            mock_logger_error.assert_any_call(test_utils.
                                              RegexMatch("There has been a "
                                                         "problem removing "
                                                         "the floating IP "
                                                         "\s*\S+..."))
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing floating "
                                                         "IP \s*\S+ ..."))

    @mock.patch('time.sleep')
    @mock.patch('functest.utils.openstack_clean.remove_routers')
    @mock.patch('functest.utils.openstack_clean.remove_ports')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_networks(self, mock_logger_debug,
                             mock_remove_ports,
                             mock_remove_routers, *args):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_network_list',
                        return_value=self.test_dict_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.get_port_list', return_value=self.ports), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.get_router_list', return_value=self.routers):
            openstack_clean.remove_networks(self.client, self.update_list,
                                            self.update_list)
            mock_logger_debug.assert_any_call("Removing Neutron objects")
            mock_logger_debug.assert_any_call("   > this is a default "
                                              "network and will "
                                              "NOT be deleted.")
            mock_remove_ports.assert_called_once_with(self.client, self.ports,
                                                      [])
            mock_remove_routers.assert_called_once_with(self.client,
                                                        self.routers,
                                                        self.update_list)

    @mock.patch('time.sleep')
    @mock.patch('functest.utils.openstack_clean.remove_routers')
    @mock.patch('functest.utils.openstack_clean.remove_ports')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_networks_missing_networks(self, mock_logger_debug,
                                              mock_remove_ports,
                                              mock_remove_routers, *args):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_network_list', return_value=None), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.get_port_list', return_value=self.ports), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.get_router_list', return_value=self.routers):
            openstack_clean.remove_networks(self.client, self.update_list,
                                            self.update_list)
            mock_logger_debug.assert_any_call("Removing Neutron objects")
            mock_logger_debug.assert_any_call("There are no networks in the"
                                              " deployment. ")
            mock_remove_ports.assert_called_once_with(self.client, self.ports,
                                                      [])
            mock_remove_routers.assert_called_once_with(self.client,
                                                        self.routers,
                                                        self.update_list)

    @mock.patch('time.sleep')
    @mock.patch('functest.utils.openstack_clean.remove_routers')
    @mock.patch('functest.utils.openstack_clean.remove_ports')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_networks_delete_success(self, mock_logger_debug,
                                            mock_remove_ports,
                                            mock_remove_routers, *args):

        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_network_list',
                        return_value=self.test_dict_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_neutron_net', return_value=True), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.get_port_list', return_value=self.ports), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.get_router_list', return_value=self.routers):
            openstack_clean.remove_networks(self.client, self.remove_list,
                                            self.remove_list)
            mock_logger_debug.assert_any_call("Removing Neutron objects")
            mock_logger_debug.assert_any_call("   > this network will be "
                                              "deleted.")
            mock_logger_debug.assert_any_call("  > Done!")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing network "
                                                         "\s*\S+ ..."))
            mock_remove_ports.assert_called_once_with(self.client, self.ports,
                                                      ['id1', 'id2'])
            mock_remove_routers.assert_called_once_with(self.client,
                                                        self.routers,
                                                        self.remove_list)

    @mock.patch('time.sleep')
    @mock.patch('functest.utils.openstack_clean.remove_routers')
    @mock.patch('functest.utils.openstack_clean.remove_ports')
    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_networks_delete_failed(self, mock_logger_debug,
                                           mock_logger_error,
                                           mock_remove_ports,
                                           mock_remove_routers, *args):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_network_list',
                        return_value=self.test_dict_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_neutron_net', return_value=False), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.get_port_list', return_value=self.ports), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.get_router_list', return_value=self.routers):
            openstack_clean.remove_networks(self.client, self.remove_list,
                                            self.remove_list)
            mock_logger_debug.assert_any_call("Removing Neutron objects")
            mock_logger_error.assert_any_call(test_utils.
                                              RegexMatch("There has been a"
                                                         " problem removing"
                                                         " the network \s*\S+"
                                                         "..."))
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing network "
                                                         "\s*\S+ ..."))
            mock_remove_ports.assert_called_once_with(self.client, self.ports,
                                                      ['id1', 'id2'])
            mock_remove_routers.assert_called_once_with(self.client,
                                                        self.routers,
                                                        self.remove_list)

    # TODO: ports
    @mock.patch('functest.utils.openstack_clean.os_utils.update_neutron_port')
    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_force_remove_port(self, mock_logger_debug,
                               mock_logger_error,
                               mock_update_neutron_port):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.delete_neutron_port',
                        return_value=True):
            openstack_clean.force_remove_port(self.client, 'id')
            mock_logger_debug.assert_any_call("  > Done!")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Clearing device_"
                                                         "owner for port "
                                                         "\s*\S+ ..."))

    @mock.patch('functest.utils.openstack_clean.os_utils.update_neutron_port')
    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_force_remove_port_failed(self, mock_logger_debug,
                                      mock_logger_error,
                                      mock_update_neutron_port):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.delete_neutron_port',
                        return_value=False):
            openstack_clean.force_remove_port(self.client, 'id')
            mock_logger_error.assert_any_call("There has been a "
                                              "problem removing "
                                              "the port id...")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Clearing device_"
                                                         "owner for port "
                                                         "\s*\S+ ..."))

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_routers_missing_routers(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.delete_neutron_router',
                        return_value=True):
            openstack_clean.remove_routers(self.client, self.test_dict_list,
                                           self.remove_list)
            mock_logger_debug.assert_any_call("Router is not connected"
                                              " to anything."
                                              "Ready to remove...")
            mock_logger_debug.assert_any_call("  > Done!")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing router "
                                                         "\s*\S+(\s*\S+) ..."))

    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_routers_failed(self, mock_logger_debug,
                                   mock_logger_error):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.delete_neutron_router',
                        return_value=False):
            openstack_clean.remove_routers(self.client, self.test_dict_list,
                                           self.remove_list)
            mock_logger_debug.assert_any_call("Router is not connected"
                                              " to anything."
                                              "Ready to remove...")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing router "
                                                         "\s*\S+(\s*\S+) ..."))
            mock_logger_error.assert_any_call(test_utils.
                                              RegexMatch("There has been "
                                                         "a problem"
                                                         " removing the "
                                                         "router \s*\S+("
                                                         "\s*\S+)..."))

    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_missing_external_gateway(self, mock_logger_debug,
                                             mock_logger_error):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.delete_neutron_router',
                        return_value=False), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.remove_gateway_router',
                           return_value=False):
            self.test_dict_list[0]['external_gateway_info'] = mock.Mock()
            openstack_clean.remove_routers(self.client, self.test_dict_list,
                                           self.remove_list)
            mock_logger_debug.assert_any_call("Router has gateway to external"
                                              " network.Removing link...")
            mock_logger_error.assert_any_call("There has been a problem "
                                              "removing the gateway...")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch("Removing router "
                                                         "\s*\S+(\s*\S+) ..."))
            mock_logger_error.assert_any_call(test_utils.
                                              RegexMatch("There has been "
                                                         "a problem"
                                                         " removing the "
                                                         "router \s*\S+("
                                                         "\s*\S+)..."))

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def remove_security_groups(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_security_groups',
                        return_value=self.test_dict_list):
            openstack_clean.remove_security_groups(self.client,
                                                   self.update_list)
            mock_logger_debug.assert_any_call("Removing Security groups...")
            mock_logger_debug.assert_any_call("   > this is a default "
                                              "security group and will NOT "
                                              "be deleted.")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_security_groups_missing_sec_group(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_security_groups', return_value=[]):
            openstack_clean.remove_security_groups(self.client,
                                                   self.update_list)
            mock_logger_debug.assert_any_call("Removing Security groups...")
            mock_logger_debug.assert_any_call("No security groups found.")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_security_groups_delete_success(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_security_groups',
                        return_value=self.test_dict_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_security_group', return_value=True):
            openstack_clean.remove_security_groups(self.client,
                                                   self.remove_list)
            mock_logger_debug.assert_any_call("Removing Security groups...")
            mock_logger_debug.assert_any_call("  > Done!")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch(" Removing \s*\S+"
                                                         "..."))

    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_security_groups_delete_failed(self, mock_logger_debug,
                                                  mock_logger_error):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_security_groups',
                        return_value=self.test_dict_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_security_group', return_value=False):
            openstack_clean.remove_security_groups(self.client,
                                                   self.remove_list)
            mock_logger_debug.assert_any_call("Removing Security groups...")
            mock_logger_error.assert_any_call(test_utils.
                                              RegexMatch("There has been a "
                                                         "problem removing "
                                                         "the security group"
                                                         " \s*\S+..."))
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch(" Removing \s*\S+"
                                                         "..."))

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_users(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_users', return_value=self.test_list):
            openstack_clean.remove_users(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing Users...")
            mock_logger_debug.assert_any_call("   > this is a default "
                                              "user and will "
                                              "NOT be deleted.")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_users_missing_users(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_users', return_value=None):
            openstack_clean.remove_users(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing Users...")
            mock_logger_debug.assert_any_call("There are no users in"
                                              " the deployment. ")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_users_delete_success(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_users', return_value=self.test_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_user', return_value=True):
            openstack_clean.remove_users(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Users...")
            mock_logger_debug.assert_any_call("  > Done!")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch(" Removing "
                                                         "\s*\S+..."))

    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_users_delete_failed(self, mock_logger_debug,
                                        mock_logger_error):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_users', return_value=self.test_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_user', return_value=False):
            openstack_clean.remove_users(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Users...")
            mock_logger_error.assert_any_call(test_utils.
                                              RegexMatch("There has been a "
                                                         "problem removing "
                                                         "the user \s*\S+"
                                                         "..."))
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch(" Removing "
                                                         "\s*\S+..."))

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_tenants(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_tenants', return_value=self.test_list):
            openstack_clean.remove_tenants(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing Tenants...")
            mock_logger_debug.assert_any_call("   > this is a default"
                                              " tenant and will "
                                              "NOT be deleted.")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_tenants_missing_tenants(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_tenants', return_value=None):
            openstack_clean.remove_tenants(self.client, self.update_list)
            mock_logger_debug.assert_any_call("Removing Tenants...")
            mock_logger_debug.assert_any_call("There are no tenants in"
                                              " the deployment. ")

    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_tenants_delete_success(self, mock_logger_debug):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_tenants', return_value=self.test_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_tenant', return_value=True):
            openstack_clean.remove_tenants(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Tenants...")
            mock_logger_debug.assert_any_call("  > Done!")
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch(" Removing "
                                                         "\s*\S+..."))

    @mock.patch('functest.utils.openstack_clean.logger.error')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_remove_tenants_delete_failed(self, mock_logger_debug,
                                          mock_logger_error):
        with mock.patch('functest.utils.openstack_clean.os_utils'
                        '.get_tenants', return_value=self.test_list), \
                mock.patch('functest.utils.openstack_clean.os_utils'
                           '.delete_tenant', return_value=False):
            openstack_clean.remove_tenants(self.client, self.remove_list)
            mock_logger_debug.assert_any_call("Removing Tenants...")
            mock_logger_error.assert_any_call(test_utils.
                                              RegexMatch("There has been a "
                                                         "problem removing "
                                                         "the tenant \s*\S+"
                                                         "..."))
            mock_logger_debug.assert_any_call(test_utils.
                                              RegexMatch(" Removing "
                                                         "\s*\S+..."))

    @mock.patch('functest.utils.openstack_clean.os_utils.get_glance_client')
    @mock.patch('functest.utils.openstack_clean.os_utils.get_cinder_client')
    @mock.patch('functest.utils.openstack_clean.os_utils'
                '.get_keystone_client')
    @mock.patch('functest.utils.openstack_clean.os_utils'
                '.get_neutron_client')
    @mock.patch('functest.utils.openstack_clean.os_utils.get_nova_client')
    @mock.patch('functest.utils.openstack_clean.os_utils.check_credentials',
                return_value=True)
    @mock.patch('functest.utils.openstack_clean.logger.info')
    @mock.patch('functest.utils.openstack_clean.logger.debug')
    def test_main_default(self, mock_logger_debug, mock_logger_info,
                          mock_creds, mock_nova, mock_neutron,
                          mock_keystone, mock_cinder, mock_glance):

        with mock.patch('functest.utils.openstack_clean.remove_instances') \
            as mock_remove_instances, \
            mock.patch('functest.utils.openstack_clean.remove_images') \
            as mock_remove_images, \
            mock.patch('functest.utils.openstack_clean.remove_volumes') \
            as mock_remove_volumes, \
            mock.patch('functest.utils.openstack_clean.remove_floatingips') \
            as mock_remove_floatingips, \
            mock.patch('functest.utils.openstack_clean.remove_networks') \
            as mock_remove_networks, \
            mock.patch('functest.utils.openstack_clean.'
                       'remove_security_groups') \
            as mock_remove_security_groups, \
            mock.patch('functest.utils.openstack_clean.remove_users') \
            as mock_remove_users, \
            mock.patch('functest.utils.openstack_clean.remove_tenants') \
            as mock_remove_tenants, \
            mock.patch('functest.utils.openstack_clean.yaml.safe_load',
                       return_value=mock.Mock()), \
                mock.patch('six.moves.builtins.open', mock.mock_open()) as m:
            openstack_clean.main()
            self.assertTrue(mock_remove_instances)
            self.assertTrue(mock_remove_images)
            self.assertTrue(mock_remove_volumes)
            self.assertTrue(mock_remove_floatingips)
            self.assertTrue(mock_remove_networks)
            self.assertTrue(mock_remove_security_groups)
            self.assertTrue(mock_remove_users)
            self.assertTrue(mock_remove_tenants)
            m.assert_called_once_with(openstack_clean.OS_SNAPSHOT_FILE)
            mock_logger_info.assert_called_once_with("Cleaning OpenStack "
                                                     "resources...")


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
