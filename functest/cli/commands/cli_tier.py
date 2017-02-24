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
from functest.utils.constants import CONST
import functest.utils.functest_utils as ft_utils


class CliTier(object):

    def __init__(self):
        self.tiers = tb.TierBuilder(CONST.INSTALLER_TYPE,
                                    CONST.DEPLOY_SCENARIO,
                                    CONST.functest_testcases_yaml)

    def list(self):
        summary = ""
        for tier in self.tiers.get_tiers():
            summary += ("    - %s. %s:\n\t   %s\n"
                        % (tier.get_order(),
                           tier.get_name(),
                           tier.get_test_names()))
        click.echo(summary)

    def show(self, tiername):
        tier = self.tiers.get_tier(tiername)
        if tier is None:
            tier_names = self.tiers.get_tier_names()
            click.echo("The tier with name '%s' does not exist. "
                       "Available tiers are:\n  %s\n" % (tiername, tier_names))
        else:
            click.echo(self.tiers.get_tier(tiername))

    def gettests(self, tiername):
        tier = self.tiers.get_tier(tiername)
        if tier is None:
            tier_names = self.tiers.get_tier_names()
            click.echo("The tier with name '%s' does not exist. "
                       "Available tiers are:\n  %s\n" % (tiername, tier_names))
        else:
            tests = tier.get_test_names()
            click.echo("Test cases in tier '%s':\n %s\n" % (tiername, tests))

    @staticmethod
    def run(tiername, noclean=False, report=False):

        flags = ""
        if noclean:
            flags += "-n "
        if report:
            flags += "-r "

        if not os.path.isfile(CONST.env_active):
            click.echo("Functest environment is not ready. "
                       "Run first 'functest env prepare'")
        else:
            cmd = ("python %s/functest/ci/run_tests.py "
                   "%s -t %s" % (CONST.dir_repo_functest, flags, tiername))
            ft_utils.execute_command(cmd)
