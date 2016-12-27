#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from opnfv.utils.constants import Constants

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils


class TestcaseBase(Constants):

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
                return TestcaseBase.EX_OK
        except:
            self.logger.error("Please run test before checking the results")
        return TestcaseBase.EX_TEST_FAIL

    def run(self, **kwargs):
        self.logger.error("Run must be implemented")
        return TestcaseBase.EX_RUN_ERROR

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
                return TestcaseBase.EX_OK
            else:
                self.logger.error("The results cannot be pushed to DB")
                return TestcaseBase.EX_PUSH_RESULT_FAIL
        except Exception:
            self.logger.exception("The results cannot be pushed to DB")
            return TestcaseBase.EX_PUSH_RESULT_FAIL
