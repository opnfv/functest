#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# This script boots an instance and assigns a floating ip
#

import os
import sys

import argparse

import functest.utils.config_functest as config_functest
import functest.utils.functest_logger as ft_logger
import functest.utils.openstack_utils as os_utils

CONF = config_functest.CONF

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")

args = parser.parse_args()

""" logging configuration """
logger = ft_logger.Logger("create_instance_and_ip").getLogger()

HOME = os.environ['HOME'] + "/"

VM_BOOT_TIMEOUT = 180

IMAGE_PATH = CONF.functest_data_dir + "/" + CONF.os_image_file

# NEUTRON Private Network parameters


def main():

    nova_client = os_utils.get_nova_client()
    neutron_client = os_utils.get_neutron_client()
    glance_client = os_utils.get_glance_client()

    image_id = os_utils.create_glance_image(glance_client,
                                            CONF.example_image_name,
                                            IMAGE_PATH,
                                            disk=CONF.os_image_format,
                                            container="bare",
                                            public=True)

    network_dic = os_utils.create_network_full(neutron_client,
                                               CONF.example_private_net_name,
                                               CONF.example_private_subnet_name,
                                               CONF.example_router_name,
                                               CONF.example_private_subnet_cidr)
    if not network_dic:
        logger.error(
            "There has been a problem when creating the neutron network")
        sys.exit(-1)

    network_id = network_dic["net_id"]

    sg_id = os_utils.create_security_group_full(neutron_client,
                                                CONF.example_sg_name, CONF.example_sg_descr)

    # boot INTANCE
    logger.info("Creating instance '%s'..." % CONF.example_vm_name)
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n "
        "network=%s \n" % (CONF.example_vm_name, CONF.example_flavor, image_id, network_id))
    instance = os_utils.create_instance_and_wait_for_active(CONF.example_flavor,
                                                            image_id,
                                                            network_id,
                                                            CONF.example_vm_name)

    if instance is None:
        logger.error("Error while booting instance.")
        sys.exit(-1)
    # Retrieve IP of INSTANCE
    instance_ip = instance.networks.get(CONF.example_private_net_name)[0]
    logger.debug("Instance '%s' got private ip '%s'." %
                 (CONF.example_vm_name, instance_ip))

    logger.info("Adding '%s' to security group '%s'..."
                % (CONF.example_vm_name, CONF.example_sg_name))
    os_utils.add_secgroup_to_instance(nova_client, instance.id, sg_id)

    logger.info("Creating floating IP for VM '%s'..." % CONF.example_vm_name)
    floatip_dic = os_utils.create_floating_ip(neutron_client)
    floatip = floatip_dic['fip_addr']
    # floatip_id = floatip_dic['fip_id']

    if floatip is None:
        logger.error("Cannot create floating IP.")
        sys.exit(-1)
    logger.info("Floating IP created: '%s'" % floatip)

    logger.info("Associating floating ip: '%s' to VM '%s' "
                % (floatip, CONF.example_vm_name))
    if not os_utils.add_floating_ip(nova_client, instance.id, floatip):
        logger.error("Cannot associate floating IP to VM.")
        sys.exit(-1)

    sys.exit(0)

if __name__ == '__main__':
    main()
