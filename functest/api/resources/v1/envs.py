#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from flask import jsonify

from functest.cli.commands.cli_env import CliEnv
from functest.api import ApiResource


class V1Envs(ApiResource):
    def get(self):
        environment_show = CliEnv().show()
        return jsonify(environment_show)

    def post(self):
        return self._dispatch_post()

    def prepare(self, args):
        print("def prepare")
        CliEnv().prepare()
