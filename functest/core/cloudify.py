#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Cloudify testcase implementation."""

from __future__ import division

import logging
import time

from cloudify_rest_client import CloudifyClient

from functest.core import singlevm


class Cloudify(singlevm.SingleVm2):
    """Cloudify Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    filename = ('/home/opnfv/functest/images/'
                'cloudify-manager-premium-4.0.1.qcow2')
    flavor_ram = 4096
    flavor_vcpus = 2
    flavor_disk = 50
    username = 'centos'
    ssh_connect_loops = 12
    port = 80

    def __init__(self, **kwargs):
        """Initialize Cloudify testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cloudify"
        super(Cloudify, self).__init__(**kwargs)
        self.cfy_client = None

    def prepare(self):
        super(Cloudify, self).prepare()
        self.cloud.create_security_group_rule(
            self.sec.id, port_range_min=self.port, port_range_max=self.port,
            protocol='tcp', direction='ingress')

    def execute(self):
        """
        Deploy Cloudify Manager.
        """
        self.cfy_client = CloudifyClient(
            host=self.fip.floating_ip_address,
            username='admin', password='admin', tenant='default_tenant',
            api_version='v3')
        self.__logger.info("Attemps running status of the Manager")
        for loop in range(10):
            try:
                self.__logger.debug(
                    "status %s", self.cfy_client.manager.get_status())
                cfy_status = self.cfy_client.manager.get_status()['status']
                self.__logger.info(
                    "The current manager status is %s", cfy_status)
                if str(cfy_status) != 'running':
                    raise Exception("Cloudify Manager isn't up and running")
                break
            except Exception:  # pylint: disable=broad-except
                self.__logger.info(
                    "try %s: Cloudify Manager isn't up and running", loop + 1)
                time.sleep(30)
        else:
            self.__logger.error("Cloudify Manager isn't up and running")
            return 1
        self.__logger.info("Cloudify Manager is up and running")
        return 0
