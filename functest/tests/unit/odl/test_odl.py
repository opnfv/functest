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
import StringIO
import unittest

from keystoneauth1.exceptions import auth_plugins
from robot.errors import DataError, RobotError
from robot.result import testcase as result_testcase
from robot.utils.robottime import timestamp_to_secs

from functest.core import testcase
from functest.opnfv_tests.sdn.odl import odl


class ODLTesting(unittest.TestCase):

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
        self.test = odl.ODLTests()
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

    def test_empty_visitor(self):
        visitor = odl.ODLResultVisitor()
        self.assertFalse(visitor.get_data())

    def test_visitor(self):
        visitor = odl.ODLResultVisitor()
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
        visitor.visit_test(test)
        self.assertEqual(visitor.get_data(), [data])

    @mock.patch('robot.api.ExecutionResult', side_effect=DataError)
    def test_parse_results_raises_exceptions(self, *args):
        with self.assertRaises(DataError):
            self.test.parse_results()

    def test_parse_results(self, *args):
        config = {'name': 'dummy', 'starttime': '20161216 16:00:00.000',
                  'endtime': '20161216 16:00:01.000', 'status': 'PASS'}
        suite = mock.Mock()
        suite.configure_mock(**config)
        with mock.patch('robot.api.ExecutionResult',
                        return_value=mock.Mock(suite=suite)):
            self.test.parse_results()
            self.assertEqual(self.test.criteria, config['status'])
            self.assertEqual(self.test.start_time,
                             timestamp_to_secs(config['starttime']))
            self.assertEqual(self.test.stop_time,
                             timestamp_to_secs(config['endtime']))
            self.assertEqual(self.test.details,
                             {'description': config['name'], 'tests': []})

    @mock.patch('fileinput.input', side_effect=Exception())
    def test_set_robotframework_vars_failed(self, *args):
        self.assertFalse(self.test.set_robotframework_vars())

    @mock.patch('fileinput.input', return_value=[])
    def test_set_robotframework_vars_empty(self, args):
        self.assertTrue(self.test.set_robotframework_vars())

    @mock.patch('sys.stdout', new_callable=StringIO.StringIO)
    def _test_set_robotframework_vars(self, msg1, msg2, *args):
        line = mock.MagicMock()
        line.__iter__.return_value = [msg1]
        with mock.patch('fileinput.input', return_value=line) as mock_method:
            self.assertTrue(self.test.set_robotframework_vars())
            mock_method.assert_called_once_with(
                os.path.join(odl.ODLTests.odl_test_repo,
                             'csit/variables/Variables.py'), inplace=True)
            self.assertEqual(args[0].getvalue(), "{}\n".format(msg2))

    def test_set_robotframework_vars_auth_default(self):
        self._test_set_robotframework_vars("AUTH = []",
                                           "AUTH = [u'admin', u'admin']")

    def test_set_robotframework_vars_auth1(self):
        self._test_set_robotframework_vars("AUTH1 = []", "AUTH1 = []")

    @mock.patch('sys.stdout', new_callable=StringIO.StringIO)
    def test_set_robotframework_vars_auth_foo(self, *args):
        line = mock.MagicMock()
        line.__iter__.return_value = ["AUTH = []"]
        with mock.patch('fileinput.input', return_value=line) as mock_method:
            self.assertTrue(self.test.set_robotframework_vars('foo', 'bar'))
            mock_method.assert_called_once_with(
                os.path.join(odl.ODLTests.odl_test_repo,
                             'csit/variables/Variables.py'), inplace=True)
            self.assertEqual(args[0].getvalue(),
                             "AUTH = [u'{}', u'{}']\n".format('foo', 'bar'))

    @classmethod
    def _fake_url_for(cls, service_type='identity', **kwargs):
        if service_type == 'identity':
            return "http://{}:5000/v2.0".format(
                ODLTesting._keystone_ip)
        elif service_type == 'network':
            return "http://{}:9696".format(ODLTesting._neutron_ip)
        else:
            return None

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

    def _test_main_missing_keyword(self, key):
        kwargs = self._get_main_kwargs(key)
        self.assertEqual(self.test.main(**kwargs),
                         testcase.TestCase.EX_RUN_ERROR)

    def test_main_missing_odlusername(self):
        self._test_main_missing_keyword('odlusername')

    def test_main_missing_odlpassword(self):
        self._test_main_missing_keyword('odlpassword')

    def test_main_missing_neutronip(self):
        self._test_main_missing_keyword('neutronip')

    def test_main_missing_osauthurl(self):
        self._test_main_missing_keyword('osauthurl')

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
            self._test_main(testcase.TestCase.EX_RUN_ERROR)
            self.test.set_robotframework_vars.assert_called_once_with(
                self._odl_username, self._odl_password)

    @mock.patch('os.makedirs', side_effect=Exception)
    def test_main_makedirs_exception(self, mock_method):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                self.assertRaises(Exception):
            self._test_main(testcase.TestCase.EX_RUN_ERROR,
                            mock_method)

    @mock.patch('os.makedirs', side_effect=OSError)
    def test_main_makedirs_oserror(self, mock_method):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True):
            self._test_main(testcase.TestCase.EX_RUN_ERROR,
                            mock_method)

    @mock.patch('robot.run', side_effect=RobotError)
    @mock.patch('os.makedirs')
    def test_main_robot_run_failed(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True), \
                self.assertRaises(RobotError):
            self._test_main(testcase.TestCase.EX_RUN_ERROR, *args)

    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_main_parse_results_failed(self, *args):
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
    def test_main_remove_exception(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(self.test, 'parse_results'), \
                self.assertRaises(Exception):
            self._test_main(testcase.TestCase.EX_OK, *args)

    @mock.patch('os.remove')
    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_main(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(testcase.TestCase.EX_OK, *args)

    @mock.patch('os.remove')
    @mock.patch('robot.run')
    @mock.patch('os.makedirs', side_effect=OSError(errno.EEXIST, ''))
    def test_main_makedirs_oserror17(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(testcase.TestCase.EX_OK, *args)

    @mock.patch('os.remove')
    @mock.patch('robot.run', return_value=1)
    @mock.patch('os.makedirs')
    def test_main_testcases_in_failure(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(testcase.TestCase.EX_OK, *args)

    @mock.patch('os.remove', side_effect=OSError)
    @mock.patch('robot.run')
    @mock.patch('os.makedirs')
    def test_main_remove_oserror(self, *args):
        with mock.patch.object(self.test, 'set_robotframework_vars',
                               return_value=True), \
                mock.patch.object(odl, 'open', mock.mock_open(),
                                  create=True), \
                mock.patch.object(self.test, 'parse_results'):
            self._test_main(testcase.TestCase.EX_OK, *args)

    def _test_run_missing_env_var(self, var):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        side_effect=self._fake_url_for):
            del os.environ[var]
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def _test_run(self, status=testcase.TestCase.EX_OK,
                  exception=None, odlip="127.0.0.3", odlwebport="8080",
                  odlrestconfport="8181"):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        side_effect=self._fake_url_for):
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

    def _test_run_defining_multiple_suites(
            self, suites,
            status=testcase.TestCase.EX_OK,
            exception=None, odlip="127.0.0.3", odlwebport="8080",
            odlrestconfport="8181"):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        side_effect=self._fake_url_for):
            if exception:
                self.test.main = mock.Mock(side_effect=exception)
            else:
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

    def test_run_exception(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        side_effect=auth_plugins.MissingAuthPlugin()):
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def test_run_missing_os_auth_url(self):
        self._test_run_missing_env_var("OS_AUTH_URL")

    def test_run_missing_os_username(self):
        self._test_run_missing_env_var("OS_USERNAME")

    def test_run_missing_os_password(self):
        self._test_run_missing_env_var("OS_PASSWORD")

    def test_run_missing_os_tenant_name(self):
        self._test_run_missing_env_var("OS_TENANT_NAME")

    def test_run_main_false(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_RUN_ERROR,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_run_main_exception(self):
        with self.assertRaises(Exception):
            os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
            self._test_run(status=testcase.TestCase.EX_RUN_ERROR,
                           exception=Exception(),
                           odlip=self._sdn_controller_ip,
                           odlwebport=self._odl_webport)

    def test_run_missing_sdn_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        side_effect=self._fake_url_for):
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def test_run_without_installer_type(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=self._sdn_controller_ip,
                       odlwebport=self._odl_webport)

    def test_run_redefining_suites(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        self._test_run_defining_multiple_suites(
            [odl.ODLTests.basic_suite_dir],
            testcase.TestCase.EX_OK,
            odlip=self._sdn_controller_ip,
            odlwebport=self._odl_webport)

    def test_run_fuel(self):
        os.environ["INSTALLER_TYPE"] = "fuel"
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=self._neutron_ip, odlwebport='8282')

    def test_run_apex_missing_sdn_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        side_effect=self._fake_url_for):
            os.environ["INSTALLER_TYPE"] = "apex"
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def test_run_apex(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "apex"
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=self._sdn_controller_ip, odlwebport='8081',
                       odlrestconfport='8081')

    def test_run_netvirt_missing_sdn_controller_ip(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        side_effect=self._fake_url_for):
            os.environ["INSTALLER_TYPE"] = "netvirt"
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def test_run_netvirt(self):
        os.environ["SDN_CONTROLLER_IP"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "netvirt"
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=self._sdn_controller_ip, odlwebport='8081',
                       odlrestconfport='8081')

    def test_run_joid_missing_sdn_controller(self):
        with mock.patch('functest.utils.openstack_utils.get_endpoint',
                        side_effect=self._fake_url_for):
            os.environ["INSTALLER_TYPE"] = "joid"
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_RUN_ERROR)

    def test_run_joid(self):
        os.environ["SDN_CONTROLLER"] = self._sdn_controller_ip
        os.environ["INSTALLER_TYPE"] = "joid"
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=self._sdn_controller_ip, odlwebport='8080')

    def test_run_compass(self, *args):
        os.environ["INSTALLER_TYPE"] = "compass"
        self._test_run(testcase.TestCase.EX_OK,
                       odlip=self._neutron_ip, odlwebport='8181')

    def test_argparser_default(self):
        parser = odl.ODLParser()
        self.assertEqual(parser.parse_args(), self.defaultargs)

    def test_argparser_basic(self):
        self.defaultargs['neutronip'] = self._neutron_ip
        self.defaultargs['odlip'] = self._sdn_controller_ip
        parser = odl.ODLParser()
        self.assertEqual(parser.parse_args(
            ["--neutronip={}".format(self._neutron_ip),
             "--odlip={}".format(self._sdn_controller_ip)
             ]), self.defaultargs)

    @mock.patch('sys.stderr', new_callable=StringIO.StringIO)
    def test_argparser_fail(self, *args):
        self.defaultargs['foo'] = 'bar'
        parser = odl.ODLParser()
        with self.assertRaises(SystemExit):
            parser.parse_args(["--foo=bar"])

    def _test_argparser(self, arg, value):
        self.defaultargs[arg] = value
        parser = odl.ODLParser()
        self.assertEqual(parser.parse_args(["--{}={}".format(arg, value)]),
                         self.defaultargs)

    def test_argparser_odlusername(self):
        self._test_argparser('odlusername', 'foo')

    def test_argparser_odlpassword(self):
        self._test_argparser('odlpassword', 'foo')

    def test_argparser_osauthurl(self):
        self._test_argparser('osauthurl', 'http://127.0.0.4:5000/v2')

    def test_argparser_neutronip(self):
        self._test_argparser('neutronip', '127.0.0.4')

    def test_argparser_osusername(self):
        self._test_argparser('osusername', 'foo')

    def test_argparser_ostenantname(self):
        self._test_argparser('ostenantname', 'foo')

    def test_argparser_ospassword(self):
        self._test_argparser('ospassword', 'foo')

    def test_argparser_odlip(self):
        self._test_argparser('odlip', '127.0.0.4')

    def test_argparser_odlwebport(self):
        self._test_argparser('odlwebport', '80')

    def test_argparser_odlrestconfport(self):
        self._test_argparser('odlrestconfport', '80')

    def test_argparser_pushtodb(self):
        self.defaultargs['pushtodb'] = True
        parser = odl.ODLParser()
        self.assertEqual(parser.parse_args(["--{}".format('pushtodb')]),
                         self.defaultargs)

    def test_argparser_multiple_args(self):
        self.defaultargs['neutronip'] = self._neutron_ip
        self.defaultargs['odlip'] = self._sdn_controller_ip
        parser = odl.ODLParser()
        self.assertEqual(parser.parse_args(
            ["--neutronip={}".format(self._neutron_ip),
             "--odlip={}".format(self._sdn_controller_ip)
             ]), self.defaultargs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
