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
import socket

from flask import jsonify
from flasgger.utils import swag_from
import pkg_resources

from functest.api.base import ApiResource
from functest.api.common import api_utils
from functest.ci import run_tests
from functest.cli.commands.cli_os import OpenStack
from functest.utils import constants

LOGGER = logging.getLogger(__name__)

ADDRESS = socket.gethostbyname(socket.gethostname())
ENDPOINT_CREDS = ('http://{}:5000/api/v1/functest/openstack'.format(ADDRESS))


class V1Creds(ApiResource):
    """ V1Creds Resource class"""

    @swag_from(
        pkg_resources.resource_filename('functest', 'api/swagger/creds.yaml'),
        endpoint='{0}/credentials'.format(ENDPOINT_CREDS))
    def get(self):  # pylint: disable=no-self-use
        """ Get credentials """
        run_tests.Runner.source_envfile(constants.ENV_FILE)
        credentials_show = OpenStack.show_credentials()
        return jsonify(credentials_show)

    @swag_from(
        pkg_resources.resource_filename('functest',
                                        'api/swagger/creds_action.yaml'),
        endpoint='{0}/action'.format(ENDPOINT_CREDS))
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

        rc_file = constants.ENV_FILE
        with open(rc_file, 'w') as creds_file:
            creds_file.writelines(lines)

        LOGGER.info("Sourcing the OpenStack RC file...")
        try:
            run_tests.Runner.source_envfile(rc_file)
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.exception('Failed to source the OpenStack RC file')
            return api_utils.result_handler(status=0, data=str(err))

        return api_utils.result_handler(
            status=0, data='Update openrc successfully')
