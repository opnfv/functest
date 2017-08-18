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

from functest.api.base import ApiResource
from functest.cli.commands.cli_env import Env
from functest.api.common import api_utils
import functest.utils.functest_utils as ft_utils


class V1Envs(ApiResource):
    """ V1Envs Resource class"""

    def get(self):  # pylint: disable=no-self-use
        """ Get environment """
        environment_show = Env().show()
        return jsonify(environment_show)

    def post(self):
        """ Used to handle post request """
        return self._dispatch_post()

    def prepare(self, args):  # pylint: disable=no-self-use, unused-argument
        """ Prepare environment """
        try:
            ft_utils.execute_command("prepare_env start")
        except Exception as err:  # pylint: disable=broad-except
            return api_utils.result_handler(status=1, data=str(err))
        return api_utils.result_handler(
            status=0, data="Prepare env successfully")
