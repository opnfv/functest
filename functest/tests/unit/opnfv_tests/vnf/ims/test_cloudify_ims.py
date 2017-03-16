#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.opnfv_tests.vnf.ims import cloudify_ims


class CloudifyImsTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os.makedirs'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'get_config', return_value='config_value'):
            self.ims_vnf = cloudify_ims.CloudifyIms()
        self.neutron_client = mock.Mock()
        self.glance_client = mock.Mock()
        self.keystone_client = mock.Mock()
        self.nova_client = mock.Mock()
        self.orchestrator = {'requirements': {'ram_min': 2,
                                              'os_image': 'test_os_image'},
                             'blueprint': {'url': 'test_url',
                                           'branch': 'test_branch'},
                             'inputs': {'public_domain': 'test_domain'},
                             'object': 'test_object',
                             'deployment_name': 'test_deployment_name'}
        self.ims_vnf.orchestrator = self.orchestrator
        self.ims_vnf.images = {'test_image': 'test_url'}
        self.ims_vnf.vnf = self.orchestrator
        self.ims_vnf.tenant_name = 'test_tenant'
        self.ims_vnf.inputs = {'public_domain': 'test_domain'}
        self.ims_vnf.glance_client = self.glance_client
        self.ims_vnf.neutron_client = self.neutron_client
        self.ims_vnf.keystone_client = self.keystone_client
        self.ims_vnf.nova_client = self.nova_client
        self.ims_vnf.admin_creds = 'test_creds'

        self.mock_post = mock.Mock()
        attrs = {'status_code': 201,
                 'cookies': ""}
        self.mock_post.configure_mock(**attrs)

        self.mock_post_200 = mock.Mock()
        attrs = {'status_code': 200,
                 'cookies': ""}
        self.mock_post_200.configure_mock(**attrs)

    def test_deploy_orchestrator_missing_image(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os_utils.get_neutron_client',
                        return_value=self.neutron_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_glance_client',
                       return_value=self.glance_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_keystone_client',
                       return_value=self.keystone_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_nova_client',
                       return_value=self.nova_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       return_value=''), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'download_and_add_image_on_glance') as m, \
                self.assertRaises(Exception) as context:
            self.ims_vnf.deploy_orchestrator()
            self.assertTrue(m.called)
            msg = "Failed to find or upload required OS "
            msg += "image for this deployment"
            self.assertTrue(msg in context.exception)

    def test_deploy_orchestrator_extend_quota_fail(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os_utils.get_neutron_client',
                        return_value=self.neutron_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_glance_client',
                       return_value=self.glance_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_keystone_client',
                       return_value=self.keystone_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_nova_client',
                       return_value=self.nova_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       return_value='image_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_tenant_id',
                       return_value='tenant_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.update_sg_quota',
                       return_value=False), \
                self.assertRaises(Exception) as context:
            self.ims_vnf.deploy_orchestrator()
            msg = "Failed to update security group quota"
            msg += " for tenant test_tenant"
            self.assertTrue(msg in context.exception)

    def _get_image_id(self, client, name):
        if name == 'test_image':
            return 'image_id'
        else:
            return ''

    def test_deploy_orchestrator_missing_flavor(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os_utils.get_neutron_client',
                        return_value=self.neutron_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_glance_client',
                       return_value=self.glance_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_keystone_client',
                       return_value=self.keystone_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_nova_client',
                       return_value=self.nova_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       side_effect=self._get_image_id), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_tenant_id',
                       return_value='tenant_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.update_sg_quota',
                       return_value=True), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_endpoint',
                       return_value='public_auth_url'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'Orchestrator', return_value=mock.Mock()) as m, \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_or_create_flavor',
                       return_value=(False, '')), \
                self.assertRaises(Exception) as context:
            self.ims_vnf.deploy_orchestrator()
            self.assertTrue(m.set_credentials.called)
            msg = "Failed to find required flavorfor this deployment"
            self.assertTrue(msg in context.exception)

    def test_deploy_orchestrator_missing_os_image(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os_utils.get_neutron_client',
                        return_value=self.neutron_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_glance_client',
                       return_value=self.glance_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_keystone_client',
                       return_value=self.keystone_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_nova_client',
                       return_value=self.nova_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       side_effect=self._get_image_id), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_tenant_id',
                       return_value='tenant_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.update_sg_quota',
                       return_value=True), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_endpoint',
                       return_value='public_auth_url'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'Orchestrator', return_value=mock.Mock()) as m, \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_or_create_flavor',
                       return_value=(True, 'flavor_id')), \
                self.assertRaises(Exception) as context:
            self.ims_vnf.deploy_orchestrator()
            self.assertTrue(m.set_credentials.called)
            self.assertTrue(m.set_flavor_id.called)
            msg = "Failed to find required OS image for cloudify manager"
            self.assertTrue(msg in context.exception)

    def test_deploy_orchestrator_get_ext_network_fail(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os_utils.get_neutron_client',
                        return_value=self.neutron_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_glance_client',
                       return_value=self.glance_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_keystone_client',
                       return_value=self.keystone_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_nova_client',
                       return_value=self.nova_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       return_value='image_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_tenant_id',
                       return_value='tenant_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.update_sg_quota',
                       return_value=True), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_endpoint',
                       return_value='public_auth_url'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'Orchestrator', return_value=mock.Mock()) as m, \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_or_create_flavor',
                       return_value=(True, 'flavor_id')), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_external_net',
                       return_value=''), \
                self.assertRaises(Exception) as context:
            self.ims_vnf.deploy_orchestrator()
            self.assertTrue(m.set_credentials.called)
            self.assertTrue(m.set_flavor_id.called)
            self.assertTrue(m.set_image_id.called)
            msg = "Failed to get external network"
            self.assertTrue(msg in context.exception)

    def test_deploy_orchestrator_with_error(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os_utils.get_neutron_client',
                        return_value=self.neutron_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_glance_client',
                       return_value=self.glance_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_keystone_client',
                       return_value=self.keystone_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_nova_client',
                       return_value=self.nova_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       return_value='image_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_tenant_id',
                       return_value='tenant_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.update_sg_quota',
                       return_value=True), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_endpoint',
                       return_value='public_auth_url'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'Orchestrator') as m, \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_or_create_flavor',
                       return_value=(True, 'flavor_id')), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_external_net',
                       return_value='ext_net'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'ft_utils.get_resolvconf_ns',
                       return_value=True), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'ft_utils.execute_command'):
            mock_obj = mock.Mock()
            attrs = {'deploy_manager.return_value': 'error'}
            mock_obj.configure_mock(**attrs)

            m.return_value = mock_obj

            self.assertEqual(self.ims_vnf.deploy_orchestrator(),
                             {'status': 'FAIL', 'result': 'error'})

    def test_deploy_orchestrator_default(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os_utils.get_neutron_client',
                        return_value=self.neutron_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_glance_client',
                       return_value=self.glance_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_keystone_client',
                       return_value=self.keystone_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_nova_client',
                       return_value=self.nova_client), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       return_value='image_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_tenant_id',
                       return_value='tenant_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.update_sg_quota',
                       return_value=True), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_endpoint',
                       return_value='public_auth_url'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'Orchestrator') as m, \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_or_create_flavor',
                       return_value=(True, 'flavor_id')), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_external_net',
                       return_value='ext_net'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'ft_utils.get_resolvconf_ns',
                       return_value=True), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'ft_utils.execute_command'):
            mock_obj = mock.Mock()
            attrs = {'deploy_manager.return_value': ''}
            mock_obj.configure_mock(**attrs)

            m.return_value = mock_obj

            self.assertEqual(self.ims_vnf.deploy_orchestrator(),
                             {'status': 'PASS', 'result': ''})

    def test_deploy_vnf_missing_flavor(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'Clearwater', return_value=mock.Mock()), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_or_create_flavor',
                       return_value=(False, '')), \
                self.assertRaises(Exception) as context:
            self.ims_vnf.deploy_vnf()
            msg = "Failed to find required flavor for this deployment"
            self.assertTrue(msg in context.exception)

    def test_deploy_vnf_missing_os_image(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'Clearwater', return_value=mock.Mock()) as m, \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_or_create_flavor',
                       return_value=(True, 'test_flavor')), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       return_value=''), \
                self.assertRaises(Exception) as context:
            self.ims_vnf.deploy_vnf()
            msg = "Failed to find required OS image"
            msg += " for clearwater VMs"
            self.assertTrue(msg in context.exception)
            self.assertTrue(m.set_flavor_id.called)

    def test_deploy_vnf_missing_get_ext_net(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'Clearwater', return_value=mock.Mock()) as m, \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_or_create_flavor',
                       return_value=(True, 'test_flavor')), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       return_value='image_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_external_net',
                       return_value=''), \
                self.assertRaises(Exception) as context:
            self.ims_vnf.deploy_vnf()
            msg = "Failed to get external network"
            self.assertTrue(msg in context.exception)
            self.assertTrue(m.set_flavor_id.called)
            self.assertTrue(m.set_image_id.called)

    def test_deploy_vnf_with_error(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'Clearwater') as m, \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_or_create_flavor',
                       return_value=(True, 'test_flavor')), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       return_value='image_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_external_net',
                       return_value='ext_net'):
            mock_obj = mock.Mock()
            attrs = {'deploy_vnf.return_value': 'error'}
            mock_obj.configure_mock(**attrs)

            m.return_value = mock_obj

            self.assertEqual(self.ims_vnf.deploy_vnf(),
                             {'status': 'FAIL', 'result': 'error'})

    def test_deploy_vnf_default(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'Clearwater') as m, \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_or_create_flavor',
                       return_value=(True, 'test_flavor')), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_image_id',
                       return_value='image_id'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.get_external_net',
                       return_value='ext_net'):
            mock_obj = mock.Mock()
            attrs = {'deploy_vnf.return_value': ''}
            mock_obj.configure_mock(**attrs)

            m.return_value = mock_obj

            self.assertEqual(self.ims_vnf.deploy_vnf(),
                             {'status': 'PASS', 'result': ''})

    def test_test_vnf_ip_retrieval_failure(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os.popen', side_effect=Exception), \
                self.assertRaises(Exception) as context:
            msg = "Unable to retrieve the IP of the "
            msg += "cloudify manager server !"
            self.ims_vnf.test_vnf()
            self.assertTrue(msg in context.exception)

    def test_test_vnf_create_number_failure(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os.popen') as m, \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'requests.get'), \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'requests.post',
                           return_value=self.mock_post), \
                self.assertRaises(Exception) as context:
            mock_obj = mock.Mock()
            attrs = {'read.return_value': 'test_ip\n'}
            mock_obj.configure_mock(**attrs)
            m.return_value = mock_obj

            self.ims_vnf.test_vnf()

            msg = "Unable to create a number:"
            self.assertTrue(msg in context.exception)

    def _get_post_status(self, url, cookies='', data=''):
        ellis_url = "http://test_ellis_ip/session"
        if url == ellis_url:
            return self.mock_post_200
        return self.mock_post

    def test_test_vnf_fail(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os.popen') as m, \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'requests.get') as mock_get, \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'requests.post',
                           side_effect=self._get_post_status), \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'ft_utils.get_resolvconf_ns'), \
                mock.patch('__builtin__.open', mock.mock_open()), \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'os.remove'), \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'json.load', return_value=''):
            mock_obj = mock.Mock()
            attrs = {'read.return_value': 'test_ip\n'}
            mock_obj.configure_mock(**attrs)
            m.return_value = mock_obj

            mock_obj2 = mock.Mock()
            attrs = {'json.return_value': {'outputs':
                                           {'dns_ip': 'test_dns_ip',
                                            'ellis_ip': 'test_ellis_ip'}}}
            mock_obj2.configure_mock(**attrs)
            mock_get.return_value = mock_obj2

            self.assertEqual(self.ims_vnf.test_vnf(),
                             {'status': 'FAIL', 'result': ''})

    def test_test_vnf_pass(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os.popen') as m, \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'requests.get') as mock_get, \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'requests.post',
                           side_effect=self._get_post_status), \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'ft_utils.get_resolvconf_ns'), \
                mock.patch('__builtin__.open', mock.mock_open()), \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'os.remove'), \
                mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                           'json.load', return_value='vims_test_result'):
            mock_obj = mock.Mock()
            attrs = {'read.return_value': 'test_ip\n'}
            mock_obj.configure_mock(**attrs)
            m.return_value = mock_obj

            mock_obj2 = mock.Mock()
            attrs = {'json.return_value': {'outputs':
                                           {'dns_ip': 'test_dns_ip',
                                            'ellis_ip': 'test_ellis_ip'}}}
            mock_obj2.configure_mock(**attrs)
            mock_get.return_value = mock_obj2

            self.assertEqual(self.ims_vnf.test_vnf(),
                             {'status': 'PASS', 'result': 'vims_test_result'})

    def test_download_and_add_image_on_glance_incorrect_url(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os.makedirs'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'ft_utils.download_url',
                       return_value=False):
            resp = cloudify_ims.download_and_add_image_on_glance(self.
                                                                 glance_client,
                                                                 'image_name',
                                                                 'http://url',
                                                                 'data_dir')
            self.assertEqual(resp, False)

    def test_download_and_add_image_on_glance_image_creation_failure(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os.makedirs'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'ft_utils.download_url',
                       return_value=True), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'os_utils.create_glance_image',
                       return_value=''):
            resp = cloudify_ims.download_and_add_image_on_glance(self.
                                                                 glance_client,
                                                                 'image_name',
                                                                 'http://url',
                                                                 'data_dir')
            self.assertEqual(resp, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
