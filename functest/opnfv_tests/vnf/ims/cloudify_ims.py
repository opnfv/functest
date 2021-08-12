#!/usr/bin/env python

# Copyright (c) 2017 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

"""CloudifyIms testcase implementation."""

from __future__ import division

import logging
import os
import time

import pkg_resources
import six

from functest.core import cloudify
from functest.opnfv_tests.vnf.ims import clearwater
from functest.utils import config
from functest.utils import env
from functest.utils import functest_utils

__author__ = "Valentin Boucher <valentin.boucher@orange.com>"


class CloudifyIms(cloudify.Cloudify):
    """Clearwater vIMS deployed with Cloudify Orchestrator Case."""

    __logger = logging.getLogger(__name__)

    filename_alt = ('/home/opnfv/functest/images/'
                    'ubuntu-14.04-server-cloudimg-amd64-disk1.img')

    flavor_alt_ram = 1024
    flavor_alt_vcpus = 1
    flavor_alt_disk = 3

    quota_security_group = 20
    quota_security_group_rule = 100
    quota_port = 50

    cop_yaml = ("https://github.com/cloudify-cosmo/cloudify-openstack-plugin/"
                "releases/download/2.14.7/plugin.yaml")
    cop_wgn = ("https://github.com/cloudify-cosmo/cloudify-openstack-plugin/"
               "releases/download/2.14.7/cloudify_openstack_plugin-2.14.7-py27"
               "-none-linux_x86_64-centos-Core.wgn")

    def __init__(self, **kwargs):
        """Initialize CloudifyIms testcase object."""
        if "case_name" not in kwargs:
            kwargs["case_name"] = "cloudify_ims"
        super().__init__(**kwargs)

        # Retrieve the configuration
        try:
            self.config = getattr(
                config.CONF, 'vnf_{}_config'.format(self.case_name))
        except Exception as exc:
            raise Exception("VNF config file not found") from exc

        self.case_dir = pkg_resources.resource_filename(
            'functest', 'opnfv_tests/vnf/ims')
        config_file = os.path.join(self.case_dir, self.config)

        self.details['orchestrator'] = dict(
            name=functest_utils.get_parameter_from_yaml(
                "orchestrator.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "orchestrator.version", config_file),
            status='ERROR',
            result=''
        )

        self.vnf = dict(
            descriptor=functest_utils.get_parameter_from_yaml(
                "vnf.descriptor", config_file),
            inputs=functest_utils.get_parameter_from_yaml(
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

        self.details['test_vnf'] = dict(
            name=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.name", config_file),
            version=functest_utils.get_parameter_from_yaml(
                "vnf_test_suite.version", config_file)
        )

        self.image_alt = None
        self.flavor_alt = None
        self.clearwater = None

    def check_requirements(self):
        if env.get('NEW_USER_ROLE').lower() == "admin":
            self.__logger.warning(
                "Defining NEW_USER_ROLE=admin will easily break the testcase "
                "because Cloudify doesn't manage tenancy (e.g. subnet "
                "overlapping)")

    def execute(self):
        """
        Deploy Cloudify Manager.

        network, security group, fip, VM creation
        """
        assert super().execute() == 0
        start_time = time.time()
        self.orig_cloud.set_network_quotas(
            self.project.project.name,
            security_group=self.quota_security_group,
            security_group_rule=self.quota_security_group_rule,
            port=self.quota_port)
        self.__logger.info("Put OpenStack creds in manager")
        cfy_creds = dict(
            keystone_username=self.project.user.name,
            keystone_password=self.project.password,
            keystone_tenant_name=self.project.project.name,
            keystone_url=self.get_public_auth_url(self.orig_cloud),
            region=os.environ.get('OS_REGION_NAME', 'RegionOne'),
            user_domain_name=os.environ.get(
                'OS_USER_DOMAIN_NAME', 'Default'),
            project_domain_name=os.environ.get(
                'OS_PROJECT_DOMAIN_NAME', 'Default'))
        self.__logger.info("Set creds for cloudify manager %s", cfy_creds)

        for loop in range(10):
            try:
                secrets_list = self.cfy_client.secrets.list()
                for k, val in six.iteritems(cfy_creds):
                    if not any(d.get('key', None) == k for d in secrets_list):
                        self.cfy_client.secrets.create(k, val)
                    else:
                        self.cfy_client.secrets.update(k, val)
                break
            except Exception:  # pylint: disable=broad-except
                self.__logger.info(
                    "try %s: Cannot create secrets", loop + 1)
                time.sleep(30)
        else:
            self.__logger.error("Cannot create secrets")
            return 1

        duration = time.time() - start_time

        self.put_private_key()
        self.upload_cfy_plugins(self.cop_yaml, self.cop_wgn)

        self.details['orchestrator'].update(status='PASS', duration=duration)

        self.vnf['inputs'].update(dict(
            external_network_name=self.ext_net.name,
            network_name=self.network.name,
            key_pair_name=self.keypair.name
        ))
        if self.deploy_vnf() and self.test_vnf():
            self.result = 100
            return 0
        self.result = 1/3 * 100
        return 1

    def deploy_vnf(self):
        """Deploy Clearwater IMS."""
        start_time = time.time()

        secgroups = self.cloud.list_security_groups(
            filters={'name': 'default',
                     'project_id': self.project.project.id})
        if secgroups:
            secgroup = secgroups[0]
        else:
            self.__logger.error("No 'default' security group in project %s",
                                self.project.project.name)
            return False

        self.cloud.create_security_group_rule(
            secgroup.id, port_range_min=22, port_range_max=22,
            protocol='tcp', direction='ingress')

        self.__logger.info("Upload VNFD")
        descriptor = self.vnf['descriptor']
        self.cfy_client.blueprints.upload(
            descriptor.get('file_name'), descriptor.get('name'))

        self.image_alt = self.publish_image_alt()
        self.flavor_alt = self.create_flavor_alt()
        self.vnf['inputs'].update(dict(
            image_id=self.image_alt.id,
            flavor_id=self.flavor_alt.id,
        ))

        self.__logger.info("Create VNF Instance")
        self.cfy_client.deployments.create(
            descriptor.get('name'), descriptor.get('name'),
            self.vnf.get('inputs'))

        cloudify.wait_for_execution(
            self.cfy_client,
            cloudify.get_execution_id(self.cfy_client, descriptor.get('name')),
            self.__logger, timeout=300)

        self.__logger.info("Start the VNF Instance deployment")
        execution = self.cfy_client.executions.start(
            descriptor.get('name'), 'install')
        # Show execution log
        execution = cloudify.wait_for_execution(
            self.cfy_client, execution, self.__logger, timeout=3600)

        self.__logger.info(execution)
        if execution.status != 'terminated':
            self.details['vnf'].update(status='FAIL',
                                       duration=time.time() - start_time)
            return False

        ellis_ip = self.cfy_client.deployments.outputs.get(
            self.vnf['descriptor'].get('name'))['outputs']['ellis_ip']
        bono_ip = self.cfy_client.deployments.outputs.get(
            self.vnf['descriptor'].get('name'))['outputs']['bono_ip']
        self.clearwater = clearwater.ClearwaterTesting(
            self.case_name, bono_ip, ellis_ip)
        self.clearwater.availability_check()

        self.details['vnf'].update(status='PASS',
                                   duration=time.time() - start_time)
        self.result += 1/3 * 100
        return True

    def test_vnf(self):
        """Run test on clearwater ims instance."""
        start_time = time.time()
        dns_ip = self.cfy_client.deployments.outputs.get(
            self.vnf['descriptor'].get('name'))['outputs']['dns_ip']
        if not dns_ip:
            return False
        short_result, vnf_test_rate = self.clearwater.run_clearwater_live_test(
            public_domain=self.vnf['inputs']["public_domain"])
        duration = time.time() - start_time
        self.__logger.info(short_result)
        self.details['test_vnf'].update(result=short_result, duration=duration)
        self.result += vnf_test_rate / 3 * 100
        if vnf_test_rate == 0:
            self.details['test_vnf'].update(status='FAIL')
        return bool(vnf_test_rate > 0)

    def clean(self):
        """Clean created objects/functions."""
        self.kill_existing_execution(self.vnf['descriptor'].get('name'))
        if self.image_alt:
            self.cloud.delete_image(self.image_alt)
        if self.flavor_alt:
            self.orig_cloud.delete_flavor(self.flavor_alt.id)
        super().clean()
