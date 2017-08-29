#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.core import vnf
from functest.opnfv_tests.vnf.router import cloudify_vrouter

from snaps.openstack.os_credentials import OSCreds


class CloudifyVrouterTesting(unittest.TestCase):

    def setUp(self):

        self.tenant = 'cloudify_vrouter'
        self.creds = {'username': 'user',
                      'password': 'pwd'}
        self.orchestrator = {'name': 'cloudify',
                             'version': '4.0',
                             'object': 'foo',
                             'requirements': {'flavor': {'name': 'm1.medium',
                                                         'ram_min': 4096},
                                              'os_image': 'manager_4.0'}}

        self.vnf = {'name': 'vrouter',
                    'descriptor': {'version': '100',
                                   'file_name': 'function-test-' +
                                                'openstack-blueprint.yaml',
                                   'name': 'vrouter-opnfv',
                                   'url': 'https://foo',
                                   'requirements': {'flavor':
                                                    {'name': 'm1.medium',
                                                     'ram_min': 2048}}}}

        with mock.patch('functest.opnfv_tests.vnf.router.cloudify_vrouter.'
                        'os.makedirs'), \
            mock.patch('functest.opnfv_tests.vnf.router.cloudify_vrouter.'
                       'get_config', return_value={
                           'tenant_images': 'foo',
                           'orchestrator': self.orchestrator,
                           'vnf': self.vnf,
                           'vnf_test_suite': '',
                           'version': 'whatever'}):

            self.router_vnf = cloudify_vrouter.CloudifyVrouter()

        self.images = {'image1': 'url1',
                       'image2': 'url2'}
        self.details = {'orchestrator': {'status': 'PASS', 'duration': 120},
                        'vnf': {},
                        'test_vnf':  {}}

    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                return_value=True)
    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
                return_value=True)
    @mock.patch('functest.core.vnf.os_utils.get_credentials',
                return_value={'auth_url': 'test/v1'})
    @mock.patch('snaps.openstack.create_image.OpenStackImage.create')
    def test_prepare_default(self, *args):
        self.assertIsNone(self.router_vnf.prepare())
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
        with self.assertRaises(Exception):
            self.router_vnf.image_creator(
                OSCreds(username='user', password='pass', auth_url='url',
                        project_name='project', identity_api_version=3),
                mock.Mock())
            args[0].assert_not_called()

    def test_prepare_missing_param(self):
        with self.assertRaises(vnf.VnfPreparationException):
            self.router_vnf.prepare()

    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                side_effect=Exception)
    def test_prepare_keystone_exception(self, *args):
        with self.assertRaises(vnf.VnfPreparationException):
            self.router_vnf.prepare()
        args[0].assert_called_once_with()

    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                side_effect=Exception)
    def test_prepare_tenant_exception(self, *args):
        with self.assertRaises(vnf.VnfPreparationException):
            self.router_vnf.prepare()
        args[1].assert_called_once_with()

    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                return_value=True)
    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
                side_effect=Exception)
    def test_prepare_user_exception(self, *args):
        with self.assertRaises(vnf.VnfPreparationException):
            self.router_vnf.prepare()
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
        with self.assertRaises(vnf.VnfPreparationException):
            self.router_vnf.prepare()
        args[0].assert_called_once_with()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
