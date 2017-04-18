#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the parent class of all Functest TestCases."""

import os

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class TestCase(object):
    """Parent class of Functest TestCase."""

    EX_OK = os.EX_OK
    """Status code returned when everything is OK"""

    EX_RUN_ERROR = os.EX_SOFTWARE
    """Status code returned when run() fails"""

    EX_PUSH_TO_DB_ERROR = os.EX_SOFTWARE - 1
    """Status code returned when push_to_db() fails"""

    EX_TESTCASE_FAILED = os.EX_SOFTWARE - 2
    """Status code returned when results are false"""

    logger = ft_logger.Logger(__name__).getLogger()

    def __init__(self, **kwargs):
        self.details = {}
        self.project_name = kwargs.get('project_name', 'functest')
        self.case_name = kwargs.get('case_name', '')
        self.criteria = ""
        self.start_time = ""
        self.stop_time = ""

    def check_criteria(self):
        """Interpret the results of TestCase.

        It allows getting the results of TestCase. It completes run()
        which only returns the execution status.

        It can be overriden if checking criteria is not suitable.

        Returns:
            TestCase.EX_OK if criteria is 'PASS'.
            TestCase.EX_TESTCASE_FAILED otherwise.
        """
        try:
            assert self.criteria
            if self.criteria == 'PASS':
                return TestCase.EX_OK
        except AssertionError:
            self.logger.error("Please run test before checking the results")
        return TestCase.EX_TESTCASE_FAILED

    def run(self, **kwargs):
        """Run TestCase.

        It allows running TestCase and getting its execution
        status.

        The subclasses must override the default implementation which
        is false on purpose. The only prerequisite is to set the
        following attributes to push the results to DB:

            * case_name,
            * criteria,
            * start_time,
            * stop_time.

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            TestCase.EX_RUN_ERROR.
        """
        # pylint: disable=unused-argument
        self.logger.error("Run must be implemented")
        return TestCase.EX_RUN_ERROR

    def push_to_db(self):
        """Push the results of TestCase to the DB.

        It allows publishing the results and to check the status.

        It could be overriden if the common implementation is not
        suitable. The following attributes must be set before pushing
        the results to DB:

            * project_name,
            * case_name,
            * criteria,
            * start_time,
            * stop_time.

        Returns:
            TestCase.EX_OK if results were pushed to DB.
            TestCase.EX_PUSH_TO_DB_ERROR otherwise.
        """
        try:
            assert self.project_name
            assert self.case_name
            assert self.criteria
            assert self.start_time
            assert self.stop_time
            if ft_utils.push_results_to_db(
                    self.project_name, self.case_name, self.start_time,
                    self.stop_time, self.criteria, self.details):
                self.logger.info("The results were successfully pushed to DB")
                return TestCase.EX_OK
            else:
                self.logger.error("The results cannot be pushed to DB")
                return TestCase.EX_PUSH_TO_DB_ERROR
        except Exception:  # pylint: disable=broad-except
            self.logger.exception("The results cannot be pushed to DB")
            return TestCase.EX_PUSH_TO_DB_ERROR
