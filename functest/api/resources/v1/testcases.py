#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from flask import jsonify

from functest.api.base import ApiResource
from functest.api.utils.api_utils import change_obj_to_dict
from functest.cli.commands.cli_testcase import CliTestcase


class V1Testcases(ApiResource):
    def get(self):
        testcases_list = CliTestcase().list()
        result = {'testcases': testcases_list.split('\n')[:-1]}
        return jsonify(result)


class V1Testcase(ApiResource):
    def get(self, testcase_name):
        testcase_info = change_obj_to_dict(CliTestcase().show(testcase_name))
        dependency_dict = change_obj_to_dict(testcase_info.get('dependency'))
        testcase_info.pop('name')
        testcase_info.pop('dependency')
        result = {'testcase': testcase_name}
        result.update(testcase_info)
        result.update({'dependency': dependency_dict})
        return jsonify(result)
