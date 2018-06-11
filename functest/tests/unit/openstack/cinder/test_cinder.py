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

from functest.opnfv_tests.openstack.cinder import cinder_test


class CinderTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('os_client_config.get_config') as mock_get_config, \
                mock.patch('shade.OpenStackCloud') as mock_shade:
            self.cinder = cinder_test.CinderCheck()
        self.assertTrue(mock_get_config.called)
        self.assertTrue(mock_shade.called)

    def test_clean_exc(self):
        self.cinder.cloud = None
        with self.assertRaises(Exception):
            self.cinder.clean()

    def test_clean_up_default(self):
        self.cinder.cloud.delete_floating_ip = mock.Mock(id='fip2')
        self.cinder.cloud.delete_volume = mock.Mock(id='volume')
        self.cinder.cloud.delete_server.assert_called_once_with(
            munch.Munch(), wait=True)
        self.cinder.clean()

if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
