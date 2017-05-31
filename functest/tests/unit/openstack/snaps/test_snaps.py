#!/usr/bin/env python

# Copyright (c) 2017 Cable Television Laboratories, Inc. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import mock
import unittest

from snaps.openstack.os_credentials import OSCreds

from functest.core.testcase import TestCase
from functest.opnfv_tests.openstack.snaps import connection_check


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

    result = mock.MagicMock(name='unittest.TextTestResult')
    result.testsRun = 100
    result.failures = []
    result.errors = []
    @mock.patch('functest.opnfv_tests.openstack.snaps.connection_check.'
                'ConnectionCheck')
    @mock.patch('snaps.test_suite_builder.add_openstack_client_tests')
    @mock.patch('unittest.TextTestRunner.run', return_value=result)
    def test_run_success(self, mock_test, add_os_client_tests, result):
        self.assertEquals(TestCase.EX_OK, self.connection_check.run())
        self.assertEquals(TestCase.EX_OK,
                          self.connection_check.is_successful())

    result = mock.MagicMock(name='unittest.TextTestResult')
    result.testsRun = 100
    result.failures = ['foo']
    result.errors = []
    @mock.patch('functest.opnfv_tests.openstack.snaps.connection_check.'
                'ConnectionCheck')
    @mock.patch('snaps.test_suite_builder.add_openstack_client_tests')
    @mock.patch('unittest.TextTestRunner.run', return_value=result)
    def test_run_1_of_100_failures(self, mock_test, add_os_client_tests,
                                   result):
        self.assertEquals(TestCase.EX_OK, self.connection_check.run())
        self.assertEquals(TestCase.EX_TESTCASE_FAILED,
                          self.connection_check.is_successful())

    result = mock.MagicMock(name='unittest.TextTestResult')
    result.testsRun = 100
    result.failures = ['foo']
    result.errors = []
    @mock.patch('functest.opnfv_tests.openstack.snaps.connection_check.'
                'ConnectionCheck')
    @mock.patch('snaps.test_suite_builder.add_openstack_client_tests')
    @mock.patch('unittest.TextTestRunner.run', return_value=result)
    def test_run_1_of_100_failures_within_criteria(self, mock_test,
                                                   add_os_client_tests,
                                                   result):
        self.connection_check.criteria = 90
        self.assertEquals(TestCase.EX_OK, self.connection_check.run())
        self.assertEquals(TestCase.EX_OK,
                          self.connection_check.is_successful())
