#!/usr/bin/python
#
# Copyright (c) 2017 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# 0.1: This script boots the VM1 and allocates IP address from Nova
# Later, the VM2 boots then execute cloud-init to ping VM1.
# After successful ping, both the VMs are deleted.
# 0.2: measure test duration and publish results under json format
#
#
import functest.core.feature as base
from functest.utils.constants import CONST


class Doctor(base.BashFeature):
    def __init__(self, **kwargs):
        repo = CONST.__getattribute__('dir_repo_doctor')
        kwargs["cmd"] = 'cd %s/tests && ./run.sh' % repo
        super(Doctor, self).__init__(**kwargs)
