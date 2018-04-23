#!/usr/bin/env python

# Copyright (c) 2017 Cable Television Laboratories, Inc. and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import unittest

import mock
from snaps.config.keypair import KeypairConfig
from snaps.config.network import NetworkConfig, PortConfig, SubnetConfig
from snaps.config.router import RouterConfig
from snaps.config.security_group import SecurityGroupConfig
from snaps.config.vm_inst import VmInstanceConfig
from snaps.openstack.create_image import OpenStackImage
from snaps.openstack.create_instance import OpenStackVmInstance
from snaps.openstack.create_keypairs import OpenStackKeypair
from snaps.openstack.create_network import OpenStackNetwork
from snaps.openstack.create_router import OpenStackRouter
from snaps.openstack.create_security_group import OpenStackSecurityGroup
from snaps.openstack.os_credentials import OSCreds
from xtesting.core import testcase

from functest.opnfv_tests.openstack.vping import vping_userdata, vping_ssh
from functest.utils import env


class VPingUserdataTesting(unittest.TestCase):
    """
    Ensures the VPingUserdata class can run in Functest. This test does not
    actually connect with an OpenStack pod.
    """

    def setUp(self):
        self.os_creds = OSCreds(
            username='user', password='pass',
            auth_url='http://foo.com:5000/v3', project_name='bar')

        self.vping_userdata = vping_userdata.VPingUserdata(
            os_creds=self.os_creds)

    @mock.patch('snaps.openstack.utils.deploy_utils.create_vm_instance')
    @mock.patch('os.path.exists', return_value=True)
    @mock.patch('snaps.openstack.utils.keystone_utils.keystone_client')
    @mock.patch('snaps.openstack.utils.keystone_utils.get_project')
    @mock.patch('snaps.openstack.create_flavor.OpenStackFlavor.create',
                return_value=None)
    @mock.patch('snaps.openstack.create_instance.OpenStackVmInstance.'
                'get_port_ip', return_value='10.0.0.1')
    @mock.patch('snaps.openstack.create_instance.OpenStackVmInstance.'
                'vm_active', return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name', return_value='foo')
    def test_vping_userdata(self, *args):
        # pylint: disable=unused-argument
        with mock.patch('snaps.openstack.create_image.OpenStackImage.create',
                        return_value=OpenStackImage(self.os_creds, None)), \
                mock.patch(
                    'snaps.openstack.create_network.OpenStackNetwork.create',
                    return_value=OpenStackNetwork(
                        self.os_creds, NetworkConfig(name='foo'))), \
                mock.patch(
                    'snaps.openstack.create_router.OpenStackRouter.create',
                    return_value=OpenStackRouter(
                        self.os_creds, RouterConfig(name='foo'))), \
                mock.patch('snaps.openstack.utils.deploy_utils.'
                           'create_vm_instance',
                           return_value=OpenStackVmInstance(
                               self.os_creds,
                               VmInstanceConfig(
                                   name='foo', flavor='bar',
                                   port_settings=[PortConfig(
                                       name='foo', network_name='bar')]),
                               None)), \
                mock.patch('snaps.openstack.create_instance.'
                           'OpenStackVmInstance.get_console_output',
                           return_value='vPing OK'):
            self.assertEquals(
                testcase.TestCase.EX_OK, self.vping_userdata.run())


class VPingSSHTesting(unittest.TestCase):
    """
    Ensures the VPingUserdata class can run in Functest. This test does not
    actually connect with an OpenStack pod.
    """

    def setUp(self):
        self.os_creds = OSCreds(
            username='user', password='pass',
            auth_url='http://foo.com:5000/v3', project_name='bar')

        self.vping_ssh = vping_ssh.VPingSSH(
            os_creds=self.os_creds)

    @mock.patch('snaps.openstack.utils.deploy_utils.create_vm_instance')
    @mock.patch('os.path.exists', return_value=True)
    @mock.patch('snaps.openstack.utils.keystone_utils.keystone_client')
    @mock.patch('snaps.openstack.utils.keystone_utils.get_project')
    @mock.patch('snaps.openstack.create_flavor.OpenStackFlavor.create',
                return_value=None)
    @mock.patch('snaps.openstack.create_instance.OpenStackVmInstance.'
                'get_port_ip', return_value='10.0.0.1')
    @mock.patch('snaps.openstack.create_instance.OpenStackVmInstance.'
                'vm_active', return_value=True)
    @mock.patch('snaps.openstack.create_instance.OpenStackVmInstance.'
                'vm_ssh_active', return_value=True)
    @mock.patch('snaps.openstack.create_instance.OpenStackVmInstance.'
                'ssh_client', return_value=True)
    @mock.patch('scp.SCPClient')
    @mock.patch('functest.opnfv_tests.openstack.vping.vping_ssh.'
                'VPingSSH._transfer_ping_script', return_value=True)
    @mock.patch('functest.opnfv_tests.openstack.vping.vping_ssh.'
                'VPingSSH._do_vping_ssh', return_value=testcase.TestCase.EX_OK)
    @mock.patch('functest.opnfv_tests.openstack.snaps.snaps_utils.'
                'get_ext_net_name', return_value='foo')
    def test_vping_ssh(self, *args):
        # pylint: disable=unused-argument
        os_vm_inst = mock.MagicMock(name='get_console_output')
        os_vm_inst.get_console_output.return_value = 'vPing OK'
        ssh_client = mock.MagicMock(name='get_transport')
        ssh_client.get_transport.return_value = None
        scp_client = mock.MagicMock(name='put')
        scp_client.put.return_value = None

        subnet_config = SubnetConfig(
            name='bar',
            cidr='10.0.0.1/24',
            dns_nameservers=[env.get('NAMESERVER')])

        with mock.patch('snaps.openstack.create_image.OpenStackImage.create',
                        return_value=OpenStackImage(self.os_creds, None)), \
                mock.patch(
                    'snaps.openstack.create_network.OpenStackNetwork.create',
                    return_value=OpenStackNetwork(
                        self.os_creds,
                        NetworkConfig(
                            name='foo',
                            subnet_settings=[subnet_config]))), \
                mock.patch('snaps.openstack.utils.deploy_utils.'
                           'create_vm_instance',
                           return_value=OpenStackVmInstance(
                               self.os_creds,
                               VmInstanceConfig(
                                   name='foo', flavor='bar',
                                   port_settings=[PortConfig(
                                       name='foo', network_name='bar')]),
                               None)), \
                mock.patch('snaps.openstack.utils.deploy_utils.create_keypair',
                           return_value=OpenStackKeypair(
                               self.os_creds, KeypairConfig(name='foo'))), \
                mock.patch(
                    'snaps.openstack.create_router.OpenStackRouter.create',
                    return_value=OpenStackRouter(
                        self.os_creds, RouterConfig(name='foo'))), \
                mock.patch('snaps.openstack.utils.deploy_utils.'
                           'create_security_group',
                           return_value=OpenStackSecurityGroup(
                               self.os_creds,
                               SecurityGroupConfig(name='foo'))), \
                mock.patch('snaps.openstack.create_instance.'
                           'OpenStackVmInstance.'
                           'get_vm_inst', return_value=os_vm_inst), \
                mock.patch('snaps.openstack.create_instance.'
                           'OpenStackVmInstance.'
                           'ssh_client', return_value=ssh_client):
            self.assertEquals(testcase.TestCase.EX_OK, self.vping_ssh.run())


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
