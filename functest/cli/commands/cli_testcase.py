#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

""" global variables """

import os
import pkg_resources
import sys

import click

from functest.ci import run_tests
from functest.ci import tier_builder
from functest.utils.constants import CONST
from functest.utils import functest_vacation


class CliTestcase(object):

    def __init__(self):
        self.tiers = tier_builder.TierBuilder(
            CONST.__getattribute__('INSTALLER_TYPE'),
            CONST.__getattribute__('DEPLOY_SCENARIO'),
            pkg_resources.resource_filename('functest', 'ci/testcases.yaml'))

    def list(self):
        summary = ""
        for tier in self.tiers.get_tiers():
            for test in tier.get_tests():
                summary += (" %s\n" % test.get_name())
        click.echo(summary)

    def show(self, testname):
        description = self.tiers.get_test(testname)
        if description is None:
            click.echo("The test case '%s' does not exist or is not supported."
                       % testname)

        click.echo(description)

    @staticmethod
    def run(testname, noclean=False, report=False):
        if testname == 'vacation':
            functest_vacation.main()
        elif not os.path.isfile(CONST.__getattribute__('env_active')):
            click.echo("Functest environment is not ready. "
                       "Run first 'functest env prepare'")
        else:
            tests = testname.split(",")
            for test in tests:
                sys.argv[3] = 'test'
                sys.argv[4] = test
                sys.argv[5] = 'report'
                sys.argv[6] = report
                sys.argv[7] = 'noclean'
                sys.argv[8] = noclean
                run_tests.main()
