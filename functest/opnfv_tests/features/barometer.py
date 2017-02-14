#!/usr/bin/python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0

import functest.core.feature_base as base


class Barometercollectd(base.FeatureBase):

    def __init__(self):
        super(Barometercollectd, self).__init__(project='barometer',
                                                case='barometercollectd',
                                                repo='dir_repo_barometer')
        self.cmd = ('cd %s && python ./tests/barometer_collectd.py' %
                    self.dir_promise_functest)
