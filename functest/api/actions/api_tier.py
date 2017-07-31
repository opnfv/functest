#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import os

from functest.cli.commands.cli_tier import Tier
import functest.utils.functest_utils as ft_utils
from functest.utils.constants import CONST


class ApiTier(Tier):

    def __init__(self):
        super(ApiTier, self).__init__()

    def list(self):
        return super(ApiTier, self).list()

    def show(self, tiername):
        return super(ApiTier, self).show(tiername)

    def gettests(self, tiername):
        return super(ApiTier, self).gettests(tiername)

    @staticmethod
    def run(args):

        flags = ""
        if args.get('noclean'):
            flags += "-n "
        if args.get('report'):
            flags += "-r "
        tier_name = args.get('tier')

        if not os.path.isfile(CONST.__getattribute__('env_active')):
            return ("Functest environment is not ready.")

        testcases_result = {}
        for testcase in ApiTier().gettests(tier_name):
            try:
                cmd = "run_tests {}-t {}".format(flags, testcase)
                runner = ft_utils.execute_command(cmd)
            except KeyboardInterrupt:
                raise
            if runner == os.EX_OK:
                result = 'PASS'
            else:
                result = 'FAIL'

            testcases_result[testcase] = result

        env_info = {
            'installer': CONST.__getattribute__('INSTALLER_TYPE'),
            'scenario': CONST.__getattribute__('DEPLOY_SCENARIO'),
            'build_tag': CONST.__getattribute__('BUILD_TAG'),
            'ci_loop': CONST.__getattribute__('CI_LOOP')
        }

        result = {
            'task_id': args.get('task_id'),
            'tier_name': tier_name,
            'env_info': env_info,
            'result': testcases_result
        }
        print("Done, exiting")
        return {'result': result}
