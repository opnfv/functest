#!/usr/bin/env python

# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""CinderCheck testcase."""

import logging
import os
import tempfile
import time

import paramiko
from xtesting.core import testcase
from xtesting.energy import energy

from functest.opnfv_tests.openstack.cinder import cinder_base
from functest.utils import config


class CinderCheck(cinder_base.CinderBase):
    """
    CinderCheck testcase implementation.

    Class to execute the CinderCheck test using 2 Floating IPs
    to connect to the VMs and one data volume
    """

    def __init__(self, **kwargs):
        """Initialize testcase."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cinder_test"
        super(CinderCheck, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.vm1 = None
        self.vm2 = None
        self.sec = None
        self.fip1 = None
        self.fip2 = None
        self.keypair1 = None
        self.keypair2 = None
        self.ssh = paramiko.SSHClient()
        (_, self.key1_filename) = tempfile.mkstemp()
        self.ssh = paramiko.SSHClient()
        (_, self.key2_filename) = tempfile.mkstemp()

    @energy.enable_recording
    def run(self, **kwargs):
        """
        Excecute CinderCheck testcase.

        Sets up the OpenStack keypair, router, security group, and VM instance
        objects then validates the ping.
        :return: the exit code from the super.execute() method
        """
        try:
            assert self.cloud
            super(CinderCheck, self).run()

            # Creating key pair 1
            kp_name1 = getattr(
                config.CONF, 'cinder_keypair_name') + '_1' + self.guid
            self.logger.info("Creating keypair with name: '%s'", kp_name1)
            self.keypair1 = self.cloud.create_keypair(kp_name1)
            self.logger.debug("keypair: %s", self.keypair1)
            self.logger.debug("private_key: %s", self.keypair1.private_key)
            with open(self.key1_filename, 'w') as private_key1_file:
                private_key1_file.write(self.keypair1.private_key)
            # Creating key pair 2
            kp_name2 = getattr(
                config.CONF, 'cinder_keypair_name') + '_2' + self.guid
            self.logger.info("Creating keypair with name: '%s'", kp_name2)
            self.keypair2 = self.cloud.create_keypair(kp_name2)
            self.logger.debug("keypair: %s", self.keypair2)
            self.logger.debug("private_key: %s", self.keypair2.private_key)
            with open(self.key2_filename, 'w') as private_key2_file:
                private_key2_file.write(self.keypair2.private_key)

            # Creating security group
            self.sec = self.cloud.create_security_group(
                getattr(config.CONF, 'cinder_sg_name') + self.guid,
                getattr(config.CONF, 'cinder_sg_desc'))
            self.cloud.create_security_group_rule(
                self.sec.id, port_range_min='22', port_range_max='22',
                protocol='tcp', direction='ingress')
            self.cloud.create_security_group_rule(
                self.sec.id, protocol='icmp', direction='ingress')

            # Creating VM 1
            vm1_name = "{}-{}-{}".format(
                getattr(config.CONF, 'cinder_vm_name_1'), "ssh", self.guid)
            self.logger.info(
                "Creating VM 1 instance with name: '%s'", vm1_name)
            self.vm1 = self.cloud.create_server(
                vm1_name, image=self.image.id, flavor=self.flavor.id,
                key_name=self.keypair1.id,
                auto_ip=False, wait=True,
                timeout=getattr(config.CONF, 'cinder_vm_boot_timeout'),
                network=self.network.id,
                security_groups=[self.sec.id])
            self.logger.debug("vm1: %s", self.vm2)
            self.fip1 = self.cloud.create_floating_ip(
                network=self.ext_net.id, server=self.vm1)
            self.logger.debug("floating_ip1: %s", self.fip1)
            self.vm1 = self.cloud.wait_for_server(self.vm1, auto_ip=False)
            p_console1 = self.cloud.get_server_console(self.vm1.id)
            self.cloud.attach_volume(self.vm1, self.volume)

            # Creating VM 2
            vm2_name = "{}-{}-{}".format(
                getattr(config.CONF, 'cinder_vm_name_2'), "ssh", self.guid)
            self.logger.info(
                "Creating VM 2 instance with name: '%s'", vm2_name)
            self.vm2 = self.cloud.create_server(
                vm2_name, image=self.image.id, flavor=self.flavor.id,
                key_name=self.keypair2.id,
                auto_ip=False, wait=True,
                timeout=getattr(config.CONF, 'cinder_vm_boot_timeout'),
                network=self.network.id,
                security_groups=[self.sec.id])
            self.logger.debug("vm2: %s", self.vm2)
            self.fip2 = self.cloud.create_floating_ip(
                network=self.ext_net.id, server=self.vm2)
            self.logger.debug("floating_ip2: %s", self.fip2)
            self.vm2 = self.cloud.wait_for_server(self.vm2, auto_ip=False)
            p_console2 = self.cloud.get_server_console(self.vm2.id)

            return self._execute()
        except Exception:  # pylint: disable=broad-except
            self.logger.exception('Unexpected error running cinder_ssh')
            return testcase.TestCase.EX_RUN_ERROR

    def _write_data(self):
        time.sleep(10)
        cmd = 'sudo /usr/sbin/mkfs.ext4 -F /dev/vdc;' \
            'sudo mkdir -p -m 777 ~/volume;' \
            'sudo mount /dev/vdc ~/volume;' \
            'sudo touch  ~/volume/new_data;' \
            'if [[ $(sudo mount|grep vdc) ]];' \
            'then echo \"New data added to the volume\"; fi'
        self.ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.ssh.connect(
            self.vm1.public_v4,
            username=getattr(config.CONF, 'openstack_image_user'),
            key_filename=self.key1_filename,
            timeout=getattr(config.CONF, 'cinder_vm_ssh_connect_timeout'))
        self.logger.debug("ssh: %s", self.ssh)
        (stdin, stdout, stderr) = self.ssh.exec_command(cmd)
        self.logger.debug("volume_write output: %s", stdout.read())
        return stdout.channel.recv_exit_status()

    def _read_data(self):
        assert self.cloud
        # Detach volume from VM 1
        self.logger.info("Detach volume from VM 1")
        self.cloud.detach_volume(self.vm1, self.volume)
        # Attach volume to VM 2
        self.logger.info("Attach volume to VM 2")
        self.cloud.attach_volume(self.vm2, self.volume)
        # Check volume data
        time.sleep(10)
        cmd = 'sudo mkdir -p -m 777 ~/volume;' \
            'sudo mount /dev/vdc ~/volume;' \
            'if [[ $(ls ~/volume|grep new_data) ]];' \
            'then echo \"Found existing data\"; fi'
        self.ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.ssh.connect(
            self.vm2.public_v4,
            username=getattr(config.CONF, 'openstack_image_user'),
            key_filename=self.key2_filename,
            timeout=getattr(config.CONF, 'cinder_vm_ssh_connect_timeout'))
        self.logger.debug("ssh: %s", self.ssh)
        (stdin, stdout, stderr) = self.ssh.exec_command(cmd)
        self.logger.debug("read volume output: %s", stdout.read())
        return stdout.channel.recv_exit_status()

    def clean(self):
        assert self.cloud
        os.remove(self.key1_filename)
        os.remove(self.key2_filename)
        self.cloud.delete_server(
            self.vm1, wait=True,
            timeout=getattr(config.CONF, 'cinder_vm_delete_timeout'))
        self.cloud.delete_server(
            self.vm2, wait=True,
            timeout=getattr(config.CONF, 'cinder_vm_delete_timeout'))
        self.cloud.delete_security_group(self.sec.id)
        self.cloud.delete_keypair(self.keypair1.id)
        self.cloud.delete_keypair(self.keypair2.id)
        self.cloud.delete_floating_ip(self.fip1.id)
        self.cloud.delete_floating_ip(self.fip2.id)
        super(CinderCheck, self).clean()
