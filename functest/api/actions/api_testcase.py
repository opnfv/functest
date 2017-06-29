#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
"""

from functest.cli.commands.cli_testcase import Testcase


class ApiTestcase(Testcase):

    def __init__(self):
        super(ApiTestcase, self).__init__()

    def list(self):
        return super(ApiTestcase, self).list()

    def show(self, testname):
        return super(ApiTestcase, self).show(testname)
