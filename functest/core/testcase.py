#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import os

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils


class TestCase(object):

    EX_OK = os.EX_OK
    EX_RUN_ERROR = os.EX_SOFTWARE
    EX_PUSH_TO_DB_ERROR = os.EX_SOFTWARE - 1
    EX_TESTCASE_FAILED = os.EX_SOFTWARE - 2

    logger = ft_logger.Logger(__name__).getLogger()

    def __init__(self):
        self.details = {}
        self.project_name = "functest"
        self.case_name = ""
        self.criteria = ""
        self.start_time = ""
        self.stop_time = ""

    def check_criteria(self):
        try:
            assert self.criteria
            if self.criteria == 'PASS':
                return TestCase.EX_OK
        except AssertionError:
            self.logger.error("Please run test before checking the results")
        return TestCase.EX_TESTCASE_FAILED

    def run(self, **kwargs):
        # pylint: disable=unused-argument
        self.logger.error("Run must be implemented")
        return TestCase.EX_RUN_ERROR

    def push_to_db(self):
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
