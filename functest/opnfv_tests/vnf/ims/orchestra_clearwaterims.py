#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""Orchestra Clearwater IMS testcase implementation."""

import json
import logging
import os
import socket
import time

import pkg_resources
import yaml

from functest.core import vnf
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils import config

from org.openbaton.cli.errors.errors import NfvoException
from org.openbaton.cli.agents.agents import MainAgent
from snaps.config.flavor import FlavorConfig
from snaps.config.image import ImageConfig
from snaps.config.network import NetworkConfig, PortConfig, SubnetConfig
from snaps.config.router import RouterConfig
from snaps.config.security_group import (
    Direction, Protocol, SecurityGroupConfig, SecurityGroupRuleConfig)
from snaps.config.vm_inst import FloatingIpConfig
from snaps.config.vm_inst import VmInstanceConfig
from snaps.openstack.utils import keystone_utils
from snaps.openstack.create_flavor import OpenStackFlavor
from snaps.openstack.create_image import OpenStackImage
from snaps.openstack.create_instance import OpenStackVmInstance
from snaps.openstack.create_network import OpenStackNetwork
from snaps.openstack.create_router import OpenStackRouter
from snaps.openstack.create_security_group import OpenStackSecurityGroup


__author__ = "Pauls, Michael <michael.pauls@fokus.fraunhofer.de>"
# ----------------------------------------------------------
#
#               UTILS
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
                             " reporting.yaml", parameter)
    return value


def servertest(host, port):
    """Method to test that a server is reachable at IP:port"""
    args = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
    for family, socktype, proto, _, sockaddr in args:
        sock = socket.socket(family, socktype, proto)
        try:
            sock.connect(sockaddr)
        except socket.error:
            return False
        else:
            sock.close()
            return True


def get_userdata(orchestrator=dict):
    """Build userdata for Open Baton machine"""
    userdata = "#!/bin/bash\n"
    userdata += "echo \"Executing userdata...\"\n"
    userdata += "set -x\n"
    userdata += "set -e\n"
    userdata += "echo \"Install curl...\"\n"
    userdata += "apt-get install curl\n"
    userdata += "echo \"Inject public key...\"\n"
    userdata += ("echo \"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCuPXrV3"
                 "geeHc6QUdyUr/1Z+yQiqLcOskiEGBiXr4z76MK4abiFmDZ18OMQlc"
                 "fl0p3kS0WynVgyaOHwZkgy/DIoIplONVr2CKBKHtPK+Qcme2PVnCtv"
                 "EqItl/FcD+1h5XSQGoa+A1TSGgCod/DPo+pes0piLVXP8Ph6QS1k7S"
                 "ic7JDeRQ4oT1bXYpJ2eWBDMfxIWKZqcZRiGPgMIbJ1iEkxbpeaAd9O"
                 "4MiM9nGCPESmed+p54uYFjwEDlAJZShcAZziiZYAvMZhvAhe6USljc"
                 "7YAdalAnyD/jwCHuwIrUw/lxo7UdNCmaUxeobEYyyFA1YVXzpNFZya"
                 "XPGAAYIJwEq/ openbaton@opnfv\" >> /home/ubuntu/.ssh/aut"
                 "horized_keys\n")
    userdata += "echo \"Download bootstrap...\"\n"
    userdata += ("curl -s %s "
                 "> ./bootstrap\n" % orchestrator['bootstrap']['url'])
    userdata += ("curl -s %s" "> ./config_file\n" %
                 orchestrator['bootstrap']['config']['url'])
    userdata += ("echo \"Disable usage of mysql...\"\n")
    userdata += "sed -i s/mysql=.*/mysql=no/g /config_file\n"
    userdata += "echo \"Set autostart of components to 'false'\"\n"
    userdata += "export OPENBATON_COMPONENT_AUTOSTART=false\n"
    userdata += "echo \"Execute bootstrap...\"\n"
    bootstrap = "sh ./bootstrap release -configFile=./config_file"
    userdata += bootstrap + "\n"
    userdata += "echo \"Setting 'nfvo.plugin.timeout' to '300000'\"\n"
    userdata += ("echo \"nfvo.plugin.timeout=600000\" >> "
                 "/etc/openbaton/openbaton-nfvo.properties\n")
    userdata += (
        "wget %s -O /etc/openbaton/openbaton-vnfm-generic-user-data.sh\n" %
        orchestrator['gvnfm']['userdata']['url'])
    userdata += "sed -i '113i"'\ \ \ \ '"sleep 60' " \
                "/etc/openbaton/openbaton-vnfm-generic-user-data.sh\n"
    userdata += ("sed -i s/nfvo.marketplace.port=8082/nfvo.marketplace."
                 "port=8080/g /etc/openbaton/openbaton-nfvo.properties\n")
    userdata += "echo \"Starting NFVO\"\n"
    userdata += "service openbaton-nfvo restart\n"
    userdata += "echo \"Starting Generic VNFM\"\n"
    userdata += "service openbaton-vnfm-generic restart\n"
    userdata += "echo \"...end of userdata...\"\n"
    return userdata


class ClearwaterImsVnf(vnf.VnfOnBoarding):
    """Clearwater IMS VNF deployed with openBaton orchestrator"""

    # logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "orchestra_clearwaterims"
        super(ClearwaterImsVnf, self).__init__(**kwargs)
        self.logger = logging.getLogger("functest.ci.run_tests.orchestra")
        self.logger.info("kwargs %s", (kwargs))

        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/ims/')
        self.data_dir = getattr(config.CONF, 'dir_ims_data')
        self.test_dir = getattr(config.CONF, 'dir_repo_vims_test')
        self.created_resources = []
        self.logger.info("%s VNF onboarding test starting", self.case_name)

        try:
            self.config = getattr(
                config.CONF, 'vnf_{}_config'.format(self.case_name))
        except BaseException:
            raise Exception("Orchestra VNF config file not found")

        config_file = self.case_dir + self.config

        self.mano = dict(
            get_config("mano", config_file),
            details={}
        )
        self.logger.debug("Orchestrator configuration %s", self.mano)

        self.details['orchestrator'] = dict(
            name=self.mano['name'],
            version=self.mano['version'],
            status='ERROR',
            result=''
        )

        self.vnf = dict(
            get_config(self.case_name, config_file),
        )
        self.logger.debug("VNF configuration: %s", self.vnf)

        self.details['vnf'] = dict(
            name=self.vnf['name'],
        )

        self.details['test_vnf'] = dict(
            name=self.case_name,
        )

        # Orchestra base Data directory creation
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.images = get_config("tenant_images.orchestrator", config_file)
        self.images.update(
            get_config(
                "tenant_images.%s" %
                self.case_name,
                config_file))
        self.creds = None
        self.orchestra_router = None

    def prepare(self):
        """Prepare testscase (Additional pre-configuration steps)."""
        super(ClearwaterImsVnf, self).prepare()

        self.logger.info("Additional pre-configuration steps")

        public_auth_url = keystone_utils.get_endpoint(
            self.snaps_creds, 'identity')
        self.creds = {
            "tenant": self.snaps_creds.project_name,
            "username": self.snaps_creds.username,
            "password": self.snaps_creds.password,
            "auth_url": public_auth_url}
        self.prepare_images()
        self.prepare_flavor()
        self.prepare_security_groups()
        self.prepare_network()

    def prepare_images(self):
        """Upload images if they doen't exist yet"""
        self.logger.info("Upload images if they doen't exist yet")
        for image_name, image_file in self.images.iteritems():
            self.logger.info("image: %s, file: %s", image_name, image_file)
            if image_file and image_name:
                image = OpenStackImage(
                    self.snaps_creds,
                    ImageConfig(name=image_name,
                                image_user='cloud',
                                img_format='qcow2',
                                image_file=image_file,
                                public=True))
                image.create()
                self.created_resources.append(image)

    def prepare_security_groups(self):
        """Create Open Baton security group if it doesn't exist yet"""
        self.logger.info(
            "Creating security group for Open Baton if not yet existing...")
        sg_rules = list()
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name="orchestra-sec-group-allowall-{}".format(
                    self.uuid),
                direction=Direction.ingress,
                protocol=Protocol.tcp,
                port_range_min=1,
                port_range_max=65535))
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name="orchestra-sec-group-allowall-{}".format(
                    self.uuid),
                direction=Direction.egress,
                protocol=Protocol.tcp,
                port_range_min=1,
                port_range_max=65535))
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name="orchestra-sec-group-allowall-{}".format(
                    self.uuid),
                direction=Direction.ingress,
                protocol=Protocol.udp,
                port_range_min=1,
                port_range_max=65535))
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name="orchestra-sec-group-allowall-{}".format(
                    self.uuid),
                direction=Direction.egress,
                protocol=Protocol.udp,
                port_range_min=1,
                port_range_max=65535))
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name="orchestra-sec-group-allowall-{}".format(
                    self.uuid),
                direction=Direction.ingress,
                protocol=Protocol.icmp))
        sg_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name="orchestra-sec-group-allowall-{}".format(
                    self.uuid),
                direction=Direction.egress,
                protocol=Protocol.icmp))
        security_group = OpenStackSecurityGroup(
            self.snaps_creds,
            SecurityGroupConfig(
                name="orchestra-sec-group-allowall-{}".format(
                    self.uuid),
                rule_settings=sg_rules))
        security_group_info = security_group.create()
        self.created_resources.append(security_group)
        self.mano['details']['sec_group'] = security_group_info.name
        self.logger.info(
            "Security group orchestra-sec-group-allowall prepared")

    def prepare_flavor(self):
        """Create Open Baton flavor if it doesn't exist yet"""
        self.logger.info(
            "Create Flavor for Open Baton NFVO if not yet existing")

        flavor_settings = FlavorConfig(
            name=self.mano['requirements']['flavor']['name'],
            ram=self.mano['requirements']['flavor']['ram_min'],
            disk=self.mano['requirements']['flavor']['disk'],
            vcpus=self.mano['requirements']['flavor']['vcpus'])
        flavor = OpenStackFlavor(self.snaps_creds, flavor_settings)
        flavor_info = flavor.create()
        self.created_resources.append(flavor)
        self.mano['details']['flavor'] = {}
        self.mano['details']['flavor']['name'] = flavor_settings.name
        self.mano['details']['flavor']['id'] = flavor_info.id

    def prepare_network(self):
        """Create network/subnet/router if they doen't exist yet"""
        self.logger.info(
            "Creating network/subnet/router if they doen't exist yet...")
        subnet_settings = SubnetConfig(
            name='{}_subnet-{}'.format(self.case_name, self.uuid),
            cidr="192.168.100.0/24")
        network_settings = NetworkConfig(
            name='{}_net-{}'.format(self.case_name, self.uuid),
            subnet_settings=[subnet_settings])
        orchestra_network = OpenStackNetwork(
            self.snaps_creds, network_settings)
        orchestra_network_info = orchestra_network.create()
        self.mano['details']['network'] = {}
        self.mano['details']['network']['id'] = orchestra_network_info.id
        self.mano['details']['network']['name'] = orchestra_network_info.name
        self.mano['details']['external_net_name'] = snaps_utils.\
            get_ext_net_name(self.snaps_creds)
        self.created_resources.append(orchestra_network)
        self.orchestra_router = OpenStackRouter(
            self.snaps_creds,
            RouterConfig(
                name='{}_router-{}'.format(self.case_name, self.uuid),
                external_gateway=self.mano['details']['external_net_name'],
                internal_subnets=[
                    subnet_settings.name]))
        self.orchestra_router.create()
        self.created_resources.append(self.orchestra_router)
        self.logger.info("Created network and router for Open Baton NFVO...")

    def get_vim_descriptor(self):
        """"Create VIM descriptor to be used for onboarding"""
        self.logger.info(
            "Building VIM descriptor with PoP creds: %s",
            self.creds)
        self.logger.debug("VIM project/tenant id: %s",
                          self.snaps_creds.project_name)
        keystone = keystone_utils.keystone_client(self.snaps_creds)
        project_id = keystone_utils.get_project(
            keystone=keystone, project_name=self.snaps_creds.project_name).id
        vim_json = {
            "name": "vim-instance",
            "authUrl": self.creds.get("auth_url"),
            "tenant": project_id,
            "username": self.creds.get("username"),
            "password": self.creds.get("password"),
            "securityGroups": [
                self.mano['details']['sec_group']
            ],
            "type": "openstack",
            "location": {
                "name": "opnfv",
                "latitude": "52.525876",
                "longitude": "13.314400"
            }
        }
        self.logger.info("Built VIM descriptor: %s", vim_json)
        return vim_json

    def deploy_orchestrator(self):
        self.logger.info("Deploying Open Baton...")
        self.logger.info("Details: %s", self.mano['details'])
        start_time = time.time()

        self.logger.info("Creating orchestra instance...")
        userdata = get_userdata(self.mano)
        self.logger.info("flavor: %s\n"
                         "image: %s\n"
                         "network_id: %s\n",
                         self.mano['details']['flavor']['name'],
                         self.mano['requirements']['image'],
                         self.mano['details']['network']['id'])
        self.logger.debug("userdata: %s\n", userdata)
        # setting up image
        image_settings = ImageConfig(
            name=self.mano['requirements']['image'],
            image_user='ubuntu',
            exists=True)
        # setting up port
        port_settings = PortConfig(
            name='{}_port-{}'.format(self.case_name, self.uuid),
            network_name=self.mano['details']['network']['name'])

        # build configuration of vm
        orchestra_settings = VmInstanceConfig(
            name=self.case_name,
            flavor=self.mano['details']['flavor']['name'],
            port_settings=[port_settings],
            security_group_names=[self.mano['details']['sec_group']],
            floating_ip_settings=[FloatingIpConfig(
                name='orchestra_fip-{}'.format(self.uuid),
                port_name=port_settings.name,
                router_name=self.orchestra_router.router_settings.name)],
            userdata=str(userdata))
        orchestra_vm = OpenStackVmInstance(
            self.snaps_creds, orchestra_settings, image_settings)
        orchestra_vm.create()
        self.mano['details']['fip'] = orchestra_vm.get_floating_ip()
        self.created_resources.append(orchestra_vm)
        self.mano['details']['id'] = orchestra_vm.get_vm_info()['id']
        self.logger.info(
            "Created orchestra instance: %s", self.mano['details']['id'])
        self.logger.info("Waiting for Open Baton NFVO to be up and running...")
        timeout = 0
        while timeout < 20:
            if servertest(
                    self.mano['details']['fip'].ip,
                    "8080"):
                break
            else:
                self.logger.info(
                    "Open Baton NFVO is not started yet (%ss)",
                    (timeout * 60))
                time.sleep(60)
                timeout += 1

        if timeout >= 20:
            duration = time.time() - start_time
            self.details["orchestrator"].update(
                status='FAIL', duration=duration)
            self.logger.error("Open Baton is not started correctly")
            return False

        self.logger.info("Waiting for all components to be up and running...")
        time.sleep(60)
        duration = time.time() - start_time
        self.details["orchestrator"].update(status='PASS', duration=duration)
        self.logger.info("Deploy Open Baton NFVO: OK")
        return True

    def deploy_vnf(self):
        start_time = time.time()
        self.logger.info("Deploying %s...", self.vnf['name'])

        main_agent = MainAgent(
            nfvo_ip=self.mano['details']['fip'].ip,
            nfvo_port=8080,
            https=False,
            version=1,
            username=self.mano['credentials']['username'],
            password=self.mano['credentials']['password'])

        self.logger.info(
            "Create %s Flavor if not existing", self.vnf['name'])
        flavor_settings = FlavorConfig(
            name=self.vnf['requirements']['flavor']['name'],
            ram=self.vnf['requirements']['flavor']['ram_min'],
            disk=self.vnf['requirements']['flavor']['disk'],
            vcpus=self.vnf['requirements']['flavor']['vcpus'])
        flavor = OpenStackFlavor(self.snaps_creds, flavor_settings)
        flavor_info = flavor.create()
        self.logger.debug("Flavor id: %s", flavor_info.id)

        self.logger.info("Getting project 'default'...")
        project_agent = main_agent.get_agent("project", "")
        for project in json.loads(project_agent.find()):
            if project.get("name") == "default":
                self.mano['details']['project_id'] = project.get("id")
                self.logger.info("Found project 'default': %s", project)
                break

        vim_json = self.get_vim_descriptor()
        self.logger.info("Registering VIM: %s", vim_json)

        main_agent.get_agent(
            "vim", project_id=self.mano['details']['project_id']).create(
                entity=json.dumps(vim_json))

        market_agent = main_agent.get_agent(
            "market", project_id=self.mano['details']['project_id'])

        try:
            self.logger.info("sending: %s", self.vnf['descriptor']['url'])
            nsd = market_agent.create(entity=self.vnf['descriptor']['url'])
            if nsd.get('id') is None:
                self.logger.error("NSD not onboarded correctly")
                duration = time.time() - start_time
                self.details["vnf"].update(status='FAIL', duration=duration)
                return False
            self.mano['details']['nsd_id'] = nsd.get('id')
            self.logger.info("Onboarded NSD: " + nsd.get("name"))

            nsr_agent = main_agent.get_agent(
                "nsr", project_id=self.mano['details']['project_id'])

            self.mano['details']['nsr'] = nsr_agent.create(
                self.mano['details']['nsd_id'])
        except NfvoException:
            self.logger.exception("failed")
            duration = time.time() - start_time
            self.details["vnf"].update(status='FAIL', duration=duration)
            return False

        if self.mano['details']['nsr'].get('code') is not None:
            self.logger.error(
                "%s cannot be deployed: %s -> %s",
                self.vnf['name'],
                self.mano['details']['nsr'].get('code'),
                self.mano['details']['nsr'].get('message'))
            self.logger.error("%s cannot be deployed", self.vnf['name'])
            duration = time.time() - start_time
            self.details["vnf"].update(status='FAIL', duration=duration)
            return False

        timeout = 0
        self.logger.info("Waiting for NSR to go to ACTIVE...")
        while self.mano['details']['nsr'].get("status") != 'ACTIVE' \
                and self.mano['details']['nsr'].get("status") != 'ERROR':
            timeout += 1
            self.logger.info("NSR is not yet ACTIVE... (%ss)", 60 * timeout)
            if timeout == 30:
                self.logger.error("INACTIVE NSR after %s sec..", 60 * timeout)
                duration = time.time() - start_time
                self.details["vnf"].update(status='FAIL', duration=duration)
                return False
            time.sleep(60)
            self.mano['details']['nsr'] = json.loads(
                nsr_agent.find(self.mano['details']['nsr'].get('id')))

        duration = time.time() - start_time
        if self.mano['details']['nsr'].get("status") == 'ACTIVE':
            self.details["vnf"].update(status='PASS', duration=duration)
            self.logger.info("Sleep for 60s to ensure that all "
                             "services are up and running...")
            time.sleep(60)
            result = True
        else:
            self.details["vnf"].update(status='FAIL', duration=duration)
            self.logger.error("NSR: %s", self.mano['details'].get('nsr'))
            result = False
        return result

    def test_vnf(self):
        self.logger.info(
            "Testing VNF Clearwater IMS is not yet implemented...")
        start_time = time.time()

        duration = time.time() - start_time
        self.details["test_vnf"].update(status='PASS', duration=duration)
        self.logger.info("Test VNF: OK")
        return True

    def clean(self):
        self.logger.info("Cleaning %s...", self.case_name)
        try:
            main_agent = MainAgent(
                nfvo_ip=self.mano['details']['fip'].ip,
                nfvo_port=8080, https=False, version=1,
                username=self.mano['credentials']['username'],
                password=self.mano['credentials']['password'])
            self.logger.info("Terminating %s...", self.vnf['name'])
            if self.mano['details'].get('nsr'):
                main_agent.get_agent(
                    "nsr",
                    project_id=self.mano['details']['project_id']).delete(
                        self.mano['details']['nsr'].get('id'))
                self.logger.info("Sleeping 60 seconds...")
                time.sleep(60)
            else:
                self.logger.info("No need to terminate the VNF...")
        except (NfvoException, KeyError) as exc:
            self.logger.error('Unexpected error cleaning - %s', exc)
        super(ClearwaterImsVnf, self).clean()
