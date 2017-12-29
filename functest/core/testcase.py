#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the parent class of all Functest TestCases."""

from datetime import datetime as dt
import json
import logging
import os
import re

import prettytable
import requests

from functest.utils.constants import CONST


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

    @staticmethod
    def get_version():
        """
        Get version
        """
        # Use the build tag to retrieve the version
        # By default version is unknown
        # if launched through CI the build tag has the following format
        # jenkins-<project>-<installer>-<pod>-<job>-<branch>-<id>
        # e.g. jenkins-functest-fuel-opnfv-jump-2-daily-master-190
        # jenkins-functest-fuel-baremetal-weekly-master-8
        # use regex to match branch info
        rule = "(dai|week)ly-(.+?)-[0-9]*"
        build_tag = CONST.__getattribute__('BUILD_TAG')
        if not build_tag:
            build_tag = 'none'
        m = re.search(rule, build_tag)
        if m:
            return m.group(2)
        else:
            return "unknown"

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
            installer = os.environ['INSTALLER_TYPE']
            scenario = os.environ['DEPLOY_SCENARIO']
            pod_name = os.environ['NODE_NAME']
            build_tag = os.environ['BUILD_TAG']
            version = TestCase.get_version()
            test_start = dt.fromtimestamp(self.start_time).strftime(
                '%Y-%m-%d %H:%M:%S')
            test_stop = dt.fromtimestamp(self.stop_time).strftime(
                '%Y-%m-%d %H:%M:%S')
            if (hasattr(CONST, 'TEST_DB_URL')):
                url = CONST.__getattribute__('TEST_DB_URL')
            else:
                url = CONST.__getattribute__("results_test_db_url")
            pub_result = 'PASS' if self.is_successful(
                ) == TestCase.EX_OK else 'FAIL'

            params = {"project_name": self.project_name,
                      "case_name": self.case_name,
                      "pod_name": pod_name,
                      "installer": installer,
                      "version": version,
                      "scenario": scenario,
                      "criteria": self.result,
                      "build_tag": build_tag,
                      "start_date": test_start,
                      "stop_date": test_stop,
                      "details": self.details}
        except Exception:  # pylint: disable=broad-except
            self.__logger.error("Problem while getting test parameters.")
            return TestCase.EX_PUSH_TO_DB_ERROR

        error = None
        headers = {'Content-Type': 'application/json'}
        try:
            r = requests.post(url, data=json.dumps(params, sort_keys=True),
                              headers=headers)
            r.raise_for_status()
        except requests.RequestException as exc:
            if 'r' in locals():
                error = ("Pushing Result to DB(%s) failed: %s" %
                         (r.url, r.content))
            else:
                error = ("Pushing Result to DB(%s) failed: %s" % (url, exc))
        except Exception as e:
            error = ("Error [push_results_to_db("
                     "DB: '%(db)s', "
                     "project: '%(project)s', "
                     "case: '%(case)s', "
                     "pod: '%(pod)s', "
                     "version: '%(v)s', "
                     "scenario: '%(s)s', "
                     "criteria: '%(c)s', "
                     "build_tag: '%(t)s', "
                     "details: '%(d)s')]: "
                     "%(error)s" %
                     {
                         'db': url,
                         'project': self.project_name,
                         'case': self.case_name,
                         'pod': pod_name,
                         'v': version,
                         's': scenario,
                         'c': self.result,
                         't': build_tag,
                         'd': self.details,
                         'error': e
                     })
        finally:
            if error:
                self.__logger.error("The results cannot be "
                                    "pushed to DB. %s" % error)
                return TestCase.EX_PUSH_TO_DB_ERROR
            else:
                self.__logger.info(
                    "The results were successfully pushed to DB")
                return TestCase.EX_OK

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

    def clean(self):
        """Clean the resources.

        It can be overriden if resources must be deleted after
        running the test case.
        """
