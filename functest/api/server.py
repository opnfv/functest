#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Used to launch Functest RestApi

"""

import logging
import socket
from urlparse import urljoin
import pkg_resources

from flask import Flask
from flask_restful import Api

from functest.api.base import ApiResource
from functest.api.urls import URLPATTERNS
from functest.api.common import api_utils


LOGGER = logging.getLogger(__name__)


def get_resource(resource_name):
    """ Obtain the required resource according to resource name """
    name = ''.join(resource_name.split('_'))
    return next((r for r in api_utils.itersubclasses(ApiResource)
                 if r.__name__.lower() == name))


def get_endpoint(url):
    """ Obtain the endpoint of url """
    address = socket.gethostbyname(socket.gethostname())
    return urljoin('http://{}:5000'.format(address), url)


def api_add_resource(api):
    """
    The resource has multiple URLs and you can pass multiple URLs to the
    add_resource() method on the Api object. Each one will be routed to
    your Resource
    """
    for url_pattern in URLPATTERNS:
        try:
            api.add_resource(
                get_resource(url_pattern.target), url_pattern.url,
                endpoint=get_endpoint(url_pattern.url))
        except StopIteration:
            LOGGER.error('url resource not found: %s', url_pattern.url)


def main():
    """Entry point"""
    logging.config.fileConfig(pkg_resources.resource_filename(
        'functest', 'ci/logging.ini'))
    LOGGER.info('Starting Functest server')
    app = Flask(__name__)
    api = Api(app)
    api_add_resource(api)
    app.run(host='0.0.0.0')
