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
import json
import logging
import yaml
import datetime
import requests
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
GLANCE_IMAGE_NAME = functest_yaml.get("general"). \
    get("openstack").get("image_name")
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


def create_private_neutron_net(neutron):

    neutron.format = 'json'
    logger.info('Creating neutron network %s...' % NEUTRON_PRIVATE_NET_NAME)
    network_id = functest_utils. \
        create_neutron_net(neutron, NEUTRON_PRIVATE_NET_NAME)

    if not network_id:
        return False
    logger.debug("Network '%s' created successfully" % network_id)
    logger.debug('Creating Subnet....')
    subnet_id = functest_utils. \
        create_neutron_subnet(neutron,
                              NEUTRON_PRIVATE_SUBNET_NAME,
                              NEUTRON_PRIVATE_SUBNET_CIDR,
                              network_id)
    if not subnet_id:
        return False
    logger.debug("Subnet '%s' created successfully" % subnet_id)
    logger.debug('Creating Router...')
    router_id = functest_utils. \
        create_neutron_router(neutron, NEUTRON_ROUTER_NAME)

    if not router_id:
        return False

    logger.debug("Router '%s' created successfully" % router_id)
    logger.debug('Adding router to subnet...')

    result = functest_utils.add_interface_router(neutron, router_id, subnet_id)

    if not result:
        return False

    logger.debug("Interface added successfully.")
    network_dic = {'net_id': network_id,
                   'subnet_id': subnet_id,
                   'router_id': router_id}
    return network_dic


def cleanup(nova, neutron, network_dic):

    # delete both VMs
    logger.info("Cleaning up...")
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

    # delete created network
    logger.info("Deleting network '%s'..." % NEUTRON_PRIVATE_NET_NAME)
    net_id = network_dic["net_id"]
    subnet_id = network_dic["subnet_id"]
    router_id = network_dic["router_id"]

    if not functest_utils.remove_interface_router(neutron, router_id,
                                                  subnet_id):
        logger.error("Unable to remove subnet '%s' from router '%s'" % (
            subnet_id, router_id))
        return False

    logger.debug("Interface removed successfully")
    if not functest_utils.delete_neutron_router(neutron, router_id):
        logger.error("Unable to delete router '%s'" % router_id)
        return False

    logger.debug("Router deleted successfully")

    if not functest_utils.delete_neutron_subnet(neutron, subnet_id):
        logger.error("Unable to delete subnet '%s'" % subnet_id)
        return False

    logger.debug(
        "Subnet '%s' deleted successfully" % NEUTRON_PRIVATE_SUBNET_NAME)

    if not functest_utils.delete_neutron_net(neutron, net_id):
        logger.error("Unable to delete network '%s'" % net_id)
        return False

    logger.debug(
        "Network '%s' deleted successfully" % NEUTRON_PRIVATE_NET_NAME)
    return True


def push_results_to_db(payload):

    # TODO move DB creds into config file
    url = TEST_DB + "/results"
    params = {"project_name": "functest", "case_name": "vPing", "pod_id": 1,
              "details": payload}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(params), headers=headers)
    logger.debug(r)


def main():

    creds_nova = functest_utils.get_credentials("nova")
    nova_client = novaclient.Client(**creds_nova)
    creds_neutron = functest_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)
    EXIT_CODE = -1

    image = None
    flavor = None

    # Check if the given image exists
    try:
        image = nova_client.images.find(name=GLANCE_IMAGE_NAME)
        logger.info("Glance image found '%s'" % GLANCE_IMAGE_NAME)
    except:
        logger.error("ERROR: Glance image '%s' not found." % GLANCE_IMAGE_NAME)
        logger.info("Available images are: ")
        pMsg(nova_client.images.list())
        exit(-1)

    network_dic = create_private_neutron_net(neutron_client)

    if not network_dic:
        logger.error(
            "There has been a problem when creating the neutron network")
        exit(-1)

    network_id = network_dic["net_id"]

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
    start_time_ts = time.time()
    end_time_ts = start_time_ts
    logger.info("vPing Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time_ts).strftime(
            '%Y-%m-%d %H:%M:%S')))

    # create VM
    logger.debug("Creating port 'vping-port-1' with IP %s..." % IP_1)
    port_id = functest_utils.create_neutron_port(neutron_client,
                                                 "vping-port-1", network_id,
                                                 IP_1)
    if not port_id:
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
        nics=[{"port-id": port_id}]
    )

    # wait until VM status is active
    if not waitVmActive(nova_client, vm1):

        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (
            NAME_VM_1, functest_utils.get_instance_status(nova_client, vm1)))
        cleanup(nova_client, neutron_client, network_dic)
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
    port_id = functest_utils.create_neutron_port(neutron_client,
                                                 "vping-port-2", network_id,
                                                 IP_2)

    if not port_id:
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
        nics=[{"port-id": port_id}],
        userdata=u
    )

    if not waitVmActive(nova_client, vm2):
        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (
            NAME_VM_2, functest_utils.get_instance_status(nova_client, vm2)))
        cleanup(nova_client, neutron_client, network_dic)
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

    cleanup(nova_client, neutron_client, network_dic)

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
            push_results_to_db(
                {'timestart': start_time_ts, 'duration': duration,
                 'status': test_status})
            # with open("vPing-result.json", "w") as outfile:
            # json.dump({'timestart': start_time_ts, 'duration': duration,
            # 'status': test_status}, outfile, indent=4)
    except:
        logger.error("Error pushing results into Database")

    exit(EXIT_CODE)

if __name__ == '__main__':
    main()
