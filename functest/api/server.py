#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import socket

from flask import Flask
from flask_restful import Api

from functest.api.base import ApiResource
from functest.api.urls import urlpatterns
from functest.api.utils import api_utils
from functest.utils.constants import CONST

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)


def get_resource(resource_name):
    name = ''.join(resource_name.split('_'))
    return next((r for r in api_utils.itersubclasses(ApiResource)
                 if r.__name__.lower() == name))


def get_endpoint(url):
    ip = socket.gethostbyname(socket.gethostname())
    return urljoin(
        'http://{}:{}'.format(ip, CONST.__getattribute__('api_port')), url)


for u in urlpatterns:
    try:
        api.add_resource(
            get_resource(u.target), u.url, endpoint=get_endpoint(u.url))
    except StopIteration:
        logger.error('url resource not found: %s', u.url)


if __name__ == '__main__':
    logging.basicConfig()
    logger.info('Starting Functest server')
    app.run(host='0.0.0.0')
