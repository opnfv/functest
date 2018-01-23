#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import click

from functest.cli.commands import cli_tier
from functest.utils import functest_utils


class Testcase(cli_tier.Tier):

    def list(self):
        summary = ""
        for tier in self.tiers.get_tiers():
            for test in tier.get_tests():
                summary += (" %s\n" % test.get_name())
        return summary

    def show(self, name):
        description = self.tiers.get_test(name)
        return description

    @staticmethod
    def run(name, noclean=False, report=False):
        tests = name.split(",")
        for test in tests:
            cmd = "run_tests {}-t {}".format(
                Testcase.get_flags(noclean, report), test)
            functest_utils.execute_command(cmd)


class CliTestcase(Testcase):

    def list(self):
        click.echo(super(CliTestcase, self).list())

    def show(self, name):
        testcase_show = super(CliTestcase, self).show(name)
        if testcase_show:
            click.echo(testcase_show)
        else:
            click.echo("The test case '%s' does not exist or is not supported."
                       % name)
