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
from cloudify_rest_client.executions import Execution

from functest.core import singlevm


class Cloudify(singlevm.SingleVm2):
    """Cloudify Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    filename = ('/home/opnfv/functest/images/'
                'cloudify-manager-premium-4.0.1.qcow2')
    flavor_ram = 4096
    flavor_vcpus = 2
    flavor_disk = 40
    username = 'centos'
    ssh_connect_loops = 12
    create_server_timeout = 600
    ports = [80, 443, 5671, 53333]

    def __init__(self, **kwargs):
        """Initialize Cloudify testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cloudify"
        super(Cloudify, self).__init__(**kwargs)
        self.cfy_client = None

    def prepare(self):
        super(Cloudify, self).prepare()
        for port in self.ports:
            self.cloud.create_security_group_rule(
                self.sec.id, port_range_min=port, port_range_max=port,
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
                self.cfy_client.secrets.create(
                    "foo", "bar", update_if_exists=True)
                self.__logger.debug(
                    "List secrets: %s", self.cfy_client.secrets.list())
                self.cfy_client.secrets.delete("foo")
                self.__logger.info("Secrets API successfully reached")
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


def wait_for_execution(client, execution, logger, timeout=3600, ):
    """Wait for a workflow execution on Cloudify Manager."""
    # if execution already ended - return without waiting
    if execution.status in Execution.END_STATES:
        return execution

    if timeout is not None:
        deadline = time.time() + timeout

    # Poll for execution status and execution logs, until execution ends
    # and we receive an event of type in WORKFLOW_END_TYPES
    offset = 0
    batch_size = 50
    event_list = []
    execution_ended = False
    while True:
        event_list = client.events.list(
            execution_id=execution.id,
            _offset=offset,
            _size=batch_size,
            include_logs=True,
            sort='@timestamp').items

        offset = offset + len(event_list)
        for event in event_list:
            logger.debug(event.get('message'))

        if timeout is not None:
            if time.time() > deadline:
                raise RuntimeError(
                    'execution of operation {0} for deployment {1} '
                    'timed out'.format(execution.workflow_id,
                                       execution.deployment_id))
            else:
                # update the remaining timeout
                timeout = deadline - time.time()

        if not execution_ended:
            execution = client.executions.get(execution.id)
            execution_ended = execution.status in Execution.END_STATES

        if execution_ended:
            break

        time.sleep(5)

    return execution


def get_execution_id(client, deployment_id):
    """
    Get the execution id of a env preparation.

    network, security group, fip, VM creation
    """
    executions = client.executions.list(deployment_id=deployment_id)
    for execution in executions:
        if execution.workflow_id == 'create_deployment_environment':
            return execution
    raise RuntimeError('Failed to get create_deployment_environment '
                       'workflow execution.'
                       'Available executions: {0}'.format(executions))
