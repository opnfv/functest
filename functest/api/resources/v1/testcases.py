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
from functest.api.actions.api_testcase import ApiTestcase
from functest.utils import error


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
