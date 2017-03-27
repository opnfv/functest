#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import subprocess32 as subprocess
import unittest

import mock

from functest.opnfv_tests.vnf.ims import orchestrator_cloudify


class ImsVnfTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.orchestrator = orchestrator_cloudify.Orchestrator('test_dir')
        self.bp = {'file_name': 'test_file',
                   'destination_folder': 'test_folder',
                   'url': 'test_url',
                   'branch': 'test_branch'}

    def test_download_manager_blueprint_download_blueprint_failed(self):
        self.orchestrator.manager_blueprint = False
        with mock.patch.object(self.orchestrator, '_download_blueprints',
                               return_value=False), \
            mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                       'exit') as mock_exit:
            self.orchestrator.download_manager_blueprint('test_url',
                                                         'test_branch')
            mock_exit.assert_any_call(-1)

    def test_download_manager_blueprint_download_blueprint_passed(self):
        self.orchestrator.manager_blueprint = False
        with mock.patch.object(self.orchestrator, '_download_blueprints',
                               return_value=True):
            self.orchestrator.download_manager_blueprint('test_url',
                                                         'test_branch')
            self.assertEqual(self.orchestrator.manager_blueprint,
                             True)

    def test_deploy_manager_failed(self):
        self.orchestrator.manager_blueprint = True
        with mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                       'os.remove'), \
            mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                       'execute_command', return_value='error'):
            self.assertEqual(self.orchestrator.deploy_manager(),
                             'error')
            self.assertEqual(self.orchestrator.manager_up,
                             False)

    def test_deploy_manager_passed(self):
        self.orchestrator.manager_blueprint = True
        with mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                       'os.remove'), \
            mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                       'execute_command', return_value=''):
            self.orchestrator.deploy_manager()
            self.assertEqual(self.orchestrator.manager_up,
                             True)

    def test_undeploy_manager_passed(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                        'execute_command', return_value=''):
            self.orchestrator.deploy_manager()
            self.assertEqual(self.orchestrator.manager_up,
                             False)

    def test_dwnld_upload_and_depl_blueprint_dwnld_blueprint_failed(self):
        with mock.patch.object(self.orchestrator, '_download_blueprints',
                               return_value=False), \
            mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                       'exit', side_effect=Exception) as mock_exit, \
                self.assertRaises(Exception):
            self.orchestrator.download_upload_and_deploy_blueprint(self.bp,
                                                                   'cfig',
                                                                   'bpn',
                                                                   'dpn')
            mock_exit.assert_any_call(-1)

    def test_dwnld_upload_and_depl_blueprint_failed(self):
        with mock.patch.object(self.orchestrator, '_download_blueprints',
                               return_value=True), \
            mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                       'execute_command', return_value='error'):
            r = self.orchestrator.download_upload_and_deploy_blueprint(self.bp,
                                                                       'cfig',
                                                                       'bpn',
                                                                       'dpn')
            self.assertEqual(r, 'error')

    def test__download_blueprints_failed(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                        'shutil.rmtree'), \
            mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                       'Repo.clone_from', side_effect=Exception):
            self.assertEqual(self.orchestrator._download_blueprints('bp_url',
                                                                    'branch',
                                                                    'dest'),
                             False)

    def test__download_blueprints_passed(self):
        with mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                        'shutil.rmtree'), \
            mock.patch('functest.opnfv_tests.vnf.ims.orchestrator_cloudify.'
                       'Repo.clone_from'):
            self.assertEqual(self.orchestrator._download_blueprints('bp_url',
                                                                    'branch',
                                                                    'dest'),
                             True)

    def test_execute_command_failed(self):
        with mock.patch('__builtin__.open',
                        mock.mock_open(read_data='test_data\n')):
            subprocess.call = mock.create_autospec(subprocess.call,
                                                   return_value=0)
            mock_log = mock.Mock()
            cmd = 'test_cmd -e test_env bash_script'
            ret = orchestrator_cloudify.execute_command(cmd, mock_log,
                                                        timeout=100)
            self.assertEqual(ret, False)

    def test_execute_command_default(self):
        with mock.patch('__builtin__.open',
                        mock.mock_open(read_data='test_data\n')):
            subprocess.call = mock. \
                create_autospec(subprocess.call,
                                return_value=subprocess.TimeoutExpired)
            mock_log = mock.Mock()
            cmd = 'test_cmd -e test_env bash_script'
            ret = orchestrator_cloudify.execute_command(cmd, mock_log,
                                                        timeout=100)
            self.assertEqual(ret, ['test_data\n'])

    def test_set_methods(self):
        self.orchestrator.set_credentials('test_username', 'test_password',
                                          'test_tenant_name', 'test_auth_url')
        self.assertTrue(self.orchestrator.config['keystone_username'],
                        'test_username')
        self.assertTrue(self.orchestrator.config['keystone_password'],
                        'test_password')
        self.assertTrue(self.orchestrator.config['keystone_url'],
                        'test_auth_url')
        self.assertTrue(self.orchestrator.config['keystone_tenant_name'],
                        'test_tenant_name')
        self.orchestrator.set_flavor_id('test_flavor_id')
        self.assertTrue(self.orchestrator.config['flavor_id'],
                        'test_flavor_id')
        self.orchestrator.set_image_id('test_image_id')
        self.assertTrue(self.orchestrator.config['image_id'], 'test_image_id')
        self.orchestrator.set_external_network_name('test_network')
        self.assertTrue(self.orchestrator.config['external_network_name'],
                        'test_network')
        self.orchestrator.set_ssh_user('test_user')
        self.assertTrue(self.orchestrator.config['ssh_user'],
                        'test_user')
        self.orchestrator.set_nova_url('test_nova_url')
        self.assertTrue(self.orchestrator.config['nova_url'],
                        'test_nova_url')
        self.orchestrator.set_neutron_url('test_neutron_url')
        self.assertTrue(self.orchestrator.config['neutron_url'],
                        'test_neutron_url')
        self.orchestrator.set_nameservers(['test_subnet'])
        self.assertTrue(self.orchestrator.config['dns_subnet_1'],
                        'test_subnet')

if __name__ == "__main__":
    unittest.main(verbosity=2)