#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import sys
import unittest

import mock

from functest.core import testcase
sys.modules['baro_tests'] = mock.Mock()  # noqa
# pylint: disable=wrong-import-position
from functest.opnfv_tests.features import barometer


class BarometerTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    _case_name = "barometercollectd"
    _project_name = "barometer"

    def setUp(self):
        self.barometer = barometer.BarometerCollectd(
            case_name=self._case_name, project_name=self._project_name)

    def test_init(self):
        self.assertEqual(self.barometer.project_name, self._project_name)
        self.assertEqual(self.barometer.case_name, self._case_name)

    def test_run_ko(self):
        sys.modules['baro_tests'].collectd.main = mock.Mock(return_value=1)
        self.assertEqual(self.barometer.run(),
                         testcase.TestCase.EX_RUN_ERROR)

    def test_run(self):
        sys.modules['baro_tests'].collectd.main = mock.Mock(return_value=0)
        self.assertEqual(self.barometer.run(), testcase.TestCase.EX_OK)


if __name__ == "__main__":
    unittest.main(verbosity=2)
