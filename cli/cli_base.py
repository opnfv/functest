import click

from functest.cli.commands.cli_env import CliEnv
from functest.cli.commands.cli_testcase import CliTestcase
from functest.cli.commands.cli_tier import CliTier

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='opnfv colorado.0.1 ')
def cli():
    pass

_env = CliEnv()
_testcase = CliTestcase()
_tier = CliTier()


@cli.group()
@click.pass_context
def env(ctx):
    pass


@cli.group()
@click.pass_context
def testcase(ctx):
    pass


@cli.group()
@click.pass_context
def tier(ctx):
    pass


# ###################
# env commands
# ###################
@env.command('show', help="write the help here")
def env_show():
    _env.show()


@env.command('status', help="write the help here")
def env_status():
    _env.status()


@env.command('getrc', help="write the help here")
def env_getrc():
    _env.getrc()


@env.command('sourcerc', help="write the help here")
def env_sourcerc():
    _env.sourcerc()


@env.command('setdefaults', help="write the help here")
def env_setdefaults():
    _env.setdefaults()


@env.command('getdefaults', help="write the help here")
def env_getdefaults():
    _env.getdefaults()


@env.command('clean', help="write the help here")
def env_clean():
    _env.clean()


# ###################
# testcase commands
# ###################
@testcase.command('list', help="write the help here")
def testcase_list():
    _testcase.list()


@testcase.command('show', help="write the help here")
@click.argument('testname', type=click.STRING, required=True)
def testcase_show(testname):
    _testcase.show(testname)


@testcase.command('run', help="write the help here")
@click.argument('testname', type=click.STRING, required=True)
def testcase_run(testname):
    _testcase.run(testname)


# ###################
# tier commands
# ###################
@tier.command('list', help="write the help here")
def tier_list():
    _tier.list()


@tier.command('show', help="write the help here")
@click.argument('tiername', type=click.STRING, required=True)
def tier_show(tiername):
    _tier.show(tiername)


@tier.command('run', help="write the help here")
@click.argument('tiername', type=click.STRING, required=True)
def tier_run(tiername):
    _tier.run(tiername)
