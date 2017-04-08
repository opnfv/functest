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

from functest.opnfv_tests.vnf.rnc import parser
from functest.utils import constants


class ParserTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    _case_name = "parser-basics"
    _project_name = "parser"

    def setUp(self):
        self.parser = parser.Parser(
            case_name=self._case_name, project_name=self._project_name)

    def test_init(self):
        self.assertEqual(self.parser.project_name, self._project_name)
        self.assertEqual(self.parser.case_name, self._case_name)
        self.assertEqual(
            self.parser.repo,
            constants.CONST.__getattribute__("dir_repo_parser"))
        self.assertEqual(
            self.parser.cmd,
            'cd {}/tests && ./functest_run.sh'.format(self.parser.repo))


if __name__ == "__main__":
    unittest.main(verbosity=2)
