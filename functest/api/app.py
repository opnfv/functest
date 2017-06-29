#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging

from flask import Flask
from flask_restful import Api

from functest.api.urls import urlpatterns

logger = logging.getLogger(__name__)

app = Flask(__name__)

api = Api(app)

for u in urlpatterns:
    api.add_resource(u.resource, u.url, endpoint=u.endpoint)

if __name__ == '__main__':
    logging.basicConfig()
    logger.info('Starting Functest server')
    app.run(host='0.0.0.0')
