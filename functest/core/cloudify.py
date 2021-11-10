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
import os
import time
import traceback

from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.executions import Execution
import scp

from functest.core import singlevm


class Cloudify(singlevm.SingleVm2):
    """Cloudify Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    filename = ('/home/opnfv/functest/images/'
                'ubuntu-16.04-server-cloudimg-amd64-disk1.img')
    flavor_ram = 4096
    flavor_vcpus = 2
    flavor_disk = 40
    username = 'ubuntu'
    ssh_connect_loops = 12
    create_server_timeout = 600
    ports = [80, 443, 5671, 53333]

    cloudify_archive = ('/home/opnfv/functest/images/'
                        'cloudify-docker-manager-community-19.01.24.tar')
    cloudify_container = "docker-cfy-manager:latest"

    def __init__(self, **kwargs):
        """Initialize Cloudify testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cloudify"
        super().__init__(**kwargs)
        self.cfy_client = None

    def prepare(self):
        super().prepare()
        for port in self.ports:
            self.cloud.create_security_group_rule(
                self.sec.id, port_range_min=port, port_range_max=port,
                protocol='tcp', direction='ingress')

    def execute(self):
        """
        Deploy Cloudify Manager.
        """
        scpc = scp.SCPClient(self.ssh.get_transport())
        scpc.put(self.cloudify_archive,
                 remote_path=os.path.basename(self.cloudify_archive))
        (_, stdout, stderr) = self.ssh.exec_command(
            "sudo wget https://get.docker.com/ -O script.sh && "
            "sudo chmod +x script.sh && "
            "sudo ./script.sh && "
            "sudo docker load -i "
            f"~/{os.path.basename(self.cloudify_archive)} && "
            "sudo docker run --name cfy_manager_local -d "
            "--restart unless-stopped -v /sys/fs/cgroup:/sys/fs/cgroup:ro "
            "--tmpfs /run --tmpfs /run/lock --security-opt seccomp:unconfined "
            f"--cap-add SYS_ADMIN --network=host {self.cloudify_container}")
        self.__logger.debug("output:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("error:\n%s", stderr.read().decode("utf-8"))
        self.cfy_client = CloudifyClient(
            host=self.fip.floating_ip_address if self.fip else (
                self.sshvm.public_v4),
            username='admin', password='admin', tenant='default_tenant')
        self.__logger.info("Attemps running status of the Manager")
        secret_key = "foo"
        secret_value = "bar"
        for loop in range(20):
            try:
                self.__logger.debug(
                    "status %s", self.cfy_client.manager.get_status())
                cfy_status = self.cfy_client.manager.get_status()['status']
                self.__logger.info(
                    "The current manager status is %s", cfy_status)
                if str(cfy_status) != 'running':
                    raise Exception("Cloudify Manager isn't up and running")
                for secret in iter(self.cfy_client.secrets.list()):
                    if secret_key == secret["key"]:
                        self.__logger.debug("Updating secrets: %s", secret_key)
                        self.cfy_client.secrets.update(
                            secret_key, secret_value)
                        break
                else:
                    self.__logger.debug("Creating secrets: %s", secret_key)
                    self.cfy_client.secrets.create(secret_key, secret_value)
                self.cfy_client.secrets.delete(secret_key)
                self.__logger.info("Secrets API successfully reached")
                break
            except Exception:  # pylint: disable=broad-except
                self.__logger.debug(
                    "try %s: Cloudify Manager isn't up and running \n%s",
                    loop + 1, traceback.format_exc())
                time.sleep(30)
        else:
            self.__logger.error("Cloudify Manager isn't up and running")
            return 1
        self.__logger.info("Cloudify Manager is up and running")
        return 0

    def put_private_key(self):
        """Put private keypair in manager"""
        self.__logger.info("Put private keypair in manager")
        scpc = scp.SCPClient(self.ssh.get_transport())
        scpc.put(self.key_filename, remote_path='~/cloudify_ims.pem')
        (_, stdout, stderr) = self.ssh.exec_command(
            "sudo docker cp ~/cloudify_ims.pem "
            "cfy_manager_local:/etc/cloudify/ && "
            "sudo docker exec cfy_manager_local "
            "chmod 444 /etc/cloudify/cloudify_ims.pem")
        self.__logger.debug("output:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("error:\n%s", stderr.read().decode("utf-8"))

    def upload_cfy_plugins(self, yaml, wgn):
        """Upload Cloudify plugins"""
        (_, stdout, stderr) = self.ssh.exec_command(
            "sudo docker exec cfy_manager_local "
            f"cfy plugins upload -y {yaml} {wgn} && "
            "sudo docker exec cfy_manager_local cfy status")
        self.__logger.debug("output:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("error:\n%s", stderr.read().decode("utf-8"))

    def kill_existing_execution(self, dep_name):
        """kill existing execution"""
        try:
            self.__logger.info('Deleting the current deployment')
            exec_list = self.cfy_client.executions.list()
            for execution in exec_list:
                if execution['status'] == "started":
                    try:
                        self.cfy_client.executions.cancel(
                            execution['id'], force=True)
                    except Exception:  # pylint: disable=broad-except
                        self.__logger.warning("Can't cancel the current exec")
            execution = self.cfy_client.executions.start(
                dep_name, 'uninstall', parameters=dict(ignore_failure=True))
            wait_for_execution(self.cfy_client, execution, self.__logger)
            self.cfy_client.deployments.delete(dep_name)
            time.sleep(10)
            self.cfy_client.blueprints.delete(dep_name)
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Some issue during the undeployment ..")


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
                    'execution of operation {execution.workflow_id} for '
                    'deployment {execution.deployment_id} timed out')
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
                       f'Available executions: {executions}')
