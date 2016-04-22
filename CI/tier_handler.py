#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


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
        array_str = []
        for test in self.tests_array:
            array_str.append(test.name)
        return array_str

    def __str__(self):
        return ("Tier info:\n"
                "    Name: " + self.name + "\n"
                "    Description: " + self.description + "\n"
                "    Order: " + str(self.order) + "\n"
                "    Test cases: " + str(self.get_tests()) + "\n")


class TestCase:
    def __init__(self, name, dependency, description=""):
        self.name = name
        self.dependency = dependency
        self.description = description

    def __str__(self):
        return ("Testcase info:\n"
                "    Name: " + self.name + "\n"
                "    Description: " + self.description + "\n"
                "    " + str(self.dependency) + "\n")


class Dependency:
    def __init__(self, installer, scenario):
        self.installer = installer
        self.scenario = scenario

    def __str__(self):
        return ("Dependency info:\n"
                "        installer: " + self.installer + "\n"
                "        scenario:  " + self.scenario + "\n")
