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

from copy import deepcopy
import pkg_resources
import six
import yaml

from functest.core import singlevm
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

CREDS_TEMPLATE = """credentials:
  abot-epc:
    default-credential: abot-epc
    abot-epc:
      auth-type: userpass
      password: {pass}
      project-domain-name: {project_domain_n}
      tenant-name: {tenant_n}
      user-domain-name: {user_domain_n}
      username: {user_n}"""


class JujuEpc(singlevm.VmReady2):
    # pylint:disable=too-many-instance-attributes
    """Abot EPC deployed with JUJU Orchestrator Case"""

    __logger = logging.getLogger(__name__)

    filename = ('/home/opnfv/functest/images/'
                'ubuntu-16.04-server-cloudimg-amd64-disk1.img')
    filename_alt = ('/home/opnfv/functest/images/'
                    'ubuntu-14.04-server-cloudimg-amd64-disk1.img')

    flavor_ram = 2048
    flavor_vcpus = 1
    flavor_disk = 10

    flavor_alt_ram = 4096
    flavor_alt_vcpus = 1
    flavor_alt_disk = 10

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

        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), self.case_name)

        try:
            self.public_auth_url = self.get_public_auth_url(self.orig_cloud)
            if not self.public_auth_url.endswith(('v3', 'v3/')):
                self.public_auth_url = six.moves.urllib.parse.urljoin(
                    self.public_auth_url, 'v3')
        except Exception:  # pylint: disable=broad-except
            self.public_auth_url = None
        self.sec = None
        self.image_alt = None
        self.flavor_alt = None

    def check_requirements(self):
        if env.get('NEW_USER_ROLE').lower() == "admin":
            self.__logger.warn(
                "Defining NEW_USER_ROLE=admin will easily break the testcase "
                "because Juju doesn't manage tenancy (e.g. subnet  "
                "overlapping)")

    def _register_cloud(self):
        assert self.public_auth_url
        self.__logger.info("Creating Cloud for Abot-epc .....")
        clouds_yaml = os.path.join(self.res_dir, "clouds.yaml")
        cloud_data = {
            'url': self.public_auth_url,
            'region': self.cloud.region_name if self.cloud.region_name else (
                'RegionOne')}
        with open(clouds_yaml, 'w') as yfile:
            yfile.write(CLOUD_TEMPLATE.format(**cloud_data))
        cmd = ['juju', 'add-cloud', 'abot-epc', '-f', clouds_yaml, '--replace']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)

    def _register_credentials(self):
        self.__logger.info("Creating Credentials for Abot-epc .....")
        credentials_yaml = os.path.join(self.res_dir, "credentials.yaml")
        creds_data = {
            'pass': self.project.password,
            'tenant_n': self.project.project.name,
            'user_n': self.project.user.name,
            'project_domain_n': self.cloud.auth.get(
                "project_domain_name", "Default"),
            'user_domain_n': self.cloud.auth.get(
                "user_domain_name", "Default")}
        with open(credentials_yaml, 'w') as yfile:
            yfile.write(CREDS_TEMPLATE.format(**creds_data))
        cmd = ['juju', 'add-credential', 'abot-epc', '-f', credentials_yaml,
               '--replace']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)

    def prepare(self):
        """Prepare testcase (Additional pre-configuration steps)."""
        assert self.public_auth_url
        self.__logger.info("Additional pre-configuration steps")
        try:
            os.makedirs(self.res_dir)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                self.__logger.exception("Cannot create %s", self.res_dir)
                raise Exception

        self.__logger.info("ENV:\n%s", env.string())
        self._register_cloud()
        self._register_credentials()

    def publish_image(self, name=None):
        image = super(JujuEpc, self).publish_image(name)
        cmd = ['juju', 'metadata', 'generate-image', '-d', '/root',
               '-i', image.id, '-s', 'xenial',
               '-r', self.cloud.region_name if self.cloud.region_name else (
                   'RegionOne'),
               '-u', self.public_auth_url]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        return image

    def publish_image_alt(self, name=None):
        image_alt = super(JujuEpc, self).publish_image_alt(name)
        cmd = ['juju', 'metadata', 'generate-image', '-d', '/root',
               '-i', image_alt.id, '-s', 'trusty',
               '-r', self.cloud.region_name if self.cloud.region_name else (
                   'RegionOne'),
               '-u', self.public_auth_url]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self.__logger.info("%s\n%s", " ".join(cmd), output)
        return image_alt

    def deploy_orchestrator(self):  # pylint: disable=too-many-locals
        """
        Create network, subnet, router

        Bootstrap juju
        """
        self.image_alt = self.publish_image_alt()
        self.flavor_alt = self.create_flavor_alt()
        self.__logger.info("Starting Juju Bootstrap process...")
        try:
            cmd = ['timeout', '-t', JujuEpc.juju_timeout,
                   'juju', 'bootstrap',
                   'abot-epc/{}'.format(
                       self.cloud.region_name if self.cloud.region_name else (
                           'RegionOne')),
                   'abot-controller',
                   '--agent-version', '2.2.9',
                   '--metadata-source', '/root',
                   '--constraints', 'mem=2G',
                   '--bootstrap-series', 'xenial',
                   '--config', 'network={}'.format(self.network.id),
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

    def run(self, **kwargs):
        self.start_time = time.time()
        try:
            assert super(JujuEpc, self).run(**kwargs) == self.EX_OK
            self.prepare()
            if (self.deploy_orchestrator() and
                    self.deploy_vnf() and
                    self.test_vnf()):
                self.stop_time = time.time()
                self.result = 100
                return self.EX_OK
            self.result = 0
            self.stop_time = time.time()
            return self.EX_TESTCASE_FAILED
        except Exception:  # pylint: disable=broad-except
            self.stop_time = time.time()
            self.__logger.exception("Exception on VNF testing")
            return self.EX_TESTCASE_FAILED

    def clean(self):
        """Clean created objects/functions."""
        try:
            cmd = ['juju', 'debug-log', '--replay', '--no-tail']
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            self.__logger.debug("%s\n%s", " ".join(cmd), output)
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
        for fip in self.cloud.list_floating_ips():
            self.cloud.delete_floating_ip(fip.id)
        if self.image_alt:
            self.cloud.delete_image(self.image_alt)
        if self.flavor_alt:
            self.orig_cloud.delete_flavor(self.flavor_alt.id)
        super(JujuEpc, self).clean()


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
