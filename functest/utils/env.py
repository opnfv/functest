#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import os

import prettytable
from xtesting.utils import env

INPUTS = {
    'EXTERNAL_NETWORK': None,
    'CI_LOOP': env.INPUTS['CI_LOOP'],
    'DEPLOY_SCENARIO': env.INPUTS['DEPLOY_SCENARIO'],
    'INSTALLER_TYPE': env.INPUTS['INSTALLER_TYPE'],
    'SDN_CONTROLLER_IP': None,
    'BUILD_TAG': env.INPUTS['BUILD_TAG'],
    'NODE_NAME': env.INPUTS['NODE_NAME'],
    'POD_ARCH': None,
    'TEST_DB_URL': env.INPUTS['TEST_DB_URL'],
    'ENERGY_RECORDER_API_URL': env.INPUTS['ENERGY_RECORDER_API_URL'],
    'ENERGY_RECORDER_API_USER': env.INPUTS['ENERGY_RECORDER_API_USER'],
    'ENERGY_RECORDER_API_PASSWORD': env.INPUTS['ENERGY_RECORDER_API_PASSWORD'],
    'VOLUME_DEVICE_NAME': 'vdb',
    'NAMESERVER': '8.8.8.8',
    'NEW_USER_ROLE': 'Member'
}


def get(env_var):
    if env_var not in INPUTS.keys():
        return os.environ.get(env_var, None)
    return os.environ.get(env_var, INPUTS[env_var])


def string():
    msg = prettytable.PrettyTable(
        header_style='upper', padding_width=5,
        field_names=['env var', 'value'])
    for env_var in INPUTS:
        msg.add_row([env_var, get(env_var) if get(env_var) else ''])
    return msg
