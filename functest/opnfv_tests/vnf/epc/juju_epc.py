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
import re
import subprocess
import sys
import uuid
from copy import deepcopy
import pkg_resources
import yaml

import six
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
from snaps.openstack.utils import neutron_utils

from functest.core import vnf
from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils import config
from functest.utils import env

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

    juju_timeout = '3600'

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

    def _bypass_juju_netdiscovery_bug(self, name):
        user_creator = OpenStackUser(
            self.snaps_creds,
            UserConfig(
                name=name,
                password=str(uuid.uuid4()),
                project_name=self.tenant_name,
                domain_name=self.snaps_creds.user_domain_name,
                roles={'_member_': self.tenant_name}))
        user_creator.create()
        self.created_object.append(user_creator)
        return user_creator

    def _register_cloud(self):
        self.__logger.info("Creating Cloud for Abot-epc .....")
        clouds_yaml = os.path.join(self.res_dir, "clouds.yaml")
        cloud_data = {
            'url': self.public_auth_url,
            'region': self.snaps_creds.region_name if (
                self.snaps_creds.region_name) else 'RegionOne'}
        with open(clouds_yaml, 'w') as yfile:
            yfile.write(CLOUD_TEMPLATE.format(**cloud_data))
        cmd = ['juju', 'add-cloud', 'abot-epc', '-f', clouds_yaml, '--replace']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)

    def _register_credentials_v2(self):
        self.__logger.info("Creating Credentials for Abot-epc .....")
        user_creator = self._bypass_juju_netdiscovery_bug(
            'juju_network_discovery_bug')
        snaps_creds = user_creator.get_os_creds(self.snaps_creds.project_name)
        self.__logger.debug("snaps creds: %s", snaps_creds)
        credentials_yaml = os.path.join(self.res_dir, "credentials.yaml")
        creds_data = {
            'pass': snaps_creds.password,
            'tenant_n': snaps_creds.project_name,
            'user_n': snaps_creds.username}
        with open(credentials_yaml, 'w') as yfile:
            yfile.write(CREDS_TEMPLATE2.format(**creds_data))
        cmd = ['juju', 'add-credential', 'abot-epc', '-f', credentials_yaml,
               '--replace']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)

    def _register_credentials_v3(self):
        self.__logger.info("Creating Credentials for Abot-epc .....")
        user_creator = self._bypass_juju_netdiscovery_bug(
            'juju_network_discovery_bug')
        snaps_creds = user_creator.get_os_creds(self.snaps_creds.project_name)
        self.__logger.debug("snaps creds: %s", snaps_creds)
        credentials_yaml = os.path.join(self.res_dir, "credentials.yaml")
        creds_data = {
            'pass': snaps_creds.password,
            'tenant_n': snaps_creds.project_name,
            'user_n': snaps_creds.username,
            'project_domain_n': snaps_creds.project_domain_name,
            'user_domain_n': snaps_creds.user_domain_name}
        with open(credentials_yaml, 'w') as yfile:
            yfile.write(CREDS_TEMPLATE3.format(**creds_data))
        cmd = ['juju', 'add-credential', 'abot-epc', '-f', credentials_yaml,
               '--replace']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)

    def _add_custom_rule(self, sec_grp_name):
        """ To add custom rule for SCTP Traffic """

        security_group = OpenStackSecurityGroup(
            self.snaps_creds,
            SecurityGroupConfig(
                name=sec_grp_name))

        security_group.create()

        # Add custom security rule to the obtained Security Group
        self.__logger.info("Adding SCTP ingress rule to SG:%s",
                           security_group.sec_grp_settings.name)

        try:
            security_group.add_rule(SecurityGroupRuleConfig(
                sec_grp_name=sec_grp_name, direction=Direction.ingress,
                protocol=Protocol.sctp))
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception(
                "Some issue encountered with adding SCTP security rule ...")

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

        self.__logger.info("ENV:\n%s", env.string())

        self.public_auth_url = keystone_utils.get_endpoint(
            self.snaps_creds, 'identity')

        # it enforces a versioned public identity endpoint as juju simply
        # adds /auth/tokens wich fails vs an unversioned endpoint.
        if not self.public_auth_url.endswith(('v3', 'v3/', 'v2.0', 'v2.0/')):
            self.public_auth_url = six.moves.urllib.parse.urljoin(
                self.public_auth_url, 'v3')
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
        self.__logger.info("Deploying Juju Orchestrator")
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
        self.__logger.info("Creating full network with nameserver: %s",
                           env.get('NAMESERVER'))
        subnet_settings = SubnetConfig(
            name=private_subnet_name,
            cidr=private_subnet_cidr,
            dns_nameservers=[env.get('NAMESERVER')])
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
        for image_name, image_file in six.iteritems(images):
            self.__logger.info("image: %s, file: %s", image_name, image_file)
            if image_file and image_name:
                image_creator = OpenStackImage(self.snaps_creds, ImageConfig(
                    name=image_name, image_user='cloud', img_format='qcow2',
                    image_file=image_file))
                image_id = image_creator.create().id
                cmd = ['juju', 'metadata', 'generate-image', '-d', '/root',
                       '-i', image_id, '-s', image_name, '-r',
                       self.snaps_creds.region_name if (
                           self.snaps_creds.region_name) else 'RegionOne',
                       '-u', self.public_auth_url]
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                self.__logger.info("%s\n%s", " ".join(cmd), output)
                self.created_object.append(image_creator)
        self.__logger.info("Network ID  : %s", net_id)

        self.__logger.info("Starting Juju Bootstrap process...")
        try:
            cmd = ['timeout', '-t', JujuEpc.juju_timeout,
                   'juju', 'bootstrap', 'abot-epc', 'abot-controller',
                   '--metadata-source', '/root',
                   '--constraints', 'mem=2G',
                   '--bootstrap-series', 'xenial',
                   '--config', 'network={}'.format(net_id),
                   '--config', 'ssl-hostname-verification=false',
                   '--config', 'use-floating-ip=true',
                   '--config', 'use-default-secgroup=true',
                   '--debug']
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            self.__logger.info("%s\n%s", " ".join(cmd), output)
        except subprocess.CalledProcessError as cpe:
            self.__logger.error(
                "Exception with Juju Bootstrap: %s\n%s",
                cpe.cmd, cpe.output)
            return False
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Some issue with Juju Bootstrap ...")
            return False

        return True

    def check_app(self, name='abot-epc-basic', status='active'):
        """Check application status."""
        cmd = ['juju', 'status', '--format', 'short', name]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        ret = re.search(r'(?=workload:({})\))'.format(status), output)
        if ret:
            self.__logger.info("%s workload is %s", name, status)
            return True
        self.__logger.error("%s workload differs from %s", name, status)
        return False

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
        cmd = ['juju', 'deploy', '{}'.format(descriptor.get('file_name'))]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        self.__logger.info("Waiting for instances .....")
        try:
            cmd = ['timeout', '-t', JujuEpc.juju_timeout, 'juju-wait']
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            self.__logger.info("%s\n%s", " ".join(cmd), output)
            self.__logger.info("Deployed Abot-epc on Openstack")
        except subprocess.CalledProcessError as cpe:
            self.__logger.error(
                "Exception with Juju VNF Deployment: %s\n%s",
                cpe.cmd, cpe.output)
            return False
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Some issue with the VNF Deployment ..")
            return False

        self.__logger.info("Checking status of ABot and EPC units ...")
        cmd = ['juju', 'status']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.debug("%s\n%s", " ".join(cmd), output)
        for app in ['abot-epc-basic', 'oai-epc', 'oai-hss']:
            if not self.check_app(app):
                return False

        nova_client = nova_utils.nova_client(self.snaps_creds)
        instances = get_instances(nova_client)
        self.__logger.info("List of Instance: %s", instances)
        for items in instances:
            metadata = get_instance_metadata(nova_client, items)
            if 'juju-units-deployed' in metadata:
                sec_group = 'juju-{}-{}'.format(
                    metadata['juju-controller-uuid'],
                    metadata['juju-model-uuid'])
                self.__logger.info("Instance: %s", sec_group)
                break
        self.__logger.info("Adding Security group rule....")
        # This will add sctp rule to a common Security Group Created
        # by juju and shared to all deployed units.
        self._add_custom_rule(sec_group)

        self.__logger.info("Transferring the feature files to Abot_node ...")
        cmd = ['timeout', '-t', JujuEpc.juju_timeout,
               'juju', 'scp', '--', '-r', '-v',
               '{}/featureFiles'.format(self.case_dir), 'abot-epc-basic/0:~/']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)

        self.__logger.info("Copying the feature files within Abot_node ")
        cmd = ['timeout', '-t', JujuEpc.juju_timeout,
               'juju', 'ssh', 'abot-epc-basic/0',
               'sudo', 'cp', '-vfR', '~/featureFiles/*',
               '/etc/rebaca-test-suite/featureFiles']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        return True

    def test_vnf(self):
        """Run test on ABoT."""
        start_time = time.time()
        self.__logger.info("Running VNF Test cases....")
        cmd = ['juju', 'run-action', 'abot-epc-basic/0', 'run',
               'tagnames={}'.format(self.details['test_vnf']['tag_name'])]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)

        cmd = ['timeout', '-t', JujuEpc.juju_timeout, 'juju-wait']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)

        duration = time.time() - start_time
        self.__logger.info("Getting results from Abot node....")
        cmd = ['timeout', '-t', JujuEpc.juju_timeout,
               'juju', 'scp', '--', '-v',
               'abot-epc-basic/0:'
               '/var/lib/abot-epc-basic/artifacts/TestResults.json',
               '{}/.'.format(self.res_dir)]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        self.__logger.info("Parsing the Test results...")
        res = (process_abot_test_result('{}/TestResults.json'.format(
            self.res_dir)))
        short_result = sig_test_format(res)
        self.__logger.info(short_result)
        self.details['test_vnf'].update(
            status='PASS', result=short_result, full_result=res,
            duration=duration)
        self.__logger.info(
            "Test VNF result: Passed: %d, Failed:%d, Skipped: %d",
            short_result['passed'],
            short_result['failures'], short_result['skipped'])
        return True

    def _get_floating_ips(self):
        """Get the list of floating IPs associated with the current project"""

        project_id = self.os_project.get_project().id

        neutron_client = neutron_utils.neutron_client(self.snaps_creds)
        floating_ips = neutron_utils.get_floating_ips(neutron_client)

        project_floating_ip_list = list()
        for floating_ip in floating_ips:
            if project_id and project_id == floating_ip.project_id:
                project_floating_ip_list.append(floating_ip)

        return project_floating_ip_list

    def _release_floating_ips(self, fip_list):
        """
        Responsible for deleting a list of floating IPs
        :param fip_list: A list of SNAPS FloatingIp objects
        :return:
        """
        if not fip_list:
            return

        neutron_client = neutron_utils.neutron_client(self.snaps_creds)

        for floating_ip in fip_list:
            neutron_utils.delete_floating_ip(neutron_client, floating_ip)

    def clean(self):
        """Clean created objects/functions."""

        # Store Floating IPs of instances created by Juju
        fip_list = self._get_floating_ips()
        self.__logger.info("Floating IPs assigned to project:%s",
                           self.os_project.get_project().name)
        for floating_ip in fip_list:
            self.__logger.debug("%s:%s", floating_ip.ip,
                                floating_ip.description)

        try:
            cmd = ['juju', 'debug-log', '--replay', '--no-tail']
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            self.__logger.debug("%s\n%s", " ".join(cmd), output)
            if not self.orchestrator['requirements']['preserve_setup']:
                self.__logger.info("Destroying Orchestrator...")
                cmd = ['timeout', '-t', JujuEpc.juju_timeout,
                       'juju', 'destroy-controller', '-y', 'abot-controller',
                       '--destroy-all-models']
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                self.__logger.info("%s\n%s", " ".join(cmd), output)
        except subprocess.CalledProcessError as cpe:
            self.__logger.error(
                "Exception with Juju Cleanup: %s\n%s",
                cpe.cmd, cpe.output)
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("General issue during the undeployment ..")

        if not self.orchestrator['requirements']['preserve_setup']:
            try:
                self.__logger.info('Release floating IPs assigned by Juju...')
                self._release_floating_ips(fip_list)
            except Exception:  # pylint: disable=broad-except
                self.__logger.exception(
                    "Exception while releasing floating IPs ...")

            self.__logger.info('Remove the Abot_epc OS objects ..')
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
            except Exception:  # pylint: disable=broad-except
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
