#!/usr/bin/env python
#
# Copyright (c) 2017 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
import json
import os

import requests

import functest.core.vnf_base as vnf_base
from functest.utils.constants import CONST
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils


class ImsOnBoardingBase(vnf_base.VnfOnBoardingBase):

    def __init__(self, project='functest', case='', repo='', cmd=''):
        self.logger = ft_logger.Logger(__name__).getLogger()
        super(ImsOnBoardingBase, self).__init__(project, case, repo, cmd)
        self.case_dir = os.path.join(CONST.dir_functest_test, 'vnf', 'ims')
        self.data_dir = CONST.dir_ims_data
        self.result_dir = os.path.join(CONST.dir_results, case)
        self.test_dir = CONST.dir_repo_vims_test

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

    def config_ellis(self, ellis_ip, signup_code='secret', two_numbers=False):
        output_dict = {}
        self.logger.info('Configure Ellis: %s', ellis_ip)
        output_dict['ellis_ip'] = ellis_ip
        account_url = 'http://{0}/accounts'.format(ellis_ip)
        params = {"password": "functest",
                  "full_name": "opnfv functest user",
                  "email": "functest@opnfv.org",
                  "signup_code": signup_code}
        rq = requests.post(account_url, data=params)
        output_dict['login'] = params
        if rq.status_code != 201 and rq.status_code != 409:
            raise Exception("Unable to create an account for number"
                            " provision: %s" % rq.json()['reason'])
        self.logger.info('Account is created on Ellis: %s', params)

        session_url = 'http://{0}/session'.format(ellis_ip)
        session_data = {
            'username': params['email'],
            'password': params['password']
        }
        rq = requests.post(session_url, data=session_data)
        if rq.status_code != 201:
            raise Exception('Failed to get cookie for Ellis')
        cookies = rq.cookies
        self.logger.info('Cookies: %s' % cookies)

        number_url = 'http://{0}/accounts/{1}/numbers'.format(
                     ellis_ip,
                     params['email'])
        self.logger.info('Create 1st calling number on Ellis')
        number_res = self.create_ellis_number(number_url, cookies)
        output_dict['number'] = number_res

        if two_numbers:
            self.logger.info('Create 2nd calling number on Ellis')
            number_res = self.create_ellis_number(number_url, cookies)
            output_dict['number2'] = number_res

        return output_dict

    def create_ellis_number(self, number_url, cookies):
        rq = requests.post(number_url, cookies=cookies)

        if rq.status_code != 200:
            raise Exception("Unable to create a number: %s"
                            % rq.json()['reason'])
        number_res = rq.json()
        self.logger.info('Calling number is created: %s', number_res)
        return number_res

    def run_clearwater_live_test(self, dns_ip, bono_ip, ellis_ip,
                                 public_domain, signup_code='secret'):
        self.logger.info('Run Clearwater live test')
        nameservers = ft_utils.get_resolvconf_ns()
        resolvconf = ""
        for ns in nameservers:
            resolvconf += "\nnameserver " + ns

        script = ('echo -e "nameserver {0}{1}" > /etc/resolv.conf;'
                  'source /etc/profile.d/rvm.sh;'
                  'cd {2};'
                  'rake test[{3}] SIGNUP_CODE={4}'
                  ' PROXY={5} ELLIS={6}'
                  ' --trace'
                  .format(dns_ip,
                          resolvconf,
                          self.test_dir,
                          public_domain,
                          signup_code,
                          bono_ip,
                          ellis_ip))

        cmd = "/bin/bash -c '{0}'".format(script)
        self.logger.info(cmd)
        output_file = os.path.join(self.result_dir, "ims_test_output.txt")
        ft_utils.execute_command(cmd,
                                 error_msg='Clearwater live test failed',
                                 output_file=output_file)

        f = open(output_file, 'r')
        result = f.read()
        if result != "":
            self.logger.debug(result)

        vims_test_result = ""
        tempFile = os.path.join(self.test_dir, "temp.json")
        try:
            self.logger.debug("Trying to load test results")
            with open(tempFile) as f:
                vims_test_result = json.load(f)
            f.close()
        except Exception:
            self.logger.error("Unable to retrieve test results")

        try:
            os.remove(tempFile)
        except Exception:
            self.logger.error("Deleting file failed")

        return vims_test_result

