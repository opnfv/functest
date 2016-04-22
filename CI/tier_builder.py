#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import yaml

from tier_handler import Tier, TestCase, Dependency


class TierBuilder:
    def __init__(self):
        self.dic_tier_array = []
        self.tier_objects = []
        self.testcases_yaml = None

    def read_test_yaml(self):
        with open("testcases.yaml") as f:
            self.testcases_yaml = yaml.safe_load(f)

        del self.dic_tier_array[:]
        for tier in self.testcases_yaml.get("tiers"):
            self.dic_tier_array.append(tier)

    def generate_tiers(self):
        if self.dic_tier_array is None:
            self.read_test_yaml()

        del self.tier_objects[:]
        for dic_tier in self.dic_tier_array:
            tier = Tier(name=dic_tier['name'],
                        order=dic_tier['order'],
                        ci=dic_tier['ci'],
                        description=dic_tier['description'])

            for dic_testcase in dic_tier['testcases']:
                installer = dic_testcase['dependencies']['installer']
                scenario = dic_testcase['dependencies']['scenario']
                dep = Dependency(installer, scenario)

                testcase = TestCase(name=dic_testcase['name'],
                                    dependency=dep,
                                    description=dic_testcase['description'])
                tier.add_test(testcase)

            self.tier_objects.append(tier)

    def __str__(self):
        output = ""
        for i in range(0, len(self.tier_objects)):
            output += str(self.tier_objects[i]) + "\n"
        return output
