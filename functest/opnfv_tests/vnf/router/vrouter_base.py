#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

"""vrouter testing base class module"""

import datetime
import json
import logging
import os
import time

import pkg_resources

from functest.utils import config
from functest.opnfv_tests.vnf.router.test_controller import function_test_exec
from functest.opnfv_tests.vnf.router.utilvnf import Utilvnf

__author__ = "Shuya Nakama <shuya.nakama@okinawaopenlabs.org>"

REBOOT_WAIT = 30


class VrouterOnBoardingBase(object):
    """vrouter testing base class"""

    def __init__(self, case_name, **kwargs):
        self.logger = logging.getLogger(__name__)
        super(VrouterOnBoardingBase, self).__init__(**kwargs)
        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/router')
        self.data_dir = getattr(config.CONF, 'dir_router_data')
        self.result_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), case_name)
        self.util = Utilvnf()
        self.util_info = {}
        self.vnf_list = []
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def test_vnf(self):
        """vrouter test execution"""
        result = False
        test_result_data_list = []
        test_scenario_file_path = os.path.join(self.case_dir,
                                               self.util.test_scenario_yaml)
        test_scenario_list = self.util.get_test_scenario(
            test_scenario_file_path)
        for test_scenario in test_scenario_list:
            if test_scenario["test_type"] == "function_test":
                function_test_list = test_scenario["function_test_list"]
                for function_test in function_test_list:
                    test_list = function_test["test_list"]
                    target_vnf_name = function_test["target_vnf_name"]
                    for test_info in test_list:
                        self.logger.info(
                            "%s %s test.", test_info["protocol"],
                            test_info["test_kind"])
                        (result, result_data) = self.function_test_vrouter(
                            target_vnf_name, test_info)
                        test_result_data_list.append(result_data)
                        if not result:
                            break

        self.util.request_vm_delete(self.vnf_list)

        test_result_data = json.dumps(test_result_data_list, indent=4)

        return result, test_result_data

    def function_test_vrouter(self, target_vnf_name, test_info):
        """function test execution"""

        test_protocol = test_info["protocol"]
        test_list = test_info[test_protocol]

        vnf_info_list = self.get_vnf_info_list(target_vnf_name)
        self.vnf_list = vnf_info_list

        self.logger.debug("request vnf's reboot.")
        self.util.request_vnf_reboot(vnf_info_list)
        time.sleep(REBOOT_WAIT)

        target_vnf = self.util.get_target_vnf(vnf_info_list)

        reference_vnf_list = self.util.get_reference_vnf_list(vnf_info_list)

        test_exec = function_test_exec.FunctionTestExec(self.util_info)

        # start test
        start_time_ts = time.time()
        self.logger.info("vRouter test Start Time:'%s'", (
            datetime.datetime.fromtimestamp(start_time_ts).strftime(
                '%Y-%m-%d %H:%M:%S')))

        (result, test_result_data) = test_exec.run(target_vnf,
                                                   reference_vnf_list,
                                                   test_info,
                                                   test_list)

        end_time_ts = time.time()
        duration = round(end_time_ts - start_time_ts, 1)
        self.logger.info("vRouter test duration :'%s'", duration)

        return result, test_result_data

    def get_vnf_info_list(self, target_vnf_name):
        # pylint: disable=unused-argument,no-self-use
        vnf_info_list = []
        return vnf_info_list
