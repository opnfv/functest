#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

import functest.core.feature as base
from functest.utils.constants import CONST


class SecurityScan(base.FeatureBase):
    def __init__(self):
        super(SecurityScan, self).__init__(project='securityscanning',
                                           case='security_scan',
                                           repo='dir_repo_securityscan')
        self.cmd = ('. {0}/stackrc && '
                    'cd {1} && '
                    'python security_scan.py --config config.ini && '
                    'cd -'.format(CONST.dir_functest_conf,
                                  self.repo))
