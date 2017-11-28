#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define classes required to run any Robot suites."""

from __future__ import division

import errno
import logging
import os

import robot.api
from robot.errors import RobotError
import robot.run
from robot.utils.robottime import timestamp_to_secs
from six import StringIO

from functest.core import testcase
from functest.utils import constants

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class ResultVisitor(robot.api.ResultVisitor):
    """Visitor to get result details."""

    def __init__(self):
        self._data = []

    def visit_test(self, test):
        output = {}
        output['name'] = test.name
        output['parent'] = test.parent.name
        output['status'] = test.status
        output['starttime'] = test.starttime
        output['endtime'] = test.endtime
        output['critical'] = test.critical
        output['text'] = test.message
        output['elapsedtime'] = test.elapsedtime
        self._data.append(output)

    def get_data(self):
        """Get the details of the result."""
        return self._data


class RobotFramework(testcase.TestCase):
    """RobotFramework runner."""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        self.res_dir = os.path.join(
            constants.CONST.__getattribute__('dir_results'), 'robot')
        self.xml_file = os.path.join(self.res_dir, 'output.xml')
        super(RobotFramework, self).__init__(**kwargs)

    def parse_results(self):
        """Parse output.xml and get the details in it."""
        result = robot.api.ExecutionResult(self.xml_file)
        visitor = ResultVisitor()
        result.visit(visitor)
        try:
            self.result = 100 * (
                result.suite.statistics.critical.passed /
                result.suite.statistics.critical.total)
        except ZeroDivisionError:
            self.__logger.error("No test has been run")
        self.start_time = timestamp_to_secs(result.suite.starttime)
        self.stop_time = timestamp_to_secs(result.suite.endtime)
        self.details = {}
        self.details['description'] = result.suite.name
        self.details['tests'] = visitor.get_data()

    def run(self, **kwargs):
        """Run the RobotFramework suites

        Here are the steps:
           * create the output directories if required,
           * get the results in output.xml,
           * delete temporary files.

        Args:
            kwargs: Arbitrary keyword arguments.

        Returns:
            EX_OK if all suites ran well.
            EX_RUN_ERROR otherwise.
        """
        try:
            suites = kwargs["suites"]
            variable = kwargs.get("variable", [])
        except KeyError:
            self.__logger.exception("Mandatory args were not passed")
            return self.EX_RUN_ERROR
        try:
            os.makedirs(self.res_dir)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                self.__logger.exception("Cannot create %s", self.res_dir)
                return self.EX_RUN_ERROR
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot create %s", self.res_dir)
            return self.EX_RUN_ERROR
        stream = StringIO()
        robot.run(*suites, variable=variable, output=self.xml_file,
                  log='NONE', report='NONE', stdout=stream)
        self.__logger.info("\n" + stream.getvalue())
        self.__logger.info("Results were successfully generated")
        try:
            self.parse_results()
            self.__logger.info("Results were successfully parsed")
        except RobotError as ex:
            self.__logger.error("Run suites before publishing: %s", ex.message)
            return self.EX_RUN_ERROR
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot parse results")
            return self.EX_RUN_ERROR
        return self.EX_OK
