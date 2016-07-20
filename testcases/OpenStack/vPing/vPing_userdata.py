#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# 0.1: This script boots the VM1 and allocates IP address from Nova
# Later, the VM2 boots then execute cloud-init to ping VM1.
# After successful ping, both the VMs are deleted.
# 0.2: measure test duration and publish results under json format
# 0.3: adapt push 2 DB after Test API refacroting
#
#

import argparse
import datetime
import os
import pprint
import sys
import time
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils
import functest.utils.openstack_utils as os_utils
import yaml


pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser()
image_exists = False

parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")

args = parser.parse_args()

""" logging configuration """
logger = ft_logger.Logger("vping_userdata").getLogger()

REPO_PATH = os.environ['repos_dir'] + '/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)
f.close()

HOME = os.environ['HOME'] + "/"
# vPing parameters
VM_BOOT_TIMEOUT = 180
VM_DELETE_TIMEOUT = 100
PING_TIMEOUT = functest_yaml.get("vping").get("ping_timeout")
TEST_DB = functest_yaml.get("results").get("test_db_url")
NAME_VM_1 = functest_yaml.get("vping").get("vm_name_1")
NAME_VM_2 = functest_yaml.get("vping").get("vm_name_2")
GLANCE_IMAGE_NAME = functest_yaml.get("vping").get("image_name")
GLANCE_IMAGE_FILENAME = functest_yaml.get("general").get(
    "openstack").get("image_file_name")
GLANCE_IMAGE_FORMAT = functest_yaml.get("general").get(
    "openstack").get("image_disk_format")
GLANCE_IMAGE_PATH = functest_yaml.get("general").get("directories").get(
    "dir_functest_data") + "/" + GLANCE_IMAGE_FILENAME


FLAVOR = functest_yaml.get("vping").get("vm_flavor")

# NEUTRON Private Network parameters

PRIVATE_NET_NAME = functest_yaml.get("vping").get(
    "vping_private_net_name")
PRIVATE_SUBNET_NAME = functest_yaml.get("vping").get(
    "vping_private_subnet_name")
PRIVATE_SUBNET_CIDR = functest_yaml.get("vping").get(
    "vping_private_subnet_cidr")
ROUTER_NAME = functest_yaml.get("vping").get("vping_router_name")

SECGROUP_NAME = functest_yaml.get("vping").get("vping_sg_name")
SECGROUP_DESCR = functest_yaml.get("vping").get("vping_sg_descr")


def pMsg(value):
    """pretty printing"""
    pp.pprint(value)


def waitVmActive(nova, vm):

    # sleep and wait for VM status change
    sleep_time = 3
    count = VM_BOOT_TIMEOUT / sleep_time
    while True:
        status = os_utils.get_instance_status(nova, vm)
        logger.debug("Status: %s" % status)
        if status == "ACTIVE":
            return True
        if status == "ERROR" or status == "error":
            return False
        if count == 0:
            logger.debug("Booting a VM timed out...")
            return False
        count -= 1
        time.sleep(sleep_time)
    return False


def waitVmDeleted(nova, vm):

    # sleep and wait for VM status change
    sleep_time = 3
    count = VM_DELETE_TIMEOUT / sleep_time
    while True:
        status = os_utils.get_instance_status(nova, vm)
        if not status:
            return True
        elif count == 0:
            logger.debug("Timeout")
            return False
        else:
            # return False
            count -= 1
        time.sleep(sleep_time)
    return False


def create_security_group(neutron_client):
    sg_id = os_utils.get_security_group_id(neutron_client,
                                           SECGROUP_NAME)
    if sg_id != '':
        logger.info("Using existing security group '%s'..." % SECGROUP_NAME)
    else:
        logger.info("Creating security group  '%s'..." % SECGROUP_NAME)
        SECGROUP = os_utils.create_security_group(neutron_client,
                                                  SECGROUP_NAME,
                                                  SECGROUP_DESCR)
        if not SECGROUP:
            logger.error("Failed to create the security group...")
            return False

        sg_id = SECGROUP['id']

        logger.debug("Security group '%s' with ID=%s created successfully."
                     % (SECGROUP['name'], sg_id))

        logger.debug("Adding ICMP rules in security group '%s'..."
                     % SECGROUP_NAME)
        if not os_utils.create_secgroup_rule(neutron_client, sg_id,
                                             'ingress', 'icmp'):
            logger.error("Failed to create the security group rule...")
            return False

        logger.debug("Adding SSH rules in security group '%s'..."
                     % SECGROUP_NAME)
        if not os_utils.create_secgroup_rule(neutron_client, sg_id,
                                             'ingress', 'tcp',
                                             '22', '22'):
            logger.error("Failed to create the security group rule...")
            return False

        if not os_utils.create_secgroup_rule(neutron_client, sg_id,
                                             'egress', 'tcp',
                                             '22', '22'):
            logger.error("Failed to create the security group rule...")
            return False
    return sg_id


def main():

    nova_client = os_utils.get_nova_client()
    neutron_client = os_utils.get_neutron_client()
    glance_client = os_utils.get_glance_client()

    EXIT_CODE = -1

    image_id = None
    flavor = None

    # Check if the given image exists
    image_id = os_utils.get_image_id(glance_client, GLANCE_IMAGE_NAME)
    if image_id != '':
        logger.info("Using existing image '%s'..." % GLANCE_IMAGE_NAME)
        global image_exists
        image_exists = True
    else:
        logger.info("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME,
                                                          GLANCE_IMAGE_PATH))
        image_id = os_utils.create_glance_image(glance_client,
                                                GLANCE_IMAGE_NAME,
                                                GLANCE_IMAGE_PATH)
        if not image_id:
            logger.error("Failed to create a Glance image...")
            exit(EXIT_CODE)
        logger.debug("Image '%s' with ID=%s created successfully."
                     % (GLANCE_IMAGE_NAME, image_id))

    network_dic = os_utils.create_network_full(neutron_client,
                                               PRIVATE_NET_NAME,
                                               PRIVATE_SUBNET_NAME,
                                               ROUTER_NAME,
                                               PRIVATE_SUBNET_CIDR)
    if not network_dic:
        logger.error(
            "There has been a problem when creating the neutron network")
        exit(EXIT_CODE)
    network_id = network_dic["net_id"]

    create_security_group(neutron_client)

    # Check if the given flavor exists
    try:
        flavor = nova_client.flavors.find(name=FLAVOR)
        logger.info("Flavor found '%s'" % FLAVOR)
    except:
        logger.error("Flavor '%s' not found." % FLAVOR)
        logger.info("Available flavors are: ")
        pMsg(nova_client.flavor.list())
        exit(-1)

    # Deleting instances if they exist
    servers = nova_client.servers.list()
    for server in servers:
        if server.name == NAME_VM_1 or server.name == NAME_VM_2:
            logger.info("Instance %s found. Deleting..." % server.name)
            server.delete()

    # boot VM 1
    # basic boot
    # tune (e.g. flavor, images, network) to your specific
    # openstack configuration here
    # we consider start time at VM1 booting
    start_time = time.time()
    stop_time = start_time
    logger.info("vPing Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time).strftime(
            '%Y-%m-%d %H:%M:%S')))

    # create VM
    logger.info("Creating instance '%s'..." % NAME_VM_1)
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n "
        "network=%s \n" % (NAME_VM_1, flavor, image_id, network_id))
    vm1 = nova_client.servers.create(
        name=NAME_VM_1,
        flavor=flavor,
        image=image_id,
        config_drive=True,
        nics=[{"net-id": network_id}]
    )

    # wait until VM status is active
    if not waitVmActive(nova_client, vm1):

        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (
            NAME_VM_1, os_utils.get_instance_status(nova_client, vm1)))
        exit(EXIT_CODE)
    else:
        logger.info("Instance '%s' is ACTIVE." % NAME_VM_1)

    # Retrieve IP of first VM
    test_ip = vm1.networks.get(PRIVATE_NET_NAME)[0]
    logger.debug("Instance '%s' got %s" % (NAME_VM_1, test_ip))

    # boot VM 2
    # we will boot then execute a ping script with cloud-init
    # the long chain corresponds to the ping procedure converted with base 64
    # tune (e.g. flavor, images, network) to your specific openstack
    #  configuration here
    u = ("#!/bin/sh\n\nwhile true; do\n ping -c 1 %s 2>&1 >/dev/null\n "
         "RES=$?\n if [ \"Z$RES\" = \"Z0\" ] ; then\n  echo 'vPing OK'\n "
         "break\n else\n  echo 'vPing KO'\n fi\n sleep 1\ndone\n" % test_ip)

    # create VM
    logger.info("Creating instance '%s'..." % NAME_VM_2)
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n network=%s "
        "\n userdata= \n%s" % (
            NAME_VM_2, flavor, image_id, network_id, u))
    vm2 = nova_client.servers.create(
        name=NAME_VM_2,
        flavor=flavor,
        image=image_id,
        nics=[{"net-id": network_id}],
        config_drive=True,
        userdata=u
    )

    if not waitVmActive(nova_client, vm2):
        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (
            NAME_VM_2, os_utils.get_instance_status(nova_client, vm2)))
        exit(EXIT_CODE)
    else:
        logger.info("Instance '%s' is ACTIVE." % NAME_VM_2)

    logger.info("Waiting for ping...")
    sec = 0
    metadata_tries = 0
    console_log = vm2.get_console_output()
    duration = 0
    stop_time = time.time()

    while True:
        time.sleep(1)
        console_log = vm2.get_console_output()
        # print "--"+console_log
        # report if the test is failed
        if "vPing OK" in console_log:
            logger.info("vPing detected!")

            # we consider start time at VM1 booting
            stop_time = time.time()
            duration = round(stop_time - start_time, 1)
            logger.info("vPing duration:'%s'" % duration)
            EXIT_CODE = 0
            break
        elif ("failed to read iid from metadata" in console_log or
              metadata_tries > 5):
            EXIT_CODE = -2
            break
        elif sec == PING_TIMEOUT:
            logger.info("Timeout reached.")
            break
        elif sec % 10 == 0:
            if "request failed" in console_log:
                logger.debug("It seems userdata is not supported in "
                             "nova boot. Waiting a bit...")
                metadata_tries += 1
            else:
                logger.debug("Pinging %s. Waiting for response..." % test_ip)
        sec += 1

    test_status = "FAIL"
    if EXIT_CODE == 0:
        logger.info("vPing OK")
        test_status = "PASS"
    elif EXIT_CODE == -2:
        duration = 0
        logger.info("Userdata is not supported in nova boot. Aborting test...")
    else:
        duration = 0
        logger.error("vPing FAILED")

    if args.report:
        try:
            logger.debug("Pushing vPing userdata results into DB...")
            functest_utils.push_results_to_db("functest",
                                              "vping_userdata",
                                              logger,
                                              start_time,
                                              stop_time,
                                              test_status,
                                              details={'timestart': start_time,
                                                       'duration': duration,
                                                       'status': test_status})
        except:
            logger.error("Error pushing results into Database '%s'"
                         % sys.exc_info()[0])

    exit(EXIT_CODE)

if __name__ == '__main__':
    main()
