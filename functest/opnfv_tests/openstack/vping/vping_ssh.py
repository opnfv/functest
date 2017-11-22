#!/usr/bin/env python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0


"""vPingSSH testcase."""

# This 1st import is here simply for pep8 as the 'os' package import appears
# to be required for mock and the unit tests will fail without it
import os  # noqa # pylint: disable=unused-import
import time

from scp import SCPClient
import pkg_resources

from functest.core.testcase import TestCase
from functest.energy import energy
from functest.opnfv_tests.openstack.vping import vping_base
from functest.utils.constants import CONST

from snaps.config.keypair import KeypairConfig
from snaps.config.network import PortConfig
from snaps.config.security_group import (
    Direction, Protocol, SecurityGroupConfig, SecurityGroupRuleConfig)
from snaps.config.vm_inst import FloatingIpConfig, VmInstanceConfig

from snaps.openstack.utils import deploy_utils


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

        self.kp_name = CONST.__getattribute__('vping_keypair_name') + self.guid
        self.kp_priv_file = CONST.__getattribute__('vping_keypair_priv_file')
        self.kp_pub_file = CONST.__getattribute__('vping_keypair_pub_file')
        self.sg_name = CONST.__getattribute__('vping_sg_name') + self.guid
        self.sg_desc = CONST.__getattribute__('vping_sg_desc')

    @energy.enable_recording
    def run(self):
        """
        Excecute VPingSSH testcase.

        Sets up the OpenStack keypair, router, security group, and VM instance
        objects then validates the ping.
        :return: the exit code from the super.execute() method
        """
        try:
            super(VPingSSH, self).run()

            log = "Creating keypair with name: '%s'" % self.kp_name
            self.logger.info(log)
            kp_creator = deploy_utils.create_keypair(
                self.os_creds,
                KeypairConfig(
                    name=self.kp_name, private_filepath=self.kp_priv_file,
                    public_filepath=self.kp_pub_file))
            self.creators.append(kp_creator)

            # Creating Instance 1
            port1_settings = PortConfig(
                name=self.vm1_name + '-vPingPort',
                network_name=self.network_creator.network_settings.name)
            instance1_settings = VmInstanceConfig(
                name=self.vm1_name, flavor=self.flavor_name,
                vm_boot_timeout=self.vm_boot_timeout,
                vm_delete_timeout=self.vm_delete_timeout,
                ssh_connect_timeout=self.vm_ssh_connect_timeout,
                port_settings=[port1_settings])

            log = ("Creating VM 1 instance with name: '%s'"
                   % instance1_settings.name)
            self.logger.info(log)
            self.vm1_creator = deploy_utils.create_vm_instance(
                self.os_creds,
                instance1_settings,
                self.image_creator.image_settings,
                keypair_creator=kp_creator)
            self.creators.append(self.vm1_creator)

            # Creating Instance 2
            sg_creator = self.__create_security_group()
            self.creators.append(sg_creator)

            port2_settings = PortConfig(
                name=self.vm2_name + '-vPingPort',
                network_name=self.network_creator.network_settings.name)
            instance2_settings = VmInstanceConfig(
                name=self.vm2_name, flavor=self.flavor_name,
                vm_boot_timeout=self.vm_boot_timeout,
                vm_delete_timeout=self.vm_delete_timeout,
                ssh_connect_timeout=self.vm_ssh_connect_timeout,
                port_settings=[port2_settings],
                security_group_names=[sg_creator.sec_grp_settings.name],
                floating_ip_settings=[FloatingIpConfig(
                    name=self.vm2_name + '-FIPName',
                    port_name=port2_settings.name,
                    router_name=self.router_creator.router_settings.name)])

            log = ("Creating VM 2 instance with name: '%s'"
                   % instance2_settings.name)
            self.logger.info(log)
            self.vm2_creator = deploy_utils.create_vm_instance(
                self.os_creds,
                instance2_settings,
                self.image_creator.image_settings,
                keypair_creator=kp_creator)
            self.creators.append(self.vm2_creator)

            return self._execute()
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.error('Unexpected error running test - ' + exc.message)
            return TestCase.EX_RUN_ERROR
        finally:
            self._cleanup()

    def _do_vping(self, vm_creator, test_ip):
        """
        Execute ping command.

        Override from super
        """
        if vm_creator.vm_ssh_active(block=True):
            ssh = vm_creator.ssh_client()
            if not self._transfer_ping_script(ssh):
                return TestCase.EX_RUN_ERROR
            return self._do_vping_ssh(ssh, test_ip)
        else:
            return TestCase.EX_RUN_ERROR

    def _transfer_ping_script(self, ssh):
        """
        Transfert vping script to VM.

        Uses SCP to copy the ping script via the SSH client
        :param ssh: the SSH client
        :return:
        """
        self.logger.info("Trying to transfer ping.sh")
        scp = SCPClient(ssh.get_transport())
        ping_script = pkg_resources.resource_filename(
            'functest.opnfv_tests.openstack.vping', 'ping.sh')
        try:
            scp.put(ping_script, "~/")
        except Exception:
            self.logger.error("Cannot SCP the file '%s'", ping_script)
            return False

        cmd = 'chmod 755 ~/ping.sh'
        # pylint: disable=unused-variable
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
        for line in stdout.readlines():
            print line

        return True

    def _do_vping_ssh(self, ssh, test_ip):
        """
        Execute ping command via SSH.

        Pings the test_ip via the SSH client
        :param ssh: the SSH client used to issue the ping command
        :param test_ip: the IP for the ping command to use
        :return: exit_code (int)
        """
        exit_code = TestCase.EX_TESTCASE_FAILED
        self.logger.info("Waiting for ping...")

        sec = 0
        cmd = '~/ping.sh ' + test_ip
        flag = False

        while True:
            time.sleep(1)
            (_, stdout, _) = ssh.exec_command(cmd)
            output = stdout.readlines()

            for line in output:
                if "vPing OK" in line:
                    self.logger.info("vPing detected!")
                    exit_code = TestCase.EX_OK
                    flag = True
                    break

                elif sec == self.ping_timeout:
                    self.logger.info("Timeout reached.")
                    flag = True
                    break
            if flag:
                break
            log = "Pinging %s. Waiting for response..." % test_ip
            self.logger.debug(log)
            sec += 1
        return exit_code

    def __create_security_group(self):
        """
        Configure OpenStack security groups.

        Configures and deploys an OpenStack security group object
        :return: the creator object
        """
        sg_rules = list()
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name=self.sg_name, direction=Direction.ingress,
                protocol=Protocol.icmp))
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name=self.sg_name, direction=Direction.ingress,
                protocol=Protocol.tcp, port_range_min=22, port_range_max=22))
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name=self.sg_name, direction=Direction.egress,
                protocol=Protocol.tcp, port_range_min=22, port_range_max=22))

        log = "Security group with name: '%s'" % self.sg_name
        self.logger.info(log)
        return deploy_utils.create_security_group(self.os_creds,
                                                  SecurityGroupConfig(
                                                      name=self.sg_name,
                                                      description=self.sg_desc,
                                                      rule_settings=sg_rules))
