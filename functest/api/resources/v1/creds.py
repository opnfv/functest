#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Resources to handle openstack related requests
"""

from flask import jsonify

from functest.api.base import ApiResource
from functest.cli.commands.cli_os import OpenStack
from functest.utils import openstack_utils as os_utils
from functest.utils.constants import CONST


class V1Creds(ApiResource):
    """ V1Creds Resource class"""

    def get(self):  # pylint: disable=no-self-use
        """ Get credentials """
        os_utils.source_credentials(CONST.__getattribute__('openstack_creds'))
        credentials_show = OpenStack.show_credentials()
        return jsonify(credentials_show)
