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
import shade

from functest.opnfv_tests.openstack.vmtp import vmtp


class VmtpInitTesting(unittest.TestCase):

    def _test_exc_init(self):
        testcase = vmtp.Vmtp()
        self.assertEqual(testcase.case_name, "vmtp")
        self.assertEqual(testcase.result, 0)
        for func in ['generate_keys', 'write_config', 'run_vmtp']:
            with self.assertRaises(AssertionError):
                getattr(testcase, func)()
        self.assertEqual(testcase.run(), testcase.EX_RUN_ERROR)
        self.assertEqual(testcase.clean(), None)

    @mock.patch('os_client_config.get_config', side_effect=Exception)
    def test_init1(self, *args):
        self._test_exc_init()
        args[0].assert_called_once_with()

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OpenStackCloud', side_effect=Exception)
    def test_init2(self, *args):
        self._test_exc_init()
        args[0].assert_called_once_with(cloud_config=mock.ANY)
        args[1].assert_called_once_with()

    @mock.patch('os_client_config.get_config')
    @mock.patch('shade.OpenStackCloud')
    def test_case_name(self, *args):
        testcase = vmtp.Vmtp(case_name="foo")
        self.assertEqual(testcase.case_name, "foo")
        args[0].assert_called_once_with(cloud_config=mock.ANY)
        args[1].assert_called_once_with()


class VmtpTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('os_client_config.get_config'), \
                mock.patch('shade.OpenStackCloud'):
            self.testcase = vmtp.Vmtp()
            self.testcase.cloud = mock.Mock()
        self.testcase.cloud.create_keypair.return_value = munch.Munch(
            private_key="priv", public_key="pub", id="id")

    @mock.patch('six.moves.builtins.open')
    def test_generate_keys1(self, *args):
        self.testcase.generate_keys()
        self.testcase.cloud.create_keypair.assert_called_once_with(
            'vmtp_{}'.format(self.testcase.guid))
        self.testcase.cloud.delete_keypair.assert_called_once_with('id')
        calls = [mock.call(self.testcase.privkey_filename, 'w'),
                 mock.call(self.testcase.pubkey_filename, 'w')]
        args[0].assert_has_calls(calls, any_order=True)

    @mock.patch('six.moves.builtins.open')
    def test_generate_keys2(self, *args):
        # pylint: disable=bad-continuation
        with mock.patch.object(
                self.testcase.cloud, "create_keypair",
                side_effect=shade.OpenStackCloudException(None)) as mock_obj, \
                self.assertRaises(shade.OpenStackCloudException):
            self.testcase.generate_keys()
        mock_obj.assert_called_once_with('vmtp_{}'.format(self.testcase.guid))
        args[0].assert_not_called()

if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
