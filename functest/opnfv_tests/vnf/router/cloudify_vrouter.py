#!/usr/bin/env python

# Copyright (c) 2017 Okinawa Open Laboratory and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

"""vrouter testcase implementation."""

import logging
import os
import time

import pkg_resources

from functest.core import cloudify
from functest.opnfv_tests.vnf.router import vrouter_base
from functest.opnfv_tests.vnf.router.utilvnf import Utilvnf
from functest.utils import config
from functest.utils import env
from functest.utils import functest_utils


__author__ = "Shuya Nakama <shuya.nakama@okinawaopenlabs.org>"


class CloudifyVrouter(cloudify.Cloudify):
    # pylint: disable=too-many-instance-attributes
    """vrouter testcase deployed with Cloudify Orchestrator."""

    __logger = logging.getLogger(__name__)

    filename_alt = '/home/opnfv/functest/images/vyos-1.1.8-amd64.qcow2'

    flavor_alt_ram = 1024
    flavor_alt_vcpus = 1
    flavor_alt_disk = 3

    check_console_loop = 12

    cop_yaml = ("https://github.com/cloudify-cosmo/cloudify-openstack-plugin/"
                "releases/download/2.14.7/plugin.yaml")
    cop_wgn = ("https://github.com/cloudify-cosmo/cloudify-openstack-plugin/"
               "releases/download/2.14.7/cloudify_openstack_plugin-2.14.7-py27"
               "-none-linux_x86_64-centos-Core.wgn")

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = "vyos_vrouter"
        super().__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = getattr(
                config.CONF, f'vnf_{self.case_name}_config')
        except Exception as exc:
            raise Exception("VNF config file not found") from exc

        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/router')
        config_file = os.path.join(self.case_dir, self.config)
        self.orchestrator = dict(
            requirements=functest_utils.get_parameter_from_yaml(
                "orchestrator.requirements", config_file),
        )
        self.details['orchestrator'] = dict(
            name=functest_utils.get_parameter_from_yaml(
                "orchestrator.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "orchestrator.version", config_file),
            status='ERROR',
            result=''
        )
        self.__logger.debug("Orchestrator configuration %s", self.orchestrator)
        self.__logger.debug("name = %s", __name__)
        self.vnf = dict(
            descriptor=functest_utils.get_parameter_from_yaml(
                "vnf.descriptor", config_file),
            inputs=functest_utils.get_parameter_from_yaml(
                "vnf.inputs", config_file),
            requirements=functest_utils.get_parameter_from_yaml(
                "vnf.requirements", config_file)
        )
        self.details['vnf'] = dict(
            descriptor_version=self.vnf['descriptor']['version'],
            name=functest_utils.get_parameter_from_yaml(
                "vnf.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "vnf.version", config_file),
        )
        self.__logger.debug("VNF configuration: %s", self.vnf)

        self.util = Utilvnf()
        self.util.set_credentials(self.cloud)
        credentials = {"cloud": self.cloud}
        self.util_info = {"credentials": credentials,
                          "vnf_data_dir": self.util.vnf_data_dir}

        self.details['test_vnf'] = dict(
            name=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.version", config_file)
        )
        self.images = functest_utils.get_parameter_from_yaml(
            "tenant_images", config_file)
        self.__logger.info("Images needed for vrouter: %s", self.images)

        self.image_alt = None
        self.flavor_alt = None

    def check_requirements(self):
        if env.get('NEW_USER_ROLE').lower() == "admin":
            self.__logger.warning(
                "Defining NEW_USER_ROLE=admin will easily break the testcase "
                "because Cloudify doesn't manage tenancy (e.g. subnet "
                "overlapping)")

    def execute(self):
        # pylint: disable=too-many-locals,too-many-statements
        """
        Deploy Cloudify Manager.
        network, security group, fip, VM creation
        """
        # network creation
        super().execute()
        start_time = time.time()
        self.put_private_key()
        self.upload_cfy_plugins(self.cop_yaml, self.cop_wgn)

        self.image_alt = self.publish_image_alt()
        self.flavor_alt = self.create_flavor_alt()

        duration = time.time() - start_time
        self.details['orchestrator'].update(status='PASS', duration=duration)

        self.vnf['inputs'].update(dict(
            external_network_name=self.ext_net.name))
        self.vnf['inputs'].update(dict(
            target_vnf_image_id=self.image_alt.id))
        self.vnf['inputs'].update(dict(
            reference_vnf_image_id=self.image_alt.id))
        self.vnf['inputs'].update(dict(
            target_vnf_flavor_id=self.flavor_alt.id))
        self.vnf['inputs'].update(dict(
            reference_vnf_flavor_id=self.flavor_alt.id))
        self.vnf['inputs'].update(dict(
            keystone_username=self.project.user.name))
        self.vnf['inputs'].update(dict(
            keystone_password=self.project.password))
        self.vnf['inputs'].update(dict(
            keystone_tenant_name=self.project.project.name))
        self.vnf['inputs'].update(dict(
            keystone_user_domain_name=os.environ.get(
                'OS_USER_DOMAIN_NAME', 'Default')))
        self.vnf['inputs'].update(dict(
            keystone_project_domain_name=os.environ.get(
                'OS_PROJECT_DOMAIN_NAME', 'Default')))
        self.vnf['inputs'].update(dict(
            region=os.environ.get('OS_REGION_NAME', 'RegionOne')))
        self.vnf['inputs'].update(dict(
            keystone_url=self.get_public_auth_url(self.orig_cloud)))

        if self.deploy_vnf() and self.test_vnf():
            self.result = 100
            return 0
        self.result = 1/3 * 100
        return 1

    def deploy_vnf(self):
        start_time = time.time()
        self.__logger.info("Upload VNFD")
        descriptor = self.vnf['descriptor']
        self.util_info["cfy"] = self.cfy_client
        self.util_info["cfy_manager_ip"] = self.fip.floating_ip_address
        self.util_info["deployment_name"] = descriptor.get('name')

        self.cfy_client.blueprints.upload(
            descriptor.get('file_name'), descriptor.get('name'))

        self.__logger.info("Create VNF Instance")
        self.cfy_client.deployments.create(
            descriptor.get('name'), descriptor.get('name'),
            self.vnf.get('inputs'))

        cloudify.wait_for_execution(
            self.cfy_client, cloudify.get_execution_id(
                self.cfy_client, descriptor.get('name')),
            self.__logger, timeout=7200)

        self.__logger.info("Start the VNF Instance deployment")
        execution = self.cfy_client.executions.start(
            descriptor.get('name'), 'install')
        # Show execution log
        execution = cloudify.wait_for_execution(
            self.cfy_client, execution, self.__logger)

        duration = time.time() - start_time

        self.__logger.info(execution)
        if execution.status == 'terminated':
            self.details['vnf'].update(status='PASS', duration=duration)
            result = True
        else:
            self.details['vnf'].update(status='FAIL', duration=duration)
            result = False
        return result

    def test_vnf(self):
        start_time = time.time()
        testing = vrouter_base.VrouterOnBoardingBase(self.util, self.util_info)
        result, test_result_data = testing.test_vnf()
        duration = time.time() - start_time
        if result:
            self.details['test_vnf'].update(
                status='PASS', result='OK', full_result=test_result_data,
                duration=duration)
        else:
            self.details['test_vnf'].update(
                status='FAIL', result='NG', full_result=test_result_data,
                duration=duration)
        return True

    def clean(self):
        self.kill_existing_execution(self.vnf['descriptor'].get('name'))
        if self.image_alt:
            self.cloud.delete_image(self.image_alt)
        if self.flavor_alt:
            self.orig_cloud.delete_flavor(self.flavor_alt.id)
        super().clean()
