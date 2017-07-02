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
import prettytable

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
                    os.remove(CONST.__getattribute__('env_active'))
                    break
                elif answer.lower() in ["n", "no"]:
                    return
                else:
                    answer = raw_input("Invalid answer. Please type [y|n]\n")

        ft_utils.execute_command("prepare_env start")

    def show(self):
        def _get_value(attr, default='Unknown'):
            return attr if attr else default

        install_type = _get_value(CONST.__getattribute__('INSTALLER_TYPE'))
        installer_ip = _get_value(CONST.__getattribute__('INSTALLER_IP'))
        installer_info = ("%s, %s" % (install_type, installer_ip))
        scenario = _get_value(CONST.__getattribute__('DEPLOY_SCENARIO'))
        node = _get_value(CONST.__getattribute__('NODE_NAME'))
        is_debug = _get_value(CONST.__getattribute__('CI_DEBUG'), 'false')
        build_tag = CONST.__getattribute__('BUILD_TAG')
        if build_tag is not None:
            build_tag = build_tag.lstrip(
                "jenkins-").lstrip("functest").lstrip("-")

        STATUS = "not ready"
        if self.status(verbose=False) == 0:
            STATUS = "ready"

        msg = prettytable.PrettyTable(
            header_style='upper', padding_width=5,
            field_names=['Functest Environment', 'value'])
        msg.add_row(['INSTALLER', installer_info])
        msg.add_row(['SCENARIO', scenario])
        msg.add_row(['POD', node])
        if build_tag:
            msg.add_row(['BUILD TAG', build_tag])
        msg.add_row(['DEBUG FLAG', is_debug])
        msg.add_row(['STATUS', STATUS])
        click.echo(msg.get_string())

    def status(self, verbose=True):
        ret_val = 0
        if not os.path.isfile(CONST.__getattribute__('env_active')):
            if verbose:
                click.echo("Functest environment is not installed.\n")
            ret_val = 1
        elif verbose:
            click.echo("Functest environment ready to run tests.\n")

        return ret_val
