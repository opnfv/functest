# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

from __future__ import division

import logging
import time
import unittest

import six

from functest.core import testcase


class PyTestSuiteRunner(testcase.TestCase):
    """
    This superclass is designed to execute pre-configured unittest.TestSuite()
    objects
    """

    def __init__(self, **kwargs):
        super(PyTestSuiteRunner, self).__init__(**kwargs)
        self.suite = None
        self.logger = logging.getLogger(__name__)

    def run(self, **kwargs):
        """
        Starts test execution from the functest framework
        """
        try:
            name = kwargs["name"]
            try:
                self.suite = unittest.TestLoader().loadTestsFromName(name)
            except ImportError:
                self.logger.error("Can not import %s", name)
                return testcase.TestCase.EX_RUN_ERROR
        except KeyError:
            pass
        self.start_time = time.time()
        stream = six.StringIO()
        result = unittest.TextTestRunner(
            stream=stream, verbosity=2).run(self.suite)
        self.logger.debug("\n\n%s", stream.getvalue())
        self.stop_time = time.time()
        self.details = {"failures": result.failures,
                        "errors": result.errors}
        try:
            self.result = 100 * (
                (result.testsRun - (len(result.failures) +
                                    len(result.errors))) /
                result.testsRun)
            return testcase.TestCase.EX_OK
        except ZeroDivisionError:
            self.logger.error("No test has been run")
            return testcase.TestCase.EX_RUN_ERROR
