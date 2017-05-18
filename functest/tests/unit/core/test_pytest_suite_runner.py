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
        self.result = mock.Mock()
        attrs = {'errors': [('test1', 'error_msg1')],
                 'failures': [('test2', 'failure_msg1')]}
        self.result.configure_mock(**attrs)

        self.pass_results = mock.Mock()
        attrs = {'errors': None,
                 'failures': None}
        self.pass_results.configure_mock(**attrs)

    def test_run(self):
        self.psrunner.case_name = 'test_case_name'
        with mock.patch('functest.core.pytest_suite_runner.'
                        'unittest.TextTestRunner.run',
                        return_value=self.result):
            self.assertEqual(self.psrunner.run(),
                             testcase.TestCase.EX_OK)

        with mock.patch('functest.core.pytest_suite_runner.'
                        'unittest.TextTestRunner.run',
                        return_value=self.pass_results):
            self.assertEqual(self.psrunner.run(),
                             testcase.TestCase.EX_OK)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
