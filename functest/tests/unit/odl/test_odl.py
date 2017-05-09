#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the classes required to fully cover odl."""

import errno
import logging
import os
import StringIO
import unittest

from keystoneauth1.exceptions import auth_plugins
import mock
from robot.errors import DataError, RobotError
from robot.result import testcase as result_testcase
from robot.utils.robottime import timestamp_to_secs

from functest.core import testcase
from functest.opnfv_tests.sdn.odl import odl

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class ODLVisitorTesting(unittest.TestCase):

    """The class testing ODLResultVisitor."""
    # pylint: disable=missing-docstring

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.visitor = odl.ODLResultVisitor()

    def test_empty(self):
        self.assertFalse(self.visitor.get_data())

    def test_ok(self):
        data = {'name': 'foo',
                'parent': 'bar',
                'status': 'PASS',
                'starttime': "20161216 16:00:00.000",
                'endtime': "20161216 16:00:01.000",
                'elapsedtime': 1000,
                'text': 'Hello, World!',
                'critical': True}
        test = result_testcase.TestCase(name=data['name'],
                                        status=data['status'],
                                        message=data['text'],
                                        starttime=data['starttime'],
                                        endtime=data['endtime'])
        test.parent = mock.Mock()
        config = {'name': data['parent'],
                  'criticality.test_is_critical.return_value': data[
                      'critical']}
        test.parent.configure_mock(**config)
        self.visitor.visit_test(test)
        self.assertEqual(self.visitor.get_data(), [data])


class ODLTesting(unittest.TestCase):

    """The super class which testing classes could inherit."""
    # pylint: disable=missing-docstring

    logging.disable(logging.CRITICAL)

    _keystone_ip = "127.0.0.1"
    _neutron_ip = "127.0.0.2"
    _sdn_controller_ip = "127.0.0.3"
    _os_auth_url = "http://{}:5000/v2.0".format(_keystone_ip)
    _os_tenantname = "admin"
    _os_username = "admin"
    _os_password = "admin"
    _odl_webport = "8080"
    _odl_restconfport = "8181"
    _odl_username = "admin"
    _odl_password = "admin"

    def setUp(self):
        for var in ("INSTALLER_TYPE", "SDN_CONTROLLER", "SDN_CONTROLLER_IP"):
            if var in os.environ:
                del os.environ[var]
        os.environ["OS_AUTH_URL"] = self._os_auth_url
        os.environ["OS_USERNAME"] = self._os_username
        os.environ["OS_PASSWORD"] = self._os_password
        os.environ["OS_TENANT_NAME"] = self._os_tenantname
        self.test = odl.ODLTests(case_name='odl', project_name='functest')
        self.defaultargs = {'odlusername': self._odl_username,
                            'odlpassword': self._odl_password,
                            'neutronip': self._keystone_ip,
                            'osauthurl': self._os_auth_url,
                            'osusername': self._os_username,
                            'ostenantname': self._os_tenantname,
                            'ospassword': self._os_password,
                            'odlip': self._keystone_ip,
                            'odlwebport': self._odl_webport,
                            'odlrestconfport': self._odl_restconfport,
                            'pushtodb': False}


class ODLParseResultTesting(ODLTesting):

    """The class testing ODLTests.parse_results()."""
    # pylint: disable=missing-docstring

    _config = {'name': 'dummy', 'starttime': '20161216 16:00:00.000',
               'endtime': '20161216 16:00:01.000'}

    @mock.patch('robot.api.ExecutionResult', side_effect=DataError)
    def test_raises_exc(self, mock_method):
        with self.assertRaises(DataError):
            self.test.parse_results()
        mock_method.assert_called_once_with(
            os.path.join(odl.ODLTests.res_dir, 'output.xml'))

    def _test_result(self, config, result):
        suite = mock.Mock()
        suite.configure_mock(**config)
        with mock.patch('robot.api.ExecutionResult',
                        return_value=mock.Mock(suite=suite)):
            self.test.parse_results()
            self.assertEqual(self.test.result, result)
            self.assertEqual(self.test.start_time,
                             timestamp_to_secs(config['starttime']))
            self.assertEqual(self.test.stop_time,
                             timestamp_to_secs(config['endtime']))
            self.assertEqual(self.test.details,
                             {'description': config['name'], 'tests': []})

    def test_null_passed(self):
        self._config.update({'statistics.all.passed': 0,
                             'statistics.all.total': 20})
        self._test_result(self._config, 0)

    def test_no_test(self):
        self._config.update({'statistics.all.passed': 20,
                             'statistics.all.total': 0})
        self._test_result(self._config, 0)

    def test_half_success(self):
        self._config.update({'statistics.all.passed': 10,
                             'statistics.all.total': 20})
        self._test_result(self._config, 50)

    def test_success(self):
        self._config.update({'statistics.all.passed': 20,
                             'statistics.all.total': 20})
        self._test_result(self._config, 100)


class ODLRobotTesting(ODLTesting):

    """The class testing ODLTests.set_robotframework_vars()."""
    # pylint: disable=missing-docstring

    @mock.patch('fileinput.input', side_effect=Exception())
    def test_set_vars_ko(self, mock_method):
        self.assertFalse(self.test.set_robotframework_vars())
        mock_method.assert_called_once_with(
            os.path.join(odl.ODLTests.odl_test_repo,
                         'csit/variables/Variables.py'), inplace=True)

    @mock.patch('fileinput.input', return_value=[])
    def test_set_vars_empty(self, mock_method):
        self.assertTrue(self.test.set_robotframework_vars())
        mock_method.assert_called_once_with(
            os.path.join(odl.ODLTests.odl_test_repo,
                         'csit/variables/Variables.py'), inplace=True)

    @mock.patch('sys.stdout', new_callable=StringIO.StringIO)
    def _test_set_vars(self, msg1, msg2, *args):
        line = mock.MagicMock()
        line.__iter__.return_value = [msg1]
        with mock.patch('fileinput.input', return_value=line) as mock_method:
            self.assertTrue(self.test.set_robotframework_vars())
            mock_method.assert_called_once_with(
                os.path.join(odl.ODLTests.odl_test_repo,
                             'csit/variables/Variables.py'), inplace=True)
            self.assertEqual(args[0].getvalue(), "{}\n".format(msg2))

    def test_set_vars_auth_default(self):
        self._test_set_vars("AUTH = []",
                            "AUTH = [u'admin', u'admin']")

    def test_set_vars_auth1(self):
        self._test_set_vars("AUTH1 = []", "AUTH1 = []")

    @mock.patch('sys.stdout', new_callable=StringIO.StringIO)
    def test_set_vars_auth_foo(self, *args):
        line = mock.MagicMock()
        line.__iter__.return_value = ["AUTH = []"]
        with mock.patch('fileinput.input', return_value=line) as mock_method:
            self.assertTrue(self.test.set_robotframework_vars('foo', 'bar'))
            mock_method.assert_called_once_with(
                os.path.join(odl.ODLTests.odl_test_repo,
                             'csit/variables/Variables.py'), inplace=True)
            self.assertEqual(args[0].getvalue(),
                             "AUTH = [u'{}', u'{}']\n".format('foo', 'bar'))


class ODLMainTesting(ODLTesting):

    """The class testing ODLTests.main()."""
    # pylint: disable=missing-docstring

    def _get_main_kwargs(self, key=None):
        kwargs = {'odlusername': self._odl_username,
                  'odlpassword': self._odl_password,
                  'neutronip': self._neutron_ip,
                  'osauthurl': self._os_auth_url,
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
        if len(args) > 0:
            args[0].assert_called_once_with(
                odl.ODLTests.res_dir)
        if len(args) > 1:
            variable = ['KEYSTONE:{}'.format(self._keystone_ip),
                        'NEUTRON:{}'.format(self._neutron_ip),
                        'OS_AUTH_URL:"{}"'.format(self._os_auth_url),
                        'OSUSERNAME:"{}"'.format(self._os_username),
                        'OSTENANTNAME:"{}"'.format(self._os_tenantname),
                        'OSPASSWORD:"{}"'.format(self._os_password),
                        'ODL_SYSTEM_IP:{}'.format(self._sdn_controller_ip),
                        'PORT:{}'.format(self._odl_webport),
                        'RESTCONFPORT:{}'.format(self._odl_restconfport)]
            args[1].assert_called_once_with(
                odl.ODLTests.basic_suite_dir,
                odl.ODLTests.neutron_suite_dir,
                log='NONE',
                output=os.path.join(odl.ODLTests.res_dir, 'output.xml'),
                report='NONE',
                stdout=mock.ANY,
                variable=variable)
        if len(args) > 2:
            args[2].assert_called_with(
                os.path.join(odl.ODLTests.res_dir, 'stdout.txt'))

    def _test_no_keyword(self, key):
        kwargs = self._get_main_kwargs(key)
        self.assertEqual(self.test.main(**kwargs),
                         testcase.TestCase.EX_RUN_ERROR)

    def test_no_odlusername(self):
        self._test_no_keyword('odlusername')

    def test_no_odlpassword(self):
        self._test_no_keyword('odlpassword')

    def test_no_neutronip(self):
        self._test_no_keyword('neutronip')

    def test_no_osauthurl(self):
        self._test_no_keyword('osauthurl')

    def test_no_osusername(self):
        self._test_no_keyword('osusername')

    def test_no_ostenantname(self):
        self._test_no_keyword('ostenantname')

    def test_no_ospassword(self):
        self._test_no_keyword('ospassword')

    def test_no_odlip(self):
        self._test_no_keyword('odlip')

    def test_no_odlwebport(self):
        self._test_no_keyword('odlwebport')

    def test_no_odlrestconfport(self):
        self._test_no_keyword('odlrestconfport')

    def test_set_vars_ko(self):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=False) as mock_object:
            self._test_main(testcase.TestCase.EX_RUN_ERROR)
            mock_object.assert_called_once_with(
                self._odl_username, self._odl_password)

    @mock.patch('os.makedirs', side_effect=Exception)
    def test_makedirs_exc(self, mock_method):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                self.assertRaises(Exception):
            self._test_main(testcase.TestCase.EX_RUN_ERROR,
                            mock_method)

    @mock.patch('os.makedirs', side_effect=OSError)
    def test_makedirs_oserror(self, mock_method):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True):
            self._test_main(testcase.TestCase.EX_RUN_ERROR,
                            mock_method)

    @mock.patch('robot.run', side_effect=RobotError)
    @mock.patch('os.makedirs')
    def test_run_ko(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True), \
                self.assertRaises(RobotError):
            self._test_main(testcase.TestCase.EX_RUN_ERROR, *args)

    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_parse_results_ko(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True), \
                mock.patch.object(self.test, 'parse_results',
                                  side_effect=RobotError):
            self._test_main(testcase.TestCase.EX_RUN_ERROR, *args)

    @mock.patch('os.remove', side_effect=Exception)
    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_remove_exc(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'), \
                self.assertRaises(Exception):
            self._test_main(testcase.TestCase.EX_OK, *args)

    @mock.patch('os.remove')
    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_ok(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(testcase.TestCase.EX_OK, *args)

    @mock.patch('os.remove')
    @mock.patch('robot.run')
    @mock.patch('os.makedirs', side_effect=OSError(errno.EEXIST, ''))
    def test_makedirs_oserror17(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True) as mock_open, \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(testcase.TestCase.EX_OK, *args)
        mock_open.assert_called_once_with(
            os.path.join(odl.ODLTests.res_dir, 'stdout.txt'), 'w+')

    @mock.patch('os.remove')
    @mock.patch('robot.run', return_value=1)
    @mock.patch('os.makedirs')
    def test_testcases_in_failure(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True) as mock_open, \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(testcase.TestCase.EX_OK, *args)
        mock_open.assert_called_once_with(
            os.path.join(odl.ODLTests.res_dir, 'stdout.txt'), 'w+')

    @mock.patch('os.remove', side_effect=OSError)
    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_remove_oserror(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True) as mock_open, \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(testcase.TestCase.EX_OK, *args)
        mock_open.assert_called_once_with(
            os.path.join(odl.ODLTests.res_dir, 'stdout.txt'), 'w+')


class ODLRunTesting(ODLTesting):

    """The class testing ODLTests.run()."""
    # pylint: disable=missing-docstring

    def _test_no_env_var(self, var):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value="http://{}:9696".format(
                            ODLTesting._neutron_ip)):
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
                        return_value="http://{}:9696".format(
                            ODLTesting._neutron_ip)):
            if exception:
                self.test.main = mock.Mock(side_effect=exception)
            else:
                self.test.main = mock.Mock(return_value=status)
            self.assertEqual(self.test.run(), status)
            self.test.main.assert_called_once_with(
                odl.ODLTests.default_suites,
                neutronip=self._neutron_ip,
                odlip=odlip, odlpassword=self._odl_password,
                odlrestconfport=odlrestconfport,
                odlusername=self._odl_username, odlwebport=odlwebport,
                osauthurl=self._os_auth_url,
                ospassword=self._os_password, ostenantname=self._os_tenantname,
                osusername=self._os_username)

    def _test_multiple_suites(self, suites,
                              status=testcase.TestCase.EX_OK, **kwargs):
        odlip = kwargs['odlip'] if 'odlip' in kwargs else '127.0.0.3'
        odlwebport = kwargs['odlwebport'] if 'odlwebport' in kwargs else '8080'
        odlrestconfport = (kwargs['odlrestconfport']
                           if 'odlrestconfport' in kwargs else '8181')
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value="http://{}:9696".format(
                            ODLTesting._neutron_ip)):
            self.test.main = mock.Mock(return_value=status)
            self.assertEqual(self.test.run(suites=suites), status)
            self.test.main.assert_called_once_with(
                suites,
                neutronip=self._neutron_ip,
                odlip=odlip, odlpassword=self._odl_password,
                odlrestconfport=odlrestconfport,
                odlusername=self._odl_username, odlwebport=odlwebport,
                osauthurl=self._os_auth_url,
                ospassword=self._os_password, ostenantname=self._os_tenantname,
                osusername=self._os_username)

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

    def test_no_os_tenant_name(self):
        self._test_no_env_var("OS_TENANT_NAME")

    def test_main_false(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_RUN_ERROR,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_main_exc(self):
        with self.assertRaises(Exception):
            os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
            self._test_run(status=testcase.TestCase.EX_RUN_ERROR,
                           exception=Exception(),
                           odlip=self._sdn_controller_ip,
                           odlwebport=self._odl_webport)

    def test_no_sdn_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value="http://{}:9696".format(
                            ODLTesting._neutron_ip)):
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
                       odlip=self._neutron_ip, odlwebport='8282')

    def test_apex_no_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        return_value="http://{}:9696".format(
                            ODLTesting._neutron_ip)):
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
                        return_value="http://{}:9696".format(
                            ODLTesting._neutron_ip)):
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
                        return_value="http://{}:9696".format(
                            ODLTesting._neutron_ip)):
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
                       odlip=self._neutron_ip, odlwebport='8181')


class ODLArgParserTesting(ODLTesting):

    """The class testing ODLParser."""
    # pylint: disable=missing-docstring

    def setUp(self):
        self.parser = odl.ODLParser()
        super(ODLArgParserTesting, self).setUp()

    def test_default(self):
        self.assertEqual(self.parser.parse_args(), self.defaultargs)

    def test_basic(self):
        self.defaultargs['neutronip'] = self._neutron_ip
        self.defaultargs['odlip'] = self._sdn_controller_ip
        self.assertEqual(
            self.parser.parse_args(
                ["--neutronip={}".format(self._neutron_ip),
                 "--odlip={}".format(self._sdn_controller_ip)]),
            self.defaultargs)

    @mock.patch('sys.stderr', new_callable=StringIO.StringIO)
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

    def test_neutronip(self):
        self._test_arg('neutronip', '127.0.0.4')

    def test_osusername(self):
        self._test_arg('osusername', 'foo')

    def test_ostenantname(self):
        self._test_arg('ostenantname', 'foo')

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
        self.defaultargs['neutronip'] = self._neutron_ip
        self.defaultargs['odlip'] = self._sdn_controller_ip
        self.assertEqual(
            self.parser.parse_args(
                ["--neutronip={}".format(self._neutron_ip),
                 "--odlip={}".format(self._sdn_controller_ip)]),
            self.defaultargs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
