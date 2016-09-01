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

import click
import functest.ci.tier_builder as tb
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_vacation as vacation
from functest.utils.functest_utils import FUNCTEST_REPO as FUNCTEST_REPO

functest_yaml = ft_utils.get_functest_yaml()

FUNCTEST_CONF_DIR = functest_yaml.get("general").get(
    "directories").get("dir_functest_conf")
ENV_FILE = FUNCTEST_CONF_DIR + "/env_active"


class CliTestcase:

    def __init__(self):
        CI_INSTALLER_TYPE = os.getenv('INSTALLER_TYPE')
        CI_SCENARIO = os.getenv('DEPLOY_SCENARIO')
        testcases = ft_utils.get_testcases_file()
        self.tiers = tb.TierBuilder(CI_INSTALLER_TYPE, CI_SCENARIO, testcases)

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

    def run(self, testname, noclean=False):
        if testname == 'vacation':
            vacation.main()
        elif not os.path.isfile(ENV_FILE):
            click.echo("Functest environment is not ready. "
                       "Run first 'functest env prepare'")
        else:
            if noclean:
                cmd = ("python %s/ci/run_tests.py "
                       "-n -t %s" % (FUNCTEST_REPO, testname))
            else:
                cmd = ("python %s/ci/run_tests.py "
                       "-t %s" % (FUNCTEST_REPO, testname))
            ft_utils.execute_command(cmd)
