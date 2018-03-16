#!/usr/bin/env python

# Copyright (c) 2016 Rebaca and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
"""Juju testcase implementation."""

import errno
import logging
import os
import time
import json
import sys
import uuid
from copy import deepcopy
from urlparse import urljoin
import pkg_resources
import yaml

from functest.core import vnf
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils import config
from functest.utils import env

from snaps.config.flavor import FlavorConfig
from snaps.config.image import ImageConfig
from snaps.config.network import NetworkConfig, SubnetConfig
from snaps.config.router import RouterConfig
from snaps.config.security_group import (
    Direction, Protocol, SecurityGroupConfig, SecurityGroupRuleConfig)
from snaps.config.user import UserConfig
from snaps.openstack.create_flavor import OpenStackFlavor
from snaps.openstack.create_image import OpenStackImage
from snaps.openstack.create_network import OpenStackNetwork
from snaps.openstack.create_router import OpenStackRouter
from snaps.openstack.create_security_group import OpenStackSecurityGroup
from snaps.openstack.create_user import OpenStackUser
from snaps.openstack.utils import keystone_utils
from snaps.openstack.utils import nova_utils

__author__ = "Amarendra Meher <amarendra@rebaca.com>"
__author__ = "Soumaya K Nayek <soumaya.nayek@rebaca.com>"

CLOUD_TEMPLATE = """clouds:
  abot-epc:
    type: openstack
    auth-types: [userpass]
    endpoint: {url}
    regions:
      {region}:
        endpoint: {url}"""

CREDS_TEMPLATE2 = """credentials:
  abot-epc:
    default-credential: abot-epc
    abot-epc:
      auth-type: userpass
      password: {pass}
      project-domain-name: {project_domain_n}
      tenant-name: {tenant_n}"""

CREDS_TEMPLATE3 = """credentials:
  abot-epc:
    default-credential: abot-epc
    abot-epc:
      auth-type: userpass
      password: {pass}
      project-domain-name: {project_domain_n}
      tenant-name: {tenant_n}
      user-domain-name: {user_domain_n}
      username: {user_n}"""


class JujuEpc(vnf.VnfOnBoarding):
    # pylint:disable=too-many-instance-attributes
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
            self.config = getattr(
                config.CONF, 'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")
        self.config_file = os.path.join(self.case_dir, self.config)
        self.orchestrator = dict(requirements=get_config(
            "orchestrator.requirements", self.config_file))

        self.created_object = []
        self.details['orchestrator'] = dict(
            name=get_config("orchestrator.name", self.config_file),
            version=get_config("orchestrator.version", self.config_file),
            status='ERROR',
            result=''
        )

        self.vnf = dict(
            descriptor=get_config("vnf.descriptor", self.config_file),
            requirements=get_config("vnf.requirements", self.config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=get_config("vnf.name", self.config_file),
            version=get_config("vnf.version", self.config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)

        self.details['test_vnf'] = dict(
            name=get_config("vnf_test_suite.name", self.config_file),
            version=get_config("vnf_test_suite.version", self.config_file),
            tag_name=get_config("vnf_test_suite.tag_name", self.config_file)
        )
        self.public_auth_url = None

        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), self.case_name)

    def _bypass_juju_network_discovery_bug(self, name):
        self.__logger.debug("snaps creds: %s", self.snaps_creds)
        user_creator = OpenStackUser(
            self.snaps_creds,
            UserConfig(
                name=name,
                password=str(uuid.uuid4()),
                project_name=self.tenant_name,
                domain=self.snaps_creds.user_domain_name,
                roles={'_member_': self.tenant_name}))
        user_creator.create()
        self.created_object.append(user_creator)
        return user_creator

    def _register_cloud(self):
        self.__logger.info("Creating Cloud for Abot-epc .....")
        clouds_yaml = os.path.join(self.res_dir, "clouds.yaml")
        # It allows gating APEX and ensures this testcase is working till
        # https://jira.opnfv.org/browse/APEX-570 is fixed in APEX.
        # It must be removed as soon as possible to disable per installer
        # processing in Functest.
        region = self.snaps_creds.region_name
        if not region and env.get('INSTALLER_TYPE') == 'apex':
            region = "regionOne"
        cloud_data = {
            'url': self.public_auth_url,
            'region': region}
        with open(clouds_yaml, 'w') as yfile:
            yfile.write(CLOUD_TEMPLATE.format(**cloud_data))
        if os.system(
                'juju add-cloud abot-epc -f {} --replace'.format(clouds_yaml)):
            raise vnf.VnfPreparationException

    def _register_credentials_v2(self):
        self.__logger.info("Creating Credentials for Abot-epc .....")
        user_creator = self._bypass_juju_network_discovery_bug(
            'juju_network_discovery_bug')
        snaps_creds = user_creator.get_os_creds(self.snaps_creds.project_name)
        credentials_yaml = os.path.join(self.res_dir, "credentials.yaml")
        creds_data = {
            'pass': snaps_creds.password,
            'tenant_n': snaps_creds.project_name,
            'user_n': snaps_creds.username}
        with open(credentials_yaml, 'w') as yfile:
            yfile.write(CREDS_TEMPLATE2.format(**creds_data))
        if os.system(
                'juju add-credential abot-epc -f {} --replace'.format(
                    credentials_yaml)):
            raise vnf.VnfPreparationException

    def _register_credentials_v3(self):
        self.__logger.info("Creating Credentials for Abot-epc .....")
        user_creator = self._bypass_juju_network_discovery_bug(
            'juju_network_discovery_bug')
        snaps_creds = user_creator.get_os_creds(self.snaps_creds.project_name)
        credentials_yaml = os.path.join(self.res_dir, "credentials.yaml")
        creds_data = {
            'pass': snaps_creds.password,
            'tenant_n': snaps_creds.project_name,
            'user_n': snaps_creds.username,
            'project_domain_n': snaps_creds.project_domain_name,
            'user_domain_n': snaps_creds.user_domain_name}
        with open(credentials_yaml, 'w') as yfile:
            yfile.write(CREDS_TEMPLATE3.format(**creds_data))
        if os.system(
                'juju add-credential abot-epc -f {} --replace'.format(
                    credentials_yaml)):
            raise vnf.VnfPreparationException

    def _add_custom_rule(self, sec_grp_name):
        """ To add custom rule for SCTP Traffic """
        sec_grp_rules = list()
        sec_grp_rules.append(
            SecurityGroupRuleConfig(
                sec_grp_name=sec_grp_name, direction=Direction.ingress,
                protocol=Protocol.sctp))
        security_group = OpenStackSecurityGroup(
            self.snaps_creds,
            SecurityGroupConfig(
                name=sec_grp_name,
                rule_settings=sec_grp_rules))
        security_group.create()
        self.created_object.append(security_group)

    def prepare(self):
        """Prepare testcase (Additional pre-configuration steps)."""
        self.__logger.info("Additional pre-configuration steps")
        super(JujuEpc, self).prepare()
        try:
            os.makedirs(self.res_dir)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                self.__logger.exception("Cannot create %s", self.res_dir)
                raise vnf.VnfPreparationException
        self.public_auth_url = keystone_utils.get_endpoint(
            self.snaps_creds, 'identity')
        # it enforces a versioned public identity endpoint as juju simply
        # adds /auth/tokens wich fails vs an unversioned endpoint.
        if not self.public_auth_url.endswith(('v3', 'v3/', 'v2.0', 'v2.0/')):
            self.public_auth_url = urljoin(self.public_auth_url, 'v3')
        self._register_cloud()
        if self.snaps_creds.identity_api_version == 3:
            self._register_credentials_v3()
        else:
            self._register_credentials_v2()

    def deploy_orchestrator(self):  # pylint: disable=too-many-locals
        """
        Create network, subnet, router

        Bootstrap juju
        """
        self.__logger.info("Deployed Orchestrator")
        private_net_name = getattr(
            config.CONF, 'vnf_{}_private_net_name'.format(self.case_name))
        private_subnet_name = '{}-{}'.format(
            getattr(config.CONF,
                    'vnf_{}_private_subnet_name'.format(self.case_name)),
            self.uuid)
        private_subnet_cidr = getattr(
            config.CONF, 'vnf_{}_private_subnet_cidr'.format(self.case_name))
        abot_router = '{}-{}'.format(
            getattr(config.CONF,
                    'vnf_{}_external_router'.format(self.case_name)),
            self.uuid)
        self.__logger.info("Creating full network ...")
        subnet_settings = SubnetConfig(
            name=private_subnet_name, cidr=private_subnet_cidr)
        network_settings = NetworkConfig(
            name=private_net_name, subnet_settings=[subnet_settings])
        network_creator = OpenStackNetwork(self.snaps_creds, network_settings)
        net_id = network_creator.create().id
        self.created_object.append(network_creator)

        ext_net_name = snaps_utils.get_ext_net_name(self.snaps_creds)
        self.__logger.info("Creating network Router ....")
        router_creator = OpenStackRouter(
            self.snaps_creds, RouterConfig(
                name=abot_router,
                external_gateway=ext_net_name,
                internal_subnets=[subnet_settings.name]))
        router_creator.create()
        self.created_object.append(router_creator)
        self.__logger.info("Creating Flavor ....")
        flavor_settings = FlavorConfig(
            name=self.orchestrator['requirements']['flavor']['name'],
            ram=self.orchestrator['requirements']['flavor']['ram_min'],
            disk=10, vcpus=1)
        flavor_creator = OpenStackFlavor(self.snaps_creds, flavor_settings)
        flavor_creator.create()
        self.created_object.append(flavor_creator)
        self.__logger.info("Upload some OS images if it doesn't exist")
        images = get_config("tenant_images", self.config_file)
        self.__logger.info("Images needed for vEPC: %s", images)
        for image_name, image_file in images.iteritems():
            self.__logger.info("image: %s, file: %s", image_name, image_file)
            if image_file and image_name:
                image_creator = OpenStackImage(self.snaps_creds, ImageConfig(
                    name=image_name, image_user='cloud', img_format='qcow2',
                    image_file=image_file))
                image_id = image_creator.create().id
                # It allows gating APEX and ensures this testcase is working
                # till https://jira.opnfv.org/browse/APEX-570 is fixed in APEX.
                # It must be removed as soon as possible to disable per
                # installer processing in Functest.
                region = self.snaps_creds.region_name
                if not region and env.get('INSTALLER_TYPE') == 'apex':
                    region = "regionOne"
                os.system(
                    'juju metadata generate-image -d ~ -i {} -s {} -r '
                    '{} -u {}'.format(
                        image_id, image_name, region,
                        self.public_auth_url))
                self.created_object.append(image_creator)
        self.__logger.info("Network ID  : %s", net_id)
        juju_bootstrap_command = (
            'juju bootstrap abot-epc abot-controller --config network={} '
            '--metadata-source ~  --config ssl-hostname-verification=false '
            '--constraints mem=2G --bootstrap-series xenial '
            '--config use-floating-ip=true --debug '
            '--config use-default-secgroup=true'.format(net_id))
        os.system(juju_bootstrap_command)
        return True

    def deploy_vnf(self):
        """Deploy ABOT-OAI-EPC."""
        self.__logger.info("Upload VNFD")
        descriptor = self.vnf['descriptor']
        self.__logger.info("Get or create flavor for all Abot-EPC")
        flavor_settings = FlavorConfig(
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
        nova_client = nova_utils.nova_client(self.snaps_creds)
        if status == 0:
            instances = get_instances(nova_client)
            self.__logger.info("List of Instance: %s", instances)
            for items in instances:
                metadata = get_instance_metadata(nova_client, items)
                if 'juju-units-deployed' in metadata:
                    sec_group = ('juju-' +
                                 metadata['juju-controller-uuid'] +
                                 '-' + metadata['juju-model-uuid'])
                    self.__logger.info("Instance: %s", sec_group)
                    break
            self.__logger.info("Adding Security group rule....")
            # This will add sctp rule to a common Security Group Created
            # by juju and shared to all deployed units.
            self._add_custom_rule(sec_group)
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
        return False

    def test_vnf(self):
        """Run test on ABoT."""
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
        """Clean created objects/functions."""
        try:
            if not self.orchestrator['requirements']['preserve_setup']:
                self.__logger.info("Removing deployment files...")
                testresult = os.path.join(self.case_dir, 'TestResults.json')
                if os.path.exists(testresult):
                    os.remove(testresult)
                self.__logger.info("Destroying Orchestrator...")
                os.system('juju destroy-controller -y abot-controller '
                          '--destroy-all-models')
        except Exception:  # pylint: disable=broad-except
            self.__logger.warn("Some issue during the undeployment ..")
            self.__logger.warn("Tenant clean continue ..")

        if not self.orchestrator['requirements']['preserve_setup']:
            self.__logger.info('Remove the Abot_epc OS object ..')
            super(JujuEpc, self).clean()

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

    except Exception:  # pylint: disable=broad-except
        logging.error("Error in updating data, %s", sys.exc_info()[0])
        raise

    return obj


def get_instances(nova_client):
    """ To get all vm info of a project """
    try:
        instances = nova_client.servers.list()
        return instances
    except Exception as exc:  # pylint: disable=broad-except
        logging.error("Error [get_instances(nova_client)]: %s", exc)
        return None


def get_instance_metadata(nova_client, instance):
    """ Get instance Metadata - Instance ID """
    try:
        instance = nova_client.servers.get(instance.id)
        return instance.metadata
    except Exception as exc:  # pylint: disable=broad-except
        logging.error("Error [get_instance_status(nova_client)]: %s", exc)
        return None
