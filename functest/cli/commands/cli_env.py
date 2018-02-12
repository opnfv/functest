#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import os

import click
import prettytable
import six


class Env(object):  # pylint: disable=too-few-public-methods

    @staticmethod
    def show():
        install_type = os.environ.get('INSTALLER_TYPE', 'Unknown')
        installer_ip = os.environ.get('INSTALLER_IP', 'Unknown')
        installer_info = ("%s, %s" % (install_type, installer_ip))
        scenario = os.environ.get('DEPLOY_SCENARIO', 'Unknown')
        node = os.environ.get('NODE_NAME', 'Unknown')
        build_tag = os.environ.get('BUILD_TAG', None)
        if build_tag:
            build_tag = build_tag.lstrip(
                "jenkins-").lstrip("functest").lstrip("-")

        env_info = {'INSTALLER': installer_info,
                    'SCENARIO': scenario,
                    'POD': node,
                    'BUILD_TAG': build_tag}

        return env_info


class CliEnv(object):  # pylint: disable=too-few-public-methods

    @staticmethod
    def show():
        env_info = Env.show()
        msg = prettytable.PrettyTable(
            header_style='upper', padding_width=5,
            field_names=['Functest Environment', 'value'])
        for key, value in six.iteritems(env_info):
            if key is not None:
                msg.add_row([key, value])
        click.echo(msg.get_string())
