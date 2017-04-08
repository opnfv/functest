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

from functest.opnfv_tests.features import domino
from functest.utils import constants


class DominoTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    _case_name = "domino-multinode"
    _project_name = "domino"

    def setUp(self):
        self.domino = domino.Domino(case_name=self._case_name,
                                    project_name=self._project_name)

    def test_init(self):
        self.assertEqual(self.domino.project_name, self._project_name)
        self.assertEqual(self.domino.case_name, self._case_name)
        self.assertEqual(
            self.domino.repo,
            constants.CONST.__getattribute__("dir_repo_domino"))
        self.assertEqual(
            self.domino.cmd,
            'cd {} && ./tests/run_multinode.sh'.format(self.domino.repo))


if __name__ == "__main__":
    unittest.main(verbosity=2)
