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
from xtesting.core import testcase
from functest.opnfv_tests.openstack.cinder import cinder_test


class CinderTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('os_client_config.get_config') as mock_get_config, \
                mock.patch('shade.OpenStackCloud') as mock_shade:
            self.cinder = cinder_test.CinderCheck()
            self.cinder.floating_ip = munch.Munch(id='fip2')
            self.cinder.volume = munch.Munch(id='volume')
            self.cinder.server = munch.Munch()
        self.assertTrue(mock_get_config.called)
        self.assertTrue(mock_shade.called)


    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.CinderCheck.prepare')
    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.'
                'CinderCheck._write_data', return_value=testcase.TestCase.EX_OK)
    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.'
                'CinderCheck._read_data', return_value=testcase.TestCase.EX_OK)

    def test_cinder_execute(self):
        self.assertEquals(testcase.TestCase.EX_OK, self.cinder.execute())

    def test_clean_exc(self):
        self.cinder.cloud = None
        with self.assertRaises(Exception):
            self.cinder.clean()

    def test_clean_up_default(self):
        self.cinder.volume = mock.Mock(id='volume')
        self.cinder.floating_ip = mock.Mock(id='fip2')
        self.cinder.vm2 = mock.Mock()
        self.cinder.clean()

        self.cinder.cloud.delete_server.assert_called_once_with(
            munch.Munch(), wait=True)

        self.cinder.clean()

if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
