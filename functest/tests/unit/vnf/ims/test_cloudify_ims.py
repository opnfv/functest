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

    @mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                'os.makedirs')
    @mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                'get_config')
    def setUp(self):
        self.neutron_client = mock.Mock()
        self.glance_client = mock.Mock()
        self.keystone_client = mock.Mock()
        self.nova_client = mock.Mock()
        self.orchestrator = {'name': 'cloudify',
                             'version': '4.0',
                             'requirements': {'flavor': {'name': 'm1.medium',
                                                         'ram_min': 4096},
                                              'os_image': 'manager_4.0'
                                              }
                             }

        self.vnf = {'name': 'clearwater',
                    'version': '107',
                    'descriptor': {
                        'file_name': 'openstack-blueprint.yaml',
                        'name': 'clearwater-opnfv',
                        'url': 'https://foo',
                        'version': '107',
                        'requirements': {'flavor': {'name': 'm1.medium',
                                                    'ram_min': 2048}
                                         }
                        }
                    }

        self.images = {'image1': 'url1',
                       'image2': 'url2'}

        self.ims_vnf = cloudify_ims.CloudifyIms()

    #   def test_init(self):
    #   def test_init_no_config_file(self):
    #   def test_init_bad_path_config_file(self):
    #   def test_init_orchestrator_not_found(self):
    #   def test_init_vnf_not_found(self):
    #   def test_init_vnf_test_suite_not_found(self):
    #   def test_init_images_not_found(self):
    #
    #   def test_prepare(self):
    #   def test_prepare_bad_image_link(self):
    #   def test_prepare_get_image_fail(self):
    #   def test_prepare_download_error(self):
    #   def test_prepare_get_tenant_error(self):
    #   def test_prepare_update_quota_error(self):
    #
    #   def test_deploy_orchestrator(self):
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
