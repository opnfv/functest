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

from keystoneauth1.exceptions import auth_plugins
import mock
from robot.errors import RobotError
import six
from six.moves import urllib

from functest.core import testcase
from functest.opnfv_tests.sdn.odl import odl

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class ODLTesting(unittest.TestCase):

    """The super class which testing classes could inherit."""
    # pylint: disable=missing-docstring

    logging.disable(logging.CRITICAL)

    _keystone_ip = "127.0.0.1"
    _neutron_url = "http://127.0.0.2:9696"
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
        if len(args) > 0:
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
                odl.ODLTests.basic_suite_dir,
                odl.ODLTests.neutron_suite_dir,
                log='NONE',
                output=os.path.join(self.test.res_dir, 'output.xml'),
                report='NONE',
                stdout=mock.ANY,
                variable=variable)

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

    @mock.patch('robot.run', side_effect=RobotError)
    @mock.patch('os.path.isfile', return_value=True)
    def test_run_ko(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                self.assertRaises(RobotError):
            self._test_run_suites(testcase.TestCase.EX_RUN_ERROR, *args)

    @mock.patch('robot.run')
    @mock.patch('os.path.isfile', return_value=True)
    def test_parse_results_ko(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results',
                                  side_effect=RobotError):
            self._test_run_suites(testcase.TestCase.EX_RUN_ERROR, *args)

    @mock.patch('robot.run')
    @mock.patch('os.path.isfile', return_value=True)
    def test_ok(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_run_suites(testcase.TestCase.EX_OK, *args)

    @mock.patch('robot.run')
    @mock.patch('os.path.isfile', return_value=False)
    def test_ok_no_creds(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True) as mock_method, \
                mock.patch.object(self.test, 'parse_results'):
            self._test_run_suites(testcase.TestCase.EX_OK, *args)
            mock_method.assert_not_called()

    @mock.patch('robot.run', return_value=1)
    @mock.patch('os.path.isfile', return_value=True)
    def test_testcases_in_failure(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_run_suites(testcase.TestCase.EX_OK, *args)


class ODLRunTesting(ODLTesting):

    """The class testing ODLTests.run()."""
    # pylint: disable=missing-docstring

    def _test_no_env_var(self, var):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value=ODLTesting._neutron_url):
            del os.environ[var]
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def _test_run(self, status=testcase.TestCase.EX_OK,
                  exception=None, **kwargs):
        odlip = kwargs['odlip'] if 'odlip' in kwargs else '127.0.0.3'
        odlwebport = kwargs['odlwebport'] if 'odlwebport' in kwargs else '8080'
        odlrestconfport = (kwargs['odlrestconfport']
                           if 'odlrestconfport' in kwargs else '8181')

        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value=ODLTesting._neutron_url):
            if exception:
                self.test.run_suites = mock.Mock(side_effect=exception)
            else:
                self.test.run_suites = mock.Mock(return_value=status)
            self.assertEqual(self.test.run(), status)
            self.test.run_suites.assert_called_once_with(
                odl.ODLTests.default_suites,
                neutronurl=self._neutron_url,
                odlip=odlip, odlpassword=self._odl_password,
                odlrestconfport=odlrestconfport,
                odlusername=self._odl_username, odlwebport=odlwebport,
                osauthurl=self._os_auth_url,
                ospassword=self._os_password,
                osprojectname=self._os_projectname,
                osusername=self._os_username,
                osprojectdomainname=self._os_projectdomainname,
                osuserdomainname=self._os_userdomainname)

    def _test_multiple_suites(self, suites,
                              status=testcase.TestCase.EX_OK, **kwargs):
        odlip = kwargs['odlip'] if 'odlip' in kwargs else '127.0.0.3'
        odlwebport = kwargs['odlwebport'] if 'odlwebport' in kwargs else '8080'
        odlrestconfport = (kwargs['odlrestconfport']
                           if 'odlrestconfport' in kwargs else '8181')
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value=ODLTesting._neutron_url):
            self.test.run_suites = mock.Mock(return_value=status)
            self.assertEqual(self.test.run(suites=suites), status)
            self.test.run_suites.assert_called_once_with(
                suites,
                neutronurl=self._neutron_url,
                odlip=odlip, odlpassword=self._odl_password,
                odlrestconfport=odlrestconfport,
                odlusername=self._odl_username, odlwebport=odlwebport,
                osauthurl=self._os_auth_url,
                ospassword=self._os_password,
                osprojectname=self._os_projectname,
                osusername=self._os_username,
                osprojectdomainname=self._os_projectdomainname,
                osuserdomainname=self._os_userdomainname)

    def test_exc(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        side_effect=auth_plugins.MissingAuthPlugin()):
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

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
        self._test_run(testcase.TestCase.EX_RUN_ERROR,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_run_suites_exc(self):
        with self.assertRaises(Exception):
            os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
            self._test_run(status=testcase.TestCase.EX_RUN_ERROR,
                           exception=Exception(),
                           odlip=self._sdn_controller_ip,
                           odlwebport=self._odl_webport)

    def test_no_sdn_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value=ODLTesting._neutron_url):
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def test_without_installer_type(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_suites(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_multiple_suites(
            [odl.ODLTests.basic_suite_dir],
            testcase.TestCase.EX_OK,
            odlip=self._sdn_controller_ip,
            odlwebport=self._odl_webport)

    def test_fuel(self):
        os.environ["INSTALLER_TYPE"] = "fuel"
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=urllib.parse.urlparse(self._neutron_url).hostname,
                       odlwebport='8181',
                       odlrestconfport='8282')

    def test_apex_no_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value=ODLTesting._neutron_url):
            os.environ["INSTALLER_TYPE"] = "apex"
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def test_apex(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "apex"
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=self._sdn_controller_ip, odlwebport='8081',
                       odlrestconfport='8081')

    def test_netvirt_no_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value=ODLTesting._neutron_url):
            os.environ["INSTALLER_TYPE"] = "netvirt"
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def test_netvirt(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "netvirt"
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=self._sdn_controller_ip, odlwebport='8081',
                       odlrestconfport='8081')

    def test_joid_no_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value=ODLTesting._neutron_url):
            os.environ["INSTALLER_TYPE"] = "joid"
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def test_joid(self):
        os.environ["SDN_CONTROLLER"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "joid"
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=self._sdn_controller_ip, odlwebport='8080')

    def test_compass(self):
        os.environ["INSTALLER_TYPE"] = "compass"
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=urllib.parse.urlparse(self._neutron_url).hostname,
                       odlrestconfport='8080')

    def test_daisy_no_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value=ODLTesting._neutron_url):
            os.environ["INSTALLER_TYPE"] = "daisy"
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def test_daisy(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "daisy"
        self._test_run(testcase.TestCase.EX_OK,
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
