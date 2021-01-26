#!/usr/bin/env python

# Copyright (c) 2021 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""sctp testcase"""

import logging

from xtesting.core import testcase
from functest.core import singlevm
from functest.utils import config
from functest.utils import env


class Sctp(singlevm.SingleVm2):
    """
    Class to execute the sctp test using userdata and the VM's console
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=logging-format-interpolation
    # pylint: disable=line-too-long

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "sctp"
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.filename = ('/home/opnfv/functest/images/'
                         'ubuntu-14.04-server-cloudimg-amd64-disk1.img')
        self.flavor_ram = 2048
        self.flavor_vcpus = 2
        self.flavor_disk = 4
        self.flavor_extra_specs = {}
        self.flavor_alt_ram = 2048
        self.flavor_alt_vcpus = 2
        self.flavor_alt_disk = 4
        self.fip2 = None
        self.ssh2 = None
        self.vm2 = None
        self.network2 = None
        self.subnet2 = None
        self.cidr2 = '192.168.130.0/24'
        self.username = 'ubuntu'
        self.pid = self.project.project.id
        self.networks = []
        self.sctp_darn_client_stdout = None
        self.sctp_darn_client_stderr = None

    def get_networks_to_connect_to_vm(self):
        """Return the list of networks to connect to vms"""

        if self.network and self.network2:
            self.networks.append(self.network.id)
            self.networks.append(self.network2.id)
        elif self.network:
            self.networks.append(self.network.id)
        elif self.network2:
            self.networks.append(self.network2.id)
        else:
            self.networks.append(env.get("EXTERNAL_NETWORK"))

    def boot_vm(self, name=None, **kwargs):
        """Boot the virtual machine

        It allows booting multiple machines for the child testcases. It forces
        the same configuration for all subtestcases.

        Returns: vm

        Raises: expection on error
        """
        assert self.cloud
        vm1 = self.cloud.create_server(
            name if name else '{}-vm_{}'.format(self.case_name, self.guid),
            image=self.image.id, flavor=self.flavor.id,
            auto_ip=False,
            network=self.networks,
            timeout=self.create_server_timeout, wait=True, **kwargs)
        self.logger.debug("vm: %s", vm1)
        return vm1

    def prepare(self):
        super().prepare()
        self.network2 = self.cloud.create_network(
            '{}-net_{}'.format(self.case_name, self.guid),
            project_id=self.pid,
            shared=False)
        self.logger.debug("network: %s", self.network2)

        self.subnet2 = self.cloud.create_subnet(
            self.network2.id,
            subnet_name='{}-subnet_{}'.format(self.case_name, self.guid),
            cidr=getattr(
                config.CONF, '{}_private_subnet_cidr'.format(self.case_name),
                self.cidr2),
            enable_dhcp=True,
            dns_nameservers=[env.get('NAMESERVER')])
        self.logger.debug("subnet: %s", self.subnet2)
        self.get_networks_to_connect_to_vm()
        self.cloud.create_security_group_rule(
            self.sec.id, port_range_min='5201', port_range_max='5201',
            protocol='sctp', direction='ingress')
        self.cloud.create_security_group_rule(
            self.sec.id, port_range_min='5201', port_range_max='5201',
            protocol='sctp', direction='egress')

        self.vm2 = self.boot_vm(
            '{}-vm2_{}'.format(self.case_name, self.guid),
            key_name=self.keypair.id,
            security_groups=[self.sec.id])
        (self.fip2, self.ssh2) = self.connect(self.vm2)

    def execute(self):
        """Execute Sctp testcase.

        Sets up the OpenStack keypair, router, security group, and VM instance
        objects then validates Sctp connection using lsctp-tools.
        :return: the exit code from the super.execute() method
        """
        return self._do_sctp_darn()

    def _do_sctp_darn(self):
        """
        Override from super
        """
        if not (self.vm2.private_v4 or
                self.vm2.addresses[self.network.name][0].addr):
            self.logger.error("vm2: IP addr missing")
            return testcase.TestCase.EX_TESTCASE_FAILED

        self.logger.info("Waiting for connect...")
        self.logger.info("sshvm: {} vm2: {}".format(self.sshvm, self.vm2))
        self.logger.info("vm2 net1:{} sshvm net1:{} \
                         vm2 net2:{} sshvm net2:{}".format(
                             self.vm2.addresses[self.network.name][0].addr,
                             self.sshvm.addresses[self.network.name][0].addr,
                             self.vm2.addresses[self.network.name][1].addr,
                             self.sshvm.addresses[self.network.name][1].addr))
        exit_code = 1
        self.logger.info("ssh: %s", self.ssh)
        (_, stdout, stderr) = self.ssh.exec_command(
            "sudo ip link set dev eth1 up && \
             sudo dhclient eth1 && ip a && \
             sudo apt-get install -y lksctp-tools")
        self.logger.info(
            "lksctp-tools install server stdout: %s",
            stdout.read().decode("utf-8"))
        self.logger.info(
            "lksctp-tools install server stderr: %s",
            stderr.read().decode("utf-8"))

        self.logger.debug("ssh: %s", self.ssh2)
        (_, stdout, stderr) = self.ssh2.exec_command(
            "sudo ip link set dev eth1 up && \
             sudo dhclient eth1 && ip a && \
             sudo apt-get install -y lksctp-tools")
        self.logger.info(
            "lksctp-tools install \
            client stdout: %s", stdout.read().decode("utf-8"))
        self.logger.info(
            "lksctp-tools install \
            client stderr: %s", stderr.read().decode("utf-8"))

        self.logger.debug("ssh: %s", self.ssh)
        (_, stdout, stderr) = self.ssh.exec_command(
            "sudo sctp_darn -l -P 5201 "
            "-H %s -B %s > /tmp/sctp_darn_logs 2>&1 &" % (
                self.sshvm.addresses[self.network.name][1].addr,
                self.sshvm.addresses[self.network.name][0].addr))
        self.logger.info(
            "sctp_darn server stdout: %s", stdout.read().decode("utf-8"))
        self.logger.info(
            "sctp_darn server stderr: %s", stderr.read().decode("utf-8"))

        self.logger.debug("ssh: %s", self.ssh2)
        (_, stdout, stderr) = self.ssh2.exec_command(
            "(i=1; while [ $i -le 20 ]; do echo blah; sleep 1;"
            " ((i++));  done)|sudo sctp_darn -P "
            "5201 -H {} -h {} -p 5201 -B {} -s".format(
                self.vm2.addresses[self.network.name][1].addr,
                self.sshvm.addresses[self.network.name][1].addr,
                self.vm2.addresses[self.network.name][0].addr))
        self.sctp_darn_client_stdout = stdout.read().decode("utf-8")
        self.sctp_darn_client_stderr = stderr.read().decode("utf-8")
        self.logger.info(
            "sctp_darn client stdout: %s", self.sctp_darn_client_stdout)
        self.logger.info(
            "sctp_darn client stderr: %s", self.sctp_darn_client_stderr)
        if "Recieved SCTP_COMM_UP" in self.sctp_darn_client_stdout:
            exit_code = 0
        return exit_code

    def clean(self):
        assert self.cloud
        if self.fip2:
            self.cloud.delete_floating_ip(self.fip2.id)
        if self.vm2:
            self.cloud.delete_server(
                self.vm2, wait=True,
                timeout=getattr(config.CONF, 'vping_vm_delete_timeout'),
                delete_ips=True)
        if self.sshvm:
            self.cloud.delete_server(
                self.sshvm, wait=True,
                timeout=getattr(config.CONF, 'vping_vm_delete_timeout'),
                delete_ips=True)
        if self.subnet2:
            self.cloud.delete_subnet(self.subnet2.id)
        if self.network2:
            self.cloud.delete_network(self.network2.id)
        super().clean()
