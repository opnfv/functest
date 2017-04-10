#!/usr/bin/python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

#
import functest.core.feature as base
from functest.utils.constants import CONST


class GluonVping(base.BashFeature):

    def __init__(self, **kwargs):
        repo = CONST.__getattribute__('dir_repo_netready')
        dir_netready_functest = '{}/test/functest'.format(repo)
        kwargs["cmd"] = ('cd %s && python ./gluon-test-suite.py' %
                         dir_netready_functest)
        super(GluonVping, self).__init__(**kwargs)
