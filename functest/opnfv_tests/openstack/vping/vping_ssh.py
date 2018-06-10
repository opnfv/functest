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
        (_, stdout, _) = self.ssh.exec_command(
            'ping -c 1 ' + self.vm2.private_v4)
        self.__logger.debug("output:\n%s", stdout.read())
        return stdout.channel.recv_exit_status()

    def clean(self):
        assert self.cloud
        self.cloud.delete_server(
            self.vm2, wait=True,
            timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        super(VPingSSH, self).clean()
