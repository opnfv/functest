#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import argparse
import os
from scp import SCPClient
import sys
import time

from snaps.openstack.create_instance import FloatingIpSettings, \
    VmInstanceSettings
from snaps.openstack.create_keypairs import KeypairSettings
from snaps.openstack.create_network import PortSettings
from snaps.openstack.create_router import RouterSettings
from snaps.openstack.create_security_group import Direction, Protocol, \
    SecurityGroupSettings, SecurityGroupRuleSettings
from snaps.openstack.utils import deploy_utils

from functest.core.testcase_base import TestcaseBase
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger
import vping_base


class VPingSSH(vping_base.VPingBase):
    """
    Class to execute the vPing test using a Floating IP to connect to one VM
    to issue the ping command to the second
    """

    def __init__(self, case_name='vping_ssh'):
        super(VPingSSH, self).__init__(case_name)
        self.logger = ft_logger.Logger(self.case_name).getLogger()

        self.kp_name = CONST.vping_keypair_name + self.guid
        self.kp_priv_file = CONST.vping_keypair_priv_file
        self.kp_pub_file = CONST.vping_keypair_pub_file
        self.router_name = CONST.vping_router_name + self.guid
        self.sg_name = CONST.vping_sg_name + self.guid
        self.sg_desc = CONST.vping_sg_desc

        self.ext_net_name = snaps_utils.get_ext_net_name()

    def run(self):
        """
        Sets up the OpenStack keypair, router, security group, and VM instance
        objects then validates the ping.
        :return: the exit code from the super.execute() method
        """
        try:
            super(VPingSSH, self).run()

            self.logger.info("Creating keypair with name: '%s'" % self.kp_name)
            self.kp_creator = deploy_utils.create_keypair(
                self.os_creds,
                KeypairSettings(name=self.kp_name,
                                private_filepath=self.kp_priv_file,
                                public_filepath=self.kp_pub_file))

            # Creating router to external network
            self.logger.info("Creating router with name: '%s'"
                             % self.router_name)
            net_set = self.network_creator.network_settings
            sub_set = [net_set.subnet_settings[0].name]
            self.router_creator = deploy_utils.create_router(
                self.os_creds,
                RouterSettings(
                    name=self.router_name,
                    external_gateway=self.ext_net_name,
                    internal_subnets=sub_set))

            # Creating Instance 1
            port1_settings = PortSettings(
                name=self.vm1_name + '-vPingPort',
                network_name=self.network_creator.network_settings.name)
            instance1_settings = VmInstanceSettings(
                name=self.vm1_name, flavor=self.flavor_name,
                vm_boot_timeout=self.vm_boot_timeout,
                vm_delete_timeout=self.vm_delete_timeout,
                ssh_connect_timeout=self.vm_ssh_connect_timeout,
                port_settings=[port1_settings])

            self.logger.info(
                "Creating VM 1 instance with name: '%s'"
                % instance1_settings.name)
            self.vm1_creator = deploy_utils.create_vm_instance(
                self.os_creds,
                instance1_settings,
                self.image_creator.image_settings,
                keypair_creator=self.kp_creator)

            # Creating Instance 2
            self.sg_creator = self.__create_security_group()

            port2_settings = PortSettings(
                name=self.vm2_name + '-vPingPort',
                network_name=self.network_creator.network_settings.name)
            instance2_settings = VmInstanceSettings(
                name=self.vm2_name, flavor=self.flavor_name,
                vm_boot_timeout=self.vm_boot_timeout,
                vm_delete_timeout=self.vm_delete_timeout,
                ssh_connect_timeout=self.vm_ssh_connect_timeout,
                port_settings=[port2_settings],
                security_group_names=[self.sg_creator.sec_grp_settings.name],
                floating_ip_settings=[FloatingIpSettings(
                    name=self.vm2_name + '-FIPName',
                    port_name=port2_settings.name,
                    router_name=self.router_creator.router_settings.name)])

            self.logger.info(
                "Creating VM 2 instance with name: '%s'"
                % instance2_settings.name)
            self.vm2_creator = deploy_utils.create_vm_instance(
                self.os_creds,
                instance2_settings,
                self.image_creator.image_settings,
                keypair_creator=self.kp_creator)

            return self._execute()
        except Exception as e:
            self.logger.error('Unexpected error running test - ' + e.message)
            return TestcaseBase.EX_RUN_ERROR
        finally:
            self._cleanup()

    def _do_vping(self, vm_creator, test_ip):
        """
        Override from super
        """
        if vm_creator.vm_ssh_active(block=True):
            ssh = vm_creator.ssh_client()
            if not self.__transfer_ping_script(ssh):
                return TestcaseBase.EX_RUN_ERROR
            return self.__do_vping_ssh(ssh, test_ip)
        else:
            return -1

    def __transfer_ping_script(self, ssh):
        """
        Uses SCP to copy the ping script via the SSH client
        :param ssh: the SSH client
        :return:
        """
        self.logger.info("Trying to transfer ping.sh")
        scp = SCPClient(ssh.get_transport())
        local_path = self.functest_repo + "/" + self.repo
        ping_script = os.path.join(local_path, "ping.sh")
        try:
            scp.put(ping_script, "~/")
        except:
            self.logger.error("Cannot SCP the file '%s'" % ping_script)
            return False

        cmd = 'chmod 755 ~/ping.sh'
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
        for line in stdout.readlines():
            print line

        return True

    def __do_vping_ssh(self, ssh, test_ip):
        """
        Pings the test_ip via the SSH client
        :param ssh: the SSH client used to issue the ping command
        :param test_ip: the IP for the ping command to use
        :return: exit_code (int)
        """
        exit_code = -1
        self.logger.info("Waiting for ping...")

        sec = 0
        cmd = '~/ping.sh ' + test_ip
        flag = False

        while True:
            time.sleep(1)
            (stdin, stdout, stderr) = ssh.exec_command(cmd)
            output = stdout.readlines()

            for line in output:
                if "vPing OK" in line:
                    self.logger.info("vPing detected!")
                    exit_code = 0
                    flag = True
                    break

                elif sec == self.ping_timeout:
                    self.logger.info("Timeout reached.")
                    flag = True
                    break
            if flag:
                break
            self.logger.debug("Pinging %s. Waiting for response..." % test_ip)
            sec += 1
        return exit_code

    def __create_security_group(self):
        """
        Configures and deploys an OpenStack security group object
        :return: the creator object
        """
        sg_rules = list()
        sg_rules.append(
            SecurityGroupRuleSettings(sec_grp_name=self.sg_name,
                                      direction=Direction.ingress,
                                      protocol=Protocol.icmp))
        sg_rules.append(
            SecurityGroupRuleSettings(sec_grp_name=self.sg_name,
                                      direction=Direction.ingress,
                                      protocol=Protocol.tcp, port_range_min=22,
                                      port_range_max=22))
        sg_rules.append(
            SecurityGroupRuleSettings(sec_grp_name=self.sg_name,
                                      direction=Direction.egress,
                                      protocol=Protocol.tcp, port_range_min=22,
                                      port_range_max=22))

        self.logger.info("Security group with name: '%s'" % self.sg_name)
        return deploy_utils.create_security_group(self.os_creds,
                                                  SecurityGroupSettings(
                                                      name=self.sg_name,
                                                      description=self.sg_desc,
                                                      rule_settings=sg_rules))


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-r", "--report",
                             help="Create json result file",
                             action="store_true")
    args = vars(args_parser.parse_args())
    sys.exit(vping_base.VPingMain(VPingSSH).main(**args))
