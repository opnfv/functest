# Copyright (c) 2017 Cable Television Laboratories, Inc. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import mock
import os
import unittest

from snaps.openstack.os_credentials import OSCreds

from functest.core.testcase import TestCase
from functest.opnfv_tests.openstack.snaps import (connection_check, api_check,
                                                  health_check, smoke)


class ConnectionCheckTesting(unittest.TestCase):
    """
    Ensures the VPingUserdata class can run in Functest. This test does not
    actually connect with an OpenStack pod.
    """

    def setUp(self):
        self.os_creds = OSCreds(
            username='user', password='pass',
            auth_url='http://foo.com:5000/v3', project_name='bar')

        self.connection_check = connection_check.ConnectionCheck(
            os_creds=self.os_creds, ext_net_name='foo')

    @mock.patch('snaps_suite_builder.add_openstack_client_tests')
    def test_run_success(self, add_os_client_tests):
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = []
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.connection_check.run())
            self.assertEquals(TestCase.EX_OK,
                              self.connection_check.is_successful())

    @mock.patch('snaps_suite_builder.add_openstack_client_tests')
    def test_run_1_of_100_failures(self, add_os_client_tests):
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = ['foo']
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.connection_check.run())
            self.assertEquals(TestCase.EX_TESTCASE_FAILED,
                              self.connection_check.is_successful())

    @mock.patch('snaps_suite_builder.add_openstack_client_tests')
    def test_run_1_of_100_failures_within_criteria(self, add_os_client_tests):
        self.connection_check.criteria = 90
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = ['foo']
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.connection_check.run())
            self.assertEquals(TestCase.EX_OK,
                              self.connection_check.is_successful())


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

    @mock.patch('snaps_suite_builder.add_openstack_api_tests')
    def test_run_success(self, add_tests):
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = []
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.api_check.run())
            self.assertEquals(TestCase.EX_OK,
                              self.api_check.is_successful())

    @mock.patch('snaps_suite_builder.add_openstack_api_tests')
    def test_run_1_of_100_failures(self, add_tests):
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = ['foo']
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.api_check.run())
            self.assertEquals(TestCase.EX_TESTCASE_FAILED,
                              self.api_check.is_successful())

    @mock.patch('snaps_suite_builder.add_openstack_api_tests')
    def test_run_1_of_100_failures_within_criteria(self, add_tests):
        self.api_check.criteria = 90
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = ['foo']
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.api_check.run())
            self.assertEquals(TestCase.EX_OK,
                              self.api_check.is_successful())


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

    @mock.patch('snaps_suite_builder.add_openstack_client_tests')
    def test_run_success(self, add_tests):
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = []
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.health_check.run())
            self.assertEquals(TestCase.EX_OK,
                              self.health_check.is_successful())

    @mock.patch('snaps_suite_builder.add_openstack_client_tests')
    def test_run_1_of_100_failures(self, add_tests):
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = ['foo']
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.health_check.run())
            self.assertEquals(TestCase.EX_TESTCASE_FAILED,
                              self.health_check.is_successful())

    @mock.patch('snaps_suite_builder.add_openstack_client_tests')
    def test_run_1_of_100_failures_within_criteria(self, add_tests):
        self.health_check.criteria = 90
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = ['foo']
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.health_check.run())
            self.assertEquals(TestCase.EX_OK,
                              self.health_check.is_successful())


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

    @mock.patch('snaps_suite_builder.add_openstack_integration_tests')
    @mock.patch('os.path.join', return_value=os.getcwd())
    def test_run_success(self, add_tests, cwd):
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = []
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.smoke.run())
            self.assertEquals(TestCase.EX_OK,
                              self.smoke.is_successful())

    @mock.patch('snaps_suite_builder.add_openstack_integration_tests')
    @mock.patch('os.path.join', return_value=os.getcwd())
    def test_run_1_of_100_failures(self, add_tests, cwd):
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = ['foo']
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.smoke.run())
            self.assertEquals(TestCase.EX_TESTCASE_FAILED,
                              self.smoke.is_successful())

    @mock.patch('snaps_suite_builder.add_openstack_integration_tests')
    @mock.patch('os.path.join', return_value=os.getcwd())
    def test_run_1_of_100_failures_within_criteria(self, add_tests, cwd):
        self.smoke.criteria = 90
        result = mock.MagicMock(name='unittest.TextTestResult')
        result.testsRun = 100
        result.failures = ['foo']
        result.errors = []
        with mock.patch('unittest.TextTestRunner.run', return_value=result):
            self.assertEquals(TestCase.EX_OK, self.smoke.run())
            self.assertEquals(TestCase.EX_OK,
                              self.smoke.is_successful())
