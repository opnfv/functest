#!/usr/bin/env python

import logging
import mock
import unittest

import TestCasesBase


class TestCasesBaseTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.test = TestCasesBase.TestCasesBase()
        self.test.project = "functest"
        self.test.case_name = "base"
        self.test.start_time = "1"
        self.test.stop_time = "2"
        self.test.criteria = "100"
        self.test.details = {"Hello":  "World"}

    def test_run_unimplemented(self):
        self.assertEqual(self.test.run(),
                         TestCasesBase.TestCasesBase.EX_RUN_ERROR)

    def _test_missing_attribute(self):
        with mock.patch('functest.utils.functest_utils.push_results_to_db',
                        return_value=False) as mock_function:
            self.assertEqual(self.test.push_to_db(),
                             TestCasesBase.TestCasesBase.EX_PUSH_TO_DB_ERROR)
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

    def test_missing_details(self):
        self.test.details = None
        with mock.patch('functest.utils.functest_utils.push_results_to_db',
                        return_value=True) as mock_function:
            self.assertEqual(self.test.push_to_db(),
                             TestCasesBase.TestCasesBase.EX_OK)
            mock_function.assert_called_once_with(
                self.test.project, self.test.case_name, self.test.start_time,
                self.test.stop_time, self.test.criteria, self.test.details)

    def test_push_to_db_failed(self):
        with mock.patch('functest.utils.functest_utils.push_results_to_db',
                        return_value=False) as mock_function:
            self.assertEqual(self.test.push_to_db(),
                             TestCasesBase.TestCasesBase.EX_PUSH_TO_DB_ERROR)
            mock_function.assert_called_once_with(
                self.test.project, self.test.case_name, self.test.start_time,
                self.test.stop_time, self.test.criteria, self.test.details)

    def test_push_to_db(self):
        with mock.patch('functest.utils.functest_utils.push_results_to_db',
                        return_value=True) as mock_function:
            self.assertEqual(self.test.push_to_db(),
                             TestCasesBase.TestCasesBase.EX_OK)
            mock_function.assert_called_once_with(
                self.test.project, self.test.case_name, self.test.start_time,
                self.test.stop_time, self.test.criteria, self.test.details)


if __name__ == "__main__":
    unittest.main(verbosity=2)
