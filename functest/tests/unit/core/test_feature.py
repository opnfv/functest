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
from functest.utils import constants


class FeatureInitTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    @unittest.skip("JIRA: FUNCTEST-780")
    def test_init_with_wrong_repo(self):
        with self.assertRaises(ValueError):
            feature.Feature(repo='foo')

    def test_init(self):
        barometer = feature.Feature(repo='dir_repo_barometer')
        self.assertEqual(barometer.project_name, "functest")
        self.assertEqual(barometer.case_name, "")
        self.assertEqual(
            barometer.repo,
            constants.CONST.__getattribute__('dir_repo_barometer'))


class FeatureTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.feature = feature.Feature(repo='dir_repo_barometer')

    @unittest.skip("JIRA: FUNCTEST-781")
    def test_prepare_ko(self):
        # pylint: disable=bad-continuation
        with mock.patch.object(
                self.feature, 'prepare',
                return_value=testcase.TestCase.EX_RUN_ERROR) as mock_object:
            self.assertEqual(self.feature.run(),
                             testcase.TestCase.EX_RUN_ERROR)
            mock_object.assert_called_once_with()

    @unittest.skip("JIRA: FUNCTEST-781")
    def test_prepare_exc(self):
        with mock.patch.object(self.feature, 'prepare',
                               side_effect=Exception) as mock_object:
            self.assertEqual(self.feature.run(),
                             testcase.TestCase.EX_RUN_ERROR)
            mock_object.assert_called_once_with()

    @unittest.skip("JIRA: FUNCTEST-781")
    def test_post_ko(self):
        # pylint: disable=bad-continuation
        with mock.patch.object(
                self.feature, 'post',
                return_value=testcase.TestCase.EX_RUN_ERROR) as mock_object:
            self.assertEqual(self.feature.run(),
                             testcase.TestCase.EX_RUN_ERROR)
            mock_object.assert_called_once_with()

    @unittest.skip("JIRA: FUNCTEST-781")
    def test_post_exc(self):
        with mock.patch.object(self.feature, 'post',
                               side_effect=Exception) as mock_object:
            self.assertEqual(self.feature.run(),
                             testcase.TestCase.EX_RUN_ERROR)
            mock_object.assert_called_once_with()

    @unittest.skip("JIRA: FUNCTEST-778")
    def test_execute_ko(self):
        with mock.patch.object(self.feature, 'execute',
                               return_value=1) as mock_object:
            self.assertEqual(self.feature.run(),
                             testcase.TestCase.EX_RUN_ERROR)
            mock_object.assert_called_once_with()

    @unittest.skip("JIRA: FUNCTEST-778")
    def test_execute_exc(self):
        with mock.patch.object(self.feature, 'execute',
                               side_effect=Exception) as mock_object:
            self.assertEqual(self.feature.run(),
                             testcase.TestCase.EX_RUN_ERROR)
            mock_object.assert_called_once_with()

    def test_run(self):
        with mock.patch.object(self.feature, 'execute',
                               return_value=0) as mock_object:
            self.assertEqual(self.feature.run(),
                             testcase.TestCase.EX_OK)
            mock_object.assert_called_once_with()


if __name__ == "__main__":
    unittest.main(verbosity=2)
