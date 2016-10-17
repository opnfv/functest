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
from functest.testcases.vnf.vRouter.vnf_controller.vnf_controller import VNF_controller

""" logging configuration """
logger = ft_logger.Logger("vRouter.test_exec").getLogger()

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)
f.close()

VNF_DATA_DIR = functest_yaml.get("general").get(
    "directories").get("dir_vRouter_data") + "/"
PROTOCOL_STABLE_WAIT = functest_yaml.get("vRouter").get("general").get(
    "protocol_stable_wait")

class Test_exec():

    def __init__(self, util_info):
        logger.debug("init test exec")
        self.credentials = util_info["credentials"]
        self.vnf_ctrl = VNF_controller(util_info)

        test_cmd_map_file = open(VNF_DATA_DIR +
                                 "opnfv-vnf-data/command_template/" +
                                 "test_cmd_map.yaml",
                                 'r')
        self.test_cmd_map_yaml = yaml.safe_load(test_cmd_map_file)
        test_cmd_map_file.close()

        self.util = utilvnf(logger)
        self.util.set_credentials(self.credentials["username"],
                                  self.credentials["password"],
                                  self.credentials["auth_url"],
                                  self.credentials["tenant_name"],
                                  self.credentials["region_name"])

    def config_target_vnf(self, target_vnf, reference_vnf, test_kind):
        logger.debug("Configuration to target vnf")
        test_info = self.test_cmd_map_yaml[target_vnf["os_type"]]
        test_cmd_file_path = test_info[test_kind]["pre_command"]
        target_parameter_file_path = test_info[test_kind]["parameter_target"]
        prompt_file_path = test_info["prompt"]

        return self.vnf_ctrl.config_vnf(target_vnf,
                                        reference_vnf,
                                        test_cmd_file_path,
                                        target_parameter_file_path,
                                        prompt_file_path)


    def config_reference_vnf(self, target_vnf, reference_vnf,test_kind):
        logger.debug("Configuration to reference vnf")
        test_info = self.test_cmd_map_yaml[reference_vnf["os_type"]]
        test_cmd_file_path = test_info[test_kind]["pre_command"]
        reference_parameter_file_path = test_info[test_kind][
                                            "parameter_reference"]
        prompt_file_path = test_info["prompt"]

        return self.vnf_ctrl.config_vnf(reference_vnf,
                                        target_vnf,
                                        test_cmd_file_path,
                                        reference_parameter_file_path,
                                        prompt_file_path)

    def result_check(self, target_vnf, reference_vnf, test_kind, test_list):
        test_info = self.test_cmd_map_yaml[target_vnf["os_type"]]
        target_parameter_file_path = test_info[test_kind]["parameter_target"]
        prompt_file_path = test_info["prompt"]
        check_rule_file_path_list = []

        for test in test_list:
            check_rule_file_path_list.append(test_info[test_kind][test])

        return self.vnf_ctrl.result_check(target_vnf,
                                          reference_vnf,
                                          check_rule_file_path_list,
                                          target_parameter_file_path,
                                          prompt_file_path)

    def run(self, target_vnf, reference_vnf_list, test_kind, test_list):
        for reference_vnf in reference_vnf_list:
            logger.debug("Start config command " + target_vnf["vnf_name"] +
                         " and " + reference_vnf["vnf_name"])

            result = self.config_target_vnf(target_vnf,
                                            reference_vnf,
                                            test_kind)
            if not result:
                return False

            result = self.config_reference_vnf(target_vnf,
                                               reference_vnf,
                                               test_kind)
            if not result:
                return False

            logger.debug("Finish config command.")

            logger.debug("Start check method")
            time.sleep(PROTOCOL_STABLE_WAIT)

            result = self.result_check(target_vnf,
                                       reference_vnf,
                                       test_kind,
                                       test_list)
            if not result:
                return False

            logger.debug("Finish check method.")

            # Clear the test configuration.
            self.util.reboot_v(target_vnf["vnf_name"])
            self.util.reboot_v(reference_vnf["vnf_name"])

        return True
