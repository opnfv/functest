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
import shlex
import shutil
import subprocess
import time

import pkg_resources
import requests

from functest.utils import config
import functest.utils.functest_utils as ft_utils

__author__ = ("Valentin Boucher <valentin.boucher@orange.com>, "
              "Helen Yao <helanyao@gmail.com>")


class ClearwaterTesting(object):
    """vIMS clearwater base usable by several orchestrators"""

    def __init__(self, case_name, ellis_ip):
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

    def availability_check_by_creating_numbers(self,
                                               signup_code='secret',
                                               two_numbers=False):
        """Create one or two numbers"""
        assert self.ellis_ip
        output_dict = {}
        self.logger.debug('Ellis IP: %s', self.ellis_ip)
        output_dict['ellis_ip'] = self.ellis_ip
        account_url = 'http://{0}/accounts'.format(self.ellis_ip)
        params = {"password": "functest",
                  "full_name": "opnfv functest user",
                  "email": "functest@opnfv.org",
                  "signup_code": signup_code}
        output_dict['login'] = params

        number_res = self._create_ellis_account(account_url, params)
        output_dict['number'] = number_res

        session_url = 'http://{0}/session'.format(self.ellis_ip)
        session_data = {
            'username': params['email'],
            'password': params['password'],
            'email': params['email']
        }
        cookies = self._get_ellis_session_cookies(session_url, session_data)

        number_url = 'http://{0}/accounts/{1}/numbers'.format(
            self.ellis_ip, params['email'])
        self.logger.debug('Create 1st calling number on Ellis')
        number_res = self._create_ellis_number(number_url, cookies)

        if two_numbers:
            self.logger.debug('Create 2nd calling number on Ellis')
            number_res = self._create_ellis_number(number_url, cookies)
            output_dict['number2'] = number_res

        return output_dict

    def _create_ellis_account(self, account_url, params):
        i = 50
        for iloop in range(i):
            try:
                req = requests.post(account_url, data=params)
                if req.status_code == 201:
                    account_res = req.json()
                    self.logger.info(
                        'Account %s is created on Ellis\n%s',
                        params.get('full_name'), account_res)
                    return account_res
                else:
                    raise Exception("Cannot create ellis account")
            except Exception:  # pylint: disable=broad-except
                self.logger.info(
                    "try %s: cannot create ellis account", iloop + 1)
                time.sleep(25)
        raise Exception(
            "Unable to create an account {}".format(
                params.get('full_name')))

    def _get_ellis_session_cookies(self, session_url, params):
        i = 15
        for iloop in range(i):
            try:
                req = requests.post(session_url, data=params)
                if req.status_code == 201:
                    cookies = req.cookies
                    self.logger.debug('cookies: %s', cookies)
                    return cookies
                else:
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
                else:
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

    def run_clearwater_live_test(self, dns_ip, public_domain,
                                 bono_ip=None, ellis_ip=None,
                                 signup_code='secret'):
        """Run the Clearwater live tests

        It first runs dnsmasq to reach clearwater services by FQDN and then the
        Clearwater live tests. All results are saved in ims_test_output.txt.

        Returns:
            - a dict containing the overall results
            - None on error
        """
        # pylint: disable=too-many-locals,too-many-arguments
        self.logger.info('Run Clearwater live test')
        dns_file = '/etc/resolv.conf'
        dns_file_bak = '/etc/resolv.conf.bak'
        self.logger.debug('Backup %s -> %s', dns_file, dns_file_bak)
        shutil.copy(dns_file, dns_file_bak)
        cmd = ("dnsmasq -d -u root --server=/clearwater.opnfv/{0} "
               "-r /etc/resolv.conf.bak".format(dns_ip))
        dnsmasq_process = subprocess.Popen(shlex.split(cmd))
        script = ('echo -e "nameserver {0}" > {1};'
                  'cd {2};'
                  'rake test[{3}] SIGNUP_CODE={4}'
                  .format('127.0.0.1',
                          dns_file,
                          self.test_dir,
                          public_domain,
                          signup_code))
        if bono_ip and ellis_ip:
            subscript = ' PROXY={0} ELLIS={1}'.format(bono_ip, ellis_ip)
            script = '{0}{1}'.format(script, subscript)
        script = ('{0}{1}'.format(script, ' --trace'))
        cmd = "/bin/bash -c '{0}'".format(script)
        self.logger.debug('Live test cmd: %s', cmd)
        output_file = os.path.join(self.result_dir, "ims_test_output.txt")
        ft_utils.execute_command(cmd,
                                 error_msg='Clearwater live test failed',
                                 output_file=output_file)
        dnsmasq_process.kill()
        with open(dns_file_bak, 'r') as bak_file:
            result = bak_file.read()
            with open(dns_file, 'w') as dfile:
                dfile.write(result)

        with open(output_file, 'r') as ofile:
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
        except Exception:  # pylint: disable=broad-except
            self.logger.exception("Cannot parse live tests results")
            return None
        return vims_test_result
