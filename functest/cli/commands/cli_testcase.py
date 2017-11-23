#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

""" global variables """

import pkg_resources

import click

import functest.ci.tier_builder as tb
from functest.utils.constants import CONST
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_vacation as vacation


class Testcase(object):

    def __init__(self):
        self.tiers = tb.TierBuilder(
            CONST.__getattribute__('INSTALLER_TYPE'),
            CONST.__getattribute__('DEPLOY_SCENARIO'),
            pkg_resources.resource_filename('functest', 'ci/testcases.yaml'))

    def list(self):
        summary = ""
        for tier in self.tiers.get_tiers():
            for test in tier.get_tests():
                summary += (" %s\n" % test.get_name())
        return summary

    def show(self, testname):
        description = self.tiers.get_test(testname)
        return description

    @staticmethod
    def run(testname, noclean=False, report=False):

        flags = ""
        if noclean:
            flags += "-n "
        if report:
            flags += "-r "

        if testname == 'vacation':
            vacation.main()
        else:
            tests = testname.split(",")
            for test in tests:
                cmd = "run_tests {}-t {}".format(flags, test)
                ft_utils.execute_command(cmd)


class CliTestcase(Testcase):

    def __init__(self):
        super(CliTestcase, self).__init__()

    def list(self):
        click.echo(super(CliTestcase, self).list())

    def show(self, testname):
        testcase_show = super(CliTestcase, self).show(testname)
        if testcase_show:
            click.echo(testcase_show)
        else:
            click.echo("The test case '%s' does not exist or is not supported."
                       % testname)
