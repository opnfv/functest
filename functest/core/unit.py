#!/usr/bin/env python

# Copyright (c) 2016 Cable Television Laboratories, Inc. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the parent class to run unittest.TestSuite as TestCase."""

from __future__ import division

import logging
import time
import unittest

import six

from functest.core import testcase

__author__ = ("Steven Pisarski <s.pisarski@cablelabs.com>, "
              "Cedric Ollivier <cedric.ollivier@orange.com>")


class Suite(testcase.TestCase):
    """Base model for running unittest.TestSuite."""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        super(Suite, self).__init__(**kwargs)
        self.suite = None

    def run(self, **kwargs):
        """Run the test suite.

        It allows running any unittest.TestSuite and getting its
        execution status.

        By default, it runs the suite defined as instance attribute.
        It can be overriden by passing name as arg. It must
        conform with TestLoader.loadTestsFromName().

        It sets the following attributes required to push the results
        to DB:

            * result,
            * start_time,
            * stop_time,
            * details.

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            TestCase.EX_OK if any TestSuite has been run,
            TestCase.EX_RUN_ERROR otherwise.
        """
        try:
            name = kwargs["name"]
            try:
                self.suite = unittest.TestLoader().loadTestsFromName(name)
            except ImportError:
                self.__logger.error("Can not import %s", name)
                return testcase.TestCase.EX_RUN_ERROR
        except KeyError:
            pass
        try:
            assert self.suite
            self.start_time = time.time()
            stream = six.StringIO()
            result = unittest.TextTestRunner(
                stream=stream, verbosity=2).run(self.suite)
            self.__logger.debug("\n\n%s", stream.getvalue())
            self.stop_time = time.time()
            self.details = {
                "testsRun": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "stream": stream.getvalue()}
            self.result = 100 * (
                (result.testsRun - (len(result.failures) +
                                    len(result.errors))) /
                result.testsRun)
            return testcase.TestCase.EX_OK
        except AssertionError:
            self.__logger.error("No suite is defined")
            return testcase.TestCase.EX_RUN_ERROR
        except ZeroDivisionError:
            self.__logger.error("No test has been run")
            return testcase.TestCase.EX_RUN_ERROR
