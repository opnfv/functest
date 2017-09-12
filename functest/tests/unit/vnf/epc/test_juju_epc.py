#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.core import vnf
from functest.opnfv_tests.vnf.epc import juju_epc

from snaps.openstack.os_credentials import OSCreds


class JujuEpcTesting(unittest.TestCase):

    def setUp(self):

        self.tenant = 'juju_epc'
        self.creds = {'username': 'user',
                      'password': 'pwd'}
        self.orchestrator = {'name': 'juju',
                             'version': '2.0',
                             'object': 'foo',
                             'requirements': {'flavor': {'name': 'm1.small',
                                                         'ram_min': 2048},
                                              'pip': 'python3-pip',
                                              'repo_link': 'ppa:juju/stable',
                                              'dep_package': 'software-properties-common',
                                              'pip3_packages': 'juju-wait'}}
        

        self.vnf = {'name': 'juju_epc',
                    'descriptor': {'version': '1',
                                   'file_name': '/src/epc-test/abot_charm/functest-abot-epc-bundle/bundle.yaml',
                                   'name': 'abot-oai-epc',
                                   'requirements': {'flavor':
                                                    {'name': 'm1.medium',
                                                     'ram_min': 4096}}}}
        with mock.patch('functest.opnfv_tests.vnf.epc.juju_epc.'
                        'os.makedirs'), \
             mock.patch('functest.opnfv_tests.vnf.epc.juju_epc.'
                       'get_config', return_value={
                           'tenant_images': 'foo',
                           'orchestrator': self.orchestrator,
                           'vnf': self.vnf,
                           'vnf_test_suite': '',
                           'version': 'whatever'}), \
            mock.patch('functest.utils.openstack_utils.'
                        'get_keystone_client', return_value='test'), \
            mock.patch('functest.utils.openstack_utils.'
                        'get_glance_client', return_value='test'), \
            mock.patch('functest.utils.openstack_utils.'
                        'get_neutron_client', return_value='test'), \
            mock.patch('functest.utils.openstack_utils.'
                        'get_nova_client', return_value='test'):

            self.epc_vnf = juju_epc.JujuEpc()

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
                return_value={'auth_url': 'test/v1',
                              'project_name': 'test_tenant'})
    @mock.patch('snaps.openstack.create_image.OpenStackImage.create')
    @mock.patch('os.system')
    def test_prepare_default(self, *args):
        self.epc_vnf.orchestrator = self.orchestrator
        self.assertIsNone(self.epc_vnf.prepare())
        args[4].assert_called_once_with('test', 'debayan', 'OAI EPC deployed with Juju')

#    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
#                return_value='test')
#    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
#                return_value=True)
#    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
#                return_value=True)
#    @mock.patch('functest.core.vnf.os_utils.get_credentials',
#                return_value={'auth_url': 'test/no_v'})
#    @mock.patch('snaps.openstack.create_image.OpenStackImage.create')
#    def test_prepare_bad_auth_url(self, *args):
#        with self.assertRaises(Exception):
#            self.epc_vnf.image_creator(
#                OSCreds(username='user', password='pass', auth_url='url',
#                        project_name='project', identity_api_version=3),
#                mock.Mock())
#            args[0].assert_not_called()

#    def test_prepare_missing_param(self):
#        with self.assertRaises(vnf.VnfPreparationException):
#            self.epc_vnf.prepare()

#    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
#                side_effect=Exception)
#    def test_prepare_keystone_exception(self, *args):
#        with self.assertRaises(vnf.VnfPreparationException):
#            self.epc_vnf.prepare()
#        args[0].assert_called_once_with()

#    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
#                return_value='test')
#    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
#                side_effect=Exception)
#    def test_prepare_tenant_exception(self, *args):
#        with self.assertRaises(vnf.VnfPreparationException):
#            self.epc_vnf.prepare()
#        args[1].assert_called_once_with()

#    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
#                return_value='test')
#    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
#                return_value=True)
#    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
#                side_effect=Exception)
#    def test_prepare_user_exception(self, *args):
#        with self.assertRaises(vnf.VnfPreparationException):
#            self.epc_vnf.prepare()
#        args[2].assert_called_once_with()

#    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
#                return_value='test')
#    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
#                return_value=True)
#    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
#                return_value=True)
#    @mock.patch('functest.core.vnf.os_utils.get_credentials',
#                side_effect=Exception)
#    def test_prepare_credentials_exception(self, *args):
#        with self.assertRaises(vnf.VnfPreparationException):
#            self.epc_vnf.prepare()
#        args[0].assert_called_once_with()

    # @mock.patch('snaps.openstack.create_keypairs.OpenStackKeypair',
    #             side_effect=Exception)
    # def test_deploy_orchestrator_keypair_exception(self, *args):
    #    with self.assertRaises(vnf.OrchestratorDeploymentException):
    #        self.epc_vnf.deploy_orchestrator()

    #   def test_deploy_orchestrator_network_creation_fail(self):
    #   def test_deploy_orchestrator_floatting_ip_creation_fail(self):
    #   def test_deploy_orchestrator_flavor_fail(self):
    #   def test_deploy_orchestrator_get_image_id_fail(self):
    #   def test_deploy_orchestrator_create_instance_fail(self):
    #   def test_deploy_orchestrator_secgroup_fail(self):
    #   def test_deploy_orchestrator_add_floating_ip_fail(self):
    #   def test_deploy_orchestrator_get_endpoint_fail(self):
    #   def test_deploy_orchestrator_initiate CloudifyClient_fail(self):
    #   def test_deploy_orchestrator_get_status_fail(self):
    #

    #   def test_deploy_vnf(self):
    #   def test_deploy_vnf_publish_fail(self):
    #   def test_deploy_vnf_get_flavor_fail(self):
    #   def test_deploy_vnf_get_external_net_fail(self):
    #   def test_deploy_vnf_deployment_create_fail(self):
    #   def test_deploy_vnf_start_fail(self):
    #
    #   def test_test_vnf(self):
    #   def test_test_vnf_deployment_get_fail(self):
    #   def test_test_vnf_run_live_test_fail(self):
    #
    #   def test_clean(self):
    #   def test_clean_execution_start_fail(self):
    #   def test_clean_deployment_delete_fail(self):
    #   def test_clean_blueprint_delete_fail(self):


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
