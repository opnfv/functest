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

from functest.opnfv_tests.features import sdnvpn
from functest.utils import constants


class SdnVpnTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.sdnvpn = sdnvpn.SdnVpnTests()

    def test_init(self):
        self.assertEqual(self.sdnvpn.project_name, "sdnvpn")
        self.assertEqual(self.sdnvpn.case_name, "bgpvpn")
        self.assertEqual(
            self.sdnvpn.repo,
            constants.CONST.__getattribute__("dir_repo_sdnvpn"))
        self.assertEqual(
            self.sdnvpn.cmd,
            'cd {}/sdnvpn/test/functest && python ./run_tests.py'.format(
                self.sdnvpn.repo))


if __name__ == "__main__":
    unittest.main(verbosity=2)
