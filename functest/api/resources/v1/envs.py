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

import IPy
from flask import jsonify

from functest.api.base import ApiResource
from functest.api.common import api_utils
from functest.cli.commands.cli_env import Env
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

    def update_hosts(self, hosts_info):  # pylint: disable=no-self-use
        """ Update hosts info """

        if not isinstance(hosts_info, dict):
            return api_utils.result_handler(
                status=1, data='Error, args should be a dict')

        for key, value in hosts_info.items():
            if key:
                try:
                    IPy.IP(value)
                except Exception:  # pylint: disable=broad-except
                    return api_utils.result_handler(
                        status=1, data='The IP %s is invalid' % value)
            else:
                return api_utils.result_handler(
                    status=1, data='Domain name is absent')

        try:
            functest_flag = "# SUT hosts info for Functest"
            hosts_list = ('\n{} {} {}'.format(ip, host_name, functest_flag)
                          for host_name, ip in hosts_info.items())

            with open("/etc/hosts", 'r') as file_hosts:
                origin_lines = [line for line in file_hosts
                                if functest_flag not in line]

            with open("/etc/hosts", 'w') as file_hosts:
                file_hosts.writelines(origin_lines)
                file_hosts.write(functest_flag)
                file_hosts.writelines(hosts_list)
        except Exception:  # pylint: disable=broad-except
            return api_utils.result_handler(
                status=1, data='Error when updating hosts info')
        else:
            return api_utils.result_handler(
                status=0, data='Update hosts info successfully')
