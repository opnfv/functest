#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import click

from functest.cli.commands.cli_env import CliEnv
from functest.cli.commands.cli_os import CliOpenStack
from functest.cli.commands.cli_testcase import CliTestcase
from functest.cli.commands.cli_tier import CliTier

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='opnfv colorado.0.1 ')
def cli():
    pass

_env = CliEnv()
_openstack = CliOpenStack()
_testcase = CliTestcase()
_tier = CliTier()


@cli.group()
@click.pass_context
def env(ctx):
    pass


@cli.group()
@click.pass_context
def openstack(ctx):
    pass


@cli.group()
@click.pass_context
def testcase(ctx):
    pass


@cli.group()
@click.pass_context
def tier(ctx):
    pass


@openstack.command('check', help="Checks connectivity and status "
                   "to the OpenStack deployment.")
def os_check():
    _openstack.check()


@openstack.command('snapshot-create', help="Generates a snapshot of the "
                   "current OpenStack resources.")
def os_snapshot_create():
    _openstack.snapshot_create()


@openstack.command('snapshot-show', help="Prints the OpenStack snapshot.")
def os_snapshot_show():
    _openstack.snapshot_show()


@openstack.command('clean',
                   help="Cleans the OpenStack resources except the snapshot.")
def os_clean():
    _openstack.clean()


@openstack.command('show-credentials',
                   help="Prints the OpenStack credentials.")
def os_show_credentials():
    _openstack.show_credentials()


@openstack.command('fetch-rc', help="Fetch the OpenStack RC file from "
                   "the installer.")
def os_fetch_rc():
    _openstack.fetch_credentials()


@env.command('prepare', help="Prepares the Functest environment. This step is "
             "needed run the tests.")
def env_prepare():
    _env.prepare()


@env.command('show', help="Shows information about the current environment.")
def env_show():
    _env.show()


@env.command('status', help="Checks if the Functest environment is ready to "
             "run the tests.")
def env_status():
    _env.status()


@testcase.command('list', help="Lists the available testcases.")
def testcase_list():
    _testcase.list()


@testcase.command('show', help="Shows information about a test case.")
@click.argument('testname', type=click.STRING, required=True)
def testcase_show(testname):
    _testcase.show(testname)


@testcase.command('run', help="Executes a test case.")
@click.argument('testname', type=click.STRING, required=True)
@click.option('-n', '--noclean', is_flag=True, default=False,
              help='The created openstack resources by the test'
              'will not be cleaned after the execution.')
def testcase_run(testname, noclean):
    _testcase.run(testname, noclean)


@tier.command('list', help="Lists the available tiers.")
def tier_list():
    _tier.list()


@tier.command('show', help="Shows information about a tier.")
@click.argument('tiername', type=click.STRING, required=True)
def tier_show(tiername):
    _tier.show(tiername)


@tier.command('get-tests', help="Prints the tests in a tier.")
@click.argument('tiername', type=click.STRING, required=True)
def tier_gettests(tiername):
    _tier.gettests(tiername)


@tier.command('run', help="Executes all the tests within a tier.")
@click.argument('tiername', type=click.STRING, required=True)
@click.option('-n', '--noclean', is_flag=True, default=False,
              help='The created openstack resources by the tests'
              'will not be cleaned after the execution.')
def tier_run(tiername, noclean):
    _tier.run(tiername, noclean)
