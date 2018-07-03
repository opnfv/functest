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
from xtesting.core import testcase
from functest.opnfv_tests.openstack.cinder import cinder_test


class CinderTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('os_client_config.get_config') as mock_get_config, \
                mock.patch('shade.OpenStackCloud') as mock_shade:
            self.cinder = cinder_test.CinderCheck()
        self.assertTrue(mock_get_config.called)
        self.assertTrue(mock_shade.called)

    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.'
                'CinderCheck._write_data',
                return_value=testcase.TestCase.EX_OK)
    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.'
                'CinderCheck._read_data',
                return_value=testcase.TestCase.EX_OK)
    def test_cinder_execute(self, *args):
        self.assertEquals(self.cinder.execute(), testcase.TestCase.EX_OK)
        for func in args:
            func.assert_called()

    def test_clean_exc(self):
        self.cinder.cloud = None
        with self.assertRaises(Exception):
            self.cinder.clean()

    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.'
                'CinderCheck.clean')
    def test_clean_up_default(self, mock_cinder_clean):
        self.cinder.vm2 = mock.Mock()
        self.cinder.volume = mock.Mock(id='fip2')
        self.cinder.fip2 = mock.Mock(id='volume')
        self.cinder.clean()
        mock_cinder_clean.assert_called_once()

if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
