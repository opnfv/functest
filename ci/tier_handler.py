#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


import re


class Tier:
    def __init__(self, name, order, ci, description=""):
        self.tests_array = []
        self.name = name
        self.order = order
        self.ci = ci
        self.description = description

    def add_test(self, testcase):
        self.tests_array.append(testcase)

    def get_tests(self):
        array_tests = []
        for test in self.tests_array:
            array_tests.append(test)
        return array_tests

    def get_test_names(self):
        array_tests = []
        for test in self.tests_array:
            array_tests.append(test.get_name())
        return array_tests

    def get_test(self, test_name):
        if self.is_test(test_name):
            for test in self.tests_array:
                if test.get_name() == test_name:
                    return test
        return None

    def is_test(self, test_name):
        for test in self.tests_array:
            if test.get_name() == test_name:
                return True
        return False

    def get_name(self):
        return self.name

    def __str__(self):
        return ("Tier info:\n"
                "    Name: " + self.name + "\n"
                "    Description: " + self.description + "\n"
                "    Order: " + str(self.order) + "\n"
                "    Test cases: " + str(self.get_test_names()) + "\n")


class TestCase:
    def __init__(self, name, dependency, description=""):
        self.name = name
        self.dependency = dependency
        self.description = description

    def is_compatible(self, ci_installer, ci_scenario):
        if re.search(self.dependency.get_installer(), ci_installer) is None:
            return False

        if re.search(self.dependency.get_scenario(), ci_scenario) is None:
            return False

        return True

    def get_name(self):
        return self.name

    def __str__(self):
        return ("Testcase info:\n"
                "    Name: " + self.name + "\n"
                "    Description: " + self.description + "\n"
                "    " + str(self.dependency) + "\n")


class Dependency:
    def __init__(self, installer, scenario):
        self.installer = installer
        self.scenario = scenario

    def get_installer(self):
        return self.installer

    def get_scenario(self):
        return self.scenario

    def __str__(self):
        return ("Dependency info:\n"
                "        installer: " + self.installer + "\n"
                "        scenario:  " + self.scenario + "\n")
