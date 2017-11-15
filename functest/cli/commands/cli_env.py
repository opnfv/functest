#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import click
import prettytable

from functest.utils.constants import CONST


class Env(object):

    def __init__(self):
        pass

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

        env_info = {'INSTALLER': installer_info,
                    'SCENARIO': scenario,
                    'POD': node,
                    'DEBUG FLAG': is_debug,
                    'BUILD_TAG': build_tag,
                    'STATUS': STATUS}

        return env_info


class CliEnv(Env):

    def __init__(self):
        super(CliEnv, self).__init__()

    def show(self):
        env_info = super(CliEnv, self).show()
        msg = prettytable.PrettyTable(
            header_style='upper', padding_width=5,
            field_names=['Functest Environment', 'value'])
        for key, value in env_info.iteritems():
            if key is not None:
                msg.add_row([key, value])
        click.echo(msg.get_string())
