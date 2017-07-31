#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import json
import os

from functest.cli.commands.cli_testcase import Testcase
import functest.utils.functest_utils as ft_utils
from functest.utils.constants import CONST


class ApiTestcase(Testcase):

    def __init__(self):
        super(ApiTestcase, self).__init__()

    def list(self):
        return super(ApiTestcase, self).list()

    def show(self, case_name):
        return super(ApiTestcase, self).show(case_name)

    @staticmethod
    def run(args):
        flags = ""
        if args.get('noclean'):
            flags += "-n "
        if args.get('report'):
            flags += "-r "
        case_name = args.get('testcase')

        if not os.path.isfile(CONST.__getattribute__('env_active')):
            return ("Functest environment is not ready.")

        try:
            cmd = "run_tests {}-t {}".format(flags, case_name)
            runner = ft_utils.execute_command(cmd)
        except Exception:
            result = 'FAIL'
        if runner == os.EX_OK:
            result = 'PASS'
        else:
            result = 'FAIL'

        env_info = {
            'installer': CONST.__getattribute__('INSTALLER_TYPE'),
            'scenario': CONST.__getattribute__('DEPLOY_SCENARIO'),
            'build_tag': CONST.__getattribute__('BUILD_TAG'),
            'ci_loop': CONST.__getattribute__('CI_LOOP')
        }
        result = {
            'task_id': args.get('task_id'),
            'case_name': case_name,
            'env_info': env_info,
            'result': result
        }

        print("Done, exiting")
        return {'result': result}
