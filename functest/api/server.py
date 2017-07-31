#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Used to launch Functest RestApi

"""

import inspect
import logging
import pkg_resources
import socket
from urlparse import urljoin

from flask import Flask
from flask_restful import Api

from functest.api.base import ApiResource
from functest.api.common import api_utils
from functest.api.database.db import Base
from functest.api.database.db import db_session
from functest.api.database.db import engine
from functest.api.database.v1 import models
from functest.api.urls import urlpatterns


LOGGER = logging.getLogger(__name__)

APP = Flask(__name__)
API = Api(APP)


@APP.teardown_request
def shutdown_session(exception=None):
    """
    To be called at the end of each request whether it is successful
    or an exception is raised
    """
    db_session.remove()


def get_resource(resource_name):
    """ Obtain the required resource according to resource name """
    name = ''.join(resource_name.split('_'))
    return next((r for r in api_utils.itersubclasses(ApiResource)
                 if r.__name__.lower() == name))


def get_endpoint(url):
    """ Obtain the endpoint of url """
    address = socket.gethostbyname(socket.gethostname())
    return urljoin('http://{}:5000'.format(address), url)


def api_add_resource():
    """
    The resource has multiple URLs and you can pass multiple URLs to the
    add_resource() method on the Api object. Each one will be routed to
    your Resource
    """
    for u in urlpatterns:
        try:
            API.add_resource(
                get_resource(u.target), u.url, endpoint=get_endpoint(u.url))
        except StopIteration:
            LOGGER.error('url resource not found: %s', u.url)


def init_db():
    def func(a):
        try:
            if issubclass(a[1], Base):
                return True
        except TypeError:
            pass
        return False

    subclses = filter(func, inspect.getmembers(models, inspect.isclass))
    LOGGER.debug('Import models: %s', [a[1] for a in subclses])
    Base.metadata.create_all(bind=engine)


def main():
    """Entry point"""
    logging.config.fileConfig(pkg_resources.resource_filename(
        'functest', 'ci/logging.ini'))
    LOGGER.info('Starting Functest server')
    api_add_resource()
    init_db()
    APP.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
