#!/usr/bin/env python

# Copyright (c) 2017 Cable Television Laboratories, Inc. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import os
import unittest

from snaps.openstack.os_credentials import OSCreds

from functest.core.testcase import TestCase
from functest.opnfv_tests.openstack.snaps import connection_check, api_check,\
    health_check, smoke


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

    @mock.patch('functest.opnfv_tests.openstack.snaps.connection_check.'
                'ConnectionCheck')
    def test_run(self, mock_logger_debug):
        with mock.patch('snaps.test_suite_builder.add_openstack_client_tests'):
            self.assertEquals(TestCase.EX_OK, self.connection_check.run())


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

    @mock.patch('functest.opnfv_tests.openstack.snaps.api_check.ApiCheck')
    def test_run(self, mock_logger_debug):
        with mock.patch('snaps.test_suite_builder.add_openstack_api_tests'):
            self.assertEquals(TestCase.EX_OK, self.api_check.run())


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

    @mock.patch('functest.opnfv_tests.openstack.snaps.health_check.'
                'HealthCheck')
    def test_run(self, mock_logger_debug):
        with mock.patch('snaps.openstack.tests.os_source_file_test.'
                        'OSIntegrationTestCase.parameterize'):
            self.assertEquals(TestCase.EX_OK, self.health_check.run())


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

    @mock.patch('functest.opnfv_tests.openstack.snaps.smoke.SnapsSmoke')
    def test_run(self, mock_logger_debug):
        with mock.patch('snaps.test_suite_builder.'
                        'add_openstack_integration_tests'), \
             mock.patch('os.path.join', return_value=os.getcwd()):
            self.assertEquals(TestCase.EX_OK, self.smoke.run())


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
