#!/usr/bin/python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0


import functest.core.feature_base as base

from functest.utils.constants import CONST
from baro_tests import collectd


class BarometerCollectd(base.FeatureBase):
    '''
    Class for executing barometercollectd testcase.
    '''

    def __init__(self):
        super(BarometerCollectd, self).__init__(project='barometer',
                                                case='barometercollectd',
                                                repo='dir_repo_barometer')
        self.result_file = "{}/functest.log".format(CONST.dir_results)

    def execute(self):
        return collectd.main(self.logger)
