#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


import re

LINE_LENGTH = 72


def split_text(text, max_len):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        if len(line) + len(word) < max_len - 1:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    if line != "":
        lines.append(line)
    return lines


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
        lines = split_text(self.description, LINE_LENGTH - 6)

        out = ""
        out += ("+%s+\n" % ("=" * (LINE_LENGTH - 2)))
        out += ("| Tier:  " + self.name.ljust(LINE_LENGTH - 10) + "|\n")
        out += ("+%s+\n" % ("=" * (LINE_LENGTH - 2)))
        out += ("| Order: " + str(self.order).ljust(LINE_LENGTH - 10) + "|\n")
        out += ("| CI Loop: " + str(self.ci_loop).ljust(LINE_LENGTH - 12) +
                "|\n")
        out += ("| Description:".ljust(LINE_LENGTH - 1) + "|\n")
        for line in lines:
            out += ("|    " + line.ljust(LINE_LENGTH - 7) + " |\n")
        out += ("| Test cases:".ljust(LINE_LENGTH - 1) + "|\n")
        tests = self.get_test_names()
        if len(tests) > 0:
            for i in range(len(tests)):
                out += ("|    - %s |\n" % tests[i].ljust(LINE_LENGTH - 9))
        else:
            out += ("|    (There are no supported test cases "
                    .ljust(LINE_LENGTH - 1) + "|\n")
            out += ("|    in this tier for the given scenario) "
                    .ljust(LINE_LENGTH - 1) + "|\n")
        out += ("|".ljust(LINE_LENGTH - 1) + "|\n")
        out += ("+%s+\n" % ("-" * (LINE_LENGTH - 2)))
        return out


class TestCase:

    def __init__(self, name, dependency, criteria, blocking, description=""):
        self.name = name
        self.dependency = dependency
        self.description = description
        self.criteria = criteria
        self.blocking = blocking

    def is_compatible(self, ci_installer, ci_scenario):
        try:
            if ci_installer is not None:
                if re.search(self.dependency.get_installer(),
                             ci_installer) is None:
                    return False
            if ci_scenario is not None:
                if re.search(self.dependency.get_scenario(),
                             ci_scenario) is None:
                    return False
            return not (ci_scenario is None and ci_installer is None)
        except TypeError:
            return False

    def get_name(self):
        return self.name

    def get_criteria(self):
        return self.criteria

    def is_blocking(self):
        return self.blocking

    def __str__(self):
        lines = split_text(self.description, LINE_LENGTH - 6)

        out = ""
        out += ("+%s+\n" % ("=" * (LINE_LENGTH - 2)))
        out += ("| Testcase:  " + self.name.ljust(LINE_LENGTH - 14) + "|\n")
        out += ("+%s+\n" % ("=" * (LINE_LENGTH - 2)))
        out += ("| Description:".ljust(LINE_LENGTH - 1) + "|\n")
        for line in lines:
            out += ("|    " + line.ljust(LINE_LENGTH - 7) + " |\n")
        out += ("| Criteria:  " +
                self.criteria.ljust(LINE_LENGTH - 14) + "|\n")
        out += ("| Dependencies:".ljust(LINE_LENGTH - 1) + "|\n")
        installer = self.dependency.get_installer()
        scenario = self.dependency.get_scenario()
        out += ("|   - Installer:" + installer.ljust(LINE_LENGTH - 17) + "|\n")
        out += ("|   - Scenario :" + scenario.ljust(LINE_LENGTH - 17) + "|\n")
        out += ("|".ljust(LINE_LENGTH - 1) + "|\n")
        out += ("+%s+\n" % ("-" * (LINE_LENGTH - 2)))
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
