#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock
import munch

from functest.opnfv_tests.openstack.vping import vping_base

class VpingBaseTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('os_client_config.make_shade'):
            self.vping = vping_base.VPingBase()

    def test_clean_exc(self):
        self.vping.cloud = None
        with self.assertRaises(Exception):
            self.vping.clean()

    def test_clean(self):
        self.vping.vm1 = munch.Munch()
        self.vping.sec1 = munch.Munch(id='sec1')
        self.vping.image = munch.Munch()
        self.vping.router = munch.Munch()
        self.vping.subnet = munch.Munch(id='subnet')
        self.vping.router = munch.Munch(id='router')
        self.vping.network = munch.Munch(id='network')
        self.vping.flavor = munch.Munch(id='flavor')
        self.vping.clean()
        self.vping.cloud.delete_server.assert_called_once_with(
            munch.Munch(), wait=True)

if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
