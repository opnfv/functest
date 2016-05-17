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
import argparse
import datetime
import os
import paramiko
import pprint
import re
import time
import yaml
from scp import SCPClient

from novaclient import client as novaclient
from neutronclient.v2_0 import client as neutronclient
from keystoneclient.v2_0 import client as keystoneclient
from glanceclient import client as glanceclient

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils
import functest.utils.openstack_utils as openstack_utils

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser()
image_exists = False

parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")

args = parser.parse_args()

""" logging configuration """
logger = ft_logger.Logger("vping_ssh").getLogger()

paramiko.util.log_to_file("/var/log/paramiko.log")

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
GLANCE_IMAGE_FILENAME = functest_yaml.get("general").get("openstack").get(
    "image_file_name")
GLANCE_IMAGE_FORMAT = functest_yaml.get("general").get("openstack").get(
    "image_disk_format")
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
ROUTER_NAME = functest_yaml.get("vping").get(
    "vping_router_name")

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
        status = openstack_utils.get_instance_status(nova, vm)
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
        status = openstack_utils.get_instance_status(nova, vm)
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
    sg_id = openstack_utils.get_security_group_id(neutron_client,
                                                  SECGROUP_NAME)
    if sg_id != '':
        logger.info("Using existing security group '%s'..." % SECGROUP_NAME)
    else:
        logger.info("Creating security group  '%s'..." % SECGROUP_NAME)
        SECGROUP = openstack_utils.create_security_group(neutron_client,
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
        if not openstack_utils.create_secgroup_rule(neutron_client, sg_id,
                                                    'ingress', 'icmp'):
            logger.error("Failed to create the security group rule...")
            return False

        logger.debug("Adding SSH rules in security group '%s'..."
                     % SECGROUP_NAME)
        if not openstack_utils.create_secgroup_rule(
                neutron_client, sg_id, 'ingress', 'tcp', '22', '22'):
            logger.error("Failed to create the security group rule...")
            return False

        if not openstack_utils.create_secgroup_rule(
                neutron_client, sg_id, 'egress', 'tcp', '22', '22'):
            logger.error("Failed to create the security group rule...")
            return False
    return sg_id


def push_results(start_time_ts, duration, test_status):
    try:
        logger.debug("Pushing result into DB...")
        scenario = functest_utils.get_scenario(logger)
        version = functest_utils.get_version(logger)
        criteria = "failed"
        if test_status == "OK":
            criteria = "passed"
        pod_name = functest_utils.get_pod_name(logger)
        build_tag = functest_utils.get_build_tag(logger)
        functest_utils.push_results_to_db(TEST_DB,
                                          "functest",
                                          "vPing",
                                          logger, pod_name, version, scenario,
                                          criteria, build_tag,
                                          payload={'timestart': start_time_ts,
                                                   'duration': duration,
                                                   'status': test_status})
    except:
        logger.error("Error pushing results into Database '%s'"
                     % sys.exc_info()[0])


def main():

    creds_nova = openstack_utils.get_credentials("nova")
    nova_client = novaclient.Client('2', **creds_nova)
    creds_neutron = openstack_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)
    creds_keystone = openstack_utils.get_credentials("keystone")
    keystone_client = keystoneclient.Client(**creds_keystone)
    glance_endpoint = keystone_client.service_catalog.url_for(
        service_type='image', endpoint_type='publicURL')
    glance_client = glanceclient.Client(1, glance_endpoint,
                                        token=keystone_client.auth_token)
    EXIT_CODE = -1

    image_id = None
    flavor = None

    # Check if the given image exists
    image_id = openstack_utils.get_image_id(glance_client, GLANCE_IMAGE_NAME)
    if image_id != '':
        logger.info("Using existing image '%s'..." % GLANCE_IMAGE_NAME)
        global image_exists
        image_exists = True
    else:
        logger.info("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME,
                                                          GLANCE_IMAGE_PATH))
        image_id = openstack_utils.create_glance_image(glance_client,
                                                       GLANCE_IMAGE_NAME,
                                                       GLANCE_IMAGE_PATH)
        if not image_id:
            logger.error("Failed to create a Glance image...")
            return(EXIT_CODE)
        logger.debug("Image '%s' with ID=%s created successfully."
                     % (GLANCE_IMAGE_NAME, image_id))

    network_dic = openstack_utils.create_network_full(logger,
                                                      neutron_client,
                                                      PRIVATE_NET_NAME,
                                                      PRIVATE_SUBNET_NAME,
                                                      ROUTER_NAME,
                                                      PRIVATE_SUBNET_CIDR)
    if not network_dic:
        logger.error(
            "There has been a problem when creating the neutron network")
        return(EXIT_CODE)

    network_id = network_dic["net_id"]

    sg_id = create_security_group(neutron_client)

    # Check if the given flavor exists
    try:
        flavor = nova_client.flavors.find(name=FLAVOR)
        logger.info("Using existing Flavor '%s'..." % FLAVOR)
    except:
        logger.error("Flavor '%s' not found." % FLAVOR)
        logger.info("Available flavors are: ")
        pMsg(nova_client.flavor.list())
        return(EXIT_CODE)

    # Deleting instances if they exist
    servers = nova_client.servers.list()
    for server in servers:
        if server.name == NAME_VM_1 or server.name == NAME_VM_2:
            logger.info("Instance %s found. Deleting..." % server.name)
            server.delete()

    # boot VM 1
    start_time_ts = time.time()
    end_time_ts = start_time_ts
    logger.info("vPing Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time_ts).strftime(
            '%Y-%m-%d %H:%M:%S')))

    logger.info("Creating instance '%s'..." % NAME_VM_1)
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n "
        "network=%s \n" % (NAME_VM_1, flavor, image_id, network_id))
    vm1 = nova_client.servers.create(
        name=NAME_VM_1,
        flavor=flavor,
        image=image_id,
        nics=[{"net-id": network_id}]
    )

    # wait until VM status is active
    if not waitVmActive(nova_client, vm1):
        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (
            NAME_VM_1, openstack_utils.get_instance_status(nova_client, vm1)))
        return (EXIT_CODE)
    else:
        logger.info("Instance '%s' is ACTIVE." % NAME_VM_1)

    # Retrieve IP of first VM
    test_ip = vm1.networks.get(PRIVATE_NET_NAME)[0]
    logger.debug("Instance '%s' got private ip '%s'." % (NAME_VM_1, test_ip))

    logger.info("Adding '%s' to security group '%s'..."
                % (NAME_VM_1, SECGROUP_NAME))
    openstack_utils.add_secgroup_to_instance(nova_client, vm1.id, sg_id)

    # boot VM 2
    logger.info("Creating instance '%s'..." % NAME_VM_2)
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n "
        "network=%s \n" % (NAME_VM_2, flavor, image_id, network_id))
    vm2 = nova_client.servers.create(
        name=NAME_VM_2,
        flavor=flavor,
        image=image_id,
        nics=[{"net-id": network_id}]
    )

    if not waitVmActive(nova_client, vm2):
        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (
            NAME_VM_2, openstack_utils.get_instance_status(nova_client, vm2)))
        return (EXIT_CODE)
    else:
        logger.info("Instance '%s' is ACTIVE." % NAME_VM_2)

    logger.info("Adding '%s' to security group '%s'..." % (NAME_VM_2,
                                                           SECGROUP_NAME))
    openstack_utils.add_secgroup_to_instance(nova_client, vm2.id, sg_id)

    logger.info("Creating floating IP for VM '%s'..." % NAME_VM_2)
    floatip_dic = openstack_utils.create_floating_ip(neutron_client)
    floatip = floatip_dic['fip_addr']
    # floatip_id = floatip_dic['fip_id']

    if floatip is None:
        logger.error("Cannot create floating IP.")
        return (EXIT_CODE)
    logger.info("Floating IP created: '%s'" % floatip)

    logger.info("Associating floating ip: '%s' to VM '%s' "
                % (floatip, NAME_VM_2))
    if not openstack_utils.add_floating_ip(nova_client, vm2.id, floatip):
        logger.error("Cannot associate floating IP to VM.")
        return (EXIT_CODE)

    logger.info("Trying to establish SSH connection to %s..." % floatip)
    username = 'cirros'
    password = 'cubswin:)'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    timeout = 50
    nolease = False
    got_ip = False
    discover_count = 0
    cidr_first_octet = PRIVATE_SUBNET_CIDR.split('.')[0]
    while timeout > 0:
        try:
            ssh.connect(floatip, username=username,
                        password=password, timeout=2)
            logger.debug("SSH connection established to %s." % floatip)
            break
        except:
            logger.debug("Waiting for %s..." % floatip)
            time.sleep(6)
            timeout -= 1

        console_log = vm2.get_console_output()

        # print each "Sending discover" captured on the console log
        if (len(re.findall("Sending discover", console_log)) >
                discover_count and not got_ip):
            discover_count += 1
            logger.debug("Console-log '%s': Sending discover..."
                         % NAME_VM_2)

        # check if eth0 got an ip,the line looks like this:
        # "inet addr:192.168."....
        # if the dhcp agent fails to assing ip, this line will not appear
        if "inet addr:" + cidr_first_octet in console_log and not got_ip:
            got_ip = True
            logger.debug("The instance '%s' succeeded to get the IP "
                         "from the dhcp agent.")

        # if dhcp doesnt work,it shows "No lease, failing".The test will fail
        if "No lease, failing" in console_log and not nolease and not got_ip:
                nolease = True
                logger.debug("Console-log '%s': No lease, failing..."
                             % NAME_VM_2)
                logger.info("The instance failed to get an IP from the "
                            "DHCP agent. The test will probably timeout...")

    if timeout == 0:  # 300 sec timeout (5 min)
        logger.error("Cannot establish connection to IP '%s'. Aborting"
                     % floatip)
        return (EXIT_CODE)

    scp = SCPClient(ssh.get_transport())

    ping_script = REPO_PATH + "testcases/vPing/ping.sh"
    try:
        scp.put(ping_script, "~/")
    except:
        logger.error("Cannot SCP the file '%s' to VM '%s'"
                     % (ping_script, floatip))

    cmd = 'chmod 755 ~/ping.sh'
    (stdin, stdout, stderr) = ssh.exec_command(cmd)
    for line in stdout.readlines():
        print line

    logger.info("Waiting for ping...")
    sec = 0
    duration = 0

    cmd = '~/ping.sh ' + test_ip
    flag = False
    while True:
        time.sleep(1)
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
        output = stdout.readlines()

        for line in output:
            if "vPing OK" in line:
                logger.info("vPing detected!")

                # we consider start time at VM1 booting
                end_time_ts = time.time()
                duration = round(end_time_ts - start_time_ts, 1)
                logger.info("vPing duration:'%s' s." % duration)
                EXIT_CODE = 0
                flag = True
                break
            elif sec == PING_TIMEOUT:
                logger.info("Timeout reached.")
                flag = True
                break
        if flag:
            break
        logger.debug("Pinging %s. Waiting for response..." % test_ip)
        sec += 1

    test_status = "NOK"
    if EXIT_CODE == 0:
        logger.info("vPing OK")
        test_status = "OK"
    else:
        duration = 0
        logger.error("vPing FAILED")

    if args.report:
        push_results(start_time_ts, duration, test_status)

    exit(EXIT_CODE)

if __name__ == '__main__':
    main()
