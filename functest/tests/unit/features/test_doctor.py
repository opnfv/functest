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

from functest.opnfv_tests.features import doctor
from functest.utils import constants


class DoctorTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    def setUp(self):
        self.doctor = doctor.Doctor()

    def test_init(self):
        self.assertEqual(self.doctor.project_name, "doctor")
        self.assertEqual(self.doctor.case_name, "doctor-notification")
        self.assertEqual(
            self.doctor.repo,
            constants.CONST.__getattribute__("dir_repo_doctor"))
        self.assertEqual(
            self.doctor.cmd,
            'cd {}/tests && ./run.sh'.format(self.doctor.repo))


if __name__ == "__main__":
    unittest.main(verbosity=2)
