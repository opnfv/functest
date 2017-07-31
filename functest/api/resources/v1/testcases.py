#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Resources to handle testcase related requests
"""

import uuid
import logging

from flask import jsonify

from functest.api.actions.api_testcase import ApiTestcase
from functest.api.base import ApiResource
from functest.api.common import api_utils, error, thread
from functest.api.database.v1.handlers import TasksHandler


LOGGER = logging.getLogger(__name__)


class V1Testcases(ApiResource):
    """ V1Testcases Resource class"""

    def get(self):
        """ GET all testcases """
        testcases_list = ApiTestcase().list()
        result = {'testcases': testcases_list.split('\n')[:-1]}
        return jsonify(result)


class V1Testcase(ApiResource):
    """ V1Testcase Resource class"""

    def get(self, testcase_name):
        """ GET the info of one testcase"""
        testcase = ApiTestcase().show(testcase_name)
        if not testcase:
            return error.notFoundError("The test case '%s' does not exist or "
                                       "is not supported." % testcase_name)
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

        task_thread = thread.TaskThread(ApiTestcase.run, task_args, TasksHandler())
        task_thread.start()

        results = {'testcase': case_name, 'task_id': task_id}
        return jsonify(results)
