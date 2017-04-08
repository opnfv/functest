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


class SdnVpnTests(base.Feature):

    def __init__(self, **kwargs):
        kwargs["repo"] = 'dir_repo_sdnvpn'
        super(SdnVpnTests, self).__init__(**kwargs)
        dir_sfc_functest = '{}/sdnvpn/test/functest'.format(self.repo)
        self.cmd = 'cd %s && python ./run_tests.py' % dir_sfc_functest
