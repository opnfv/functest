#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Test module for orchestra_openims"""

import logging
import unittest

import mock
from snaps.openstack.os_credentials import OSCreds

from functest.core import vnf
from functest.opnfv_tests.vnf.ims import orchestra_openims


class OrchestraOpenImsTesting(unittest.TestCase):
    """Test class for orchestra_openims"""
    def setUp(self):

        self.tenant = 'orchestra_openims'
        self.creds = {'username': 'mocked_username',
                      'password': 'mocked_password'}
        self.tenant_images = {
            'image1': 'mocked_image_url_1',
            'image2': 'mocked_image_url_2'
        }
        self.mano = {
            'name': 'openbaton',
            'version': '3.2.0',
            'object': 'foo',
            'requirements': {
                'flavor': {
                    'name': 'mocked_flavor',
                    'ram_min': 4096,
                    'disk': 5,
                    'vcpus': 2
                },
                'os_image': 'mocked_image'
            },
            'bootstrap': {
                'url': 'mocked_bootstrap_url',
                'config': {
                    'url': 'mocked_config_url'}
            },
            'gvnfm': {
                'userdata': {
                    'url': 'mocked_userdata_url'
                }
            },
            'credentials': {
                'username': 'mocked_username',
                'password': 'mocked_password'
            }
        }
        self.vnf = {
            'name': 'openims',
            'descriptor': {
                'url': 'mocked_descriptor_url'
            },
            'requirements': {
                'flavor': {
                    'name': 'mocked_flavor',
                    'ram_min': 2048,
                    'disk': 5,
                    'vcpus': 2}
            }
        }
        self.openims = {
            'scscf': {
                'ports': [3870, 6060]
            },
            'pcscf': {
                'ports': [4060]
            },
            'icscf': {
                'ports': [3869, 5060]
            },
            'fhoss': {
                'ports': [3868]
            },
            'bind9': {
                'ports': []
            }
        }
        with mock.patch('functest.opnfv_tests.vnf.ims.orchestra_openims.'
                        'os.makedirs'),\
            mock.patch('functest.opnfv_tests.vnf.ims.orchestra_openims.'
                       'get_config', return_value={
                           'orchestrator': self.mano,
                           'name': self.mano['name'],
                           'version': self.mano['version'],
                           'requirements': self.mano['requirements'],
                           'credentials': self.mano['credentials'],
                           'bootstrap': self.mano['bootstrap'],
                           'gvnfm': self.mano['gvnfm'],
                           'os_image':
                               self.mano['requirements']['os_image'],
                           'flavor':
                               self.mano['requirements']['flavor'],
                           'url': self.mano['bootstrap']['url'],
                           'config': self.mano['bootstrap']['config'],
                           'tenant_images': self.tenant_images,
                           'vnf': self.vnf,
                           'orchestra_openims': self.openims}):
            self.ims_vnf = orchestra_openims.OpenImsVnf()

        self.details = {'orchestrator': {'status': 'PASS', 'duration': 120},
                        'vnf': {},
                        'test_vnf': {}}

    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                return_value=True)
    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
                return_value=True)
    @mock.patch('functest.core.vnf.os_utils.get_credentials',
                return_value={'auth_url': 'test/v1'})
    @mock.patch(
        'functest.utils.openstack_utils.get_tenant_id',
        return_value={'mocked_tenant_id'})
    @mock.patch(
        'functest.utils.openstack_utils.get_floating_ips',
        return_value=[])
    @mock.patch('snaps.openstack.create_image.OpenStackImage.create')
    @mock.patch('snaps.openstack.create_flavor.OpenStackFlavor.create')
    @mock.patch(
        'snaps.openstack.create_security_group.OpenStackSecurityGroup.create')
    @mock.patch('snaps.openstack.create_network.OpenStackNetwork.create')
    @mock.patch('snaps.openstack.create_router.OpenStackRouter.create')
    @mock.patch(
        'functest.opnfv_tests.openstack.snaps.snaps_utils.get_ext_net_name')
    @mock.patch(
        'functest.opnfv_tests.openstack.snaps.snaps_utils.'
        'neutron_utils.create_floating_ip')
    def test_prepare_default(self, *args):
        """Testing prepare function without any exceptions expected"""
        self.assertIsNone(self.ims_vnf.prepare())
        args[4].assert_called_once_with()

    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                return_value=True)
    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
                return_value=True)
    @mock.patch('functest.core.vnf.os_utils.get_credentials',
                return_value={'auth_url': 'test/no_v'})
    @mock.patch('snaps.openstack.create_image.OpenStackImage.create')
    def test_prepare_bad_auth_url(self, *args):
        """Testing prepare function with bad auth url"""
        with self.assertRaises(Exception):
            self.ims_vnf.image_creator(
                OSCreds(username='user', password='pass', auth_url='url',
                        project_name='project', identity_api_version=3),
                mock.Mock())
            args[0].assert_not_called()

    def test_prepare_missing_param(self):
        """Testing prepare function with missing param"""
        with self.assertRaises(vnf.VnfPreparationException):
            self.ims_vnf.prepare()

    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                side_effect=Exception)
    def test_prepare_keystone_exception(self, *args):
        """Testing prepare function with keystone exception"""
        with self.assertRaises(vnf.VnfPreparationException):
            self.ims_vnf.prepare()
        args[0].assert_called_once_with()

    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                side_effect=Exception)
    def test_prepare_tenant_exception(self, *args):
        """Testing prepare function with tenant exception"""
        with self.assertRaises(vnf.VnfPreparationException):
            self.ims_vnf.prepare()
        args[1].assert_called_once_with()

    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                return_value=True)
    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
                side_effect=Exception)
    def test_prepare_user_exception(self, *args):
        """Testing prepare function with user exception"""
        with self.assertRaises(vnf.VnfPreparationException):
            self.ims_vnf.prepare()
        args[2].assert_called_once_with()

    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                return_value=True)
    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
                return_value=True)
    @mock.patch('functest.core.vnf.os_utils.get_credentials',
                side_effect=Exception)
    def test_prepare_credentials_exception(self, *args):
        """Testing prepare function with credentials exception"""
        with self.assertRaises(vnf.VnfPreparationException):
            self.ims_vnf.prepare()
        args[0].assert_called_once_with()

    # # @mock.patch('functest.opnfv_tests.
        # vnf.ims.orchestra_openims.get_userdata')
    # def test_deploy_orchestrator(self, *args):
    #     floating_ip = FloatingIp
    #     floating_ip.ip = 'mocked_ip'
    #     details = {'fip':floating_ip,'flavor':{'name':'mocked_name'}}
    #     self.mano['details'] = details
    #     with mock.patch.dict(self.mano, {'details':
    #     {'fip':floating_ip,'flavor':{'name':'mocked_name'}}}):
    #     # with mock.patch.dict(self.mano, details):
    #         orchestra_openims.get_userdata(self.mano)
    #     self.assertIsNone(self.ims_vnf.deploy_orchestrator())
    #     args[4].assert_called_once_with()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
