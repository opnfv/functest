#!/usr/bin/env python

# Copyright (c) 2017 Cable Television Laboratories, Inc. and others.
#
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the parent class of vping_ssh and vping_userdata testcases."""

from datetime import datetime
import logging
import time
import uuid

from snaps.config.flavor import FlavorConfig
from snaps.config.network import NetworkConfig
from snaps.config.network import SubnetConfig
from snaps.config.router import RouterConfig
from snaps.openstack.create_flavor import OpenStackFlavor
from snaps.openstack.create_image import OpenStackImage
from snaps.openstack.create_network import OpenStackNetwork
from snaps.openstack.create_router import OpenStackRouter
from snaps.openstack.tests import openstack_tests
from xtesting.core import testcase

from functest.opnfv_tests.openstack.snaps import snaps_utils
from functest.utils import config
from functest.utils import env


class VPingBase(testcase.TestCase):

    """
    Base class for vPing tests that check connectivity between two VMs shared
    internal network.
    This class is responsible for creating the image, internal network.
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, **kwargs):
        super(VPingBase, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.os_creds = kwargs.get('os_creds') or snaps_utils.get_credentials()
        self.creators = list()
        self.image_creator = None
        self.network_creator = None
        self.vm1_creator = None
        self.vm2_creator = None
        self.router_creator = None

        # Shared metadata
        self.guid = '-' + str(uuid.uuid4())

        self.router_name = getattr(
            config.CONF, 'vping_router_name') + self.guid
        self.vm1_name = getattr(
            config.CONF, 'vping_vm_name_1') + self.guid
        self.vm2_name = getattr(config.CONF, 'vping_vm_name_2') + self.guid

        self.vm_boot_timeout = getattr(config.CONF, 'vping_vm_boot_timeout')
        self.vm_delete_timeout = getattr(
            config.CONF, 'vping_vm_delete_timeout')
        self.vm_ssh_connect_timeout = getattr(
            config.CONF, 'vping_vm_ssh_connect_timeout')
        self.ping_timeout = getattr(config.CONF, 'vping_ping_timeout')
        self.flavor_name = 'vping-flavor' + self.guid

        # Move this configuration option up for all tests to leverage
        if hasattr(config.CONF, 'snaps_images_cirros'):
            self.cirros_image_config = getattr(
                config.CONF, 'snaps_images_cirros')
        else:
            self.cirros_image_config = None

    def run(self, **kwargs):  # pylint: disable=too-many-locals
        """
        Begins the test execution which should originate from the subclass
        """
        self.logger.info('Begin virtual environment setup')

        self.start_time = time.time()
        self.logger.info(
            "vPing Start Time:'%s'",
            datetime.fromtimestamp(self.start_time).strftime(
                '%Y-%m-%d %H:%M:%S'))

        image_base_name = '{}-{}'.format(
            getattr(config.CONF, 'vping_image_name'), self.guid)
        os_image_settings = openstack_tests.cirros_image_settings(
            image_base_name, image_metadata=self.cirros_image_config)
        self.logger.info("Creating image with name: '%s'", image_base_name)

        self.image_creator = OpenStackImage(
            self.os_creds, os_image_settings)
        self.image_creator.create()
        self.creators.append(self.image_creator)

        private_net_name = getattr(
            config.CONF, 'vping_private_net_name') + self.guid
        private_subnet_name = str(getattr(
            config.CONF, 'vping_private_subnet_name') + self.guid)
        private_subnet_cidr = getattr(config.CONF, 'vping_private_subnet_cidr')

        vping_network_type = None
        vping_physical_network = None
        vping_segmentation_id = None

        if hasattr(config.CONF, 'vping_network_type'):
            vping_network_type = getattr(config.CONF, 'vping_network_type')
        if hasattr(config.CONF, 'vping_physical_network'):
            vping_physical_network = getattr(
                config.CONF, 'vping_physical_network')
        if hasattr(config.CONF, 'vping_segmentation_id'):
            vping_segmentation_id = getattr(
                config.CONF, 'vping_segmentation_id')

        self.logger.info(
            "Creating network with name: '%s'", private_net_name)
        subnet_settings = SubnetConfig(
            name=private_subnet_name,
            cidr=private_subnet_cidr,
            dns_nameservers=[env.get('NAMESERVER')])
        self.network_creator = OpenStackNetwork(
            self.os_creds,
            NetworkConfig(
                name=private_net_name,
                network_type=vping_network_type,
                physical_network=vping_physical_network,
                segmentation_id=vping_segmentation_id,
                subnet_settings=[subnet_settings]))
        self.network_creator.create()
        self.creators.append(self.network_creator)

        # Creating router to external network
        self.logger.info("Creating router with name: '%s'", self.router_name)
        ext_net_name = snaps_utils.get_ext_net_name(self.os_creds)
        self.router_creator = OpenStackRouter(
            self.os_creds,
            RouterConfig(
                name=self.router_name,
                external_gateway=ext_net_name,
                internal_subnets=[subnet_settings.name]))
        self.router_creator.create()
        self.creators.append(self.router_creator)

        self.logger.info(
            "Creating flavor with name: '%s'", self.flavor_name)
        flavor_ram = getattr(config.CONF, 'openstack_flavor_ram')
        flavor_metadata = getattr(config.CONF, 'flavor_extra_specs', None)

        flavor_creator = OpenStackFlavor(
            self.os_creds,
            FlavorConfig(name=self.flavor_name, ram=flavor_ram, disk=1,
                         vcpus=1, metadata=flavor_metadata))
        flavor_creator.create()
        self.creators.append(flavor_creator)

    def _execute(self):
        """
        Method called by subclasses after environment has been setup
        :return: the exit code
        """
        self.logger.info('Begin test execution')

        test_ip = self.vm1_creator.get_port_ip(
            self.vm1_creator.instance_settings.port_settings[0].name)

        if self.vm1_creator.vm_active(
                block=True) and self.vm2_creator.vm_active(block=True):
            result = self._do_vping(self.vm2_creator, test_ip)
        else:
            raise Exception('VMs never became active')

        self.stop_time = time.time()

        if result != testcase.TestCase.EX_OK:
            self.result = 0
            return testcase.TestCase.EX_RUN_ERROR

        self.result = 100
        return testcase.TestCase.EX_OK

    def clean(self):
        """
        Cleanup all OpenStack objects. Should be called on completion
        :return:
        """
        if getattr(config.CONF, 'vping_cleanup_objects') == 'True':
            for creator in reversed(self.creators):
                try:
                    creator.clean()
                except Exception:  # pylint: disable=broad-except
                    self.logger.exception('Unexpected error cleaning')

    def _do_vping(self, vm_creator, test_ip):
        """
        Method to be implemented by subclasses
        Begins the real test after the OpenStack environment has been setup
        :param vm_creator: the SNAPS VM instance creator object
        :param test_ip: the IP to which the VM needs to issue the ping
        :return: T/F
        """
        raise NotImplementedError('vping execution is not implemented')
