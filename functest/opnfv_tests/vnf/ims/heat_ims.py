#!/usr/bin/env python

# Copyright (c) 2018 Kontron, Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""HeatIms testcase implementation."""

from __future__ import division

import logging
import os
import re
import time
import tempfile

import paramiko
import pkg_resources
from xtesting.core import testcase

from functest.core import singlevm
from functest.opnfv_tests.vnf.ims import clearwater
from functest.utils import config
from functest.utils import env
from functest.utils import functest_utils

__author__ = "Valentin Boucher <valentin.boucher@kontron.com>"


class HeatIms(singlevm.VmReady2):
    # pylint: disable=too-many-instance-attributes
    """Clearwater vIMS deployed with Heat Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    filename = ('/home/opnfv/functest/images/'
                'ubuntu-14.04-server-cloudimg-amd64-disk1.img')

    flavor_ram = 1024
    flavor_vcpus = 1
    flavor_disk = 3

    quota_security_group = 20
    quota_security_group_rule = 100
    quota_port = 50

    parameters = {
        'private_mgmt_net_cidr': '192.168.100.0/24',
        'private_mgmt_net_gateway': '192.168.100.254',
        'private_mgmt_net_pool_start': '192.168.100.1',
        'private_mgmt_net_pool_end': '192.168.100.253'}

    def __init__(self, **kwargs):
        """Initialize HeatIms testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "heat_ims"
        super().__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = getattr(
                config.CONF, f'vnf_{self.case_name}_config')
        except Exception as exc:
            raise Exception("VNF config file not found") from exc

        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/ims')
        config_file = os.path.join(self.case_dir, self.config)

        self.vnf = dict(
            descriptor=functest_utils.get_parameter_from_yaml(
                "vnf.descriptor", config_file),
            parameters=functest_utils.get_parameter_from_yaml(
                "vnf.inputs", config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=functest_utils.get_parameter_from_yaml(
                "vnf.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "vnf.version", config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)
        self.keypair = None
        self.stack = None
        self.clearwater = None
        self.role = None
        (_, self.key_filename) = tempfile.mkstemp()

    def create_network_resources(self):
        pass

    def execute(self):
        # pylint: disable=too-many-locals,too-many-statements
        """
        Prepare Tenant/User

        network, security group, fip, VM creation
        """
        self.orig_cloud.set_network_quotas(
            self.project.project.name,
            security_group=self.quota_security_group,
            security_group_rule=self.quota_security_group_rule,
            port=self.quota_port)
        if not self.orig_cloud.get_role("heat_stack_owner"):
            self.role = self.orig_cloud.create_role("heat_stack_owner")
        self.orig_cloud.grant_role(
            "heat_stack_owner", user=self.project.user.id,
            project=self.project.project.id,
            domain=self.project.domain.id)
        self.keypair = self.cloud.create_keypair(
            f'{self.case_name}-kp_{self.guid}')
        self.__logger.info("keypair:\n%s", self.keypair.private_key)
        with open(
                self.key_filename, 'w', encoding='utf-8') as private_key_file:
            private_key_file.write(self.keypair.private_key)

        if self.deploy_vnf() and self.test_vnf():
            self.result = 100
            return 0
        self.result = 1/3 * 100
        return 1

    def run(self, **kwargs):
        """Deploy and test clearwater

        Here are the main actions:
        - deploy clearwater stack via heat
        - test the vnf instance

        Returns:
        - TestCase.EX_OK
        - TestCase.EX_RUN_ERROR on error
        """
        status = testcase.TestCase.EX_RUN_ERROR
        try:
            assert self.cloud
            assert super().run(
                **kwargs) == testcase.TestCase.EX_OK
            self.result = 0
            if not self.execute():
                self.result = 100
                status = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception('Cannot run %s', self.case_name)
        finally:
            self.stop_time = time.time()
        return status

    def _monit(self, username="ubuntu", timeout=60):
        servers = self.cloud.list_servers(detailed=True)
        self.__logger.debug("servers: %s", servers)
        for server in servers:
            if 'ns' in server.name:
                break
            self.__logger.info("server:\n%s", server.name)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
            ssh.connect(
                server.public_v4, username=username,
                key_filename=self.key_filename, timeout=timeout)
            (_, stdout, _) = ssh.exec_command('sudo monit summary')
            self.__logger.info("output:\n%s", stdout.read().decode("utf-8"))
            ssh.close()

    def deploy_vnf(self):
        """Deploy Clearwater IMS."""
        start_time = time.time()
        descriptor = self.vnf['descriptor']
        parameters = self.vnf['parameters']

        parameters['public_mgmt_net_id'] = self.ext_net.id
        parameters['flavor'] = self.flavor.name
        parameters['image'] = self.image.name
        parameters['key_name'] = self.keypair.name
        parameters['external_mgmt_dns_ip'] = env.get('NAMESERVER')
        parameters.update(self.parameters)

        self.__logger.info("Create Heat Stack")
        self.stack = self.cloud.create_stack(
            name=descriptor.get('name'),
            template_file=descriptor.get('file_name'),
            wait=True, **parameters)
        self.__logger.debug("stack: %s", self.stack)

        self._monit()

        servers = self.cloud.list_servers(detailed=True)
        self.__logger.debug("servers: %s", servers)
        for server in servers:
            if not self.check_regex_in_console(
                    server.name, regex='Cloud-init .* finished at ', loop=1):
                return False
            if 'ellis' in server.name:
                self.__logger.debug("ellis: %s", server)
                ellis_ip = server.public_v4
            elif 'bono' in server.name:
                self.__logger.debug("bono: %s", server)
                bono_ip = server.public_v4

        assert ellis_ip
        assert bono_ip
        self.clearwater = clearwater.ClearwaterTesting(
            self.case_name, bono_ip, ellis_ip)
        # This call can take time and many retry because Heat is
        # an infrastructure orchestrator so when Heat say "stack created"
        # it means that all OpenStack ressources are created but not that
        # Clearwater are up and ready (Cloud-Init script still running)
        self.clearwater.availability_check()

        duration = time.time() - start_time

        self.details['vnf'].update(status='PASS', duration=duration)
        self.result += 1/3 * 100

        return True

    def test_vnf(self):
        """Run test on clearwater ims instance."""
        start_time = time.time()
        outputs = self.cloud.get_stack(self.stack.id).outputs
        self.__logger.debug("stack outputs: %s", outputs)
        dns_ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(outputs))[0]
        if not dns_ip:
            return False
        short_result, vnf_test_rate = self.clearwater.run_clearwater_live_test(
            public_domain=self.vnf['parameters']["zone"])
        duration = time.time() - start_time
        self.__logger.info(short_result)
        self.details['test_vnf'] = dict(result=short_result, duration=duration)
        self.result += vnf_test_rate / 3 * 100
        if vnf_test_rate == 0:
            self.details['test_vnf'].update(status='FAIL')
        self._monit()
        return bool(vnf_test_rate > 0)

    def clean(self):
        """Clean created objects/functions."""
        assert self.cloud
        try:
            if self.stack:
                self.cloud.delete_stack(self.stack.id, wait=True)
        except TypeError:
            # shade raises TypeError exceptions when checking stack status
            pass
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean stack ressources")
        super().clean()
        if self.role:
            self.orig_cloud.delete_role(self.role.id)
