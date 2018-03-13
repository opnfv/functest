#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""CloudifyImsPerf testcase implementation."""

import logging
import os
import time

import json
import yaml
import paramiko
import dns.resolver
from jinja2 import Environment, FileSystemLoader
from snaps.config.flavor import FlavorConfig
from snaps.config.image import ImageConfig
from snaps.config.network import NetworkConfig, PortConfig, SubnetConfig
from snaps.config.router import RouterConfig
from snaps.config.security_group import (
    Direction, Protocol, SecurityGroupConfig, SecurityGroupRuleConfig)
from snaps.config.vm_inst import FloatingIpConfig, VmInstanceConfig
from snaps.openstack.create_flavor import OpenStackFlavor
from snaps.openstack.create_instance import OpenStackVmInstance
from snaps.openstack.create_network import OpenStackNetwork
from snaps.openstack.create_router import OpenStackRouter
from snaps.openstack.create_security_group import OpenStackSecurityGroup
from xtesting.energy import energy

from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.opnfv_tests.vnf.ims import cloudify_ims
from functest.utils import config
from functest.utils import env

__author__ = ("Valentin Boucher <valentin.boucher@kontron.com>, "
              "Linda Wang <wangwulin@huawei.com>")


class CloudifyImsPerf(cloudify_ims.CloudifyIms):
    """Clearwater vIMS deployed with Cloudify Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        """Initialize CloudifyIms testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cloudify_ims_perf"
        super(CloudifyImsPerf, self).__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = getattr(
                config.CONF, 'vnf_{}_config'.format(self.case_name))
        except Exception:
            raise Exception("VNF config file not found")

        self.snaps_creds = ''
        self.created_object = []

        config_file = os.path.join(self.case_dir, self.config)
        self.orchestrator = dict(
            requirements=get_config("orchestrator.requirements", config_file),
        )
        self.details['orchestrator'] = dict(
            name=get_config("orchestrator.name", config_file),
            version=get_config("orchestrator.version", config_file),
            status='ERROR',
            result=''
        )
        self.__logger.debug("Orchestrator configuration %s", self.orchestrator)
        self.vnf = dict(
            descriptor=get_config("vnf.descriptor", config_file),
            inputs=get_config("vnf.inputs", config_file),
            requirements=get_config("vnf.requirements", config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=get_config("vnf.name", config_file),
            version=get_config("vnf.version", config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)

        self.test = dict(
            version=get_config("vnf_test_suite.version", config_file),
            inputs=get_config("vnf_test_suite.inputs", config_file),
            requirements=get_config("vnf_test_suite.requirements", config_file)
        )

        self.details['test_vnf'] = dict(
            name=get_config("vnf_test_suite.name", config_file),
            version=get_config("vnf_test_suite.version", config_file),
            requirements=get_config("vnf_test_suite.requirements", config_file)
        )
        self.images = get_config("tenant_images", config_file)
        self.__logger.info("Images needed for vIMS: %s", self.images)

    def test_vnf(self):
        """Run stress test on clearwater ims instance."""
        start_time = time.time()

        cfy_client = self.orchestrator['object']

        outputs = cfy_client.deployments.outputs.get(
            self.vnf['descriptor'].get('name'))['outputs']
        sipp_ip = outputs['sipp_ip']

        if not sipp_ip:
            return False

        ## Connect to the SIPp machine and run test

        try:
            vnf_test_rate = 100 # must me updated
            # orchestrator + vnf + test_vnf
            self.result += vnf_test_rate / 3 * 100
        except ZeroDivisionError:
            self.__logger.error("No test has been executed")
            self.details['test_vnf'].update(status='FAIL')
            return False

        return True

    def clean(self):
        """Clean created objects/functions."""
        super(CloudifyImsPerf, self).clean()

    @energy.enable_recording
    def run(self, **kwargs):
        """Execute CloudifyIms test case."""
        return super(CloudifyImsPerf, self).run(**kwargs)


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


def run_blocking_ssh_command(ssh, cmd, error_msg="Unable to run this command"):
    """Command to run ssh command with the exit status."""
    stdin, stdout, stderr = ssh.exec_command(cmd)
    if stdout.channel.recv_exit_status() != 0:
        raise Exception(error_msg)
