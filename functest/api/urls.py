#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from functest.api import Url

urlpatterns = [
    Url('/api/v1/functest/envs', 'v1_envs'),
    Url('/api/v1/functest/envs/action', 'v1_envs'),
    Url('/api/v1/functest/openstack/credentials', 'v1_creds'),
    Url('/api/v1/functest/testcases', 'v1_test_cases'),
    Url('/api/v1/functest/testcases/<testcase_name>', 'v1_testcase'),
    Url('/api/v1/functest/tiers', 'v1_tiers'),
    Url('/api/v1/functest/tiers/<tier_name>', 'v1_tier'),
    Url('/api/v1/functest/tiers/<tier_name>/testcases', 'v1_testcases_in_tier')
]
