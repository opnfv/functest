#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import pkg_resources

import click
from xtesting.ci import tier_builder

from functest.utils import functest_utils


class Tier(object):

    def __init__(self):
        self.tiers = tier_builder.TierBuilder(
            pkg_resources.resource_filename('functest', 'ci/testcases.yaml'))

    def list(self):
        summary = ""
        for tier in self.tiers.get_tiers():
            summary += ("    - %s. %s:\n\t   %s\n"
                        % (tier.get_order(),
                           tier.get_name(),
                           tier.get_test_names()))
        return summary

    def show(self, name):
        tier = self.tiers.get_tier(name)
        if tier is None:
            return None
        tier_info = self.tiers.get_tier(name)
        return tier_info

    def gettests(self, name):
        tier = self.tiers.get_tier(name)
        if tier is None:
            return None
        tests = tier.get_test_names()
        return tests

    @staticmethod
    def get_flags(noclean=False, report=False):
        flags = ""
        if noclean:
            flags += "-n "
        if report:
            flags += "-r "
        return flags

    @staticmethod
    def run(name, noclean=False, report=False):
        cmd = "run_tests {}-t {}".format(Tier.get_flags(noclean, report), name)
        functest_utils.execute_command(cmd)


class CliTier(Tier):

    def list(self):
        click.echo(super(CliTier, self).list())

    def show(self, name):
        tier_info = super(CliTier, self).show(name)
        if tier_info:
            click.echo(tier_info)
        else:
            tier_names = self.tiers.get_tier_names()
            click.echo("The tier with name '%s' does not exist. "
                       "Available tiers are:\n  %s\n" % (name, tier_names))

    def gettests(self, name):
        tests = super(CliTier, self).gettests(name)
        if tests:
            click.echo("Test cases in tier '%s':\n %s\n" % (name, tests))
        else:
            tier_names = self.tiers.get_tier_names()
            click.echo("The tier with name '%s' does not exist. "
                       "Available tiers are:\n  %s\n" % (name, tier_names))
