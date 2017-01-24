#!/usr/bin/python
#
# Copyright 2016 AT&T Intellectual Property, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import functest.core.feature_base as base


class Copper(base.FeatureBase):
    def __init__(self):
        super(Copper, self).__init__(project='copper',
                                     case='copper-notification',
                                     repo='dir_repo_copper')
        self.cmd = 'cd %s/tests && bash run.sh && cd -' % self.repo
