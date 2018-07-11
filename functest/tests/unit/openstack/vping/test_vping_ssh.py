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

from paramiko import ssh_exception
import mock
import munch
import shade

from functest.opnfv_tests.openstack.vping import vping_ssh
from functest.utils import config


class VpingSSHTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('functest.core.singlevm.SingleVm2.__init__'):
            self.vping = vping_ssh.VPingSSH()
            self.vping.cloud = mock.Mock()
            self.vping.case_name = 'vping'
            self.vping.guid = '1'

    @mock.patch('functest.core.singlevm.SingleVm2.prepare',
                side_effect=Exception)
    def test_prepare_exc1(self, *args):
        with self.assertRaises(Exception):
            self.vping.prepare()
        args[0].assert_called_once_with()

    @mock.patch('functest.opnfv_tests.openstack.vping.vping_ssh.VPingSSH.'
                'boot_vm',
                side_effect=Exception)
    @mock.patch('functest.core.singlevm.SingleVm2.prepare')
    def test_prepare_exc2(self, *args):
        self.vping.sec = munch.Munch(id='foo')
        with self.assertRaises(Exception):
            self.vping.prepare()
        args[0].assert_called_once_with()
        args[1].assert_called_once_with(
            '{}-vm2_{}'.format(self.vping.case_name, self.vping.guid),
            security_groups=[self.vping.sec.id])

    @mock.patch('functest.opnfv_tests.openstack.vping.vping_ssh.VPingSSH.'
                'boot_vm')
    @mock.patch('functest.core.singlevm.SingleVm2.prepare')
    def test_prepare(self, *args):
        self.vping.sec = munch.Munch(id='foo')
        self.vping.prepare()
        args[0].assert_called_once_with()
        args[1].assert_called_once_with(
            '{}-vm2_{}'.format(self.vping.case_name, self.vping.guid),
            security_groups=[self.vping.sec.id])

    def test_execute_exc(self):
        self.vping.vm2 = munch.Munch(private_v4='127.0.0.1')
        self.vping.ssh = mock.Mock()
        self.vping.ssh.exec_command.side_effect = ssh_exception.SSHException
        with self.assertRaises(ssh_exception.SSHException):
            self.vping.execute()
        self.vping.ssh.exec_command.assert_called_once_with(
            'ping -c 1 {}'.format(self.vping.vm2.private_v4))

    def _test_execute(self, ret=0):
        self.vping.vm2 = munch.Munch(private_v4='127.0.0.1')
        self.vping.ssh = mock.Mock()
        stdout = mock.Mock()
        stdout.channel.recv_exit_status.return_value = ret
        self.vping.ssh.exec_command.return_value = (None, stdout, None)
        self.assertEqual(self.vping.execute(), ret)
        self.vping.ssh.exec_command.assert_called_once_with(
            'ping -c 1 {}'.format(self.vping.vm2.private_v4))

    def test_execute1(self):
        self._test_execute()

    def test_execute2(self):
        self._test_execute(1)

    def test_clean_exc1(self):
        self.vping.cloud = None
        with self.assertRaises(AssertionError):
            self.vping.clean()

    def test_clean_exc2(self):
        self.vping.vm2 = munch.Munch(id='vm2')
        mdelete_server = self.vping.cloud.delete_server
        mdelete_server.side_effect = shade.OpenStackCloudException(None)
        with self.assertRaises(shade.OpenStackCloudException):
            self.vping.clean()

    @mock.patch('functest.core.singlevm.SingleVm2.clean',
                side_effect=Exception)
    def test_clean_exc3(self, *args):
        self.vping.vm2 = munch.Munch(id='vm2')
        with self.assertRaises(Exception):
            self.vping.clean()
        self.vping.cloud.delete_server.assert_called_once_with(
            self.vping.vm2, wait=True,
            timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        args[0].assert_called_once_with()

    @mock.patch('functest.core.singlevm.SingleVm2.clean')
    def test_clean1(self, *args):
        self.vping.vm2 = None
        self.vping.clean()
        self.vping.cloud.delete_server.assert_not_called()
        args[0].assert_called_once_with()

    @mock.patch('functest.core.singlevm.SingleVm2.clean')
    def test_clean2(self, *args):
        self.vping.vm2 = munch.Munch(id='vm2')
        self.vping.clean()
        self.vping.cloud.delete_server.assert_called_once_with(
            self.vping.vm2, wait=True,
            timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        args[0].assert_called_once_with()


if __name__ == '__main__':
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
