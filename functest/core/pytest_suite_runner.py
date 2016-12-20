#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import testcase_base as base
import unittest
import time


class PyTestSuiteRunner(base.TestcaseBase):
    """
    This superclass is designed to execute pre-configured unittest.TestSuite()
    objects
    """
    def __init__(self):
        super(PyTestSuiteRunner, self).__init__()
        self.suite = None

    def run(self, **kwargs):
        """
        Starts test execution from the functest framework
        """
        self.start_time = time.time()
        result = unittest.TextTestRunner(verbosity=2).run(self.suite)
        self.stop_time = time.time()

        if result.errors:
            self.logger.error('Number of errors in test suite - ' +
                              str(len(result.errors)))
            for test, message in result.errors:
                self.logger.error(str(test) + " ERROR with " + message)

        if result.failures:
            self.logger.error('Number of failures in test suite - ' +
                              str(len(result.failures)))
            for test, message in result.failures:
                self.logger.error(str(test) + " FAILED with " + message)

        if ((result.errors and len(result.errors) > 0)
                or (result.failures and len(result.failures) > 0)):
            self.logger.info("%s FAILED" % self.case_name)
            self.criteria = 'FAIL'
            exit_code = base.TestcaseBase.EX_RUN_ERROR
        else:
            self.logger.info("%s OK" % self.case_name)
            exit_code = base.TestcaseBase.EX_OK
            self.criteria = 'PASS'

        self.details = {}
        return exit_code
