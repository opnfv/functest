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
            self.clearwater.deploy_vnf(self.bp),
            self.assertEqual(self.clearwater.deploy, True)

    def test_undeploy_vnf_deployment_passed(self):
        with mock.patch.object(self.clearwater.orchestrator,
                               'undeploy_deployment'):
            self.clearwater.deploy = True
            self.clearwater.undeploy_vnf(),
            self.assertEqual(self.clearwater.deploy, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
