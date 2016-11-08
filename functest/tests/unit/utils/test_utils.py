#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import mock
import unittest

from functest.utils import functest_utils


class FunctestUtilsTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.test = functest_utils

    def test_check_internet_connectivity(self):
        self.assertTrue(self.test.check_internet_connectivity())
# TODO
# ...        

if __name__ == "__main__":
    unittest.main(verbosity=2)
