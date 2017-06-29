#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from flask import jsonify

from functest.cli.commands.cli_testcase import CliTestcase
from functest.api import ApiResource


class V1Testcases(ApiResource):
    def get(self):
        testcases_list = CliTestcase().list()
        result = {'testcases': testcases_list.split('\n')[:-1]}
        return jsonify(result)


class V1Testcase(ApiResource):
    def get(self, testcase_name):
        testcase_info = CliTestcase().show(testcase_name)
        dependency_dict = testcase_info.__dict__.get('dependency').__dict__
        testcase_info.__dict__.pop('name')
        testcase_info.__dict__.pop('dependency')
        result = {'testcase': testcase_name}
        result.update(testcase_info.__dict__)
        result.update({'dependency': dependency_dict})
        return jsonify(result)
