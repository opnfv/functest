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

from functest.utils import decorators
from functest.utils import functest_utils
from functest.utils.constants import CONST

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"

VERSION = 'master'
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
    _build_tag = VERSION
    _node_name = 'bar'
    _deploy_scenario = 'foo'
    _installer_type = 'debian'

    def setUp(self):
        os.environ['INSTALLER_TYPE'] = self._installer_type
        os.environ['DEPLOY_SCENARIO'] = self._deploy_scenario
        os.environ['NODE_NAME'] = self._node_name
        os.environ['BUILD_TAG'] = self._build_tag

    def test_wraps(self):
        self.assertEqual(functest_utils.push_results_to_db.__name__,
                         "push_results_to_db")

    def _get_json(self):
        stop_time = datetime.fromtimestamp(self._stop_time).strftime(
            '%Y-%m-%d %H:%M:%S')
        start_time = datetime.fromtimestamp(self._start_time).strftime(
            '%Y-%m-%d %H:%M:%S')
        data = {'project_name': self._project_name,
                'stop_date': stop_time, 'start_date': start_time,
                'case_name': self._case_name, 'build_tag': self._build_tag,
                'pod_name': self._node_name, 'installer': self._installer_type,
                'scenario': self._deploy_scenario, 'version': VERSION,
                'details': {}, 'criteria': self._result}
        return json.dumps(data, sort_keys=True)

    @mock.patch('{}.get_version'.format(functest_utils.__name__),
                return_value=VERSION)
    @mock.patch('requests.post')
    def test_http_shema(self, *args):
        CONST.__setattr__('results_test_db_url', 'http://127.0.0.1')
        self.assertTrue(functest_utils.push_results_to_db(
            self._project_name, self._case_name, self._start_time,
            self._stop_time, self._result, {}))
        args[1].assert_called_once_with()
        args[0].assert_called_once_with(
            'http://127.0.0.1', data=self._get_json(),
            headers={'Content-Type': 'application/json'})

    def test_wrong_shema(self):
        CONST.__setattr__('results_test_db_url', '/dev/null')
        self.assertFalse(functest_utils.push_results_to_db(
            self._project_name, self._case_name, self._start_time,
            self._stop_time, self._result, {}))

    @mock.patch('{}.get_version'.format(functest_utils.__name__),
                return_value=VERSION)
    def _test_dump(self, *args):
        CONST.__setattr__('results_test_db_url', URL)
        with mock.patch.object(decorators, 'open', mock.mock_open(),
                               create=True) as mock_open:
            self.assertTrue(functest_utils.push_results_to_db(
                self._project_name, self._case_name, self._start_time,
                self._stop_time, self._result, {}))
        mock_open.assert_called_once_with(FILE, 'a')
        handle = mock_open()
        call_args, _ = handle.write.call_args
        self.assertIn('POST', call_args[0])
        self.assertIn(self._get_json(), call_args[0])
        args[0].assert_called_once_with()

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
        CONST.__setattr__('results_test_db_url', URL)
        self.assertFalse(
            functest_utils.push_results_to_db(
                self._project_name, self._case_name, self._start_time,
                self._stop_time, self._result, {}))
        args[0].assert_called_once_with(DIR)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
