#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import tier_handler as th
import yaml


class TierBuilder:

    def __init__(self, ci_installer, ci_scenario, testcases_file):
        self.ci_installer = ci_installer
        self.ci_scenario = ci_scenario
        self.testcases_file = testcases_file
        self.dic_tier_array = None
        self.tier_objects = []
        self.testcases_yaml = None
        self.generate_tiers()

    def read_test_yaml(self):
        with open(self.testcases_file) as f:
            self.testcases_yaml = yaml.safe_load(f)

        self.dic_tier_array = []
        for tier in self.testcases_yaml.get("tiers"):
            self.dic_tier_array.append(tier)

    def generate_tiers(self):
        if self.dic_tier_array is None:
            self.read_test_yaml()

        del self.tier_objects[:]
        for dic_tier in self.dic_tier_array:
            tier = th.Tier(name=dic_tier['name'],
                           order=dic_tier['order'],
                           ci_loop=dic_tier['ci_loop'],
                           description=dic_tier['description'])

            for dic_testcase in dic_tier['testcases']:
                installer = dic_testcase['dependencies']['installer']
                scenario = dic_testcase['dependencies']['scenario']
                dep = th.Dependency(installer, scenario)

                testcase = th.TestCase(name=dic_testcase['name'],
                                       dependency=dep,
                                       criteria=dic_testcase['criteria'],
                                       blocking=dic_testcase['blocking'],
                                       description=dic_testcase['description'])
                if testcase.is_compatible(self.ci_installer, self.ci_scenario):
                    tier.add_test(testcase)

            self.tier_objects.append(tier)

    def get_tiers(self):
        return self.tier_objects

    def get_tier_names(self):
        tier_names = []
        for tier in self.tier_objects:
            tier_names.append(tier.get_name())
        return tier_names

    def get_tier(self, tier_name):
        for i in range(0, len(self.tier_objects)):
            if self.tier_objects[i].get_name() == tier_name:
                return self.tier_objects[i]
        return None

    def get_test(self, test_name):
        for i in range(0, len(self.tier_objects)):
            if self.tier_objects[i].is_test(test_name):
                return self.tier_objects[i].get_test(test_name)
        return None

    def get_tests(self, tier_name):
        for i in range(0, len(self.tier_objects)):
            if self.tier_objects[i].get_name() == tier_name:
                return self.tier_objects[i].get_tests()
        return None

    def __str__(self):
        output = ""
        for i in range(0, len(self.tier_objects)):
            output += str(self.tier_objects[i]) + "\n"
        return output
