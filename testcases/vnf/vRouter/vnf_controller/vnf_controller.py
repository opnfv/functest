##!/usr/bin/python
## coding: utf8
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
import time
import yaml

import functest.utils.functest_logger as ft_logger
from functest.testcases.vnf.vRouter.utilvnf import utilvnf
from functest.testcases.vnf.vRouter.vnf_controller.checker import Checker
from functest.testcases.vnf.vRouter.vnf_controller.command_generator import Command_generator
from functest.testcases.vnf.vRouter.vnf_controller.ssh_client import SSH_Client

""" logging configuration """
logger = ft_logger.Logger("vRouter.vnf_controller").getLogger()

REPO_PATH = os.environ['repos_dir'] + '/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)
f.close()

REBOOT_WAIT = functest_yaml.get("vRouter").get("general").get("reboot_wait")
COMMAND_WAIT = functest_yaml.get("vRouter").get("general").get("command_wait")
SSH_CONNECT_TIMEOUT = functest_yaml.get("vRouter").get("general").get(
    "ssh_connect_timeout")
SSH_CONNECT_RETRY_COUNT = functest_yaml.get("vRouter").get("general").get(
    "ssh_connect_retry_count")

class VNF_controller():

    def __init__(self, util_info):
        logger.debug("init vnf controller")
        self.command_gen = Command_generator()
        self.credentials = util_info["credentials"]

        self.util = utilvnf(logger)
        self.util.set_credentials(self.credentials["username"],
                                  self.credentials["password"],
                                  self.credentials["auth_url"],
                                  self.credentials["tenant_name"],
                                  self.credentials["region_name"])

    def command_gen_from_template(self, command_file_path, cmd_input_param):
        (command_file_dir, command_file_name) = os.path.split(command_file_path)
        template = self.command_gen.load_template(command_file_dir,
                                                  command_file_name)
        return self.command_gen.command_create(template,
                                               cmd_input_param)

    def config_vnf(self, source_vnf, destination_vnf, test_cmd_file_path,
                   parameter_file_path, prompt_file_path):
        parameter_file = open(parameter_file_path,
                              'r')
        cmd_input_param = yaml.safe_load(parameter_file)
        parameter_file.close() 

        cmd_input_param["source_ip"] = source_vnf["data_plane_network_ip"]
        cmd_input_param["destination_ip"] = destination_vnf[
                                                "data_plane_network_ip"]

        prompt_file = open(prompt_file_path,
                           'r')
        prompt = yaml.safe_load(prompt_file)
        prompt_file.close()
        config_mode_prompt = prompt["config_mode"]

        ssh = SSH_Client(source_vnf["floating_ip"],
                         source_vnf["user"],
                         source_vnf["pass"])

        result = ssh.connect(SSH_CONNECT_TIMEOUT,
                             SSH_CONNECT_RETRY_COUNT)
        if not result:
            logger.debug("try to vm reboot.")
            self.util.reboot_v(source_vnf["vnf_name"])
            time.sleep(REBOOT_WAIT)
            result = ssh.connect(SSH_CONNECT_TIMEOUT,
                                 SSH_CONNECT_RETRY_COUNT)
            if not result:
                return False

        commands = self.command_gen_from_template(test_cmd_file_path,
                                                  cmd_input_param)
        result = self.command_list_execute(ssh,
                                           commands,
                                           config_mode_prompt)
        if not result:
            ssh.close()
            return False

        ssh.close()

        return True

    def result_check(self, target_vnf, reference_vnf,
                     check_rule_file_path_list, parameter_file_path,
                     prompt_file_path):
        parameter_file = open(parameter_file_path,
                              'r')
        cmd_input_param = yaml.safe_load(parameter_file)
        parameter_file.close()

        cmd_input_param["source_ip"] = target_vnf["data_plane_network_ip"]
        cmd_input_param["destination_ip"] = reference_vnf[
                                                "data_plane_network_ip"]

        prompt_file = open(prompt_file_path,
                           'r')
        prompt = yaml.safe_load(prompt_file)
        prompt_file.close()
        terminal_mode_prompt = prompt["terminal_mode"]

        ssh = SSH_Client(target_vnf["floating_ip"],
                         target_vnf["user"],
                         target_vnf["pass"])

        result = ssh.connect(SSH_CONNECT_TIMEOUT,
                             SSH_CONNECT_RETRY_COUNT)
        if not result:
            return False

        checker = Checker()

        status = True
        res_data_list = []
        for check_rule_file_path in check_rule_file_path_list:
            (check_rule_dir, check_rule_file) = os.path.split(
                                                    check_rule_file_path)
            check_rules = checker.load_check_rule(check_rule_dir,
                                                  check_rule_file,
                                                  cmd_input_param)
            res = self.command_execute(ssh,
                                       check_rules["command"],
                                       terminal_mode_prompt)
            res_data_list.append(res)
            if res == None:
                status = False
                break
            checker.regexp_information(res,
                                       check_rules)
            time.sleep(COMMAND_WAIT)

        ssh.close()

        self.output_chcke_result_detail_data(res_data_list) 

        return status

    def output_chcke_result_detail_data(self, res_data_list):
        for res_data in res_data_list:
             logger.debug(res_data)

    def command_list_execute(self, ssh, commands, prompt):
        for command in commands:
            logger.debug("Command : " + command)
            res = self.command_execute(ssh,
                                       command,
                                       prompt)
            time.sleep(COMMAND_WAIT)
            logger.debug("Response : " + res)
            if not ssh.error_check(res):
                logger.debug("Command : " + command)
                res = self.command_execute(ssh,
                                           command,
                                           prompt)
                logger.debug("Response : " + res)
                if not ssh.error_check(res):
                    return False

        return True

    def command_execute(self, ssh, command, prompt):
        res = ssh.send(command,
                       prompt)
        if res == None:
            logger.info("retry send command : " + command)
            res = ssh.send(command,
                           prompt)
        return res

