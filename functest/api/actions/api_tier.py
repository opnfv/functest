#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
"""

from functest.cli.commands.cli_tier import Tier


class ApiTier(Tier):

    def __init__(self):
        super(ApiTier, self).__init__()

    def list(self):
        return super(ApiTier, self).list()

    def show(self, tiername):
        return super(ApiTier, self).show(tiername)

    def gettests(self, tiername):
        return super(ApiTier, self).gettests(tiername)
