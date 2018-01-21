#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock

from functest.core import vnf
from functest.opnfv_tests.vnf.ims import cloudify_ims


class CloudifyImsTesting(unittest.TestCase):

    def setUp(self):

        self.tenant = 'cloudify_ims'
        self.creds = {'username': 'user',
                      'password': 'pwd'}
        self.orchestrator = {'name': 'cloudify',
                             'version': '4.0',
                             'object': 'foo',
                             'requirements': {'flavor': {'name': 'm1.medium',
                                                         'ram_min': 4096},
                                              'os_image': 'manager_4.0'}}

        self.vnf = {'name': 'clearwater',
                    'descriptor': {'version': '108',
                                   'file_name': 'openstack-blueprint.yaml',
                                   'name': 'clearwater-opnfv',
                                   'url': 'https://foo',
                                   'requirements': {'flavor':
                                                    {'name': 'm1.medium',
                                                     'ram_min': 2048}}}}

        with mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                        'os.makedirs'), \
            mock.patch('functest.opnfv_tests.vnf.ims.cloudify_ims.'
                       'get_config', return_value={
                           'tenant_images': 'foo',
                           'orchestrator': self.orchestrator,
                           'vnf': self.vnf,
                           'vnf_test_suite': '',
                           'version': 'whatever'}):

            self.ims_vnf = cloudify_ims.CloudifyIms()

        self.images = {'image1': 'url1',
                       'image2': 'url2'}
        self.details = {'orchestrator': {'status': 'PASS', 'duration': 120},
                        'vnf': {},
                        'test_vnf':  {}}

    def test_prepare_missing_param(self):
        with self.assertRaises(vnf.VnfPreparationException):
            self.ims_vnf.prepare()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
