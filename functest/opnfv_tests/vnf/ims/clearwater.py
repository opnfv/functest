#!/usr/bin/env python
#
# Copyright (c) 2017 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""Ease testing any Clearwater deployment"""

import logging
import os
import re
import time

import pkg_resources
import requests

from functest.utils import config
import functest.utils.functest_utils as ft_utils

__author__ = ("Valentin Boucher <valentin.boucher@orange.com>, "
              "Helen Yao <helanyao@gmail.com>")


class ClearwaterTesting():
    """vIMS clearwater base usable by several orchestrators"""

    def __init__(self, case_name, bono_ip, ellis_ip):
        self.logger = logging.getLogger(__name__)
        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/ims')
        self.data_dir = getattr(config.CONF, 'dir_ims_data')
        self.result_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), case_name)
        self.test_dir = getattr(config.CONF, 'dir_repo_vims_test')

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

        self.ellis_ip = ellis_ip
        self.bono_ip = bono_ip

    def availability_check(self, signup_code='secret', two_numbers=False):
        """Create one or two numbers"""
        assert self.ellis_ip
        output_dict = {}
        self.logger.debug('Ellis IP: %s', self.ellis_ip)
        output_dict['ellis_ip'] = self.ellis_ip
        account_url = f'http://{self.ellis_ip}/accounts'
        params = {"password": "functest",
                  "full_name": "opnfv functest user",
                  "email": "functest@opnfv.org",
                  "signup_code": signup_code}
        output_dict['login'] = params

        number_res = self._create_ellis_account(account_url, params)
        output_dict['number'] = number_res

        session_url = f'http://{self.ellis_ip}/session'
        session_data = {
            'username': params['email'],
            'password': params['password'],
            'email': params['email']
        }
        cookies = self._get_ellis_session_cookies(session_url, session_data)

        number_url = (
            f"http://{self.ellis_ip}/accounts/{params['email']}/numbers")
        self.logger.debug('Create 1st calling number on Ellis')
        number_res = self._create_ellis_number(number_url, cookies)

        if two_numbers:
            self.logger.debug('Create 2nd calling number on Ellis')
            number_res = self._create_ellis_number(number_url, cookies)
            output_dict['number2'] = number_res

        return output_dict

    def _create_ellis_account(self, account_url, params):
        i = 80
        for iloop in range(i):
            try:
                req = requests.post(account_url, data=params)
                if req.status_code == 201:
                    account_res = req.json()
                    self.logger.info(
                        'Account %s is created on Ellis\n%s',
                        params.get('full_name'), account_res)
                    return account_res
                raise Exception("Cannot create ellis account")
            except Exception:  # pylint: disable=broad-except
                self.logger.info(
                    "try %s: cannot create ellis account", iloop + 1)
                time.sleep(30)
        raise Exception(
            f"Unable to create an account {params.get('full_name')}")

    def _get_ellis_session_cookies(self, session_url, params):
        i = 15
        for iloop in range(i):
            try:
                req = requests.post(session_url, data=params)
                if req.status_code == 201:
                    cookies = req.cookies
                    self.logger.debug('cookies: %s', cookies)
                    return cookies
                raise Exception('Failed to get cookies for Ellis')
            except Exception:  # pylint: disable=broad-except
                self.logger.info(
                    "try %s: cannot get cookies for Ellis", iloop + 1)
                time.sleep(10)
        raise Exception('Failed to get cookies for Ellis')

    def _create_ellis_number(self, number_url, cookies):
        i = 30
        for iloop in range(i):
            try:
                req = requests.post(number_url, cookies=cookies)
                if req.status_code == 200:
                    number_res = req.json()
                    self.logger.info(
                        'Calling number is created: %s', number_res)
                    return number_res
                if req and req.json():
                    reason = req.json()['reason']
                else:
                    reason = req
                self.logger.info("cannot create a number: %s", reason)
                raise Exception('Failed to create a number')
            except Exception:  # pylint: disable=broad-except
                self.logger.info(
                    "try %s: cannot create a number", iloop + 1)
                time.sleep(25)
        raise Exception('Failed to create a number')

    def run_clearwater_live_test(self, public_domain, signup_code='secret'):
        """Run the Clearwater live tests

        It first runs dnsmasq to reach clearwater services by FQDN and then the
        Clearwater live tests. All results are saved in ims_test_output.txt.

        Returns:
            - a dict containing the overall results
            - None on error
        """
        # pylint: disable=too-many-locals,too-many-arguments
        self.logger.info('Run Clearwater live test')
        script = (f'cd {self.test_dir};'
                  f'rake test[{public_domain}] SIGNUP_CODE={signup_code}')
        if self.bono_ip and self.ellis_ip:
            subscript = f' PROXY={self.bono_ip} ELLIS={self.ellis_ip}'
            script = f'{script}{subscript}'
        script = f'{script} --trace'
        cmd = f"/bin/sh -c '{script}'"
        self.logger.debug('Live test cmd: %s', cmd)
        output_file = os.path.join(self.result_dir, "ims_test_output.txt")
        ft_utils.execute_command(cmd,
                                 error_msg='Clearwater live test failed',
                                 output_file=output_file)

        with open(output_file, 'r', encoding='utf-8') as ofile:
            result = ofile.read()

        if result != "":
            self.logger.debug(result)

        vims_test_result = {}
        try:
            grp = re.search(
                r'^(\d+) failures out of (\d+) tests run.*\n'
                r'(\d+) tests skipped$', result, re.MULTILINE | re.DOTALL)
            assert grp
            vims_test_result["failures"] = int(grp.group(1))
            vims_test_result["total"] = int(grp.group(2))
            vims_test_result["skipped"] = int(grp.group(3))
            vims_test_result['passed'] = (
                int(grp.group(2)) - int(grp.group(3)) - int(grp.group(1)))
            if vims_test_result['total'] - vims_test_result['skipped'] > 0:
                vnf_test_rate = vims_test_result['passed'] / (
                    vims_test_result['total'] - vims_test_result['skipped'])
            else:
                vnf_test_rate = 0
        except Exception:  # pylint: disable=broad-except
            self.logger.exception("Cannot parse live tests results")
            return None, 0
        return vims_test_result, vnf_test_rate
