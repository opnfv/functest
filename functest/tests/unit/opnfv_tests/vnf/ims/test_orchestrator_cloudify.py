#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.opnfv_tests.vnf.ims import orchestrator_cloudify


class OrchestratorImsTesting(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
