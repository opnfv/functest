#!/usr/bin/env python
#
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

from functest.api import views
from functest.api.utils.common import Url

urlpatterns = [
    Url('/api/v1/functest/envs', views.Envs, 'envs'),
    # Url('/api/v1/functest/envs/action', views.EnvsAction, 'envs_action'),
    # Url('/api/v1/functest/openstack/credentials',
    #     views.OpenStackCredentials, 'openstack_credentials'),
    # Url('/api/v1/functest/openstack/action',
    #     views.OpenStackAction, 'openstack_action'),
    Url('/api/v1/functest/testcases', views.Testcases, 'testcases'),
    # Url('/api/v1/functest/testcases/<testcase_name>',
    #     views.TestcasesOne, 'testcases_one'),
    # Url('/api/v1/functest/testcases/<testcase_name>/action',
    #     views.TestcasesAction, 'testcases'),
    Url('/api/v1/functest/tiers', views.Tiers, 'tiers'),
    # Url('/api/v1/functest/tiers/<tier_name>',
    #     views.TiersOne, 'tiers_one'),
    # Url('/api/v1/functest/tiers/<tier_name>/testcases',
    #     views.TestcasesinOneTier, 'testcases_in_one_tier'),
    # Url('/api/v1/functest/tiers/<tier_name>/action',
    #     views.TiersAction, 'tiers_action'),
    # Url('/api/v1/functest/tasks/<task_id>',
    #     views.Tasks, 'tasks')
]
