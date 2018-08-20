#!/usr/bin/env python

# Copyright (c) 2018 Intracom Telecom and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import re

import os_client_config
import paramiko
import shade
from six.moves import configparser

from functest.opnfv_tests.openstack.tempest import tempest


class IntelNfvCi(tempest.TempestCommon):

    __logger = logging.getLogger(__name__)
    qemu_ssh_user = 'ubuntu'
    qemu_ssh_private_key_path = '/root/.ssh/id_rsa'

    def configure(self, **kwargs):
        super(IntelNfvCi, self).configure(**kwargs)
        rconfig = configparser.RawConfigParser()
        rconfig.read(self.conf_file)
        rconfig.add_section('intel_nfv_ci')
        rconfig.set('intel_nfv_ci', 'qemu_ssh_user',
                    kwargs.get('qemu_ssh_user', self.qemu_ssh_user))
        rconfig.set('intel_nfv_ci', 'qemu_ssh_private_key_path',
                    kwargs.get('qemu_ssh_private_key_path',
                               self.qemu_ssh_private_key_path))
        with open(self.conf_file, 'wb') as config_file:
            rconfig.write(config_file)
        self.backup_tempest_config(self.conf_file, self.res_dir)

    def is_numa_enabled(self, node):
        cmd = 'ls /sys/devices/system/node | grep -Po "node[0-9]+" | wc -l'
        (_, stdout, _) = node.exec_command(cmd)
        try:
            return int(stdout.read()) > 1
        except ValueError:
            return False

    def has_hyperthreading_enabled(self, node):
        cmd = 'cat /sys/devices/system/cpu/cpu0/topology/thread_siblings_list'
        (_, stdout, _) = node.exec_command(cmd)
        return bool(re.match(r'0-[0-9]+\n', stdout.read()))

    def has_hugepages_enabled(self, node):
        cmd = "cat /proc/meminfo | grep HugePages_Total | awk '{print $2}'"
        (_, stdout, _) = node.exec_command(cmd)
        try:
            return int(stdout.read()) > 0
        except ValueError:
            return False

    def check_requirements(self):
        try:
            cloud_config = os_client_config.get_config()
            cloud = shade.OpenStackCloud(cloud_config=cloud_config)
            for hypervisor in cloud.list_hypervisors():
                node_ip = hypervisor.host_ip
                ssh_session = paramiko.SSHClient()
                ssh_session.set_missing_host_key_policy(paramiko.client.
                                                        AutoAddPolicy())
                ssh_session.connect(node_ip, username=self.qemu_ssh_user)
                if (
                    not self.is_numa_enabled(ssh_session) or
                    not self.has_hyperthreading_enabled(ssh_session) or
                    not self.has_hugepages_enabled(ssh_session)
                ):
                    self.is_skipped = True
                ssh_session.close()
        except Exception:  # pylint: disable=broad-except
            pass
