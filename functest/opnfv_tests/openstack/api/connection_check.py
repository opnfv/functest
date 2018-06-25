#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Verify the connection to OpenStack Services"""

import logging
import time

import os_client_config
import shade
from xtesting.core import testcase


class ConnectionCheck(testcase.TestCase):
    """Perform simplest queries"""
    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'connection_check'
        super(ConnectionCheck, self).__init__(**kwargs)
        try:
            cloud_config = os_client_config.get_config()
            self.cloud = shade.OpenStackCloud(cloud_config=cloud_config)
        except Exception:  # pylint: disable=broad-except
            self.cloud = None

    def run(self, **kwargs):
        """Run all read operations to check connections"""
        status = testcase.TestCase.EX_RUN_ERROR
        try:
            assert self.cloud
            self.start_time = time.time()
            for func in ["list_aggregates", "list_domains", "list_endpoints",
                         "list_floating_ip_pools", "list_floating_ips",
                         "list_hypervisors", "list_keypairs", "list_networks",
                         "list_ports", "list_role_assignments", "list_roles",
                         "list_routers", "list_servers", "list_services",
                         "list_subnets", "list_zones"]:
                self.__logger.debug(
                    "%s: %s", func, getattr(self.cloud, func)())
            self.result = 100
            status = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception('Cannot run %s', self.case_name)
        finally:
            self.stop_time = time.time()
        return status
