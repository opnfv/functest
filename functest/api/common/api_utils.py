#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Utils for functest restapi

"""

import collections
import logging
import os
import sys
from oslo_utils import importutils

from flask import jsonify
import six

import functest

LOGGER = logging.getLogger(__name__)


def change_to_str_in_dict(obj):
    """
    Return a dict with key and value both in string if they are in Unicode
    """
    if isinstance(obj, collections.Mapping):
        return {str(k): change_to_str_in_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [change_to_str_in_dict(ele) for ele in obj]
    elif isinstance(obj, six.text_type):
        return str(obj)
    return obj


def itersubclasses(cls, _seen=None):
    """ Generator over all subclasses of a given class in depth first order """

    if not isinstance(cls, type):
        raise TypeError("itersubclasses must be called with "
                        "new-style classes, not %.100r" % cls)
    _seen = _seen or set()
    try:
        subs = cls.__subclasses__()
    except TypeError:   # fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for itersub in itersubclasses(sub, _seen):
                yield itersub


def import_modules_from_package(package):
    """
    Import modules from package and append into sys.modules
    :param: package - Full package name. For example: functest.api.resources
    """
    path = [os.path.dirname(functest.__file__), ".."] + package.split(".")
    path = os.path.join(*path)
    for root, _, files in os.walk(path):
        for filename in files:
            if filename.startswith("__") or not filename.endswith(".py"):
                continue
            new_package = ".".join(root.split(os.sep)).split("....")[1]
            module_name = "%s.%s" % (new_package, filename[:-3])
            try:
                try_append_module(module_name, sys.modules)
            except ImportError:
                LOGGER.exception("unable to import %s", module_name)


def try_append_module(name, modules):
    """ Append the module into specified module system """

    if name not in modules:
        modules[name] = importutils.import_module(name)


def change_obj_to_dict(obj):
    """  Transfer the object into dict """
    dic = {}
    for key, value in vars(obj).items():
        dic.update({key: value})
    return dic


def result_handler(status, data):
    """ Return the json format of result in dict """
    result = {
        'status': status,
        'result': data
    }
    return jsonify(result)
