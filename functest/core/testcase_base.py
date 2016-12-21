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
from functest.utils.constants import CONST


class TestcaseBase(object):

    EX_OK = os.EX_OK
    EX_RUN_ERROR = os.EX_SOFTWARE
    EX_PUSH_TO_DB_ERROR = os.EX_SOFTWARE - 1
    EX_TESTCASE_FAILED = os.EX_SOFTWARE - 2
    EX_WRITE_TO_FILE_ERROR = os.EX_SOFTWARE - 3

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
        return TestcaseBase.EX_TESTCASE_FAILED

    def run(self, **kwargs):
        self.logger.error("Run must be implemented")
        return TestcaseBase.EX_RUN_ERROR

    def publish_report(self):
        if os.environ['RESULTS']:
            CONST.results_test_db_url = os.environ['RESULTS']

        try:
            assert self.project_name
            assert self.case_name
            assert self.criteria
            assert self.start_time
            assert self.stop_time
            if CONST.results_test_db_url.lower().startswith("http:///") or \
                    CONST.results_test_db_url.lower().startswith("https:///"):
                self.push_to_db()
            elif CONST.results_test_db_url.lower().startswith("file:///"):
                self.write_to_file()
            else:
                self.logger.error("Please give a valid parameter for -r")
                return TestcaseBase.EX_RUN_ERROR
        except Exception:
            self.logger.exception("The results cannot be pushed to DB")
            return TestcaseBase.EX_PUSH_TO_DB_ERROR

    def write_to_file(self, path):
        if ft_utils.write_results_to_file(
                self.project_name, self.case_name, self.start_time,
                self.stop_time, self.criteria, self.details):
            self.logger.info("The results were successfully written to a file")
            return TestcaseBase.EX_OK
        else:
            self.logger.error("wrtie results to a file failed")
            return TestcaseBase.EX_WRITE_TO_FILE_ERROR

    def push_to_db(self, url):
        if ft_utils.push_results_to_db(
                self.project_name, self.case_name, self.start_time,
                self.stop_time, self.criteria, self.details):
            self.logger.info("The results were successfully pushed to DB")
            return TestcaseBase.EX_OK
        else:
            self.logger.error("The results cannot be pushed to DB")
            return TestcaseBase.EX_PUSH_TO_DB_ERROR
