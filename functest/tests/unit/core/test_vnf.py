#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock

from functest.core import vnf
from functest.core import testcase


class VnfBaseTesting(unittest.TestCase):
    """The class testing VNF."""
    # pylint: disable=missing-docstring,too-many-public-methods

    def setUp(self):
        self.test = vnf.VnfOnBoarding(
            project='functest', case_name='aaa')
        self.test.project = "functest"
        self.test.start_time = "1"
        self.test.stop_time = "5"
        self.test.result = ""
        self.test.details = {
            "orchestrator": {"status": "PASS", "result": "", "duration": 20},
            "vnf": {"status": "PASS", "result": "", "duration": 15},
            "test_vnf": {"status": "FAIL", "result": "", "duration": 5}}
        self.test.keystone_client = 'test_client'
        self.test.tenant_name = 'test_tenant_name'

    def test_run_deploy_vnf_exception(self):
        with mock.patch.object(self.test, 'prepare'),\
            mock.patch.object(self.test, 'deploy_orchestrator',
                              return_value=None), \
            mock.patch.object(self.test, 'deploy_vnf',
                              side_effect=Exception):
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_TESTCASE_FAILED)

    def test_run_test_vnf_exception(self):
        with mock.patch.object(self.test, 'prepare'),\
            mock.patch.object(self.test, 'deploy_orchestrator',
                              return_value=None), \
            mock.patch.object(self.test, 'deploy_vnf'), \
            mock.patch.object(self.test, 'test_vnf',
                              side_effect=Exception):
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_TESTCASE_FAILED)

    def test_run_deploy_orchestrator_fail(self):
        with mock.patch.object(self.test, 'prepare'),\
                mock.patch.object(self.test, 'deploy_orchestrator',
                                  return_value=False), \
                mock.patch.object(self.test, 'deploy_vnf',
                                  return_value=True), \
                mock.patch.object(self.test, 'test_vnf',
                                  return_value=True):
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_TESTCASE_FAILED)

    def test_run_vnf_deploy_fail(self):
        with mock.patch.object(self.test, 'prepare'),\
                mock.patch.object(self.test, 'deploy_orchestrator',
                                  return_value=True), \
                mock.patch.object(self.test, 'deploy_vnf',
                                  return_value=False), \
                mock.patch.object(self.test, 'test_vnf',
                                  return_value=True):
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_TESTCASE_FAILED)

    def test_run_vnf_test_fail(self):
        with mock.patch.object(self.test, 'prepare'),\
                mock.patch.object(self.test, 'deploy_orchestrator',
                                  return_value=True), \
                mock.patch.object(self.test, 'deploy_vnf',
                                  return_value=True), \
                mock.patch.object(self.test, 'test_vnf',
                                  return_value=False):
            self.assertEqual(self.test.run(),
                             testcase.TestCase.EX_TESTCASE_FAILED)

    def test_run_default(self):
        with mock.patch.object(self.test, 'prepare'),\
                mock.patch.object(self.test, 'deploy_orchestrator',
                                  return_value=True), \
                mock.patch.object(self.test, 'deploy_vnf',
                                  return_value=True), \
                mock.patch.object(self.test, 'test_vnf',
                                  return_value=True):
            self.assertEqual(self.test.run(), testcase.TestCase.EX_OK)

    def test_deploy_vnf_unimplemented(self):
        with self.assertRaises(vnf.VnfDeploymentException):
            self.test.deploy_vnf()

    def test_test_vnf_unimplemented(self):
        with self.assertRaises(vnf.VnfTestException):
            self.test.test_vnf()

    @mock.patch('functest.core.vnf.os_utils.delete_user',
                return_value=True)
    def test_clean_user_set(self, mock_method=None):
        self.test.user_created = True
        self.test.clean()
        mock_method.assert_called_once_with('test_client',
                                            'test_tenant_name')

    @mock.patch('functest.core.vnf.os_utils.delete_user',
                return_value=False)
    def test_clean_user_unset(self, mock_method=None):
        self.test.user_created = False
        self.test.clean()
        mock_method.assert_not_called()

    @mock.patch('functest.core.vnf.os_utils.delete_tenant',
                return_value=True)
    def test_clean_tenant_set(self, mock_method=None):
        self.test.tenant_created = True
        self.test.clean()
        mock_method.assert_called_once_with('test_client',
                                            'test_tenant_name')

    @mock.patch('functest.core.vnf.os_utils.delete_tenant',
                return_value=True)
    def test_clean_tenant_unset(self, mock_method=None):
        self.test.tenant_created = False
        self.test.clean()
        mock_method.assert_not_called()

    def test_deploy_orchestrator_unimplemented(self):
        self.assertTrue(self.test.deploy_orchestrator())

    @mock.patch('functest.core.vnf.os_utils.get_credentials',
                return_value={'creds': 'test'})
    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                return_value=0)
    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
                return_value=0)
    def test_prepare_create_user_and_tenant(self, *args):
        self.assertEqual(self.test.prepare(),
                         testcase.TestCase.EX_OK)

    @mock.patch('functest.core.vnf.os_utils.get_credentials',
                side_effect=Exception)
    def test_prepare_error_admin_creds(self, *args):
        with self.assertRaises(vnf.VnfPreparationException):
            self.test.prepare()

    @mock.patch('functest.core.vnf.os_utils.get_credentials',
                return_value='creds')
    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                side_effect=Exception)
    def test_prepare_error_keystone_client(self, *args):
        with self.assertRaises(vnf.VnfPreparationException):
            self.test.prepare()

    @mock.patch('functest.core.vnf.os_utils.get_credentials',
                return_value='creds')
    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                side_effect=Exception)
    def test_prepare_error_tenant_creation(self, *args):
        with self.assertRaises(vnf.VnfPreparationException):
            self.test.prepare()

    @mock.patch('functest.core.vnf.os_utils.get_credentials',
                return_value='creds')
    @mock.patch('functest.core.vnf.os_utils.get_keystone_client',
                return_value='test')
    @mock.patch('functest.core.vnf.os_utils.get_or_create_tenant_for_vnf',
                return_value=0)
    @mock.patch('functest.core.vnf.os_utils.get_or_create_user_for_vnf',
                side_effect=Exception)
    def test_prepare_error_user_creation(self, *args):
        with self.assertRaises(vnf.VnfPreparationException):
            self.test.prepare()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
