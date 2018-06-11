#!/usr/bin/env python

# Copyright (c) 2018 Enea AB and others.
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

from functest.opnfv_tests.openstack.cinder import cinder_base


class CinderTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('os_client_config.make_shade'):
            self.cinder = cinder_base.CinderBase()

    def test_clean_exc(self):
        self.cinder.cloud = None
        with self.assertRaises(Exception):
            self.cinder.clean()

    def test_clean(self):
        self.cinder.image = munch.Munch()
        self.cinder.router = munch.Munch()
        self.cinder.subnet = munch.Munch(id='subnet')
        self.cinder.router = munch.Munch(id='router')
        self.cinder.network = munch.Munch(id='network')
        self.cinder.flavor = munch.Munch(id='flavor')
        self.cinder.volume = munch.Munch(id='volume')
        self.cinder.clean()

if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
