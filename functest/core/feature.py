#!/usr/bin/env python

# Copyright (c) 2016 ZTE Corp and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the parent class of all Functest Features.

Feature is considered as TestCase offered by Third-party. It offers
helpers to run any python method or any bash command.
"""

import time

import functest.core.testcase as base
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger
from functest.utils.constants import CONST

__author__ = ("Serena Feng <feng.xiaowei@zte.com.cn>, "
              "Cedric Ollivier <cedric.ollivier@orange.com>")


class Feature(base.TestCase):
    """Base model for single Functest feature."""

    def __init__(self, **kwargs):
        super(Feature, self).__init__(**kwargs)
        self.result_file = "{}/{}.log".format(
            CONST.__getattribute__('dir_results'), self.project_name)
        self.logger = ft_logger.Logger(self.project_name).getLogger()

    def execute(self, **kwargs):
        """Execute the Python method.

        The subclasses must override the default implementation which
        is false on purpose.

        The new implementation must return 0 if success or anything
        else if failure.

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            -1.
        """
        # pylint: disable=unused-argument,no-self-use
        return -1

    def run(self, **kwargs):
        """Run the feature.

        It allows executing any Python method by calling execute().

        It sets the following attributes required to push the results
        to DB:

            * criteria,
            * start_time,
            * stop_time.

        It doesn't fulfill details when pushing the results to the DB.

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            TestCase.EX_OK if execute() returns 0,
            TestCase.EX_RUN_ERROR otherwise.
        """
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
    """Class designed to run any bash command."""

    def execute(self, **kwargs):
        """Execute the cmd passed as arg

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            0 if cmd returns 0,
            -1 otherwise.
        """
        ret = -1
        try:
            cmd = kwargs["cmd"]
            ret = ft_utils.execute_command(cmd, output_file=self.result_file)
        except KeyError:
            self.logger.error("Please give cmd as arg. kwargs: %s", kwargs)
        except Exception:  # pylint: disable=broad-except
            self.logger.exception("Execute cmd: %s failed", cmd)
        return ret
