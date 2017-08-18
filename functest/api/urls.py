#!/usr/bin/env python

# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""
Define multiple URLs
"""


class Url(object):  # pylint: disable=too-few-public-methods
    """ Url Class """

    def __init__(self, url, target):
        super(Url, self).__init__()
        self.url = url
        self.target = target


URLPATTERNS = [
    # GET /api/v1/functest/envs => GET environment
    Url('/api/v1/functest/envs', 'v1_envs'),

    # POST /api/v1/functest/envs/action , {"action":"prepare"}
    # => Prepare environment
    Url('/api/v1/functest/envs/action', 'v1_envs'),

    # GET /api/v1/functest/openstack/credentials => GET credentials
    Url('/api/v1/functest/openstack/credentials', 'v1_creds'),

    # POST /api/v1/functest/openstack/action
    # {"action":"update_openrc", "args": {"openrc": {}}} => Update openrc
    Url('/api/v1/functest/openstack/action', 'v1_creds'),

    # GET /api/v1/functest/testcases => GET all testcases
    Url('/api/v1/functest/testcases', 'v1_test_cases'),

    # GET /api/v1/functest/testcases/<testcase_name>
    # => GET the info of one testcase
    Url('/api/v1/functest/testcases/<testcase_name>', 'v1_testcase'),

    # GET /api/v1/functest/testcases => GET all tiers
    Url('/api/v1/functest/tiers', 'v1_tiers'),

    # GET /api/v1/functest/tiers/<tier_name>
    # => GET the info of one tier
    Url('/api/v1/functest/tiers/<tier_name>', 'v1_tier'),

    # GET /api/v1/functest/tiers/<tier_name>/testcases
    # => GET all testcases within given tier
    Url('/api/v1/functest/tiers/<tier_name>/testcases', 'v1_testcases_in_tier')
]
