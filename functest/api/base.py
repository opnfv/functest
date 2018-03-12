#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
The base class to dispatch request

"""

import logging

from flask import request
from flask_restful import Resource

from functest.api.common import api_utils


LOGGER = logging.getLogger(__name__)


class ApiResource(Resource):
    """ API Resource class"""

    def _post_args(self):  # pylint: disable=no-self-use
        # pylint: disable=maybe-no-member
        """ Return action and args after parsing request """

        data = request.json if request.json else {}
        params = api_utils.change_to_str_in_dict(data)
        action = params.get('action', request.form.get('action', ''))
        args = params.get('args', {})
        try:
            args['file'] = request.files['file']
        except KeyError:
            pass
        LOGGER.debug('Input args are: action: %s, args: %s', action, args)

        return action, args

    def _get_args(self):  # pylint: disable=no-self-use
        """ Convert the unicode to string for request.args """
        args = api_utils.change_to_str_in_dict(request.args)
        return args

    def _dispatch_post(self):
        """ Dispatch request """
        action, args = self._post_args()
        return self._dispatch(args, action)

    def _dispatch(self, args, action):
        """
        Dynamically load the classes with reflection and
        obtain corresponding methods
        """
        try:
            return getattr(self, action)(args)
        except AttributeError:
            api_utils.result_handler(status=1, data='No such action')


# Import modules from package "functest.api.resources"
# and append them into sys.modules
api_utils.import_modules_from_package("functest.api.resources")
