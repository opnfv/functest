#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

from functest.opnfv_tests.features import copper
from functest.utils import constants


class CopperTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.copper = copper.Copper(case_name="copper-notification")

    def test_init(self):
        self.assertEqual(self.copper.project_name, "copper")
        self.assertEqual(self.copper.case_name, "copper-notification")
        self.assertEqual(
            self.copper.repo,
            constants.CONST.__getattribute__("dir_repo_copper"))
        self.assertEqual(
            self.copper.cmd,
            "cd {}/tests && bash run.sh && cd -".format(self.copper.repo))


if __name__ == "__main__":
    unittest.main(verbosity=2)
