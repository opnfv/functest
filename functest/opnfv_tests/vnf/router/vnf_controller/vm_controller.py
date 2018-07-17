#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

"""vm controll module"""

import logging
import os
import time
import yaml

from functest.opnfv_tests.vnf.router.utilvnf import Utilvnf
from functest.opnfv_tests.vnf.router.vnf_controller.command_generator import (
    CommandGenerator)
from functest.opnfv_tests.vnf.router.vnf_controller.ssh_client import (
    SshClient)


class VmController(object):
    """vm controll class"""

    logger = logging.getLogger(__name__)

    def __init__(self, util_info):
        self.logger.debug("initialize vm controller")
        self.command_gen = CommandGenerator()
        credentials = util_info["credentials"]

        self.util = Utilvnf()
        self.util.set_credentials(credentials["cloud"])

        with open(self.util.test_env_config_yaml) as file_fd:
            test_env_config_yaml = yaml.safe_load(file_fd)
        file_fd.close()

        self.command_wait = test_env_config_yaml.get("general").get(
            "command_wait")
        self.ssh_connect_timeout = test_env_config_yaml.get("general").get(
            "ssh_connect_timeout")
        self.ssh_connect_retry_count = test_env_config_yaml.get("general").get(
            "ssh_connect_retry_count")

    def command_gen_from_template(self, command_file_path, cmd_input_param):
        (command_file_dir, command_file_name) = os.path.split(
            command_file_path)
        template = self.command_gen.load_template(command_file_dir,
                                                  command_file_name)
        return self.command_gen.command_create(template,
                                               cmd_input_param)

    def config_vm(self, vm_info, test_cmd_file_path,
                  cmd_input_param, prompt_file_path):
        ssh = self.connect_ssh_and_config_vm(vm_info,
                                             test_cmd_file_path,
                                             cmd_input_param,
                                             prompt_file_path)
        if ssh is None:
            return False

        ssh.close()

        return True

    def connect_ssh_and_config_vm(self, vm_info, test_cmd_file_path,
                                  cmd_input_param, prompt_file_path):

        key_filename = None
        if "key_path" in vm_info:
            key_filename = vm_info["key_path"]

        ssh = SshClient(ip_address=vm_info["floating_ip"],
                        user=vm_info["user"],
                        password=vm_info["pass"],
                        key_filename=key_filename)

        result = ssh.connect(self.ssh_connect_timeout,
                             self.ssh_connect_retry_count)
        if not result:
            self.logger.error(
                "Cannot establish connection to IP '%s'. Aborting!",
                ssh.ip_address)
            return None

        (result, _) = self.command_create_and_execute(
            ssh,
            test_cmd_file_path,
            cmd_input_param,
            prompt_file_path)
        if not result:
            ssh.close()
            return None

        return ssh

    def command_create_and_execute(self, ssh, test_cmd_file_path,
                                   cmd_input_param, prompt_file_path):
        prompt_file = open(prompt_file_path,
                           'r')
        prompt = yaml.safe_load(prompt_file)
        prompt_file.close()
        config_mode_prompt = prompt["config_mode"]

        commands = self.command_gen_from_template(test_cmd_file_path,
                                                  cmd_input_param)
        return self.command_list_execute(ssh,
                                         commands,
                                         config_mode_prompt)

    def command_list_execute(self, ssh, command_list, prompt):
        res_data_list = []
        for command in command_list:
            self.logger.debug("Command : %s", command)
            (res, res_data) = self.command_execute(ssh,
                                                   command,
                                                   prompt)
            self.logger.debug("Response : %s", res_data)
            res_data_list.append(res_data)
            if not res:
                return res, res_data_list

            time.sleep(self.command_wait)

        return True, res_data_list

    def command_execute(self, ssh, command, prompt):
        res_data = ssh.send(command, prompt)
        if res_data is None:
            self.logger.info("retry send command : %s", command)
            res_data = ssh.send(command,
                                prompt)
            if not ssh.error_check(res_data):
                return False, res_data

        return True, res_data
