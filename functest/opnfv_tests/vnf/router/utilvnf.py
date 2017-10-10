#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

""" Utility module of vrouter testcase """

import json
import logging
import os
import pkg_resources
import requests
import yaml

from functest.utils.constants import CONST
from git import Repo
from novaclient import client as novaclient
from keystoneauth1.identity import v3
from keystoneauth1 import session
from requests.auth import HTTPBasicAuth

RESULT_SPRIT_INDEX = {
    "transfer": 8,
    "bandwidth": 6,
    "jitter": 4,
    "los_total": 2,
    "pkt_loss": 1
}

BIT_PER_BYTE = 8

NOVA_CLIENT_API_VERSION = '2'
NOVA_CILENT_NETWORK_INFO_INDEX = 0
CFY_INFO_OUTPUT_FILE = "output.txt"

CIDR_NETWORK_SEGMENT_INFO_INDEX = 0
PACKET_LOST_INFO_INDEX = 0
PACKET_TOTAL_INFO_INDEX = 1

NUMBER_OF_DIGITS_FOR_AVG_TRANSFER = 0
NUMBER_OF_DIGITS_FOR_AVG_BANDWIDTH = 0
NUMBER_OF_DIGITS_FOR_AVG_JITTER = 3
NUMBER_OF_DIGITS_FOR_AVG_PKT_LOSS = 1


class Utilvnf(object):
    """ Utility class of vrouter testcase """

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.username = ""
        self.password = ""
        self.auth_url = ""
        self.tenant_name = ""

        data_dir = data_dir = CONST.__getattribute__('dir_router_data')

        self.vnf_data_dir = data_dir
        self.opnfv_vnf_data_dir = "opnfv-vnf-data/"
        self.command_template_dir = "command_template/"
        self.test_scenario_yaml = "test_scenario.yaml"
        test_env_config_yaml_file = "test_env_config.yaml"
        self.test_cmd_map_yaml_file = "test_cmd_map.yaml"
        self.test_env_config_yaml = os.path.join(
            self.vnf_data_dir,
            self.opnfv_vnf_data_dir,
            test_env_config_yaml_file)

        self.blueprint_dir = "opnfv-vnf-vyos-blueprint/"
        self.blueprint_file_name = "function-test-openstack-blueprint.yaml"

        if not os.path.exists(self.vnf_data_dir):
            os.makedirs(self.vnf_data_dir)

        case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/router')

        config_file_name = CONST.__getattribute__(
            'vnf_{}_config'.format("vyos_vrouter"))

        config_file = os.path.join(case_dir, config_file_name)

        with open(config_file) as file_fd:
            vrouter_config_yaml = yaml.safe_load(file_fd)
        file_fd.close()

        test_data = vrouter_config_yaml.get("test_data")

        self.logger.debug("Downloading the test data.")
        vrouter_data_path = self.vnf_data_dir + self.opnfv_vnf_data_dir

        if not os.path.exists(vrouter_data_path):
            Repo.clone_from(test_data['url'],
                            vrouter_data_path,
                            branch=test_data['branch'])

        with open(self.test_env_config_yaml) as file_fd:
            test_env_config_yaml = yaml.safe_load(file_fd)
        file_fd.close()

        self.image = test_env_config_yaml.get(
            "general").get("images").get("vyos")
        self.tester_image = test_env_config_yaml.get(
            "general").get("images").get("tester_vm_os")

        self.test_result_json_file = "test_result.json"
        if os.path.isfile(self.test_result_json_file):
            os.remove(self.test_result_json_file)
            self.logger.debug("removed %s" % self.test_result_json_file)

    def get_nova_client(self):
        creds = self.get_nova_credentials()
        auth = v3.Password(auth_url=creds['auth_url'],
                           username=creds['username'],
                           password=creds['password'],
                           project_name=creds['tenant_name'],
                           user_domain_id='default',
                           project_domain_id='default')
        sess = session.Session(auth=auth)
        nova_client = novaclient.Client(NOVA_CLIENT_API_VERSION, session=sess)

        return nova_client

    def set_credentials(self, username, password, auth_url, tenant_name):
        self.username = username
        self.password = password
        self.auth_url = auth_url
        self.tenant_name = tenant_name

    def get_nova_credentials(self):
        creds = {}
        creds['username'] = self.username
        creds['password'] = self.password
        creds['auth_url'] = self.auth_url
        creds['tenant_name'] = self.tenant_name
        return creds

    def get_address(self, server_name, network_name):
        nova_client = self.get_nova_client()
        servers_list = nova_client.servers.list()
        server = None

        for server in servers_list:
            if server.name == server_name:
                break

        address = server.addresses[
                      network_name][NOVA_CILENT_NETWORK_INFO_INDEX]["addr"]

        return address

    def get_mac_address(self, server_name, network_name):
        nova_client = self.get_nova_client()
        servers_list = nova_client.servers.list()
        server = None

        for server in servers_list:
            if server.name == server_name:
                break

        mac_address = server.addresses[network_name][
                          NOVA_CILENT_NETWORK_INFO_INDEX][
                          "OS-EXT-IPS-MAC:mac_addr"]

        return mac_address

    def reboot_vm(self, server_name):
        nova_client = self.get_nova_client()
        servers_list = nova_client.servers.list()
        server = None

        for server in servers_list:
            if server.name == server_name:
                break

        server.reboot()

        return

    def delete_vm(self, server_name):
        nova_client = self.get_nova_client()
        servers_list = nova_client.servers.list()
        server = None

        for server in servers_list:
            if server.name == server_name:
                nova_client.servers.delete(server)
                break

        return

    def get_blueprint_outputs(self, cfy_manager_ip, deployment_name):
        url = "http://%s/deployments/%s/outputs" % (
            cfy_manager_ip, deployment_name)

        response = requests.get(
            url,
            auth=HTTPBasicAuth('admin', 'admin'),
            headers={'Tenant': 'default_tenant'})

        resp_data = response.json()
        self.logger.debug(resp_data)
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

    def request_vnf_reboot(self, vnf_info_list):
        for vnf in vnf_info_list:
            self.logger.debug("reboot the " + vnf["vnf_name"])
            self.reboot_vm(vnf["vnf_name"])

    def request_vm_delete(self, vnf_info_list):
        for vnf in vnf_info_list:
            self.logger.debug("delete the " + vnf["vnf_name"])
            self.delete_vm(vnf["vnf_name"])

    def get_vnf_info_list(self, cfy_manager_ip, topology_deploy_name,
                          target_vnf_name):
        network_list = self.get_blueprint_outputs_networks(
            cfy_manager_ip,
            topology_deploy_name)
        vnf_info_list = self.get_blueprint_outputs_vnfs(cfy_manager_ip,
                                                        topology_deploy_name)
        for vnf in vnf_info_list:
            vnf_name = vnf["vnf_name"]
            vnf["os_type"] = self.image["os_type"]
            vnf["user"] = self.image["user"]
            vnf["pass"] = self.image["pass"]

            if vnf_name == target_vnf_name:
                vnf["target_vnf_flag"] = True
            else:
                vnf["target_vnf_flag"] = False

            self.logger.debug("vnf name : " + vnf_name)
            self.logger.debug(vnf_name + " floating ip address : " +
                              vnf["floating_ip"])

            for network in network_list:
                network_name = network["network_name"]
                ip_address = self.get_address(vnf["vnf_name"],
                                              network["network_name"])
                vnf[network_name + "_ip"] = ip_address
                mac = self.get_mac_address(vnf["vnf_name"],
                                           network["network_name"])
                vnf[network_name + "_mac"] = mac

                self.logger.debug(network_name + "_ip of " + vnf["vnf_name"] +
                                  " : " + vnf[network_name + "_ip"])
                self.logger.debug(network_name + "_mac of " + vnf["vnf_name"] +
                                  " : " + vnf[network_name + "_mac"])

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

    def get_vnf_info(self, vnf_info_list, vnf_name):
        for vnf in vnf_info_list:
            if vnf["vnf_name"] == vnf_name:
                return vnf

        return None

    def convert_functional_test_result(self, result_data_list):
        result = {}
        for result_data in result_data_list:
            test_kind = result_data["test_kind"]
            protocol = result_data["protocol"]
            test_result_data = result_data["result"]

            if test_kind not in result:
                result[test_kind] = []

            result[test_kind].append({protocol: test_result_data})

        return {"Functional_test": result}

    def write_result_data(self, result_data):
        test_result = []
        if not os.path.isfile(self.test_result_json_file):
            file_fd = open(self.test_result_json_file, "w")
            file_fd.close()
        else:
            file_fd = open(self.test_result_json_file, "r")
            test_result = json.load(file_fd)
            file_fd.close()

        test_result.append(result_data)

        file_fd = open(self.test_result_json_file, "w")
        json.dump(test_result, file_fd)
        file_fd.close()

    def output_test_result_json(self):
        if os.path.isfile(self.test_result_json_file):
            file_fd = open(self.test_result_json_file, "r")
            test_result = json.load(file_fd)
            file_fd.close()
            output_json_data = json.dumps(test_result,
                                          sort_keys=True,
                                          indent=4)
            self.logger.debug("test_result %s" % output_json_data)
        else:
            self.logger.debug("Not found %s" % self.test_result_json_file)

    def get_test_scenario(self, file_path):
        test_scenario_file = open(file_path,
                                  'r')
        test_scenario_yaml = yaml.safe_load(test_scenario_file)
        test_scenario_file.close()
        return test_scenario_yaml["test_scenario_list"]
