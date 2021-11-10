#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

"""vrouter controll module"""

import logging
import os
import time
import yaml

import prettytable

from functest.opnfv_tests.vnf.router.utilvnf import Utilvnf
from functest.opnfv_tests.vnf.router.vnf_controller.checker import Checker
from functest.opnfv_tests.vnf.router.vnf_controller.ssh_client import (
    SshClient)
from functest.opnfv_tests.vnf.router.vnf_controller.vm_controller import (
    VmController)


class VnfController():
    """vrouter controll class"""

    logger = logging.getLogger(__name__)

    def __init__(self, util_info):
        self.logger.debug("init vnf controller")
        self.util = Utilvnf()
        self.vm_controller = VmController(util_info)

        with open(self.util.test_env_config_yaml, encoding='utf-8') as file_fd:
            test_env_config_yaml = yaml.safe_load(file_fd)
        file_fd.close()

        self.cmd_wait = test_env_config_yaml.get("general").get("command_wait")
        self.ssh_connect_timeout = test_env_config_yaml.get("general").get(
            "ssh_connect_timeout")
        self.ssh_connect_retry_count = test_env_config_yaml.get("general").get(
            "ssh_connect_retry_count")

    def config_vnf(self, source_vnf, destination_vnf, test_cmd_file_path,
                   parameter_file_path, prompt_file_path):
        # pylint: disable=too-many-arguments
        with open(
                parameter_file_path, 'r', encoding='utf-8') as parameter_file:
            cmd_input_param = yaml.safe_load(parameter_file)

        cmd_input_param["macaddress"] = source_vnf["data_plane_network_mac"]
        cmd_input_param["source_ip"] = source_vnf["data_plane_network_ip"]
        cmd_input_param["destination_ip"] = destination_vnf[
            "data_plane_network_ip"]

        return self.vm_controller.config_vm(source_vnf,
                                            test_cmd_file_path,
                                            cmd_input_param,
                                            prompt_file_path)

    def result_check(self, target_vnf, reference_vnf,
                     check_rule_file_path_list, parameter_file_path,
                     prompt_file_path):
        # pylint: disable=too-many-arguments,too-many-locals

        res_dict_data_list = []

        with open(
                parameter_file_path, 'r', encoding='utf-8') as parameter_file:
            cmd_input_param = yaml.safe_load(parameter_file)

        cmd_input_param["source_ip"] = target_vnf["data_plane_network_ip"]
        cmd_input_param["destination_ip"] = reference_vnf[
            "data_plane_network_ip"]

        with open(prompt_file_path, 'r', encoding='utf-8') as prompt_file:
            prompt = yaml.safe_load(prompt_file)
        terminal_mode_prompt = prompt["terminal_mode"]

        ssh = SshClient(target_vnf["floating_ip"],
                        target_vnf["user"],
                        target_vnf["pass"])

        result = ssh.connect(self.ssh_connect_timeout,
                             self.ssh_connect_retry_count)
        if not result:
            return False, res_dict_data_list

        checker = Checker()

        res_table = prettytable.PrettyTable(
            header_style='upper', padding_width=5,
            field_names=['test item', 'result'])

        status = True
        res_data_list = []
        for check_rule_file_path in check_rule_file_path_list:
            (check_rule_dir, check_rule_file) = os.path.split(
                check_rule_file_path)
            check_rules = checker.load_check_rule(check_rule_dir,
                                                  check_rule_file,
                                                  cmd_input_param)
            (res, res_data) = self.vm_controller.command_execute(
                ssh,
                check_rules["command"],
                terminal_mode_prompt)
            res_data_list.append(res_data)
            if not res:
                status = False
                break

            (res, res_dict_data) = checker.regexp_information(res_data,
                                                              check_rules)
            res_dict_data_list.append(res_dict_data)
            res_table.add_row([res_dict_data["test_name"],
                               res_dict_data["result"]])
            if not res:
                status = False

            time.sleep(self.cmd_wait)

        ssh.close()

        self.logger.info("Test result:\n\n%s\n", res_table.get_string())

        self.output_check_result_detail_data(res_data_list)

        return status, res_dict_data_list

    def output_check_result_detail_data(self, res_data_list):
        for res_data in res_data_list:
            self.logger.debug(res_data)
