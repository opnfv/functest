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
import sys

from copy import deepcopy
import pkg_resources
import scp

from functest.core import singlevm
from functest.utils import config
from functest.utils import env
from functest.utils import functest_utils

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
      password: '{pass}'
      project-domain-name: {project_domain_n}
      tenant-name: {tenant_n}"""

CREDS_TEMPLATE = """credentials:
  abot-epc:
    default-credential: abot-epc
    abot-epc:
      auth-type: userpass
      password: '{pass}'
      project-domain-name: {project_domain_n}
      tenant-name: {tenant_n}
      user-domain-name: {user_domain_n}
      username: {user_n}"""


class JujuEpc(singlevm.SingleVm2):
    # pylint:disable=too-many-instance-attributes
    """Abot EPC deployed with JUJU Orchestrator Case"""

    __logger = logging.getLogger(__name__)

    cidr = '192.168.120.0/24'

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
    username = 'ubuntu'
    juju_timeout = '4800'

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "juju_epc"
        super().__init__(**kwargs)

        # Retrieve the configuration
        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/epc')
        try:
            self.config = getattr(
                config.CONF, f'vnf_{self.case_name}_config')
        except Exception as exc:
            raise Exception("VNF config file not found") from exc
        self.config_file = os.path.join(self.case_dir, self.config)
        self.orchestrator = dict(
            requirements=functest_utils.get_parameter_from_yaml(
                "orchestrator.requirements", self.config_file))

        self.created_object = []
        self.details['orchestrator'] = dict(
            name=functest_utils.get_parameter_from_yaml(
                "orchestrator.name", self.config_file),
            version=functest_utils.get_parameter_from_yaml(
                "orchestrator.version", self.config_file),
            status='ERROR',
            result=''
        )

        self.vnf = dict(
            descriptor=functest_utils.get_parameter_from_yaml(
                "vnf.descriptor", self.config_file),
            requirements=functest_utils.get_parameter_from_yaml(
                "vnf.requirements", self.config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=functest_utils.get_parameter_from_yaml(
                "vnf.name", self.config_file),
            version=functest_utils.get_parameter_from_yaml(
                "vnf.version", self.config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)

        self.details['test_vnf'] = dict(
            name=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.name", self.config_file),
            version=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.version", self.config_file),
            tag_name=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.tag_name", self.config_file)
        )

        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), self.case_name)

        try:
            self.public_auth_url = self.get_public_auth_url(self.orig_cloud)
            if not self.public_auth_url.endswith(('v3', 'v3/')):
                self.public_auth_url = f"{self.public_auth_url}/v3"
        except Exception:  # pylint: disable=broad-except
            self.public_auth_url = None
        self.sec = None
        self.image_alt = None
        self.flavor_alt = None

    def _install_juju(self):
        (_, stdout, stderr) = self.ssh.exec_command(
            'sudo snap install juju --channel=2.3/stable --classic')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        return not stdout.channel.recv_exit_status()

    def _install_juju_wait(self):
        (_, stdout, stderr) = self.ssh.exec_command(
            'sudo apt-get update && sudo apt-get install python3-pip -y && '
            'sudo pip3 install juju_wait===2.6.4')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        return not stdout.channel.recv_exit_status()

    def _register_cloud(self):
        assert self.public_auth_url
        self.__logger.info("Creating Cloud for Abot-epc .....")
        clouds_yaml = os.path.join(self.res_dir, "clouds.yaml")
        cloud_data = {
            'url': self.public_auth_url,
            'region': self.cloud.region_name if self.cloud.region_name else (
                'RegionOne')}
        with open(clouds_yaml, 'w', encoding='utf-8') as yfile:
            yfile.write(CLOUD_TEMPLATE.format(**cloud_data))
        scpc = scp.SCPClient(self.ssh.get_transport())
        scpc.put(clouds_yaml, remote_path='~/')
        (_, stdout, stderr) = self.ssh.exec_command(
            '/snap/bin/juju add-cloud abot-epc -f clouds.yaml --replace')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        return not stdout.channel.recv_exit_status()

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
        with open(credentials_yaml, 'w', encoding='utf-8') as yfile:
            yfile.write(CREDS_TEMPLATE.format(**creds_data))
        scpc = scp.SCPClient(self.ssh.get_transport())
        scpc.put(credentials_yaml, remote_path='~/')
        (_, stdout, stderr) = self.ssh.exec_command(
            '/snap/bin/juju add-credential abot-epc -f credentials.yaml '
            ' --replace --debug')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        return not stdout.channel.recv_exit_status()

    def _publish_image(self):
        region_name = self.cloud.region_name if self.cloud.region_name else (
            'RegionOne')
        (_, stdout, stderr) = self.ssh.exec_command(
            '/snap/bin/juju metadata generate-image -d /home/ubuntu '
            f'-i {self.image.id} -s xenial -r {region_name} '
            f'-u {self.public_auth_url}')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        return not stdout.channel.recv_exit_status()

    def publish_image_alt(self, name=None):
        image_alt = super().publish_image_alt(name)
        region_name = self.cloud.region_name if self.cloud.region_name else (
            'RegionOne')
        (_, stdout, stderr) = self.ssh.exec_command(
            '/snap/bin/juju metadata generate-image -d /home/ubuntu '
            f'-i {image_alt.id} -s trusty -r {region_name} '
            f'-u {self.public_auth_url}')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        return image_alt

    def deploy_orchestrator(self):  # pylint: disable=too-many-locals
        """
        Create network, subnet, router

        Bootstrap juju
        """
        self._publish_image()
        self.image_alt = self.publish_image_alt()
        self.flavor_alt = self.create_flavor_alt()
        self.__logger.info("Starting Juju Bootstrap process...")
        region_name = self.cloud.region_name if self.cloud.region_name else (
            'RegionOne')
        (_, stdout, stderr) = self.ssh.exec_command(
            f'timeout {JujuEpc.juju_timeout} '
            f'/snap/bin/juju bootstrap abot-epc/{region_name} abot-controller '
            '--agent-version 2.3.9 --metadata-source /home/ubuntu '
            '--constraints mem=2G --bootstrap-series xenial '
            f'--config network={self.network.id} '
            '--config ssl-hostname-verification=false '
            f'--config external-network={self.ext_net.id} '
            '--config use-floating-ip=true '
            '--config use-default-secgroup=true '
            '--debug')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        return not stdout.channel.recv_exit_status()

    def check_app(self, name='abot-epc-basic', status='active'):
        """Check application status."""
        for i in range(10):
            (_, stdout, stderr) = self.ssh.exec_command(
                f'/snap/bin/juju status --format short {name}')
            output = stdout.read().decode("utf-8")
            self.__logger.debug("stdout:\n%s", output)
            self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
            if stdout.channel.recv_exit_status():
                continue
            ret = re.search(
                rf'(?=workload:({status})\))', output)
            if ret:
                self.__logger.info("%s workload is %s", name, status)
                break
            self.__logger.info(
                "loop %d: %s workload differs from %s", i + 1, name, status)
            time.sleep(60)
        else:
            self.__logger.error("%s workload differs from %s", name, status)
            return False
        return True

    def deploy_vnf(self):
        """Deploy ABOT-OAI-EPC."""
        self.__logger.info("Upload VNFD")
        scpc = scp.SCPClient(self.ssh.get_transport())
        scpc.put(
            '/src/epc-requirements/abot_charm', remote_path='~/',
            recursive=True)
        self.__logger.info("Deploying Abot-epc bundle file ...")
        (_, stdout, stderr) = self.ssh.exec_command(
            'sudo mkdir -p /src/epc-requirements && '
            'sudo mv abot_charm /src/epc-requirements/abot_charm && '
            '/snap/bin/juju deploy '
            '/src/epc-requirements/abot_charm/functest-abot-epc-bundle/'
            'bundle.yaml')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        if stdout.channel.recv_exit_status():
            return not stdout.channel.recv_exit_status()
        (_, stdout, stderr) = self.ssh.exec_command(
            'PATH=/snap/bin/:$PATH '
            f'timeout {JujuEpc.juju_timeout} juju-wait')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        if stdout.channel.recv_exit_status():
            return not stdout.channel.recv_exit_status()
        self.__logger.info("Checking status of ABot and EPC units ...")
        (_, stdout, stderr) = self.ssh.exec_command('/snap/bin/juju status')
        output = stdout.read().decode("utf-8")
        self.__logger.debug("stdout:\n%s", output)
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        if stdout.channel.recv_exit_status():
            return not stdout.channel.recv_exit_status()
        for app in ['abot-epc-basic', 'oai-epc', 'oai-hss']:
            if not self.check_app(app):
                return False
        scpc = scp.SCPClient(self.ssh.get_transport())
        scpc.put(
            f'{self.case_dir}/featureFiles', remote_path='~/',
            recursive=True)
        (_, stdout, stderr) = self.ssh.exec_command(
            f'timeout {JujuEpc.juju_timeout} /snap/bin/juju scp -- -r -v '
            '~/featureFiles abot-epc-basic/0:/etc/rebaca-test-suite/')
        output = stdout.read().decode("utf-8")
        self.__logger.debug("stdout:\n%s", output)
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        return not stdout.channel.recv_exit_status()

    def test_vnf(self):
        """Run test on ABoT."""
        start_time = time.time()
        (_, stdout, stderr) = self.ssh.exec_command(
            "/snap/bin/juju run-action abot-epc-basic/0 "
            f"run tagnames={self.details['test_vnf']['tag_name']}")
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        if stdout.channel.recv_exit_status():
            return not stdout.channel.recv_exit_status()
        (_, stdout, stderr) = self.ssh.exec_command(
            'PATH=/snap/bin/:$PATH '
            f'timeout {JujuEpc.juju_timeout} juju-wait')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        if stdout.channel.recv_exit_status():
            return not stdout.channel.recv_exit_status()
        duration = time.time() - start_time
        self.__logger.info("Getting results from Abot node....")
        (_, stdout, stderr) = self.ssh.exec_command(
            f'timeout {JujuEpc.juju_timeout} /snap/bin/juju scp '
            '-- -v abot-epc-basic/0:'
            '/var/lib/abot-epc-basic/artifacts/TestResults.json .')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        if stdout.channel.recv_exit_status():
            return not stdout.channel.recv_exit_status()
        scpc = scp.SCPClient(self.ssh.get_transport())
        scpc.get('TestResults.json', self.res_dir)
        self.__logger.info("Parsing the Test results...")
        res = process_abot_test_result(f'{self.res_dir}/TestResults.json')
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

    def execute(self):
        """Prepare testcase (Additional pre-configuration steps)."""
        assert self.public_auth_url
        self.__logger.info("Additional pre-configuration steps")
        try:
            os.makedirs(self.res_dir)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                self.__logger.exception("Cannot create %s", self.res_dir)
                raise Exception from ex
        self.__logger.info("ENV:\n%s", env.string())
        try:
            assert self._install_juju()
            assert self._install_juju_wait()
            assert self._register_cloud()
            assert self._register_credentials()
            assert self.deploy_orchestrator()
            assert self.deploy_vnf()
            assert self.test_vnf()
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("juju_epc failed")
            return 1
        return 0

    def clean(self):
        """Clean created objects/functions."""
        (_, stdout, stderr) = self.ssh.exec_command(
            '/snap/bin/juju debug-log --replay --no-tail')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        (_, stdout, stderr) = self.ssh.exec_command(
            '/snap/bin/juju destroy-controller -y abot-controller '
            '--destroy-all-models')
        self.__logger.debug("stdout:\n%s", stdout.read().decode("utf-8"))
        self.__logger.debug("stderr:\n%s", stderr.read().decode("utf-8"))
        for fip in self.cloud.list_floating_ips():
            self.cloud.delete_floating_ip(fip.id)
        if self.image_alt:
            self.cloud.delete_image(self.image_alt)
        if self.flavor_alt:
            self.orig_cloud.delete_flavor(self.flavor_alt.id)
        super().clean()


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
    with open(file_path, encoding='utf-8') as test_result:
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
