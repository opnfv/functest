#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import re


class RegexMatch(object):
    def __init__(self, msg):
        self.msg = msg

    def __eq__(self, other):
        match = re.search(self.msg, other)
        if match:
            return True
        return False


class SubstrMatch(object):
    def __init__(self, msg):
        self.msg = msg

    def __eq__(self, other):
        if self.msg in other:
            return True
        return False
