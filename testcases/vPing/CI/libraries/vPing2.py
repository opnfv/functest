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
import logging
import os
import paramiko
import pprint
import subprocess
import sys
import time
import yaml
from scp import SCPClient
from novaclient import client as novaclient
from neutronclient.v2_0 import client as neutronclient
from keystoneclient.v2_0 import client as keystoneclient
from glanceclient import client as glanceclient

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")

args = parser.parse_args()

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
paramiko.util.log_to_file("/var/log/paramiko.log")

REPO_PATH = os.environ['repos_dir']+'/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)
sys.path.append(REPO_PATH + "testcases/")
import functest_utils

with open("/home/opnfv/functest/conf/config_functest.yaml") as f:
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

NEUTRON_PRIVATE_NET_NAME = functest_yaml.get("vping"). \
    get("vping_private_net_name")

NEUTRON_PRIVATE_SUBNET_NAME = functest_yaml.get("vping"). \
    get("vping_private_subnet_name")

NEUTRON_PRIVATE_SUBNET_CIDR = functest_yaml.get("vping"). \
    get("vping_private_subnet_cidr")

NEUTRON_ROUTER_NAME = functest_yaml.get("vping"). \
    get("vping_router_name")


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

    if not functest_utils.add_interface_router(neutron, router_id, subnet_id):
        return False
    logger.debug("Interface added successfully.")

    logger.debug('Adding gateway to router...')
    if not functest_utils.add_gateway_router(neutron, router_id):
        return False
    logger.debug("Gateway added successfully.")

    network_dic = {'net_id': network_id,
                   'subnet_id': subnet_id,
                   'router_id': router_id}
    return network_dic


def cleanup(nova, neutron, image_id, network_dic, port_id1, port_id2):

    # delete both VMs
    logger.info("Cleaning up...")
    logger.debug("Deleting image...")
    if not functest_utils.delete_glance_image(nova, image_id):
        logger.error("Error deleting the glance image")

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

    if not functest_utils.delete_neutron_port(neutron, port_id1):
        logger.error("Unable to remove port '%s'" % port_id1)
        return False
    logger.debug("Port '%s' removed successfully" % port_id1)

    if not functest_utils.delete_neutron_port(neutron, port_id2):
        logger.error("Unable to remove port '%s'" % port_id2)
        return False
    logger.debug("Port '%s' removed successfully" % port_id2)

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

def push_results(start_time_ts, duration, test_status):
    try:
        logger.debug("Pushing result into DB...")
        scenario = functest_utils.get_scenario(logger)
        pod_name = functest_utils.get_pod_name(logger)
        functest_utils.push_results_to_db(TEST_DB,
                                          "vPing",
                                          logger, pod_name, scenario,
                                          payload={'timestart': start_time_ts,
                                                   'duration': duration,
                                                   'status': test_status})
    except:
        logger.error("Error pushing results into Database '%s'" % sys.exc_info()[0])


def main():

    creds_nova = functest_utils.get_credentials("nova")
    nova_client = novaclient.Client('2', **creds_nova)
    creds_neutron = functest_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)
    creds_keystone = functest_utils.get_credentials("keystone")
    keystone_client = keystoneclient.Client(**creds_keystone)
    glance_endpoint = keystone_client.service_catalog.url_for(service_type='image',
                                                              endpoint_type='publicURL')
    glance_client = glanceclient.Client(1, glance_endpoint,
                                        token=keystone_client.auth_token)
    EXIT_CODE = -1

    image = None
    flavor = None

    logger.debug("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME,
                                                       GLANCE_IMAGE_PATH))
    image_id = functest_utils.create_glance_image(glance_client,
                                                  GLANCE_IMAGE_NAME,
                                                  GLANCE_IMAGE_PATH)
    if not image_id:
        logger.error("Failed to create a Glance image...")
        return(EXIT_CODE)

    # Check if the given image exists
    image = functest_utils.get_image_id(glance_client, GLANCE_IMAGE_NAME)
    if image == '':
        logger.error("ERROR: Glance image '%s' not found." % GLANCE_IMAGE_NAME)
        logger.info("Available images are: ")
        pMsg(nova_client.images.list())
        return(EXIT_CODE)

    network_dic = create_private_neutron_net(neutron_client)

    if not network_dic:
        logger.error(
            "There has been a problem when creating the neutron network")
        return(EXIT_CODE)

    network_id = network_dic["net_id"]

    # Check if the given flavor exists

    try:
        flavor = nova_client.flavors.find(name=FLAVOR)
        logger.info("Flavor found '%s'" % FLAVOR)
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
        return(EXIT_CODE)

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
        cleanup(nova_client, neutron_client, image_id, network_dic, port_id1)
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


    # create VM
    logger.debug("Creating port 'vping-port-2' with IP %s..." % IP_2)
    port_id2 = functest_utils.create_neutron_port(neutron_client,
                                                  "vping-port-2", network_id,
                                                  IP_2)

    if not port_id2:
        logger.error("Unable to create port.")
        return(EXIT_CODE)

    logger.info("Creating instance '%s' with IP %s..." % (NAME_VM_2, IP_2))
    logger.debug(
        "Configuration:\n name=%s \n flavor=%s \n image=%s \n network=%s "
        "\n" % (NAME_VM_2, flavor, image, network_id))
    vm2 = nova_client.servers.create(
        name=NAME_VM_2,
        flavor=flavor,
        image=image,
        nics=[{"port-id": port_id2}]
    )

    if not waitVmActive(nova_client, vm2):
        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (
            NAME_VM_2, functest_utils.get_instance_status(nova_client, vm2)))
        cleanup(nova_client, neutron_client, image_id, network_dic,
                port_id1, port_id2)
        return (EXIT_CODE)
    else:
        logger.info("Instance '%s' is ACTIVE." % NAME_VM_2)

    logger.info("Creating floating IP for the second VM...")
    floatip = functest_utils.create_floating_ip(neutron_client)
    if floatip == None:
        logger.error("Cannot create floating IP.")
        cleanup(nova_client, neutron_client, image_id, network_dic,
            port_id1, port_id2)
        return (EXIT_CODE)
    logger.info("Floating IP created: '%s'" % floatip)

    logger.info("Associating floating ip: '%s' to VM2 " % floatip)
    if not functest_utils.add_floating_ip(nova_client, vm2.id, floatip):
        logger.error("Cannot associate floating IP to VM.")
        cleanup(nova_client, neutron_client, image_id, network_dic,
            port_id1, port_id2)
        return (EXIT_CODE)

    logger.info("Trying to establish SSH connection to %s..." % floatip)
    username='cirros'
    password='cubswin:)'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    timeout = 50
    while timeout > 0:
        try:
            ssh.connect(floatip, username=username, password=password, timeout=2)
            logger.debug("SSH connection established to %s." % floatip)
            break
        except Exception, e:
            #print e
            logger.debug("Waiting for %s..." % floatip)
            time.sleep(6)
            timeout -= 1

    if timeout == 0: # 300 sec timeout (5 min)
        logger.error("Cannot establish connection to IP '%s'. Aborting" % floatip)
        cleanup(nova_client, neutron_client, image_id, network_dic,
            port_id1, port_id2)
        return (EXIT_CODE)

    scp = SCPClient(ssh.get_transport())

    ping_script = REPO_PATH + "testcases/vPing/CI/libraries/ping.sh"
    try:
        scp.put(ping_script,"~/")
    except Exception, e:
        logger.error("Cannot SCP the file '%s' to VM '%s'" % (ping_script,floatip))


    #SSH_OPTS="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "+\
    #    "-o LogLevel=quiet"

    #cmd1 = "sshpass -p 'cubswin:)' scp " + SSH_OPTS + " " + \
    #    ping_script + " cirros@"+floatip+":~/ping.sh"
    #cmd2 = "sshpass -p 'cubswin:)' ssh " + SSH_OPTS + \
    #    " cirros@"+floatip+" 'chmod 755 ~/ping.sh '"
    #cmd3 = "sshpass -p 'cubswin:)' ssh " + SSH_OPTS + \
    #    " cirros@"+floatip+" '~/ping.sh "+IP_1+"'"

    cmd = 'chmod 755 ~/ping.sh'
    (stdin, stdout, stderr) = ssh.exec_command(cmd)
    for line in stdout.readlines():
        print line

    logger.info("Waiting for ping...")
    sec = 0
    duration = 0

    cmd = '~/ping.sh ' + IP_1
    flag = False
    while True:
        time.sleep(1)
        # we do the SCP every time in the loop because while testing, I observed
        # that for some strange reason, the cirros VM was deleting the file if
        # do the scp only once
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
        output = stdout.readlines()
        #for line in output:
        #    print line

        # print "--"+console_log
        # report if the test is failed
        for line in output:
            if "vPing OK" in line:
                logger.info("vPing detected!")

                # we consider start time at VM1 booting
                end_time_ts = time.time()
                duration = round(end_time_ts - start_time_ts, 1)
                logger.info("vPing duration:'%s'" % duration)
                EXIT_CODE = 0
                flag = True
                break
            elif sec == PING_TIMEOUT:
                logger.info("Timeout reached.")
                flag = True
                break
        if flag :
            break
        logger.debug("Pinging %s. Waiting for response..." % IP_1)
        sec += 1


    test_status = "NOK"
    if EXIT_CODE == 0:
        logger.info("vPing OK")
        test_status = "OK"
    else:
        duration = 0
        logger.error("vPing FAILED")

    cleanup(nova_client, neutron_client, image_id, network_dic,
            port_id1, port_id2)

    if args.report:
        push_results(start_time_ts, duration, test_status)

    exit(EXIT_CODE)

if __name__ == '__main__':
    main()
