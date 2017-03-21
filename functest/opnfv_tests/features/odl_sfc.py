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
from sfc.tests.functest import run_tests


class OpenDaylightSFC(base.FeatureBase):

    def __init__(self):
        super(OpenDaylightSFC, self).__init__(project='sfc',
                                              case='functest-odl-sfc"',
                                              repo='dir_repo_sfc')

    def execute(self):
        return run_tests.main(report=True)
