#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the classes required to fully cover odl."""

import logging
import os
import unittest

import mock
import munch
from robot.errors import RobotError
import six
from six.moves import urllib
from xtesting.core import testcase

from functest.opnfv_tests.sdn.odl import odl

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class ODLTesting(unittest.TestCase):

    """The super class which testing classes could inherit."""
    # pylint: disable=missing-docstring

    logging.disable(logging.CRITICAL)

    _keystone_ip = "127.0.0.1"
    _neutron_url = u"https://127.0.0.1:9696"
    _neutron_id = u"dummy"
    _sdn_controller_ip = "127.0.0.3"
    _os_auth_url = "http://{}:5000/v3".format(_keystone_ip)
    _os_projectname = "admin"
    _os_username = "admin"
    _os_password = "admin"
    _odl_webport = "8080"
    _odl_restconfport = "8181"
    _odl_username = "admin"
    _odl_password = "admin"
    _os_userdomainname = 'Default'
    _os_projectdomainname = 'Default'
    _os_interface = "public"

    def setUp(self):
        for var in ("INSTALLER_TYPE", "SDN_CONTROLLER", "SDN_CONTROLLER_IP"):
            if var in os.environ:
                del os.environ[var]
        os.environ["OS_AUTH_URL"] = self._os_auth_url
        os.environ["OS_USERNAME"] = self._os_username
        os.environ["OS_USER_DOMAIN_NAME"] = self._os_userdomainname
        os.environ["OS_PASSWORD"] = self._os_password
        os.environ["OS_PROJECT_NAME"] = self._os_projectname
        os.environ["OS_PROJECT_DOMAIN_NAME"] = self._os_projectdomainname
        os.environ["OS_PASSWORD"] = self._os_password
        os.environ["OS_INTERFACE"] = self._os_interface
        self.test = odl.ODLTests(case_name='odl', project_name='functest')
        self.defaultargs = {'odlusername': self._odl_username,
                            'odlpassword': self._odl_password,
                            'neutronurl': "http://{}:9696".format(
                                self._keystone_ip),
                            'osauthurl': self._os_auth_url,
                            'osusername': self._os_username,
                            'osuserdomainname': self._os_userdomainname,
                            'osprojectname': self._os_projectname,
                            'osprojectdomainname': self._os_projectdomainname,
                            'ospassword': self._os_password,
                            'odlip': self._keystone_ip,
                            'odlwebport': self._odl_webport,
                            'odlrestconfport': self._odl_restconfport,
                            'pushtodb': False}


class ODLRobotTesting(ODLTesting):

    """The class testing ODLTests.set_robotframework_vars()."""
    # pylint: disable=missing-docstring

    @mock.patch('fileinput.input', side_effect=Exception())
    def test_set_vars_ko(self, mock_method):
        self.assertFalse(self.test.set_robotframework_vars())
        mock_method.assert_called_once_with(
            os.path.join(odl.ODLTests.odl_test_repo,
                         'csit/variables/Variables.robot'), inplace=True)

    @mock.patch('fileinput.input', return_value=[])
    def test_set_vars_empty(self, mock_method):
        self.assertTrue(self.test.set_robotframework_vars())
        mock_method.assert_called_once_with(
            os.path.join(odl.ODLTests.odl_test_repo,
                         'csit/variables/Variables.robot'), inplace=True)

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    def _test_set_vars(self, msg1, msg2, *args):
        line = mock.MagicMock()
        line.__iter__.return_value = [msg1]
        with mock.patch('fileinput.input', return_value=line) as mock_method:
            self.assertTrue(self.test.set_robotframework_vars())
            mock_method.assert_called_once_with(
                os.path.join(odl.ODLTests.odl_test_repo,
                             'csit/variables/Variables.robot'), inplace=True)
            self.assertEqual(args[0].getvalue(), "{}\n".format(msg2))

    def test_set_vars_auth_default(self):
        self._test_set_vars(
            "@{AUTH} ",
            "@{AUTH}           admin    admin")

    def test_set_vars_auth1(self):
        self._test_set_vars(
            "@{AUTH1}           foo    bar",
            "@{AUTH1}           foo    bar")

    @mock.patch('sys.stdout', new_callable=six.StringIO)
    def test_set_vars_auth_foo(self, *args):
        line = mock.MagicMock()
        line.__iter__.return_value = ["@{AUTH} "]
        with mock.patch('fileinput.input', return_value=line) as mock_method:
            self.assertTrue(self.test.set_robotframework_vars('foo', 'bar'))
            mock_method.assert_called_once_with(
                os.path.join(odl.ODLTests.odl_test_repo,
                             'csit/variables/Variables.robot'), inplace=True)
            self.assertEqual(
                args[0].getvalue(),
                "@{AUTH}           foo    bar\n")


class ODLMainTesting(ODLTesting):

    """The class testing ODLTests.run_suites()."""
    # pylint: disable=missing-docstring

    def _get_run_suites_kwargs(self, key=None):
        kwargs = {'odlusername': self._odl_username,
                  'odlpassword': self._odl_password,
                  'neutronurl': self._neutron_url,
                  'osauthurl': self._os_auth_url,
                  'osusername': self._os_username,
                  'osuserdomainname': self._os_userdomainname,
                  'osprojectname': self._os_projectname,
                  'osprojectdomainname': self._os_projectdomainname,
                  'ospassword': self._os_password,
                  'odlip': self._sdn_controller_ip,
                  'odlwebport': self._odl_webport,
                  'odlrestconfport': self._odl_restconfport}
        if key:
            del kwargs[key]
        return kwargs

    def _test_run_suites(self, status, *args):
        kwargs = self._get_run_suites_kwargs()
        self.assertEqual(self.test.run_suites(**kwargs), status)
        if args:
            args[0].assert_called_once_with(self.test.odl_variables_file)
        if len(args) > 1:
            variable = [
                'KEYSTONEURL:{}://{}'.format(
                    urllib.parse.urlparse(self._os_auth_url).scheme,
                    urllib.parse.urlparse(self._os_auth_url).netloc),
                'NEUTRONURL:{}'.format(self._neutron_url),
                'OS_AUTH_URL:"{}"'.format(self._os_auth_url),
                'OSUSERNAME:"{}"'.format(self._os_username),
                'OSUSERDOMAINNAME:"{}"'.format(self._os_userdomainname),
                'OSTENANTNAME:"{}"'.format(self._os_projectname),
                'OSPROJECTDOMAINNAME:"{}"'.format(self._os_projectdomainname),
                'OSPASSWORD:"{}"'.format(self._os_password),
                'ODL_SYSTEM_IP:{}'.format(self._sdn_controller_ip),
                'PORT:{}'.format(self._odl_webport),
                'RESTCONFPORT:{}'.format(self._odl_restconfport)]
            args[1].assert_called_once_with(
                odl.ODLTests.basic_suite_dir, odl.ODLTests.neutron_suite_dir,
                include=[],
                log='NONE',
                output=os.path.join(self.test.res_dir, 'output.xml'),
                report='NONE', stdout=mock.ANY, variable=variable,
                variablefile=[])

    def _test_no_keyword(self, key):
        kwargs = self._get_run_suites_kwargs(key)
        self.assertEqual(self.test.run_suites(**kwargs),
                         testcase.TestCase.EX_RUN_ERROR)

    def test_no_odlusername(self):
        self._test_no_keyword('odlusername')

    def test_no_odlpassword(self):
        self._test_no_keyword('odlpassword')

    def test_no_neutronurl(self):
        self._test_no_keyword('neutronurl')

    def test_no_osauthurl(self):
        self._test_no_keyword('osauthurl')

    def test_no_osusername(self):
        self._test_no_keyword('osusername')

    def test_no_osprojectname(self):
        self._test_no_keyword('osprojectname')

    def test_no_ospassword(self):
        self._test_no_keyword('ospassword')

    def test_no_odlip(self):
        self._test_no_keyword('odlip')

    def test_no_odlwebport(self):
        self._test_no_keyword('odlwebport')

    def test_no_odlrestconfport(self):
        self._test_no_keyword('odlrestconfport')

    @mock.patch('os.path.isfile', return_value=True)
    def test_set_vars_ko(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=False) as mock_object:
            self._test_run_suites(testcase.TestCase.EX_RUN_ERROR)
            mock_object.assert_called_once_with(
                self._odl_username, self._odl_password)
        args[0].assert_called_once_with(self.test.odl_variables_file)

    @mock.patch('os.makedirs')
    @mock.patch('robot.run', side_effect=RobotError)
    @mock.patch('os.path.isfile', return_value=True)
    def test_run_ko(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                self.assertRaises(RobotError):
            self._test_run_suites(testcase.TestCase.EX_RUN_ERROR, *args)

    @mock.patch('os.makedirs')
    @mock.patch('robot.run')
    @mock.patch('os.path.isfile', return_value=True)
    def test_parse_results_ko(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results',
                                  side_effect=RobotError):
            self._test_run_suites(testcase.TestCase.EX_RUN_ERROR, *args)

    @mock.patch('os.makedirs')
    @mock.patch('robot.run')
    @mock.patch('os.path.isfile', return_value=True)
    def test_ok(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_run_suites(testcase.TestCase.EX_OK, *args)

    @mock.patch('os.makedirs')
    @mock.patch('robot.run')
    @mock.patch('os.path.isfile', return_value=False)
    def test_ok_no_creds(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True) as mock_method, \
                mock.patch.object(self.test, 'parse_results'):
            self._test_run_suites(testcase.TestCase.EX_OK, *args)
            mock_method.assert_not_called()

    @mock.patch('os.makedirs')
    @mock.patch('robot.run', return_value=1)
    @mock.patch('os.path.isfile', return_value=True)
    def test_testcases_in_failure(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_run_suites(testcase.TestCase.EX_OK, *args)


class ODLRunTesting(ODLTesting):
    """The class testing ODLTests.run()."""
    # pylint: disable=too-many-public-methods,missing-docstring

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud', side_effect=Exception)
    def test_no_cloud(self, *args):
        self.assertEqual(self.test.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].assert_called_once_with(cloud_config=mock.ANY)

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def test_no_service1(self, *args):
        args[0].return_value.search_services.return_value = None
        self.assertEqual(self.test.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].return_value.search_services.assert_called_once_with('neutron')
        args[0].return_value.search_endpoints.assert_not_called()

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def test_no_service2(self, *args):
        args[0].return_value.search_services.return_value = []
        self.assertEqual(self.test.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].return_value.search_services.assert_called_once_with('neutron')
        args[0].return_value.search_endpoints.assert_not_called()

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def test_no_service3(self, *args):
        args[0].return_value.search_services.return_value = [
            munch.Munch()]
        self.assertEqual(self.test.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].return_value.search_services.assert_called_once_with('neutron')
        args[0].return_value.search_endpoints.assert_not_called()

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def test_no_endpoint1(self, *args):
        args[0].return_value.search_services.return_value = [
            munch.Munch(id=self._neutron_id)]
        args[0].return_value.search_endpoints.return_value = None
        self.assertEqual(self.test.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].return_value.search_services.assert_called_once_with('neutron')
        args[0].return_value.search_endpoints.assert_called_once_with(
            filters={'interface': self._os_interface,
                     'service_id': self._neutron_id})

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def test_no_endpoint2(self, *args):
        args[0].return_value.search_services.return_value = [
            munch.Munch(id=self._neutron_id)]
        args[0].return_value.search_endpoints.return_value = []
        self.assertEqual(self.test.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].return_value.search_services.assert_called_once_with('neutron')
        args[0].return_value.search_endpoints.assert_called_once_with(
            filters={'interface': self._os_interface,
                     'service_id': self._neutron_id})

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def test_no_endpoint3(self, *args):
        args[0].return_value.search_services.return_value = [
            munch.Munch(id=self._neutron_id)]
        args[0].return_value.search_endpoints.return_value = [munch.Munch()]
        self.assertEqual(self.test.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].return_value.search_services.assert_called_once_with('neutron')
        args[0].return_value.search_endpoints.assert_called_once_with(
            filters={'interface': self._os_interface,
                     'service_id': self._neutron_id})

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def test_endpoint_interface(self, *args):
        args[0].return_value.search_services.return_value = [
            munch.Munch(id=self._neutron_id)]
        args[0].return_value.search_endpoints.return_value = [munch.Munch()]
        self.assertEqual(self.test.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].return_value.search_services.assert_called_once_with('neutron')
        args[0].return_value.search_endpoints.assert_called_once_with(
            filters={'interface': self._os_interface,
                     'service_id': self._neutron_id})

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def _test_no_env_var(self, var, *args):
        del os.environ[var]
        self.assertEqual(self.test.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].assert_called_once_with(cloud_config=mock.ANY)

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def _test_missing_value(self, *args):
        self.assertEqual(self.test.run(), testcase.TestCase.EX_RUN_ERROR)
        args[0].assert_called_once_with(cloud_config=mock.ANY)

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def _test_run(self, status=testcase.TestCase.EX_OK,
                  exception=None, *args, **kwargs):
        args[0].return_value.search_services.return_value = [
            munch.Munch(id=self._neutron_id)]
        args[0].return_value.search_endpoints.return_value = [
            munch.Munch(url=self._neutron_url)]
        odlip = kwargs['odlip'] if 'odlip' in kwargs else '127.0.0.3'
        odlwebport = kwargs['odlwebport'] if 'odlwebport' in kwargs else '8080'
        odlrestconfport = (kwargs['odlrestconfport']
                           if 'odlrestconfport' in kwargs else '8181')
        if exception:
            self.test.run_suites = mock.Mock(side_effect=exception)
        else:
            self.test.run_suites = mock.Mock(return_value=status)
        self.assertEqual(self.test.run(), status)
        self.test.run_suites.assert_called_once_with(
            odl.ODLTests.default_suites, neutronurl=self._neutron_url,
            odlip=odlip, odlpassword=self._odl_password,
            odlrestconfport=odlrestconfport, odlusername=self._odl_username,
            odlwebport=odlwebport, osauthurl=self._os_auth_url,
            ospassword=self._os_password, osprojectname=self._os_projectname,
            osusername=self._os_username,
            osprojectdomainname=self._os_projectdomainname,
            osuserdomainname=self._os_userdomainname)
        args[0].assert_called_once_with(cloud_config=mock.ANY)
        args[0].return_value.search_services.assert_called_once_with('neutron')
        args[0].return_value.search_endpoints.assert_called_once_with(
            filters={
                'interface': os.environ.get(
                    "OS_INTERFACE", "public").replace('URL', ''),
                'service_id': self._neutron_id})

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OperatorCloud')
    def _test_multiple_suites(self, suites,
                              status=testcase.TestCase.EX_OK, *args, **kwargs):
        args[0].return_value.search_endpoints.return_value = [
            munch.Munch(url=self._neutron_url)]
        args[0].return_value.search_services.return_value = [
            munch.Munch(id=self._neutron_id)]
        odlip = kwargs['odlip'] if 'odlip' in kwargs else '127.0.0.3'
        odlwebport = kwargs['odlwebport'] if 'odlwebport' in kwargs else '8080'
        odlrestconfport = (kwargs['odlrestconfport']
                           if 'odlrestconfport' in kwargs else '8181')
        self.test.run_suites = mock.Mock(return_value=status)
        self.assertEqual(self.test.run(suites=suites), status)
        self.test.run_suites.assert_called_once_with(
            suites, neutronurl=self._neutron_url, odlip=odlip,
            odlpassword=self._odl_password, odlrestconfport=odlrestconfport,
            odlusername=self._odl_username, odlwebport=odlwebport,
            osauthurl=self._os_auth_url, ospassword=self._os_password,
            osprojectname=self._os_projectname, osusername=self._os_username,
            osprojectdomainname=self._os_projectdomainname,
            osuserdomainname=self._os_userdomainname)
        args[0].assert_called_once_with(cloud_config=mock.ANY)
        args[0].return_value.search_services.assert_called_once_with('neutron')
        args[0].return_value.search_endpoints.assert_called_once_with(
            filters={'interface': os.environ.get("OS_INTERFACE", "public"),
                     'service_id': self._neutron_id})

    @mock.patch('os_client_config.get_config')
    def test_exc(self, *args):
        with mock.patch('shade.OperatorCloud',
                        side_effect=Exception()):
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)
            args[0].assert_called_once_with()

    def test_no_os_auth_url(self):
        self._test_no_env_var("OS_AUTH_URL")

    def test_no_os_username(self):
        self._test_no_env_var("OS_USERNAME")

    def test_no_os_password(self):
        self._test_no_env_var("OS_PASSWORD")

    def test_no_os__name(self):
        self._test_no_env_var("OS_PROJECT_NAME")

    def test_run_suites_false(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_RUN_ERROR, None,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_run_suites_exc(self):
        with self.assertRaises(Exception):
            os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
            self._test_run(testcase.TestCase.EX_RUN_ERROR,
                           Exception(),
                           odlip=self._sdn_controller_ip,
                           odlwebport=self._odl_webport)

    def test_no_sdn_controller_ip(self):
        self._test_missing_value()

    def test_without_installer_type(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_without_os_interface(self):
        del os.environ["OS_INTERFACE"]
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_os_interface_public(self):
        os.environ["OS_INTERFACE"] = "public"
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_os_interface_publicurl(self):
        os.environ["OS_INTERFACE"] = "publicURL"
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_os_interface_internal(self):
        os.environ["OS_INTERFACE"] = "internal"
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_os_interface_admin(self):
        os.environ["OS_INTERFACE"] = "admin"
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_suites(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_multiple_suites(
            [odl.ODLTests.basic_suite_dir],
            testcase.TestCase.EX_OK,
            odlip=self._sdn_controller_ip,
            odlwebport=self._odl_webport)

    def test_fuel_no_controller_ip(self):
        os.environ["INSTALLER_TYPE"] = "fuel"
        self._test_missing_value()

    def test_fuel(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "fuel"
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip,
                       odlwebport='8282',
                       odlrestconfport='8282')

    def test_apex_no_controller_ip(self):
        os.environ["INSTALLER_TYPE"] = "apex"
        self._test_missing_value()

    def test_apex(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "apex"
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip, odlwebport='8081',
                       odlrestconfport='8081')

    def test_netvirt_no_controller_ip(self):
        os.environ["INSTALLER_TYPE"] = "netvirt"
        self._test_missing_value()

    def test_netvirt(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "netvirt"
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip, odlwebport='8081',
                       odlrestconfport='8081')

    def test_compass(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "compass"
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip,
                       odlrestconfport='8080')

    def test_daisy_no_controller_ip(self):
        os.environ["INSTALLER_TYPE"] = "daisy"
        self._test_missing_value()

    def test_daisy(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "daisy"
        self._test_run(testcase.TestCase.EX_OK, None,
                       odlip=self._sdn_controller_ip, odlwebport='8181',
                       odlrestconfport='8087')


class ODLArgParserTesting(ODLTesting):

    """The class testing ODLParser."""
    # pylint: disable=missing-docstring

    def setUp(self):
        self.parser = odl.ODLParser()
        super(ODLArgParserTesting, self).setUp()

    def test_default(self):
        self.assertEqual(self.parser.parse_args(), self.defaultargs)

    def test_basic(self):
        self.defaultargs['neutronurl'] = self._neutron_url
        self.defaultargs['odlip'] = self._sdn_controller_ip
        self.assertEqual(
            self.parser.parse_args(
                ["--neutronurl={}".format(self._neutron_url),
                 "--odlip={}".format(self._sdn_controller_ip)]),
            self.defaultargs)

    @mock.patch('sys.stderr', new_callable=six.StringIO)
    def test_fail(self, mock_method):
        self.defaultargs['foo'] = 'bar'
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--foo=bar"])
        self.assertTrue(mock_method.getvalue().startswith("usage:"))

    def _test_arg(self, arg, value):
        self.defaultargs[arg] = value
        self.assertEqual(
            self.parser.parse_args(["--{}={}".format(arg, value)]),
            self.defaultargs)

    def test_odlusername(self):
        self._test_arg('odlusername', 'foo')

    def test_odlpassword(self):
        self._test_arg('odlpassword', 'foo')

    def test_osauthurl(self):
        self._test_arg('osauthurl', 'http://127.0.0.4:5000/v2')

    def test_neutronurl(self):
        self._test_arg('neutronurl', 'http://127.0.0.4:9696')

    def test_osusername(self):
        self._test_arg('osusername', 'foo')

    def test_osuserdomainname(self):
        self._test_arg('osuserdomainname', 'domain')

    def test_osprojectname(self):
        self._test_arg('osprojectname', 'foo')

    def test_osprojectdomainname(self):
        self._test_arg('osprojectdomainname', 'domain')

    def test_ospassword(self):
        self._test_arg('ospassword', 'foo')

    def test_odlip(self):
        self._test_arg('odlip', '127.0.0.4')

    def test_odlwebport(self):
        self._test_arg('odlwebport', '80')

    def test_odlrestconfport(self):
        self._test_arg('odlrestconfport', '80')

    def test_pushtodb(self):
        self.defaultargs['pushtodb'] = True
        self.assertEqual(self.parser.parse_args(["--{}".format('pushtodb')]),
                         self.defaultargs)

    def test_multiple_args(self):
        self.defaultargs['neutronurl'] = self._neutron_url
        self.defaultargs['odlip'] = self._sdn_controller_ip
        self.assertEqual(
            self.parser.parse_args(
                ["--neutronurl={}".format(self._neutron_url),
                 "--odlip={}".format(self._sdn_controller_ip)]),
            self.defaultargs)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
