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
    def __init__(self, name, order, ci_loop, description=""):
        self.tests_array = []
        self.name = name
        self.order = order
        self.ci_loop = ci_loop
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

    def get_order(self):
        return self.order

    def get_ci_loop(self):
        return self.ci_loop

    def __str__(self):
        lines = []
        line_max = 50
        line = ""
        line_count = 0
        for i in range(len(self.description)):
            line += self.description[i]
            if line_count >= line_max - 1:
                line_count = 0
                lines.append(line)
                line = ""
            else:
                line_count += 1
        if line != "":
            lines.append(line)

        out = ""
        out += ("+=======================================================+\n")
        out += ("| Tier:  " + self.name.ljust(47) + "|\n")
        out += ("+=======================================================+\n")
        out += ("| Order: " + str(self.order).ljust(47) + "|\n")
        out += ("| CI Loop: " + str(self.ci_loop).ljust(45) + "|\n")
        out += ("| Description:                                          |\n")
        for i in range(len(lines)):
            out += ("|    " + lines[i].ljust(50) + " |\n")
        out += ("| Test cases:                                           |\n")
        tests = self.get_test_names()
        if len(tests) > 0:
            for i in range(len(tests)):
                out += ("|    - %s |\n" % tests[i].ljust(48))
        else:
            out += ("|    (There are no supported test cases "
                    .ljust(56) + "|\n")
            out += ("|    in this tier for the given scenario) "
                    .ljust(56) + "|\n")
        out += ("|".ljust(56) + "|\n")
        out += ("+-------------------------------------------------------+\n")
        return out


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
        lines = []
        line_max = 50
        line = ""
        line_count = 0
        for i in range(len(self.description)):
            line += self.description[i]
            if line_count >= line_max - 1:
                line_count = 0
                lines.append(line)
                line = ""
            else:
                line_count += 1
        if line != "":
            lines.append(line)

        out = ""
        out += ("+=======================================================+\n")
        out += ("| Testcase:  " + self.name.ljust(43) + "|\n")
        out += ("+=======================================================+\n")
        out += ("| Description:                                          |\n")
        for i in range(len(lines)):
            out += ("|    " + lines[i].ljust(50) + " |\n")
        out += ("| Dependencies:                                         |\n")
        installer = self.dependency.get_installer()
        scenario = self.dependency.get_scenario()
        out += ("|    - Installer: " + installer.ljust(38) + "|\n")
        out += ("|    - Scenario : " + scenario.ljust(38) + "|\n")
        out += ("|".ljust(56) + "|\n")
        out += ("+-------------------------------------------------------+\n")
        return out


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
