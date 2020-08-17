#!/usr/bin/env python

# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""vPingSSH testcase."""

import logging

from functest.core import singlevm
from functest.utils import config


class VPingSSH(singlevm.SingleVm2):
    """
    VPingSSH testcase implementation.

    Class to execute the vPing test using a Floating IP to connect to one VM
    to issue the ping command to the second
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        """Initialize testcase."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "vping_ssh"
        super(VPingSSH, self).__init__(**kwargs)
        self.vm2 = None

    def prepare(self):
        super(VPingSSH, self).prepare()
        self.vm2 = self.boot_vm(
            '{}-vm2_{}'.format(self.case_name, self.guid),
            security_groups=[self.sec.id])

    def execute(self):
        """Ping the second VM

        Returns: ping exit codes
        """
        assert self.ssh
        if not self.check_regex_in_console(self.vm2.name):
            return 1
        (_, stdout, stderr) = self.ssh.exec_command(
            'ping -c 1 {}'.format(
                self.vm2.private_v4 or self.vm2.addresses[
                    self.network.name][0].addr))
        self.__logger.info("output:\n%s", stdout.read().decode("utf-8"))
        self.__logger.info("error:\n%s", stderr.read().decode("utf-8"))
        return stdout.channel.recv_exit_status()

    def clean(self):
        assert self.cloud
        if self.vm2:
            self.cloud.delete_server(
                self.vm2, wait=True,
                timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        super(VPingSSH, self).clean()
