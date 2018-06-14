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

import inspect
import logging
import socket
import pkg_resources

from flask import Flask
from flask_restful import Api
from flasgger import Swagger
import six

from functest.api.base import ApiResource
from functest.api.common import api_utils
from functest.api.database.db import BASE
from functest.api.database.db import DB_SESSION
from functest.api.database.db import ENGINE
from functest.api.database.v1 import models
from functest.api.urls import URLPATTERNS


LOGGER = logging.getLogger(__name__)

APP = Flask(__name__)
API = Api(APP)
Swagger(APP)


@APP.teardown_request
def shutdown_session(exception=None):  # pylint: disable=unused-argument
    """
    To be called at the end of each request whether it is successful
    or an exception is raised
    """
    DB_SESSION.remove()


def get_resource(resource_name):
    """ Obtain the required resource according to resource name """
    name = ''.join(resource_name.split('_'))
    return next((r for r in api_utils.itersubclasses(ApiResource)
                 if r.__name__.lower() == name))


def get_endpoint(url):
    """ Obtain the endpoint of url """
    address = socket.gethostbyname(socket.gethostname())
    return six.moves.urllib.parse.urljoin(
        'http://{}:5000'.format(address), url)


def api_add_resource():
    """
    The resource has multiple URLs and you can pass multiple URLs to the
    add_resource() method on the Api object. Each one will be routed to
    your Resource
    """
    for url_pattern in URLPATTERNS:
        try:
            API.add_resource(
                get_resource(url_pattern.target), url_pattern.url,
                endpoint=get_endpoint(url_pattern.url))
        except StopIteration:
            LOGGER.error('url resource not found: %s', url_pattern.url)


def init_db():
    """
    Import all modules here that might define models so that
    they will be registered properly on the metadata, and then
    create a database
    """
    def func(subcls):
        """ To check the subclasses of BASE"""
        try:
            if issubclass(subcls[1], BASE):
                return True
        except TypeError:
            pass
        return False
    # pylint: disable=bad-option-value,bad-builtin,
    subclses = filter(func, inspect.getmembers(models, inspect.isclass))
    LOGGER.debug('Import models: %s', [subcls[1] for subcls in subclses])
    BASE.metadata.create_all(bind=ENGINE)


def main():
    """Entry point"""
    logging.config.fileConfig(pkg_resources.resource_filename(
        'functest', 'ci/logging.ini'))
    logging.captureWarnings(True)
    LOGGER.info('Starting Functest server')
    api_add_resource()
    init_db()
    APP.run(host='0.0.0.0')
