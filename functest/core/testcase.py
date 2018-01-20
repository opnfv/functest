#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the parent class of all Functest TestCases."""

from datetime import datetime
import json
import logging
import os
import re
import requests

from functest.utils import decorators


import prettytable


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

    _job_name_rule = "(dai|week)ly-(.+?)-[0-9]*"
    _headers = {'Content-Type': 'application/json'}
    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        self.details = {}
        self.project_name = kwargs.get('project_name', 'functest')
        self.case_name = kwargs.get('case_name', '')
        self.criteria = kwargs.get('criteria', 100)
        self.result = 0
        self.start_time = 0
        self.stop_time = 0

    def __str__(self):
        try:
            assert self.project_name
            assert self.case_name
            result = 'PASS' if(self.is_successful(
                ) == TestCase.EX_OK) else 'FAIL'
            msg = prettytable.PrettyTable(
                header_style='upper', padding_width=5,
                field_names=['test case', 'project', 'duration',
                             'result'])
            msg.add_row([self.case_name, self.project_name,
                         self.get_duration(), result])
            return msg.get_string()
        except AssertionError:
            self.__logger.error("We cannot print invalid objects")
            return super(TestCase, self).__str__()

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
        except Exception:  # pylint: disable=broad-except
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
            assert self.result is not None
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

    @decorators.can_dump_request_to_file
    def push_to_db(self):
        """Push the results of the test case to the DB.

        It allows publishing the results and checking the status.

        It could be overriden if the common implementation is not
        suitable.

        The following attributes must be set before pushing the results to DB:

            * project_name,
            * case_name,
            * result,
            * start_time,
            * stop_time.

        The next vars must be set in env:

            * TEST_DB_URL,
            * INSTALLER_TYPE,
            * DEPLOY_SCENARIO,
            * NODE_NAME,
            * BUILD_TAG.

        Returns:
            TestCase.EX_OK if results were pushed to DB.
            TestCase.EX_PUSH_TO_DB_ERROR otherwise.
        """
        try:
            assert self.project_name
            assert self.case_name
            assert self.start_time
            assert self.stop_time
            url = os.environ['TEST_DB_URL']
            data = {"project_name": self.project_name,
                    "case_name": self.case_name,
                    "details": self.details}
            data["installer"] = os.environ['INSTALLER_TYPE']
            data["scenario"] = os.environ['DEPLOY_SCENARIO']
            data["pod_name"] = os.environ['NODE_NAME']
            data["build_tag"] = os.environ['BUILD_TAG']
            data["criteria"] = 'PASS' if self.is_successful(
                ) == TestCase.EX_OK else 'FAIL'
            data["start_date"] = datetime.fromtimestamp(
                self.start_time).strftime('%Y-%m-%d %H:%M:%S')
            data["stop_date"] = datetime.fromtimestamp(
                self.stop_time).strftime('%Y-%m-%d %H:%M:%S')
            try:
                data["version"] = re.search(
                    TestCase._job_name_rule,
                    os.environ['BUILD_TAG']).group(2)
            except Exception:  # pylint: disable=broad-except
                data["version"] = "unknown"
            req = requests.post(
                url, data=json.dumps(data, sort_keys=True),
                headers=self._headers)
            req.raise_for_status()
            self.__logger.info(
                "The results %s were successfully pushed to DB %s", data, url)
        except AssertionError:
            self.__logger.exception(
                "Please run test before publishing the results")
            return TestCase.EX_PUSH_TO_DB_ERROR
        except KeyError as exc:
            self.__logger.error("Please set env var: " + str(exc))
            return TestCase.EX_PUSH_TO_DB_ERROR
        except requests.exceptions.HTTPError:
            self.__logger.exception("The HTTP request raises issues")
            return TestCase.EX_PUSH_TO_DB_ERROR
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("The results cannot be pushed to DB")
            return TestCase.EX_PUSH_TO_DB_ERROR
        return TestCase.EX_OK

    def clean(self):
        """Clean the resources.

        It can be overriden if resources must be deleted after
        running the test case.
        """
