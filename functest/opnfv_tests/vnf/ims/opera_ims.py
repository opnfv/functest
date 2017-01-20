#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import json
import os
import requests
import subprocess
import time

import functest.core.vnf_base as vnf_base
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
from functest.utils.constants import CONST


class ImsVnf(vnf_base.VnfOnBoardingBase):

    def __init__(self, project='functest', case='opera_ims',
                 repo='', cmd=''):
        super(ImsVnf, self).__init__(project, case, repo, cmd)
        self.logger = ft_logger.Logger("vIMS").getLogger()
        self.case_dir = os.path.join(CONST.functest_test, 'vnf/ims/')
        self.data_dir = CONST.dir_vIMS_data
        self.test_dir = CONST.dir_repo_vims_test

        # vIMS Data directory creation
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def deploy_orchestrator(self, **kwargs):
        # TODO
        # deploy open-O from Functest docker located on the Jumphost
        # you have admin rights on OpenStack SUT
        # you can cretae a VM, spawn docker on the jumphost
        # spawn docker on a VM in the SUT, ..up to you
        #
        # note: this step can be ignored
        # if Open-O is part of the installer
        self.logger.info("Deploy orchestrator: OK")

    def deploy_vnf(self):
        # TODO
        self.logger.info("Deploy VNF: OK")

    def test_vnf(self):
        # Adaptations probably needed
        # code used for cloudify_ims
        # ruby client on jumphost calling the vIMS on the SUT
        script = "source {0}venv_cloudify/bin/activate; "
        script += "cd {0}; "
        script += "cfy status | grep -Eo \"([0-9]{{1,3}}\.){{3}}[0-9]{{1,3}}\""
        cmd = "/bin/bash -c '" + script.format(self.data_dir) + "'"

        try:
            self.logger.debug("Trying to get clearwater manager IP ... ")
            mgr_ip = os.popen(cmd).read()
            mgr_ip = mgr_ip.splitlines()[0]
        except:
            self.step_failure("Unable to retrieve the IP of the "
                              "cloudify manager server !")

        api_url = "http://" + mgr_ip + "/api/v2"
        dep_outputs = requests.get(api_url + "/deployments/" +
                                   self.vnf.deployment_name + "/outputs")
        dns_ip = dep_outputs.json()['outputs']['dns_ip']
        ellis_ip = dep_outputs.json()['outputs']['ellis_ip']

        ellis_url = "http://" + ellis_ip + "/"
        url = ellis_url + "accounts"

        params = {"password": "functest",
                  "full_name": "opnfv functest user",
                  "email": "functest@opnfv.fr",
                  "signup_code": "secret"}

        rq = requests.post(url, data=params)
        i = 20
        while rq.status_code != 201 and i > 0:
            rq = requests.post(url, data=params)
            i = i - 1
            time.sleep(10)

        if rq.status_code == 201:
            url = ellis_url + "session"
            rq = requests.post(url, data=params)
            cookies = rq.cookies

        url = ellis_url + "accounts/" + params['email'] + "/numbers"
        if cookies != "":
            rq = requests.post(url, cookies=cookies)
            i = 24
            while rq.status_code != 200 and i > 0:
                rq = requests.post(url, cookies=cookies)
                i = i - 1
                time.sleep(25)

        if rq.status_code != 200:
            self.step_failure("Unable to create a number: %s"
                              % rq.json()['reason'])

        nameservers = ft_utils.get_resolvconf_ns()
        resolvconf = ""
        for ns in nameservers:
            resolvconf += "\nnameserver " + ns

        if dns_ip != "":
            script = ('echo -e "nameserver ' + dns_ip + resolvconf +
                      '" > /etc/resolv.conf; ')
            script += 'source /etc/profile.d/rvm.sh; '
            script += 'cd {0}; '
            script += ('rake test[{1}] SIGNUP_CODE="secret"')

            cmd = ("/bin/bash -c '" +
                   script.format(self.data_dir, self.inputs["public_domain"]) +
                   "'")
            output_file = "output.txt"
            f = open(output_file, 'w+')
            subprocess.call(cmd, shell=True, stdout=f,
                            stderr=subprocess.STDOUT)
            f.close()

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
            except:
                self.logger.error("Unable to retrieve test results")

            try:
                os.remove(tempFile)
            except:
                self.logger.error("Deleting file failed")

            if vims_test_result != '':
                return {'status': 'PASS', 'result': vims_test_result}
            else:
                return {'status': 'FAIL', 'result': ''}

    def clean(self):
        # TODO
        super(ImsVnf, self).clean()
