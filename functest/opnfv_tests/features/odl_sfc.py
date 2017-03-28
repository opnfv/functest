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
from sfc.tests.functest import run_tests


class OpenDaylightSFC(base.Feature):

    def __init__(self):
        super(OpenDaylightSFC, self).__init__(project='sfc',
                                              case='functest-odl-sfc',
                                              repo='dir_repo_sfc')
        dir_sfc_functest = '{}/sfc/tests/functest'.format(self.repo)
        self.cmd = 'cd %s && python ./run_tests.py' % dir_sfc_functest
