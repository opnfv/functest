#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import os
import time
import yaml

from cloudify_rest_client import CloudifyClient
import functest.opnfv_tests.vnf.ims.clearwater_ims_base as clearwater_ims_base
from functest.utils.constants import CONST
import functest.utils.openstack_utils as os_utils

from snaps.openstack.os_credentials import OSCreds
from snaps.openstack.create_network import NetworkSettings, SubnetSettings, \
                                            OpenStackNetwork
from snaps.openstack.create_security_group import SecurityGroupSettings, \
                                                    SecurityGroupRuleSettings,\
                                                    Direction, Protocol, \
                                                    OpenStackSecurityGroup
from snaps.openstack.create_router import RouterSettings, OpenStackRouter
from snaps.openstack.create_instance import VmInstanceSettings, \
                                                FloatingIpSettings, \
                                                OpenStackVmInstance
from snaps.openstack.create_flavor import FlavorSettings, OpenStackFlavor
from snaps.openstack.create_image import ImageSettings, OpenStackImage
from snaps.openstack.create_keypairs import KeypairSettings, OpenStackKeypair
from snaps.openstack.create_network import PortSettings

from functest.opnfv_tests.openstack.snaps import snaps_utils


__author__ = "Valentin Boucher <valentin.boucher@orange.com>"


class CloudifyIms(clearwater_ims_base.ClearwaterOnBoardingBase):
    """Clearwater vIMS deployed with Cloudify Orchestrator Case"""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cloudify_ims"
        super(CloudifyIms, self).__init__(**kwargs)

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
        super(CloudifyIms, self).prepare()

        self.__logger.info("Additional pre-configuration steps")

        if os_utils.is_keystone_v3():
            tenant = self.creds['project_name']
            identity_api_version = 3
        else:
            tenant = self.creds['tenant_name']
            identity_api_version = 2

        self.snaps_creds = OSCreds(username=self.creds['username'],
                                   password=self.creds['password'],
                                   auth_url=self.creds['auth_url'],
                                   project_name=tenant,
                                   identity_api_version=identity_api_version)

        # needs some images
        self.__logger.info("Upload some OS images if it doesn't exist")
        for image_name, image_url in self.images.iteritems():
            self.__logger.info("image: %s, url: %s", image_name, image_url)
            image_creator = OpenStackImage(self.snaps_creds,
                                           ImageSettings(name=image_name,
                                                         image_user='',
                                                         img_format='qcow2',
                                                         url=image_name))
            image_creator.create()
            self.created_object.append(image_creator)

            # Need to extend quota
        # self.__logger.info("Update security group quota for this tenant")
        # tenant_id = os_utils.get_tenant_id(keystone_client,
        #                                    self.tenant_name)
        # self.__logger.debug("Tenant id found %s", tenant_id)
        # if not os_utils.update_sg_quota(self.neutron_client,
        #                                 tenant_id, 50, 100):
        #     self.__logger.error("Failed to update security group quota"
        #                         " for tenant " + self.tenant_name)

        # self.__logger.debug("group quota extended")

    def deploy_orchestrator(self):
        """
        Deploy Cloudify Manager

        network, security group, fip, VM creation
        """
        # network creation

        start_time = time.time()
        self.__logger.info("Creating keypair ...")
        kp_file = os.path.join(self.data_dir, "cloudify_ims.pem")
        keypair_settings = KeypairSettings(name='cloudify_ims_kp',
                                           private_filepath=kp_file)
        keypair_creator = OpenStackKeypair(self.snaps_creds, keypair_settings)
        keypair_creator.create()
        self.created_object.append(keypair_creator)

        self.__logger.info("Creating full network ...")
        subnet_settings = SubnetSettings(name='cloudify_ims_subnet',
                                         cidr='10.67.79.0/24')
        network_settings = NetworkSettings(name='cloudify_ims_network',
                                           subnet_settings=[subnet_settings])
        network_creator = OpenStackNetwork(self.snaps_creds, network_settings)
        network_creator.create()
        self.created_object.append(network_creator)
        ext_net_name = snaps_utils.get_ext_net_name(self.snaps_creds)
        router_creator = OpenStackRouter(
            self.snaps_creds,
            RouterSettings(
                name='cloudify_ims_router',
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

        securit_group_creator = OpenStackSecurityGroup(
            self.snaps_creds,
            SecurityGroupSettings(
                name="sg-cloudify-manager",
                rule_settings=sg_rules))

        securit_group_creator.create()
        self.created_object.append(securit_group_creator)

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
            img_format='qcow2',
            url='')

        port_settings = PortSettings(name='cloudify_manager_port',
                                     network_name=network_settings.name)

        manager_settings = VmInstanceSettings(
            name='cloudify_manager',
            flavor=flavor_settings.name,
            port_settings=[port_settings],
            security_group_names=[securit_group_creator.sec_grp_settings.name],
            floating_ip_settings=[FloatingIpSettings(
                name='cloudify_manager_fip',
                port_name=port_settings,
                router_name=router_creator.router_settings.name)])

        manager_creator = OpenStackVmInstance(self.snaps_creds,
                                              manager_settings,
                                              image_settings,
                                              keypair_settings)

        manager_creator.create()
        self.created_object.append(manager_creator)

        public_auth_url = os_utils.get_endpoint('identity')

        self.__logger.info("Set creds for cloudify manager")
        cfy_creds = dict(keystone_username=self.tenant_name,
                         keystone_password=self.tenant_name,
                         keystone_tenant_name=self.tenant_name,
                         keystone_url=public_auth_url)

        cfy_client = CloudifyClient(host=manager_creator.get_floating_ip(),
                                    username='admin',
                                    password='admin',
                                    tenant='default_tenant')

        self.orchestrator['object'] = cfy_client

        # TRY GET STATUS UNTIL 6 min
        cfy_status = None
        retry = 30
        while cfy_status != 'running' and retry:
            try:
                cfy_status = cfy_client.manager.get_status()['status']
            except Exception:  # pylint: disable=broad-except
                self.__logger.warning("Cloudify Manager isn't" +
                                      "up and running. Retrying ...")
            retry = retry - 1
            time.sleep(10)

        if cfy_status == 'running':
            self.__logger.info("Cloudify Manager is up and running")
        else:
            raise Exception("Cloudify Manager isn't up and running")

        secrets_list = cfy_client.secrets.list()
        for k, val in cfy_creds.iteritems():
            if not any(d.get('key', None) == k for d in secrets_list):
                cfy_client.secrets.create(k, val)
            else:
                cfy_client.secrets.update(k, val)

        duration = time.time() - start_time

        self.details['orchestrator'].update(status='PASS', duration=duration)

        self.vnf['inputs'].update(dict(
            external_network_name=ext_net_name,
            network_name=network_settings.name,
            private_key_path=keypair_settings.private_filepath
        ))
        return True

    def deploy_vnf(self):
        """
        Deploy Clearwater IMS
        """
        start_time = time.time()

        cfy_client = self.orchestrator['object']
        descriptor = self.vnf['descriptor']
        cfy_client.blueprints.publish_archive(descriptor.get('url'),
                                              descriptor.get('name'),
                                              descriptor.get('file_name'))

        self.__logger.info("Get or create flavor for all clearwater vm")
        self.exist_obj['flavor2'], flavor_id = os_utils.get_or_create_flavor(
            self.vnf['requirements']['flavor']['name'],
            self.vnf['requirements']['flavor']['ram_min'],
            '30',
            '1',
            public=True)

        self.vnf['inputs'].update(dict(
            flavor_id=flavor_id,
        ))

        cfy_client.deployments.create(descriptor.get('name'),
                                      descriptor.get('name'),
                                      self.vnf.get('inputs'))

        cfy_client.executions.start(descriptor.get('name'), 'install')

        duration = time.time() - start_time

        self.details['vnf'].update(status='PASS', duration=duration)

    def test_vnf(self):
        """
        Run test on clearwater ims instance
        """
        start_time = time.time()

        cfy_client = self.orchestrator['object']

        outputs = cfy_client.deployments.get('cw-site1').outputs
        dns_ip = outputs['dns_ip']
        ellis_ip = outputs['ellis_ip']
        self.config_ellis(ellis_ip)

        if dns_ip != "":
            vims_test_result = self.run_clearwater_live_test(
                dns_ip=dns_ip,
                public_domain=self.vnf['inputs']["public_domain"])
            duration = time.time() - start_time
            self.details['test_vnf'].update(status='PASS',
                                            result=vims_test_result,
                                            duration=duration)
            return True

    def clean(self):
        cfy_client = self.orchestrator['object']

        cfy_client.executions.start(self.vnf['descriptor'].get('name'),
                                    'uninstall',
                                    parameters=dict(ignore_failure=True),
                                    force=True)

        cfy_client.deployments.delete(self.vnf['descriptor'].get('name'))

        cfy_client.blueprints.delete(self.vnf['descriptor'].get('name'))

        for creator in reversed(self.created_object):
            try:
                creator.clean()
            except Exception as e:
                self.logger.error('Unexpected error cleaning - %s', e)
        super(CloudifyIms, self).clean()


# ----------------------------------------------------------
#
#               YAML UTILS
#
# -----------------------------------------------------------
def get_config(parameter, file_path):
    """
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
