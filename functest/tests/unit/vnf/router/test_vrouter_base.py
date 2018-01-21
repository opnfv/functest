#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock

from functest.opnfv_tests.vnf.router import vrouter_base


class VrouterOnBoardingBaseTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('functest.opnfv_tests.vnf.router.cloudify_vrouter.'
                        'os.makedirs'):
            self.vrouter_vnf = vrouter_base.VrouterOnBoardingBase()


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
