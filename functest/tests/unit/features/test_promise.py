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

from functest.opnfv_tests.features import promise
from functest.utils import constants


class PromiseTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.promise = promise.Promise(case_name="promise")

    def test_init(self):
        self.assertEqual(self.promise.project_name, "promise")
        self.assertEqual(self.promise.case_name, "promise")
        self.assertEqual(
            self.promise.repo,
            constants.CONST.__getattribute__("dir_repo_promise"))
        self.assertEqual(
            self.promise.cmd,
            'cd {}/promise/test/functest && python ./run_tests.py'.format(
                self.promise.repo))


if __name__ == "__main__":
    unittest.main(verbosity=2)
