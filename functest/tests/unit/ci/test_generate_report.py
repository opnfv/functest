#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest
import urllib2

from functest.ci import generate_report as gr
import functest.utils.functest_utils as ft_utils


class AnyStringWith(str):
    def __eq__(self, other):
        if self in other:
            return True
        return False


class GenerateReportTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def test_init(self):
        test_array = gr.init([])
        self.assertEqual(test_array, [])

    @mock.patch('functest.ci.generate_report.urllib2.urlopen',
                side_effect=urllib2.URLError('no host given'))
    def test_get_results_from_db_fail(self, mock_method):
        url = "%s/results?build_tag=%s" % (ft_utils.get_db_url(),
                                           gr.GlobalVariables.BUILD_TAG)
        self.assertIsNone(gr.get_results_from_db())
        mock_method.assert_called_once_with(url)

    @mock.patch('functest.ci.generate_report.urllib2.urlopen',
                return_value={'results': []})
    def test_get_results_from_db_success(self, mock_method):
        url = "%s/results?build_tag=%s" % (ft_utils.get_db_url(),
                                           gr.GlobalVariables.BUILD_TAG)
        self.assertEqual(gr.get_results_from_db(), None)
        mock_method.assert_called_once_with(url)

    def test_get_data(self):
        self.assertIsInstance(gr.get_data({'result': ''}, ''), dict)

    def test_print_line_with_ci_run(self):
        gr.GlobalVariables.IS_CI_RUN = True
        w1 = 'test_print_line'
        w2 = ''
        w3 = ''
        w4 = ''
        w5 = ''
        str = ('| ' + w1.ljust(gr.COL_1_LEN - 1) +
               '| ' + w2.ljust(gr.COL_2_LEN - 1) +
               '| ' + w3.ljust(gr.COL_3_LEN - 1) +
               '| ' + w4.ljust(gr.COL_4_LEN - 1) +
               '| ' + w5.ljust(gr.COL_5_LEN - 1))
        str += '|\n'
        self.assertEqual(gr.print_line(w1), str)

    def test_print_line_without_ci_run(self):
        gr.GlobalVariables.IS_CI_RUN = False
        w1 = 'test_print_line'
        w2 = ''
        w3 = ''
        w4 = ''
        str = ('| ' + w1.ljust(gr.COL_1_LEN - 1) +
               '| ' + w2.ljust(gr.COL_2_LEN - 1) +
               '| ' + w3.ljust(gr.COL_3_LEN - 1) +
               '| ' + w4.ljust(gr.COL_4_LEN - 1))
        str += '|\n'
        self.assertEqual(gr.print_line(w1), str)

    def test_print_line_no_column_with_ci_run(self):
        gr.GlobalVariables.IS_CI_RUN = True
        TOTAL_LEN = gr.COL_1_LEN + gr.COL_2_LEN + gr.COL_3_LEN
        TOTAL_LEN += gr.COL_4_LEN + 2
        TOTAL_LEN += gr.COL_5_LEN + 1
        str = ('| ' + 'test'.ljust(TOTAL_LEN) + "|\n")
        self.assertEqual(gr.print_line_no_columns('test'), str)

    def test_print_line_no_column_without_ci_run(self):
        gr.GlobalVariables.IS_CI_RUN = False
        TOTAL_LEN = gr.COL_1_LEN + gr.COL_2_LEN + gr.COL_3_LEN
        TOTAL_LEN += gr.COL_4_LEN + 2
        str = ('| ' + 'test'.ljust(TOTAL_LEN) + "|\n")
        self.assertEqual(gr.print_line_no_columns('test'), str)

    def test_print_separator_with_ci_run(self):
        gr.GlobalVariables.IS_CI_RUN = True
        str = ("+" + "=" * gr.COL_1_LEN +
               "+" + "=" * gr.COL_2_LEN +
               "+" + "=" * gr.COL_3_LEN +
               "+" + "=" * gr.COL_4_LEN +
               "+" + "=" * gr.COL_5_LEN)
        str += '+\n'
        self.assertEqual(gr.print_separator(), str)

    def test_print_separator_without_ci_run(self):
        gr.GlobalVariables.IS_CI_RUN = False
        str = ("+" + "=" * gr.COL_1_LEN +
               "+" + "=" * gr.COL_2_LEN +
               "+" + "=" * gr.COL_3_LEN +
               "+" + "=" * gr.COL_4_LEN)
        str += "+\n"
        self.assertEqual(gr.print_separator(), str)

    @mock.patch('functest.ci.generate_report.logger.info')
    def test_main_with_ci_run(self, mock_method):
        gr.GlobalVariables.IS_CI_RUN = True
        gr.main([])
        mock_method.assert_called_once_with(AnyStringWith('URL'))

    @mock.patch('functest.ci.generate_report.logger.info')
    def test_main_with_ci_loop(self, mock_method):
        gr.GlobalVariables.CI_LOOP = 'daily'
        gr.main([])
        mock_method.assert_called_once_with(AnyStringWith('CI LOOP'))

    @mock.patch('functest.ci.generate_report.logger.info')
    def test_main_with_scenario(self, mock_method):
        gr.GlobalVariables.SCENARIO = 'test_scenario'
        gr.main([])
        mock_method.assert_called_once_with(AnyStringWith('SCENARIO'))

    @mock.patch('functest.ci.generate_report.logger.info')
    def test_main_with_build_tag(self, mock_method):
        gr.GlobalVariables.SCENARIO = 'test_build_tag'
        gr.main([])
        mock_method.assert_called_once_with(AnyStringWith('BUILD TAG'))


if __name__ == "__main__":
    unittest.main(verbosity=2)
