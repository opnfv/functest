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

from functest.opnfv_tests.features import security_scan
from functest.utils import constants


class SecurityScanTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    _case_name = "security_scan"
    _project_name = "security_scan"

    def setUp(self):
        self.sscan = security_scan.SecurityScan(
            case_name=self._case_name, project_name=self._project_name)

    def test_init(self):
        self.assertEqual(self.sscan.project_name, self._project_name)
        self.assertEqual(self.sscan.case_name, self._case_name)
        self.assertEqual(
            self.sscan.repo,
            constants.CONST.__getattribute__("dir_repo_securityscan"))
        self.assertEqual(
            self.sscan.cmd, (
                '. {0}/stackrc && cd {1} && '
                'python security_scan.py --config config.ini && '
                'cd -'.format(
                    constants.CONST.__getattribute__("dir_functest_conf"),
                    self.sscan.repo)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
