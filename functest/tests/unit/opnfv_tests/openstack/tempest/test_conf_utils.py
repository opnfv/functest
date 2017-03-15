#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.opnfv_tests.openstack.tempest import conf_utils
from functest.utils.constants import CONST


class OSTempestConfUtilsTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def test_create_tempest_resources_missing_network_dic(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                        'os_utils.get_keystone_client',
                        return_value=mock.Mock()), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.create_tenant',
                       return_value='test_tenant_id'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.create_user',
                       return_value='test_user_id'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.create_shared_network_full',
                       return_value=None), \
                self.assertRaises(Exception) as context:
            conf_utils.create_tempest_resources()
            msg = 'Failed to create private network'
            self.assertTrue(msg in context)

    def test_create_tempest_resources_missing_image(self):
        CONST.tempest_use_custom_images = 'test_image'
        with mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                        'os_utils.get_keystone_client',
                        return_value=mock.Mock()), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.create_tenant',
                       return_value='test_tenant_id'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.create_user',
                       return_value='test_user_id'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.create_shared_network_full',
                       return_value=mock.Mock()), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.get_or_create_image',
                       return_value=(mock.Mock(), None)), \
                self.assertRaises(Exception) as context:
            conf_utils.create_tempest_resources()
            msg = 'Failed to create image'
            self.assertTrue(msg in context)

    def test_create_tempest_resources_missing_flavor(self):
        CONST.tempest_use_custom_images = 'test_image'
        CONST.tempest_use_custom_flavors = 'test_flavour'
        with mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                        'os_utils.get_keystone_client',
                        return_value=mock.Mock()), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.create_tenant',
                       return_value='test_tenant_id'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.create_user',
                       return_value='test_user_id'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.create_shared_network_full',
                       return_value=mock.Mock()), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.get_or_create_image',
                       return_value=(mock.Mock(), 'image_id')), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'os_utils.get_or_create_flavor',
                       return_value=(mock.Mock(), None)), \
                self.assertRaises(Exception) as context:
            conf_utils.create_tempest_resources()
            msg = 'Failed to create flavor'
            self.assertTrue(msg in context)

    def test_get_verifier_id_missing_verifier(self):
        CONST.tempest_deployment_name = 'test_deploy_name'
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.subprocess.Popen') as mock_popen, \
                self.assertRaises(Exception):
            mock_stdout = mock.Mock()
            attrs = {'stdout.readline.return_value': ''}
            mock_stdout.configure_mock(**attrs)
            mock_popen.return_value = mock_stdout
            conf_utils.get_verifier_id(),

    def test_get_verifier_id_default(self):
        CONST.tempest_deployment_name = 'test_deploy_name'
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.subprocess.Popen') as mock_popen:
            mock_stdout = mock.Mock()
            attrs = {'stdout.readline.return_value': 'test_deploy_id'}
            mock_stdout.configure_mock(**attrs)
            mock_popen.return_value = mock_stdout

            self.assertEqual(conf_utils.get_verifier_id(),
                             'test_deploy_id')

    def test_get_verifier_deployment_id_missing_rally(self):
        CONST.rally_deployment_name = 'test_rally_deploy_name'
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.subprocess.Popen') as mock_popen, \
                self.assertRaises(Exception):
            mock_stdout = mock.Mock()
            attrs = {'stdout.readline.return_value': ''}
            mock_stdout.configure_mock(**attrs)
            mock_popen.return_value = mock_stdout
            conf_utils.get_verifier_deployment_id(),

    def test_get_verifier_deployment_id_default(self):
        CONST.rally_deployment_name = 'test_rally_deploy_name'
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.subprocess.Popen') as mock_popen:
            mock_stdout = mock.Mock()
            attrs = {'stdout.readline.return_value': 'test_deploy_id'}
            mock_stdout.configure_mock(**attrs)
            mock_popen.return_value = mock_stdout

            self.assertEqual(conf_utils.get_verifier_deployment_id(),
                             'test_deploy_id')

    def test_get_verifier_repo_dir_default(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.os.path.join',
                        return_value='test_verifier_repo_dir'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.get_verifier_id') as m:
            self.assertEqual(conf_utils.get_verifier_repo_dir(''),
                             'test_verifier_repo_dir')
            self.assertTrue(m.called)

    def test_get_verifier_deployment_dir_default(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.os.path.join',
                        return_value='test_verifier_repo_dir'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.get_verifier_id') as m1, \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.get_verifier_deployment_id') as m2:
            self.assertEqual(conf_utils.get_verifier_deployment_dir('', ''),
                             'test_verifier_repo_dir')
            self.assertTrue(m1.called)
            self.assertTrue(m2.called)


if __name__ == "__main__":
    unittest.main(verbosity=2)
