#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the parent class of all Functest TestCases."""

import logging
import os

import functest.utils.functest_utils as ft_utils

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class TestCase(object):
    """Base model for single test case."""

    EX_OK = os.EX_OK
    """everything is OK"""

    EX_RUN_ERROR = os.EX_SOFTWARE
    """run() failed"""

    EX_PUSH_TO_DB_ERROR = os.EX_SOFTWARE - 1
    """push_to_db() failed"""

    EX_TESTCASE_FAILED = os.EX_SOFTWARE - 2
    """results are false"""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        self.details = {}
        self.project_name = kwargs.get('project_name', 'functest')
        self.case_name = kwargs.get('case_name', '')
        self.criteria = kwargs.get('criteria', 100)
        self.result = 0
        self.start_time = 0
        self.stop_time = 0

    def get_duration(self):
        """Return the duration of the test case.

        Returns:
            duration if start_time and stop_time are set
            "XX:XX" otherwise.
        """
        try:
            assert self.start_time
            assert self.stop_time
            if self.stop_time < self.start_time:
                return "XX:XX"
            return "{0[0]:02.0f}:{0[1]:02.0f}".format(divmod(
                self.stop_time - self.start_time, 60))
        except Exception:
            self.__logger.error("Please run test before getting the duration")
            return "XX:XX"

    def is_successful(self):
        """Interpret the result of the test case.

        It allows getting the result of TestCase. It completes run()
        which only returns the execution status.

        It can be overriden if checking result is not suitable.

        Returns:
            TestCase.EX_OK if result is 'PASS'.
            TestCase.EX_TESTCASE_FAILED otherwise.
        """
        try:
            assert self.criteria
            if (not isinstance(self.result, str) and
                    not isinstance(self.criteria, str)):
                if self.result >= self.criteria:
                    return TestCase.EX_OK
            else:
                # Backward compatibility
                # It must be removed as soon as TestCase subclasses
                # stop setting result = 'PASS' or 'FAIL'.
                # In this case criteria is unread.
                self.__logger.warning(
                    "Please update result which must be an int!")
                if self.result == 'PASS':
                    return TestCase.EX_OK
        except AssertionError:
            self.__logger.error("Please run test before checking the results")
        return TestCase.EX_TESTCASE_FAILED

    def run(self, **kwargs):
        """Run the test case.

        It allows running TestCase and getting its execution
        status.

        The subclasses must override the default implementation which
        is false on purpose.

        The new implementation must set the following attributes to
        push the results to DB:

            * result,
            * start_time,
            * stop_time.

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            TestCase.EX_RUN_ERROR.
        """
        # pylint: disable=unused-argument
        self.__logger.error("Run must be implemented")
        return TestCase.EX_RUN_ERROR

    def push_to_db(self):
        """Push the results of the test case to the DB.

        It allows publishing the results and to check the status.

        It could be overriden if the common implementation is not
        suitable. The following attributes must be set before pushing
        the results to DB:

            * project_name,
            * case_name,
            * result,
            * start_time,
            * stop_time.

        Returns:
            TestCase.EX_OK if results were pushed to DB.
            TestCase.EX_PUSH_TO_DB_ERROR otherwise.
        """
        try:
            assert self.project_name
            assert self.case_name
            assert self.start_time
            assert self.stop_time
            pub_result = 'PASS' if self.is_successful(
                ) == TestCase.EX_OK else 'FAIL'
            if ft_utils.push_results_to_db(
                    self.project_name, self.case_name, self.start_time,
                    self.stop_time, pub_result, self.details):
                self.__logger.info(
                    "The results were successfully pushed to DB")
                return TestCase.EX_OK
            else:
                self.__logger.error("The results cannot be pushed to DB")
                return TestCase.EX_PUSH_TO_DB_ERROR
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("The results cannot be pushed to DB")
            return TestCase.EX_PUSH_TO_DB_ERROR
