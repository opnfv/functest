#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the class required to fully cover decorators."""

from datetime import datetime
import errno
import json
import logging
import os
import unittest

import mock

from functest.core import testcase
from functest.utils import decorators

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"

DIR = '/dev'
FILE = '{}/null'.format(DIR)
URL = 'file://{}'.format(FILE)


class DecoratorsTesting(unittest.TestCase):
    # pylint: disable=missing-docstring

    _case_name = 'base'
    _project_name = 'functest'
    _start_time = 1.0
    _stop_time = 2.0
    _result = 'PASS'
    _version = 'unknown'
    _build_tag = 'none'
    _node_name = 'bar'
    _deploy_scenario = 'foo'
    _installer_type = 'debian'

    def setUp(self):
        os.environ['INSTALLER_TYPE'] = self._installer_type
        os.environ['DEPLOY_SCENARIO'] = self._deploy_scenario
        os.environ['NODE_NAME'] = self._node_name
        os.environ['BUILD_TAG'] = self._build_tag

    def test_wraps(self):
        self.assertEqual(testcase.TestCase.push_to_db.__name__,
                         "push_to_db")

    def _get_json(self):
        stop_time = datetime.fromtimestamp(self._stop_time).strftime(
            '%Y-%m-%d %H:%M:%S')
        start_time = datetime.fromtimestamp(self._start_time).strftime(
            '%Y-%m-%d %H:%M:%S')
        data = {'project_name': self._project_name,
                'stop_date': stop_time, 'start_date': start_time,
                'case_name': self._case_name, 'build_tag': self._build_tag,
                'pod_name': self._node_name, 'installer': self._installer_type,
                'scenario': self._deploy_scenario, 'version': self._version,
                'details': {}, 'criteria': self._result}
        return json.dumps(data, sort_keys=True)

    def _get_testcase(self):
        test = testcase.TestCase(
            project_name=self._project_name, case_name=self._case_name)
        test.start_time = self._start_time
        test.stop_time = self._stop_time
        test.result = 100
        test.details = {}
        return test

    @mock.patch('requests.post')
    def test_http_shema(self, *args):
        os.environ['TEST_DB_URL'] = 'http://127.0.0.1'
        test = self._get_testcase()
        self.assertEqual(test.push_to_db(), testcase.TestCase.EX_OK)
        args[0].assert_called_once_with(
            'http://127.0.0.1', data=self._get_json(),
            headers={'Content-Type': 'application/json'})

    def test_wrong_shema(self):
        os.environ['TEST_DB_URL'] = '/dev/null'
        test = self._get_testcase()
        self.assertEqual(
            test.push_to_db(), testcase.TestCase.EX_PUSH_TO_DB_ERROR)

    def _test_dump(self):
        os.environ['TEST_DB_URL'] = URL
        with mock.patch.object(decorators, 'open', mock.mock_open(),
                               create=True) as mock_open:
            test = self._get_testcase()
            self.assertEqual(test.push_to_db(), testcase.TestCase.EX_OK)
        mock_open.assert_called_once_with(FILE, 'a')
        handle = mock_open()
        call_args, _ = handle.write.call_args
        self.assertIn('POST', call_args[0])
        self.assertIn(self._get_json(), call_args[0])

    @mock.patch('os.makedirs')
    def test_default_dump(self, mock_method=None):
        self._test_dump()
        mock_method.assert_called_once_with(DIR)

    @mock.patch('os.makedirs', side_effect=OSError(errno.EEXIST, ''))
    def test_makedirs_dir_exists(self, mock_method=None):
        self._test_dump()
        mock_method.assert_called_once_with(DIR)

    @mock.patch('os.makedirs', side_effect=OSError)
    def test_makedirs_exc(self, *args):
        os.environ['TEST_DB_URL'] = URL
        test = self._get_testcase()
        self.assertEqual(
            test.push_to_db(), testcase.TestCase.EX_PUSH_TO_DB_ERROR)
        args[0].assert_called_once_with(DIR)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
