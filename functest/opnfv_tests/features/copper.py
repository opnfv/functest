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
import functest.core.feature as base
from functest.utils.constants import CONST


class Copper(base.BashFeature):
    def __init__(self, **kwargs):
        repo = CONST.__getattribute__('dir_repo_copper')
        kwargs["cmd"] = 'cd %s/tests && bash run.sh && cd -' % repo
        super(Copper, self).__init__(**kwargs)
