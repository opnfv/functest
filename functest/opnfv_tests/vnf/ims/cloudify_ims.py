#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""CloudifyIms testcase implementation."""

import logging
import os
import time

from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.executions import Execution
from scp import SCPClient
import yaml

from functest.energy import energy
from functest.opnfv_tests.openstack.snaps import snaps_utils
import functest.opnfv_tests.vnf.ims.clearwater_ims_base as clearwater_ims_base
from functest.utils.constants import CONST

from snaps.config.flavor import FlavorConfig
from snaps.config.image import ImageConfig
from snaps.config.keypair import KeypairConfig
from snaps.config.network import NetworkConfig, PortConfig, SubnetConfig
from snaps.config.router import RouterConfig
from snaps.config.security_group import (
    Direction, Protocol, SecurityGroupConfig, SecurityGroupRuleConfig)
from snaps.config.vm_inst import FloatingIpConfig, VmInstanceConfig

from snaps.openstack.create_flavor import OpenStackFlavor
from snaps.openstack.create_image import OpenStackImage
from snaps.openstack.create_instance import OpenStackVmInstance
from snaps.openstack.create_keypairs import OpenStackKeypair
from snaps.openstack.create_network import OpenStackNetwork
from snaps.openstack.create_router import OpenStackRouter
from snaps.openstack.create_security_group import OpenStackSecurityGroup
from snaps.openstack.utils import keystone_utils


__author__ = "Valentin Boucher <valentin.boucher@orange.com>"


class CloudifyIms(clearwater_ims_base.ClearwaterOnBoardingBase):
    """Clearwater vIMS deployed with Cloudify Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        """Initialize CloudifyIms testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cloudify_ims"
        super(CloudifyIms, self).__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = CONST.__getattribute__(
                'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")

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

        self.details['test_vnf'] = dict(
            name=get_config("vnf_test_suite.name", config_file),
            version=get_config("vnf_test_suite.version", config_file)
        )
        self.images = get_config("tenant_images", config_file)
        self.__logger.info("Images needed for vIMS: %s", self.images)

    def prepare(self):
        """Prepare testscase (Additional pre-configuration steps)."""
        super(CloudifyIms, self).prepare()

        self.__logger.info("Additional pre-configuration steps")

        compute_quotas = self.os_project.get_compute_quotas()
        network_quotas = self.os_project.get_network_quotas()

        for key, value in (
                self.vnf['requirements']['compute_quotas'].items()):
            setattr(compute_quotas, key, value)

        for key, value in (
                self.vnf['requirements']['network_quotas'].items()):
            setattr(network_quotas, key, value)

        compute_quotas = self.os_project.update_compute_quotas(compute_quotas)
        network_quotas = self.os_project.update_network_quotas(network_quotas)

        # needs some images
        self.__logger.info("Upload some OS images if it doesn't exist")
        for image_name, image_file in self.images.iteritems():
            self.__logger.info("image: %s, file: %s", image_name, image_file)
            if image_file and image_name:
                image_creator = OpenStackImage(
                    self.snaps_creds,
                    ImageConfig(
                        name=image_name, image_user='cloud',
                        img_format='qcow2', image_file=image_file))
                image_creator.create()
                # self.created_object.append(image_creator)

    def deploy_orchestrator(self):
        """
        Deploy Cloudify Manager.

        network, security group, fip, VM creation
        """
        # network creation

        start_time = time.time()
        self.__logger.info("Creating keypair ...")
        kp_file = os.path.join(self.data_dir, "cloudify_ims.pem")
        keypair_settings = KeypairConfig(name='cloudify_ims_kp',
                                         private_filepath=kp_file)
        keypair_creator = OpenStackKeypair(self.snaps_creds, keypair_settings)
        keypair_creator.create()
        self.created_object.append(keypair_creator)

        self.__logger.info("Creating full network ...")
        subnet_settings = SubnetConfig(name='cloudify_ims_subnet',
                                       cidr='10.67.79.0/24')
        network_settings = NetworkConfig(name='cloudify_ims_network',
                                         subnet_settings=[subnet_settings])
        network_creator = OpenStackNetwork(self.snaps_creds, network_settings)
        network_creator.create()
        self.created_object.append(network_creator)
        ext_net_name = snaps_utils.get_ext_net_name(self.snaps_creds)
        router_creator = OpenStackRouter(
            self.snaps_creds,
            RouterConfig(
                name='cloudify_ims_router',
                external_gateway=ext_net_name,
                internal_subnets=[subnet_settings.name]))
        router_creator.create()
        self.created_object.append(router_creator)

        # security group creation
        self.__logger.info("Creating security group for cloudify manager vm")
        sg_rules = list()
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name="sg-cloudify-manager",
                direction=Direction.ingress, protocol=Protocol.tcp,
                port_range_min=1, port_range_max=65535))
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name="sg-cloudify-manager",
                direction=Direction.ingress, protocol=Protocol.udp,
                port_range_min=1, port_range_max=65535))

        security_group_creator = OpenStackSecurityGroup(
            self.snaps_creds,
            SecurityGroupConfig(
                name="sg-cloudify-manager",
                rule_settings=sg_rules))

        security_group_creator.create()
        self.created_object.append(security_group_creator)

        # orchestrator VM flavor
        self.__logger.info("Get or create flavor for cloudify manager vm ...")

        flavor_settings = FlavorConfig(
            name=self.orchestrator['requirements']['flavor']['name'],
            ram=self.orchestrator['requirements']['flavor']['ram_min'],
            disk=50,
            vcpus=2)
        flavor_creator = OpenStackFlavor(self.snaps_creds, flavor_settings)
        flavor_creator.create()
        self.created_object.append(flavor_creator)
        image_settings = ImageConfig(
            name=self.orchestrator['requirements']['os_image'],
            image_user='centos',
            exists=True)

        port_settings = PortConfig(name='cloudify_manager_port',
                                   network_name=network_settings.name)

        manager_settings = VmInstanceConfig(
            name='cloudify_manager',
            flavor=flavor_settings.name,
            port_settings=[port_settings],
            security_group_names=[
                security_group_creator.sec_grp_settings.name],
            floating_ip_settings=[FloatingIpConfig(
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

        public_auth_url = keystone_utils.get_endpoint(
            self.snaps_creds, 'identity')

        self.__logger.info("Set creds for cloudify manager")
        cfy_creds = dict(keystone_username=self.snaps_creds.username,
                         keystone_password=self.snaps_creds.password,
                         keystone_tenant_name=self.snaps_creds.project_name,
                         keystone_url=public_auth_url)

        cfy_client = CloudifyClient(host=manager_creator.get_floating_ip().ip,
                                    username='admin',
                                    password='admin',
                                    tenant='default_tenant')

        self.orchestrator['object'] = cfy_client

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
            cmd = "sudo cp ~/cloudify_ims.pem /etc/cloudify/"
            run_blocking_ssh_command(ssh, cmd)
            cmd = "sudo chmod 444 /etc/cloudify/cloudify_ims.pem"
            run_blocking_ssh_command(ssh, cmd)
            cmd = "sudo yum install -y gcc python-devel"
            run_blocking_ssh_command(ssh, cmd, "Unable to install packages \
                                                on manager")

        self.details['orchestrator'].update(status='PASS', duration=duration)

        self.vnf['inputs'].update(dict(
            external_network_name=ext_net_name,
            network_name=network_settings.name
        ))
        self.result = 1/3 * 100
        return True

    def deploy_vnf(self):
        """Deploy Clearwater IMS."""
        start_time = time.time()

        self.__logger.info("Upload VNFD")
        cfy_client = self.orchestrator['object']
        descriptor = self.vnf['descriptor']
        cfy_client.blueprints.publish_archive(descriptor.get('url'),
                                              descriptor.get('name'),
                                              descriptor.get('file_name'))

        self.__logger.info("Get or create flavor for all clearwater vm")
        flavor_settings = FlavorConfig(
            name=self.vnf['requirements']['flavor']['name'],
            ram=self.vnf['requirements']['flavor']['ram_min'],
            disk=25,
            vcpus=1)
        flavor_creator = OpenStackFlavor(self.snaps_creds, flavor_settings)
        flavor_creator.create()
        self.created_object.append(flavor_creator)

        self.vnf['inputs'].update(dict(
            flavor_id=self.vnf['requirements']['flavor']['name'],
        ))

        self.__logger.info("Create VNF Instance")
        cfy_client.deployments.create(descriptor.get('name'),
                                      descriptor.get('name'),
                                      self.vnf.get('inputs'))

        wait_for_execution(cfy_client,
                           _get_deployment_environment_creation_execution(
                               cfy_client, descriptor.get('name')),
                           self.__logger,
                           timeout=300)

        self.__logger.info("Start the VNF Instance deployment")
        execution = cfy_client.executions.start(descriptor.get('name'),
                                                'install')
        # Show execution log
        execution = wait_for_execution(cfy_client, execution, self.__logger)

        duration = time.time() - start_time

        self.__logger.info(execution)
        if execution.status == 'terminated':
            self.details['vnf'].update(status='PASS', duration=duration)
            self.result += 1/3 * 100
            result = True
        else:
            self.details['vnf'].update(status='FAIL', duration=duration)
            result = False
        return result

    def test_vnf(self):
        """Run test on clearwater ims instance."""
        start_time = time.time()

        cfy_client = self.orchestrator['object']

        outputs = cfy_client.deployments.outputs.get(
            self.vnf['descriptor'].get('name'))['outputs']
        dns_ip = outputs['dns_ip']
        ellis_ip = outputs['ellis_ip']
        self.config_ellis(ellis_ip)

        if not dns_ip:
            return False

        vims_test_result = self.run_clearwater_live_test(
            dns_ip=dns_ip,
            public_domain=self.vnf['inputs']["public_domain"])
        duration = time.time() - start_time
        short_result, nb_test = sig_test_format(vims_test_result)
        self.__logger.info(short_result)
        self.details['test_vnf'].update(result=short_result,
                                        full_result=vims_test_result,
                                        duration=duration)
        try:
            vnf_test_rate = short_result['passed'] / nb_test
            # orchestrator + vnf + test_vnf
            self.result += vnf_test_rate / 3 * 100
        except ZeroDivisionError:
            self.__logger.error("No test has been executed")
            self.details['test_vnf'].update(status='FAIL')
            return False

        return True

    def clean(self):
        """Clean created objects/functions."""
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
                parameters=dict(ignore_failure=True),
                force=True)

            wait_for_execution(cfy_client, execution, self.__logger)
            cfy_client.deployments.delete(self.vnf['descriptor'].get('name'))
            cfy_client.blueprints.delete(self.vnf['descriptor'].get('name'))
        except:  # pylint: disable=broad-except
            self.__logger.warn("Some issue during the undeployment ..")
            self.__logger.warn("Tenant clean continue ..")

        super(CloudifyIms, self).clean()

    @energy.enable_recording
    def run(self, **kwargs):
        """Execute CloudifyIms test case."""
        return super(CloudifyIms, self).run(**kwargs)


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


def wait_for_execution(client, execution, logger, timeout=1500, ):
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


def _get_deployment_environment_creation_execution(client, deployment_id):
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


def sig_test_format(sig_test):
    """Process the signaling result to have a short result."""
    nb_passed = 0
    nb_failures = 0
    nb_skipped = 0
    for data_test in sig_test:
        if data_test['result'] == "Passed":
            nb_passed += 1
        elif data_test['result'] == "Failed":
            nb_failures += 1
        elif data_test['result'] == "Skipped":
            nb_skipped += 1
    short_sig_test_result = {}
    short_sig_test_result['passed'] = nb_passed
    short_sig_test_result['failures'] = nb_failures
    short_sig_test_result['skipped'] = nb_skipped
    nb_test = nb_passed + nb_skipped
    return (short_sig_test_result, nb_test)


def run_blocking_ssh_command(ssh, cmd, error_msg="Unable to run this command"):
    """Command to run ssh command with the exit status."""
    stdin, stdout, stderr = ssh.exec_command(cmd)
    if stdout.channel.recv_exit_status() != 0:
        raise Exception(error_msg)
