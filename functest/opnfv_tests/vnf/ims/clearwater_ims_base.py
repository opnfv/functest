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


class ClearwaterOnBoardingBase(object):
    """vIMS clearwater base usable by several orchestrators"""

    def __init__(self, case_name):
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

    def config_ellis(self, ellis_ip, signup_code='secret', two_numbers=False):
        """Create one or two numbers"""
        output_dict = {}
        self.logger.debug('Configure Ellis: %s', ellis_ip)
        output_dict['ellis_ip'] = ellis_ip
        account_url = 'http://{0}/accounts'.format(ellis_ip)
        params = {"password": "functest",
                  "full_name": "opnfv functest user",
                  "email": "functest@opnfv.org",
                  "signup_code": signup_code}
        req = requests.post(account_url, data=params)
        output_dict['login'] = params
        if req.status_code != 201 and req.status_code != 409:
            raise Exception(
                "Unable to create an account {}\n{}".format(
                    params, req.text))
        self.logger.debug(
            'Account %s is created on Ellis\n%s', params, req.json())

        session_url = 'http://{0}/session'.format(ellis_ip)
        session_data = {
            'username': params['email'],
            'password': params['password'],
            'email': params['email']
        }
        req = requests.post(session_url, data=session_data)
        if req.status_code != 201:
            raise Exception('Failed to get cookie for Ellis\n{}'.format(
                req.text))
        cookies = req.cookies
        self.logger.debug('Cookies: %s', cookies)

        number_url = 'http://{0}/accounts/{1}/numbers'.format(
            ellis_ip, params['email'])
        self.logger.debug('Create 1st calling number on Ellis')
        i = 30
        while req.status_code != 200 and i > 0:
            try:
                number_res = self._create_ellis_number(number_url, cookies)
                break
            except Exception:  # pylint: disable=broad-except
                if i == 1:
                    self.logger.exception("Unable to create a number")
                    raise Exception("Unable to create a number")
                self.logger.info("Unable to create a number. Retry ..")
                time.sleep(25)
            i = i - 1
        output_dict['number'] = number_res

        if two_numbers:
            self.logger.debug('Create 2nd calling number on Ellis')
            number_res = self._create_ellis_number(number_url, cookies)
            output_dict['number2'] = number_res

        return output_dict

    def _create_ellis_number(self, number_url, cookies):
        req = requests.post(number_url, cookies=cookies)

        if req.status_code != 200:
            if req and req.json():
                reason = req.json()['reason']
            else:
                reason = req
            raise Exception("Unable to create a number: %s" % reason)
        number_res = req.json()
        self.logger.info('Calling number is created: %s', number_res)
        return number_res

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
                r'(\d+) failures out of (\d+) tests run.*'
                r'(\d+) tests skipped', result, re.MULTILINE | re.DOTALL)
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
