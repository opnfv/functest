#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.opnfv_tests.openstack.tempest import tempest, conf_utils
from functest.utils.constants import CONST
from snaps.openstack.os_credentials import OSCreds


class OSTempestConfUtilsTesting(unittest.TestCase):

    def setUp(self):
        self.os_creds = OSCreds(
            username='user', password='pass',
            auth_url='http://foo.com:5000/v3', project_name='bar')

    @mock.patch('snaps.openstack.utils.deploy_utils.create_project',
                return_value=mock.Mock())
    @mock.patch('snaps.openstack.utils.deploy_utils.create_user',
                return_value=mock.Mock())
    @mock.patch('snaps.openstack.utils.deploy_utils.create_network',
                return_value=None)
    @mock.patch('snaps.openstack.utils.deploy_utils.create_image',
                return_value=mock.Mock())
    def test_create_tempest_resources_missing_network_dic(self, *mock_args):
        tempest_resources = tempest.TempestResourcesManager(os_creds={})
        with self.assertRaises(Exception) as context:
            tempest_resources.create()
        msg = 'Failed to create private network'
        self.assertTrue(msg in context.exception)

    @mock.patch('snaps.openstack.utils.deploy_utils.create_project',
                return_value=mock.Mock())
    @mock.patch('snaps.openstack.utils.deploy_utils.create_user',
                return_value=mock.Mock())
    @mock.patch('snaps.openstack.utils.deploy_utils.create_network',
                return_value=mock.Mock())
    @mock.patch('snaps.openstack.utils.deploy_utils.create_image',
                return_value=None)
    def test_create_tempest_resources_missing_image(self, *mock_args):
        tempest_resources = tempest.TempestResourcesManager(os_creds={})

        CONST.__setattr__('tempest_use_custom_imagess', True)
        with self.assertRaises(Exception) as context:
            tempest_resources.create()
        msg = 'Failed to create image'
        self.assertTrue(msg in context.exception, msg=str(context.exception))

        CONST.__setattr__('tempest_use_custom_imagess', False)
        with self.assertRaises(Exception) as context:
            tempest_resources.create(use_custom_images=True)
        msg = 'Failed to create image'
        self.assertTrue(msg in context.exception, msg=str(context.exception))

    @mock.patch('snaps.openstack.utils.deploy_utils.create_project',
                return_value=mock.Mock())
    @mock.patch('snaps.openstack.utils.deploy_utils.create_user',
                return_value=mock.Mock())
    @mock.patch('snaps.openstack.utils.deploy_utils.create_network',
                return_value=mock.Mock())
    @mock.patch('snaps.openstack.utils.deploy_utils.create_image',
                return_value=mock.Mock())
    @mock.patch('snaps.openstack.create_flavor.OpenStackFlavor.create',
                return_value=None)
    def test_create_tempest_resources_missing_flavor(self, *mock_args):
        tempest_resources = tempest.TempestResourcesManager(
            os_creds=self.os_creds)

        CONST.__setattr__('tempest_use_custom_images', True)
        CONST.__setattr__('tempest_use_custom_flavors', True)
        with self.assertRaises(Exception) as context:
            tempest_resources.create()
        msg = 'Failed to create flavor'
        self.assertTrue(msg in context.exception, msg=str(context.exception))

        CONST.__setattr__('tempest_use_custom_images', True)
        CONST.__setattr__('tempest_use_custom_flavors', False)
        with self.assertRaises(Exception) as context:
            tempest_resources.create(use_custom_flavors=True)
        msg = 'Failed to create flavor'
        self.assertTrue(msg in context.exception, msg=str(context.exception))

    @mock.patch('functest.ci.prepare_env.os_utils.get_credentials_for_rally')
    @mock.patch('functest.ci.prepare_env.logger.info')
    @mock.patch('functest.ci.prepare_env.ft_utils.execute_command_raise')
    @mock.patch('functest.ci.prepare_env.ft_utils.execute_command')
    def test_install_rally(self, mock_exec, mock_exec_raise, mock_logger_info,
                           mock_os_utils):

        mock_os_utils.return_value = self._get_rally_creds()

        conf_utils.create_rally_deployment()

        cmd = "rally deployment destroy opnfv-rally"
        error_msg = "Deployment %s does not exist." % \
                    CONST.__getattribute__('rally_deployment_name')
        mock_logger_info.assert_any_call("Creating Rally environment...")
        mock_exec.assert_any_call(cmd, error_msg=error_msg, verbose=False)

        cmd = "rally deployment create --file=rally_conf.json --name="
        cmd += CONST.__getattribute__('rally_deployment_name')
        error_msg = "Problem while creating Rally deployment"
        mock_exec_raise.assert_any_call(cmd, error_msg=error_msg)

        cmd = "rally deployment check"
        error_msg = ("OpenStack not responding or "
                     "faulty Rally deployment.")
        mock_exec_raise.assert_any_call(cmd, error_msg=error_msg)

    @mock.patch('functest.ci.prepare_env.logger.debug')
    def test_create_verifier(self, mock_logger_debug):
        mock_popen = mock.Mock()
        attrs = {'poll.return_value': None,
                 'stdout.readline.return_value': '0'}
        mock_popen.configure_mock(**attrs)

        CONST.__setattr__('tempest_verifier_name', 'test_veifier_name')
        with mock.patch('functest.ci.prepare_env.'
                        'ft_utils.execute_command_raise',
                        side_effect=Exception), \
            mock.patch('functest.ci.prepare_env.subprocess.Popen',
                       return_value=mock_popen), \
                self.assertRaises(Exception):
            conf_utils.create_verifier()
            mock_logger_debug.assert_any_call("Tempest test_veifier_name"
                                              " does not exist")

    @mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                'create_verifier', return_value=mock.Mock())
    @mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                'create_rally_deployment', return_value=mock.Mock())
    def test_get_verifier_id_missing_verifier(self, mock_rally, mock_tempest):
        CONST.__setattr__('tempest_verifier_name', 'test_verifier_name')
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.subprocess.Popen') as mock_popen, \
                self.assertRaises(Exception):
            mock_stdout = mock.Mock()
            attrs = {'stdout.readline.return_value': ''}
            mock_stdout.configure_mock(**attrs)
            mock_popen.return_value = mock_stdout
            conf_utils.get_verifier_id()

    @mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                'create_verifier', return_value=mock.Mock())
    @mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                'create_rally_deployment', return_value=mock.Mock())
    def test_get_verifier_id_default(self, mock_rally, mock_tempest):
        CONST.__setattr__('tempest_verifier_name', 'test_verifier_name')
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.subprocess.Popen') as mock_popen:
            mock_stdout = mock.Mock()
            attrs = {'stdout.readline.return_value': 'test_deploy_id'}
            mock_stdout.configure_mock(**attrs)
            mock_popen.return_value = mock_stdout

            self.assertEqual(conf_utils.get_verifier_id(),
                             'test_deploy_id')

    def test_get_verifier_deployment_id_missing_rally(self):
        CONST.__setattr__('tempest_verifier_name', 'test_deploy_name')
        with mock.patch('functest.opnfv_tests.openstack.tempest.'
                        'conf_utils.subprocess.Popen') as mock_popen, \
                self.assertRaises(Exception):
            mock_stdout = mock.Mock()
            attrs = {'stdout.readline.return_value': ''}
            mock_stdout.configure_mock(**attrs)
            mock_popen.return_value = mock_stdout
            conf_utils.get_verifier_deployment_id(),

    def test_get_verifier_deployment_id_default(self):
        CONST.__setattr__('tempest_verifier_name', 'test_deploy_name')
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
                       'conf_utils.configure_tempest_update_params') as m1:
            conf_utils.configure_tempest('test_dep_dir')
            self.assertTrue(m1.called)

    def test_configure_tempest_defcore_default(self):
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
                       'conf_utils.generate_test_accounts_file'), \
            mock.patch('functest.opnfv_tests.openstack.tempest.'
                       'conf_utils.shutil.copyfile'):
            conf_utils.configure_tempest_defcore(
                'test_dep_dir', 'test_image_id', 'test_flavor_id',
                'test_image_alt_id', 'test_flavor_alt_id', 'test_tenant_id')
            mset.assert_any_call('compute', 'image_ref', 'test_image_id')
            mset.assert_any_call('compute', 'image_ref_alt',
                                 'test_image_alt_id')
            mset.assert_any_call('compute', 'flavor_ref', 'test_flavor_id')
            mset.assert_any_call('compute', 'flavor_ref_alt',
                                 'test_flavor_alt_id')
            self.assertTrue(mread.called)
            self.assertTrue(mwrite.called)

    def test_generate_test_accounts_file_default(self):
        with mock.patch("__builtin__.open", mock.mock_open()), \
            mock.patch('functest.opnfv_tests.openstack.tempest.conf_utils.'
                       'yaml.dump') as mock_dump:
            conf_utils.generate_test_accounts_file('test_tenant_id')
            self.assertTrue(mock_dump.called)

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
                       'conf_utils.backup_tempest_config'), \
            mock.patch('functest.utils.functest_utils.yaml.safe_load',
                       return_value={'validation': {'ssh_timeout': 300}}):
            CONST.__setattr__('OS_ENDPOINT_TYPE', None)
            conf_utils.\
                configure_tempest_update_params('test_conf_file',
                                                image_id=image_id,
                                                flavor_id=flavor_id)
            mset.assert_any_call(params[0], params[1], params[2])
            self.assertTrue(mread.called)
            self.assertTrue(mwrite.called)

    def test_configure_tempest_update_params_missing_image_id(self):
            CONST.__setattr__('tempest_use_custom_images', True)
            self._test_missing_param(('compute', 'image_ref',
                                      'test_image_id'), 'test_image_id',
                                     None)

    def test_configure_tempest_update_params_missing_image_id_alt(self):
            CONST.__setattr__('tempest_use_custom_images', True)
            conf_utils.IMAGE_ID_ALT = 'test_image_id_alt'
            self._test_missing_param(('compute', 'image_ref_alt',
                                      'test_image_id_alt'), None, None)

    def test_configure_tempest_update_params_missing_flavor_id(self):
            CONST.__setattr__('tempest_use_custom_flavors', True)
            self._test_missing_param(('compute', 'flavor_ref',
                                      'test_flavor_id'), None,
                                     'test_flavor_id')

    def test_configure_tempest_update_params_missing_flavor_id_alt(self):
            CONST.__setattr__('tempest_use_custom_flavors', True)
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


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
