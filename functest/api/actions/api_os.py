#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
"""

from functest.cli.commands.cli_os import OpenStack


class ApiOpenStack(OpenStack):

    def __init__(self):
        super(ApiOpenStack, self).__init__()

    @staticmethod
    def show_credentials():
        return OpenStack.show_credentials()
