#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import json
import socket
import sys
import time
import yaml

import functest.core.vnf_base as vnf_base
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
import os
from functest.utils.constants import CONST

from org.openbaton.cli.agents.agents import MainAgent
from org.openbaton.cli.errors.errors import NfvoException

# ----------------------------------------------------------
#
#               UTILS
#
# -----------------------------------------------------------


def get_config(parameter, file):
    """
    Returns the value of a given parameter in file.yaml
    parameter must be given in string format with dots
    Example: general.openstack.image_name
    """
    with open(file) as f:
        file_yaml = yaml.safe_load(f)
    f.close()
    value = file_yaml
    for element in parameter.split("."):
        value = value.get(element)
        if value is None:
            raise ValueError("The parameter %s is not defined in"
                             " %s" % (parameter, file))
    return value


def download_and_add_image_on_glance(glance, image_name,
                                     image_url, data_dir):
    dest_path = data_dir
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    file_name = image_url.rsplit('/')[-1]
    if not ft_utils.download_url(image_url, dest_path):
        return False
    image = os_utils.create_glance_image(
        glance, image_name, dest_path + file_name)
    if not image:
        return False
    return image


def servertest(host, port):
    args = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
    for family, socktype, proto, canonname, sockaddr in args:
        s = socket.socket(family, socktype, proto)
        try:
            s.connect(sockaddr)
        except socket.error:
            return False
        else:
            s.close()
            return True


class ImsVnf(vnf_base.VnfOnBoardingBase):

    def __init__(self, project='functest', case_name='orchestra_ims',
                 repo='', cmd=''):
        super(ImsVnf, self).__init__(project, case_name, repo, cmd)
        self.ob_password = "openbaton"
        self.ob_username = "admin"
        self.ob_https = False
        self.ob_port = "8080"
        self.ob_ip = "localhost"
        self.ob_instance_id = ""
        self.logger = logging.getLogger(__name__)
        self.case_dir = os.path.join(CONST.dir_functest_test, 'vnf/ims/')
        self.data_dir = CONST.dir_ims_data
        self.test_dir = CONST.dir_repo_vims_test
        self.ob_projectid = ""
        self.keystone_client = os_utils.get_keystone_client()
        self.ob_nsr_id = ""
        self.nsr = None
        self.main_agent = None
        # vIMS Data directory creation
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        # Retrieve the configuration
        try:
            self.config = CONST.__getattribute__(
                'vnf_{}_config'.format(self.case_name))
        except BaseException:
            raise Exception("Orchestra VNF config file not found")
        config_file = self.case_dir + self.config
        self.imagename = get_config("openbaton.imagename", config_file)
        self.bootstrap_link = get_config("openbaton.bootstrap_link",
                                         config_file)
        self.bootstrap_config_link = get_config(
            "openbaton.bootstrap_config_link", config_file)
        self.market_link = get_config("openbaton.marketplace_link",
                                      config_file)
        self.images = get_config("tenant_images", config_file)
        self.ims_conf = get_config("vIMS", config_file)
        self.userdata_file = get_config("openbaton.userdata.file",
                                        config_file)

    def deploy_orchestrator(self, **kwargs):
        self.logger.info("Additional pre-configuration steps")
        nova_client = os_utils.get_nova_client()
        neutron_client = os_utils.get_neutron_client()
        glance_client = os_utils.get_glance_client()

        # Import images if needed
        # needs some images
        self.logger.info("Upload some OS images if it doesn't exist")
        temp_dir = os.path.join(self.data_dir, "tmp/")
        for image_name, image_url in self.images.iteritems():
            self.logger.info("image: %s, url: %s" % (image_name, image_url))
            try:
                image_id = os_utils.get_image_id(glance_client,
                                                 image_name)
                self.logger.info("image_id: %s" % image_id)
            except BaseException:
                self.logger.error("Unexpected error: %s" % sys.exc_info()[0])

            if image_id == '':
                self.logger.info("""%s image doesn't exist on glance repository. Try
                downloading this image and upload on glance !""" % image_name)
                image_id = download_and_add_image_on_glance(glance_client,
                                                            image_name,
                                                            image_url,
                                                            temp_dir)
            if image_id == '':
                self.step_failure(
                    "Failed to find or upload required OS "
                    "image for this deployment")
        network_dic = os_utils.create_network_full(neutron_client,
                                                   "openbaton_mgmt",
                                                   "openbaton_mgmt_subnet",
                                                   "openbaton_router",
                                                   "192.168.100.0/24")

        # orchestrator VM flavor
        self.logger.info(
            "Check if orchestra Flavor is available, if not create one")
        flavor_exist, flavor_id = os_utils.get_or_create_flavor(
            "orchestra",
            "4096",
            '20',
            '2',
            public=True)
        self.logger.debug("Flavor id: %s" % flavor_id)

        if not network_dic:
            self.logger.error("There has been a problem when creating the "
                              "neutron network")

        network_id = network_dic["net_id"]

        self.logger.info("Creating floating IP for VM in advance...")
        floatip_dic = os_utils.create_floating_ip(neutron_client)
        floatip = floatip_dic['fip_addr']

        if floatip is None:
            self.logger.error("Cannot create floating IP.")

        userdata = "#!/bin/bash\n"
        userdata += "echo \"Executing userdata...\"\n"
        userdata += "set -x\n"
        userdata += "set -e\n"
        userdata += "echo \"Set nameserver to '8.8.8.8'...\"\n"
        userdata += "echo \"nameserver   8.8.8.8\" >> /etc/resolv.conf\n"
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
                     "> ./bootstrap\n" % self.bootstrap_link)
        userdata += ("curl -s %s"
                     "> ./config_file\n" % self.bootstrap_config_link)
        userdata += ("echo \"Disable usage of mysql...\"\n")
        userdata += "sed -i s/mysql=.*/mysql=no/g /config_file\n"
        userdata += ("echo \"Setting 'rabbitmq_broker_ip' to '%s'\"\n"
                     % floatip)
        userdata += ("sed -i s/rabbitmq_broker_ip=localhost/rabbitmq_broker_ip"
                     "=%s/g /config_file\n" % floatip)
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
            self.userdata_file)
        userdata += "sed -i '113i\ \ \ \ sleep 60' " \
                    "/etc/openbaton/openbaton-vnfm-generic-user-data.sh\n"
        userdata += "echo \"Starting NFVO\"\n"
        userdata += "service openbaton-nfvo restart\n"
        userdata += "echo \"Starting Generic VNFM\"\n"
        userdata += "service openbaton-vnfm-generic restart\n"
        userdata += "echo \"...end of userdata...\"\n"

        sg_id = os_utils.create_security_group_full(neutron_client,
                                                    "orchestra-sec-group",
                                                    "allowall")

        os_utils.create_secgroup_rule(neutron_client, sg_id, "ingress",
                                      "icmp", 0, 255)
        os_utils.create_secgroup_rule(neutron_client, sg_id, "egress",
                                      "icmp", 0, 255)
        os_utils.create_secgroup_rule(neutron_client, sg_id, "ingress",
                                      "tcp", 1, 65535)
        os_utils.create_secgroup_rule(neutron_client, sg_id, "ingress",
                                      "udp", 1, 65535)
        os_utils.create_secgroup_rule(neutron_client, sg_id, "egress",
                                      "tcp", 1, 65535)
        os_utils.create_secgroup_rule(neutron_client, sg_id, "egress",
                                      "udp", 1, 65535)

        self.logger.info("Security group set")

        self.logger.info("Create instance....")
        self.logger.info("flavor: m1.medium\n"
                         "image: %s\n"
                         "network_id: %s\n"
                         "userdata: %s\n"
                         % (self.imagename, network_id, userdata))

        instance = os_utils.create_instance_and_wait_for_active(
            "orchestra",
            os_utils.get_image_id(glance_client, self.imagename),
            network_id,
            "orchestra-openbaton",
            config_drive=False,
            userdata=userdata)

        self.ob_instance_id = instance.id

        self.logger.info("Adding sec group to orchestra instance")
        os_utils.add_secgroup_to_instance(nova_client,
                                          self.ob_instance_id, sg_id)

        self.logger.info("Associating floating ip: '%s' to VM '%s' "
                         % (floatip, "orchestra-openbaton"))
        if not os_utils.add_floating_ip(nova_client, instance.id, floatip):
            self.step_failure("Cannot associate floating IP to VM.")

        self.logger.info("Waiting for Open Baton NFVO to be up and running...")
        x = 0
        while x < 100:
            if servertest(floatip, "8080"):
                break
            else:
                self.logger.debug(
                    "Open Baton NFVO is not started yet (%ss)" %
                    (x * 5))
                time.sleep(5)
                x += 1

        if x == 100:
            self.step_failure("Open Baton is not started correctly")

        self.ob_ip = floatip
        self.ob_password = "openbaton"
        self.ob_username = "admin"
        self.ob_https = False
        self.ob_port = "8080"
        self.logger.info("Waiting for all components up and running...")
        time.sleep(60)
        self.details["orchestrator"] = {
            'status': "PASS", 'result': "Deploy Open Baton NFVO: OK"}
        self.logger.info("Deploy Open Baton NFVO: OK")

    def deploy_vnf(self):
        self.logger.info("Starting vIMS Deployment...")

        self.main_agent = MainAgent(nfvo_ip=self.ob_ip,
                                    nfvo_port=self.ob_port,
                                    https=self.ob_https,
                                    version=1,
                                    username=self.ob_username,
                                    password=self.ob_password)

        self.logger.info(
            "Check if openims Flavor is available, if not create one")
        flavor_exist, flavor_id = os_utils.get_or_create_flavor(
            "m1.small",
            "2048",
            '20',
            '1',
            public=True)
        self.logger.debug("Flavor id: %s" % flavor_id)

        self.logger.info("Getting project 'default'...")
        project_agent = self.main_agent.get_agent("project", self.ob_projectid)
        for p in json.loads(project_agent.find()):
            if p.get("name") == "default":
                self.ob_projectid = p.get("id")
                self.logger.info("Found project 'default': %s" % p)
                break

        self.logger.debug("project id: %s" % self.ob_projectid)
        if self.ob_projectid == "":
            self.step_failure("Default project id was not found!")

        creds = os_utils.get_credentials()
        self.logger.info("PoP creds: %s" % creds)

        if os_utils.is_keystone_v3():
            self.logger.info(
                "Using v3 API of OpenStack... -> Using OS_PROJECT_ID")
            project_id = os_utils.get_tenant_id(
                os_utils.get_keystone_client(),
                creds.get("project_name"))
        else:
            self.logger.info(
                "Using v2 API of OpenStack... -> Using OS_TENANT_NAME")
            project_id = creds.get("tenant_name")

        self.logger.debug("project id: %s" % project_id)

        vim_json = {
            "name": "vim-instance",
            "authUrl": creds.get("auth_url"),
            "tenant": project_id,
            "username": creds.get("username"),
            "password": creds.get("password"),
            "securityGroups": [
                "default",
                "orchestra-sec-group"
            ],
            "type": "openstack",
            "location": {
                "name": "opnfv",
                "latitude": "52.525876",
                "longitude": "13.314400"
            }
        }

        self.logger.debug("Registering VIM: %s" % vim_json)

        self.main_agent.get_agent(
            "vim",
            project_id=self.ob_projectid).create(entity=json.dumps(vim_json))

        market_agent = self.main_agent.get_agent("market",
                                                 project_id=self.ob_projectid)

        nsd = {}
        try:
            self.logger.info("sending: %s" % self.market_link)
            nsd = market_agent.create(entity=self.market_link)
            self.logger.info("Onboarded NSD: " + nsd.get("name"))
        except NfvoException as e:
            self.step_failure(e.message)

        nsr_agent = self.main_agent.get_agent("nsr",
                                              project_id=self.ob_projectid)
        nsd_id = nsd.get('id')
        if nsd_id is None:
            self.step_failure("NSD not onboarded correctly")

        try:
            self.nsr = nsr_agent.create(nsd_id)
        except NfvoException as e:
            self.step_failure(e.message)

        if self.nsr.get('code') is not None:
            self.logger.error(
                "vIMS cannot be deployed: %s -> %s" %
                (self.nsr.get('code'), self.nsr.get('message')))
            self.step_failure("vIMS cannot be deployed")

        i = 0
        self.logger.info("Waiting for NSR to go to ACTIVE...")
        while self.nsr.get("status") != 'ACTIVE' and self.nsr.get(
                "status") != 'ERROR':
            i += 1
            if i == 150:
                self.step_failure("After %s sec the NSR did not go to ACTIVE.."
                                  % 5 * i)
            time.sleep(5)
            self.nsr = json.loads(nsr_agent.find(self.nsr.get('id')))

        if self.nsr.get("status") == 'ACTIVE':
            self.details["vnf"] = {'status': "PASS", 'result': self.nsr}
            self.logger.info("Deploy VNF: OK")
        else:
            self.details["vnf"] = {'status': "FAIL", 'result': self.nsr}
            self.logger.error(self.nsr)
            self.step_failure("Deploy VNF: ERROR")
        self.ob_nsr_id = self.nsr.get("id")
        self.logger.info(
            "Sleep for 60s to ensure that all services are up and running...")
        time.sleep(60)
        return self.details.get("vnf")

    def test_vnf(self):
        # Adaptations probably needed
        # code used for cloudify_ims
        # ruby client on jumphost calling the vIMS on the SUT
        self.logger.info(
            "Testing if %s works properly..." %
            self.nsr.get('name'))
        for vnfr in self.nsr.get('vnfr'):
            self.logger.info(
                "Checking ports %s of VNF %s" %
                (self.ims_conf.get(
                    vnfr.get('name')).get('ports'),
                    vnfr.get('name')))
            for vdu in vnfr.get('vdu'):
                for vnfci in vdu.get('vnfc_instance'):
                    self.logger.debug(
                        "Checking ports of VNFC instance %s" %
                        vnfci.get('hostname'))
                    for floatingIp in vnfci.get('floatingIps'):
                        self.logger.debug(
                            "Testing %s:%s" %
                            (vnfci.get('hostname'), floatingIp.get('ip')))
                        for port in self.ims_conf.get(
                                vnfr.get('name')).get('ports'):
                            if servertest(floatingIp.get('ip'), port):
                                self.logger.info(
                                    "VNFC instance %s is reachable at %s:%s" %
                                    (vnfci.get('hostname'),
                                     floatingIp.get('ip'),
                                     port))
                            else:
                                self.logger.error(
                                    "VNFC instance %s is not reachable "
                                    "at %s:%s" % (vnfci.get('hostname'),
                                                  floatingIp.get('ip'), port))
                                self.details["test_vnf"] = {
                                    'status': "FAIL", 'result': (
                                        "Port %s of server %s -> %s is "
                                        "not reachable" %
                                        (port, vnfci.get('hostname'),
                                         floatingIp.get('ip')))}
                                self.step_failure("Test VNF: ERROR")
        self.details["test_vnf"] = {
            'status': "PASS",
            'result': "All tests have been executed successfully"}
        self.logger.info("Test VNF: OK")
        return self.details.get('test_vnf')

    def clean(self):
        self.main_agent.get_agent(
            "nsr",
            project_id=self.ob_projectid).delete(self.ob_nsr_id)
        time.sleep(5)
        os_utils.delete_instance(nova_client=os_utils.get_nova_client(),
                                 instance_id=self.ob_instance_id)
        # TODO question is the clean removing also the VM?
        # I think so since is goinf to remove the tenant...
        super(ImsVnf, self).clean()

    def main(self, **kwargs):
        self.logger.info("Orchestra IMS VNF onboarding test starting")
        self.execute()
        self.logger.info("Orchestra IMS VNF onboarding test executed")
        if self.result is "PASS":
            return self.EX_OK
        else:
            return self.EX_RUN_ERROR

    def run(self):
        kwargs = {}
        return self.main(**kwargs)


if __name__ == '__main__':
    test = ImsVnf()
    test.deploy_orchestrator()
    test.deploy_vnf()
    test.test_vnf()
    test.clean()
