#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import os
import sys

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils


class TestCasesBase(object):

    EX_OK = os.EX_OK
    EX_RUN_ERROR = os.EX_SOFTWARE
    EX_PUSH_TO_DB_ERROR = os.EX_SOFTWARE - 1

    logger = ft_logger.Logger(__name__).getLogger()

    def __init__(self, project='functest', case=''):
        self.details = {}
        self.project_name = project
        self.case_name = case
        self.criteria = ""
        self.start_time = ""
        self.stop_time = ""

        self.results_dir = self.get_conf('general.directories.dir_results')

    def run(self, **kwargs):
        self.logger.error("Run must be implemented")
        return TestCasesBase.EX_RUN_ERROR

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
                return TestCasesBase.EX_OK
            else:
                self.logger.error("The results cannot be pushed to DB")
                return TestCasesBase.EX_PUSH_TO_DB_ERROR
        except Exception:
            self.logger.exception("The results cannot be pushed to DB")
            return TestCasesBase.EX_PUSH_TO_DB_ERROR

    @classmethod
    def main(project_cls, args_parser, **kwargs):
        args = vars(args_parser.parse_args())
        project_obj = project_cls()
        try:
            result = project_obj.run(**args)
            if result != TestCasesBase.EX_OK:
                sys.exit(result)
            if args['report']:
                sys.exit(project_obj.push_to_db())
        except Exception:
            sys.exit(TestCasesBase.EX_RUN_ERROR)


    @staticmethod
    def get_conf(parameter):
        return ft_utils.get_functest_config(parameter)

    @staticmethod
    def parser_results(test_name, ret, start_time, stop_time):
        def get_criteria_value():
            return ft_utils.get_criteria_by_test(test_name).split('==')[1].strip()

        status = 'FAIL'
        if str(ret) == get_criteria_value():
            status = 'PASS'

        details = {
            'timestart': start_time,
            'duration': round(stop_time - start_time, 1),
            'status': status,
        }

        return status, details
