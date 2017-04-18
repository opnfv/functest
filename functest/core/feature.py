#!/usr/bin/env python

# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import time

import functest.core.testcase as base
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger
from functest.utils.constants import CONST


class Feature(base.TestCase):

    def __init__(self, **kwargs):
        super(Feature, self).__init__(**kwargs)
        self.result_file = "{}/{}.log".format(
            CONST.__getattribute__('dir_results'), self.project_name)
        self.logger = ft_logger.Logger(self.project_name).getLogger()

    def execute(self, **kwargs):
        # pylint: disable=unused-argument,no-self-use
        return -1

    def run(self, **kwargs):
        self.start_time = time.time()
        exit_code = base.TestCase.EX_RUN_ERROR
        self.criteria = "FAIL"
        try:
            if self.execute(**kwargs) == 0:
                exit_code = base.TestCase.EX_OK
                self.criteria = 'PASS'
            ft_utils.logger_test_results(
                self.project_name, self.case_name,
                self.criteria, self.details)
            self.logger.info("%s %s", self.project_name, self.criteria)
        except Exception:  # pylint: disable=broad-except
            self.logger.exception("%s FAILED", self.project_name)
        self.logger.info("Test result is stored in '%s'", self.result_file)
        self.stop_time = time.time()
        return exit_code


class BashFeature(Feature):

    def execute(self, **kwargs):
        ret = -1
        try:
            cmd = kwargs["cmd"]
            ret = ft_utils.execute_command(cmd, output_file=self.result_file)
        except KeyError:
            self.logger.error("Please give cmd as arg. kwargs: %s", kwargs)
        except Exception:  # pylint: disable=broad-except
            self.logger.exception("Execute cmd: %s failed", cmd)
        return ret
