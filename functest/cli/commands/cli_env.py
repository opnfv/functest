#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import os

import click
import git

from functest.utils.constants import CONST
import functest.utils.functest_utils as ft_utils


class CliEnv(object):

    def __init__(self):
        pass

    def prepare(self):
        if self.status(verbose=False) == 0:
            answer = raw_input("It seems that the environment has been "
                               "already prepared. Do you want to do "
                               "it again? [y|n]\n")
            while True:
                if answer.lower() in ["y", "yes"]:
                    os.remove(CONST.env_active)
                    break
                elif answer.lower() in ["n", "no"]:
                    return
                else:
                    answer = raw_input("Invalid answer. Please type [y|n]\n")

        cmd = ("python %s/functest/ci/prepare_env.py start" %
               CONST.dir_repo_functest)
        ft_utils.execute_command(cmd)

    def show(self):
        def _get_value(attr, default='Unknown'):
            return attr if attr else default

        install_type = _get_value(CONST.INSTALLER_TYPE)
        installer_ip = _get_value(CONST.INSTALLER_IP)
        installer_info = ("%s, %s" % (install_type, installer_ip))
        scenario = _get_value(CONST.DEPLOY_SCENARIO)
        node = _get_value(CONST.NODE_NAME)
        repo_h = git.Repo(CONST.dir_repo_functest).head
        if repo_h.is_detached:
            git_branch = 'detached from FETCH_HEAD'
            git_hash = repo_h.commit.hexsha
        else:
            branch = repo_h.reference
            git_branch = branch.name
            git_hash = branch.commit.hexsha
        is_debug = _get_value(CONST.CI_DEBUG, 'false')
        build_tag = CONST.BUILD_TAG
        if build_tag is not None:
            build_tag = build_tag.lstrip(
                "jenkins-").lstrip("functest").lstrip("-")

        STATUS = "not ready"
        if self.status(verbose=False) == 0:
            STATUS = "ready"

        click.echo("+======================================================+")
        click.echo("| Functest Environment info                            |")
        click.echo("+======================================================+")
        click.echo("|  INSTALLER: %s|" % installer_info.ljust(41))
        click.echo("|   SCENARIO: %s|" % scenario.ljust(41))
        click.echo("|        POD: %s|" % node.ljust(41))
        click.echo("| GIT BRACNH: %s|" % git_branch.ljust(41))
        click.echo("|   GIT HASH: %s|" % git_hash.ljust(41))
        if build_tag:
            click.echo("|  BUILD TAG: %s|" % build_tag.ljust(41))
        click.echo("| DEBUG FLAG: %s|" % is_debug.ljust(41))
        click.echo("+------------------------------------------------------+")
        click.echo("|     STATUS: %s|" % STATUS.ljust(41))
        click.echo("+------------------------------------------------------+")
        click.echo("")

    def status(self, verbose=True):
        ret_val = 0
        if not os.path.isfile(CONST.env_active):
            if verbose:
                click.echo("Functest environment is not installed.\n")
            ret_val = 1
        elif verbose:
            click.echo("Functest environment ready to run tests.\n")

        return ret_val
