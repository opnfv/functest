#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock

from functest.core import feature
from functest.core import testcase

# logging must be disabled else it calls time.time()
# what will break these unit tests.
logging.disable(logging.CRITICAL)


class FeatureTestingBase(unittest.TestCase):

    _case_name = "foo"
    _project_name = "bar"
    _repo = "dir_repo_copper"
    _cmd = "cd /home/opnfv/repos/foo/tests && bash run.sh && cd -"
    _output_file = '/home/opnfv/functest/results/bar.log'
    feature = None

    @mock.patch('time.time', side_effect=[1, 2])
    def _test_run(self, status, mock_method=None):
        self.assertEqual(self.feature.run(cmd=self._cmd), status)
        if status == testcase.TestCase.EX_OK:
            self.assertEqual(self.feature.result, 100)
        else:
            self.assertEqual(self.feature.result, 0)
        mock_method.assert_has_calls([mock.call(), mock.call()])
        self.assertEqual(self.feature.start_time, 1)
        self.assertEqual(self.feature.stop_time, 2)


class FeatureTesting(FeatureTestingBase):

    def setUp(self):
        self.feature = feature.Feature(
            project_name=self._project_name, case_name=self._case_name)

    def test_run_exc(self):
        # pylint: disable=bad-continuation
        with mock.patch.object(
                self.feature, 'execute',
                side_effect=Exception) as mock_method:
            self._test_run(testcase.TestCase.EX_RUN_ERROR)
            mock_method.assert_called_once_with(cmd=self._cmd)

    def test_run(self):
        self._test_run(testcase.TestCase.EX_RUN_ERROR)


class BashFeatureTesting(FeatureTestingBase):

    def setUp(self):
        self.feature = feature.BashFeature(
            project_name=self._project_name, case_name=self._case_name)

    @mock.patch("functest.utils.functest_utils.execute_command")
    def test_run_no_cmd(self, mock_method=None):
        self.assertEqual(self.feature.run(), testcase.TestCase.EX_RUN_ERROR)
        mock_method.assert_not_called()

    @mock.patch("functest.utils.functest_utils.execute_command",
                return_value=1)
    def test_run_ko(self, mock_method=None):
        self._test_run(testcase.TestCase.EX_RUN_ERROR)
        mock_method.assert_called_once_with(
            self._cmd, output_file=self._output_file)

    @mock.patch("functest.utils.functest_utils.execute_command",
                side_effect=Exception)
    def test_run_exc(self, mock_method=None):
        self._test_run(testcase.TestCase.EX_RUN_ERROR)
        mock_method.assert_called_once_with(
            self._cmd, output_file=self._output_file)

    @mock.patch("functest.utils.functest_utils.execute_command",
                return_value=0)
    def test_run(self, mock_method):
        self._test_run(testcase.TestCase.EX_OK)
        mock_method.assert_called_once_with(
            self._cmd, output_file=self._output_file)


if __name__ == "__main__":
    unittest.main(verbosity=2)
