#!/usr/bin/env python

# Copyright (c) 2018 Enea AB and others

# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""CinderCheck testcase."""

import logging

import pkg_resources
from scp import SCPClient
from xtesting.core import testcase

from functest.core import singlevm
from functest.utils import config
from functest.utils import env


class CinderCheck(singlevm.SingleVm2):
    """
    CinderCheck testcase implementation.

    Class to execute the CinderCheck test using 2 Floating IPs
    to connect to the VMs and one data volume
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, **kwargs):
        """Initialize testcase."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cinder_test"
        super(CinderCheck, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.vm2 = None
        self.fip2 = None
        self.ssh2 = None
        self.volume = None

    def execute(self):
        """Execute CinderCheck testcase.

        Sets up the OpenStack keypair, router, security group, and VM instance
        objects then validates cinder.
        :return: the exit code from the super.execute() method
        """
        return self._write_data() or self._read_data()

    def prepare(self):
        super(CinderCheck, self).prepare()
        self.vm2 = self.boot_vm(
            '{}-vm2_{}'.format(self.case_name, self.guid),
            key_name=self.keypair.id,
            security_groups=[self.sec.id])
        (self.fip2, self.ssh2) = self.connect(self.vm2)
        self.volume = self.cloud.create_volume(
            name='{}-volume_{}'.format(self.case_name, self.guid), size='2')

    def _write_data(self):
        assert self.cloud
        self.cloud.attach_volume(self.sshvm, self.volume)
        write_data_script = pkg_resources.resource_filename(
            'functest.opnfv_tests.openstack.cinder', 'write_data.sh')
        try:
            scp = SCPClient(self.ssh.get_transport())
            scp.put(write_data_script, remote_path="~/")
        except Exception:  # pylint: disable=broad-except
            self.logger.error("File not transfered!")
            return testcase.TestCase.EX_RUN_ERROR
        self.logger.debug("ssh: %s", self.ssh)
        (_, stdout, stderr) = self.ssh.exec_command(
            "sh ~/write_data.sh {}".format(env.get('VOLUME_DEVICE_NAME')))
        self.logger.debug("volume_write stdout: %s", stdout.read())
        self.logger.debug("volume_write stderr: %s", stderr.read())
        # Detach volume from VM 1
        self.logger.info("Detach volume from VM 1")
        self.cloud.detach_volume(self.sshvm, self.volume)
        return stdout.channel.recv_exit_status()

    def _read_data(self):
        assert self.cloud
        # Attach volume to VM 2
        self.logger.info("Attach volume to VM 2")
        self.cloud.attach_volume(self.vm2, self.volume)
        # Check volume data
        read_data_script = pkg_resources.resource_filename(
            'functest.opnfv_tests.openstack.cinder', 'read_data.sh')
        try:
            scp = SCPClient(self.ssh2.get_transport())
            scp.put(read_data_script, remote_path="~/")
        except Exception:  # pylint: disable=broad-except
            self.logger.error("File not transfered!")
            return testcase.TestCase.EX_RUN_ERROR
        self.logger.debug("ssh: %s", self.ssh2)
        (_, stdout, stderr) = self.ssh2.exec_command(
            "sh ~/read_data.sh {}".format(env.get('VOLUME_DEVICE_NAME')))
        self.logger.debug("read volume stdout: %s", stdout.read())
        self.logger.debug("read volume stderr: %s", stderr.read())
        self.logger.info("Detach volume from VM 2")
        self.cloud.detach_volume(self.vm2, self.volume)
        return stdout.channel.recv_exit_status()

    def clean(self):
        assert self.cloud
        self.cloud.delete_server(
            self.vm2, wait=True,
            timeout=getattr(config.CONF, 'vping_vm_delete_timeout'))
        self.cloud.delete_floating_ip(self.fip2.id)
        self.cloud.delete_volume(self.volume.id)
        super(CinderCheck, self).clean()
