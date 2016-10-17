#!/usr/bin/python
# coding: utf8
#######################################################################
#
# Copyright (c) 2016 Okinawa Open Laboratory
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
########################################################################
import os
import re
import requests
import yaml

from novaclient import client as novaclient

REPO_PATH = os.environ['repos_dir'] + '/functest/'
if not os.path.exists(REPO_PATH):
    exit(-1)

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)
f.close()

IMAGE = functest_yaml.get("vRouter").get("general").get("images").get("vyos")


class utilvnf:

    def __init__(self, logger=None):
        self.logger = logger
        self.username = ""
        self.password = ""
        self.auth_url = ""
        self.tenant_name = ""
        self.region_name = ""

    def set_credentials(self, username, password, auth_url,
                        tenant_name, region_name):
        self.username = username
        self.password = password
        self.auth_url = auth_url
        self.tenant_name = tenant_name
        self.region_name = region_name

    def get_nova_credentials(self):
        d = {}
        d['version'] = '2'
        d['username'] = self.username
        d['api_key'] = self.password
        d['auth_url'] = self.auth_url
        d['project_id'] = self.tenant_name
        d['region_name'] = self.region_name
        return d

    def get_address(self, server_name, network_name):
        creds = self.get_nova_credentials()
        nova_client = novaclient.Client(**creds)
        servers_list = nova_client.servers.list()

        for s in servers_list:
            if s.name == server_name:
                break

        address = s.addresses[network_name][0]["addr"]

        return address

    def reboot_v(self, server_name):
        creds = self.get_nova_credentials()
        nova_client = novaclient.Client(**creds)
        servers_list = nova_client.servers.list()

        for s in servers_list:
            if s.name == server_name:
                break

        s.reboot()

        return

    def get_cfy_manager_address(self, cfy, testcase_dir):
        script = "set -e; "
        script += ("source " + testcase_dir +
                   "venv_cloudify/bin/activate; ")
        script += "cd " + testcase_dir + "; "
        script += "cfy status; "
        cmd = "/bin/bash -c '" + script + "'"
        cfy.exec_cmd(cmd)

        f = open("output.txt",
                 'r')
        output_data = f.read()
        f.close()

        manager_address = None
        pattern = r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
        match = re.search(pattern,
                          output_data)
        if match:
            manager_address = match.group()

        return manager_address

    def get_blueprint_outputs(self, cfy_manager_ip, deployment_name):
        url = "http://" + cfy_manager_ip + "/deployments/" + \
              deployment_name + "/outputs"

        response = requests.get(url)

        resp_data = response.json()
        data = resp_data["outputs"]
        return data

    def get_blueprint_outputs_vnfs(self, cfy_manager_ip, deployment_name):
        outputs = self.get_blueprint_outputs(cfy_manager_ip,
                                             deployment_name)
        vnfs = outputs["vnfs"]
        vnf_list = []
        for vnf_name in vnfs:
            vnf_list.append(vnfs[vnf_name])
        return vnf_list

    def get_blueprint_outputs_networks(self, cfy_manager_ip, deployment_name):
        outputs = self.get_blueprint_outputs(cfy_manager_ip,
                                             deployment_name)
        networks = outputs["networks"]
        network_list = []
        for network_name in networks:
            network_list.append(networks[network_name])
        return network_list

    def get_vnf_info_list(self, cfy_manager_ip, topology_deploy_name,
                          target_vnf_name):
        network_list = self.get_blueprint_outputs_networks(
                                                        cfy_manager_ip,
                                                        topology_deploy_name)
        vnf_info_list = self.get_blueprint_outputs_vnfs(cfy_manager_ip,
                                                        topology_deploy_name)
        for vnf in vnf_info_list:
            vnf_name = vnf["vnf_name"]
            vnf["os_type"] = IMAGE["os_type"]
            vnf["user"] = IMAGE["user"]
            vnf["pass"] = IMAGE["pass"]

            if vnf_name == target_vnf_name:
                vnf["target_vnf_flag"] = True
            else:
                vnf["target_vnf_flag"] = False

            self.logger.debug("vnf name : " + vnf_name)
            self.logger.debug(vnf_name + " floating ip address : " +
                              vnf["floating_ip"])

            for network in network_list:
                ip = self.get_address(vnf["vnf_name"],
                                      network["network_name"])
                network_name = network["network_name"]
                vnf[network_name + "_ip"] = ip
                self.logger.debug(network_name + "_ip of " + vnf["vnf_name"] +
                                  " : " + vnf[network_name + "_ip"])

        return vnf_info_list

    def get_target_vnf(self, vnf_info_list):
        for vnf in vnf_info_list:
            if vnf["target_vnf_flag"]:
                return vnf

        return None

    def get_reference_vnf_list(self, vnf_info_list):
        reference_vnf_list = []
        for vnf in vnf_info_list:
            if not vnf["target_vnf_flag"]:
                reference_vnf_list.append(vnf)

        return reference_vnf_list

    def request_vnf_reboot(self, vnf_info_list):
        for vnf in vnf_info_list:
            self.logger.debug("reboot the " + vnf["vnf_name"])
            self.reboot_v(vnf["vnf_name"])
