#!/usr/bin/env python

# Copyright (c) 2018 Enea AB and others.
#
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0

"""Define the parent class of cinder_test"""

from datetime import datetime
import logging
import time
import uuid

import os_client_config
from xtesting.core import testcase

from functest.utils import config
from functest.utils import env
from functest.utils import functest_utils


class CinderBase(testcase.TestCase):

    """
    Base class for CinderCheck tests that check volume data persistence
    between two VMs shared internal network.
    This class is responsible for creating the image, internal network,
    flavor, volume.
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, **kwargs):
        super(CinderBase, self).__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.cloud = os_client_config.make_shade()
        self.ext_net = functest_utils.get_external_network(self.cloud)
        self.logger.debug("ext_net: %s", self.ext_net)
        self.guid = '-' + str(uuid.uuid4())
        self.network = None
        self.subnet = None
        self.router = None
        self.image = None
        self.flavor = None
        self.vm1 = None
        self.volume = None

    def run(self, **kwargs):  # pylint: disable=too-many-locals
        """
        Begins the test execution which should originate from the subclass
        """
        assert self.cloud
        assert self.ext_net
        self.logger.info('Begin virtual environment setup')

        self.start_time = time.time()
        self.logger.info(
            "CinderCheck Start Time:'%s'",
            datetime.fromtimestamp(self.start_time).strftime(
                '%Y-%m-%d %H:%M:%S'))

        image_base_name = '{}-{}'.format(
            getattr(config.CONF, 'cinder_image_name'), self.guid)
        self.logger.info("Creating image with name: '%s'", image_base_name)
        meta = getattr(config.CONF, 'openstack_extra_properties', None)
        self.logger.info("Image metadata: %s", meta)
        self.image = self.cloud.create_image(
            image_base_name,
            filename=getattr(config.CONF, 'openstack_image_url'),
            meta=meta)
        self.logger.debug("image: %s", self.image)

        private_net_name = getattr(
            config.CONF, 'cinder_private_net_name') + self.guid
        private_subnet_name = str(getattr(
            config.CONF, 'cinder_private_subnet_name') + self.guid)
        private_subnet_cidr = getattr(
            config.CONF, 'cinder_private_subnet_cidr')

        provider = {}
        if hasattr(config.CONF, 'cinder_network_type'):
            provider["network_type"] = getattr(
                config.CONF, 'cinder_network_type')
        if hasattr(config.CONF, 'cinder_physical_network'):
            provider["physical_network"] = getattr(
                config.CONF, 'cinder_physical_network')
        if hasattr(config.CONF, 'cinder_segmentation_id'):
            provider["segmentation_id"] = getattr(
                config.CONF, 'cinder_segmentation_id')
        self.logger.info(
            "Creating network with name: '%s'", private_net_name)
        self.network = self.cloud.create_network(
            private_net_name,
            provider=provider)
        self.logger.debug("network: %s", self.network)

        self.subnet = self.cloud.create_subnet(
            self.network.id,
            subnet_name=private_subnet_name,
            cidr=private_subnet_cidr,
            enable_dhcp=True,
            dns_nameservers=[env.get('NAMESERVER')])
        self.logger.debug("subnet: %s", self.subnet)

        router_name = getattr(config.CONF, 'cinder_router_name') + self.guid
        self.logger.info("Creating router with name: '%s'", router_name)
        self.router = self.cloud.create_router(
            name=router_name,
            ext_gateway_net_id=self.ext_net.id)
        self.logger.debug("router: %s", self.router)
        self.cloud.add_router_interface(self.router, subnet_id=self.subnet.id)

        flavor_name = 'cinder-flavor' + self.guid
        self.logger.info(
            "Creating flavor with name: '%s'", flavor_name)
        self.flavor = self.cloud.create_flavor(
            flavor_name, getattr(config.CONF, 'openstack_flavor_ram'),
            getattr(config.CONF, 'openstack_flavor_vcpus'),
            getattr(config.CONF, 'openstack_flavor_disk'))
        self.logger.debug("flavor: %s", self.flavor)
        self.cloud.set_flavor_specs(
            self.flavor.id, getattr(config.CONF, 'flavor_extra_specs', {}))
        volume_name = 'cinder-volume' + self.guid
        self.logger.info(
            "Creating volume with name: %s", volume_name)
        self.volume = self.cloud.create_volume(
            name=volume_name, size='2')
        self.logger.info("volume: %s", self.volume)

    def execute(self):
        """
        Method called by subclasses after environment has been setup
        :return: the exit code
        """
        self.logger.info('Begin test execution')
        self.stop_time = time.time()
        write_data = self.write_data()
        if write_data == testcase.TestCase.EX_OK:
            result = self.read_data()
        else:
            result = testcase.TestCase.EX_RUN_ERROR
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
        assert self.cloud
        self.cloud.delete_image(self.image)
        self.cloud.remove_router_interface(self.router, self.subnet.id)
        self.cloud.delete_router(self.router.id)
        self.cloud.delete_network(self.network.id)
        self.cloud.delete_flavor(self.flavor.id)
        self.cloud.delete_volume(self.volume.id)

    def write_data(self):
        """
        Method to be implemented by subclasses
        Begins the real test after the OpenStack environment has been setup
        :return: T/F
        """
        raise NotImplementedError('cinder test execution is not implemented')

    def read_data(self):
        """
        Method to be implemented by subclasses
        Begins the real test after the OpenStack environment has been setup
        :return: T/F
        """
        raise NotImplementedError('cinder test execution is not implemented')
