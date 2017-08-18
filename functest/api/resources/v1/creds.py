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

import collections
import logging

from flask import jsonify

from functest.api.base import ApiResource
from functest.api.common import api_utils
from functest.cli.commands.cli_os import OpenStack
from functest.utils import openstack_utils as os_utils
from functest.utils.constants import CONST

LOGGER = logging.getLogger(__name__)


class V1Creds(ApiResource):
    """ V1Creds Resource class"""

    def get(self):  # pylint: disable=no-self-use
        """ Get credentials """
        os_utils.source_credentials(CONST.__getattribute__('openstack_creds'))
        credentials_show = OpenStack.show_credentials()
        return jsonify(credentials_show)

    def post(self):
        """ Used to handle post request """
        return self._dispatch_post()

    def update_openrc(self, args):  # pylint: disable=no-self-use
        """ Used to update the OpenStack RC file """
        try:
            openrc_vars = args['openrc']
        except KeyError:
            return api_utils.result_handler(
                status=0, data='openrc must be provided')
        else:
            if not isinstance(openrc_vars, collections.Mapping):
                return api_utils.result_handler(
                    status=0, data='args should be a dict')

        lines = ['export {}={}\n'.format(k, v) for k, v in openrc_vars.items()]

        rc_file = CONST.__getattribute__('openstack_creds')
        with open(rc_file, 'w') as creds_file:
            creds_file.writelines(lines)

        LOGGER.info("Sourcing the OpenStack RC file...")
        try:
            os_utils.source_credentials(rc_file)
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.exception('Failed to source the OpenStack RC file')
            return api_utils.result_handler(status=0, data=str(err))

        return api_utils.result_handler(
            status=0, data='Update openrc successfully')
