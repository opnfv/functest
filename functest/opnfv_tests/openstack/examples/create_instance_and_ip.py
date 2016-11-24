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

import argparse
import sys
import functest.utils.functest_logger as ft_logger
import functest.utils.openstack_utils as os_utils
import functest.utils.functest_constants as ft_constants

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")

args = parser.parse_args()

""" logging configuration """
logger = ft_logger.Logger("create_instance_and_ip").getLogger()

HOME = ft_constants.HOME + "/"

VM_BOOT_TIMEOUT = 180

EXAMPLE_INSTANCE_NAME = ft_constants.EXAMPLE_INSTANCE_NAME
EXAMPLE_FLAVOR = ft_constants.EXAMPLE_FLAVOR
EXAMPLE_IMAGE_NAME = ft_constants.EXAMPLE_IMAGE_NAME
IMAGE_FILENAME = ft_constants.GLANCE_IMAGE_FILENAME
IMAGE_FORMAT = ft_constants.GLANCE_IMAGE_FORMAT
IMAGE_PATH = ft_constants.FUNCTEST_DATA_DIR + \
    "/" + IMAGE_FILENAME

# NEUTRON Private Network parameters

EXAMPLE_PRIVATE_NET_NAME = ft_constants.EXAMPLE_PRIVATE_NET_NAME
EXAMPLE_PRIVATE_SUBNET_NAME = ft_constants.EXAMPLE_PRIVATE_SUBNET_NAME
EXAMPLE_PRIVATE_SUBNET_CIDR = ft_constants.EXAMPLE_PRIVATE_SUBNET_CIDR
EXAMPLE_ROUTER_NAME = ft_constants.EXAMPLE_ROUTER_NAME

EXAMPLE_SECGROUP_NAME = ft_constants.EXAMPLE_SECGROUP_NAME
EXAMPLE_SECGROUP_DESCR = ft_constants.EXAMPLE_SECGROUP_DESCR


def main():

    nova_client = os_utils.get_nova_client()
    neutron_client = os_utils.get_neutron_client()
    glance_client = os_utils.get_glance_client()

    image_id = os_utils.create_glance_image(glance_client,
                                            EXAMPLE_IMAGE_NAME,
                                            IMAGE_PATH,
                                            disk=IMAGE_FORMAT,
                                            container="bare",
                                            public=True)

    network_dic = os_utils.create_network_full(neutron_client,
                                               EXAMPLE_PRIVATE_NET_NAME,
                                               EXAMPLE_PRIVATE_SUBNET_NAME,
                                               EXAMPLE_ROUTER_NAME,
                                               EXAMPLE_PRIVATE_SUBNET_CIDR)
    if not network_dic:
        logger.error(
            "There has been a problem when creating the neutron network")
        sys.exit(-1)

    network_id = network_dic["net_id"]

    sg_id = os_utils.create_security_group_full(neutron_client,
                                                EXAMPLE_SECGROUP_NAME,
                                                EXAMPLE_SECGROUP_DESCR)

    # boot INTANCE
    logger.info("Creating instance '%s'..." % EXAMPLE_INSTANCE_NAME)
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n "
        "network=%s \n"
        % (EXAMPLE_INSTANCE_NAME, EXAMPLE_FLAVOR, image_id, network_id))
    instance = \
        os_utils.create_instance_and_wait_for_active(EXAMPLE_FLAVOR,
                                                     image_id,
                                                     network_id,
                                                     EXAMPLE_INSTANCE_NAME)

    if instance is None:
        logger.error("Error while booting instance.")
        sys.exit(-1)
    # Retrieve IP of INSTANCE
    instance_ip = instance.networks.get(EXAMPLE_PRIVATE_NET_NAME)[0]
    logger.debug("Instance '%s' got private ip '%s'." %
                 (EXAMPLE_INSTANCE_NAME, instance_ip))

    logger.info("Adding '%s' to security group '%s'..."
                % (EXAMPLE_INSTANCE_NAME, EXAMPLE_SECGROUP_NAME))
    os_utils.add_secgroup_to_instance(nova_client, instance.id, sg_id)

    logger.info("Creating floating IP for VM '%s'..." % EXAMPLE_INSTANCE_NAME)
    floatip_dic = os_utils.create_floating_ip(neutron_client)
    floatip = floatip_dic['fip_addr']
    # floatip_id = floatip_dic['fip_id']

    if floatip is None:
        logger.error("Cannot create floating IP.")
        sys.exit(-1)
    logger.info("Floating IP created: '%s'" % floatip)

    logger.info("Associating floating ip: '%s' to VM '%s' "
                % (floatip, EXAMPLE_INSTANCE_NAME))
    if not os_utils.add_floating_ip(nova_client, instance.id, floatip):
        logger.error("Cannot associate floating IP to VM.")
        sys.exit(-1)

    sys.exit(0)


if __name__ == '__main__':
    main()
