#!/usr/bin/env python

# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""vPingSSH testcase."""

import logging
import os
import tempfile
import time

import paramiko
import pkg_resources
from scp import SCPClient
from xtesting.core import testcase
from xtesting.energy import energy

from functest.opnfv_tests.openstack.vping import vping_base
from functest.utils import config


class VPingSSH(vping_base.VPingBase):
    """
    VPingSSH testcase implementation.

    Class to execute the vPing test using a Floating IP to connect to one VM
    to issue the ping command to the second
    """

    def __init__(self, **kwargs):
        """Initialize testcase."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "vping_ssh"
        super(VPingSSH, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.vm2 = None
        self.sec = None
        self.fip = None
        self.keypair = None
        self.ssh = paramiko.SSHClient()
        (_, self.key_filename) = tempfile.mkstemp()

    @energy.enable_recording
    def run(self, **kwargs):
        """
        Excecute VPingSSH testcase.

        Sets up the OpenStack keypair, router, security group, and VM instance
        objects then validates the ping.
        :return: the exit code from the super.execute() method
        """
        try:
            super(VPingSSH, self).run()

            kp_name = getattr(config.CONF, 'vping_keypair_name') + self.guid
            self.logger.info("Creating keypair with name: '%s'", kp_name)
            self.keypair = self.cloud.create_keypair(kp_name)
            self.logger.debug("keypair: %s", self.keypair)
            self.logger.debug("private_key: %s", self.keypair.private_key)
            with open(self.key_filename, 'w') as private_key_file:
                private_key_file.write(self.keypair.private_key)

            self.sec = self.cloud.create_security_group(
                getattr(config.CONF, 'vping_sg_name') + self.guid,
                getattr(config.CONF, 'vping_sg_desc'))
            self.cloud.create_security_group_rule(
                self.sec.id, port_range_min='22', port_range_max='22',
                protocol='tcp', direction='ingress')
            self.cloud.create_security_group_rule(
                self.sec.id, protocol='icmp', direction='ingress')

            vm2_name = "{}-{}-{}".format(
                getattr(config.CONF, 'vping_vm_name_2'), "ssh", self.guid)
            self.logger.info(
                "Creating VM 2 instance with name: '%s'", vm2_name)
            self.vm2 = self.cloud.create_server(
                vm2_name, image=self.image.id, flavor=self.flavor.id,
                key_name=self.keypair.id,
                auto_ip=False, wait=True,
                timeout=getattr(config.CONF, 'vping_vm_boot_timeout'),
                network=self.network.id,
                security_groups=[self.sec.id])
            self.logger.debug("vm2: %s", self.vm2)
            self.fip = self.cloud.create_floating_ip(
                network=self.ext_net.id, server=self.vm2)
            self.logger.debug("floating_ip2: %s", self.fip)
            self.vm2 = self.cloud.wait_for_server(self.vm2, auto_ip=False)

            return self._execute()
        except Exception:  # pylint: disable=broad-except
            self.logger.exception('Unexpected error running vping_ssh')
            return testcase.TestCase.EX_RUN_ERROR

    def _do_vping(self):
        """
        Execute ping command.

        Override from super
        """
        time.sleep(10)
        self.ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.ssh.connect(
            self.vm2.public_v4,
            username=getattr(config.CONF, 'openstack_image_user'),
            key_filename=self.key_filename,
            timeout=getattr(config.CONF, 'vping_vm_ssh_connect_timeout'))
        self.logger.debug("ssh: %s", self.ssh)
        if not self._transfer_ping_script():
            return testcase.TestCase.EX_RUN_ERROR
        return self._do_vping_ssh()

    def _transfer_ping_script(self):
        """
        Transfert vping script to VM.

        Uses SCP to copy the ping script via the SSH client
        :param ssh: the SSH client
        :return:
        """
        self.logger.info("Trying to transfer ping.sh")
        scp = SCPClient(self.ssh.get_transport())
        ping_script = pkg_resources.resource_filename(
            'functest.opnfv_tests.openstack.vping', 'ping.sh')
        try:
            scp.put(ping_script, "~/")
        except Exception:  # pylint: disable=broad-except
            self.logger.error("Cannot SCP the file '%s'", ping_script)
            return False

        cmd = 'chmod 755 ~/ping.sh'
        (_, stdout, _) = self.ssh.exec_command(cmd)
        for line in stdout.readlines():
            print line

        return True

    def _do_vping_ssh(self):
        """
        Execute ping command via SSH.

        Pings the test_ip via the SSH client
        :param ssh: the SSH client used to issue the ping command
        :param test_ip: the IP for the ping command to use
        :return: exit_code (int)
        """
        exit_code = testcase.TestCase.EX_TESTCASE_FAILED
        self.logger.info("Waiting for ping...")

        sec = 0
        cmd = '~/ping.sh ' + self.vm1.private_v4
        flag = False

        while True:
            time.sleep(1)
            (_, stdout, _) = self.ssh.exec_command(cmd)
            output = stdout.readlines()

            for line in output:
                if "vPing OK" in line:
                    self.logger.info("vPing detected!")
                    exit_code = testcase.TestCase.EX_OK
                    flag = True
                    break
                elif sec == getattr(config.CONF, 'vping_ping_timeout'):
                    self.logger.info("Timeout reached.")
                    flag = True
                    break
            if flag:
                break
            log = "Pinging %s. Waiting for response..." % self.vm1.private_v4
            self.logger.debug(log)
            sec += 1
        return exit_code

    def clean(self):
        os.remove(self.key_filename)
        self.cloud.delete_server(
            self.vm2, wait=True,
            timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        self.cloud.delete_security_group(self.sec.id)
        self.cloud.delete_keypair(self.keypair.id)
        self.cloud.delete_floating_ip(self.fip.id)
        super(VPingSSH, self).clean()
