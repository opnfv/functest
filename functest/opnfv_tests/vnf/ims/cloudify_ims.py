#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import os
import sys
import time
import yaml

from cloudify_rest_client import CloudifyClient

import functest.core.vnf as vnf
import functest.opnfv_tests.vnf.ims.clearwater_ims_base as clearwater_ims_base
from functest.utils.constants import CONST
import functest.utils.openstack_utils as os_utils

__author__ = "Valentin Boucher <valentin.boucher@orange.com>"


class CloudifyIms(clearwater_ims_base.ClearwaterOnBoardingBase):
    """Clearwater vIMS deployed with Cloudify Orchestrator Case"""

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cloudify_ims"
        super(CloudifyIms, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.neutron_client = ''
        self.glance_client = ''
        self.nova_client = ''

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
        self.logger.debug("Orchestrator configuration: %s", self.orchestrator)
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
        self.logger.debug("VNF configuration: %s", self.vnf)

        self.details['test_vnf'] = dict(
            name=get_config("vnf_test_suite.name", config_file),
            version=get_config("vnf_test_suite.version", config_file)
        )
        self.images = get_config("tenant_images", config_file)
        self.logger.info("Images needed for vIMS: %s", self.images)

    def prepare(self):
        super(CloudifyIms, self).prepare()

        self.logger.info("Additional pre-configuration steps")
        self.neutron_client = os_utils.get_neutron_client(self.creds)
        self.glance_client = os_utils.get_glance_client(self.creds)
        keystone_client = os_utils.get_keystone_client(self.creds)
        self.nova_client = os_utils.get_nova_client(self.creds)

        # needs some images
        self.logger.info("Upload some OS images if it doesn't exist")
        temp_dir = os.path.join(self.data_dir, "tmp/")
        for image_name, image_url in self.images.iteritems():
            self.logger.info("image: %s, url: %s", image_name, image_url)
            try:
                image_id = os_utils.get_image_id(self.glance_client,
                                                 image_name)
                self.logger.debug("image_id: %s", image_id)
            except Exception:  # pylint: disable=broad-except
                self.logger.error("Unexpected error: %s", sys.exc_info()[0])
                raise vnf.VnfPreparationException

            if image_id == '':
                self.logger.info("""%s image does not exist on glance repo.
                                 Try downloading this image
                                 and upload on glance !""",
                                 image_name)
                image_id = os_utils.download_and_add_image_on_glance(
                    self.glance_client,
                    image_name,
                    image_url,
                    temp_dir)
        # Need to extend quota
        self.logger.info("Update security group quota for this tenant")
        tenant_id = os_utils.get_tenant_id(keystone_client,
                                           self.tenant_name)
        self.logger.debug("Tenant id found %s", tenant_id)
        if not os_utils.update_sg_quota(self.neutron_client,
                                        tenant_id, 50, 100):
            self.logger.error("Failed to update security group quota"
                              " for tenant " + self.tenant_name)

        self.logger.debug("group quota extended")

    def deploy_orchestrator(self):
        """
        Deploy Cloudify Manager

        network, security group, fip, VM creation
        """
        # network creation

        start_time = time.time()
        self.logger.info("Creating full network ...")
        network_id = os_utils.create_network_full(
            self.neutron_client,
            "cloudify_ims_network",
            "cloudify_ims_subnet",
            "cloudify_ims_router",
            "10.67.79.0/24")["net_id"]

        # floating ip creation
        self.logger.info("Creating floating IP for cloudify manager vm ...")
        floating_ip = os_utils.create_floating_ip(
            self.neutron_client)['fip_addr']

        # security group creation
        self.logger.info("Creating security group for cloudify manager vm ...")
        sg_id = os_utils.create_security_group_full(self.neutron_client,
                                                    "sg-cloudify-manager",
                                                    "Cloudify manager")
        os_utils.create_secgroup_rule(self.neutron_client, sg_id, "ingress",
                                      "tcp", 1, 65535)
        os_utils.create_secgroup_rule(self.neutron_client, sg_id, "ingress",
                                      "udp", 1, 65535)
        os_utils.create_secgroup_rule(self.neutron_client, sg_id, "egress",
                                      "tcp", 1, 65535)
        os_utils.create_secgroup_rule(self.neutron_client, sg_id, "egress",
                                      "udp", 1, 65535)

        # orchestrator VM flavor
        self.logger.info("Get or create flavor for cloudify manager vm ...")

        self.exist_obj['flavor1'], flavor_id = os_utils.get_or_create_flavor(
            self.orchestrator['requirements']['flavor']['name'],
            self.orchestrator['requirements']['flavor']['ram_min'],
            '50',
            '2',
            public=True)
        self.logger.debug("Flavor id: %s", flavor_id)

        image_id = os_utils.get_image_id(self.glance_client,
                                         self.orchestrator
                                         ['requirements']['os_image'])

        instance = os_utils.create_instance_and_wait_for_active(
            self.orchestrator['requirements']['flavor']['name'],
            image_id,
            network_id,
            "cloudify_manager")

        os_utils.add_secgroup_to_instance(self.nova_client,
                                          instance.id,
                                          sg_id)
        self.logger.info("Associating floating ip: '%s' to VM '%s' ",
                         floating_ip,
                         "cloudify_manager")
        os_utils.add_floating_ip(self.nova_client, instance.id, floating_ip)

        public_auth_url = os_utils.get_endpoint('identity')

        self.logger.info("Set creds for cloudify manager")
        cfy_creds = dict(keystone_username=self.tenant_name,
                         keystone_password=self.tenant_name,
                         keystone_tenant_name=self.tenant_name,
                         keystone_url=public_auth_url)

        cfy_client = CloudifyClient(host=floating_ip,
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
                self.logger.warning("Cloudify Manager isn't" +
                                    "up and running. Retrying ...")
            retry = retry - 1
            time.sleep(10)

        if cfy_status == 'running':
            self.logger.info("Cloudify Manager is up and running")
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

        self.logger.info("Get or create flavor for all clearwater vm")
        self.exist_obj['flavor2'], flavor_id = os_utils.get_or_create_flavor(
            self.vnf['requirements']['flavor']['name'],
            self.vnf['requirements']['flavor']['ram_min'],
            '30',
            '1',
            public=True)

        self.vnf['inputs'].update(dict(
            flavor_id=flavor_id,
            external_network_name=os_utils.get_external_net(
                                                self.neutron_client),
            network_name="cloudify_ims_network",
            private_key_path=""
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
