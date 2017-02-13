#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest

from functest.core import feature_base
from functest.core import testcase_base as base
from functest.utils.constants import CONST


class FeatureBaseTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        CONST.dir_results = 'test_dir'
        with mock.patch('functest.core.feature_base.'
                        'CONST.__getattribute__',
                        return_value='test_repo'):
            self.feature = feature_base.FeatureBase()

    def test_run_default(self):
        with mock.patch('functest.core.feature_base.'
                        'ft_utils.execute_command') as m, \
            mock.patch.object(self.feature, 'parse_results',
                              return_value=base.TestcaseBase.EX_OK), \
                mock.patch.object(self.feature, 'log_results'):
            self.assertEqual(self.feature.run(),
                             base.TestcaseBase.EX_OK)
            self.assertTrue(m.called)

    def test_parse_results_passed(self):
        self.assertEqual(self.feature.parse_results(0),
                         base.TestcaseBase.EX_OK)

    def test_parse_results_failed(self):
        self.assertEqual(self.feature.parse_results(1),
                         base.TestcaseBase.EX_RUN_ERROR)

    def test_get_result_file_default(self):
        CONST.dir_results = 'test_dir'
        self.assertEqual(self.feature.get_result_file(),
                         'test_dir/functest.log')

    def test_log_results_default(self):
        with mock.patch('functest.core.feature_base.'
                        'ft_utils.logger_test_results') \
                as m:
            self.feature.log_results()
            self.assertTrue(m.called)


if __name__ == "__main__":
    unittest.main(verbosity=2)
