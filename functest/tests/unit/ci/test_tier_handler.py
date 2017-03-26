#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.ci import tier_handler


class TierHandlerTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.test = mock.Mock()
        attrs = {'get_name.return_value': 'test_name'}
        self.test.configure_mock(**attrs)

        self.mock_depend = mock.Mock()
        attrs = {'get_scenario.return_value': 'test_scenario',
                 'get_installer.return_value': 'test_installer'}
        self.mock_depend.configure_mock(**attrs)

        self.tier = tier_handler.Tier('test_tier',
                                      'test_order',
                                      'test_ci_loop',
                                      description='test_desc')
        self.testcase = tier_handler.TestCase('test_name',
                                              self.mock_depend,
                                              'test_criteria',
                                              'test_blocking',
                                              'test_clean_flag',
                                              description='test_desc')

        self.dependency = tier_handler.Dependency('test_installer',
                                                  'test_scenario')

        self.testcase.str = self.testcase.__str__()
        self.dependency.str = self.dependency.__str__()
        self.tier.str = self.tier.__str__()

    def test_split_text(self):
        test_str = 'this is for testing'
        self.assertEqual(tier_handler.split_text(test_str, 10),
                         ['this is ', 'for ', 'testing '])

    def test_add_test(self):
        self.tier.add_test(self.test)
        self.assertEqual(self.tier.tests_array,
                         [self.test])

    def test_get_tests(self):
        self.tier.tests_array = [self.test]
        self.assertEqual(self.tier.get_tests(),
                         [self.test])

    def test_get_test_names(self):
        self.tier.tests_array = [self.test]
        self.assertEqual(self.tier.get_test_names(),
                         ['test_name'])

    def test_get_test(self):
        self.tier.tests_array = [self.test]
        with mock.patch.object(self.tier, 'is_test',
                               return_value=True):
            self.assertEqual(self.tier.get_test('test_name'),
                             self.test)

    def test_get_test_missing_test(self):
        self.tier.tests_array = [self.test]
        with mock.patch.object(self.tier, 'is_test',
                               return_value=False):
            self.assertEqual(self.tier.get_test('test_name'),
                             None)

    def test_get_name(self):
        self.assertEqual(self.tier.get_name(),
                         'test_tier')

    def test_get_order(self):
        self.assertEqual(self.tier.get_order(),
                         'test_order')

    def test_get_ci_loop(self):
        self.assertEqual(self.tier.get_ci_loop(),
                         'test_ci_loop')

    def test_testcase_is_none_present_item(self):
        self.assertEqual(tier_handler.TestCase.is_none("item"),
                         False)

    def test_testcase_is_none_missing_item(self):
        self.assertEqual(tier_handler.TestCase.is_none(None),
                         True)

    def test_testcase_is_compatible(self):
        self.assertEqual(self.testcase.is_compatible('test_installer',
                                                     'test_scenario'),
                         True)

    def test_testcase_is_compatible_missing_installer_scenario(self):
        self.assertEqual(self.testcase.is_compatible('missing_installer',
                                                     'test_scenario'),
                         False)
        self.assertEqual(self.testcase.is_compatible('test_installer',
                                                     'missing_scenario'),
                         False)

    def test_testcase_get_name(self):
        self.assertEqual(self.tier.get_name(),
                         'test_tier')

    def test_testcase_get_criteria(self):
        self.assertEqual(self.tier.get_order(),
                         'test_order')

    def test_testcase_is_blocking(self):
        self.assertEqual(self.tier.get_ci_loop(),
                         'test_ci_loop')

    def test_dependency_get_installer(self):
        self.assertEqual(self.dependency.get_installer(),
                         'test_installer')

    def test_dependency_get_scenario(self):
        self.assertEqual(self.dependency.get_scenario(),
                         'test_scenario')


if __name__ == "__main__":
    unittest.main(verbosity=2)
