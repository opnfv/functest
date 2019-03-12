#!/usr/bin/env python

# Copyright (c) 2017 Rebaca and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

""" Unit test testcase for JuJu EPC Implementation"""

import logging
import unittest

import mock

from functest.opnfv_tests.vnf.epc import juju_epc


class JujuEpcTesting(unittest.TestCase):
    # pylint: disable=missing-docstring
    """Unittest for ABoT EPC with juju orchestrator"""

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
                                              'dep_package': 'software-'
                                                             'properties'
                                                             '-common',
                                              'pip3_packages': 'juju-wait'}}
        self.vnf = {'name': 'juju_epc',
                    'descriptor': {'version': '1',
                                   'file_name': '/src/epc-test/'
                                                'abot_charm/'
                                                'functest-abot-'
                                                'epc-bundle/bundle.yaml',
                                   'name': 'abot-oai-epc',
                                   'requirements': {'flavor':
                                                    {'name': 'm1.medium',
                                                     'ram_min': 4096}}}}
        with mock.patch('functest.opnfv_tests.vnf.epc.juju_epc.os.makedirs'), \
            mock.patch('functest.opnfv_tests.vnf.epc.juju_epc.get_config',
                       return_value={'tenant_images': 'foo',
                                     'orchestrator': self.orchestrator,
                                     'vnf': self.vnf, 'vnf_test_suite': '',
                                     'version': 'whatever'}):
            self.epc_vnf = juju_epc.JujuEpc()

        self.images = {'image1': 'url1',
                       'image2': 'url2'}
        self.details = {'orchestrator': {'status': 'PASS', 'duration': 120},
                        'vnf': {},
                        'test_vnf':  {}}

    @unittest.skip("It must be fixed. Please see JIRA FUNCTEST-915")
    @mock.patch('os.system')
    def test_prepare_default(self, *args):
        """ Unittest for Prepare testcase """
        self.epc_vnf.orchestrator = self.orchestrator
        self.assertIsNone(self.epc_vnf.prepare())
        args[4].assert_called_once_with('test',
                                        'debayan',
                                        'OAI EPC deployed '
                                        'with Juju')


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
