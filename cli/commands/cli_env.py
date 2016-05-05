#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import click
import os

import functest.utils.functest_utils as ft_utils

ENV_FILE = "/home/opnfv/functest/conf/env_active"


class CliEnv:
    def __init__(self):
        pass

    def prepare(self):
        cmd = ("python /home/opnfv/repos/functest/ci/prepare_env.py start")
        ft_utils.execute_command(cmd)

    def show(self):
        click.echo("env show")

    def status(self):
        ret_val = 0
        if not os.path.isfile(ENV_FILE):
            click.echo("Functest environment is not installed.\n")
            ret_val = 1
        return ret_val
