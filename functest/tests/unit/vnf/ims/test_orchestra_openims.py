#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Test module for orchestra_openims"""

import logging
import unittest

import mock

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

    def test_prepare_missing_param(self):
        """Testing prepare function with missing param"""
        with self.assertRaises(vnf.VnfPreparationException):
            self.ims_vnf.prepare()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
