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
import functest.utils.openstack_utils as os_utils

from clearwater import Clearwater
from functest.utils.constants import CONST
from orchestrator_cloudify import Orchestrator


class ImsVnf(vnf_base.VnfOnBoardingBase):

    def __init__(self, project='functest', case='cloudify_ims',
                 repo='', cmd=''):
        super(ImsVnf, self).__init__(project, case, repo, cmd)
        self.logger = ft_logger.Logger("vIMS").getLogger()
        self.case_dir = os.path.join(CONST.functest_test, 'vnf/ims/')
        self.data_dir = CONST.dir_vIMS_data
        self.test_dir = CONST.dir_repo_vims_test

        self.orchestrator = dict(
            requirements=CONST.cloudify_requirements,
            blueprint=CONST.cloudify_blueprint,
            inputs=CONST.cloudify_inputs
        )

        self.vnf = dict(
            blueprint=CONST.clearwater_blueprint,
            deployment_name=CONST.clearwater_deployment_name,
            inputs=CONST.clearwater_inputs,
            requirements=CONST.clearwater_requirements
        )

        # vIMS Data directory creation
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def deploy_orchestrator(self, **kwargs):
        public_auth_url = os_utils.get_endpoint('identity')

        cfy = Orchestrator(self.data_dir, self.orchestrator.inputs)
        self.orchestrator.object = cfy

        if 'tenant_name' in self.creds.keys():
            tenant_name = self.creds['tenant_name']
        elif 'project_name' in self.creds.keys():
            tenant_name = self.creds['project_name']

        cfy.set_credentials(username=self.creds['username'],
                            password=self.creds['password'],
                            tenant_name=tenant_name,
                            auth_url=public_auth_url)

        # orchestrator VM flavor
        flavor_id = self.get_flavor("m1.large", self.orchestrator.requirements)
        if not flavor_id:
            self.logger.info("Available flavors are: ")
            self.pMsg(self.nova_client.flavor.list())
            self.step_failure("Failed to find required flavor"
                              "for this deployment")
        cfy.set_flavor_id(flavor_id)

        # orchestrator VM image
        if 'os_image' in self.orchestrator.requirements.keys():
            image_id = os_utils.get_image_id(
                self.glance_client, self.orchestrator.requirements['os_image'])
            if image_id == '':
                self.step_failure("Failed to find required OS image"
                                  " for cloudify manager")
        else:
            self.step_failure("Failed to find required OS image"
                              " for cloudify manager")

        cfy.set_image_id(image_id)

        ext_net = os_utils.get_external_net(self.neutron_client)
        if not ext_net:
            self.step_failure("Failed to get external network")

        cfy.set_external_network_name(ext_net)

        ns = ft_utils.get_resolvconf_ns()
        if ns:
            cfy.set_nameservers(ns)

        if 'compute' in self.nova_client.client.services_url:
            cfy.set_nova_url(self.nova_client.client.services_url['compute'])
        if self.neutron_client.httpclient.endpoint_url is not None:
            cfy.set_neutron_url(self.neutron_client.httpclient.endpoint_url)

        self.logger.info("Prepare virtualenv for cloudify-cli")
        cmd = "chmod +x " + self.case_dir + "create_venv.sh"
        ft_utils.execute_command(cmd)
        time.sleep(3)
        cmd = self.case_dir + "create_venv.sh " + self.data_dir
        ft_utils.execute_command(cmd)

        cfy.download_manager_blueprint(self.orchestrator.blueprint['url'],
                                       self.orchestrator.blueprint['branch'])

        cfy.deploy_manager()
        return {'status': 'PASS', 'result': ''}

    def deploy_vnf(self):
        cw = Clearwater(self.vnf.inputs, self.orchestrator.object, self.logger)
        self.vnf.object = cw

        self.logger.info("Collect flavor id for all clearwater vm")
        flavor_id = self.get_flavor("m1.small", self.vnf.requirements)
        if not flavor_id:
            self.logger.info("Available flavors are: ")
            self.pMsg(self.nova_client.flavor.list())
            self.step_failure("Failed to find required flavor"
                              " for this deployment")

        cw.set_flavor_id(flavor_id)

        # VMs image
        if 'os_image' in self.vnf.requirements.keys():
            image_id = os_utils.get_image_id(
                self.glance_client, self.vnf.requirements['os_image'])
            if image_id == '':
                self.step_failure("Failed to find required OS image"
                                  " for clearwater VMs")
        else:
            self.step_failure("Failed to find required OS image"
                              " for clearwater VMs")

        cw.set_image_id(image_id)

        ext_net = os_utils.get_external_net(self.neutron_client)
        if not ext_net:
            self.step_failure("Failed to get external network")

        cw.set_external_network_name(ext_net)

        cw.deploy_vnf()
        return {'status': 'PASS', 'result': ''}

    def test_vnf(self):
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
        self.vnf.object.undeploy_vnf()
        self.orchestrator.object.undeploy_manager()
        super(ImsVnf, self).clean()

    def get_flavor(self, flavor_name, requirements):
        try:
            flavor_id = os_utils.get_flavor_id(self.nova_client, flavor_name)
            if 'ram_min' in requirements.keys():
                flavor_id = os_utils.get_flavor_id_by_ram_range(
                    self.nova_client, requirements['ram_min'], 7500)

            if flavor_id == '':
                self.logger.error(
                    "Failed to find %s flavor. "
                    "Try with ram range default requirement !" % flavor_name)
                flavor_id = os_utils.get_flavor_id_by_ram_range(
                                    self.nova_client,
                                    4000, 10000)
            return flavor_id
        except:
            self.logger.error("Flavor '%s' not found." % self.flavor_name)
            self.logger.info("Available flavors are: ")
            self.pMsg(self.nova_client.flavor.list())
            return None
