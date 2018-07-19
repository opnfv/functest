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
import yaml

import pkg_resources
from xtesting.core import testcase

from functest.core import singlevm
from functest.opnfv_tests.vnf.ims import clearwater
from functest.utils import config

__author__ = "Valentin Boucher <valentin.boucher@kontron.com>"


class HeatIms(singlevm.SingleVm2):
    """Clearwater vIMS deployed with Heat Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    filename_alt = ('/home/opnfv/functest/images/'
                    'ubuntu-14.04-server-cloudimg-amd64-disk1.img')

    flavor_alt_ram = 2048
    flavor_alt_vcpus = 2
    flavor_alt_disk = 25

    quota_security_group = 20
    quota_security_group_rule = 100
    quota_port = 50

    def __init__(self, **kwargs):
        """Initialize HeatIms testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "heat_ims"
        super(HeatIms, self).__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = getattr(
                config.CONF, 'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")

        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/ims')
        config_file = os.path.join(self.case_dir, self.config)

        self.vnf = dict(
            descriptor=get_config("vnf.descriptor", config_file),
            parameters=get_config("vnf.inputs", config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=get_config("vnf.name", config_file),
            version=get_config("vnf.version", config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)

        self.image_alt = None
        self.flavor_alt = None
        self.stack = None
        self.clearwater = None

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

        if (self.deploy_vnf() and self.test_vnf()):
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
            self.start_time = time.time()
            self.result = 0
            if not self.execute():
                self.result = 100
                status = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception('Cannot run %s', self.case_name)
        finally:
            self.stop_time = time.time()
        return status

    def deploy_vnf(self):
        """Deploy Clearwater IMS."""
        start_time = time.time()

        super(HeatIms, self).prepare()

        self.image_alt = self.publish_image_alt()
        self.flavor_alt = self.create_flavor_alt()
        # KeyPair + Image + Flavor OK

        descriptor = self.vnf['descriptor']
        parameters = self.vnf['parameters']

        parameters['public_mgmt_net_id'] = self.ext_net.id
        parameters['public_sig_net_id'] = self.ext_net.id
        parameters['flavor'] = self.flavor_alt.name
        parameters['image'] = self.image_alt.name
        parameters['key_name'] = self.keypair.name

        self.__logger.info("Create Heat Stack")
        self.stack = self.cloud.create_stack(name=descriptor.get('name'),
                                             template_file=(
                                                 descriptor.get('file_name')),
                                             wait=True,
                                             **parameters)
        self.__logger.debug("stack: %s", self.stack)

        servers = self.cloud.list_servers(detailed=True)
        self.__logger.debug("servers: %s", servers)
        for server in servers:
            if 'ellis' in server.name:
                self.__logger.debug("server: %s", server)
                ellis_ip = server.public_v4

        assert ellis_ip
        self.clearwater = clearwater.ClearwaterTesting(self.case_name,
                                                       ellis_ip)
        # This call can take time and many retry because Heat is
        # an infrastructure orchestrator so when Heat say "stack created"
        # it means that all OpenStack ressources are created but not that
        # Clearwater are up and ready (Cloud-Init script still running)
        self.clearwater.availability_check_by_creating_numbers()

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

        short_result = self.clearwater.run_clearwater_live_test(
            dns_ip=dns_ip,
            public_domain=self.vnf['parameters']["zone"])
        duration = time.time() - start_time
        self.__logger.info(short_result)
        self.details['test_vnf'] = dict(result=short_result,
                                        duration=duration)
        try:
            vnf_test_rate = short_result['passed'] / (
                short_result['total'] - short_result['skipped'])
            # orchestrator + vnf + test_vnf
            self.result += vnf_test_rate / 3 * 100
        except ZeroDivisionError:
            self.__logger.error("No test has been executed")
            self.details['test_vnf'].update(status='FAIL')
            return False
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot calculate results")
            self.details['test_vnf'].update(status='FAIL')
            return False
        return True if vnf_test_rate > 0 else False

    def clean(self):
        """Clean created objects/functions."""
        assert self.cloud
        try:
            if self.stack:
                self.cloud.delete_stack(self.stack.id, wait=True)
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot clean stack ressources")
        super(HeatIms, self).clean()


# ----------------------------------------------------------
#
#               YAML UTILS
#
# -----------------------------------------------------------
def get_config(parameter, file_path):
    """
    Get config parameter.

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
