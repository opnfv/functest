#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from flask import jsonify

from functest.cli.commands.cli_os import CliOpenStack
from functest.utils import openstack_utils as os_utils
from functest.utils.constants import CONST
from functest.api import ApiResource


class V1Creds(ApiResource):
    def get(self):
        os_utils.source_credentials(CONST.__getattribute__('openstack_creds'))
        credentials_show = CliOpenStack.show_credentials()
        return jsonify(credentials_show)
