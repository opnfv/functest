#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import unittest

import mock

from functest.ci import tier_builder


class TierBuilderTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.dependency = {'installer': 'test_installer',
                           'scenario': 'test_scenario'}

        self.testcase = {'dependencies': self.dependency,
                         'case_name': 'test_name',
                         'criteria': 'test_criteria',
                         'blocking': 'test_blocking',
                         'clean_flag': 'test_clean_flag',
                         'description': 'test_desc'}

        self.dic_tier = {'name': 'test_tier',
                         'order': 'test_order',
                         'ci_loop': 'test_ci_loop',
                         'description': 'test_desc',
                         'testcases': [self.testcase]}

        self.mock_yaml = mock.Mock()
        attrs = {'get.return_value': [self.dic_tier]}
        self.mock_yaml.configure_mock(**attrs)

        with mock.patch('functest.ci.tier_builder.yaml.safe_load',
                        return_value=self.mock_yaml), \
                mock.patch('__builtin__.open', mock.mock_open()):
            self.tierbuilder = tier_builder.TierBuilder('test_installer',
                                                        'test_scenario',
                                                        'testcases_file')
        self.tier_obj = self.tierbuilder.tier_objects[0]

    def test_get_tiers(self):
        self.assertEqual(self.tierbuilder.get_tiers(),
                         [self.tier_obj])

    def test_get_tier_names(self):
        self.assertEqual(self.tierbuilder.get_tier_names(),
                         ['test_tier'])

    def test_get_tier_present_tier(self):
        self.assertEqual(self.tierbuilder.get_tier('test_tier'),
                         self.tier_obj)

    def test_get_tier_missing_tier(self):
        self.assertEqual(self.tierbuilder.get_tier('test_tier2'),
                         None)

    def test_get_test_present_test(self):
        self.assertEqual(self.tierbuilder.get_test('test_name'),
                         self.tier_obj.get_test('test_name'))

    def test_get_test_missing_test(self):
        self.assertEqual(self.tierbuilder.get_test('test_name2'),
                         None)

    def test_get_tests_present_tier(self):
        self.assertEqual(self.tierbuilder.get_tests('test_tier'),
                         self.tier_obj.tests_array)

    def test_get_tests_missing_tier(self):
        self.assertEqual(self.tierbuilder.get_tests('test_tier2'),
                         None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
