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


class CloudifyVrouterTesting(unittest.TestCase):

    @mock.patch('functest.opnfv_tests.vnf.router.cloudify_vrouter.Utilvnf')
    @mock.patch('functest.opnfv_tests.vnf.router.cloudify_vrouter.vrouter_base'
                '.Utilvnf')
    @mock.patch('os.makedirs')
    def setUp(self, *args):

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

    def test_prepare_missing_param(self):
        with self.assertRaises(vnf.VnfPreparationException):
            self.router_vnf.prepare()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
