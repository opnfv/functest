#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging.config
import pkg_resources

import click

from functest.cli.commands.cli_env import CliEnv
from functest.cli.commands.cli_os import CliOpenStack
from functest.cli.commands.cli_testcase import CliTestcase
from functest.cli.commands.cli_tier import CliTier


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='opnfv colorado.0.1 ')
def cli():
    logging.config.fileConfig(pkg_resources.resource_filename(
        'functest', 'ci/logging.ini'))
    logging.captureWarnings(True)


ENV = CliEnv()
OPENSTACK = CliOpenStack()
TESTCASE = CliTestcase()
TIER = CliTier()


@cli.group()
@click.pass_context
def env(ctx):  # pylint: disable=unused-argument
    pass


@cli.group()
@click.pass_context
def openstack(ctx):  # pylint: disable=unused-argument
    pass


@cli.group()
@click.pass_context
def testcase(ctx):  # pylint: disable=unused-argument
    pass


@cli.group()
@click.pass_context
def tier(ctx):  # pylint: disable=unused-argument
    pass


@openstack.command('check', help="Checks connectivity and status "
                   "to the OpenStack deployment.")
def os_check():
    OPENSTACK.check()


@openstack.command('show-credentials',
                   help="Prints the OpenStack credentials.")
def os_show_credentials():
    OPENSTACK.show_credentials()


@env.command('show', help="Shows information about the current environment.")
def env_show():
    ENV.show()


@testcase.command('list', help="Lists the available testcases.")
def testcase_list():
    TESTCASE.list()


@testcase.command('show', help="Shows information about a test case.")
@click.argument('testname', type=click.STRING, required=True)
def testcase_show(testname):
    TESTCASE.show(testname)


@testcase.command('run', help="Executes a test case.")
@click.argument('testname', type=click.STRING, required=True)
@click.option('-n', '--noclean', is_flag=True, default=False,
              help='The created openstack resources by the test'
              'will not be cleaned after the execution.')
@click.option('-r', '--report', is_flag=True, default=False,
              help='Push results to the results DataBase. Only CI Pods'
              'have rights to do that.')
def testcase_run(testname, noclean, report):
    TESTCASE.run(testname, noclean, report)


@tier.command('list', help="Lists the available tiers.")
def tier_list():
    TIER.list()


@tier.command('show', help="Shows information about a tier.")
@click.argument('tiername', type=click.STRING, required=True)
def tier_show(tiername):
    TIER.show(tiername)


@tier.command('get-tests', help="Prints the tests in a tier.")
@click.argument('tiername', type=click.STRING, required=True)
def tier_gettests(tiername):
    TIER.gettests(tiername)


@tier.command('run', help="Executes all the tests within a tier.")
@click.argument('tiername', type=click.STRING, required=True)
@click.option('-n', '--noclean', is_flag=True, default=False,
              help='The created openstack resources by the tests'
              'will not be cleaned after the execution.')
@click.option('-r', '--report', is_flag=True, default=False,
              help='Push results to the results DataBase. Only CI Pods'
              'have rights to do that.')
def tier_run(tiername, noclean, report):
    TIER.run(tiername, noclean, report)
