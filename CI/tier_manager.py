#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


class Tier:
    def __init__(self, name, description, order):
        self.tests_array = []
        self.name = name
        self.description = description
        self.order = order

    def add_test(self, testcase):
        self.tests_array.append(testcase)

    def get_tests(self):
        array_str = []
        for test in self.tests_array:
            array_str.append(test.name)
        return array_str

    def __str__(self):
        return ("Tier info:\n" +
                "\tName: " + self.name + "\n" +
                "\tDescription: " + self.description + "\n" +
                "\tOrder: " + self.order + "\n" +
                "\tTest cases: " + str(self.get_tests()) + "\n")


class Testcase:
    def __init__(self, name, description, dependency):
        self.name = name
        self.description = description
        self.dependency = dependency

    def __str__(self):
        return ("Testcase info:\n" +
                "\tName: " + self.name + "\n" +
                "\tName: " + self.name + "\n" +
                "\tDescription: " + self.description + "\n" +
                "\tDependencies: " + str(self.dependency) + "\n")


class Dependency:
    def __init__(self, installer, sdn, feature, mode):
        self.installer = installer
        self.sdn = sdn
        self.feature = feature
        self.mode = mode

    def __str__(self):
        return ("Dependency info:\n" +
                "\t" + self.installer + " os-[" + self.sdn + "]-[" +
                self.feature + "]-[" + self.mode + "]" + "\n" +
                "\t\t- installer: " + self.installer + "\n" +
                "\t\t- sdn Controller: " + self.sdn + "\n" +
                "\t\t- feature: " + self.feature + "\n" +
                "\t\t- mode: " + self.mode + "\n")
