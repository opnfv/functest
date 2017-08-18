#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Resources to handle testcase related requests
"""

import os
import logging
import uuid

from flask import abort, jsonify

from functest.api.base import ApiResource
from functest.api.common import api_utils, thread
from functest.cli.commands.cli_testcase import Testcase
from functest.api.database.v1.handlers import TasksHandler
from functest.utils.constants import CONST
import functest.utils.functest_utils as ft_utils

LOGGER = logging.getLogger(__name__)


class V1Testcases(ApiResource):
    """ V1Testcases Resource class"""

    def get(self):  # pylint: disable=no-self-use
        """ GET all testcases """
        testcases_list = Testcase().list()
        result = {'testcases': testcases_list.split('\n')[:-1]}
        return jsonify(result)


class V1Testcase(ApiResource):
    """ V1Testcase Resource class"""

    def get(self, testcase_name):  # pylint: disable=no-self-use
        """ GET the info of one testcase"""
        testcase = Testcase().show(testcase_name)
        if not testcase:
            abort(404, "The test case '%s' does not exist or is not supported"
                  % testcase_name)
        testcase_info = api_utils.change_obj_to_dict(testcase)
        dependency_dict = api_utils.change_obj_to_dict(
            testcase_info.get('dependency'))
        testcase_info.pop('name')
        testcase_info.pop('dependency')
        result = {'testcase': testcase_name}
        result.update(testcase_info)
        result.update({'dependency': dependency_dict})
        return jsonify(result)

    def post(self):
        """ Used to handle post request """
        return self._dispatch_post()

    def run_test_case(self, args):
        """ Run a testcase """
        try:
            case_name = args['testcase']
        except KeyError:
            return api_utils.result_handler(
                status=1, data='testcase name must be provided')

        task_id = str(uuid.uuid4())

        task_args = {'testcase': case_name, 'task_id': task_id}

        task_args.update(args.get('opts', {}))

        task_thread = thread.TaskThread(self._run, task_args, TasksHandler())
        task_thread.start()

        results = {'testcase': case_name, 'task_id': task_id}
        return jsonify(results)

    def _run(self, args):  # pylint: disable=no-self-use
        """ The built_in function to run a test case """

        case_name = args.get('testcase')

        if not os.path.isfile(CONST.__getattribute__('env_active')):
            raise Exception("Functest environment is not ready.")
        else:
            try:
                cmd = "run_tests -t {}".format(case_name)
                runner = ft_utils.execute_command(cmd)
            except Exception:  # pylint: disable=broad-except
                result = 'FAIL'
                LOGGER.exception("Running test case %s failed!", case_name)
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

            return {'result': result}
