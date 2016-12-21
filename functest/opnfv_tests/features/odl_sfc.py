#!/usr/bin/python
#
# Copyright (c) 2016 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

import functest.core.feature_base as base
from functest.utils.constants import CONST


class OpenDaylightSFC(base.FeatureBase):

    def __init__(self):
        super(OpenDaylightSFC, self).__init__(project='sfc',
                                              case='functest-odl-sfc"',
                                              repo=CONST.dir_repo_sfc)
        self.cmd = 'cd %s/tests/functest && python ./run_tests.py' % self.repo
