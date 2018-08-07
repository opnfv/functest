#!/usr/bin/env python

# Copyright (c) 2018 Kontron and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""vGPU testcase implementation."""

from __future__ import division

import logging

from functest.core import singlevm


class vGPU(singlevm.SingleVm2):
    """vGPU Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    filename = ('/home/opnfv/functest/images/'
                'ubuntu-16.04-server-cloudimg-amd64-disk1.img')
    flavor_ram = 4096
    flavor_vcpus = 2
    flavor_disk = 40
    flavor_extra_specs = {'resources:VGPU': '1'}
    username = 'ubuntu'
    ssh_connect_loops = 12
    create_server_timeout = 300

    def __init__(self, **kwargs):
        """Initialize Cloudify testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "vgpu"
        super(vGPU, self).__init__(**kwargs)

    def execute(self):
        """
        Test if the vGPU exist.
        """
        (_, stdout, stderr) = self.ssh.exec_command('lspci')
        lspci_output = stdout.read()
        self.__logger.debug("output:\n%s", stdout.read())
        self.__logger.debug("error:\n%s", stderr.read())
        if 'VGA compatible controller: Intel' in lspci_output or \
                'VGA compatible controller: Nvidia' in lspci_output:
            self.__logger.info("The VM have a vGPU")
            return 0
        else:
            self.__logger.error("The VM haven't any vGPU")
            return 1
