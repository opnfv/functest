#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Resources to handle environment related requests
"""

from flask import jsonify

from functest.api.actions.api_env import ApiEnv
from functest.api.base import ApiResource
from functest.api.common import api_utils
import functest.utils.functest_utils as ft_utils


class V1Envs(ApiResource):
    """ V1Envs Resource class"""

    def get(self):
        """ Get environment """
        environment_show = ApiEnv().show()
        return jsonify(environment_show)

    def post(self):
        """ Used to handle post request """
        return self._dispatch_post()

    def prepare(self, args):
        """ Prepare environment """
        ft_utils.execute_command("prepare_env start")
        return api_utils.result_handler(
            status=0, data="Env prepare successfully")
