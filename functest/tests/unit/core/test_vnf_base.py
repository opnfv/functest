#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest

from functest.core import vnf_base


class TestCasesBaseTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.test = vnf_base.VnfOnBoardingBase()
        self.test.project = "functest"
        self.test.case_name = "fake_vnf"
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

    def test_deploy_vnf_unimplemented(self):
        with self.assertRaises(Exception) as context:
            self.test.deploy_vnf()
        self.assertTrue('VNF not deployed' in context.exception)

    def test_test_vnf_unimplemented(self):
        with self.assertRaises(Exception) as context:
            self.test.test_vnf()()
        self.assertTrue('VNF not tested' in context.exception)

    def test_parse_results(self):
        self.assertNotEqual(self.test.parse_results(), 0)

# TO be removed => already tested in tectcasebase tests?
    @mock.patch('functest.utils.functest_utils.push_results_to_db',
                return_value=False)
    def _test_missing_attribute(self, mock_function):
        self.assertEqual(self.test.push_to_db(),
                         vnf_base.VnfOnBoardingBase.EX_PUSH_TO_DB_ERROR)
        mock_function.assert_not_called()

    def test_missing_case_name(self):
        self.test.case_name = None
        self._test_missing_attribute()

    def test_missing_criteria(self):
        self.test.criteria = None
        self._test_missing_attribute()

    def test_missing_start_time(self):
        self.test.start_time = None
        self._test_missing_attribute()

    def test_missing_stop_time(self):
        self.test.stop_time = None
        self._test_missing_attribute()

if __name__ == "__main__":
    unittest.main(verbosity=2)
