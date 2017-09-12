#!/usr/bin/env python

# Copyright (c) 2016 Rebaca and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""Juju testcase implementation."""

import logging
import shutil
import os
import time
import json
import sys
from copy import deepcopy
import yaml
import functest.utils.openstack_utils as os_utils
import functest.core.vnf as vnf
import pkg_resources

from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils.constants import CONST

from snaps.openstack.os_credentials import OSCreds
from snaps.openstack.create_network import (NetworkSettings,
                                            SubnetSettings, OpenStackNetwork)
from snaps.openstack.create_router import (RouterSettings, OpenStackRouter)
from snaps.openstack.create_flavor import (FlavorSettings, OpenStackFlavor)
from snaps.openstack.create_image import (ImageSettings, OpenStackImage)
from snaps.openstack.tests import openstack_tests

__author__ = "Amarendra Meher <amarendra@rebaca.com>"
__author__ = "Soumaya K Nayek <soumaya.nayek@rebaca.com>"


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

        super(JujuEpc, self).prepare()

        self.__logger.info("Additional pre-configuration steps")

        self.creds = {
            "tenant": self.tenant_name,
            "username": self.tenant_name,
            "password": self.tenant_name,
            "auth_url": os_utils.get_credentials()['auth_url']
            }

        self.snaps_creds = OSCreds(
            username=self.creds['username'],
            password=self.creds['password'],
            auth_url=self.creds['auth_url'],
            project_name=self.creds['tenant'],
            identity_api_version=int(os_utils.get_keystone_client_version()))

        cloud_data = {
            'url': self.creds['auth_url'],
            'pass': self.tenant_name,
            'tenant_n': self.tenant_name,
            'user_n': self.tenant_name
        }
        self.filename = os.path.join(self.case_dir, 'abot-epc.yaml')
        self.__logger.info("Cretae  %s to add cloud info", self.filename)
        write_config(self.filename, CLOUD_TEMPLATE, **cloud_data)

        if self.snaps_creds.identity_api_version == 3:
            append_config(self.filename, '{}'.format(
                os_utils.get_credentials()['project_domain_name']),
                          '{}'.format(os_utils.get_credentials()
                                      ['user_domain_name']))

        self.__logger.info("Upload some OS images if it doesn't exist")
        for image_name, image_file in self.images.iteritems():
            self.__logger.info("image: %s, file: %s", image_name, image_file)
            if image_file and image_name:
                image_creator = OpenStackImage(
                    self.snaps_creds,
                    ImageSettings(name=image_name,
                                  image_user='cloud',
                                  img_format='qcow2',
                                  image_file=image_file))
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
        source_dir = "/src/epc-requirements/juju_bin_build"
        if os.path.exists(source_dir):
            shutil.rmtree(source_dir)
        os.makedirs(source_dir)
        os.environ['GOPATH'] = str(source_dir)
        os.environ['GOBIN'] = str(source_dir) + "/bin"
        os.environ['PATH'] = ((os.path.expandvars('$GOPATH')) + ":" +
                              (os.path.expandvars('$GOBIN')) + ":" +
                              (os.path.expandvars('$PATH')))
        os.system('go get -d -v github.com/juju/juju/...')
        os.chdir(source_dir + "/src" + "/github.com" + "/juju" + "/juju")
        os.system('git checkout tags/juju-2.2.5')
        os.system('go get github.com/rogpeppe/godeps')
        os.system('godeps -u dependencies.tsv')
        os.system('go install -v github.com/juju/juju/...')
        self.__logger.info("Creating Cloud for Abot-epc .....")
        os.system('juju add-cloud abot-epc -f {}'.format(self.filename))
        os.system('juju add-credential abot-epc -f {}'.format(self.filename))
        for image_name in self.images.keys():
            self.__logger.info("Generating Metadata for %s", image_name)
            image_id = os_utils.get_image_id(self.glance_client, image_name)
            os.system('juju metadata generate-image -d ~ -i {} -s {} -r '
                      'RegionOne -u {}'.format(image_id,
                                               image_name,
                                               self.creds['auth_url']))
        net_id = os_utils.get_network_id(self.neutron_client, private_net_name)
        self.__logger.info("Credential information  : %s", net_id)
        juju_bootstrap_command = ('juju bootstrap abot-epc abot-controller '
                                  '--config network={} --metadata-source ~  '
                                  '--constraints mem=2G --bootstrap-series '
                                  'trusty '
                                  '--config use-floating-ip=true --debug'.
                                  format(net_id))
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
            instances = os_utils.get_instances(self.nova_client)
            for items in instances:
                metadata = get_instance_metadata(self.nova_client, items)
                if 'juju-units-deployed' in metadata:
                    sec_group = ('juju-' + metadata['juju-controller-uuid'] +
                                 '-' + metadata['juju-model-uuid'])
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
                                      'grep {} | grep {} | grep {}'
                                      .format('EPC', 'is', 'running'))
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
        res = (process_abot_test_result('{}/TestResults.'
                                        'json'.format(self.case_dir)))
        short_result = sig_test_format(res)
        self.__logger.info(short_result)
        self.details['test_vnf'].update(status='PASS',
                                        result=short_result,
                                        full_result=res,
                                        duration=duration)

        self.__logger.info("Test VNF result: Passed: %d, Failed:"
                           "%d, Skipped: %d", short_result['passed'],
                           short_result['failures'], short_result['skipped'])
        return True

    def clean(self):
        try:
            if not self.orchestrator['requirements']['preserve_setup']:
                self.__logger.info("Removing deployment files...")
                testresult = os.path.join(self.case_dir, 'TestResults.json')
                if os.path.exists(testresult):
                    os.remove(testresult)
                self.__logger.info("Removing %s file ", self.filename)
                if os.path.exists(self.filename):
                    os.remove(self.filename)
                self.__logger.info("Destroying Orchestrator...")
                os.system('juju destroy-controller -y abot-controller '
                          '--destroy-all-models')
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
            # user_id = os_utils.get_user_id(self.keystone_client,
            #                               self.tenant_name)
            floating_ips = os_utils.get_floating_ips(self.neutron_client)
            tenant_id = os_utils.get_tenant_id(self.keystone_client,
                                               self.tenant_name)
            self.__logger.info("TENANT ID : %s", tenant_id)
            for item in floating_ips:
                if item['tenant_id'] == tenant_id:
                    os_utils.delete_floating_ip(self.neutron_client,
                                                item['id'])
            self.__logger.info("Cleaning Projects and Users")
            for creator in reversed(self.created_object):
                try:
                    creator.clean()
                except Exception as exc:  # pylint: disable=broad-except
                    self.__logger.error('Unexpected error cleaning - %s', exc)
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


CLOUD_TEMPLATE = """clouds:
    abot-epc:
      type: openstack
      auth-types: [userpass]
      endpoint: {url}
      regions:
        RegionOne:
          endpoint: {url}
credentials:
  abot-epc:
    abot-epc:
      auth-type: userpass
      password: {pass}
      tenant-name: {tenant_n}
      username: {user_n}"""


def write_config(fname, template, **kwargs):
    """ Generate yaml from template for addinh cloud in juju """
    with open(fname, 'w') as yfile:
        yfile.write(template.format(**kwargs))


def append_config(file_name, p_domain, u_domain):
    """ Append values into a yaml file  """
    with open(file_name) as yfile:
        doc = yaml.load(yfile)
    doc['credentials']['abot-epc']['abot-epc']['project-domain-name'] = (
        p_domain)
    doc['credentials']['abot-epc']['abot-epc']['user-domain-name'] = (
        u_domain)

    with open(file_name, 'w') as yfile:
        yaml.safe_dump(doc, yfile, default_flow_style=False)
