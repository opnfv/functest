#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock

from functest.core import pytest_suite_runner
from functest.core import testcase


class PyTestSuiteRunnerTesting(unittest.TestCase):

    def setUp(self):
        self.psrunner = pytest_suite_runner.PyTestSuiteRunner()

    def _test_run(self, result, status=testcase.TestCase.EX_OK):
        with mock.patch('functest.core.pytest_suite_runner.'
                        'unittest.TextTestRunner.run',
                        return_value=result):
            self.assertEqual(self.psrunner.run(), status)

    def test_run_no_ut(self):
        mock_result = mock.Mock(testsRun=0, errors=[], failures=[])
        self._test_run(mock_result, testcase.TestCase.EX_RUN_ERROR)
        self.assertEqual(self.psrunner.result, 0)
        self.assertEqual(self.psrunner.details, {'errors': [], 'failures': []})
        self.assertEqual(self.psrunner.is_successful(),
                         testcase.TestCase.EX_TESTCASE_FAILED)

    def test_run_ko(self):
        self.psrunner.criteria = 100
        mock_result = mock.Mock(testsRun=50, errors=[('test1', 'error_msg1')],
                                failures=[('test2', 'failure_msg1')])
        self._test_run(mock_result, testcase.TestCase.EX_OK)
        self.assertEqual(self.psrunner.result, 96)
        self.assertEqual(self.psrunner.details,
                         {'errors': [('test1', 'error_msg1')],
                          'failures': [('test2', 'failure_msg1')]})
        self.assertEqual(self.psrunner.is_successful(),
                         testcase.TestCase.EX_TESTCASE_FAILED)

    def test_run_ok(self):
        mock_result = mock.Mock(testsRun=50, errors=[],
                                failures=[])
        self._test_run(mock_result)
        self.assertEqual(self.psrunner.result, 100)
        self.assertEqual(self.psrunner.details, {'errors': [], 'failures': []})
        self.assertEqual(self.psrunner.is_successful(),
                         testcase.TestCase.EX_OK)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
