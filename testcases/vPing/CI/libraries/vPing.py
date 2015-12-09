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
#
#

import os
import time
import argparse
import pprint
import sys
import logging
import yaml
import datetime
import novaclient.v2.client as novaclient
from neutronclient.v2_0 import client as neutronclient

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser()

parser.add_argument("repo_path", help="Path to the repository")
parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")

args = parser.parse_args()

sys.path.append(args.repo_path + "testcases/")

import functest_utils

""" logging configuration """

logger = logging.getLogger('vPing')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()

if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s'
                              '- %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)

HOME = os.environ['HOME'] + "/"

with open(args.repo_path + "testcases/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

# vPing parameters
VM_BOOT_TIMEOUT = 180
VM_DELETE_TIMEOUT = 100
PING_TIMEOUT = functest_yaml.get("vping").get("ping_timeout")
TEST_DB = functest_yaml.get("results").get("test_db_url")
NAME_VM_1 = functest_yaml.get("vping").get("vm_name_1")
NAME_VM_2 = functest_yaml.get("vping").get("vm_name_2")
IP_1 = functest_yaml.get("vping").get("ip_1")
IP_2 = functest_yaml.get("vping").get("ip_2")
# GLANCE_IMAGE_NAME = functest_yaml.get("general"). \
#    get("openstack").get("image_name")
GLANCE_IMAGE_NAME = "functest-vping"
GLANCE_IMAGE_FILENAME = functest_yaml.get("general"). \
    get("openstack").get("image_file_name")
GLANCE_IMAGE_FORMAT = functest_yaml.get("general"). \
    get("openstack").get("image_disk_format")
GLANCE_IMAGE_PATH = functest_yaml.get("general"). \
    get("directories").get("dir_functest_data") + "/" + GLANCE_IMAGE_FILENAME


FLAVOR = functest_yaml.get("vping").get("vm_flavor")

# NEUTRON Private Network parameters

NEUTRON_PRIVATE_NET_NAME = functest_yaml.get("general"). \
    get("openstack").get("neutron_private_net_name")

NEUTRON_PRIVATE_SUBNET_NAME = functest_yaml.get("general"). \
    get("openstack").get("neutron_private_subnet_name")

NEUTRON_PRIVATE_SUBNET_CIDR = functest_yaml.get("general"). \
    get("openstack").get("neutron_private_subnet_cidr")

NEUTRON_ROUTER_NAME = functest_yaml.get("general"). \
    get("openstack").get("neutron_router_name")


def pMsg(value):

    """pretty printing"""
    pp.pprint(value)


def waitVmActive(nova, vm):

    # sleep and wait for VM status change
    sleep_time = 3
    count = VM_BOOT_TIMEOUT / sleep_time
    while True:
        status = functest_utils.get_instance_status(nova, vm)
        logger.debug("Status: %s" % status)
        if status == "ACTIVE":
            return True
        if status == "ERROR" or count == 0:
            return False
            count -= 1
        time.sleep(sleep_time)
    return False


def waitVmDeleted(nova, vm):

    # sleep and wait for VM status change
    sleep_time = 3
    count = VM_DELETE_TIMEOUT / sleep_time
    while True:
        status = functest_utils.get_instance_status(nova, vm)
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


def create_glance_image(path, name, disk_format):
    """
    Create a glance image given the absolute path of the image, its name and the disk format
    """
    cmd = ("glance image-create --name "+name+"  --visibility public "
           "--disk-format "+disk_format+" --container-format bare --file "+path)
    functest_utils.execute_command(cmd, logger)
    return True


def delete_glance_image(name):
    cmd = ("glance image-delete $(glance image-list | grep %s "
           "| awk '{print $2}' | head -1)" % name)
    functest_utils.execute_command(cmd, logger)
    return True


def cleanup(nova, neutron, port_id1, port_id2):

    # delete both VMs
    logger.info("Cleaning up...")
    logger.debug("Deleting image...")
    delete_glance_image(GLANCE_IMAGE_NAME)

    vm1 = functest_utils.get_instance_by_name(nova, NAME_VM_1)
    if vm1:
        logger.debug("Deleting '%s'..." % NAME_VM_1)
        nova.servers.delete(vm1)
        # wait until VMs are deleted
        if not waitVmDeleted(nova, vm1):
            logger.error(
                "Instance '%s' with cannot be deleted. Status is '%s'" % (
                    NAME_VM_1, functest_utils.get_instance_status(nova, vm1)))
        else:
            logger.debug("Instance %s terminated." % NAME_VM_1)

    vm2 = functest_utils.get_instance_by_name(nova, NAME_VM_2)

    if vm2:
        logger.debug("Deleting '%s'..." % NAME_VM_2)
        vm2 = nova.servers.find(name=NAME_VM_2)
        nova.servers.delete(vm2)

        if not waitVmDeleted(nova, vm2):
            logger.error(
                "Instance '%s' with cannot be deleted. Status is '%s'" % (
                    NAME_VM_2, functest_utils.get_instance_status(nova, vm2)))
        else:
            logger.debug("Instance %s terminated." % NAME_VM_2)

    # delete created ports
    logger.info("Deleting neutron ports...")
    if not functest_utils.delete_neutron_port(neutron, port_id1):
        logger.error("Unable to remove port '%s'" % port_id1)
        return False
    logger.debug("Port '%s' removed successfully" % port_id1)

    if not functest_utils.delete_neutron_port(neutron, port_id2):
        logger.error("Unable to remove port '%s'" % port_id2)
        return False
    logger.debug("Port '%s' removed successfully" % port_id2)

    return True


def main():

    creds_nova = functest_utils.get_credentials("nova")
    nova_client = novaclient.Client(**creds_nova)
    creds_neutron = functest_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)
    EXIT_CODE = -1

    image = None
    flavor = None

    logger.debug("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME, GLANCE_IMAGE_PATH))
    create_glance_image(GLANCE_IMAGE_PATH, GLANCE_IMAGE_NAME, GLANCE_IMAGE_FORMAT)

    # Check if the given image exists
    try:
        image = nova_client.images.find(name=GLANCE_IMAGE_NAME)
        logger.info("Glance image found '%s'" % GLANCE_IMAGE_NAME)
    except:
        logger.error("ERROR: Glance image '%s' not found." % GLANCE_IMAGE_NAME)
        logger.info("Available images are: ")
        pMsg(nova_client.images.list())
        exit(-1)

    # Check if the given flavor exists
    try:
        flavor = nova_client.flavors.find(name=FLAVOR)
        logger.info("Flavor found '%s'" % FLAVOR)
    except:
        logger.error("Flavor '%s' not found." % FLAVOR)
        logger.info("Available flavors are: ")
        pMsg(nova_client.flavor.list())
        exit(-1)

    # Get private network to create the VMs on
    private_net = functest_utils.get_private_net(neutron_client)
    if private_net is None:
        logger.error("Error while getting the private network.")
        exit(-1)

    network_id = private_net['id']
    logger.debug("Using private network '%s' with id='%s'..." %(private_net['name'],network_id))
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
    start_time_ts = time.time()
    end_time_ts = start_time_ts
    logger.info("vPing Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time_ts).strftime(
            '%Y-%m-%d %H:%M:%S')))



    # create VM
    logger.debug("Creating port 'vping-port-1' with IP %s..." % IP_1)
    port_id1 = functest_utils.create_neutron_port(neutron_client,
                                                  "vping-port-1", network_id,
                                                  IP_1)
    if not port_id1:
        logger.error("Unable to create port.")
        exit(-1)

    logger.info("Creating instance '%s' with IP %s..." % (NAME_VM_1, IP_1))
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n "
        "network=%s \n" % (NAME_VM_1, flavor, image, network_id))
    vm1 = nova_client.servers.create(
        name=NAME_VM_1,
        flavor=flavor,
        image=image,
        # nics = [{"net-id": network_id, "v4-fixed-ip": IP_1}]
        nics=[{"port-id": port_id1}]
    )

    # wait until VM status is active
    if not waitVmActive(nova_client, vm1):

        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (
            NAME_VM_1, functest_utils.get_instance_status(nova_client, vm1)))
        cleanup(nova_client, neutron_client)
        return (EXIT_CODE)
    else:
        logger.info("Instance '%s' is ACTIVE." % NAME_VM_1)

    # Retrieve IP of first VM
    # logger.debug("Fetching IP...")
    # server = functest_utils.get_instance_by_name(nova_client, NAME_VM_1)
    # theoretically there is only one IP address so we take the
    # first element of the table
    # Dangerous! To be improved!
    # test_ip = server.networks.get(NEUTRON_PRIVATE_NET_NAME)[0]
    test_ip = IP_1
    logger.debug("Instance '%s' got %s" % (NAME_VM_1, test_ip))

    # boot VM 2
    # we will boot then execute a ping script with cloud-init
    # the long chain corresponds to the ping procedure converted with base 64
    # tune (e.g. flavor, images, network) to your specific openstack
    #  configuration here
    u = "#!/bin/sh\n\nwhile true; do\n ping -c 1 %s 2>&1 >/dev/null\n " \
        "RES=$?\n if [ \"Z$RES\" = \"Z0\" ] ; then\n  echo 'vPing OK'\n " \
        "break\n else\n  echo 'vPing KO'\n fi\n sleep 1\ndone\n" % test_ip

    # create VM
    logger.debug("Creating port 'vping-port-2' with IP %s..." % IP_2)
    port_id2 = functest_utils.create_neutron_port(neutron_client,
                                                  "vping-port-2", network_id,
                                                  IP_2)

    if not port_id2:
        logger.error("Unable to create port.")
        exit(-1)
    logger.info("Creating instance '%s' with IP %s..." % (NAME_VM_2, IP_2))
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n network=%s "
        "\n userdata= \n%s" % (
            NAME_VM_2, flavor, image, network_id, u))
    vm2 = nova_client.servers.create(
        name=NAME_VM_2,
        flavor=flavor,
        image=image,
        # nics = [{"net-id": network_id, "v4-fixed-ip": IP_2}],
        nics=[{"port-id": port_id2}],
        userdata=u
    )

    if not waitVmActive(nova_client, vm2):
        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (
            NAME_VM_2, functest_utils.get_instance_status(nova_client, vm2)))
        cleanup(nova_client, neutron_client)
        return (EXIT_CODE)
    else:
        logger.info("Instance '%s' is ACTIVE." % NAME_VM_2)

    logger.info("Waiting for ping...")
    sec = 0
    console_log = vm2.get_console_output()

    while True:
        time.sleep(1)
        console_log = vm2.get_console_output()
        # print "--"+console_log
        # report if the test is failed
        if "vPing OK" in console_log:
            logger.info("vPing detected!")

            # we consider start time at VM1 booting
            end_time_ts = time.time()
            duration = round(end_time_ts - start_time_ts, 1)
            logger.info("vPing duration:'%s'" % duration)
            EXIT_CODE = 0
            break
        elif sec == PING_TIMEOUT:
            logger.info("Timeout reached.")
            break
        else:
            logger.debug("No vPing detected...")
        sec += 1

    cleanup(nova_client, neutron_client, port_id1, port_id2)

    test_status = "NOK"
    if EXIT_CODE == 0:
        logger.info("vPing OK")
        test_status = "OK"
    else:
        logger.error("vPing FAILED")

    try:
        if args.report:
            logger.debug("Push result into DB")
            # TODO check path result for the file
            git_version = functest_utils.get_git_branch(args.repo_path)
            pod_name = functest_utils.get_pod_name(logger)
            functest_utils.push_results_to_db(TEST_DB,
                                              "vPing",
                                              logger, pod_name, git_version,
                                              payload={'timestart': start_time_ts,
                                                       'duration': duration,
                                                       'status': test_status})
            # with open("vPing-result.json", "w") as outfile:
            # json.dump({'timestart': start_time_ts, 'duration': duration,
            # 'status': test_status}, outfile, indent=4)
    except:
        logger.error("Error pushing results into Database")

    exit(EXIT_CODE)

if __name__ == '__main__':
    main()
