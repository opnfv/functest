#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import errno
import logging
import mock
import os
import unittest

from robot.errors import RobotError

from functest.core import TestCasesBase
from functest.opnfv_tests.Controllers.ODL import OpenDaylightTesting
from functest.utils import functest_constants as ft_constants


class ODLTestCasesTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    _keystone_ip = "127.0.0.1"
    _neutron_ip = "127.0.0.2"
    _sdn_controller_ip = "127.0.0.3"
    _os_tenantname = "admin"
    _os_username = "admin"
    _os_password = "admin"
    _odl_webport = "8080"
    _odl_restconfport = "8181"
    _odl_username = "admin"
    _odl_password = "admin"

    def setUp(self):
        ft_constants.OS_USERNAME = self._os_username
        ft_constants.OS_PASSWORD = self._os_password
        ft_constants.OS_TENANT_NAME = self._os_tenantname
        self.test = OpenDaylightTesting.ODLTestCases()

    @mock.patch('fileinput.input', side_effect=Exception())
    def test_set_robotframework_vars_failed(self, *args):
        self.assertFalse(self.test.set_robotframework_vars())

    @mock.patch('fileinput.input', return_value=[])
    def test_set_robotframework_vars(self, args):
        self.assertTrue(self.test.set_robotframework_vars())

    @classmethod
    def _fake_url_for(cls, service_type='identity', **kwargs):
        if service_type == 'identity':
            return "http://{}:5000/v2.0".format(
                ODLTestCasesTesting._keystone_ip)
        elif service_type == 'network':
            return "http://{}:9696".format(ODLTestCasesTesting._neutron_ip)
        else:
            return None

    @classmethod
    def _get_fake_keystone_client(cls):
        kclient = mock.Mock()
        kclient.service_catalog = mock.Mock()
        kclient.service_catalog.url_for = mock.Mock(
            side_effect=cls._fake_url_for)
        return kclient

    def _get_main_kwargs(self, key=None):
        kwargs = {'odlusername': self._odl_username,
                  'odlpassword': self._odl_password,
                  'keystoneip': self._keystone_ip,
                  'neutronip': self._neutron_ip,
                  'osusername': self._os_username,
                  'ostenantname': self._os_tenantname,
                  'ospassword': self._os_password,
                  'odlip': self._sdn_controller_ip,
                  'odlwebport': self._odl_webport,
                  'odlrestconfport': self._odl_restconfport}
        if key:
            del kwargs[key]
        return kwargs

    def _test_main(self, status, *args):
        kwargs = self._get_main_kwargs()
        self.assertEqual(self.test.main(**kwargs), status)
        odl_res_dir = OpenDaylightTesting.ODLTestCases.res_dir
        if len(args) > 0:
            args[0].assert_called_once_with(odl_res_dir)
        if len(args) > 1:
            variable = ['KEYSTONE:{}'.format(self._keystone_ip),
                        'NEUTRON:{}'.format(self._neutron_ip),
                        'OSUSERNAME:"{}"'.format(self._os_username),
                        'OSTENANTNAME:"{}"'.format(self._os_tenantname),
                        'OSPASSWORD:"{}"'.format(self._os_password),
                        'ODL_SYSTEM_IP:{}'.format(self._sdn_controller_ip),
                        'PORT:{}'.format(self._odl_webport),
                        'RESTCONFPORT:{}'.format(self._odl_restconfport)]
            output_file = os.path.join(odl_res_dir, 'output.xml')
            args[1].assert_called_once_with(
                OpenDaylightTesting.ODLTestCases.basic_suite_dir,
                OpenDaylightTesting.ODLTestCases.neutron_suite_dir,
                log='NONE',
                output=output_file,
                report='NONE',
                stdout=mock.ANY,
                variable=variable)
        if len(args) > 2:
            stdout_file = os.path.join(odl_res_dir, 'stdout.txt')
            args[2].assert_called_with(stdout_file)

    def _test_main_missing_keyword(self, key):
        kwargs = self._get_main_kwargs(key)
        self.assertEqual(self.test.main(**kwargs),
                         TestCasesBase.TestCasesBase.EX_RUN_ERROR)

    def test_main_missing_odlusername(self):
        self._test_main_missing_keyword('odlusername')

    def test_main_missing_odlpassword(self):
        self._test_main_missing_keyword('odlpassword')

    def test_main_missing_keystoneip(self):
        self._test_main_missing_keyword('keystoneip')

    def test_main_missing_neutronip(self):
        self._test_main_missing_keyword('neutronip')

    def test_main_missing_osusername(self):
        self._test_main_missing_keyword('osusername')

    def test_main_missing_ostenantname(self):
        self._test_main_missing_keyword('ostenantname')

    def test_main_missing_ospassword(self):
        self._test_main_missing_keyword('ospassword')

    def test_main_missing_odlip(self):
        self._test_main_missing_keyword('odlip')

    def test_main_missing_odlwebport(self):
        self._test_main_missing_keyword('odlwebport')

    def test_main_missing_odlrestconfport(self):
        self._test_main_missing_keyword('odlrestconfport')

    def test_main_set_robotframework_vars_failed(self):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=False):
            self._test_main(TestCasesBase.TestCasesBase.EX_RUN_ERROR)
            self.test.set_robotframework_vars.assert_called_once_with(
                self._odl_username, self._odl_password)

    @mock.patch('os.makedirs', side_effect=Exception)
    def test_main_makedirs_exception(self, mock_method):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                self.assertRaises(Exception):
            self._test_main(TestCasesBase.TestCasesBase.EX_RUN_ERROR,
                            mock_method)

    @mock.patch('os.makedirs', side_effect=OSError)
    def test_main_makedirs_oserror(self, mock_method):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True):
            self._test_main(TestCasesBase.TestCasesBase.EX_RUN_ERROR,
                            mock_method)

    @mock.patch('robot.run', side_effect=RobotError)
    @mock.patch('os.makedirs')
    def test_main_robot_run_failed(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                self.assertRaises(RobotError):
            self._test_main(TestCasesBase.TestCasesBase.EX_RUN_ERROR, *args)

    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_main_parse_results_failed(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results',
                                  side_effect=RobotError):
            self._test_main(TestCasesBase.TestCasesBase.EX_RUN_ERROR, *args)

    @mock.patch('os.remove', side_effect=Exception)
    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_main_remove_exception(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'), \
                self.assertRaises(Exception):
            self._test_main(TestCasesBase.TestCasesBase.EX_OK, *args)

    @mock.patch('os.remove')
    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_main(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(TestCasesBase.TestCasesBase.EX_OK, *args)

    @mock.patch('os.remove')
    @mock.patch('robot.run')
    @mock.patch('os.makedirs', side_effect=OSError(errno.EEXIST, ''))
    def test_main_makedirs_oserror17(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(TestCasesBase.TestCasesBase.EX_OK, *args)

    @mock.patch('os.remove')
    @mock.patch('robot.run', return_value=1)
    @mock.patch('os.makedirs')
    def test_main_testcases_in_failure(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(TestCasesBase.TestCasesBase.EX_OK, *args)

    @mock.patch('os.remove', side_effect=OSError)
    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_main_remove_oserror(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(TestCasesBase.TestCasesBase.EX_OK, *args)

    def _test_run_missing_env_var(self, var):
        if var == 'OS_USERNAME':
            ft_constants.OS_USERNAME = None
        elif var == 'OS_PASSWORD':
            ft_constants.OS_PASSWORD = None
        elif var == 'OS_TENANT_NAME':
            ft_constants.OS_TENANT_NAME = None

        self.assertEqual(self.test.run(),
                         TestCasesBase.TestCasesBase.EX_RUN_ERROR)

    def _test_run(self, status=TestCasesBase.TestCasesBase.EX_OK,
                  exception=None, odlip="127.0.0.3", odlwebport="8080"):
        with mock.patch('functest.utils.openstack_utils.get_keystone_client',
                        return_value=self._get_fake_keystone_client()):
            if exception:
                self.test.main = mock.Mock(side_effect=exception)
            else:
                self.test.main = mock.Mock(return_value=status)
            self.assertEqual(self.test.run(), status)
            self.test.main.assert_called_once_with(
                keystoneip=self._keystone_ip, neutronip=self._neutron_ip,
                odlip=odlip, odlpassword=self._odl_password,
                odlrestconfport=self._odl_restconfport,
                odlusername=self._odl_username, odlwebport=odlwebport,
                ospassword=self._os_password, ostenantname=self._os_tenantname,
                osusername=self._os_username)

    def test_run_missing_os_username(self):
        self._test_run_missing_env_var("OS_USERNAME")

    def test_run_missing_os_password(self):
        self._test_run_missing_env_var("OS_PASSWORD")

    def test_run_missing_os_tenant_name(self):
        self._test_run_missing_env_var("OS_TENANT_NAME")

    def test_run_main_false(self):
        ft_constants.CI_INSTALLER_TYPE = None
        ft_constants.SDN_CONTROLLER_IP = self._sdn_controller_ip
        self._test_run(TestCasesBase.TestCasesBase.EX_RUN_ERROR,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_run_main_exception(self):
        ft_constants.CI_INSTALLER_TYPE = None
        ft_constants.SDN_CONTROLLER_IP = self._sdn_controller_ip
        with self.assertRaises(Exception):
            self._test_run(status=TestCasesBase.TestCasesBase.EX_RUN_ERROR,
                           exception=Exception(),
                           odlip=self._sdn_controller_ip,
                           odlwebport=self._odl_webport)

    def test_run_missing_sdn_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_keystone_client',
                        return_value=self._get_fake_keystone_client()):
            ft_constants.CI_INSTALLER_TYPE = None
            ft_constants.SDN_CONTROLLER_IP = None
            self.assertEqual(self.test.run(),
                             TestCasesBase.TestCasesBase.EX_RUN_ERROR)

    def test_run_without_installer_type(self):
        ft_constants.SDN_CONTROLLER_IP = self._sdn_controller_ip
        ft_constants.CI_INSTALLER_TYPE = None
        self._test_run(TestCasesBase.TestCasesBase.EX_OK,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_run_fuel(self):
        ft_constants.CI_INSTALLER_TYPE = "fuel"
        self._test_run(TestCasesBase.TestCasesBase.EX_OK,
                       odlip=self._neutron_ip, odlwebport='8282')

    def test_run_apex_missing_sdn_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_keystone_client',
                        return_value=self._get_fake_keystone_client()):
            ft_constants.CI_INSTALLER_TYPE = "apex"
            ft_constants.SDN_CONTROLLER_IP = None
            self.assertEqual(self.test.run(),
                             TestCasesBase.TestCasesBase.EX_RUN_ERROR)

    def test_run_apex(self):
        ft_constants.SDN_CONTROLLER_IP = self._sdn_controller_ip
        ft_constants.CI_INSTALLER_TYPE = "apex"
        self._test_run(TestCasesBase.TestCasesBase.EX_OK,
                       odlip=self._sdn_controller_ip, odlwebport='8181')

    def test_run_joid_missing_sdn_controller(self):
        with mock.patch('functest.utils.openstack_utils.get_keystone_client',
                        return_value=self._get_fake_keystone_client()):
            ft_constants.CI_INSTALLER_TYPE = "joid"
            ft_constants.SDN_CONTROLLER = None
            self.assertEqual(self.test.run(),
                             TestCasesBase.TestCasesBase.EX_RUN_ERROR)

    def test_run_joid(self):
        ft_constants.SDN_CONTROLLER = self._sdn_controller_ip
        ft_constants.CI_INSTALLER_TYPE = "joid"
        self._test_run(TestCasesBase.TestCasesBase.EX_OK,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_run_compass(self, *args):
        ft_constants.CI_INSTALLER_TYPE = "compass"
        self._test_run(TestCasesBase.TestCasesBase.EX_OK,
                       odlip=self._neutron_ip, odlwebport='8181')


if __name__ == "__main__":
    unittest.main(verbosity=2)
