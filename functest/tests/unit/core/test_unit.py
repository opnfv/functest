#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock

from functest.core import unit
from functest.core import testcase


class PyTestSuiteRunnerTesting(unittest.TestCase):

    def setUp(self):
        self.psrunner = unit.Suite()
        self.psrunner.suite = "foo"

    @mock.patch('unittest.TestLoader')
    def _test_run(self, mock_class=None, result=mock.Mock(),
                  status=testcase.TestCase.EX_OK):
        with mock.patch('functest.core.unit.unittest.TextTestRunner.run',
                        return_value=result):
            self.assertEqual(self.psrunner.run(), status)
            mock_class.assert_not_called()

    def test_check_suite_null(self):
        self.assertEqual(unit.Suite().suite, None)
        self.psrunner.suite = None
        self._test_run(result=mock.Mock(),
                       status=testcase.TestCase.EX_RUN_ERROR)

    def test_run_no_ut(self):
        mock_result = mock.Mock(testsRun=0, errors=[], failures=[])
        self._test_run(result=mock_result,
                       status=testcase.TestCase.EX_RUN_ERROR)
        self.assertEqual(self.psrunner.result, 0)
        self.assertEqual(self.psrunner.details,
                         {'errors': 0, 'failures': 0, 'stream': '',
                          'testsRun': 0})
        self.assertEqual(self.psrunner.is_successful(),
                         testcase.TestCase.EX_TESTCASE_FAILED)

    def test_run_result_ko(self):
        self.psrunner.criteria = 100
        mock_result = mock.Mock(testsRun=50, errors=[('test1', 'error_msg1')],
                                failures=[('test2', 'failure_msg1')])
        self._test_run(result=mock_result)
        self.assertEqual(self.psrunner.result, 96)
        self.assertEqual(self.psrunner.details,
                         {'errors': 1, 'failures': 1, 'stream': '',
                          'testsRun': 50})
        self.assertEqual(self.psrunner.is_successful(),
                         testcase.TestCase.EX_TESTCASE_FAILED)

    def test_run_result_ok(self):
        mock_result = mock.Mock(testsRun=50, errors=[],
                                failures=[])
        self._test_run(result=mock_result)
        self.assertEqual(self.psrunner.result, 100)
        self.assertEqual(self.psrunner.details,
                         {'errors': 0, 'failures': 0, 'stream': '',
                          'testsRun': 50})
        self.assertEqual(self.psrunner.is_successful(),
                         testcase.TestCase.EX_OK)

    @mock.patch('unittest.TestLoader')
    def test_run_name_exc(self, mock_class=None):
        mock_obj = mock.Mock(side_effect=ImportError)
        mock_class.side_effect = mock_obj
        self.assertEqual(self.psrunner.run(name='foo'),
                         testcase.TestCase.EX_RUN_ERROR)
        mock_class.assert_called_once_with()
        mock_obj.assert_called_once_with()

    @mock.patch('unittest.TestLoader')
    def test_run_name(self, mock_class=None):
        mock_result = mock.Mock(testsRun=50, errors=[],
                                failures=[])
        mock_obj = mock.Mock()
        mock_class.side_effect = mock_obj
        with mock.patch('functest.core.unit.unittest.TextTestRunner.run',
                        return_value=mock_result):
            self.assertEqual(self.psrunner.run(name='foo'),
                             testcase.TestCase.EX_OK)
        mock_class.assert_called_once_with()
        mock_obj.assert_called_once_with()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
