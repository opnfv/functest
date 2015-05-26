#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# This script boots the VM1 and allocates IP address from Nova
# Later, the VM2 boots then execute cloud-init to ping VM1.
# After successful ping, both the VMs are deleted.
#
# Note: this is script works only with Ubuntu image, not with Cirros image
#

import os, time, subprocess, logging, argparse, yaml
import pprint
import novaclient.v2.client as novaclient
pp = pprint.PrettyPrinter(indent=4)


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
args = parser.parse_args()

""" logging configuration """
logger = logging.getLogger('vPing')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


HOME = os.environ['HOME']+"/"
with open(args.repo_path+"testcases/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

VM_BOOT_TIMEOUT = 180
PING_TIMEOUT = functest_yaml.get("vping").get("ping_timeout")
NAME_VM_1 = functest_yaml.get("vping").get("vm_name_1")
NAME_VM_2 = functest_yaml.get("vping").get("vm_name_2")
GLANCE_IMAGE_NAME = functest_yaml.get("general").get("openstack").get("image_name")
NEUTRON_PRIVATE_NET_NAME = functest_yaml.get("general").get("openstack").get("neutron_private_net_name")
FLAVOR = functest_yaml.get("vping").get("vm_flavor")


def pMsg(value):
    """pretty printing"""
    pp.pprint(value)

def print_title(title):
    """Print titles"""
    print "\n"+"#"*40+"\n# "+title+"\n"+"#"*40+"\n"

def get_credentials(service):
    """Returns a creds dictionary filled with the following keys:
    * username
    * password/api_key (depending on the service)
    * tenant_name/project_id (depending on the service)
    * auth_url
    :param service: a string indicating the name of the service
                    requesting the credentials.
    """
    #TODO: get credentials from the openrc file
    creds = {}
    # Unfortunately, each of the OpenStack client will request slightly
    # different entries in their credentials dict.
    if service.lower() in ("nova", "cinder"):
        password = "api_key"
        tenant = "project_id"
    else:
        password = "password"
        tenant = "tenant_name"

    # The most common way to pass these info to the script is to do it through
    # environment variables.
    creds.update({
        "username": os.environ.get('OS_USERNAME', "admin"),								# add your cloud username details
        password: os.environ.get("OS_PASSWORD", 'admin'),								# add password
        "auth_url": os.environ.get("OS_AUTH_URL","http://192.168.20.71:5000/v2.0"),		# Auth URL
        tenant: os.environ.get("OS_TENANT_NAME", "admin"),
    })

    return creds


def get_server(creds, servername):
    nova = novaclient.Client(**creds)
    return nova.servers.find(name=servername)


def waitVmActive(nova,vm):
    # sleep and wait for VM status change
    sleep_time = 3
    count = VM_BOOT_TIMEOUT / sleep_time
    while True:
        status = get_status(nova,vm)
        logger.debug("Status: %s" % status)
        if status == "ACTIVE":
            return True
        if status == "ERROR" or count == 0:
            return False
            count-=1
        time.sleep(sleep_time)
    return False

def get_status(nova,vm):
    vm = nova.servers.get(vm.id)
    return vm.status


def main():
    creds = get_credentials("nova")
    nova = novaclient.Client(**creds)
    EXIT_CODE = -1
    image = None
    network = None
    flavor = None

    # Check if the given image exists
    try:
        image = nova.images.find(name = GLANCE_IMAGE_NAME)
        logger.info("Glance image found '%s'" % GLANCE_IMAGE_NAME)
    except:
        logger.error("ERROR: Glance image '%s' not found." % GLANCE_IMAGE_NAME)
        logger.info("Available images are: ")
        pMsg(nova.images.list())
        exit(-1)

    # Check if the given neutron network exists
    try:
        network = nova.networks.find(label = NEUTRON_PRIVATE_NET_NAME)
        logger.info("Network found '%s'" % NEUTRON_PRIVATE_NET_NAME)
    except:
        logger.error("Neutron network '%s' not found." % NEUTRON_PRIVATE_NET_NAME)
        logger.info("Available networks are: ")
        pMsg(nova.networks.list())
        exit(-1)

    # Check if the given flavor exists
    try:
        flavor = nova.flavors.find(name = FLAVOR)
        logger.info("Flavor found '%s'" % FLAVOR)
    except:
        logger.error("Flavor '%s' not found." % FLAVOR)
        logger.info("Available flavors are: ")
        pMsg(nova.flavor.list())
        exit(-1)


    # Deleting instances if they exist
    servers=nova.servers.list()
    for server in servers:
        if server.name == NAME_VM_1 or server.name == NAME_VM_2:
            logger.info("Instance %s found. Deleting..." %server.name)
            server.delete()



    # boot VM 1
    # basic boot
    # tune (e.g. flavor, images, network) to your specific openstack configuration here

    # create VM
    logger.info("Creating instance '%s'..." % NAME_VM_1)
    logger.debug("Configuration:\n name=%s \n flavor=%s \n image=%s \n network=%s \n" %(NAME_VM_1,flavor,image,network))
    vm1 = nova.servers.create(
        name               = NAME_VM_1,
        flavor             = flavor,
        image              = image,
        nics               = [{"net-id": network.id}]
    )


    #wait until VM status is active
    if not waitVmActive(nova,vm1):
        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (NAME_VM_1,get_status(nova,vm1)))
        return (EXIT_CODE)
    else:
        logger.info("Instance '%s' is ACTIVE." % NAME_VM_1)

    #retrieve IP of first VM
    logger.debug("Fetching IP...")
    server = get_server(creds, NAME_VM_1)
    # theoretically there is only one IP address so we take the first element of the table
    # Dangerous! To be improved!
    test_ip = server.networks.get(NEUTRON_PRIVATE_NET_NAME)[0]
    logger.debug("Instance '%s' got %s" %(NAME_VM_1,test_ip))

    # boot VM 2
    # we will boot then execute a ping script with cloud-init
    # the long chain corresponds to the ping procedure converted with base 64
    # tune (e.g. flavor, images, network) to your specific openstack configuration here
    u = "#!/bin/sh\n\nwhile true; do\n ping -c 1 %s 2>&1 >/dev/null\n RES=$?\n if [ \"Z$RES\" = \"Z0\" ] ; then\n  echo 'vPing OK'\n break\n else\n  echo 'vPing KO'\n fi\n sleep 1\ndone\n"%test_ip

    # create VM
    logger.info("Creating instance '%s'..." % NAME_VM_2)
    logger.debug("Configuration:\n name=%s \n flavor=%s \n image=%s \n network=%s \n userdata= \n%s" %(NAME_VM_2,flavor,image,network,u))
    vm2 = nova.servers.create(
        name               = NAME_VM_2,
        flavor             = flavor,
        image              = image,
        nics               = [{"net-id": network.id}],
        userdata           = u,
    )

    if not waitVmActive(nova,vm2):
        logger.error("Instance '%s' cannot be booted. Status is '%s'" % (NAME_VM_2,get_status(nova,vm2)))
        return (EXIT_CODE)
    else:
        logger.info("Instance '%s' is ACTIVE." % NAME_VM_2)

    sec = 0
    console_log = vm2.get_console_output()
    while True:
        time.sleep(1)
        console_log = vm2.get_console_output()
        #print "--"+console_log
        # report if the test is failed
        if "vPing OK" in console_log:
            logger.info("vPing is OK")
            EXIT_CODE = 0
            break
        else:
            logger.info("No vPing detected...")
        sec+=1
        if sec == PING_TIMEOUT:
            logger.info("Timeout reached.")
            break


    # delete both VMs
    logger.debug("Deleting Instances...")
    nova.servers.delete(vm1)
    logger.debug("Instance %s terminated." % NAME_VM_1)
    nova.servers.delete(vm2)
    logger.debug("Instance %s terminated." % NAME_VM_2)

    if EXIT_CODE == 0:
        logger.info("vPing OK")
    else:
        logger.error("vPing FAILED")

    exit(EXIT_CODE)


if __name__ == '__main__':
    main()
