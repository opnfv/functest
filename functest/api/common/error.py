#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Used to handle results

"""

from flask import jsonify


def result_handler(status, data):
    """ Return the json format of result in dict """
    result = {
        'status': status,
        'result': data
    }
    return jsonify(result)
