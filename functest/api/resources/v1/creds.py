#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Resources to handle openstack related requests
"""

import os

from flask import jsonify

from functest.api.actions.api_os import ApiOpenStack
from functest.api.base import ApiResource
from functest.api.common import error
from functest.utils import openstack_utils as os_utils
from functest.utils.constants import CONST


class V1Creds(ApiResource):
    """ V1Creds Resource class"""

    def get(self):
        """ Get credentials """
        rc_file = CONST.__getattribute__('openstack_creds')
        if not os.path.isfile(rc_file):
            return error.notFoundError(
                "RC file %s does not exist..." % rc_file)
        os_utils.source_credentials(CONST.__getattribute__('openstack_creds'))
        credentials_show = ApiOpenStack.show_credentials()
        return jsonify(credentials_show)
