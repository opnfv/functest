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
import sys
import time
import yaml

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
        self.case_dir = os.path.join(CONST.dir_functest_test, 'vnf/ims/')
        self.data_dir = CONST.dir_ims_data
        self.test_dir = CONST.dir_repo_vims_test

        # Retrieve the configuration
        try:
            self.config = CONST.__getattribute__(
                'vnf_{}_config'.format(self.case_name))
        except:
            raise Exception("VNF config file not found")

        config_file = self.case_dir + self.config
        self.orchestrator = dict(
            requirements=get_config("cloudify.requirements", config_file),
            blueprint=get_config("cloudify.blueprint", config_file),
            inputs=get_config("cloudify.inputs", config_file)
        )
        self.logger.debug("Orchestrator configuration: %s" % self.orchestrator)
        self.vnf = dict(
            blueprint=get_config("clearwater.blueprint", config_file),
            deployment_name=get_config("clearwater.deployment_name",
                                       config_file),
            inputs=get_config("clearwater.inputs", config_file),
            requirements=get_config("clearwater.requirements", config_file)
        )
        self.logger.debug("VNF configuration: %s" % self.vnf)

        self.images = get_config("tenant_images", config_file)
        self.logger.info("Images needed for vIMS: %s" % self.images)

        # vIMS Data directory creation
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def deploy_orchestrator(self, **kwargs):

        self.logger.info("Additional pre-configuration steps")
        self.neutron_client = os_utils.get_neutron_client(self.creds)
        self.glance_client = os_utils.get_glance_client(self.creds)
        self.keystone_client = os_utils.get_keystone_client(self.creds)
        self.nova_client = os_utils.get_nova_client(self.creds)

        # needs some images
        self.logger.info("Upload some OS images if it doesn't exist")
        temp_dir = os.path.join(self.data_dir, "tmp/")
        for image_name, image_url in self.images.iteritems():
            self.logger.info("image: %s, url: %s" % (image_name, image_url))
            try:
                image_id = os_utils.get_image_id(self.glance_client,
                                                 image_name)
                self.logger.debug("image_id: %s" % image_id)
            except:
                self.logger.error("Unexpected error: %s" % sys.exc_info()[0])

            if image_id == '':
                self.logger.info("""%s image doesn't exist on glance repository. Try
                downloading this image and upload on glance !""" % image_name)
                image_id = download_and_add_image_on_glance(self.glance_client,
                                                            image_name,
                                                            image_url,
                                                            temp_dir)
            if image_id == '':
                self.step_failure(
                    "Failed to find or upload required OS "
                    "image for this deployment")
        # Need to extend quota
        self.logger.info("Update security group quota for this tenant")
        tenant_id = os_utils.get_tenant_id(self.keystone_client,
                                           self.tenant_name)
        self.logger.debug("Tenant id found %s" % tenant_id)
        if not os_utils.update_sg_quota(self.neutron_client,
                                        tenant_id, 50, 100):
            self.step_failure("Failed to update security group quota" +
                              " for tenant " + self.tenant_name)
        self.logger.debug("group quota extended")

        # start the deployment of cloudify
        public_auth_url = os_utils.get_endpoint('identity')

        self.logger.debug("CFY inputs: %s" % self.orchestrator['inputs'])
        cfy = Orchestrator(self.data_dir, self.orchestrator['inputs'])
        self.orchestrator['object'] = cfy
        self.logger.debug("Orchestrator object created")

        self.logger.debug("Tenant name: %s" % self.tenant_name)

        cfy.set_credentials(username=self.tenant_name,
                            password=self.tenant_name,
                            tenant_name=self.tenant_name,
                            auth_url=public_auth_url)
        self.logger.info("Credentials set in CFY")

        # orchestrator VM flavor
        self.logger.info("Check Flavor is available, if not create one")
        self.logger.debug("Flavor details %s " %
                          self.orchestrator['requirements']['ram_min'])
        flavor_exist, flavor_id = os_utils.get_or_create_flavor(
            "m1.large",
            self.orchestrator['requirements']['ram_min'],
            '1',
            '1',
            public=True)
        self.logger.debug("Flavor id: %s" % flavor_id)

        if not flavor_id:
            self.logger.info("Available flavors are: ")
            self.logger.info(self.nova_client.flavor.list())
            self.step_failure("Failed to find required flavor"
                              "for this deployment")
        cfy.set_flavor_id(flavor_id)
        self.logger.debug("Flavor OK")

        # orchestrator VM image
        self.logger.debug("Orchestrator image")
        if 'os_image' in self.orchestrator['requirements'].keys():
            image_id = os_utils.get_image_id(
                self.glance_client,
                self.orchestrator['requirements']['os_image'])
            self.logger.debug("Orchestrator image id: %s" % image_id)
            if image_id == '':
                self.logger.error("CFY image not found")
                self.step_failure("Failed to find required OS image"
                                  " for cloudify manager")
        else:
            self.step_failure("Failed to find required OS image"
                              " for cloudify manager")

        cfy.set_image_id(image_id)
        self.logger.debug("Orchestrator image set")

        self.logger.debug("Get External network")
        ext_net = os_utils.get_external_net(self.neutron_client)
        self.logger.debug("External network: %s" % ext_net)
        if not ext_net:
            self.step_failure("Failed to get external network")

        cfy.set_external_network_name(ext_net)
        self.logger.debug("CFY External network set")

        self.logger.debug("get resolvconf")
        ns = ft_utils.get_resolvconf_ns()
        if ns:
            cfy.set_nameservers(ns)
            self.logger.debug("Resolvconf set")

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

        cfy.download_manager_blueprint(
            self.orchestrator['blueprint']['url'],
            self.orchestrator['blueprint']['branch'])

        cfy.deploy_manager()
        return {'status': 'PASS', 'result': ''}

    def deploy_vnf(self):
        cw = Clearwater(self.vnf.inputs, self.orchestrator.object, self.logger)
        self.vnf.object = cw

        self.logger.info("Collect flavor id for all clearwater vm")
        flavor_exist, flavor_id = os_utils.get_or_create_flavor(
            "m1.small",
            self.vnf['requirements']['ram_min'],
            '1',
            '1',
            public=True)
        self.logger.debug("Flavor id: %s" % flavor_id)
        if not flavor_id:
            self.logger.info("Available flavors are: ")
            self.logger.info(self.nova_client.flavor.list())
            self.step_failure("Failed to find required flavor"
                              " for this deployment")

        cw.set_flavor_id(flavor_id)

        # VMs image
        if 'os_image' in self.vnf.requirements.keys():
            image_id = os_utils.get_image_id(
                self.glance_client, self.vnf['requirements']['os_image'])
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

    def main(self, **kwargs):
        self.logger.info("Cloudify IMS VNF onboarding test starting")
        self.execute()
        self.logger.info("Cloudify IMS VNF onboarding test executed")
        if self.criteria is "PASS":
            return self.EX_OK
        else:
            return self.EX_RUN_ERROR

    def run(self):
        kwargs = {}
        return self.main(**kwargs)


# ----------------------------------------------------------
#
#               YAML UTILS
#
# -----------------------------------------------------------
def get_config(parameter, file):
    """
    Returns the value of a given parameter in file.yaml
    parameter must be given in string format with dots
    Example: general.openstack.image_name
    """
    with open(file) as f:
        file_yaml = yaml.safe_load(f)
    f.close()
    value = file_yaml
    for element in parameter.split("."):
        value = value.get(element)
        if value is None:
            raise ValueError("The parameter %s is not defined in"
                             " reporting.yaml" % parameter)
    return value


def download_and_add_image_on_glance(glance, image_name, image_url, data_dir):
    dest_path = data_dir
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    file_name = image_url.rsplit('/')[-1]
    if not ft_utils.download_url(image_url, dest_path):
        return False

    image = os_utils.create_glance_image(
        glance, image_name, dest_path + file_name)
    if not image:
        return False

    return image
