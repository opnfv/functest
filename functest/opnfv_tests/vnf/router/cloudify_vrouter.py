#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

"""vrouter testcase implementation."""

import logging
import os
import time
import uuid

from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.executions import Execution
from scp import SCPClient
import six
from snaps.config.flavor import FlavorConfig
from snaps.config.image import ImageConfig
from snaps.config.keypair import KeypairConfig
from snaps.config.network import NetworkConfig, PortConfig, SubnetConfig
from snaps.config.router import RouterConfig
from snaps.config.security_group import (
    Direction, Protocol, SecurityGroupConfig, SecurityGroupRuleConfig)
from snaps.config.user import UserConfig
from snaps.config.vm_inst import FloatingIpConfig, VmInstanceConfig
from snaps.openstack.create_flavor import OpenStackFlavor
from snaps.openstack.create_image import OpenStackImage
from snaps.openstack.create_instance import OpenStackVmInstance
from snaps.openstack.create_keypairs import OpenStackKeypair
from snaps.openstack.create_network import OpenStackNetwork
from snaps.openstack.create_security_group import OpenStackSecurityGroup
from snaps.openstack.create_router import OpenStackRouter
from snaps.openstack.create_user import OpenStackUser
import snaps.openstack.utils.glance_utils as glance_utils
from snaps.openstack.utils import keystone_utils

from functest.core import singlevm
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.opnfv_tests.vnf.router import vrouter_base
from functest.opnfv_tests.vnf.router.utilvnf import Utilvnf
from functest.utils import config
from functest.utils import env
from functest.utils import functest_utils

__author__ = "Shuya Nakama <shuya.nakama@okinawaopenlabs.org>"


class CloudifyVrouter(singlevm.SingleVm2):
    # pylint: disable=too-many-instance-attributes
    """vrouter testcase deployed with Cloudify Orchestrator."""

    __logger = logging.getLogger(__name__)
    name = __name__

    filename = '/home/opnfv/functest/images/cloudify-manager-premium-4.0.1.qcow2'
    flavor_ram = 4096
    flavor_vcpus = 2
    flavor_disk = 50

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "vyos_vrouter"
        super(CloudifyVrouter, self).__init__(**kwargs)
        vyos = vrouter_base.VrouterOnBoardingBase(case_name)

        # Retrieve the configuration
        try:
            self.config = getattr(
                config.CONF, 'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")

        self.cfy_manager_ip = ''
        self.deployment_name = ''

        config_file = os.path.join(self.case_dir, self.config)
        self.orchestrator = dict(
            requirements=functest_utils.get_parameter_from_yaml(
                "orchestrator.requirements", config_file),
        )
        self.details['orchestrator'] = dict(
            name=functest_utils.get_parameter_from_yaml(
                "orchestrator.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "orchestrator.version", config_file),
            status='ERROR',
            result=''
        )
        self.__logger.debug("Orchestrator configuration %s", self.orchestrator)
        self.__logger.debug("name = %s", self.name)
        self.vnf = dict(
            descriptor=functest_utils.get_parameter_from_yaml(
                "vnf.descriptor", config_file),
            inputs=functest_utils.get_parameter_from_yaml(
                "vnf.inputs", config_file),
            requirements=functest_utils.get_parameter_from_yaml(
                "vnf.requirements", config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=functest_utils.get_parameter_from_yaml(
                "vnf.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "vnf.version", config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)

        self.util = Utilvnf()

        self.details['test_vnf'] = dict(
            name=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.version", config_file)
        )
        self.images = functest_utils.get_parameter_from_yaml(
            "tenant_images", config_file)
        self.__logger.info("Images needed for vrouter: %s", self.images)

    @staticmethod
    def run_blocking_ssh_command(ssh, cmd,
                                 error_msg="Unable to run this command"):
        """Command to run ssh command with the exit status."""
        (_, stdout, stderr) = ssh.exec_command(cmd)
        CloudifyVrouter.__logger.debug("SSH %s stdout: %s", cmd, stdout.read())
        if stdout.channel.recv_exit_status() != 0:
            CloudifyVrouter.__logger.error(
                "SSH %s stderr: %s", cmd, stderr.read())
            raise Exception(error_msg)

    def create_sg_rules(self):
        """
        It adds one security group rule allowing ingress 9000/tcp

        Raises: Exception on error.
        """
        assert self.orig_cloud
        super(Shaker, self).create_sg_rules()
        self.orig_cloud.create_security_group_rule(
            self.sec.id, port_range_min=1, port_range_max=65535,
            protocol='tcp', direction='ingress')
        self.orig_cloud.create_security_group_rule(
            self.sec.id, port_range_min=1, port_range_max=65535,
            protocol='udp', direction='ingress')

    def prepare(self):
        super(CloudifyVrouter, self).prepare()
        self.__logger.info("Additional pre-configuration steps")
        self.util.set_credentials(self.snaps_creds)

    def deploy_orchestrator(self):
        # pylint: disable=too-many-locals,too-many-statements
        """
        Deploy Cloudify Manager.
        network, security group, fip, VM creation
        """
        # network creation
        start_time = time.time()

        self.__logger.info("Upload some OS images if it doesn't exist")
        for image_name, image_file in six.iteritems(self.images):
            self.__logger.info("image: %s, file: %s", image_name, image_file)
            if image_file and image_name:
                image_creator = OpenStackImage(
                    snaps_creds,
                    ImageConfig(
                        name=image_name, image_user='cloud',
                        img_format='qcow2', image_file=image_file))
                image_creator.create()
                self.created_object.append(image_creator)

        cfy_client = CloudifyClient(
            host=manager_creator.get_floating_ip().ip,
            username='admin', password='admin', tenant='default_tenant',
            api_version='v3')

        self.orchestrator['object'] = cfy_client

        self.cfy_manager_ip = manager_creator.get_floating_ip().ip

        self.__logger.info("Attemps running status of the Manager")
        for loop in range(10):
            try:
                self.__logger.debug(
                    "status %s", cfy_client.manager.get_status())
                cfy_status = cfy_client.manager.get_status()['status']
                self.__logger.info(
                    "The current manager status is %s", cfy_status)
                if str(cfy_status) != 'running':
                    raise Exception("Cloudify Manager isn't up and running")
                break
            except Exception:  # pylint: disable=broad-except
                self.logger.info(
                    "try %s: Cloudify Manager isn't up and running", loop + 1)
                time.sleep(30)
        else:
            self.logger.error("Cloudify Manager isn't up and running")
            return False

        duration = time.time() - start_time

        self.__logger.info("Put private keypair in manager")
        if manager_creator.vm_ssh_active(block=True):
            ssh = manager_creator.ssh_client()
            scp = SCPClient(ssh.get_transport(), socket_timeout=15.0)
            scp.put(kp_file, '~/')
            cmd = "sudo cp ~/cloudify_vrouter.pem /etc/cloudify/"
            self.run_blocking_ssh_command(ssh, cmd)
            cmd = "sudo chmod 444 /etc/cloudify/cloudify_vrouter.pem"
            self.run_blocking_ssh_command(ssh, cmd)
            # cmd2 is badly unpinned by Cloudify
            cmd = "sudo yum install -y gcc python-devel python-cmd2"
            self.run_blocking_ssh_command(
                ssh, cmd, "Unable to install packages on manager")
        else:
            self.__logger.error("Cannot connect to manager")
            return False

        self.details['orchestrator'].update(status='PASS', duration=duration)

        self.__logger.info("Get or create flavor for vrouter")
        flavor_settings = FlavorConfig(
            name="{}-{}".format(
                self.vnf['requirements']['flavor']['name'],
                self.uuid),
            ram=self.vnf['requirements']['flavor']['ram_min'],
            disk=25, vcpus=1)
        flavor_creator = OpenStackFlavor(self.snaps_creds, flavor_settings)
        flavor = flavor_creator.create()
        self.created_object.append(flavor_creator)

        # set image name
        glance = glance_utils.glance_client(snaps_creds)
        image = glance_utils.get_image(glance, "vyos1.1.7")
        self.vnf['inputs'].update(dict(external_network_name=ext_net_name))
        self.vnf['inputs'].update(dict(target_vnf_image_id=image.id))
        self.vnf['inputs'].update(dict(reference_vnf_image_id=image.id))
        self.vnf['inputs'].update(dict(target_vnf_flavor_id=flavor.id))
        self.vnf['inputs'].update(dict(reference_vnf_flavor_id=flavor.id))
        self.vnf['inputs'].update(dict(
            keystone_username=snaps_creds.username))
        self.vnf['inputs'].update(dict(
            keystone_password=snaps_creds.password))
        self.vnf['inputs'].update(dict(
            keystone_tenant_name=snaps_creds.project_name))
        self.vnf['inputs'].update(dict(
            keystone_user_domain_name=snaps_creds.user_domain_name))
        self.vnf['inputs'].update(dict(
            keystone_project_domain_name=snaps_creds.project_domain_name))
        self.vnf['inputs'].update(dict(
            region=snaps_creds.region_name))
        self.vnf['inputs'].update(dict(
            keystone_url=keystone_utils.get_endpoint(
                snaps_creds, 'identity')))

        credentials = {"snaps_creds": snaps_creds}
        self.util_info = {"credentials": credentials,
                          "cfy": cfy_client,
                          "vnf_data_dir": self.util.vnf_data_dir}

        return True

    def deploy_vnf(self):
        start_time = time.time()

        self.__logger.info("Upload VNFD")
        cfy_client = self.orchestrator['object']
        descriptor = self.vnf['descriptor']
        self.deployment_name = descriptor.get('name')

        cfy_client.blueprints.upload(
            descriptor.get('file_name'), descriptor.get('name'))

        self.__logger.info("Create VNF Instance")
        cfy_client.deployments.create(
            descriptor.get('name'), descriptor.get('name'),
            self.vnf.get('inputs'))

        wait_for_execution(
            cfy_client, get_execution_id(cfy_client, descriptor.get('name')),
            self.__logger, timeout=7200)

        self.__logger.info("Start the VNF Instance deployment")
        execution = cfy_client.executions.start(descriptor.get('name'),
                                                'install')
        # Show execution log
        execution = wait_for_execution(cfy_client, execution, self.__logger)

        duration = time.time() - start_time

        self.__logger.info(execution)
        if execution.status == 'terminated':
            self.details['vnf'].update(status='PASS', duration=duration)
            result = True
        else:
            self.details['vnf'].update(status='FAIL', duration=duration)
            result = False
        return result

    def test_vnf(self):
        start_time = time.time()
        result, test_result_data = super(CloudifyVrouter, self).test_vnf()
        duration = time.time() - start_time
        if result:
            self.details['test_vnf'].update(
                status='PASS', result='OK', full_result=test_result_data,
                duration=duration)
        else:
            self.details['test_vnf'].update(
                status='FAIL', result='NG', full_result=test_result_data,
                duration=duration)
        return True

    def clean(self):
        try:
            cfy_client = self.orchestrator['object']
            dep_name = self.vnf['descriptor'].get('name')
            # kill existing execution
            self.__logger.info('Deleting the current deployment')
            exec_list = cfy_client.executions.list(dep_name)
            for execution in exec_list:
                if execution['status'] == "started":
                    try:
                        cfy_client.executions.cancel(
                            execution['id'], force=True)
                    except Exception:  # pylint: disable=broad-except
                        self.__logger.warn("Can't cancel the current exec")

            execution = cfy_client.executions.start(
                dep_name, 'uninstall', parameters=dict(ignore_failure=True))

            wait_for_execution(cfy_client, execution, self.__logger)
            cfy_client.deployments.delete(self.vnf['descriptor'].get('name'))
            cfy_client.blueprints.delete(self.vnf['descriptor'].get('name'))
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Some issue during the undeployment ..")

        super(CloudifyVrouter, self).clean()

    def get_vnf_info_list(self, target_vnf_name):
        return self.util.get_vnf_info_list(
            self.cfy_manager_ip, self.deployment_name, target_vnf_name)


def wait_for_execution(client, execution, logger, timeout=7200, ):
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
            execution_id=execution.id, _offset=offset, _size=batch_size,
            include_logs=True, sort='@timestamp').items

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
