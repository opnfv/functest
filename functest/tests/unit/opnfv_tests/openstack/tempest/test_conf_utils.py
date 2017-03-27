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

            CONST.tempest_use_custom_images = True
            conf_utils.create_tempest_resources()
            msg = 'Failed to create image'
            self.assertTrue(msg in context)

            CONST.tempest_use_custom_images = False
            conf_utils.create_tempest_resources(use_custom_images=True)
            msg = 'Failed to create image'
            self.assertTrue(msg in context)

    def test_create_tempest_resources_missing_flavor(self):
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
            CONST.tempest_use_custom_images = True
            CONST.tempest_use_custom_flavors = True
            conf_utils.create_tempest_resources()
            msg = 'Failed to create flavor'
            self.assertTrue(msg in context)

            CONST.tempest_use_custom_images = True
            CONST.tempest_use_custom_flavors = False
            conf_utils.create_tempest_resources(use_custom_flavors=False)
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

    def test_get_repo_tag_default(self):
        mock_popen = mock.Mock()
        attrs = {'stdout.readline.return_value': 'test_tag'}
        mock_popen.configure_mock(**attrs)

        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.subprocess.Popen',
                        return_value=mock_popen):
            self.assertEqual(conf_utils.get_repo_tag('test_repo'),
                             'test_tag')

    def test_backup_tempest_config_default(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.os.path.exists',
                        return_value=False), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.os.makedirs') as m1, \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.shutil.copyfile') as m2:
            conf_utils.backup_tempest_config('test_conf_file')
            self.assertTrue(m1.called)
            self.assertTrue(m2.called)

        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.os.path.exists',
                        return_value=True), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.shutil.copyfile') as m2:
            conf_utils.backup_tempest_config('test_conf_file')
            self.assertTrue(m2.called)

    def test_configure_tempest_default(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.configure_verifier',
                        return_value='test_conf_file'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.configure_tempest_update_params') as m1, \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.configure_tempest_multisite_params') as m2:
            conf_utils.configure_tempest('test_dep_dir',
                                         MODE='feature_multisite')
            self.assertTrue(m1.called)
            self.assertTrue(m2.called)

        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.configure_verifier',
                        return_value='test_conf_file'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.configure_tempest_update_params') as m1:
            conf_utils.configure_tempest('test_dep_dir')
            self.assertTrue(m1.called)
            self.assertTrue(m2.called)

    def test_configure_tempest_defcore_default(self):
        img_flavor_dict = {'image_id': 'test_image_id',
                           'flavor_id': 'test_flavor_id',
                           'image_id_alt': 'test_image_alt_id',
                           'flavor_id_alt': 'test_flavor_alt_id'}
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.configure_verifier',
                        return_value='test_conf_file'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.configure_tempest_update_params'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ConfigParser.RawConfigParser.'
                       'set') as mset, \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ConfigParser.RawConfigParser.'
                       'read') as mread, \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ConfigParser.RawConfigParser.'
                       'write') as mwrite, \
            mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.shutil.copyfile'):
            CONST.dir_functest_test = 'test_dir'
            CONST.refstack_tempest_conf_path = 'test_path'
            conf_utils.configure_tempest_defcore('test_dep_dir',
                                                 img_flavor_dict)
            mset.assert_any_call('compute', 'image_ref', 'test_image_id')
            mset.assert_any_call('compute', 'image_ref_alt',
                                 'test_image_alt_id')
            mset.assert_any_call('compute', 'flavor_ref', 'test_flavor_id')
            mset.assert_any_call('compute', 'flavor_ref_alt',
                                 'test_flavor_alt_id')
            self.assertTrue(mread.called)
            self.assertTrue(mwrite.called)

    def _test_missing_param(self, params, image_id, flavor_id):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.ConfigParser.RawConfigParser.'
                        'set') as mset, \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ConfigParser.RawConfigParser.'
                       'read') as mread, \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ConfigParser.RawConfigParser.'
                       'write') as mwrite, \
            mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.backup_tempest_config'):
            CONST.dir_functest_test = 'test_dir'
            CONST.OS_ENDPOINT_TYPE = None
            conf_utils.\
                configure_tempest_update_params('test_conf_file',
                                                IMAGE_ID=image_id,
                                                FLAVOR_ID=flavor_id)
            mset.assert_any_call(params[0], params[1], params[2])
            self.assertTrue(mread.called)
            self.assertTrue(mwrite.called)

    def test_configure_tempest_update_params_missing_image_id(self):
            CONST.tempest_use_custom_images = True
            self._test_missing_param(('compute', 'image_ref',
                                      'test_image_id'), 'test_image_id',
                                     None)

    def test_configure_tempest_update_params_missing_image_id_alt(self):
            CONST.tempest_use_custom_images = True
            conf_utils.IMAGE_ID_ALT = 'test_image_id_alt'
            self._test_missing_param(('compute', 'image_ref_alt',
                                      'test_image_id_alt'), None, None)

    def test_configure_tempest_update_params_missing_flavor_id(self):
            CONST.tempest_use_custom_flavors = True
            self._test_missing_param(('compute', 'flavor_ref',
                                      'test_flavor_id'), None,
                                     'test_flavor_id')

    def test_configure_tempest_update_params_missing_flavor_id_alt(self):
            CONST.tempest_use_custom_flavors = True
            conf_utils.FLAVOR_ID_ALT = 'test_flavor_id_alt'
            self._test_missing_param(('compute', 'flavor_ref_alt',
                                      'test_flavor_id_alt'), None,
                                     None)

    def test_configure_verifier_missing_temp_conf_file(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.os.path.isfile',
                        return_value=False), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ft_utils.execute_command') as mexe, \
                self.assertRaises(Exception) as context:
            conf_utils.configure_verifier('test_dep_dir')
            mexe.assert_any_call("rally verify configure-verifier")
            msg = ("Tempest configuration file 'test_dep_dir/tempest.conf'"
                   " NOT found.")
            self.assertTrue(msg in context)

    def test_configure_verifier_default(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.os.path.isfile',
                        return_value=True), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ft_utils.execute_command') as mexe:
            self.assertEqual(conf_utils.configure_verifier('test_dep_dir'),
                             'test_dep_dir/tempest.conf')
            mexe.assert_any_call("rally verify configure-verifier "
                                 "--reconfigure")

    def test_configure_tempest_multisite_params_without_fuel(self):
        conf_utils.CI_INSTALLER_TYPE = 'not_fuel'
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.os_utils.get_endpoint',
                        return_value='kingbird_endpoint_url'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ConfigParser.RawConfigParser.'
                       'set') as mset, \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ConfigParser.RawConfigParser.'
                       'read') as mread, \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ConfigParser.RawConfigParser.'
                       'add_section') as msection, \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ConfigParser.RawConfigParser.'
                       'write') as mwrite, \
            mock.patch('__builtin__.open', mock.mock_open()), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.backup_tempest_config'):

            conf_utils.configure_tempest_multisite_params('test_conf_file')
            msection.assert_any_call("kingbird")
            mset.assert_any_call('service_available', 'kingbird', 'true')
            mset.assert_any_call('kingbird', 'endpoint_type', 'publicURL')
            mset.assert_any_call('kingbird', 'TIME_TO_SYNC', '20')
            mset.assert_any_call('kingbird', 'endpoint_url',
                                 'kingbird_endpoint_url')
            self.assertTrue(mread.called)
            self.assertTrue(mwrite.called)

    def test_install_verifier_ext_default(self):
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.get_repo_tag',
                        return_value='test_tag'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.ft_utils.'
                       'execute_command_raise') as mexe:
            conf_utils.install_verifier_ext('test_path')
            cmd = ("rally verify add-verifier-ext --source test_path "
                   "--version test_tag")
            error_msg = ("Problem while adding verifier extension from"
                         " test_path")
            mexe.assert_called_once_with(cmd, error_msg=error_msg)

if __name__ == "__main__":
    unittest.main(verbosity=2)