#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import os
import unittest

from functest.core import testcase_base
from functest.utils.constants import CONST


class TestcaseBaseTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.test = testcase_base.TestcaseBase()
        self.test.project = "functest"
        self.test.case_name = "base"
        self.test.start_time = "1"
        self.test.stop_time = "2"
        self.test.criteria = "PASS"
        self.test.details = {"Hello": "World"}
        if "RESULTS_STORE" in os.environ:
            del os.environ["RESULTS_STORE"]

    def test_run_unimplemented(self):
        self.assertEqual(self.test.run(),
                         testcase_base.TestcaseBase.EX_RUN_ERROR)

    @mock.patch.dict(os.environ, {})
    @mock.patch('functest.utils.functest_utils.push_results_to_db',
                return_value=False)
    def _test_missing_attribute(self, mock_function):
        self.assertEqual(self.test.publish_report(),
                         testcase_base.TestcaseBase.EX_PUBLISH_RESULT_FAILED)
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

    @mock.patch('functest.utils.functest_utils.push_results_to_db',
                return_value=True)
    def test_missing_details(self, mock_function):
        self.test.details = None
        self.assertEqual(self.test.push_to_db(),
                         testcase_base.TestcaseBase.EX_OK)
        mock_function.assert_called_once_with(
            self.test.project, self.test.case_name, self.test.start_time,
            self.test.stop_time, self.test.criteria, self.test.details)

    @mock.patch('functest.utils.functest_utils.push_results_to_db',
                return_value=False)
    def test_push_to_db_failed(self, mock_function):
        self.assertEqual(self.test.push_to_db(),
                         testcase_base.TestcaseBase.EX_PUBLISH_RESULT_FAILED)
        mock_function.assert_called_once_with(
            self.test.project, self.test.case_name, self.test.start_time,
            self.test.stop_time, self.test.criteria, self.test.details)

    @mock.patch('functest.utils.functest_utils.push_results_to_db',
                return_value=True)
    def test_push_to_db(self, mock_function):
        self.assertEqual(self.test.push_to_db(),
                         testcase_base.TestcaseBase.EX_OK)
        mock_function.assert_called_once_with(
            self.test.project, self.test.case_name, self.test.start_time,
            self.test.stop_time, self.test.criteria, self.test.details)

    def test_check_criteria_missing(self):
        self.test.criteria = None
        self.assertEqual(self.test.check_criteria(),
                         testcase_base.TestcaseBase.EX_TESTCASE_FAILED)

    def test_check_criteria_failed(self):
        self.test.criteria = 'FAILED'
        self.assertEqual(self.test.check_criteria(),
                         testcase_base.TestcaseBase.EX_TESTCASE_FAILED)

    def test_check_criteria_pass(self):
        self.test.criteria = 'PASS'
        self.assertEqual(self.test.check_criteria(),
                         testcase_base.TestcaseBase.EX_OK)

    @mock.patch('functest.utils.functest_utils.write_results_to_file',
                return_value=False)
    def test_write_to_file_failed(self, mock_function):
        self.assertEqual(self.test.write_to_file(),
                         testcase_base.TestcaseBase.EX_PUBLISH_RESULT_FAILED)
        mock_function.assert_called_once_with(
            self.test.project, self.test.case_name, self.test.start_time,
            self.test.stop_time, self.test.criteria, self.test.details)

    @mock.patch('functest.utils.functest_utils.write_results_to_file',
                return_value=True)
    def test_write_to_file(self, mock_function):
        self.assertEqual(self.test.write_to_file(),
                         testcase_base.TestcaseBase.EX_OK)
        mock_function.assert_called_once_with(
            self.test.project, self.test.case_name, self.test.start_time,
            self.test.stop_time, self.test.criteria, self.test.details)

    def test_publish_report_no_conf(self):
        CONST.results_test_db_url = None
        self.assertEqual(self.test.publish_report(),
                         testcase_base.TestcaseBase.EX_PUBLISH_RESULT_FAILED)

    def test_publish_report_failed(self):
        CONST.results_test_db_url = "ftp://whatever"
        self.assertEqual(self.test.publish_report(),
                         testcase_base.TestcaseBase.EX_PUBLISH_RESULT_FAILED)

    @mock.patch('functest.core.testcase_base.TestcaseBase.push_to_db',
                return_value=testcase_base.TestcaseBase.EX_OK)
    def test_publish_report_http(self, mock_function):
        CONST.results_test_db_url = "http://whatever"
        self.test.publish_report()
        self.assertTrue(mock_function.called)

    @mock.patch('functest.core.testcase_base.TestcaseBase.write_to_file',
                return_value=testcase_base.TestcaseBase.EX_OK)
    def test_publish_report_file(self, mock_function):
        CONST.results_test_db_url = "file://whatever"
        self.test.publish_report()
        self.assertTrue(mock_function.called)

    def test_env_variable_result_store(self):
        CONST.results_test_db_url = "ping"
        os.environ["RESULTS_STORE"] = "pong"
        self.test.publish_report()
        self.assertTrue(CONST.results_test_db_url, "pong")


if __name__ == "__main__":
    unittest.main(verbosity=2)
