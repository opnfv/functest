#!/usr/bin/python
#
# Copyright (c) 2016 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
import functest.core.feature as base
from functest.utils.constants import CONST


class OpenDaylightSFC(base.BashFeature):

    def __init__(self, **kwargs):
        repo = CONST.__getattribute__('dir_repo_sfc')
        dir_sfc_functest = '{}/sfc/tests/functest'.format(repo)
        kwargs["cmd"] = 'cd %s && python ./run_tests.py' % dir_sfc_functest
        super(OpenDaylightSFC, self).__init__(**kwargs)
