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
from functest.utils.constants import CONST


class DoctorTesting(unittest.TestCase):

    logging.disable(logging.CRITICAL)

    _case_name = "doctor-notification"
    _project_name = "doctor"

    def setUp(self):
        self.doctor = doctor.Doctor(case_name=self._case_name,
                                    project_name=self._project_name)

    def test_init(self):
        self.assertEqual(self.doctor.project_name, self._project_name)
        self.assertEqual(self.doctor.case_name, self._case_name)
        repo = CONST.__getattribute__('dir_repo_doctor')
        self.assertEqual(
            self.doctor.cmd,
            'cd {}/tests && ./run.sh'.format(repo))


if __name__ == "__main__":
    unittest.main(verbosity=2)
