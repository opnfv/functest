#!/usr/bin/env python

# Copyright (c) 2016 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""Juju testcase implementation."""

import logging
import os
import time
import json
import sys
from copy import deepcopy
import yaml

from functest.utils.constants import CONST
import functest.utils.openstack_utils as os_utils
from functest.opnfv_tests.openstack.snaps import snaps_utils

from snaps.openstack.os_credentials import OSCreds
from snaps.openstack.create_network import (NetworkSettings,
                                            SubnetSettings, OpenStackNetwork)
from snaps.openstack.create_router import (RouterSettings, OpenStackRouter)
from snaps.openstack.create_flavor import (FlavorSettings, OpenStackFlavor)
from snaps.openstack.create_image import (ImageSettings, OpenStackImage)
import pkg_resources
from snaps.openstack.tests import openstack_tests

import functest.core.vnf as vnf

__author__ = "Amarendra Meher <amarendra@rebaca.com>"


class JujuEpc(vnf.VnfOnBoarding):
    """Abot EPC deployed with JUJU Orchestrator Case"""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "juju_epc"
        super(JujuEpc, self).__init__(**kwargs)

        # Retrieve the configuration
        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/epc')
        try:
            self.config = CONST.__getattribute__(
                'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")
        config_file = os.path.join(self.case_dir, self.config)
        self.orchestrator = dict(
            requirements=get_config("orchestrator.requirements", config_file),
        )

        self.created_object = []
        self.snaps_creds = ''

        self.os_creds = openstack_tests.get_credentials(
            os_env_file=CONST.__getattribute__('openstack_creds'))

        self.details['orchestrator'] = dict(
            name=get_config("orchestrator.name", config_file),
            version=get_config("orchestrator.version", config_file),
            status='ERROR',
            result=''
        )

        self.vnf = dict(
            descriptor=get_config("vnf.descriptor", config_file),
            requirements=get_config("vnf.requirements", config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=get_config("vnf.name", config_file),
            version=get_config("vnf.version", config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)

        self.details['test_vnf'] = dict(
            name=get_config("vnf_test_suite.name", config_file),
            version=get_config("vnf_test_suite.version", config_file),
            tag_name=get_config("vnf_test_suite.tag_name", config_file)
        )
        self.images = get_config("tenant_images", config_file)
        self.__logger.info("Images needed for vEPC: %s", self.images)
        self.keystone_client = os_utils.get_keystone_client()
        self.glance_client = os_utils.get_glance_client()
        self.neutron_client = os_utils.get_neutron_client()
        self.nova_client = os_utils.get_nova_client()

    def prepare(self):
        """Prepare testcase (Additional pre-configuration steps)."""
        self.__logger.debug("OS Credentials: %s", os_utils.get_credentials())

        if os_utils.get_credentials()['project_name'] == self.tenant_name:
            self.creds = {
                "tenant": self.tenant_name,
                "username": os_utils.get_credentials()['username'],
                "password": os_utils.get_credentials()['password'],
                "auth_url": os_utils.get_credentials()['auth_url']
            }
        else:
            super(JujuEpc, self).prepare()

        self.__logger.debug("Self Creds: %s", self.creds)
        self.__logger.info("Additional pre-configuration steps")

        self.snaps_creds = OSCreds(
            username=self.creds['username'],
            password=self.creds['password'],
            auth_url=self.creds['auth_url'],
            project_name=self.creds['tenant'],
            identity_api_version=int(os_utils.get_keystone_client_version()))

        cmd = "sed -i 's#endpoint:.*#endpoint: {}#g' {}/abot_epc_\
cloud.yaml".format(self.creds['auth_url'], self.case_dir)
        os.system(cmd)
        if self.snaps_creds.identity_api_version == 3:
            cmd = "sed -i '/username/a\      user-domain-name: {}' {}/abot_" \
                  "epc_credential.yaml".format(os_utils.get_credentials()
                                               ['user_domain_name'],
                                               self.case_dir)
            os.system(cmd)
            cmd = "sed -i '/username/a\      project-domain-name: {}' {}" \
                  "/abot_epc_credential.yaml".format(os_utils.get_credentials()
                                                     ['project_domain_name'],
                                                     self.case_dir)
            os.system(cmd)
        os.system('apt-get -y install \
                   {}'.format(self.orchestrator['requirements']['pip']))
        os.system('pip3 install {}'.format(self.orchestrator
                                           ['requirements']['pip3_packages']))
        self.__logger.info("Upload some OS images if it doesn't exist")
        for image_name, image_url in self.images.iteritems():
            self.__logger.info("image: %s, url: %s", image_name, image_url)
            if image_url and image_name:
                image_creator = OpenStackImage(
                    self.snaps_creds,
                    ImageSettings(name=image_name,
                                  image_user='cloud',
                                  img_format='qcow2',
                                  url=image_url))
                image_creator.create()
                self.created_object.append(image_creator)

    def deploy_orchestrator(self):
        self.__logger.info("Deployed Orchestrator")
        private_net_name = CONST.__getattribute__(
            'vnf_{}_private_net_name'.format(self.case_name))
        private_subnet_name = CONST.__getattribute__(
            'vnf_{}_private_subnet_name'.format(self.case_name))
        private_subnet_cidr = CONST.__getattribute__(
            'vnf_{}_private_subnet_cidr'.format(self.case_name))
        abot_router = CONST.__getattribute__(
            'vnf_{}_external_router'.format(self.case_name))
        dns_nameserver = CONST.__getattribute__(
            'vnf_{}_dns_nameserver'.format(self.case_name))
        ext_net_name = CONST.__getattribute__(
            'vnf_{}_external_network_name'.format(self.case_name))

        self.__logger.info("Creating full network ...")
        subnet_settings = SubnetSettings(name=private_subnet_name,
                                         cidr=private_subnet_cidr,
                                         dns_nameservers=dns_nameserver)
        network_settings = NetworkSettings(name=private_net_name,
                                           subnet_settings=[subnet_settings])
        network_creator = OpenStackNetwork(self.snaps_creds, network_settings)
        network_creator.create()
        self.created_object.append(network_creator)

        if ext_net_name:
            self.__logger.info("External network name %s", ext_net_name)
        else:
            ext_net_name = snaps_utils.get_ext_net_name(self.snaps_creds)

        self.__logger.info("Creating network Router ....")
        router_creator = OpenStackRouter(
            self.snaps_creds,
            RouterSettings(
                name=abot_router,
                external_gateway=ext_net_name,
                internal_subnets=[subnet_settings.name]))
        router_creator.create()
        self.created_object.append(router_creator)
        self.__logger.info("Creating Flavor ....")
        flavor_settings = FlavorSettings(
            name=self.orchestrator['requirements']['flavor']['name'],
            ram=self.orchestrator['requirements']['flavor']['ram_min'],
            disk=10,
            vcpus=1)
        flavor_creator = OpenStackFlavor(self.snaps_creds, flavor_settings)
        self.__logger.info("Juju Bootstrap: Skip creation of flavors")
        flavor_creator.create()
        self.created_object.append(flavor_creator)
        self.__logger.info("Installing Dependency Packages .......")
        os.system('apt-get -y install {}'.format(self.orchestrator
                                                 ['requirements']
                                                 ['dep_package']))
        os.system('add-apt-repository -y {}'.format(self.orchestrator
                                                    ['requirements']
                                                    ['repo_link']))
        os.system('apt-get -y update')
        os.system('apt-get -y install {}'.format(self.details
                                                 ['orchestrator']
                                                 ['name']))
        self.__logger.info("Creating Cloud for Abot-epc .....")
        os.system('juju add-cloud abot-epc -f {}/abot_'
                  'epc_cloud.yaml'.format(self.case_dir))
        os.system('juju add-credential abot-epc -f {}/abot'
                  '_epc_credential.yaml'.format(self.
                                                case_dir))
        for image_name, image_url in self.images.iteritems():
            self.__logger.info("Generating Metadata for %s", image_name)
            image_id = os_utils.get_image_id(self.glance_client, image_name)
            os.system('juju metadata generate-image -d ~ -i {} -s {} -r '
                      'RegionOne -u {}'.format(image_id,
                                               image_name,
                                               self.creds['auth_url']))
        net_id = os_utils.get_network_id(self.neutron_client, private_net_name)
        self.__logger.info("Credential information  : %s", net_id)
        juju_bootstrap_command = 'juju bootstrap abot-epc abot-controller ' \
                                 '--config network={} --metadata-source ~  ' \
                                 '--constraints mem=2G --bootstrap-series ' \
                                 'trusty ' \
                                 '--config use-floating-ip=true'. \
            format(net_id)
        os.system(juju_bootstrap_command)
        return True

    def deploy_vnf(self):
        """Deploy ABOT-OAI-EPC."""
        self.__logger.info("Upload VNFD")
        descriptor = self.vnf['descriptor']
        self.__logger.info("Get or create flavor for all Abot-EPC")
        flavor_settings = FlavorSettings(
            name=self.vnf['requirements']['flavor']['name'],
            ram=self.vnf['requirements']['flavor']['ram_min'],
            disk=10,
            vcpus=1)
        flavor_creator = OpenStackFlavor(self.snaps_creds, flavor_settings)
        flavor_creator.create()
        self.created_object.append(flavor_creator)
        self.__logger.info("Deploying Abot-epc bundle file ...")
        os.system('juju deploy {}'.format('/' + descriptor.get('file_name')))
        self.__logger.info("Waiting for instances .....")
        status = os.system('juju-wait')
        self.__logger.info("juju wait completed: %s", status)
        self.__logger.info("Deployed Abot-epc on Openstack")
        if status == 0:
            instances = self.nova_client.servers.list()
            for items in instances:
                metadata = get_instance_metadata(self.nova_client, items)
                if 'juju-units-deployed' in metadata:
                    sec_group = 'juju-' + metadata['juju-controller-uuid'] + \
                                '-' + metadata['juju-model-uuid']
                    self.sec_group_id = os_utils.get_security_group_id(
                        self.neutron_client, sec_group)
                    break
            self.__logger.info("Adding Security group rule....")
            os_utils.create_secgroup_rule(self.neutron_client,
                                          self.sec_group_id, 'ingress', 132)
            self.__logger.info("Copying the feature files to Abot_node ")
            os.system('juju scp -- -r {}/featureFiles abot-'
                      'epc-basic/0:~/'.format(self.case_dir))
            self.__logger.info("Copying the feature files in Abot_node ")
            os.system("juju ssh abot-epc-basic/0 'sudo rsync -azvv "
                      "~/featureFiles /etc/rebaca-test-suite"
                      "/featureFiles'")
            count = 0
            while count < 10:
                epcstatus = os.system('juju status oai-epc | '
                                      'grep OAI\ EPC\ is\ running')
                if epcstatus == 0:
                    break
                else:
                    time.sleep(60)
                    count = count + 1
            os.system('juju-wait')
            return True
        else:
            return False

    def test_vnf(self):
        start_time = time.time()
        self.__logger.info("Running VNF Test cases....")
        os.system('juju run-action abot-epc-basic/0 run '
                  'tagnames={}'.format(self.details['test_vnf']['tag_name']))
        os.system('juju-wait')
        duration = time.time() - start_time
        self.__logger.info("Getting results from Abot node....")
        os.system('juju scp abot-epc-basic/0:/var/lib/abot-'
                  'epc-basic/artifacts/TestResults.json {}/.'
                  .format(self.case_dir))
        self.__logger.info("Parsing the Test results...")
        res = process_abot_test_result('{}/TestResults.\
json'.format(self.case_dir))
        short_result = sig_test_format(res)
        self.__logger.info(short_result)
        self.details['test_vnf'].update(status='PASS',
                                        result=short_result,
                                        full_result=res,
                                        duration=duration)

        self.__logger.info("Test VNF result: Passed: %d, Failed:\
%d, Skipped: %d", short_result['passed'],
                           short_result['failures'], short_result['skipped'])
        return True

    def clean(self):
        try:
            if not self.orchestrator['requirements']['preserve_setup']:
                descriptor = self.vnf['descriptor']
                self.__logger.info("Removing deployment files...")
                os.system('rm {}'.format(self.case_dir + '/' +
                                         descriptor.get('file_name')))
                os.system('rm {}'.format(self.case_dir + '/' +
                                         'TestResults.json'))
                os.system("sed -i '/project-domain-name/Q' {}/abot_epc"
                          "credential.yaml".format(self.case_dir))
                self.__logger.info("Destroying Orchestrator...")
                os.system('juju destroy-controller -y abot-controller '
                          '--destroy-all-models')
                self.__logger.info("Uninstalling dependency packages...")
                os.system('dpkg --configure -a')
                os.system('apt-get -y remove {}'.format(self.details
                                                        ['orchestrator']
                                                        ['name']))
                os.system('apt-get -y remove {}'.format(self.orchestrator
                                                        ['requirements']
                                                        ['dep_package']))
                os.system('pip3 uninstall -y {}'.format(self.orchestrator
                                                        ['requirements']
                                                        ['pip3_packages']))
                os.system('apt-get -y remove {}'.format(self.orchestrator
                                                        ['requirements']
                                                        ['pip']))
                os.system('apt-get -y autoremove')
        except:
            self.__logger.warn("Some issue during the undeployment ..")
            self.__logger.warn("Tenant clean continue ..")

        if not self.orchestrator['requirements']['preserve_setup']:
            self.__logger.info('Remove the Abot_epc OS object ..')
            for creator in reversed(self.created_object):
                try:
                    creator.clean()
                except Exception as exc:
                    self.__logger.error('Unexpected error cleaning - %s', exc)

            self.__logger.info("Releasing all the floating IPs")
            user_id = os_utils.get_user_id(self.keystone_client,
                                           self.tenant_name)
            floating_ips = os_utils.get_floating_ips(self.neutron_client)
            tenant_id = os_utils.get_tenant_id(self.keystone_client,
                                               self.tenant_name)
            self.__logger.info("USER ID : %s", user_id)
            self.__logger.info("FLOATING IP : %s", floating_ips)
            self.__logger.info("TENANT ID : %s", tenant_id)
            for item in floating_ips:
                if item['tenant_id'] == tenant_id:
                    os_utils.delete_floating_ip(self.neutron_client,
                                                item['id'])
            self.__logger.info("Cleaning Projects and Users")
            if not self.exist_obj['tenant']:
                os_utils.delete_tenant(self.keystone_client,
                                       tenant_id)
            if not self.exist_obj['user']:
                os_utils.delete_user(self.keystone_client,
                                     user_id)

        return True


# ----------------------------------------------------------
#
#               YAML UTILS
#
# -----------------------------------------------------------
def get_config(parameter, file_path):
    """
    Returns the value of a given parameter in file.yaml
    parameter must be given in string format with dots
    Example: general.openstack.image_name
    """
    with open(file_path) as config_file:
        file_yaml = yaml.safe_load(config_file)
    config_file.close()
    value = file_yaml
    for element in parameter.split("."):
        value = value.get(element)
        if value is None:
            raise ValueError("The parameter %s is not defined in"
                             " reporting.yaml" % parameter)
    return value


def sig_test_format(sig_test):
    """
    Process the signaling result to have a short result
    """
    nb_passed = 0
    nb_failures = 0
    nb_skipped = 0
    for data_test in sig_test:
        if data_test['result'] == "passed":
            nb_passed += 1
        elif data_test['result'] == "failed":
            nb_failures += 1
        elif data_test['result'] == "skipped":
            nb_skipped += 1
    total_sig_test_result = {}
    total_sig_test_result['passed'] = nb_passed
    total_sig_test_result['failures'] = nb_failures
    total_sig_test_result['skipped'] = nb_skipped
    return total_sig_test_result


def process_abot_test_result(file_path):
    """ Process ABoT Result """
    with open(file_path) as test_result:
        data = json.load(test_result)
        res = []
        for tests in data:
            tests = update_data(tests)
            try:
                flatten_steps = tests['elements'][0].pop('flatten_steps')
                for steps in flatten_steps:
                    steps['result'] = steps['step_status']
                    res.append(steps)
            except:
                logging.error("Could not post data to ElasticSearch host")
                raise
        return res


def update_data(obj):
    """ Update Result data"""
    try:
        obj['feature_file'] = os.path.splitext(os.path.basename(obj['uri']))[0]

        for element in obj['elements']:
            element['final_result'] = "passed"
            element['flatten_steps'] = []

            for step in element['steps']:
                temp_dict = {}
                step['result'][step['result']['status']] = 1
                if step['result']['status'].lower() in ['fail', 'failed']:
                    element['final_result'] = "failed"

                temp_dict['feature_file'] = obj['feature_file']
                temp_dict['step_name'] = step['name']
                temp_dict['step_status'] = step['result']['status']
                temp_dict['step_duration'] = step['result'].get('duration', 0)
                temp_dict['step_' + step['result']['status']] = 1
                element['flatten_steps'].append(deepcopy(temp_dict))

            # Need to put the tag in OBJ and not ELEMENT
            if 'tags' in obj:
                element['tags'] = deepcopy(obj['tags'])
                for tag in obj['tags']:
                    element[tag['name']] = 1
            else:
                for tag in element['tags']:
                    element[tag['name']] = 1

    except:
        logging.error("Error in updating data, %s" % (sys.exc_info()[0]))
        raise

    return obj


def get_instance_metadata(nova_client, instance):
    """ Get instance Metadata - Instance ID """
    try:
        instance = nova_client.servers.get(instance.id)
        return instance.metadata
    except Exception as e:
        logging.error("Error [get_instance_status(nova_client)]: %s" % e)
        return None
