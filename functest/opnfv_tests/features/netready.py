#!/usr/bin/python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

#
import functest.core.feature_base as base


class GluonVping(base.FeatureBase):

    def __init__(self):
        super(GluonVping, self).__init__(project='netready',
                                         case='gluon_vping',
                                         repo='dir_repo_netready')
        dir_netready_functest = '{}/netready/test/functest'.format(self.repo)
        self.cmd = 'cd %s && python ./somescript.py' % dir_netready_functest
