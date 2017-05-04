#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import copy
import logging
import os
import unittest

import mock

from functest.utils import openstack_utils


class OSUtilsTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def _get_env_cred_dict(self, os_prefix=''):
        return {'OS_USERNAME': os_prefix + 'username',
                'OS_PASSWORD': os_prefix + 'password',
                'OS_AUTH_URL': os_prefix + 'auth_url',
                'OS_TENANT_NAME': os_prefix + 'tenant_name',
                'OS_USER_DOMAIN_NAME': os_prefix + 'user_domain_name',
                'OS_PROJECT_DOMAIN_NAME': os_prefix + 'project_domain_name',
                'OS_PROJECT_NAME': os_prefix + 'project_name',
                'OS_ENDPOINT_TYPE': os_prefix + 'endpoint_type',
                'OS_REGION_NAME': os_prefix + 'region_name',
                'OS_CACERT': os_prefix + 'https_cacert'}

    def _get_os_env_vars(self):
        return {'username': 'test_username', 'password': 'test_password',
                'auth_url': 'test_auth_url', 'tenant_name': 'test_tenant_name',
                'user_domain_name': 'test_user_domain_name',
                'project_domain_name': 'test_project_domain_name',
                'project_name': 'test_project_name',
                'endpoint_type': 'test_endpoint_type',
                'region_name': 'test_region_name',
                'https_cacert': 'test_https_cacert'}

    def setUp(self):
        self.env_vars = ['OS_AUTH_URL', 'OS_USERNAME', 'OS_PASSWORD']
        self.tenant_name = 'test_tenant_name'
        self.env_cred_dict = self._get_env_cred_dict()
        self.os_environs = self._get_env_cred_dict(os_prefix='test_')
        self.os_env_vars = self._get_os_env_vars()

        mock_obj = mock.Mock()
        attrs = {'name': 'test_flavor',
                 'id': 'flavor_id',
                 'ram': 2}
        mock_obj.configure_mock(**attrs)
        self.flavor = mock_obj

        mock_obj = mock.Mock()
        attrs = {'name': 'test_aggregate',
                 'id': 'aggregate_id',
                 'hosts': ['host_name']}
        mock_obj.configure_mock(**attrs)
        self.aggregate = mock_obj

        mock_obj = mock.Mock()
        attrs = {'id': 'instance_id',
                 'name': 'test_instance',
                 'status': 'ok'}
        mock_obj.configure_mock(**attrs)
        self.instance = mock_obj

        mock_obj = mock.Mock()
        attrs = {'id': 'azone_id',
                 'zoneName': 'test_azone',
                 'status': 'ok'}
        mock_obj.configure_mock(**attrs)
        self.availability_zone = mock_obj

        mock_obj = mock.Mock()
        attrs = {'id': 'floating_id',
                 'zoneName': 'test_floating_ip',
                 'status': 'ok'}
        mock_obj.configure_mock(**attrs)
        self.floating_ip = mock_obj

        mock_obj = mock.Mock()
        attrs = {'id': 'hypervisor_id',
                 'hypervisor_hostname': 'test_hostname',
                 'state': 'up'}
        mock_obj.configure_mock(**attrs)
        self.hypervisor = mock_obj

        mock_obj = mock.Mock()
        attrs = {'id': 'image_id',
                 'name': 'test_image'}
        mock_obj.configure_mock(**attrs)
        self.image = mock_obj

        mock_obj = mock.Mock()
        self.mock_return = mock_obj

        self.nova_client = mock.Mock()
        attrs = {'servers.list.return_value': [self.instance],
                 'servers.get.return_value': self.instance,
                 'servers.find.return_value': self.instance,
                 'servers.create.return_value': self.instance,
                 'flavors.list.return_value': [self.flavor],
                 'flavors.find.return_value': self.flavor,
                 'servers.add_floating_ip.return_value': mock.Mock(),
                 'servers.force_delete.return_value': mock.Mock(),
                 'aggregates.list.return_value': [self.aggregate],
                 'aggregates.add_host.return_value': mock.Mock(),
                 'aggregates.remove_host.return_value': mock.Mock(),
                 'aggregates.get.return_value': self.aggregate,
                 'aggregates.delete.return_value': mock.Mock(),
                 'availability_zones.list.return_value':
                 [self.availability_zone],
                 'floating_ips.list.return_value': [self.floating_ip],
                 'floating_ips.delete.return_value': mock.Mock(),
                 'hypervisors.list.return_value': [self.hypervisor],
                 'create.return_value': mock.Mock(),
                 'add_security_group.return_value': mock.Mock(),
                 'images.list.return_value': [self.image],
                 'images.delete.return_value': mock.Mock(),
                 }
        self.nova_client.configure_mock(**attrs)

        self.glance_client = mock.Mock()
        attrs = {'images.list.return_value': [self.image],
                 'images.create.return_value': self.image,
                 'images.upload.return_value': mock.Mock()}
        self.glance_client.configure_mock(**attrs)

        mock_obj = mock.Mock()
        attrs = {'id': 'volume_id',
                 'name': 'test_volume'}
        mock_obj.configure_mock(**attrs)
        self.volume = mock_obj

        mock_obj = mock.Mock()
        attrs = {'id': 'volume_type_id',
                 'name': 'test_volume_type',
                 'is_public': True}
        mock_obj.configure_mock(**attrs)
        self.volume_types = [mock_obj]

        mock_obj = mock.Mock()
        attrs = {'id': 'volume_type_id',
                 'name': 'test_volume_type',
                 'is_public': False}
        mock_obj.configure_mock(**attrs)
        self.volume_types.append(mock_obj)

        self.cinder_client = mock.Mock()
        attrs = {'volumes.list.return_value': [self.volume],
                 'volume_types.list.return_value': self.volume_types,
                 'volume_types.create.return_value': self.volume_types[0],
                 'volume_types.delete.return_value': mock.Mock(),
                 'quotas.update.return_value': mock.Mock(),
                 'volumes.detach.return_value': mock.Mock(),
                 'volumes.force_delete.return_value': mock.Mock(),
                 'volumes.delete.return_value': mock.Mock()
                 }
        self.cinder_client.configure_mock(**attrs)

        self.resource = mock.Mock()
        attrs = {'id': 'resource_test_id',
                 'name': 'resource_test_name'
                 }

        self.heat_client = mock.Mock()
        attrs = {'resources.get.return_value': self.resource}
        self.heat_client.configure_mock(**attrs)

        mock_obj = mock.Mock()
        attrs = {'id': 'tenant_id',
                 'name': 'test_tenant'}
        mock_obj.configure_mock(**attrs)
        self.tenant = mock_obj

        mock_obj = mock.Mock()
        attrs = {'id': 'user_id',
                 'name': 'test_user'}
        mock_obj.configure_mock(**attrs)
        self.user = mock_obj

        mock_obj = mock.Mock()
        attrs = {'id': 'role_id',
                 'name': 'test_role'}
        mock_obj.configure_mock(**attrs)
        self.role = mock_obj

        self.keystone_client = mock.Mock()
        attrs = {'projects.list.return_value': [self.tenant],
                 'tenants.list.return_value': [self.tenant],
                 'users.list.return_value': [self.user],
                 'roles.list.return_value': [self.role],
                 'projects.create.return_value': self.tenant,
                 'tenants.create.return_value': self.tenant,
                 'users.create.return_value': self.user,
                 'roles.grant.return_value': mock.Mock(),
                 'roles.add_user_role.return_value': mock.Mock(),
                 'projects.delete.return_value': mock.Mock(),
                 'tenants.delete.return_value': mock.Mock(),
                 'users.delete.return_value': mock.Mock(),
                 }
        self.keystone_client.configure_mock(**attrs)

        self.router = {'id': 'router_id',
                       'name': 'test_router'}

        self.subnet = {'id': 'subnet_id',
                       'name': 'test_subnet'}

        self.networks = [{'id': 'network_id',
                          'name': 'test_network',
                          'router:external': False,
                          'shared': True,
                          'subnets': [self.subnet]},
                         {'id': 'network_id1',
                          'name': 'test_network1',
                          'router:external': True,
                          'shared': True,
                          'subnets': [self.subnet]}]

        self.port = {'id': 'port_id',
                     'name': 'test_port'}

        self.sec_group = {'id': 'sec_group_id',
                          'name': 'test_sec_group'}

        self.sec_group_rule = {'id': 'sec_group_rule_id',
                               'direction': 'direction',
                               'protocol': 'protocol',
                               'port_range_max': 'port_max',
                               'security_group_id': self.sec_group['id'],
                               'port_range_min': 'port_min'}
        self.neutron_floatingip = {'id': 'fip_id',
                                   'floating_ip_address': 'test_ip'}
        self.neutron_client = mock.Mock()
        attrs = {'list_networks.return_value': {'networks': self.networks},
                 'list_routers.return_value': {'routers': [self.router]},
                 'list_ports.return_value': {'ports': [self.port]},
                 'list_subnets.return_value': {'subnets': [self.subnet]},
                 'create_network.return_value': {'network': self.networks[0]},
                 'create_subnet.return_value': {'subnets': [self.subnet]},
                 'create_router.return_value': {'router': self.router},
                 'create_port.return_value': {'port': self.port},
                 'create_floatingip.return_value': {'floatingip':
                                                    self.neutron_floatingip},
                 'update_network.return_value': mock.Mock(),
                 'update_port.return_value': {'port': self.port},
                 'add_interface_router.return_value': mock.Mock(),
                 'add_gateway_router.return_value': mock.Mock(),
                 'delete_network.return_value': mock.Mock(),
                 'delete_subnet.return_value': mock.Mock(),
                 'delete_router.return_value': mock.Mock(),
                 'delete_port.return_value': mock.Mock(),
                 'remove_interface_router.return_value': mock.Mock(),
                 'remove_gateway_router.return_value': mock.Mock(),
                 'create_bgpvpn.return_value': self.mock_return,
                 'create_network_association.return_value': self.mock_return,
                 'create_router_association.return_value': self.mock_return,
                 'update_bgpvpn.return_value': self.mock_return,
                 'delete_bgpvpn.return_value': self.mock_return,
                 'show_bgpvpn.return_value': self.mock_return,
                 'list_security_groups.return_value': {'security_groups':
                                                       [self.sec_group]},
                 'list_security_group_rules.'
                 'return_value': {'security_group_rules':
                                  [self.sec_group_rule]},
                 'create_security_group_rule.return_value': mock.Mock(),
                 'create_security_group.return_value': {'security_group':
                                                        self.sec_group},
                 'update_quota.return_value': mock.Mock(),
                 'delete_security_group.return_value': mock.Mock()
                 }
        self.neutron_client.configure_mock(**attrs)

        self.empty_client = mock.Mock()
        attrs = {'list_networks.return_value': {'networks': []},
                 'list_routers.return_value': {'routers': []},
                 'list_ports.return_value': {'ports': []},
                 'list_subnets.return_value': {'subnets': []}}
        self.empty_client.configure_mock(**attrs)

    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value=None)
    def test_is_keystone_v3_missing_identity(self, mock_os_getenv):
        self.assertEqual(openstack_utils.is_keystone_v3(), False)

    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value='3')
    def test_is_keystone_v3_default(self, mock_os_getenv):
        self.assertEqual(openstack_utils.is_keystone_v3(), True)

    @mock.patch('functest.utils.openstack_utils.is_keystone_v3',
                return_value=False)
    def test_get_rc_env_vars_missing_identity(self, mock_get_rc_env):
        exp_resp = self.env_vars
        exp_resp.extend(['OS_TENANT_NAME'])
        self.assertEqual(openstack_utils.get_rc_env_vars(), exp_resp)

    @mock.patch('functest.utils.openstack_utils.is_keystone_v3',
                return_value=True)
    def test_get_rc_env_vars_default(self, mock_get_rc_env):
        exp_resp = self.env_vars
        exp_resp.extend(['OS_PROJECT_NAME',
                         'OS_USER_DOMAIN_NAME',
                         'OS_PROJECT_DOMAIN_NAME'])
        self.assertEqual(openstack_utils.get_rc_env_vars(), exp_resp)

    @mock.patch('functest.utils.openstack_utils.get_rc_env_vars')
    def test_check_credentials_missing_env(self, mock_get_rc_env):
        exp_resp = self.env_vars
        exp_resp.extend(['OS_TENANT_NAME'])
        mock_get_rc_env.return_value = exp_resp
        with mock.patch.dict('functest.utils.openstack_utils.os.environ', {},
                             clear=True):
            self.assertEqual(openstack_utils.check_credentials(), False)

    @mock.patch('functest.utils.openstack_utils.get_rc_env_vars')
    def test_check_credentials_default(self, mock_get_rc_env):
        exp_resp = ['OS_TENANT_NAME']
        mock_get_rc_env.return_value = exp_resp
        with mock.patch.dict('functest.utils.openstack_utils.os.environ',
                             {'OS_TENANT_NAME': self.tenant_name},
                             clear=True):
            self.assertEqual(openstack_utils.check_credentials(), True)

    def test_get_env_cred_dict(self):
        self.assertDictEqual(openstack_utils.get_env_cred_dict(),
                             self.env_cred_dict)

    @mock.patch('functest.utils.openstack_utils.get_rc_env_vars')
    def test_get_credentials_default(self, mock_get_rc_env):
        mock_get_rc_env.return_value = self.env_cred_dict.keys()
        with mock.patch.dict('functest.utils.openstack_utils.os.environ',
                             self.os_environs,
                             clear=True):
            self.assertDictEqual(openstack_utils.get_credentials(),
                                 self.os_env_vars)

    def _get_credentials_missing_env(self, var):
        dic = copy.deepcopy(self.os_environs)
        dic.pop(var)
        with mock.patch('functest.utils.openstack_utils.get_rc_env_vars',
                        return_value=self.env_cred_dict.keys()), \
                mock.patch.dict('functest.utils.openstack_utils.os.environ',
                                dic,
                                clear=True):
            self.assertRaises(openstack_utils.MissingEnvVar,
                              lambda: openstack_utils.get_credentials())

    def test_get_credentials_missing_username(self):
        self._get_credentials_missing_env('OS_USERNAME')

    def test_get_credentials_missing_password(self):
        self._get_credentials_missing_env('OS_PASSWORD')

    def test_get_credentials_missing_auth_url(self):
        self._get_credentials_missing_env('OS_AUTH_URL')

    def test_get_credentials_missing_tenantname(self):
        self._get_credentials_missing_env('OS_TENANT_NAME')

    def test_get_credentials_missing_domainname(self):
        self._get_credentials_missing_env('OS_USER_DOMAIN_NAME')

    def test_get_credentials_missing_projectname(self):
        self._get_credentials_missing_env('OS_PROJECT_NAME')

    def test_get_credentials_missing_endpoint_type(self):
        self._get_credentials_missing_env('OS_ENDPOINT_TYPE')

    def _test_source_credentials(self, msg, key='OS_TENANT_NAME',
                                 value='admin'):
        try:
            del os.environ[key]
        except:
            pass
        f = 'rc_file'
        with mock.patch('__builtin__.open', mock.mock_open(read_data=msg),
                        create=True) as m:
            m.return_value.__iter__ = lambda self: iter(self.readline, '')
            openstack_utils.source_credentials(f)
            m.assert_called_once_with(f, 'r')
            self.assertEqual(os.environ[key], value)

    def test_source_credentials(self):
        self._test_source_credentials('OS_TENANT_NAME=admin')
        self._test_source_credentials('OS_TENANT_NAME= admin')
        self._test_source_credentials('OS_TENANT_NAME = admin')
        self._test_source_credentials('OS_TENANT_NAME = "admin"')
        self._test_source_credentials('export OS_TENANT_NAME=admin')
        self._test_source_credentials('export OS_TENANT_NAME =admin')
        self._test_source_credentials('export OS_TENANT_NAME = admin')
        self._test_source_credentials('export OS_TENANT_NAME = "admin"')
        self._test_source_credentials('OS_TENANT_NAME', value='')
        self._test_source_credentials('export OS_TENANT_NAME', value='')
        # This test will fail as soon as rc_file is fixed
        self._test_source_credentials(
            'export "\'OS_TENANT_NAME\'" = "\'admin\'"')

    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value=None)
    def test_get_keystone_client_version_missing_env(self, mock_os_getenv):
        self.assertEqual(openstack_utils.get_keystone_client_version(),
                         openstack_utils.DEFAULT_API_VERSION)

    @mock.patch('functest.utils.openstack_utils.logger.info')
    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value='3')
    def test_get_keystone_client_version_default(self, mock_os_getenv,
                                                 mock_logger_info):
        self.assertEqual(openstack_utils.get_keystone_client_version(),
                         '3')
        mock_logger_info.assert_called_once_with("OS_IDENTITY_API_VERSION is "
                                                 "set in env as '%s'", '3')

    @mock.patch('functest.utils.openstack_utils.get_session')
    @mock.patch('functest.utils.openstack_utils.keystoneclient.Client')
    @mock.patch('functest.utils.openstack_utils.get_keystone_client_version',
                return_value='3')
    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value='public')
    def test_get_keystone_client_with_interface(self, mock_os_getenv,
                                                mock_keystoneclient_version,
                                                mock_key_client,
                                                mock_get_session):
        mock_keystone_obj = mock.Mock()
        mock_session_obj = mock.Mock()
        mock_key_client.return_value = mock_keystone_obj
        mock_get_session.return_value = mock_session_obj
        self.assertEqual(openstack_utils.get_keystone_client(),
                         mock_keystone_obj)
        mock_key_client.assert_called_once_with('3',
                                                session=mock_session_obj,
                                                interface='public')

    @mock.patch('functest.utils.openstack_utils.get_session')
    @mock.patch('functest.utils.openstack_utils.keystoneclient.Client')
    @mock.patch('functest.utils.openstack_utils.get_keystone_client_version',
                return_value='3')
    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value='admin')
    def test_get_keystone_client_no_interface(self, mock_os_getenv,
                                              mock_keystoneclient_version,
                                              mock_key_client,
                                              mock_get_session):
        mock_keystone_obj = mock.Mock()
        mock_session_obj = mock.Mock()
        mock_key_client.return_value = mock_keystone_obj
        mock_get_session.return_value = mock_session_obj
        self.assertEqual(openstack_utils.get_keystone_client(),
                         mock_keystone_obj)
        mock_key_client.assert_called_once_with('3',
                                                session=mock_session_obj,
                                                interface='admin')

    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value=None)
    def test_get_nova_client_version_missing_env(self, mock_os_getenv):
        self.assertEqual(openstack_utils.get_nova_client_version(),
                         openstack_utils.DEFAULT_API_VERSION)

    @mock.patch('functest.utils.openstack_utils.logger.info')
    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value='3')
    def test_get_nova_client_version_default(self, mock_os_getenv,
                                             mock_logger_info):
        self.assertEqual(openstack_utils.get_nova_client_version(),
                         '3')
        mock_logger_info.assert_called_once_with("OS_COMPUTE_API_VERSION is "
                                                 "set in env as '%s'", '3')

    def test_get_nova_client(self):
        mock_nova_obj = mock.Mock()
        mock_session_obj = mock.Mock()
        with mock.patch('functest.utils.openstack_utils'
                        '.get_nova_client_version', return_value='3'), \
            mock.patch('functest.utils.openstack_utils'
                       '.novaclient.Client',
                       return_value=mock_nova_obj) \
            as mock_nova_client, \
            mock.patch('functest.utils.openstack_utils.get_session',
                       return_value=mock_session_obj):
            self.assertEqual(openstack_utils.get_nova_client(),
                             mock_nova_obj)
            mock_nova_client.assert_called_once_with('3',
                                                     session=mock_session_obj)

    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value=None)
    def test_get_cinder_client_version_missing_env(self, mock_os_getenv):
        self.assertEqual(openstack_utils.get_cinder_client_version(),
                         openstack_utils.DEFAULT_API_VERSION)

    @mock.patch('functest.utils.openstack_utils.logger.info')
    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value='3')
    def test_get_cinder_client_version_default(self, mock_os_getenv,
                                               mock_logger_info):
        self.assertEqual(openstack_utils.get_cinder_client_version(),
                         '3')
        mock_logger_info.assert_called_once_with("OS_VOLUME_API_VERSION is "
                                                 "set in env as '%s'", '3')

    def test_get_cinder_client(self):
        mock_cinder_obj = mock.Mock()
        mock_session_obj = mock.Mock()
        with mock.patch('functest.utils.openstack_utils'
                        '.get_cinder_client_version', return_value='3'), \
            mock.patch('functest.utils.openstack_utils'
                       '.cinderclient.Client',
                       return_value=mock_cinder_obj) \
            as mock_cind_client, \
            mock.patch('functest.utils.openstack_utils.get_session',
                       return_value=mock_session_obj):
            self.assertEqual(openstack_utils.get_cinder_client(),
                             mock_cinder_obj)
            mock_cind_client.assert_called_once_with('3',
                                                     session=mock_session_obj)

    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value=None)
    def test_get_neutron_client_version_missing_env(self, mock_os_getenv):
        self.assertEqual(openstack_utils.get_neutron_client_version(),
                         openstack_utils.DEFAULT_API_VERSION)

    @mock.patch('functest.utils.openstack_utils.logger.info')
    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value='3')
    def test_get_neutron_client_version_default(self, mock_os_getenv,
                                                mock_logger_info):
        self.assertEqual(openstack_utils.get_neutron_client_version(),
                         '3')
        mock_logger_info.assert_called_once_with("OS_NETWORK_API_VERSION is "
                                                 "set in env as '%s'", '3')

    def test_get_neutron_client(self):
        mock_neutron_obj = mock.Mock()
        mock_session_obj = mock.Mock()
        with mock.patch('functest.utils.openstack_utils'
                        '.get_neutron_client_version', return_value='3'), \
            mock.patch('functest.utils.openstack_utils'
                       '.neutronclient.Client',
                       return_value=mock_neutron_obj) \
            as mock_neut_client, \
            mock.patch('functest.utils.openstack_utils.get_session',
                       return_value=mock_session_obj):
            self.assertEqual(openstack_utils.get_neutron_client(),
                             mock_neutron_obj)
            mock_neut_client.assert_called_once_with('3',
                                                     session=mock_session_obj)

    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value=None)
    def test_get_glance_client_version_missing_env(self, mock_os_getenv):
        self.assertEqual(openstack_utils.get_glance_client_version(),
                         openstack_utils.DEFAULT_API_VERSION)

    @mock.patch('functest.utils.openstack_utils.logger.info')
    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value='3')
    def test_get_glance_client_version_default(self, mock_os_getenv,
                                               mock_logger_info):
        self.assertEqual(openstack_utils.get_glance_client_version(),
                         '3')
        mock_logger_info.assert_called_once_with("OS_IMAGE_API_VERSION is "
                                                 "set in env as '%s'", '3')

    def test_get_glance_client(self):
        mock_glance_obj = mock.Mock()
        mock_session_obj = mock.Mock()
        with mock.patch('functest.utils.openstack_utils'
                        '.get_glance_client_version', return_value='3'), \
            mock.patch('functest.utils.openstack_utils'
                       '.glanceclient.Client',
                       return_value=mock_glance_obj) \
            as mock_glan_client, \
            mock.patch('functest.utils.openstack_utils.get_session',
                       return_value=mock_session_obj):
            self.assertEqual(openstack_utils.get_glance_client(),
                             mock_glance_obj)
            mock_glan_client.assert_called_once_with('3',
                                                     session=mock_session_obj)

    @mock.patch('functest.utils.openstack_utils.os.getenv',
                return_value=None)
    def test_get_heat_client_version_missing_env(self, mock_os_getenv):
        self.assertEqual(openstack_utils.get_heat_client_version(),
                         openstack_utils.DEFAULT_HEAT_API_VERSION)

    @mock.patch('functest.utils.openstack_utils.logger.info')
    @mock.patch('functest.utils.openstack_utils.os.getenv', return_value='1')
    def test_get_heat_client_version_default(self, mock_os_getenv,
                                             mock_logger_info):
        self.assertEqual(openstack_utils.get_heat_client_version(), '1')
        mock_logger_info.assert_called_once_with(
            "OS_ORCHESTRATION_API_VERSION is set in env as '%s'", '1')

    def test_get_heat_client(self):
        mock_heat_obj = mock.Mock()
        mock_session_obj = mock.Mock()
        with mock.patch('functest.utils.openstack_utils'
                        '.get_heat_client_version', return_value='1'), \
            mock.patch('functest.utils.openstack_utils'
                       '.heatclient.Client',
                       return_value=mock_heat_obj) \
            as mock_heat_client, \
            mock.patch('functest.utils.openstack_utils.get_session',
                       return_value=mock_session_obj):
            self.assertEqual(openstack_utils.get_heat_client(),
                             mock_heat_obj)
            mock_heat_client.assert_called_once_with('1',
                                                     session=mock_session_obj)

    def test_get_instances_default(self):
        self.assertEqual(openstack_utils.get_instances(self.nova_client),
                         [self.instance])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_instances_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             get_instances(Exception),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_get_instance_status_default(self):
        self.assertEqual(openstack_utils.get_instance_status(self.nova_client,
                                                             self.instance),
                         'ok')

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_instance_status_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             get_instance_status(Exception,
                                                 self.instance),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_get_instance_by_name_default(self):
        self.assertEqual(openstack_utils.
                         get_instance_by_name(self.nova_client,
                                              'test_instance'),
                         self.instance)

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_instance_by_name_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             get_instance_by_name(Exception,
                                                  'test_instance'),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_get_flavor_id_default(self):
        self.assertEqual(openstack_utils.
                         get_flavor_id(self.nova_client,
                                       'test_flavor'),
                         self.flavor.id)

    def test_get_flavor_id_by_ram_range_default(self):
        self.assertEqual(openstack_utils.
                         get_flavor_id_by_ram_range(self.nova_client,
                                                    1, 3),
                         self.flavor.id)

    def test_get_aggregates_default(self):
        self.assertEqual(openstack_utils.
                         get_aggregates(self.nova_client),
                         [self.aggregate])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_aggregates_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             get_aggregates(Exception),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_get_aggregate_id_default(self):
        with mock.patch('functest.utils.openstack_utils.get_aggregates',
                        return_value=[self.aggregate]):
            self.assertEqual(openstack_utils.
                             get_aggregate_id(self.nova_client,
                                              'test_aggregate'),
                             'aggregate_id')

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_aggregate_id_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             get_aggregate_id(Exception,
                                              'test_aggregate'),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_get_availability_zone_names_default(self):
        with mock.patch('functest.utils.openstack_utils'
                        '.get_availability_zones',
                        return_value=[self.availability_zone]):
            self.assertEqual(openstack_utils.
                             get_availability_zone_names(self.nova_client),
                             ['test_azone'])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_availability_zone_names_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             get_availability_zone_names(Exception),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_get_availability_zones_default(self):
            self.assertEqual(openstack_utils.
                             get_availability_zones(self.nova_client),
                             [self.availability_zone])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_availability_zones_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             get_availability_zones(Exception),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_get_floating_ips_default(self):
            self.assertEqual(openstack_utils.
                             get_floating_ips(self.nova_client),
                             [self.floating_ip])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_floating_ips_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             get_floating_ips(Exception),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_get_hypervisors_default(self):
            self.assertEqual(openstack_utils.
                             get_hypervisors(self.nova_client),
                             ['test_hostname'])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_hypervisors_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             get_hypervisors(Exception),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_create_aggregate_default(self):
            self.assertTrue(openstack_utils.
                            create_aggregate(self.nova_client,
                                             'test_aggregate',
                                             'azone'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_aggregate_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             create_aggregate(Exception,
                                              'test_aggregate',
                                              'azone'),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_add_host_to_aggregate_default(self):
        with mock.patch('functest.utils.openstack_utils.get_aggregate_id'):
                self.assertTrue(openstack_utils.
                                add_host_to_aggregate(self.nova_client,
                                                      'test_aggregate',
                                                      'test_hostname'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_add_host_to_aggregate_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             add_host_to_aggregate(Exception,
                                                   'test_aggregate',
                                                   'test_hostname'),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_create_aggregate_with_host_default(self):
        with mock.patch('functest.utils.openstack_utils.create_aggregate'), \
                mock.patch('functest.utils.openstack_utils.'
                           'add_host_to_aggregate'):
            self.assertTrue(openstack_utils.
                            create_aggregate_with_host(self.nova_client,
                                                       'test_aggregate',
                                                       'test_azone',
                                                       'test_hostname'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_aggregate_with_host_exception(self, mock_logger_error):
            with mock.patch('functest.utils.openstack_utils.create_aggregate',
                            side_effect=Exception):
                self.assertEqual(openstack_utils.
                                 create_aggregate_with_host(Exception,
                                                            'test_aggregate',
                                                            'test_azone',
                                                            'test_hostname'),
                                 None)
                self.assertTrue(mock_logger_error.called)

    def test_create_instance_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_nova_client',
                        return_value=self.nova_client):
            self.assertEqual(openstack_utils.
                             create_instance('test_flavor',
                                             'image_id',
                                             'network_id'),
                             self.instance)

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_instance_exception(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_nova_client',
                        return_value=self.nova_client):
            self.nova_client.flavors.find.side_effect = Exception
            self.assertEqual(openstack_utils.
                             create_instance('test_flavor',
                                             'image_id',
                                             'network_id'),
                             None)
            self.assertTrue(mock_logger_error)

    def test_create_floating_ip_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_external_net_id',
                        return_value='external_net_id'):
            exp_resp = {'fip_addr': 'test_ip', 'fip_id': 'fip_id'}
            self.assertEqual(openstack_utils.
                             create_floating_ip(self.neutron_client),
                             exp_resp)

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_floating_ip_exception(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_external_net_id',
                        return_value='external_net_id'):
            self.assertEqual(openstack_utils.
                             create_floating_ip(Exception),
                             None)
            self.assertTrue(mock_logger_error)

    def test_add_floating_ip_default(self):
        with mock.patch('functest.utils.openstack_utils.get_aggregate_id'):
                self.assertTrue(openstack_utils.
                                add_floating_ip(self.nova_client,
                                                'test_serverid',
                                                'test_floatingip_addr'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_add_floating_ip_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             add_floating_ip(Exception,
                                             'test_serverid',
                                             'test_floatingip_addr'))
            self.assertTrue(mock_logger_error.called)

    def test_delete_instance_default(self):
            self.assertTrue(openstack_utils.
                            delete_instance(self.nova_client,
                                            'instance_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_instance_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             delete_instance(Exception,
                                             'instance_id'))
            self.assertTrue(mock_logger_error.called)

    def test_delete_floating_ip_default(self):
            self.assertTrue(openstack_utils.
                            delete_floating_ip(self.nova_client,
                                               'floating_ip_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_floating_ip_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             delete_floating_ip(Exception,
                                                'floating_ip_id'))
            self.assertTrue(mock_logger_error.called)

    def test_remove_host_from_aggregate_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_aggregate_id'):
                self.assertTrue(openstack_utils.
                                remove_host_from_aggregate(self.nova_client,
                                                           'agg_name',
                                                           'host_name'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_remove_host_from_aggregate_exception(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_aggregate_id', side_effect=Exception):
            self.assertFalse(openstack_utils.
                             remove_host_from_aggregate(self.nova_client,
                                                        'agg_name',
                                                        'host_name'))
            self.assertTrue(mock_logger_error.called)

    def test_remove_hosts_from_aggregate_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_aggregate_id'), \
            mock.patch('functest.utils.openstack_utils.'
                       'remove_host_from_aggregate',
                       return_value=True) \
                as mock_method:
            openstack_utils.remove_hosts_from_aggregate(self.nova_client,
                                                        'test_aggregate')
            mock_method.assert_any_call(self.nova_client,
                                        'test_aggregate',
                                        'host_name')

    def test_delete_aggregate_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'remove_hosts_from_aggregate'):
                self.assertTrue(openstack_utils.
                                delete_aggregate(self.nova_client,
                                                 'agg_name'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_aggregate_exception(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_utils.'
                        'remove_hosts_from_aggregate', side_effect=Exception):
            self.assertFalse(openstack_utils.
                             delete_aggregate(self.nova_client,
                                              'agg_name'))
            self.assertTrue(mock_logger_error.called)

    def test_get_network_list_default(self):
        self.assertEqual(openstack_utils.
                         get_network_list(self.neutron_client),
                         self.networks)

    def test_get_network_list_missing_network(self):
        self.assertEqual(openstack_utils.
                         get_network_list(self.empty_client),
                         None)

    def test_get_router_list_default(self):
        self.assertEqual(openstack_utils.
                         get_router_list(self.neutron_client),
                         [self.router])

    def test_get_router_list_missing_router(self):
        self.assertEqual(openstack_utils.
                         get_router_list(self.empty_client),
                         None)

    def test_get_port_list_default(self):
        self.assertEqual(openstack_utils.
                         get_port_list(self.neutron_client),
                         [self.port])

    def test_get_port_list_missing_port(self):
        self.assertEqual(openstack_utils.
                         get_port_list(self.empty_client),
                         None)

    def test_get_network_id_default(self):
        self.assertEqual(openstack_utils.
                         get_network_id(self.neutron_client,
                                        'test_network'),
                         'network_id')

    def test_get_subnet_id_default(self):
        self.assertEqual(openstack_utils.
                         get_subnet_id(self.neutron_client,
                                       'test_subnet'),
                         'subnet_id')

    def test_get_router_id_default(self):
        self.assertEqual(openstack_utils.
                         get_router_id(self.neutron_client,
                                       'test_router'),
                         'router_id')

    def test_get_private_net_default(self):
        self.assertEqual(openstack_utils.
                         get_private_net(self.neutron_client),
                         self.networks[0])

    def test_get_private_net_missing_net(self):
        self.assertEqual(openstack_utils.
                         get_private_net(self.empty_client),
                         None)

    def test_get_external_net_default(self):
        self.assertEqual(openstack_utils.
                         get_external_net(self.neutron_client),
                         'test_network1')

    def test_get_external_net_missing_net(self):
        self.assertEqual(openstack_utils.
                         get_external_net(self.empty_client),
                         None)

    def test_get_external_net_id_default(self):
        self.assertEqual(openstack_utils.
                         get_external_net_id(self.neutron_client),
                         'network_id1')

    def test_get_external_net_id_missing_net(self):
        self.assertEqual(openstack_utils.
                         get_external_net_id(self.empty_client),
                         None)

    def test_check_neutron_net_default(self):
        self.assertTrue(openstack_utils.
                        check_neutron_net(self.neutron_client,
                                          'test_network'))

    def test_check_neutron_net_missing_net(self):
        self.assertFalse(openstack_utils.
                         check_neutron_net(self.empty_client,
                                           'test_network'))

    def test_create_neutron_net_default(self):
            self.assertEqual(openstack_utils.
                             create_neutron_net(self.neutron_client,
                                                'test_network'),
                             'network_id')

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_neutron_net_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             create_neutron_net(Exception,
                                                'test_network'),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_create_neutron_subnet_default(self):
            self.assertEqual(openstack_utils.
                             create_neutron_subnet(self.neutron_client,
                                                   'test_subnet',
                                                   'test_cidr',
                                                   'network_id'),
                             'subnet_id')

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_neutron_subnet_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             create_neutron_subnet(Exception,
                                                   'test_subnet',
                                                   'test_cidr',
                                                   'network_id'),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_create_neutron_router_default(self):
            self.assertEqual(openstack_utils.
                             create_neutron_router(self.neutron_client,
                                                   'test_router'),
                             'router_id')

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_neutron_router_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             create_neutron_router(Exception,
                                                   'test_router'),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_create_neutron_port_default(self):
            self.assertEqual(openstack_utils.
                             create_neutron_port(self.neutron_client,
                                                 'test_port',
                                                 'network_id',
                                                 'test_ip'),
                             'port_id')

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_neutron_port_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             create_neutron_port(Exception,
                                                 'test_port',
                                                 'network_id',
                                                 'test_ip'),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_update_neutron_net_default(self):
            self.assertTrue(openstack_utils.
                            update_neutron_net(self.neutron_client,
                                               'network_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_update_neutron_net_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             update_neutron_net(Exception,
                                                'network_id'))
            self.assertTrue(mock_logger_error.called)

    def test_update_neutron_port_default(self):
            self.assertEqual(openstack_utils.
                             update_neutron_port(self.neutron_client,
                                                 'port_id',
                                                 'test_owner'),
                             'port_id')

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_update_neutron_port_exception(self, mock_logger_error):
            self.assertEqual(openstack_utils.
                             update_neutron_port(Exception,
                                                 'port_id',
                                                 'test_owner'),
                             None)
            self.assertTrue(mock_logger_error.called)

    def test_add_interface_router_default(self):
            self.assertTrue(openstack_utils.
                            add_interface_router(self.neutron_client,
                                                 'router_id',
                                                 'subnet_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_add_interface_router_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             add_interface_router(Exception,
                                                  'router_id',
                                                  'subnet_id'))
            self.assertTrue(mock_logger_error.called)

    def test_add_gateway_router_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_external_net_id',
                        return_value='network_id'):
                self.assertTrue(openstack_utils.
                                add_gateway_router(self.neutron_client,
                                                   'router_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_add_gateway_router_exception(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_external_net_id',
                        return_value='network_id'):
                self.assertFalse(openstack_utils.
                                 add_gateway_router(Exception,
                                                    'router_id'))
                self.assertTrue(mock_logger_error.called)

    def test_delete_neutron_net_default(self):
            self.assertTrue(openstack_utils.
                            delete_neutron_net(self.neutron_client,
                                               'network_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_neutron_net_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             delete_neutron_net(Exception,
                                                'network_id'))
            self.assertTrue(mock_logger_error.called)

    def test_delete_neutron_subnet_default(self):
            self.assertTrue(openstack_utils.
                            delete_neutron_subnet(self.neutron_client,
                                                  'subnet_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_neutron_subnet_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             delete_neutron_subnet(Exception,
                                                   'subnet_id'))
            self.assertTrue(mock_logger_error.called)

    def test_delete_neutron_router_default(self):
            self.assertTrue(openstack_utils.
                            delete_neutron_router(self.neutron_client,
                                                  'router_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_neutron_router_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             delete_neutron_router(Exception,
                                                   'router_id'))
            self.assertTrue(mock_logger_error.called)

    def test_delete_neutron_port_default(self):
            self.assertTrue(openstack_utils.
                            delete_neutron_port(self.neutron_client,
                                                'port_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_neutron_port_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             delete_neutron_port(Exception,
                                                 'port_id'))
            self.assertTrue(mock_logger_error.called)

    def test_remove_interface_router_default(self):
            self.assertTrue(openstack_utils.
                            remove_interface_router(self.neutron_client,
                                                    'router_id',
                                                    'subnet_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_remove_interface_router_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             remove_interface_router(Exception,
                                                     'router_id',
                                                     'subnet_id'))
            self.assertTrue(mock_logger_error.called)

    def test_remove_gateway_router_default(self):
            self.assertTrue(openstack_utils.
                            remove_gateway_router(self.neutron_client,
                                                  'router_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_remove_gateway_router_exception(self, mock_logger_error):
            self.assertFalse(openstack_utils.
                             remove_gateway_router(Exception,
                                                   'router_id'))
            self.assertTrue(mock_logger_error.called)

    def test_create_bgpvpn(self):
        self.assertEqual(openstack_utils.
                         create_bgpvpn(self.neutron_client),
                         self.mock_return)

    def test_create_network_association(self):
        self.assertEqual(openstack_utils.
                         create_network_association(self.neutron_client,
                                                    'bgpvpn_id',
                                                    'network_id'),
                         self.mock_return)

    def test_create_router_association(self):
        self.assertEqual(openstack_utils.
                         create_router_association(self.neutron_client,
                                                   'bgpvpn_id',
                                                   'router_id'),
                         self.mock_return)

    def test_update_bgpvpn(self):
        self.assertEqual(openstack_utils.
                         update_bgpvpn(self.neutron_client,
                                       'bgpvpn_id'),
                         self.mock_return)

    def test_delete_bgpvpn(self):
        self.assertEqual(openstack_utils.
                         delete_bgpvpn(self.neutron_client,
                                       'bgpvpn_id'),
                         self.mock_return)

    def test_get_bgpvpn(self):
        self.assertEqual(openstack_utils.
                         get_bgpvpn(self.neutron_client,
                                    'bgpvpn_id'),
                         self.mock_return)

    def test_get_bgpvpn_routers(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_bgpvpn',
                        return_value={'bgpvpn':
                                      {'routers': [self.router]}}):
            self.assertEqual(openstack_utils.
                             get_bgpvpn_routers(self.neutron_client,
                                                'bgpvpn_id'),
                             [self.router])

    def test_get_security_groups_default(self):
        self.assertEqual(openstack_utils.
                         get_security_groups(self.neutron_client),
                         [self.sec_group])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_security_groups_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         get_security_groups(Exception),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_get_security_group_id_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_security_groups',
                        return_value=[self.sec_group]):
            self.assertEqual(openstack_utils.
                             get_security_group_id(self.neutron_client,
                                                   'test_sec_group'),
                             'sec_group_id')

    def test_get_security_group_rules_default(self):
        self.assertEqual(openstack_utils.
                         get_security_group_rules(self.neutron_client,
                                                  self.sec_group['id']),
                         [self.sec_group_rule])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_security_group_rules_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         get_security_group_rules(Exception,
                                                  'sec_group_id'),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_check_security_group_rules_not_exists(self):
        self.assertEqual(openstack_utils.
                         check_security_group_rules(self.neutron_client,
                                                    'sec_group_id_2',
                                                    'direction',
                                                    'protocol',
                                                    'port_min',
                                                    'port_max'),
                         True)

    def test_check_security_group_rules_exists(self):
        self.assertEqual(openstack_utils.
                         check_security_group_rules(self.neutron_client,
                                                    self.sec_group['id'],
                                                    'direction',
                                                    'protocol',
                                                    'port_min',
                                                    'port_max'),
                         False)

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_check_security_group_rules_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         check_security_group_rules(Exception,
                                                    'sec_group_id',
                                                    'direction',
                                                    'protocol',
                                                    'port_max',
                                                    'port_min'),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_create_security_group_default(self):
        self.assertEqual(openstack_utils.
                         create_security_group(self.neutron_client,
                                               'test_sec_group',
                                               'sec_group_desc'),
                         self.sec_group)

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_security_group_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         create_security_group(Exception,
                                               'test_sec_group',
                                               'sec_group_desc'),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_create_secgroup_rule_default(self):
        self.assertTrue(openstack_utils.
                        create_secgroup_rule(self.neutron_client,
                                             'sg_id',
                                             'direction',
                                             'protocol',
                                             80,
                                             80))
        self.assertTrue(openstack_utils.
                        create_secgroup_rule(self.neutron_client,
                                             'sg_id',
                                             'direction',
                                             'protocol'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_secgroup_rule_invalid_port_range(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         create_secgroup_rule(self.neutron_client,
                                              'sg_id',
                                              'direction',
                                              'protocol',
                                              80))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_secgroup_rule_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         create_secgroup_rule(Exception,
                                              'sg_id',
                                              'direction',
                                              'protocol'))

    @mock.patch('functest.utils.openstack_utils.logger.info')
    def test_create_security_group_full_default(self, mock_logger_info):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_security_group_id',
                        return_value='sg_id'):
            self.assertEqual(openstack_utils.
                             create_security_group_full(self.neutron_client,
                                                        'sg_name',
                                                        'sg_desc'),
                             'sg_id')
            self.assertTrue(mock_logger_info)

    @mock.patch('functest.utils.openstack_utils.logger.info')
    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_security_group_full_sec_group_fail(self,
                                                       mock_logger_error,
                                                       mock_logger_info):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_security_group_id',
                        return_value=''), \
            mock.patch('functest.utils.openstack_utils.'
                       'create_security_group',
                       return_value=False):
            self.assertEqual(openstack_utils.
                             create_security_group_full(self.neutron_client,
                                                        'sg_name',
                                                        'sg_desc'),
                             None)
            self.assertTrue(mock_logger_error)
            self.assertTrue(mock_logger_info)

    @mock.patch('functest.utils.openstack_utils.logger.debug')
    @mock.patch('functest.utils.openstack_utils.logger.info')
    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_security_group_full_secgroup_rule_fail(self,
                                                           mock_logger_error,
                                                           mock_logger_info,
                                                           mock_logger_debug):
        with mock.patch('functest.utils.openstack_utils.'
                        'get_security_group_id',
                        return_value=''), \
            mock.patch('functest.utils.openstack_utils.'
                       'create_security_group',
                       return_value={'id': 'sg_id',
                                     'name': 'sg_name'}), \
            mock.patch('functest.utils.openstack_utils.'
                       'create_secgroup_rule',
                       return_value=False):
            self.assertEqual(openstack_utils.
                             create_security_group_full(self.neutron_client,
                                                        'sg_name',
                                                        'sg_desc'),
                             None)
            self.assertTrue(mock_logger_error)
            self.assertTrue(mock_logger_info)
            self.assertTrue(mock_logger_debug)

    def test_add_secgroup_to_instance_default(self):
        self.assertTrue(openstack_utils.
                        add_secgroup_to_instance(self.nova_client,
                                                 'instance_id',
                                                 'sec_group_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_add_secgroup_to_instance_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         add_secgroup_to_instance(Exception,
                                                  'instance_id',
                                                  'sec_group_id'))
        self.assertTrue(mock_logger_error.called)

    def test_update_sg_quota_default(self):
        self.assertTrue(openstack_utils.
                        update_sg_quota(self.neutron_client,
                                        'tenant_id',
                                        'sg_quota',
                                        'sg_rule_quota'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_update_sg_quota_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         update_sg_quota(Exception,
                                         'tenant_id',
                                         'sg_quota',
                                         'sg_rule_quota'))
        self.assertTrue(mock_logger_error.called)

    def test_delete_security_group_default(self):
        self.assertTrue(openstack_utils.
                        delete_security_group(self.neutron_client,
                                              'sec_group_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_security_group_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         delete_security_group(Exception,
                                               'sec_group_id'))
        self.assertTrue(mock_logger_error.called)

    def test_get_images_default(self):
        self.assertEqual(openstack_utils.
                         get_images(self.nova_client),
                         [self.image])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_images_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         get_images(Exception),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_get_image_id_default(self):
        self.assertEqual(openstack_utils.
                         get_image_id(self.glance_client,
                                      'test_image'),
                         'image_id')

    # create_glance_image, get_or_create_image
    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_glance_image_file_present(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_utils.'
                        'os.path.isfile',
                        return_value=False):
            self.assertEqual(openstack_utils.
                             create_glance_image(self.glance_client,
                                                 'test_image',
                                                 'file_path'),
                             None)
            self.assertTrue(mock_logger_error.called)

    @mock.patch('functest.utils.openstack_utils.logger.info')
    def test_create_glance_image_already_exist(self, mock_logger_info):
        with mock.patch('functest.utils.openstack_utils.'
                        'os.path.isfile',
                        return_value=True), \
            mock.patch('functest.utils.openstack_utils.get_image_id',
                       return_value='image_id'):
                self.assertEqual(openstack_utils.
                                 create_glance_image(self.glance_client,
                                                     'test_image',
                                                     'file_path'),
                                 'image_id')
                self.assertTrue(mock_logger_info.called)

    @mock.patch('functest.utils.openstack_utils.logger.info')
    def test_create_glance_image_default(self, mock_logger_info):
        with mock.patch('functest.utils.openstack_utils.'
                        'os.path.isfile',
                        return_value=True), \
            mock.patch('functest.utils.openstack_utils.get_image_id',
                       return_value=''), \
            mock.patch('__builtin__.open',
                       mock.mock_open(read_data='1')) as m:
                self.assertEqual(openstack_utils.
                                 create_glance_image(self.glance_client,
                                                     'test_image',
                                                     'file_path'),
                                 'image_id')
                m.assert_called_once_with('file_path')
                self.assertTrue(mock_logger_info.called)

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_glance_image_exception(self, mock_logger_error):
        with mock.patch('functest.utils.openstack_utils.'
                        'os.path.isfile',
                        return_value=True), \
            mock.patch('functest.utils.openstack_utils.get_image_id',
                       side_effect=Exception):
                self.assertEqual(openstack_utils.
                                 create_glance_image(self.glance_client,
                                                     'test_image',
                                                     'file_path'),
                                 None)
                self.assertTrue(mock_logger_error.called)

    def test_delete_glance_image_default(self):
        self.assertTrue(openstack_utils.
                        delete_glance_image(self.nova_client,
                                            'image_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_glance_image_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         delete_glance_image(Exception,
                                             'image_id'))
        self.assertTrue(mock_logger_error.called)

    def test_get_volumes_default(self):
        self.assertEqual(openstack_utils.
                         get_volumes(self.cinder_client),
                         [self.volume])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_volumes_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         get_volumes(Exception),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_list_volume_types_default_private(self):
        self.assertEqual(openstack_utils.
                         list_volume_types(self.cinder_client,
                                           public=False,
                                           private=True),
                         [self.volume_types[1]])

    def test_list_volume_types_default_public(self):
        self.assertEqual(openstack_utils.
                         list_volume_types(self.cinder_client,
                                           public=True,
                                           private=False),
                         [self.volume_types[0]])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_list_volume_types_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         list_volume_types(Exception),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_create_volume_type_default(self):
        self.assertEqual(openstack_utils.
                         create_volume_type(self.cinder_client,
                                            'test_volume_type'),
                         self.volume_types[0])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_volume_type_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         create_volume_type(Exception,
                                            'test_volume_type'),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_update_cinder_quota_default(self):
        self.assertTrue(openstack_utils.
                        update_cinder_quota(self.cinder_client,
                                            'tenant_id',
                                            'vols_quota',
                                            'snap_quota',
                                            'giga_quota'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_update_cinder_quota_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         update_cinder_quota(Exception,
                                             'tenant_id',
                                             'vols_quota',
                                             'snap_quota',
                                             'giga_quota'))
        self.assertTrue(mock_logger_error.called)

    def test_delete_volume_default(self):
        self.assertTrue(openstack_utils.
                        delete_volume(self.cinder_client,
                                      'volume_id',
                                      forced=False))

        self.assertTrue(openstack_utils.
                        delete_volume(self.cinder_client,
                                      'volume_id',
                                      forced=True))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_volume_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         delete_volume(Exception,
                                       'volume_id',
                                       forced=True))
        self.assertTrue(mock_logger_error.called)

    def test_delete_volume_type_default(self):
        self.assertTrue(openstack_utils.
                        delete_volume_type(self.cinder_client,
                                           self.volume_types[0]))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_volume_type_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         delete_volume_type(Exception,
                                            self.volume_types[0]))
        self.assertTrue(mock_logger_error.called)

    def test_get_tenants_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=True):
            self.assertEqual(openstack_utils.
                             get_tenants(self.keystone_client),
                             [self.tenant])
        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=False):
            self.assertEqual(openstack_utils.
                             get_tenants(self.keystone_client),
                             [self.tenant])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_tenants_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         get_tenants(Exception),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_get_users_default(self):
        self.assertEqual(openstack_utils.
                         get_users(self.keystone_client),
                         [self.user])

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_users_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         get_users(Exception),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_get_tenant_id_default(self):
        self.assertEqual(openstack_utils.
                         get_tenant_id(self.keystone_client,
                                       'test_tenant'),
                         'tenant_id')

    def test_get_user_id_default(self):
        self.assertEqual(openstack_utils.
                         get_user_id(self.keystone_client,
                                     'test_user'),
                         'user_id')

    def test_get_role_id_default(self):
        self.assertEqual(openstack_utils.
                         get_role_id(self.keystone_client,
                                     'test_role'),
                         'role_id')

    def test_create_tenant_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=True):
            self.assertEqual(openstack_utils.
                             create_tenant(self.keystone_client,
                                           'test_tenant',
                                           'tenant_desc'),
                             'tenant_id')
        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=False):
            self.assertEqual(openstack_utils.
                             create_tenant(self.keystone_client,
                                           'test_tenant',
                                           'tenant_desc'),
                             'tenant_id')

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_tenant_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         create_tenant(Exception,
                                       'test_tenant',
                                       'tenant_desc'),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_create_user_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=True):
            self.assertEqual(openstack_utils.
                             create_user(self.keystone_client,
                                         'test_user',
                                         'password',
                                         'email',
                                         'tenant_id'),
                             'user_id')
        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=False):
            self.assertEqual(openstack_utils.
                             create_user(self.keystone_client,
                                         'test_user',
                                         'password',
                                         'email',
                                         'tenant_id'),
                             'user_id')

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_create_user_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         create_user(Exception,
                                     'test_user',
                                     'password',
                                     'email',
                                     'tenant_id'),
                         None)
        self.assertTrue(mock_logger_error.called)

    def test_add_role_user_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=True):
            self.assertTrue(openstack_utils.
                            add_role_user(self.keystone_client,
                                          'user_id',
                                          'role_id',
                                          'tenant_id'))

        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=False):
            self.assertTrue(openstack_utils.
                            add_role_user(self.keystone_client,
                                          'user_id',
                                          'role_id',
                                          'tenant_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_add_role_user_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         add_role_user(Exception,
                                       'user_id',
                                       'role_id',
                                       'tenant_id'))
        self.assertTrue(mock_logger_error.called)

    def test_delete_tenant_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=True):
            self.assertTrue(openstack_utils.
                            delete_tenant(self.keystone_client,
                                          'tenant_id'))

        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=False):
            self.assertTrue(openstack_utils.
                            delete_tenant(self.keystone_client,
                                          'tenant_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_tenant_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         delete_tenant(Exception,
                                       'tenant_id'))
        self.assertTrue(mock_logger_error.called)

    def test_delete_user_default(self):
        self.assertTrue(openstack_utils.
                        delete_user(self.keystone_client,
                                    'user_id'))

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_delete_user_exception(self, mock_logger_error):
        self.assertFalse(openstack_utils.
                         delete_user(Exception,
                                     'user_id'))
        self.assertTrue(mock_logger_error.called)

    def test_get_resource_default(self):
        with mock.patch('functest.utils.openstack_utils.'
                        'is_keystone_v3', return_value=True):
            self.assertEqual(openstack_utils.
                             get_resource(self.heat_client,
                                          'stack_id',
                                          'resource'),
                             self.resource)

    @mock.patch('functest.utils.openstack_utils.logger.error')
    def test_get_resource_exception(self, mock_logger_error):
        self.assertEqual(openstack_utils.
                         get_resource(Exception,
                                      'stack_id',
                                      'resource'),
                         None)
        self.assertTrue(mock_logger_error.called)


if __name__ == "__main__":
    unittest.main(verbosity=2)
