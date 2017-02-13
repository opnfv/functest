#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import os
import unittest

import mock

from functest.core import vnf_base
from functest.core import testcase_base as base


class VnfBaseTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.test = vnf_base.VnfOnBoardingBase(project='functest',
                                               case='aaa')
        self.test.project = "functest"
        self.test.case_name = "aaa"
        self.test.start_time = "1"
        self.test.stop_time = "5"
        self.test.criteria = ""
        self.test.details = {"orchestrator": {"status": "PASS",
                                              "result": "",
                                              "duration": 20},
                             "vnf": {"status": "PASS",
                                     "result": "",
                                     "duration": 15},
                             "test_vnf": {"status": "FAIL",
                                          "result": "",
                                          "duration": 5}}
        self.test.keystone_client = 'test_client'
        self.test.tenant_name = 'test_tenant_name'

    def test_execute_deploy_vnf_fail(self):
        with mock.patch.object(self.test, 'prepare'),\
            mock.patch.object(self.test, 'deploy_orchestrator',
                              return_value=None), \
            mock.patch.object(self.test, 'deploy_vnf',
                              side_effect=Exception):
            self.assertEqual(self.test.execute(),
                             base.TestcaseBase.EX_TESTCASE_FAILED)

    def test_execute_test_vnf_fail(self):
        with mock.patch.object(self.test, 'prepare'),\
            mock.patch.object(self.test, 'deploy_orchestrator',
                              return_value=None), \
            mock.patch.object(self.test, 'deploy_vnf'), \
            mock.patch.object(self.test, 'test_vnf',
                              side_effect=Exception):
            self.assertEqual(self.test.execute(),
                             base.TestcaseBase.EX_TESTCASE_FAILED)

    def test_execute_default(self):
        with mock.patch.object(self.test, 'prepare'),\
            mock.patch.object(self.test, 'deploy_orchestrator',
                              return_value=None), \
            mock.patch.object(self.test, 'deploy_vnf'), \
            mock.patch.object(self.test, 'test_vnf'), \
            mock.patch.object(self.test, 'parse_results',
                              return_value='ret_exit_code'), \
            mock.patch.object(self.test, 'log_results'), \
            mock.patch('functest.core.vnf_base.os_utils.get_tenant_id',
                       return_value='test_tenant_id'), \
            mock.patch('functest.core.vnf_base.os_utils.delete_tenant',
                       return_value=True), \
            mock.patch('functest.core.vnf_base.os_utils.get_user_id',
                       return_value='test_user_id'), \
            mock.patch('functest.core.vnf_base.os_utils.delete_user',
                       return_value=True):
            self.assertEqual(self.test.execute(),
                             'ret_exit_code')

    def test_prepare_missing_userid(self):
        with mock.patch('functest.core.vnf_base.'
                        'os_utils.get_credentials'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_keystone_client'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_user_id',
                       return_value=''), \
                self.assertRaises(Exception):
            self.test.prepare()

    def test_prepare_missing_tenantid(self):
        with mock.patch('functest.core.vnf_base.'
                        'os_utils.get_credentials'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_keystone_client'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_user_id',
                       return_value='test_roleid'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.create_tenant',
                       return_value=''), \
                self.assertRaises(Exception):
            self.test.prepare()

    def test_prepare_missing_roleid(self):
        with mock.patch('functest.core.vnf_base.'
                        'os_utils.get_credentials'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_keystone_client'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_user_id',
                       return_value='test_roleid'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.create_tenant',
                       return_value='test_tenantid'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_role_id',
                       return_value=''), \
                self.assertRaises(Exception):
            self.test.prepare()

    def test_prepare_role_add_failure(self):
        with mock.patch('functest.core.vnf_base.'
                        'os_utils.get_credentials'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_keystone_client'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_user_id',
                       return_value='test_roleid'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.create_tenant',
                       return_value='test_tenantid'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_role_id',
                       return_value='test_roleid'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.add_role_user',
                       return_value=''), \
                self.assertRaises(Exception):
            self.test.prepare()

    def test_prepare_create_user_failure(self):
        with mock.patch('functest.core.vnf_base.'
                        'os_utils.get_credentials'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_keystone_client'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_user_id',
                       return_value='test_roleid'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.create_tenant',
                       return_value='test_tenantid'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.get_role_id',
                       return_value='test_roleid'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.add_role_user'), \
            mock.patch('functest.core.vnf_base.'
                       'os_utils.create_user',
                       return_value=''), \
                self.assertRaises(Exception):
            self.test.prepare()

    def test_log_results_default(self):
        with mock.patch('functest.core.vnf_base.'
                        'ft_utils.logger_test_results') \
                as m:
            self.test.log_results()
            self.assertTrue(m.called)

    def test_step_failures_default(self):
        with self.assertRaises(Exception):
            self.test.step_failure()

    def test_deploy_vnf_unimplemented(self):
        with self.assertRaises(Exception) as context:
            self.test.deploy_vnf()
        self.assertTrue('VNF not deployed' in context.exception)

    def test_test_vnf_unimplemented(self):
        with self.assertRaises(Exception) as context:
            self.test.test_vnf()()
        self.assertTrue('VNF not tested' in context.exception)

    def test_parse_results_ex_ok(self):
        self.test.details['test_vnf']['status'] = 'PASS'
        self.assertEqual(self.test.parse_results(), os.EX_OK)

    def test_parse_results_ex_run_error(self):
        self.test.details['vnf']['status'] = 'FAIL'
        self.assertEqual(self.test.parse_results(), os.EX_SOFTWARE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
