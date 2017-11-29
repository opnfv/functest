#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""vrouter testcase implementation."""

import logging
import os
import time

from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.executions import Execution
from scp import SCPClient
import yaml

from functest.opnfv_tests.openstack.snaps import snaps_utils
import functest.opnfv_tests.vnf.router.vrouter_base as vrouter_base
from functest.utils.constants import CONST
import functest.utils.openstack_utils as os_utils

from git import Repo

from snaps.openstack.create_network import (NetworkSettings, SubnetSettings,
                                            OpenStackNetwork)
from snaps.openstack.create_security_group import (SecurityGroupSettings,
                                                   SecurityGroupRuleSettings,
                                                   Direction, Protocol,
                                                   OpenStackSecurityGroup)
from snaps.openstack.create_router import RouterSettings, OpenStackRouter
from snaps.openstack.create_instance import (VmInstanceSettings,
                                             FloatingIpSettings,
                                             OpenStackVmInstance)
from snaps.openstack.create_flavor import FlavorSettings, OpenStackFlavor
from snaps.openstack.create_image import ImageSettings, OpenStackImage
from snaps.openstack.create_keypairs import KeypairSettings, OpenStackKeypair
from snaps.openstack.create_network import PortSettings
import snaps.openstack.utils.glance_utils as glance_utils

from functest.opnfv_tests.vnf.router.utilvnf import Utilvnf

__author__ = "Shuya Nakama <shuya.nakama@okinawaopenlabs.org>"


class CloudifyVrouter(vrouter_base.VrouterOnBoardingBase):
    """vrouter testcase deployed with Cloudify Orchestrator."""

    __logger = logging.getLogger(__name__)
    name = __name__

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "vyos_vrouter"
        super(CloudifyVrouter, self).__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = CONST.__getattribute__(
                'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")

        self.snaps_creds = ''
        self.created_object = []

        self.cfy_manager_ip = ''
        self.util_info = {}
        self.deployment_name = ''

        config_file = os.path.join(self.case_dir, self.config)
        self.orchestrator = dict(
            requirements=get_config("orchestrator.requirements", config_file),
        )
        self.details['orchestrator'] = dict(
            name=get_config("orchestrator.name", config_file),
            version=get_config("orchestrator.version", config_file),
            status='ERROR',
            result=''
        )
        self.__logger.debug("Orchestrator configuration %s", self.orchestrator)
        self.__logger.debug("name = %s", self.name)
        self.vnf = dict(
            descriptor=get_config("vnf.descriptor", config_file),
            inputs=get_config("vnf.inputs", config_file),
            requirements=get_config("vnf.requirements", config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=get_config("vnf.name", config_file),
            version=get_config("vnf.version", config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)

        self.util = Utilvnf()

        self.details['test_vnf'] = dict(
            name=get_config("vnf_test_suite.name", config_file),
            version=get_config("vnf_test_suite.version", config_file)
        )
        self.images = get_config("tenant_images", config_file)
        self.__logger.info("Images needed for vrouter: %s", self.images)

    def prepare(self):
        super(CloudifyVrouter, self).prepare()

        self.__logger.info("Additional pre-configuration steps")

        self.util.set_credentials(self.snaps_creds.username,
                                  self.snaps_creds.password,
                                  self.snaps_creds.auth_url,
                                  self.snaps_creds.project_name)

        # needs some images
        self.__logger.info("Upload some OS images if it doesn't exist")
        for image_name, image_file in self.images.iteritems():
            self.__logger.info("image: %s, file: %s", image_name, image_file)
            if image_file and image_name:
                image_creator = OpenStackImage(
                    self.snaps_creds,
                    ImageSettings(name=image_name,
                                  image_user='cloud',
                                  img_format='qcow2',
                                  image_file=image_file))
                image_creator.create()
                self.created_object.append(image_creator)

    def deploy_orchestrator(self):
        """
        Deploy Cloudify Manager.
        network, security group, fip, VM creation
        """
        # network creation

        start_time = time.time()
        self.__logger.info("Creating keypair ...")
        kp_file = os.path.join(self.data_dir, "cloudify_vrouter.pem")
        keypair_settings = KeypairSettings(name='cloudify_vrouter_kp',
                                           private_filepath=kp_file)
        keypair_creator = OpenStackKeypair(self.snaps_creds, keypair_settings)
        keypair_creator.create()
        self.created_object.append(keypair_creator)

        self.__logger.info("Creating full network ...")
        subnet_settings = SubnetSettings(name='cloudify_vrouter_subnet',
                                         cidr='10.67.79.0/24')
        network_settings = NetworkSettings(name='cloudify_vrouter_network',
                                           subnet_settings=[subnet_settings])
        network_creator = OpenStackNetwork(self.snaps_creds, network_settings)
        network_creator.create()
        self.created_object.append(network_creator)
        ext_net_name = snaps_utils.get_ext_net_name(self.snaps_creds)
        router_creator = OpenStackRouter(
            self.snaps_creds,
            RouterSettings(
                name='cloudify_vrouter_router',
                external_gateway=ext_net_name,
                internal_subnets=[subnet_settings.name]))
        router_creator.create()
        self.created_object.append(router_creator)

        # security group creation
        self.__logger.info("Creating security group for cloudify manager vm")
        sg_rules = list()
        sg_rules.append(
            SecurityGroupRuleSettings(sec_grp_name="sg-cloudify-manager",
                                      direction=Direction.ingress,
                                      protocol=Protocol.tcp, port_range_min=1,
                                      port_range_max=65535))
        sg_rules.append(
            SecurityGroupRuleSettings(sec_grp_name="sg-cloudify-manager",
                                      direction=Direction.ingress,
                                      protocol=Protocol.udp, port_range_min=1,
                                      port_range_max=65535))

        security_group_creator = OpenStackSecurityGroup(
            self.snaps_creds,
            SecurityGroupSettings(
                name="sg-cloudify-manager",
                rule_settings=sg_rules))

        security_group_creator.create()
        self.created_object.append(security_group_creator)

        # orchestrator VM flavor
        self.__logger.info("Get or create flavor for cloudify manager vm ...")

        flavor_settings = FlavorSettings(
            name=self.orchestrator['requirements']['flavor']['name'],
            ram=self.orchestrator['requirements']['flavor']['ram_min'],
            disk=50,
            vcpus=2)
        flavor_creator = OpenStackFlavor(self.snaps_creds, flavor_settings)
        flavor_creator.create()
        self.created_object.append(flavor_creator)
        image_settings = ImageSettings(
            name=self.orchestrator['requirements']['os_image'],
            image_user='centos',
            exists=True)

        port_settings = PortSettings(name='cloudify_manager_port',
                                     network_name=network_settings.name)

        manager_settings = VmInstanceSettings(
            name='cloudify_manager',
            flavor=flavor_settings.name,
            port_settings=[port_settings],
            security_group_names=[
                security_group_creator.sec_grp_settings.name],
            floating_ip_settings=[FloatingIpSettings(
                name='cloudify_manager_fip',
                port_name=port_settings.name,
                router_name=router_creator.router_settings.name)])

        manager_creator = OpenStackVmInstance(self.snaps_creds,
                                              manager_settings,
                                              image_settings,
                                              keypair_settings)

        self.__logger.info("Creating cloudify manager VM")
        manager_creator.create()
        self.created_object.append(manager_creator)

        public_auth_url = os_utils.get_endpoint('identity')

        self.__logger.info("Set creds for cloudify manager")
        cfy_creds = dict(keystone_username=self.tenant_name,
                         keystone_password=self.tenant_name,
                         keystone_tenant_name=self.tenant_name,
                         keystone_url=public_auth_url)

        cfy_client = CloudifyClient(host=manager_creator.get_floating_ip().ip,
                                    username='admin',
                                    password='admin',
                                    tenant='default_tenant')

        self.orchestrator['object'] = cfy_client

        self.cfy_manager_ip = manager_creator.get_floating_ip().ip

        self.__logger.info("Attemps running status of the Manager")
        cfy_status = None
        retry = 10
        while str(cfy_status) != 'running' and retry:
            try:
                cfy_status = cfy_client.manager.get_status()['status']
                self.__logger.debug("The current manager status is %s",
                                    cfy_status)
            except Exception:  # pylint: disable=broad-except
                self.__logger.warning("Cloudify Manager isn't " +
                                      "up and running. Retrying ...")
            retry = retry - 1
            time.sleep(30)

        if str(cfy_status) == 'running':
            self.__logger.info("Cloudify Manager is up and running")
        else:
            raise Exception("Cloudify Manager isn't up and running")

        self.__logger.info("Put OpenStack creds in manager")
        secrets_list = cfy_client.secrets.list()
        for k, val in cfy_creds.iteritems():
            if not any(d.get('key', None) == k for d in secrets_list):
                cfy_client.secrets.create(k, val)
            else:
                cfy_client.secrets.update(k, val)

        duration = time.time() - start_time

        self.__logger.info("Put private keypair in manager")
        if manager_creator.vm_ssh_active(block=True):
            ssh = manager_creator.ssh_client()
            scp = SCPClient(ssh.get_transport(), socket_timeout=15.0)
            scp.put(kp_file, '~/')
            cmd = "sudo cp ~/cloudify_vrouter.pem /etc/cloudify/"
            run_blocking_ssh_command(ssh, cmd)
            cmd = "sudo chmod 444 /etc/cloudify/cloudify_vrouter.pem"
            run_blocking_ssh_command(ssh, cmd)
            cmd = "sudo yum install -y gcc python-devel"
            run_blocking_ssh_command(
                ssh, cmd, "Unable to install packages on manager")

        self.details['orchestrator'].update(status='PASS', duration=duration)

        self.vnf['inputs'].update(dict(external_network_name=ext_net_name))

        return True

    def deploy_vnf(self):
        start_time = time.time()

        self.__logger.info("Upload VNFD")
        cfy_client = self.orchestrator['object']
        descriptor = self.vnf['descriptor']
        self.deployment_name = descriptor.get('name')

        vrouter_blueprint_dir = os.path.join(self.data_dir,
                                             self.util.blueprint_dir)
        if not os.path.exists(vrouter_blueprint_dir):
            Repo.clone_from(descriptor.get('url'),
                            vrouter_blueprint_dir,
                            branch=descriptor.get('version'))

        cfy_client.blueprints.upload(vrouter_blueprint_dir +
                                     self.util.blueprint_file_name,
                                     descriptor.get('name'))

        self.__logger.info("Get or create flavor for vrouter")
        flavor_settings = FlavorSettings(
            name=self.vnf['requirements']['flavor']['name'],
            ram=self.vnf['requirements']['flavor']['ram_min'],
            disk=25,
            vcpus=1)
        flavor_creator = OpenStackFlavor(self.snaps_creds, flavor_settings)
        flavor = flavor_creator.create()
        self.created_object.append(flavor_creator)

        # set image name
        glance = glance_utils.glance_client(self.snaps_creds)
        image = glance_utils.get_image(glance,
                                       "vyos1.1.7")
        self.vnf['inputs'].update(dict(target_vnf_image_id=image.id))
        self.vnf['inputs'].update(dict(reference_vnf_image_id=image.id))

        # set flavor id
        self.vnf['inputs'].update(dict(target_vnf_flavor_id=flavor.id))
        self.vnf['inputs'].update(dict(reference_vnf_flavor_id=flavor.id))

        self.vnf['inputs'].update(dict(keystone_username=self.tenant_name))
        self.vnf['inputs'].update(dict(keystone_password=self.tenant_name))
        self.vnf['inputs'].update(dict(keystone_tenant_name=self.tenant_name))
        self.vnf['inputs'].update(
            dict(keystone_url=os_utils.get_endpoint('identity')))

        self.__logger.info("Create VNF Instance")
        cfy_client.deployments.create(descriptor.get('name'),
                                      descriptor.get('name'),
                                      self.vnf.get('inputs'))

        wait_for_execution(cfy_client,
                           get_execution_id(
                               cfy_client, descriptor.get('name')),
                           self.__logger,
                           timeout=7200)

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
        cfy_client = self.orchestrator['object']
        credentials = {"username": self.snaps_creds.username,
                       "password": self.snaps_creds.password,
                       "auth_url": self.snaps_creds.auth_url,
                       "tenant_name": self.snaps_creds.project_name}

        self.util_info = {"credentials": credentials,
                          "cfy": cfy_client,
                          "vnf_data_dir": self.util.vnf_data_dir}

        start_time = time.time()

        result, test_result_data = super(CloudifyVrouter, self).test_vnf()

        duration = time.time() - start_time

        if result:
            self.details['test_vnf'].update(status='PASS',
                                            result='OK',
                                            full_result=test_result_data,
                                            duration=duration)
        else:
            self.details['test_vnf'].update(status='FAIL',
                                            result='NG',
                                            full_result=test_result_data,
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
                        cfy_client.executions.cancel(execution['id'],
                                                     force=True)
                    except:  # pylint: disable=broad-except
                        self.__logger.warn("Can't cancel the current exec")

            execution = cfy_client.executions.start(
                dep_name,
                'uninstall',
                parameters=dict(ignore_failure=True))

            wait_for_execution(cfy_client, execution, self.__logger)
            cfy_client.deployments.delete(self.vnf['descriptor'].get('name'))
            cfy_client.blueprints.delete(self.vnf['descriptor'].get('name'))
        except:  # pylint: disable=broad-except
            self.__logger.warn("Some issue during the undeployment ..")
            self.__logger.warn("Tenant clean continue ..")

        self.__logger.info('Remove the cloudify manager OS object ..')
        for creator in reversed(self.created_object):
            try:
                creator.clean()
            except Exception as exc:
                self.logger.error('Unexpected error cleaning - %s', exc)

        super(CloudifyVrouter, self).clean()

    def run(self, **kwargs):
        """Execute CloudifyVrouter test case."""
        return super(CloudifyVrouter, self).run(**kwargs)

    def get_vnf_info_list(self, target_vnf_name):
        return self.util.get_vnf_info_list(self.cfy_manager_ip,
                                           self.deployment_name,
                                           target_vnf_name)


# ----------------------------------------------------------
#
#               YAML UTILS
#
# -----------------------------------------------------------
def get_config(parameter, file_path):
    """
    Get config parameter.
    Returns the value of a given parameter in file.yaml
    parameter must be given in string format with dots
    Example: general.openstack.image_name
    """
    with open(file_path) as config_file:
        file_yaml = yaml.safe_load(config_file)
    config_file.close()
    value = file_yaml
    for element in parameter.split("."):
        value = value.get(element)
        if value is None:
            raise ValueError("The parameter %s is not defined in"
                             " reporting.yaml" % parameter)
    return value


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
            execution_id=execution.id,
            _offset=offset,
            _size=batch_size,
            include_logs=False,
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


def run_blocking_ssh_command(ssh, cmd, error_msg="Unable to run this command"):
    """Command to run ssh command with the exit status."""
    (_, stdout, _) = ssh.exec_command(cmd)
    if stdout.channel.recv_exit_status() != 0:
        raise Exception(error_msg)
