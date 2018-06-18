#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Ease deploying a single VM reachable via ssh

It offers a simple way to create all tenant network ressources + a VM for
advanced testcases (e.g. deploying an orchestrator).
"""

import logging
import tempfile
import time

import paramiko
from xtesting.core import testcase

from functest.core import tenantnetwork
from functest.utils import config


class SingleVm(tenantnetwork.TenantNetwork1):
    """Deploy a single VM reachable via ssh

    It inherits from TenantNetwork1 which creates all network resources and
    completes it by booting a VM attached to that network.
    """
    # pylint: disable=too-many-instance-attributes

    __logger = logging.getLogger(__name__)
    filename = '/home/opnfv/functest/images/cirros-0.4.0-x86_64-disk.img'
    flavor_ram = 1024
    flavor_vcpus = 1
    flavor_disk = 1
    username = 'cirros'
    ssh_connect_timeout = 60

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'tenantnetwork'
        super(SingleVm, self).__init__(**kwargs)
        self.image = None
        self.sshvm = None
        self.flavor = None
        self.sec = None
        self.fip = None
        self.keypair = None
        self.ssh = paramiko.SSHClient()
        (_, self.key_filename) = tempfile.mkstemp()

    def _publish_image(self):
        assert self.cloud
        meta = getattr(
            config.CONF, '{}_extra_properties'.format(self.case_name), None)
        self.image = self.cloud.create_image(
            '{}-img_{}'.format(self.case_name, self.guid),
            filename=getattr(
                config.CONF, '{}_image'.format(self.case_name),
                self.filename),
            meta=meta)
        self.__logger.debug("image: %s", self.image)

    def create_sg_rules(self):
        """Create the security group

        It can be overriden to set other rules according to the services
        running in the VM

        Raises: Exception on error
        """
        assert self.cloud
        self.sec = self.cloud.create_security_group(
            '{}-sg_{}'.format(self.case_name, self.guid),
            'created by OPNFV Functest ({})'.format(self.case_name))
        self.cloud.create_security_group_rule(
            self.sec.id, port_range_min='22', port_range_max='22',
            protocol='tcp', direction='ingress')
        self.cloud.create_security_group_rule(
            self.sec.id, protocol='icmp', direction='ingress')

    def _boot_vm(self):
        assert self.cloud
        self.flavor = self.cloud.create_flavor(
            '{}-flavor_{}'.format(self.case_name, self.guid),
            getattr(config.CONF, '{}_flavor_ram'.format(self.case_name),
                    self.flavor_ram),
            getattr(config.CONF, '{}_flavor_vcpus'.format(self.case_name),
                    self.flavor_vcpus),
            getattr(config.CONF, '{}_flavor_disk'.format(self.case_name),
                    self.flavor_disk))
        self.__logger.debug("flavor: %s", self.flavor)
        self.cloud.set_flavor_specs(
            self.flavor.id, getattr(config.CONF, 'flavor_extra_specs', {}))

        self.keypair = self.cloud.create_keypair(
            '{}-kp_{}'.format(self.case_name, self.guid))
        self.__logger.debug("keypair: %s", self.keypair)
        self.__logger.debug("private_key: %s", self.keypair.private_key)
        with open(self.key_filename, 'w') as private_key_file:
            private_key_file.write(self.keypair.private_key)

        self.sshvm = self.cloud.create_server(
            '{}-vm_{}'.format(self.case_name, self.guid),
            image=self.image.id, flavor=self.flavor.id,
            key_name=self.keypair.id,
            auto_ip=False, wait=True,
            network=self.network.id,
            security_groups=[self.sec.id])
        self.__logger.debug("vm: %s", self.sshvm)
        self.fip = self.cloud.create_floating_ip(
            network=self.ext_net.id, server=self.sshvm)
        self.__logger.debug("floating_ip: %s", self.fip)
        self.sshvm = self.cloud.wait_for_server(self.sshvm, auto_ip=False)

    def _connect(self):
        p_console = self.cloud.get_server_console(self.sshvm.id)
        self.__logger.debug("vm console: \n%s", p_console)
        self.ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        for loop in range(6):
            try:
                self.ssh.connect(
                    self.sshvm.public_v4,
                    username=getattr(
                        config.CONF,
                        '{}_image_user'.format(self.case_name), self.username),
                    key_filename=self.key_filename,
                    timeout=getattr(
                        config.CONF,
                        '{}_vm_ssh_connect_timeout'.format(self.case_name),
                        self.ssh_connect_timeout))
                break
            except Exception:  # pylint: disable=broad-except
                self.__logger.info(
                    "try %s: cannot connect to %s", loop + 1,
                    self.sshvm.public_v4)
                time.sleep(10)
        else:
            self.__logger.error("cannot connect to %s", self.sshvm.public_v4)
            return False
        return True

    def execute(self):
        """Say hello world via ssh

        It can be overriden to execute any command.

        Returns: echo exit codes
        """
        (_, stdout, _) = self.ssh.exec_command('echo Hello World')
        self.__logger.info("output:\n%s", stdout.read())
        return stdout.channel.recv_exit_status()

    def run(self, **kwargs):
        """Boot the new VM

        Here are the main actions:
        - publish the image
        - add a new ssh key
        - boot the VM
        - create the security group
        - execute the right command over ssh

        Returns:
        - TestCase.EX_OK
        - TestCase.EX_RUN_ERROR on error
        """
        status = testcase.TestCase.EX_RUN_ERROR
        try:
            assert self.cloud
            super(SingleVm, self).run(**kwargs)
            self.result = 0
            self._publish_image()
            self.create_sg_rules()
            self._boot_vm()
            assert self._connect()
            if not self.execute():
                self.result = 100
                status = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception('Cannot run %s', self.case_name)
        finally:
            self.stop_time = time.time()
        return status

    def clean(self):
        try:
            assert self.cloud
            self.cloud.delete_server(self.sshvm, wait=True)
            self.cloud.delete_security_group(self.sec.id)
            self.cloud.delete_image(self.image)
            self.cloud.delete_flavor(self.flavor.id)
            self.cloud.delete_keypair(self.keypair.id)
            self.cloud.delete_floating_ip(self.fip.id)
            self.cloud.delete_image(self.image)
        except Exception:  # pylint: disable=broad-except
            pass
