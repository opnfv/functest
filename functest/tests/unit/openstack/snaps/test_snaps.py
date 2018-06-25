# Copyright (c) 2017 Cable Television Laboratories, Inc. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock
from xtesting.core import testcase

from functest.opnfv_tests.openstack.snaps import api_check
from functest.opnfv_tests.openstack.snaps import health_check
from functest.opnfv_tests.openstack.snaps import smoke
from snaps.openstack.os_credentials import OSCreds


class APICheckTesting(unittest.TestCase):
    """
    Ensures the VPingUserdata class can run in Functest. This test does not
    actually connect with an OpenStack pod.
    """

    def setUp(self):
        self.os_creds = OSCreds(
            username='user', password='pass',
            auth_url='http://foo.com:5000/v3', project_name='bar')

        self.api_check = api_check.ApiCheck(
            os_creds=self.os_creds, ext_net_name='foo')

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_suite_builder.'
                'add_openstack_client_tests')
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_suite_builder.'
                'add_openstack_api_tests')
    @mock.patch('unittest.TextTestRunner.run',
                return_value=mock.MagicMock(name='unittest.TextTestResult'))
    def test_run_success(self, *args):
        args[0].return_value.testsRun = 100
        args[0].return_value.failures = []
        args[0].return_value.errors = []
        self.assertEquals(testcase.TestCase.EX_OK, self.api_check.run())
        self.assertEquals(
            testcase.TestCase.EX_OK, self.api_check.is_successful())
        args[0].assert_called_with(mock.ANY)
        args[1].assert_called_with(
            ext_net_name='foo', image_metadata=mock.ANY,
            os_creds=self.os_creds, suite=mock.ANY, use_keystone=True)

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_suite_builder.'
                'add_openstack_client_tests')
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_suite_builder.'
                'add_openstack_api_tests')
    @mock.patch('unittest.TextTestRunner.run',
                return_value=mock.MagicMock(name='unittest.TextTestResult'))
    def test_run_1_of_100_ko(self, *args):
        args[0].return_value.testsRun = 100
        args[0].return_value.failures = ['foo']
        args[0].return_value.errors = []
        self.assertEquals(testcase.TestCase.EX_OK, self.api_check.run())
        self.assertEquals(
            testcase.TestCase.EX_TESTCASE_FAILED,
            self.api_check.is_successful())
        args[0].assert_called_with(mock.ANY)
        args[1].assert_called_with(
            ext_net_name='foo', image_metadata=mock.ANY,
            os_creds=self.os_creds, suite=mock.ANY, use_keystone=True)

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_suite_builder.'
                'add_openstack_client_tests')
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_suite_builder.'
                'add_openstack_api_tests')
    @mock.patch('unittest.TextTestRunner.run',
                return_value=mock.MagicMock(name='unittest.TextTestResult'))
    def test_run_1_of_100_ko_criteria(self, *args):
        self.api_check.criteria = 90
        args[0].return_value.testsRun = 100
        args[0].return_value.failures = ['foo']
        args[0].return_value.errors = []
        self.assertEquals(testcase.TestCase.EX_OK, self.api_check.run())
        self.assertEquals(
            testcase.TestCase.EX_OK, self.api_check.is_successful())
        args[0].assert_called_with(mock.ANY)
        args[1].assert_called_with(
            ext_net_name='foo', image_metadata=mock.ANY,
            os_creds=self.os_creds, suite=mock.ANY, use_keystone=True)


class HealthCheckTesting(unittest.TestCase):
    """
    Ensures the VPingUserdata class can run in Functest. This test does not
    actually connect with an OpenStack pod.
    """

    def setUp(self):
        self.os_creds = OSCreds(
            username='user', password='pass',
            auth_url='http://foo.com:5000/v3', project_name='bar')

        self.health_check = health_check.HealthCheck(
            os_creds=self.os_creds, ext_net_name='foo')

    @mock.patch('snaps.openstack.tests.os_source_file_test.'
                'OSIntegrationTestCase.parameterize')
    @mock.patch('unittest.TextTestRunner.run',
                return_value=mock.MagicMock(name='unittest.TextTestResult'))
    def test_run_success(self, *args):
        args[0].return_value.testsRun = 100
        args[0].return_value.failures = []
        args[0].return_value.errors = []
        self.assertEquals(testcase.TestCase.EX_OK, self.health_check.run())
        self.assertEquals(
            testcase.TestCase.EX_OK, self.health_check.is_successful())
        args[0].assert_called_with(mock.ANY)
        args[1].assert_called_with(
            mock.ANY, ext_net_name='foo', flavor_metadata=mock.ANY,
            image_metadata=mock.ANY, netconf_override=None,
            os_creds=self.os_creds, use_keystone=True)

    @mock.patch('snaps.openstack.tests.os_source_file_test.'
                'OSIntegrationTestCase.parameterize')
    @mock.patch('unittest.TextTestRunner.run',
                return_value=mock.MagicMock(name='unittest.TextTestResult'))
    def test_run_1_of_100_ko(self, *args):
        args[0].return_value.testsRun = 100
        args[0].return_value.failures = ['foo']
        args[0].return_value.errors = []
        self.assertEquals(testcase.TestCase.EX_OK, self.health_check.run())
        self.assertEquals(
            testcase.TestCase.EX_TESTCASE_FAILED,
            self.health_check.is_successful())
        args[0].assert_called_with(mock.ANY)
        args[1].assert_called_with(
            mock.ANY, ext_net_name='foo', flavor_metadata=mock.ANY,
            image_metadata=mock.ANY, netconf_override=None,
            os_creds=self.os_creds, use_keystone=True)

    @mock.patch('snaps.openstack.tests.os_source_file_test.'
                'OSIntegrationTestCase.parameterize')
    @mock.patch('unittest.TextTestRunner.run',
                return_value=mock.MagicMock(name='unittest.TextTestResult'))
    def test_run_1_of_100_ko_criteria(self, *args):
        self.health_check.criteria = 90
        args[0].return_value.testsRun = 100
        args[0].return_value.failures = ['foo']
        args[0].return_value.errors = []
        self.assertEquals(testcase.TestCase.EX_OK, self.health_check.run())
        self.assertEquals(
            testcase.TestCase.EX_OK, self.health_check.is_successful())
        args[0].assert_called_with(mock.ANY)
        args[1].assert_called_with(
            mock.ANY, ext_net_name='foo', flavor_metadata=mock.ANY,
            image_metadata=mock.ANY, netconf_override=None,
            os_creds=self.os_creds, use_keystone=True)


class SmokeTesting(unittest.TestCase):
    """
    Ensures the VPingUserdata class can run in Functest. This test does not
    actually connect with an OpenStack pod.
    """

    def setUp(self):
        self.os_creds = OSCreds(
            username='user', password='pass',
            auth_url='http://foo.com:5000/v3', project_name='bar')

        self.smoke = smoke.SnapsSmoke(
            os_creds=self.os_creds, ext_net_name='foo')

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_suite_builder.'
                'add_openstack_integration_tests')
    @mock.patch('unittest.TextTestRunner.run',
                return_value=mock.MagicMock(name='unittest.TextTestResult'))
    def test_run_success(self, *args):
        args[0].return_value.testsRun = 100
        args[0].return_value.failures = []
        args[0].return_value.errors = []
        self.assertEquals(testcase.TestCase.EX_OK, self.smoke.run())
        self.assertEquals(testcase.TestCase.EX_OK, self.smoke.is_successful())
        args[0].assert_called_with(mock.ANY)
        args[1].assert_called_with(
            ext_net_name='foo', flavor_metadata=mock.ANY,
            image_metadata=mock.ANY, netconf_override=None,
            os_creds=self.os_creds, suite=mock.ANY, use_floating_ips=True,
            use_keystone=True)

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_suite_builder.'
                'add_openstack_integration_tests')
    @mock.patch('unittest.TextTestRunner.run',
                return_value=mock.MagicMock(name='unittest.TextTestResult'))
    def test_run_1_of_100_ko(self, *args):
        args[0].return_value.testsRun = 100
        args[0].return_value.failures = ['foo']
        args[0].return_value.errors = []
        self.assertEquals(testcase.TestCase.EX_OK, self.smoke.run())
        self.assertEquals(
            testcase.TestCase.EX_TESTCASE_FAILED, self.smoke.is_successful())
        args[0].assert_called_with(mock.ANY)
        args[1].assert_called_with(
            ext_net_name='foo', flavor_metadata=mock.ANY,
            image_metadata=mock.ANY, netconf_override=mock.ANY,
            os_creds=self.os_creds, suite=mock.ANY, use_floating_ips=True,
            use_keystone=True)

    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_suite_builder.'
                'add_openstack_integration_tests')
    @mock.patch('unittest.TextTestRunner.run',
                return_value=mock.MagicMock(name='unittest.TextTestResult'))
    def test_run_1_of_100_ko_criteria(self, *args):
        self.smoke.criteria = 90
        args[0].return_value.testsRun = 100
        args[0].return_value.failures = ['foo']
        args[0].return_value.errors = []
        self.assertEquals(testcase.TestCase.EX_OK, self.smoke.run())
        self.assertEquals(
            testcase.TestCase.EX_OK, self.smoke.is_successful())
        args[0].assert_called_with(mock.ANY)
        args[1].assert_called_with(
            ext_net_name='foo', flavor_metadata=mock.ANY,
            image_metadata=mock.ANY, netconf_override=None,
            os_creds=self.os_creds, suite=mock.ANY, use_floating_ips=True,
            use_keystone=True)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
