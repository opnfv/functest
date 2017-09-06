#!/usr/bin/env python

# Copyright (c) 2017 Orange, CableLabs. Huawei and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""HeatIms testcase implementation."""

# Notes for reviewer(s) - very important to read before your review

# replaced all Cloudify by Heat
# replaced all cloudiy be heat
# replaced all cfy by cw_heat (clearwater heat)
# In attempt to replace CloudifyClient by HeatClient trying to find where
# do I get that from snaps-oo or any other options? [1] 
# Same way for Execution should we use
#    snaps-oo HeatUtilsCreateComplexStackTests listed in snap-oo imports
#    from FUNCTEST
# What about unitest for stack tesing should we not include those in [2]
# Although I wanted to complete heat orchetsration but in absence of clear
# picture on snaps and snaps-oo will like some clerifictions
# Before I try one or more patches to get it right - this may go past
# Release-E 1.0 as is clear the scenario currently I am using is
# 'os-nosdn-nofeature-ha' and targeting compass beause I can not mix
# JOID/orchestar as they have not included the openims clearwater live tests.

#[1] https://git.opnfv.org/snaps/tree/snaps/openstack/utils/heat_utils.py
#[2] https://git.opnfv.org/snaps/tree/snaps/domain/test/stack_tests.py 

import logging
import os
import time

from heat_rest_client import HeatClient
# should we replace HeatCleint by [1]
# from heatclient.client import Client
from heat_rest_client.executions import Execution
# should we replace

from scp import SCPClient
import yaml

from functest.energy import energy
from functest.opnfv_tests.openstack.snaps import snaps_utils
# new snap-oo heat library developed by Steven P CableLabs
from functest.opnfv_tests.openstack.snaps-oo import HeatUtilsCreateSimpleStackTests
from functest.opnfv_tests.openstack.snaps-oo import HeatUtilsCreateComplexStackTests
from functest.opnfv_tests.openstack.snaps-oo import SettingsUtilsNetworkingTests
from functest.opnfv_tests.openstack.snaps-oo import SettingsUtilsVmInstTests
from functest.opnfv_tests.openstack.snaps-oo import CreateStackSuccessTests

import functest.opnfv_tests.vnf.ims.clearwater_ims_base as clearwater_ims_base
from functest.utils.constants import CONST
import functest.utils.openstack_utils as os_utils

from snaps.openstack.os_credentials import OSCreds
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


__author__ = "Valentin Boucher <valentin.boucher@orange.com> \
              Prakash Ramchabdran <prakash.ramchandran@huawei.com>"


class HeatIms(clearwater_ims_base.ClearwaterOnBoardingBase):
    """Clearwater vIMS deployed with Heat Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        """Initialize HeatIms testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "heat_ims"
        super(HeatIms, self).__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = CONST.__getattribute__(
                'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")

        self.snaps_creds = ''
        self.created_object = []

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
        super(HeatIms, self).prepare()

        self.__logger.info("Additional pre-configuration steps")

        self.snaps_creds = OSCreds(
            username=self.creds['username'],
            password=self.creds['password'],
            auth_url=self.creds['auth_url'],
            project_name=self.creds['tenant'],
            identity_api_version=int(os_utils.get_keystone_client_version()))

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
                # self.created_object.append(image_creator)

    def deploy_orchestrator(self):
        """
        Deploy Heat Manager.

        network, security group, fip, VM creation
        """
        # network creation

        start_time = time.time()
        self.__logger.info("Creating keypair ...")
        kp_file = os.path.join(self.data_dir, "heat_ims.pem")
        keypair_settings = KeypairSettings(name='heat_ims_kp',
                                           private_filepath=kp_file)
        keypair_creator = OpenStackKeypair(self.snaps_creds, keypair_settings)
        keypair_creator.create()
        self.created_object.append(keypair_creator)

        self.__logger.info("Creating full network ...")
        subnet_settings = SubnetSettings(name='heat_ims_subnet',
                                         cidr='10.67.79.0/24')
        network_settings = NetworkSettings(name='heat_ims_network',
                                           subnet_settings=[subnet_settings])
        network_creator = OpenStackNetwork(self.snaps_creds, network_settings)
        network_creator.create()
        self.created_object.append(network_creator)
        ext_net_name = snaps_utils.get_ext_net_name(self.snaps_creds)
        router_creator = OpenStackRouter(
            self.snaps_creds,
            RouterSettings(
                name='heat_ims_router',
                external_gateway=ext_net_name,
                internal_subnets=[subnet_settings.name]))
        router_creator.create()
        self.created_object.append(router_creator)

        # security group creation
        self.__logger.info("Creating security group for heat manager vm")
        sg_rules = list()
        sg_rules.append(
            SecurityGroupRuleSettings(sec_grp_name="sg-heat-manager",
                                      direction=Direction.ingress,
                                      protocol=Protocol.tcp, port_range_min=1,
                                      port_range_max=65535))
        sg_rules.append(
            SecurityGroupRuleSettings(sec_grp_name="sg-heat-manager",
                                      direction=Direction.ingress,
                                      protocol=Protocol.udp, port_range_min=1,
                                      port_range_max=65535))

        securit_group_creator = OpenStackSecurityGroup(
            self.snaps_creds,
            SecurityGroupSettings(
                name="sg-heat-manager",
                rule_settings=sg_rules))

        securit_group_creator.create()
        self.created_object.append(securit_group_creator)

        # orchestrator VM flavor
        self.__logger.info("Get or create flavor for heat manager vm ...")

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

        port_settings = PortSettings(name='heat_manager_port',
                                     network_name=network_settings.name)

        manager_settings = VmInstanceSettings(
            name='heat_manager',
            flavor=flavor_settings.name,
            port_settings=[port_settings],
            security_group_names=[securit_group_creator.sec_grp_settings.name],
            floating_ip_settings=[FloatingIpSettings(
                name='heat_manager_fip',
                port_name=port_settings.name,
                router_name=router_creator.router_settings.name)])

        manager_creator = OpenStackVmInstance(self.snaps_creds,
                                              manager_settings,
                                              image_settings,
                                              keypair_settings)

        self.__logger.info("Creating heat manager VM")
        manager_creator.create()
        self.created_object.append(manager_creator)

        public_auth_url = os_utils.get_endpoint('identity')

        self.__logger.info("Set creds for heat manager")
        cw_heat_creds = dict(keystone_username=self.tenant_name,
                         keystone_password=self.tenant_name,
                         keystone_tenant_name=self.tenant_name,
                         keystone_url=public_auth_url)

        cw_heat_client = HeatClient(host=manager_creator.get_floating_ip().ip,
                                    username='admin',
                                    password='admin',
                                    tenant='default_tenant')

        self.orchestrator['object'] = cw_heat_client

        self.__logger.info("Attemps running status of the Manager")
        cw_heat_status = None
        retry = 10
        while str(cw_heat_status) != 'running' and retry:
            try:
                cw_heat_status = cw_heat_client.manager.get_status()['status']
                self.__logger.debug("The current manager status is %s",
                                    cw_heat_status)
            except Exception:  # pylint: disable=broad-except
                self.__logger.warning("Heat Manager isn't " +
                                      "up and running. Retrying ...")
            retry = retry - 1
            time.sleep(30)

        if str(cw_heat_status) == 'running':
            self.__logger.info("Heat Manager is up and running")
        else:
            raise Exception("Heat Manager isn't up and running")

        self.__logger.info("Put OpenStack creds in manager")
        secrets_list = cw_heat_client.secrets.list()
        for k, val in cw_heat_creds.iteritems():
            if not any(d.get('key', None) == k for d in secrets_list):
                cw_heat_client.secrets.create(k, val)
            else:
                cw_heat_client.secrets.update(k, val)

        duration = time.time() - start_time

        self.__logger.info("Put private keypair in manager")
        if manager_creator.vm_ssh_active(block=True):
            ssh = manager_creator.ssh_client()
            scp = SCPClient(ssh.get_transport(), socket_timeout=15.0)
            scp.put(kp_file, '~/')
            cmd = "sudo cp ~/heat_ims.pem /etc/heat/"
            run_blocking_ssh_command(ssh, cmd)
            cmd = "sudo chmod 444 /etc/heat/heat_ims.pem"
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
        cw_heat_client = self.orchestrator['object']
        descriptor = self.vnf['descriptor']
        cw_heat_client.blueprints.publish_archive(descriptor.get('url'),
                                              descriptor.get('name'),
                                              descriptor.get('file_name'))

        self.__logger.info("Get or create flavor for all clearwater vm")
        flavor_settings = FlavorSettings(
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
        cw_heat_client.deployments.create(descriptor.get('name'),
                                      descriptor.get('name'),
                                      self.vnf.get('inputs'))

        wait_for_execution(cw_heat_client,
                           _get_deployment_environment_creation_execution(
                               cw_heat_client, descriptor.get('name')),
                           self.__logger,
                           timeout=600)

        self.__logger.info("Start the VNF Instance deployment")
        execution = cw_heat_client.executions.start(descriptor.get('name'),
                                                'install')
        # Show execution log
        execution = wait_for_execution(cw_heat_client, execution, self.__logger)

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

        cw_heat_client = self.orchestrator['object']

        outputs = cw_heat_client.deployments.outputs.get(
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
            cw_heat_client = self.orchestrator['object']
            dep_name = self.vnf['descriptor'].get('name')
            # kill existing execution
            self.__logger.info('Deleting the current deployment')
            exec_list = cw_heat_client.executions.list(dep_name)
            for execution in exec_list:
                if execution['status'] == "started":
                    try:
                        cw_heat_client.executions.cancel(execution['id'],
                                                     force=True)
                    except:  # pylint: disable=broad-except
                        self.__logger.warn("Can't cancel the current exec")

            execution = cw_heat_client.executions.start(
                dep_name,
                'uninstall',
                parameters=dict(ignore_failure=True),
                force=True)

            wait_for_execution(cw_heat_client, execution, self.__logger)
            cw_heat_client.deployments.delete(self.vnf['descriptor'].get('name'))
            cw_heat_client.blueprints.delete(self.vnf['descriptor'].get('name'))
        except:  # pylint: disable=broad-except
            self.__logger.warn("Some issue during the undeployment ..")
            self.__logger.warn("Tenant clean continue ..")

        self.__logger.info('Remove the heat manager OS object ..')
        for creator in reversed(self.created_object):
            try:
                creator.clean()
            except Exception as exc:
                self.logger.error('Unexpected error cleaning - %s', exc)
        super(HeatIms, self).clean()

    @energy.enable_recording
    def run(self, **kwargs):
        """Execute HeatIms test case."""
        super(HeatIms, self).run(**kwargs)


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


def wait_for_execution(client, execution, logger, timeout=2400, ):
    """Wait for a workflow execution on Heat Manager."""
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
