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

from flask import jsonify

from functest.api.base import ApiResource
from functest.api.utils import api_utils
from functest.cli.commands.cli_testcase import ApiTestcase
from functest.utils.constants import CONST


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
        print("------class V1Testcase, testcase_name:%s" % testcase_name)
        print("------class V1Testcase, type(testcase_name):%s" % type(testcase_name))
        testcase = ApiTestcase().show(testcase_name)
        if not testcase:
            return api_utils.result_handler(
                CONST.__getattribute__('api_error'), 'case not exists')
        testcase_info = api_utils.change_obj_to_dict(testcase)
        dependency_dict = api_utils.change_obj_to_dict(
            testcase_info.get('dependency'))
        testcase_info.pop('name')
        testcase_info.pop('dependency')
        result = {'testcase': testcase_name}
        result.update(testcase_info)
        result.update({'dependency': dependency_dict})
        return jsonify(result)
