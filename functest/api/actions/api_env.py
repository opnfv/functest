#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from functest.cli.commands.cli_env import Env


class ApiEnv(Env):
    """ Api Env class"""

    def __init__(self):
        super(ApiEnv, self).__init__()

    def show(self):
        _, env_show = super(ApiEnv, self).show()
        return env_show
