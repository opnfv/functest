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

from paramiko import ssh_exception
import mock
import munch
import shade

from xtesting.core import testcase
from functest.opnfv_tests.openstack.cinder import cinder_test
from functest.utils import config


class CinderTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('functest.core.singlevm.SingleVm2.__init__'):
            self.cinder = cinder_test.CinderCheck()
            self.cinder.cloud = mock.Mock()
            self.cinder.case_name = 'cinder'
            self.cinder.guid = '1'


    @mock.patch('functest.core.singlevm.SingleVm2.prepare',
                side_effect=Exception)
    def test_prepare_exc1(self, *args):
        with self.assertRaises(Exception):
            self.cinder.prepare()
        args[0].assert_called_once_with()


    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.CinderCheck.'
                'boot_vm',
                side_effect=Exception)
    @mock.patch('functest.core.singlevm.SingleVm2.prepare')
    def test_prepare_exc2(self, *args):
        self.cinder.sec = munch.Munch(id='foo')
        self.cinder.keypair = munch.Munch(id='foo')
        self.cinder.volume_timeout = munch.Munch(id='foo')
        with self.assertRaises(Exception):
            self.cinder.prepare()
        args[0].assert_called_with()
        args[1].assert_called_once_with(
            '{}-vm2_{}'.format(self.cinder.case_name, self.cinder.guid),
            security_groups=[self.cinder.sec.id],
            key_name=self.cinder.keypair.id)

    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.CinderCheck.'
                'boot_vm')
    @mock.patch('functest.core.singlevm.SingleVm2.prepare')
    def test_prepare(self, *args):
        self.cinder.sec = munch.Munch(id='foo')
        self.cinder.keypair = munch.Munch(id='foo')
        self.cinder.ext_net = mock.Mock(id='foo')
        self.cinder.vm2 = munch.Munch(id='vm2')
        self.cinder.ssh2 = munch.Munch(id='foo')
        self.cinder.fip2 = munch.Munch(id='fip')
        with mock.patch.object(self.cinder, 'connect',
                               return_value=(self.cinder.fip2, self.cinder.ssh2)), \
             mock.patch.object(self.cinder.cloud, 'create_volume',
                               return_value=True):
            self.cinder.prepare()
        args[0].assert_called_once_with()
        args[1].assert_called_once_with(
            '{}-vm2_{}'.format(self.cinder.case_name, self.cinder.guid),
            security_groups=[self.cinder.sec.id],
            key_name=self.cinder.keypair.id)


    def test_execute_write(self):
        self.cinder.ssh = mock.Mock()
        self.cinder.sshvm = mock.Mock(id='sshvm')
        self.cinder.volume = mock.Mock(id='volume')
        self.cinder.vm2 = mock.Mock(id='vm2')
        with mock.patch.object(self.cinder, '_read_data', return_value=False), \
                mock.patch.object(self.cinder.cloud, 'attach_volume',
                                  return_value=True), \
                mock.patch.object(self.cinder.ssh, 'exec_command',
                                  return_value=True), \
                mock.patch.object(self.cinder.cloud, 'detach_volume',
                                  return_values=True):
            self.cinder.execute()

    def test_execute_write_exc1(self):
        self.cinder.ssh = mock.Mock()
        with mock.patch.object(self.cinder, '_read_data', return_value=False), \
                mock.patch.object(self.cinder.cloud, 'attach_volume',
                                  side_effect=Exception), \
                mock.patch.object(self.cinder.ssh, 'execute_command',
                                  return_value=ssh_exception), \
                mock.patch.object(self.cinder.cloud, 'detach_volume',
                                  side_effect=Exception):
            with self.assertRaises(Exception):
                self.assertEqual(self.cinder.execute(),
                                 testcase.TestCase.EX_RUN_ERROR)

    def test_execute_read(self):
        self.cinder.ssh2 = mock.Mock()
        self.cinder.volume = mock.Mock(id='volume')
        self.cinder.vm2 = mock.Mock(id='vm2')
        with mock.patch.object(self.cinder, '_write_data', return_value=False), \
                mock.patch.object(self.cinder.cloud, 'attach_volume',
                                  return_value=True), \
                mock.patch.object(self.cinder.ssh2, 'execute_command',
                                  return_value=True), \
                mock.patch.object(self.cinder.cloud, 'detach_volume',
                                  return_values=True):
            self.cinder.execute()


    def test_execute_read_exc1(self):
        self.cinder.ssh = mock.Mock()
        with mock.patch.object(self.cinder, '_write_data', return_value=False), \
             mock.patch.object(self.cinder.cloud, 'attach_volume',
                               side_effect=Exception), \
             mock.patch.object(self.cinder.ssh, 'execute_command',
                               return_value=ssh_exception), \
             mock.patch.object(self.cinder.cloud, 'detach_volume',
                               side_effect=Exception):
            with self.assertRaises(Exception):
                self.assertEqual(self.cinder.execute(),
                                 testcase.TestCase.EX_RUN_ERROR)


    def test_clean_exc1(self):
        self.cinder.cloud = None
        with self.assertRaises(AssertionError):
            self.cinder.clean()

    def test_clean_exc2(self):
        mdelete_server = self.cinder.cloud.delete_server
        mdelete_volume = self.cinder.cloud.delete_volume
        mdelete_floating_ip = self.cinder.cloud.delete_floating_ip
        mdelete_server.side_effect = shade.OpenStackCloudException(None)
        mdelete_volume.side_effect = shade.OpenStackCloudException(None)
        mdelete_floating_ip.side_effect = shade.OpenStackCloudException(None)
        with self.assertRaises(shade.OpenStackCloudException):
            self.cinder.clean()

    @mock.patch('functest.core.singlevm.SingleVm2.clean',
                side_effect=Exception)
    def test_clean_exc3(self, mock_clean):
        self.cinder.vm2 = munch.Munch()
        self.cinder.volume = munch.Munch
        self.cinder.fip2 = munch.Munch
        with self.assertRaises(Exception):
            self.cinder.clean()
        self.cinder.cloud.delete_server.assert_called_once_with(
            self.cinder.vm2, wait=True,
            timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        mock_clean.prepare()

    @mock.patch('functest.core.singlevm.SingleVm2.clean')
    def test_clean(self, *args):
        self.cinder.vm2 = munch.Munch()
        self.cinder.volume = munch.Munch(id='volume')
        self.cinder.fip2 = munch.Munch(id='fip2')
        self.cinder.clean()
        self.cinder.cloud.delete_server.assert_called_once_with(
            self.cinder.vm2, wait=True,
            timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        args[0].assert_called_once_with()


if __name__ == '__main__':
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
