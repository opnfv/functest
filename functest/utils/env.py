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

INPUTS = {
    'EXTERNAL_NETWORK': None,
    'CI_LOOP': 'daily',
    'DEPLOY_SCENARIO': 'os-nosdn-nofeature-noha',
    'INSTALLER_TYPE': None,
    'SDN_CONTROLLER_IP': None,
    'BUILD_TAG': None,
    'NODE_NAME': None,
    'POD_ARCH': None,
    'TEST_DB_URL': 'http://testresults.opnfv.org/test/api/v1/results',
    'ENERGY_RECORDER_API_URL': 'http://energy.opnfv.fr/resources',
    'ENERGY_RECORDER_API_USER': '',
    'ENERGY_RECORDER_API_PASSWORD': ''
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
