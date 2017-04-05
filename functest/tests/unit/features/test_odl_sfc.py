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

from functest.opnfv_tests.features import odl_sfc
from functest.utils import constants


class OpenDaylightSFCTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.odl_sfc = odl_sfc.OpenDaylightSFC(case_name="functest-odl-sfc")

    def test_init(self):
        self.assertEqual(self.odl_sfc.project_name, "sfc")
        self.assertEqual(self.odl_sfc.case_name, "functest-odl-sfc")
        self.assertEqual(
            self.odl_sfc.repo,
            constants.CONST.__getattribute__("dir_repo_sfc"))
        dir_sfc_functest = '{}/sfc/tests/functest'.format(self.odl_sfc.repo)
        self.assertEqual(
            self.odl_sfc.cmd,
            'cd {} && python ./run_tests.py'.format(dir_sfc_functest))


if __name__ == "__main__":
    unittest.main(verbosity=2)
