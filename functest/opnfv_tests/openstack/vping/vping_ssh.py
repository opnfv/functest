#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

import os
import re
import sys
import time

import argparse
import paramiko
from scp import SCPClient

import functest.utils.functest_logger as ft_logger
import functest.utils.openstack_utils as os_utils
import vping_base
import functest.core.testcase as testcase


class VPingSSH(vping_base.VPingBase):

    def __init__(self):
        super(VPingSSH, self).__init__()
        self.case_name = 'vping_ssh'
        self.logger = ft_logger.Logger(self.case_name).getLogger()

    def do_vping(self, vm, test_ip):
        floatip = self.add_float_ip(vm)
        if not floatip:
            return testcase.TestCase.EX_RUN_ERROR
        ssh = self.establish_ssh(vm, floatip)
        if not ssh:
            return testcase.TestCase.EX_RUN_ERROR
        if not self.transfer_ping_script(ssh, floatip):
            return testcase.TestCase.EX_RUN_ERROR
        return self.do_vping_ssh(ssh, test_ip)

    def add_float_ip(self, vm):
        self.logger.info("Creating floating IP for VM '%s'..." % self.vm2_name)
        floatip_dic = os_utils.create_floating_ip(self.neutron_client)
        floatip = floatip_dic['fip_addr']

        if floatip is None:
            self.logger.error("Cannot create floating IP.")
            return None
        self.logger.info("Floating IP created: '%s'" % floatip)

        self.logger.info("Associating floating ip: '%s' to VM '%s' "
                         % (floatip, self.vm2_name))
        if not os_utils.add_floating_ip(self.nova_client, vm.id, floatip):
            self.logger.error("Cannot associate floating IP to VM.")
            return None

        return floatip

    def establish_ssh(self, vm, floatip):
        self.logger.info("Trying to establish SSH connection to %s..."
                         % floatip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        timeout = 50
        nolease = False
        got_ip = False
        discover_count = 0
        cidr_first_octet = self.private_subnet_cidr.split('.')[0]
        while timeout > 0:
            try:
                ssh.connect(floatip, username=self.image_username,
                            password=self.image_password, timeout=2)
                self.logger.debug("SSH connection established to %s."
                                  % floatip)
                break
            except:
                self.logger.debug("Waiting for %s..." % floatip)
                time.sleep(6)
                timeout -= 1

            console_log = vm.get_console_output()

            # print each "Sending discover" captured on the console log
            if (len(re.findall("Sending discover", console_log)) >
                    discover_count and not got_ip):
                discover_count += 1
                self.logger.debug("Console-log '%s': Sending discover..."
                                  % self.vm2_name)

            # check if eth0 got an ip,the line looks like this:
            # "inet addr:192.168."....
            # if the dhcp agent fails to assing ip, this line will not appear
            if "inet addr:" + cidr_first_octet in console_log and not got_ip:
                got_ip = True
                self.logger.debug("The instance '%s' succeeded to get the IP "
                                  "from the dhcp agent." % self.vm2_name)

            # if dhcp not work,it shows "No lease, failing".The test will fail
            if ("No lease, failing" in console_log and
                not nolease and
                    not got_ip):
                nolease = True
                self.logger.debug("Console-log '%s': No lease, failing..."
                                  % self.vm2_name)
                self.logger.info("The instance failed to get an IP from DHCP "
                                 "agent. The test will probably timeout...")

        if timeout == 0:  # 300 sec timeout (5 min)
            self.logger.error("Cannot establish connection to IP '%s'. "
                              "Aborting" % floatip)
            return None
        return ssh

    def transfer_ping_script(self, ssh, floatip):
        self.logger.info("Trying to transfer ping.sh to %s..." % floatip)
        scp = SCPClient(ssh.get_transport())
        local_path = self.functest_repo + "/" + self.repo
        ping_script = os.path.join(local_path, "ping.sh")
        try:
            scp.put(ping_script, "~/")
        except:
            self.logger.error("Cannot SCP the file '%s' to VM '%s'"
                              % (ping_script, floatip))
            return False

        cmd = 'chmod 755 ~/ping.sh'
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
        for line in stdout.readlines():
            print line

        return True

    def do_vping_ssh(self, ssh, test_ip):
        EXIT_CODE = -1
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
                    EXIT_CODE = 0
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
        return EXIT_CODE


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-r", "--report",
                             help="Create json result file",
                             action="store_true")
    args = vars(args_parser.parse_args())
    sys.exit(vping_base.VPingMain(VPingSSH).main(**args))
