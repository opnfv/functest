#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the classes required to fully cover robot."""

import errno
import logging
import os
import unittest

import mock
from robot.errors import DataError, RobotError
from robot.result import model
from robot.utils.robottime import timestamp_to_secs

from functest.core import robotframework

__author__ = "Cedric Ollivier <cedric.ollivier@orange.com>"


class ResultVisitorTesting(unittest.TestCase):

    """The class testing ResultVisitor."""
    # pylint: disable=missing-docstring

    def setUp(self):
        self.visitor = robotframework.ResultVisitor()

    def test_empty(self):
        self.assertFalse(self.visitor.get_data())

    def test_ok(self):
        data = {'name': 'foo',
                'parent': 'bar',
                'status': 'PASS',
                'starttime': "20161216 16:00:00.000",
                'endtime': "20161216 16:00:01.000",
                'elapsedtime': 1000,
                'text': 'Hello, World!',
                'critical': True}
        test = model.TestCase(
            name=data['name'], status=data['status'], message=data['text'],
            starttime=data['starttime'], endtime=data['endtime'])
        test.parent = mock.Mock()
        config = {'name': data['parent'],
                  'criticality.test_is_critical.return_value': data[
                      'critical']}
        test.parent.configure_mock(**config)
        self.visitor.visit_test(test)
        self.assertEqual(self.visitor.get_data(), [data])


class ParseResultTesting(unittest.TestCase):

    """The class testing RobotFramework.parse_results()."""
    # pylint: disable=missing-docstring

    _config = {'name': 'dummy', 'starttime': '20161216 16:00:00.000',
               'endtime': '20161216 16:00:01.000'}

    def setUp(self):
        self.test = robotframework.RobotFramework(
            case_name='robot', project_name='functest')

    @mock.patch('robot.api.ExecutionResult', side_effect=DataError)
    def test_raises_exc(self, mock_method):
        with self.assertRaises(DataError):
            self.test.parse_results()
        mock_method.assert_called_once_with(
            os.path.join(self.test.res_dir, 'output.xml'))

    def _test_result(self, config, result):
        suite = mock.Mock()
        suite.configure_mock(**config)
        with mock.patch('robot.api.ExecutionResult',
                        return_value=mock.Mock(suite=suite)):
            self.test.parse_results()
            self.assertEqual(self.test.result, result)
            self.assertEqual(self.test.start_time,
                             timestamp_to_secs(config['starttime']))
            self.assertEqual(self.test.stop_time,
                             timestamp_to_secs(config['endtime']))
            self.assertEqual(self.test.details,
                             {'description': config['name'], 'tests': []})

    def test_null_passed(self):
        self._config.update({'statistics.critical.passed': 0,
                             'statistics.critical.total': 20})
        self._test_result(self._config, 0)

    def test_no_test(self):
        self._config.update({'statistics.critical.passed': 20,
                             'statistics.critical.total': 0})
        self._test_result(self._config, 0)

    def test_half_success(self):
        self._config.update({'statistics.critical.passed': 10,
                             'statistics.critical.total': 20})
        self._test_result(self._config, 50)

    def test_success(self):
        self._config.update({'statistics.critical.passed': 20,
                             'statistics.critical.total': 20})
        self._test_result(self._config, 100)


class RunTesting(unittest.TestCase):

    """The class testing RobotFramework.run()."""
    # pylint: disable=missing-docstring

    suites = ["foo"]
    variable = []

    def setUp(self):
        self.test = robotframework.RobotFramework(
            case_name='robot', project_name='functest')

    def test_exc_key_error(self):
        self.assertEqual(self.test.run(), self.test.EX_RUN_ERROR)

    @mock.patch('robot.run')
    def _test_makedirs_exc(self, *args):
        with mock.patch.object(self.test, 'parse_results') as mock_method:
            self.assertEqual(
                self.test.run(suites=self.suites, variable=self.variable),
                self.test.EX_RUN_ERROR)
            args[0].assert_not_called()
            mock_method.asser_not_called()

    @mock.patch('os.makedirs', side_effect=Exception)
    def test_makedirs_exc(self, *args):
        self._test_makedirs_exc()
        args[0].assert_called_once_with(self.test.res_dir)

    @mock.patch('os.makedirs', side_effect=OSError)
    def test_makedirs_oserror(self, *args):
        self._test_makedirs_exc()
        args[0].assert_called_once_with(self.test.res_dir)

    @mock.patch('robot.run')
    def _test_makedirs(self, *args):
        with mock.patch.object(self.test, 'parse_results') as mock_method:
            self.assertEqual(
                self.test.run(suites=self.suites, variable=self.variable),
                self.test.EX_OK)
            args[0].assert_called_once_with(
                *self.suites, log='NONE', output=self.test.xml_file,
                report='NONE', stdout=mock.ANY, variable=self.variable)
            mock_method.assert_called_once_with()

    @mock.patch('os.makedirs', side_effect=OSError(errno.EEXIST, ''))
    def test_makedirs_oserror17(self, *args):
        self._test_makedirs()
        args[0].assert_called_once_with(self.test.res_dir)

    @mock.patch('os.makedirs')
    def test_makedirs(self, *args):
        self._test_makedirs()
        args[0].assert_called_once_with(self.test.res_dir)

    @mock.patch('robot.run')
    def _test_parse_results(self, status, *args):
        self.assertEqual(
            self.test.run(suites=self.suites, variable=self.variable), status)
        args[0].assert_called_once_with(
            *self.suites, log='NONE', output=self.test.xml_file,
            report='NONE', stdout=mock.ANY, variable=self.variable)

    def test_parse_results_exc(self):
        with mock.patch.object(self.test, 'parse_results',
                               side_effect=Exception) as mock_method:
            self._test_parse_results(self.test.EX_RUN_ERROR)
            mock_method.assert_called_once_with()

    def test_parse_results_robot_error(self):
        with mock.patch.object(self.test, 'parse_results',
                               side_effect=RobotError('foo')) as mock_method:
            self._test_parse_results(self.test.EX_RUN_ERROR)
            mock_method.assert_called_once_with()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
