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

import logging
import os
import re
import socket
import uuid

from flask import jsonify
from flasgger.utils import swag_from
import pkg_resources
from six.moves import configparser

from functest.api.base import ApiResource
from functest.api.common import api_utils, thread
from functest.cli.commands.cli_testcase import Testcase
from functest.api.database.v1.handlers import TasksHandler
from functest.utils import config
from functest.utils import env
import functest.utils.functest_utils as ft_utils

LOGGER = logging.getLogger(__name__)

ADDRESS = socket.gethostbyname(socket.gethostname())
ENDPOINT_TESTCASES = ('http://{}:5000/api/v1/functest/testcases'
                      .format(ADDRESS))


class V1Testcases(ApiResource):
    """ V1Testcases Resource class"""

    @swag_from(pkg_resources.resource_filename(
        'functest', 'api/swagger/testcases.yaml'))
    def get(self):  # pylint: disable=no-self-use
        """ GET all testcases """
        testcases_list = Testcase().list()
        result = {'testcases': re.split(' |\n ', testcases_list)[1:]}
        return jsonify(result)


class V1Testcase(ApiResource):
    """ V1Testcase Resource class"""

    @swag_from(
        pkg_resources.resource_filename('functest',
                                        'api/swagger/testcase.yaml'),
        endpoint='{0}/<testcase_name>'.format(ENDPOINT_TESTCASES))
    def get(self, testcase_name):  # pylint: disable=no-self-use
        """ GET the info of one testcase"""
        testcase = Testcase().show(testcase_name)
        if not testcase:
            return api_utils.result_handler(
                status=1,
                data="The test case '%s' does not exist or is not supported"
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

    @swag_from(
        pkg_resources.resource_filename('functest',
                                        'api/swagger/testcase_run.yaml'),
        endpoint='{0}/action'.format(ENDPOINT_TESTCASES))
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

        testcase = Testcase().show(case_name)
        if not testcase:
            return api_utils.result_handler(
                status=1,
                data="The test case '%s' does not exist or is not supported"
                % case_name)

        task_id = str(uuid.uuid4())

        task_args = {'testcase': case_name, 'task_id': task_id}

        task_args.update(args.get('opts', {}))

        task_thread = thread.TaskThread(self._run, task_args, TasksHandler())
        task_thread.start()

        result = {'testcase': case_name, 'task_id': task_id}
        return jsonify({'result': result})

    def _run(self, args):  # pylint: disable=no-self-use
        """ The built_in function to run a test case """

        case_name = args.get('testcase')
        self._update_logging_ini(args.get('task_id'))

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
            'installer': env.get('INSTALLER_TYPE'),
            'scenario': env.get('DEPLOY_SCENARIO'),
            'build_tag': env.get('BUILD_TAG'),
            'ci_loop': env.get('CI_LOOP')
        }
        result = {
            'task_id': args.get('task_id'),
            'testcase': case_name,
            'env_info': env_info,
            'result': result
        }

        return {'result': result}

    def _update_logging_ini(self, task_id):  # pylint: disable=no-self-use
        """ Update the log file for each task"""
        rconfig = configparser.RawConfigParser()
        rconfig.read(
            pkg_resources.resource_filename('functest', 'ci/logging.ini'))
        log_path = os.path.join(getattr(config.CONF, 'dir_results'),
                                '{}.log'.format(task_id))
        rconfig.set('handler_file', 'args', '("{}",)'.format(log_path))

        with open(
            pkg_resources.resource_filename(
                'functest', 'ci/logging.ini'), 'wb') as configfile:
            rconfig.write(configfile)
