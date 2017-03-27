#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.opnfv_tests.vnf.ims import clearwater
from functest.opnfv_tests.vnf.ims import orchestrator_cloudify


class ClearwaterTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.clearwater = clearwater.Clearwater()
        self.orchestrator = orchestrator_cloudify.Orchestrator('test_dir')
        self.clearwater.orchestrator = self.orchestrator
        self.clearwater.dep_name = 'test_dep_name'
        self.bp = {'file_name': 'test_file',
                   'destination_folder': 'test_folder',
                   'url': 'test_url',
                   'branch': 'test_branch'}

    def test_deploy_vnf_blueprint_download_failed(self):
        with mock.patch.object(self.clearwater.orchestrator,
                               'download_upload_and_deploy_blueprint',
                               return_value='error'):
            self.assertEqual(self.clearwater.deploy_vnf(self.bp),
                             'error')

    def test_deploy_vnf_blueprint_download_passed(self):
        with mock.patch.object(self.clearwater.orchestrator,
                               'download_upload_and_deploy_blueprint',
                               return_value=''):
            self.clearwater.deploy_vnf(self.bp)
            self.assertEqual(self.clearwater.deploy, True)

    def test_undeploy_vnf_deployment_passed(self):
        with mock.patch.object(self.clearwater.orchestrator,
                               'undeploy_deployment'):
            self.clearwater.deploy = True
            self.clearwater.undeploy_vnf()
            self.assertEqual(self.clearwater.deploy, False)

    def test_undeploy_vnf_deployment_with_undeploy(self):
        with mock.patch.object(self.clearwater.orchestrator,
                               'undeploy_deployment') as m:
            self.clearwater.deploy = False
            self.clearwater.undeploy_vnf(),
            self.assertEqual(self.clearwater.deploy, False)
            self.assertFalse(m.called)

            self.clearwater.orchestrator = None
            self.clearwater.deploy = True
            self.clearwater.undeploy_vnf(),
            self.assertEqual(self.clearwater.deploy, True)

            self.clearwater.deploy = False
            self.clearwater.undeploy_vnf(),
            self.assertEqual(self.clearwater.deploy, False)

    def test_set_methods(self):
        self.clearwater.set_orchestrator(self.orchestrator)
        self.assertTrue(self.clearwater.orchestrator, self.orchestrator)
        self.clearwater.set_flavor_id('test_flavor_id')
        self.assertTrue(self.clearwater.config['flavor_id'], 'test_flavor_id')
        self.clearwater.set_image_id('test_image_id')
        self.assertTrue(self.clearwater.config['image_id'], 'test_image_id')
        self.clearwater.set_agent_user('test_user')
        self.assertTrue(self.clearwater.config['agent_user'], 'test_user')
        self.clearwater.set_external_network_name('test_network')
        self.assertTrue(self.clearwater.config['external_network_name'],
                        'test_network')
        self.clearwater.set_public_domain('test_domain')
        self.assertTrue(self.clearwater.config['public_domain'],
                        'test_domain')

if __name__ == "__main__":
    unittest.main(verbosity=2)
