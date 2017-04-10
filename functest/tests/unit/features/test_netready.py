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

from functest.opnfv_tests.features import netready
from functest.utils.constants import CONST


class NetreadyTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    _case_name = "gluon_vping"
    _project_name = "netready"

    def setUp(self):
        self.netready = netready.GluonVping(case_name=self._case_name,
                                            project_name=self._project_name)

    def test_init(self):
        self.assertEqual(self.netready.project_name, self._project_name)
        self.assertEqual(self.netready.case_name, self._case_name)
        repo = CONST.__getattribute__('dir_repo_netready')
        self.assertEqual(
            self.netready.cmd,
            'cd {}/test/functest && python ./gluon-test-suite.py'.format(repo))


if __name__ == "__main__":
    unittest.main(verbosity=2)
