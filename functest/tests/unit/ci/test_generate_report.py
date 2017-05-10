#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest
import urllib2

import mock

from functest.ci import generate_report as gen_report
from functest.tests.unit import test_utils
from functest.utils import functest_utils as ft_utils
from functest.utils.constants import CONST


class GenerateReportTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def test_init(self):
        test_array = gen_report.init()
        self.assertEqual(test_array, [])

    @mock.patch('functest.ci.generate_report.urllib2.urlopen',
                side_effect=urllib2.URLError('no host given'))
    def test_get_results_from_db_fail(self, mock_method):
        url = "%s?build_tag=%s" % (ft_utils.get_db_url(),
                                   CONST.__getattribute__('BUILD_TAG'))
        self.assertIsNone(gen_report.get_results_from_db())
        mock_method.assert_called_once_with(url)

    @mock.patch('functest.ci.generate_report.urllib2.urlopen',
                return_value={'results': []})
    def test_get_results_from_db_success(self, mock_method):
        url = "%s?build_tag=%s" % (ft_utils.get_db_url(),
                                   CONST.__getattribute__('BUILD_TAG'))
        self.assertEqual(gen_report.get_results_from_db(), None)
        mock_method.assert_called_once_with(url)

    def test_get_data(self):
        self.assertIsInstance(gen_report.get_data({'result': ''}, ''), dict)

    def test_print_line_with_ci_run(self):
        CONST.__setattr__('IS_CI_RUN', True)
        w1 = 'test_print_line'
        test_str = ("| %s| %s| %s| %s| %s|\n"
                    % (w1.ljust(gen_report.COL_1_LEN - 1),
                       ''.ljust(gen_report.COL_2_LEN - 1),
                       ''.ljust(gen_report.COL_3_LEN - 1),
                       ''.ljust(gen_report.COL_4_LEN - 1),
                       ''.ljust(gen_report.COL_5_LEN - 1)))
        self.assertEqual(gen_report.print_line(w1), test_str)

    def test_print_line_without_ci_run(self):
        CONST.__setattr__('IS_CI_RUN', False)
        w1 = 'test_print_line'
        test_str = ("| %s| %s| %s| %s|\n"
                    % (w1.ljust(gen_report.COL_1_LEN - 1),
                       ''.ljust(gen_report.COL_2_LEN - 1),
                       ''.ljust(gen_report.COL_3_LEN - 1),
                       ''.ljust(gen_report.COL_4_LEN - 1)))
        self.assertEqual(gen_report.print_line(w1), test_str)

    def test_print_line_no_column_with_ci_run(self):
        CONST.__setattr__('IS_CI_RUN', True)
        TOTAL_LEN = gen_report.COL_1_LEN + gen_report.COL_2_LEN
        TOTAL_LEN += gen_report.COL_3_LEN + gen_report.COL_4_LEN + 2
        TOTAL_LEN += gen_report.COL_5_LEN + 1
        test_str = ("| %s|\n" % 'test'.ljust(TOTAL_LEN))
        self.assertEqual(gen_report.print_line_no_columns('test'), test_str)

    def test_print_line_no_column_without_ci_run(self):
        CONST.__setattr__('IS_CI_RUN', False)
        TOTAL_LEN = gen_report.COL_1_LEN + gen_report.COL_2_LEN
        TOTAL_LEN += gen_report.COL_3_LEN + gen_report.COL_4_LEN + 2
        test_str = ("| %s|\n" % 'test'.ljust(TOTAL_LEN))
        self.assertEqual(gen_report.print_line_no_columns('test'), test_str)

    def test_print_separator_with_ci_run(self):
        CONST.__setattr__('IS_CI_RUN', True)
        test_str = ("+" + "=" * gen_report.COL_1_LEN +
                    "+" + "=" * gen_report.COL_2_LEN +
                    "+" + "=" * gen_report.COL_3_LEN +
                    "+" + "=" * gen_report.COL_4_LEN +
                    "+" + "=" * gen_report.COL_5_LEN)
        test_str += '+\n'
        self.assertEqual(gen_report.print_separator(), test_str)

    def test_print_separator_without_ci_run(self):
        CONST.__setattr__('IS_CI_RUN', False)
        test_str = ("+" + "=" * gen_report.COL_1_LEN +
                    "+" + "=" * gen_report.COL_2_LEN +
                    "+" + "=" * gen_report.COL_3_LEN +
                    "+" + "=" * gen_report.COL_4_LEN)
        test_str += "+\n"
        self.assertEqual(gen_report.print_separator(), test_str)

    @mock.patch('functest.ci.generate_report.logger.info')
    def test_main_with_ci_run(self, mock_method):
        CONST.__setattr__('IS_CI_RUN', True)
        gen_report.main()
        mock_method.assert_called_once_with(test_utils.SubstrMatch('URL'))

    @mock.patch('functest.ci.generate_report.logger.info')
    def test_main_with_ci_loop(self, mock_method):
        CONST.__setattr__('CI_LOOP', 'daily')
        gen_report.main()
        mock_method.assert_called_once_with(test_utils.SubstrMatch('CI LOOP'))

    @mock.patch('functest.ci.generate_report.logger.info')
    def test_main_with_scenario(self, mock_method):
        CONST.__setattr__('DEPLOY_SCENARIO', 'test_scenario')
        gen_report.main()
        mock_method.assert_called_once_with(test_utils.SubstrMatch('SCENARIO'))

    @mock.patch('functest.ci.generate_report.logger.info')
    def test_main_with_build_tag(self, mock_method):
        CONST.__setattr__('BUILD_TAG', 'test_build_tag')
        gen_report.main()
        mock_method.assert_called_once_with(test_utils.
                                            SubstrMatch('BUILD TAG'))


if __name__ == "__main__":
    unittest.main(verbosity=2)
