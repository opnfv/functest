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

import pkg_resources
import mock
import munch
import shade

from functest.opnfv_tests.openstack.cinder import cinder_test
from functest.utils import config
from functest.utils import env


class CinderTesting(unittest.TestCase):

    def setUp(self):
        with mock.patch('functest.core.singlevm.SingleVm2.__init__'):
            self.cinder = cinder_test.CinderCheck()
            self.cinder.cloud = mock.Mock()
            self.cinder.case_name = 'cinder'
            self.cinder.guid = '1'

    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.'
                'CinderCheck.connect')
    @mock.patch('functest.core.singlevm.SingleVm2.prepare',
                side_effect=Exception)
    def test_prepare_exc1(self, *args):
        self.cinder.cloud.boot_vm = mock.Mock()
        with self.assertRaises(Exception):
            self.cinder.prepare()
        args[0].assert_called_once_with()
        args[1].assert_not_called()
        self.cinder.cloud.boot_vm.assert_not_called()
        self.cinder.cloud.create_volume.assert_not_called()

    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.'
                'CinderCheck.connect')
    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.'
                'CinderCheck.boot_vm',
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
        self.cinder.cloud.create_volume.assert_not_called()
        args[2].assert_not_called()

    @mock.patch('functest.opnfv_tests.openstack.cinder.cinder_test.'
                'CinderCheck.boot_vm', return_value=munch.Munch(id='vm2'))
    @mock.patch('functest.core.singlevm.SingleVm2.prepare')
    def test_prepare(self, *args):
        self.cinder.sec = munch.Munch(id='foo')
        self.cinder.keypair = munch.Munch(id='foo')
        self.cinder.ext_net = mock.Mock(id='foo')
        self.cinder.ssh2 = mock.Mock()
        self.cinder.fip2 = munch.Munch(id='fip2')
        self.cinder.connect = mock.Mock(
            return_value=(self.cinder.fip2, self.cinder.ssh2))
        self.cinder.cloud.create_volume = mock.Mock(
            return_value=munch.Munch())
        self.cinder.prepare()
        args[0].assert_called_once_with()
        args[1].assert_called_once_with(
            '{}-vm2_{}'.format(self.cinder.case_name, self.cinder.guid),
            security_groups=[self.cinder.sec.id],
            key_name=self.cinder.keypair.id)
        self.cinder.connect.assert_called_once_with(args[1].return_value)
        self.cinder.cloud.create_volume.assert_called_once_with(
            name='{}-volume_{}'.format(
                self.cinder.case_name, self.cinder.guid),
            size='2', timeout=self.cinder.volume_timeout)

    @mock.patch('scp.SCPClient.put')
    def test_write(self, *args):
        # pylint: disable=protected-access
        self.cinder.ssh = mock.Mock()
        self.cinder.sshvm = mock.Mock(id='foo')
        self.cinder.volume = mock.Mock(id='volume')
        stdout = mock.Mock()
        stdout.channel.recv_exit_status.return_value = 0
        self.cinder.ssh.exec_command.return_value = (None, stdout, mock.Mock())
        self.assertEqual(self.cinder._write_data(), 0)
        self.cinder.ssh.exec_command.assert_called_once_with(
            "sh ~/write_data.sh {}".format(env.get('VOLUME_DEVICE_NAME')))
        self.cinder.cloud.attach_volume.assert_called_once_with(
            self.cinder.sshvm, self.cinder.volume,
            timeout=self.cinder.volume_timeout)
        self.cinder.cloud.detach_volume.assert_called_once_with(
            self.cinder.sshvm, self.cinder.volume,
            timeout=self.cinder.volume_timeout)
        args[0].assert_called_once_with(
            pkg_resources.resource_filename(
                'functest.opnfv_tests.openstack.cinder', 'write_data.sh'),
            remote_path="~/")

    @mock.patch('scp.SCPClient.put', side_effect=Exception)
    def test_write_exc1(self, *args):
        # pylint: disable=protected-access
        self.cinder.ssh = mock.Mock()
        self.cinder.sshvm = mock.Mock(id='foo')
        self.cinder.cloud.attach_volume = mock.Mock()
        self.assertEqual(
            self.cinder._write_data(), self.cinder.EX_RUN_ERROR)
        args[0].assert_called_once_with(
            pkg_resources.resource_filename(
                'functest.opnfv_tests.openstack.cinder', 'write_data.sh'),
            remote_path="~/")

    @mock.patch('scp.SCPClient.put')
    def test_read(self, *args):
        # pylint: disable=protected-access
        self.cinder.ssh2 = mock.Mock()
        self.cinder.vm2 = mock.Mock(id='foo')
        self.cinder.volume = mock.Mock(id='volume')
        stdout = mock.Mock()
        self.cinder.ssh2.exec_command.return_value = (
            None, stdout, mock.Mock())
        stdout.channel.recv_exit_status.return_value = 0
        self.assertEqual(self.cinder._read_data(), 0)
        self.cinder.ssh2.exec_command.assert_called_once_with(
            "sh ~/read_data.sh {}".format(env.get('VOLUME_DEVICE_NAME')))
        self.cinder.cloud.attach_volume.assert_called_once_with(
            self.cinder.vm2, self.cinder.volume,
            timeout=self.cinder.volume_timeout)
        self.cinder.cloud.detach_volume.assert_called_once_with(
            self.cinder.vm2, self.cinder.volume,
            timeout=self.cinder.volume_timeout)
        args[0].assert_called_once_with(
            pkg_resources.resource_filename(
                'functest.opnfv_tests.openstack.cinder', 'read_data.sh'),
            remote_path="~/")

    @mock.patch('scp.SCPClient.put', side_effect=Exception)
    def test_read_exc1(self, *args):
        # pylint: disable=protected-access
        self.cinder.ssh = mock.Mock()
        self.cinder.ssh2 = mock.Mock()
        self.cinder.sshvm = mock.Mock(id='foo')
        self.cinder.cloud.attach_volume = mock.Mock()
        self.assertEqual(
            self.cinder._read_data(), self.cinder.EX_RUN_ERROR)
        args[0].assert_called_once_with(
            pkg_resources.resource_filename(
                'functest.opnfv_tests.openstack.cinder', 'read_data.sh'),
            remote_path="~/")

    def test_execute_exc1(self):
        # pylint: disable=protected-access
        self.cinder._write_data = mock.Mock(side_effect=Exception)
        self.cinder._read_data = mock.Mock()
        with self.assertRaises(Exception):
            self.cinder.execute()
        self.cinder._write_data.assert_called_once_with()
        self.cinder._read_data.assert_not_called()

    def test_execute_exc2(self):
        # pylint: disable=protected-access
        self.cinder._write_data = mock.Mock(return_value=0)
        self.cinder._read_data = mock.Mock(side_effect=Exception)
        with self.assertRaises(Exception):
            self.cinder.execute()
        self.cinder._write_data.assert_called_once_with()
        self.cinder._read_data.assert_called_once_with()

    def test_execute_res1(self):
        # pylint: disable=protected-access
        self.cinder._write_data = mock.Mock(return_value=1)
        self.cinder._read_data = mock.Mock()
        self.assertEqual(self.cinder.execute(), 1)
        self.cinder._write_data.assert_called_once_with()
        self.cinder._read_data.assert_not_called()

    def test_execute_res2(self):
        # pylint: disable=protected-access
        self.cinder._write_data = mock.Mock(return_value=0)
        self.cinder._read_data = mock.Mock(return_value=1)
        self.assertEqual(self.cinder.execute(), 1)
        self.cinder._write_data.assert_called_once_with()
        self.cinder._read_data.assert_called_once_with()

    def test_execute_res3(self):
        # pylint: disable=protected-access
        self.cinder._write_data = mock.Mock(return_value=0)
        self.cinder._read_data = mock.Mock(return_value=0)
        self.assertEqual(self.cinder.execute(), 0)
        self.cinder._write_data.assert_called_once_with()
        self.cinder._read_data.assert_called_once_with()

    def test_clean_exc1(self):
        self.cinder.cloud = None
        with self.assertRaises(AssertionError):
            self.cinder.clean()

    @mock.patch('functest.core.singlevm.SingleVm2.clean')
    def test_clean_exc2(self, *args):
        self.cinder.vm2 = munch.Munch(id='vm2')
        self.cinder.cloud.delete_server = mock.Mock(
            side_effect=shade.OpenStackCloudException("Foo"))
        with self.assertRaises(shade.OpenStackCloudException):
            self.cinder.clean()
        self.cinder.cloud.delete_server.assert_called_once_with(
            self.cinder.vm2, wait=True,
            timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        self.cinder.cloud.delete_floating_ip.assert_not_called()
        self.cinder.cloud.delete_volume.assert_not_called()
        args[0].assert_not_called()

    @mock.patch('functest.core.singlevm.SingleVm2.clean',
                side_effect=Exception)
    def test_clean_exc3(self, mock_clean):
        self.cinder.vm2 = munch.Munch(id='vm2')
        self.cinder.volume = munch.Munch(id='volume')
        self.cinder.fip2 = munch.Munch(id='fip2')
        with self.assertRaises(Exception):
            self.cinder.clean()
        self.cinder.cloud.delete_server.assert_called_once_with(
            self.cinder.vm2, wait=True,
            timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        self.cinder.cloud.delete_floating_ip.assert_called_once_with(
            self.cinder.fip2.id)
        self.cinder.cloud.delete_volume.assert_called_once_with(
            self.cinder.volume.id)
        mock_clean.prepare()

    @mock.patch('functest.core.singlevm.SingleVm2.clean')
    def test_clean(self, *args):
        self.cinder.vm2 = munch.Munch(id='vm2')
        self.cinder.volume = munch.Munch(id='volume')
        self.cinder.fip2 = munch.Munch(id='fip2')
        self.cinder.clean()
        self.cinder.cloud.delete_server.assert_called_once_with(
            self.cinder.vm2, wait=True,
            timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        self.cinder.cloud.delete_floating_ip.assert_called_once_with(
            self.cinder.fip2.id)
        self.cinder.cloud.delete_volume.assert_called_once_with(
            self.cinder.volume.id)
        args[0].assert_called_once_with()

    @mock.patch('functest.core.singlevm.SingleVm2.clean')
    def test_clean2(self, *args):
        self.cinder.clean()
        self.cinder.cloud.delete_server.assert_not_called()
        self.cinder.cloud.delete_floating_ip.assert_not_called()
        self.cinder.cloud.delete_volume.assert_not_called()
        args[0].assert_called_once_with()


if __name__ == '__main__':
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
