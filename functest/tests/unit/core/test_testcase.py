#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the classe required to fully cover testcase."""

import logging
import unittest

import mock

from functest.core import testcase

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class TestCaseTesting(unittest.TestCase):

    """The class testing TestCase."""
    # pylint: disable=missing-docstring

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.test = testcase.TestCase()
        self.test.project = "functest"
        self.test.case_name = "base"
        self.test.start_time = "1"
        self.test.stop_time = "2"
        self.test.criteria = "PASS"
        self.test.details = {"Hello": "World"}

    def test_run_unimplemented(self):
        self.assertEqual(self.test.run(),
                         testcase.TestCase.EX_RUN_ERROR)

    @mock.patch('functest.utils.functest_utils.push_results_to_db',
                return_value=False)
    def _test_missing_attribute(self, mock_function=None):
        self.assertEqual(self.test.push_to_db(),
                         testcase.TestCase.EX_PUSH_TO_DB_ERROR)
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
    def test_missing_details(self, mock_function=None):
        self.test.details = None
        self.assertEqual(self.test.push_to_db(),
                         testcase.TestCase.EX_OK)
        mock_function.assert_called_once_with(
            self.test.project, self.test.case_name, self.test.start_time,
            self.test.stop_time, self.test.criteria, self.test.details)

    @mock.patch('functest.utils.functest_utils.push_results_to_db',
                return_value=False)
    def test_push_to_db_failed(self, mock_function=None):
        self.assertEqual(self.test.push_to_db(),
                         testcase.TestCase.EX_PUSH_TO_DB_ERROR)
        mock_function.assert_called_once_with(
            self.test.project, self.test.case_name, self.test.start_time,
            self.test.stop_time, self.test.criteria, self.test.details)

    @mock.patch('functest.utils.functest_utils.push_results_to_db',
                return_value=True)
    def test_push_to_db(self, mock_function=None):
        self.assertEqual(self.test.push_to_db(),
                         testcase.TestCase.EX_OK)
        mock_function.assert_called_once_with(
            self.test.project, self.test.case_name, self.test.start_time,
            self.test.stop_time, self.test.criteria, self.test.details)

    def test_check_criteria_missing(self):
        self.test.criteria = None
        self.assertEqual(self.test.check_criteria(),
                         testcase.TestCase.EX_TESTCASE_FAILED)

    def test_check_criteria_failed(self):
        self.test.criteria = 'FAILED'
        self.assertEqual(self.test.check_criteria(),
                         testcase.TestCase.EX_TESTCASE_FAILED)

    def test_check_criteria_pass(self):
        self.test.criteria = 'PASS'
        self.assertEqual(self.test.check_criteria(),
                         testcase.TestCase.EX_OK)


if __name__ == "__main__":
    unittest.main(verbosity=2)
