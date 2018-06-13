#!/usr/bin/env python

# Copyright (c) 2018 Orange and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import os
import tempfile
import time
import uuid

import os_client_config
import paramiko
import shade
from xtesting.core import testcase

from functest.utils import config
from functest.utils import env
from functest.utils import functest_utils

class Simple(testcase.TestCase):
    # pylint: disable=too-many-instance-attributes

    __logger = logging.getLogger(__name__)
    filename = '/home/opnfv/functest/images/cirros-0.4.0-x86_64-disk.img'
    flavor_ram = 1024
    flavor_vcpus = 1
    flavor_disk = 1
    username = 'cirros'
    cidr = '192.168.0.0/24'
    ssh_connect_timeout = 60

    def __init__(self, **kwargs):
        if "case_name" not in kwargs:
            kwargs["case_name"] = 'vmtp'
        super(Simple, self).__init__(**kwargs)
        self.res_dir = os.path.join(
            getattr(config.CONF, 'dir_results'), self.case_name)
        try:
            cloud_config = os_client_config.get_config()
            self.cloud = shade.OpenStackCloud(cloud_config=cloud_config)
        except Exception:  # pylint: disable=broad-except
            self.cloud = None
            self.ext_net = None
            self.__logger.exception("Cannot connect to Cloud")
        try:
            self.ext_net = functest_utils.get_external_network(self.cloud)
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception("Cannot get the external network")
        self.guid = str(uuid.uuid4())
        self.image = None
        self.network = None
        self.subnet = None
        self.router = None
        self.sshvm = None
        self.flavor = None
        self.sec = None
        self.fip = None
        self.keypair = None
        self.ssh = paramiko.SSHClient()
        (_, self.key_filename) = tempfile.mkstemp()

    def _publish_image(self):
        assert self.cloud
        meta = getattr(
            config.CONF, '{}_extra_properties'.format(self.case_name), None)
        self.image = self.cloud.create_image(
            '{}-img_{}'.format(self.case_name, self.guid),
            filename=getattr(
                config.CONF, '{}_image'.format(self.case_name),
                self.filename),
            meta=meta)
        self.__logger.debug("image: %s", self.image)

    def _create_network_resources(self):
        assert self.cloud
        assert self.ext_net
        provider = {}
        if hasattr(config.CONF, '{}_network_type'.format(self.case_name)):
            provider["network_type"] = getattr(
                config.CONF, '{}_network_type'.format(self.case_name))
        if hasattr(config.CONF, '{}_physical_network'.format(self.case_name)):
            provider["physical_network"] = getattr(
                config.CONF, '{}_physical_network'.format(self.case_name))
        if hasattr(config.CONF, '{}_segmentation_id'.format(self.case_name)):
            provider["segmentation_id"] = getattr(
                config.CONF, '{}_segmentation_id'.format(self.case_name))
        self.network = self.cloud.create_network(
            '{}-net_{}'.format(self.case_name, self.guid),
            provider=provider)
        self.__logger.debug("network: %s", self.network)

        self.subnet = self.cloud.create_subnet(
            self.network.id,
            subnet_name='{}-subnet_{}'.format(self.case_name, self.guid),
            cidr=getattr(
                config.CONF, '{}_private_subnet_cidr'.format(self.case_name),
                self.cidr),
            enable_dhcp=True,
            dns_nameservers=[env.get('NAMESERVER')])
        self.__logger.debug("subnet: %s", self.subnet)

        self.router = self.cloud.create_router(
            name='{}-router_{}'.format(self.case_name, self.guid),
            ext_gateway_net_id=self.ext_net.id)
        self.__logger.debug("router: %s", self.router)
        self.cloud.add_router_interface(self.router, subnet_id=self.subnet.id)

    def create_sg_rules(self):
        self.sec = self.cloud.create_security_group(
            '{}-sg_{}'.format(self.case_name, self.guid),
            'created by OPNFV Functest ({})'.format(self.case_name))
        self.cloud.create_security_group_rule(
            self.sec.id, port_range_min='22', port_range_max='22',
            protocol='tcp', direction='ingress')
        self.cloud.create_security_group_rule(
            self.sec.id, protocol='icmp', direction='ingress')

    def _boot_vm(self):
        self.flavor = self.cloud.create_flavor(
            '{}-flavor_{}'.format(self.case_name, self.guid),
            getattr(config.CONF, '{}_flavor_ram'.format(self.case_name),
                    self.flavor_ram),
            getattr(config.CONF, '{}_flavor_vcpus'.format(self.case_name),
                    self.flavor_vcpus),
            getattr(config.CONF, '{}_flavor_disk'.format(self.case_name),
                    self.flavor_disk))
        self.__logger.debug("flavor: %s", self.flavor)
        self.cloud.set_flavor_specs(
            self.flavor.id, getattr(config.CONF, 'flavor_extra_specs', {}))

        self.keypair = self.cloud.create_keypair(
            '{}-kp_{}'.format(self.case_name, self.guid))
        self.__logger.debug("keypair: %s", self.keypair)
        self.__logger.debug("private_key: %s", self.keypair.private_key)
        with open(self.key_filename, 'w') as private_key_file:
            private_key_file.write(self.keypair.private_key)

        self.sshvm = self.cloud.create_server(
            '{}-vm_{}'.format(self.case_name, self.guid),
            image=self.image.id, flavor=self.flavor.id,
            key_name=self.keypair.id,
            auto_ip=False, wait=True,
            network=self.network.id,
            security_groups=[self.sec.id])
        self.__logger.debug("vm: %s", self.sshvm)
        self.fip = self.cloud.create_floating_ip(
            network=self.ext_net.id, server=self.sshvm)
        self.__logger.debug("floating_ip: %s", self.fip)
        self.sshvm = self.cloud.wait_for_server(self.sshvm, auto_ip=False)

    def _connect(self):
        p_console = self.cloud.get_server_console(self.sshvm.id)
        self.__logger.debug("vm console: \n%s", p_console)
        self.ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        for loop in range(6):
            try:
                self.ssh.connect(
                    self.sshvm.public_v4,
                    username=getattr(
                        config.CONF,
                        '{}_image_user'.format(self.case_name), self.username),
                    key_filename=self.key_filename,
                    timeout=getattr(
                        config.CONF,
                        '{}_vm_ssh_connect_timeout'.format(self.case_name),
                        self.ssh_connect_timeout))
                break
            except Exception:  # pylint: disable=broad-except
                self.__logger.info(
                    "try %s: cannot connect to %s", loop + 1,
                    self.sshvm.public_v4)
                time.sleep(10)
        else:
            self.__logger.error("cannot connect to %s", self.sshvm.public_v4)
            return False
        return True

    def execute(self):
        (_, stdout, _) = self.ssh.exec_command('echo Hello World')
        self.__logger.info("output:\n%s", stdout.read())
        return stdout.channel.recv_exit_status()

    def run(self, **kwargs):
        status = testcase.TestCase.EX_RUN_ERROR
        try:
            assert self.cloud
            self.start_time = time.time()
            self.result = 0
            self._publish_image()
            self._create_network_resources()
            self.create_sg_rules()
            self._boot_vm()
            assert self._connect()
            if not self.execute():
                self.result = 100
                status = testcase.TestCase.EX_OK
        except Exception:  # pylint: disable=broad-except
            self.__logger.exception('Cannot run %s', self.case_name)
        finally:
            self.stop_time = time.time()
        return status

    def clean(self):
        try:
            assert self.cloud
            self.cloud.delete_server(self.sshvm, wait=True)
            self.cloud.delete_security_group(self.sec.id)
            self.cloud.delete_image(self.image)
            self.cloud.remove_router_interface(self.router, self.subnet.id)
            self.cloud.delete_router(self.router.id)
            self.cloud.delete_network(self.network.id)
            self.cloud.delete_flavor(self.flavor.id)
            self.cloud.delete_keypair(self.keypair.id)
            self.cloud.delete_floating_ip(self.fip.id)
            self.cloud.delete_image(self.image)
        except Exception:  # pylint: disable=broad-except
            pass
