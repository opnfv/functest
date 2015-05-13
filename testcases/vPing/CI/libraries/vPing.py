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
import neutronclient.client as neutronclient
#import novaclient.v1_1.client as novaclient
import cinderclient.v1.client as cinderclient
pp = pprint.PrettyPrinter(indent=4)

EXIT_CODE = -1
HOME = os.environ['HOME']+"/"
with open(HOME+'.functest/functest.yaml') as f:
    functest_yaml = yaml.safe_load(f)
f.close()

PING_TIMEOUT = functest_yaml.get("vping").get("ping_timeout")
NAME_VM_1 = functest_yaml.get("vping").get("vm_name_1")
NAME_VM_2 = functest_yaml.get("vping").get("vm_name_2")
GLANCE_IMAGE_NAME = functest_yaml.get("general").get("openstack").get("image_name")
NEUTRON_PRIVATE_NET_NAME = functest_yaml.get("general").get("openstack").get("neutron_private_net_name")
FLAVOR = functest_yaml.get("vping").get("vm_flavor")


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
    while get_status(nova,vm) != "ACTIVE":
        time.sleep(3)
        logger.debug("Status: %s" % vm.status)
    logger.debug("Status: %s" % vm.status)

def get_status(nova,vm):
    vm = nova.servers.get(vm.id)
    return vm.status


def main():
    creds = get_credentials("nova")
    nova = novaclient.Client(**creds)
    cinder = cinderclient.Client(**creds)

    """
    # print images and server resources
    # print nova_images
    print_title("images list")
    pMsg(nova.images.list())
    print_title("servers list")
    pMsg(nova.servers.list())
    """
    # Check if the given image is created
    images=nova.images.list()
    image_found = False
    for image in images:
        if image.name == GLANCE_IMAGE_NAME:
            logger.info("Glance image found '%s'" %image.name)
            image_found = True
    if not image_found:
        logger.error("ERROR: Glance image %s not found." % GLANCE_IMAGE_NAME)
        logger.info("Available images are: ")
        pMsg(nova.images.list())
        exit(-1)

    # Check if the given neutron network is created
    networks=nova.networks.list()
    network_found = False
    for net in networks:
        if net.human_id == NEUTRON_PRIVATE_NET_NAME:
            logger.info("Network found '%s'" %net.human_id)
            network_found = True
    if not network_found:
        logger.error("Neutron network %s not found." % NEUTRON_PRIVATE_NET_NAME)
        logger.info("Available networks are: ")
        pMsg(nova.networks.list())
        exit(-1)

    servers=nova.servers.list()
    for server in servers:
        if server.name == NAME_VM_1 or server.name == NAME_VM_2:
            logger.info("Instance %s found. Deleting..." %server.name)
            server.delete()



    # boot VM 1
    # basic boot
  # tune (e.g. flavor, images, network) to your specific openstack configuration here
    m = NAME_VM_1
    f = nova.flavors.find(name = FLAVOR)
    i = nova.images.find(name = GLANCE_IMAGE_NAME)
    n = nova.networks.find(label = NEUTRON_PRIVATE_NET_NAME)
    u = "#cloud-config\npassword: opnfv\nchpasswd: { expire: False }\nssh_pwauth: True"
    #k = "demo-key"

    # create VM
    logger.info("Creating instance '%s'..." %m)
    logger.debug("Configuration:\n name=%s \n flavor=%s \n image=%s \n network=%s \n userdata= \n%s" %(m,f,i,n,u))
    vm1 = nova.servers.create(
        name               = m,
        flavor             = f,
        image              = i,
        nics               = [{"net-id": n.id}],
        #key_name           = k,
        userdata           = u,
    )

    #pMsg(vm1)


    #wait until VM status is active
    waitVmActive(nova,vm1)

    #retrieve IP of first VM
    logger.debug("Fetching IP...")
    server = get_server(creds, m)
    #pMsg(server.networks)
    # theoretically there is only one IP address so we take the first element of the table
    # Dangerous! To be improved!
    test_ip = server.networks.get(NEUTRON_PRIVATE_NET_NAME)[0]
    logger.debug("Instance '%s' got %s" %(m,test_ip))
    test_cmd = '/tmp/vping.sh %s'%test_ip


    # boot VM 2
    # we will boot then execute a ping script with cloud-init
    # the long chain corresponds to the ping procedure converted with base 64
  # tune (e.g. flavor, images, network) to your specific openstack configuration here
    m = NAME_VM_2
    f = nova.flavors.find(name = FLAVOR)
    i = nova.images.find(name = GLANCE_IMAGE_NAME)
    n = nova.networks.find(label = NEUTRON_PRIVATE_NET_NAME)
    # use base 64 format because bad surprises with sh script with cloud-init but script is just pinging
    #k = "demo-key"
    #u = "#cloud-config\npassword: opnfv\nchpasswd: { expire: False }\nssh_pwauth: True\nwrite_files:\n-  encoding: b64\n   path: /tmp/vping.sh\n   permissions: '0777'\n   owner: root:root\n   content: IyEvYmluL2Jhc2gKCndoaWxlIHRydWU7IGRvCiBwaW5nIC1jIDEgJDEgMj4mMSA+L2Rldi9udWxsCiBSRVM9JD8KIGlmIFsgIlokUkVTIiA9ICJaMCIgXSA7IHRoZW4KICBlY2hvICJ2UGluZyBPSyIKICBzbGVlcCAxMAogIHN1ZG8gc2h1dGRvd24gLWggbm93CiAgYnJlYWsKIGVsc2UKICBlY2hvICJ2UGluZyBLTyIKIGZpCiBzbGVlcCAxCmRvbmUK\nruncmd:\n - [ sh, -c, %s]"%test_cmd
    u = "#!/bin/sh\n\nwhile true; do\n ping -c 1 %s 2>&1 >/dev/null\n RES=$?\n if [ \"Z$RES\" = \"Z0\" ] ; then\n  echo 'vPing OK'\n break\n else\n  echo 'vPing KO'\n fi\n sleep 1\ndone\n"%test_ip
    # create VM
    logger.info("Creating instance '%s'..." %m)
    logger.debug("Configuration:\n name=%s \n flavor=%s \n image=%s \n network=%s \n userdata= \n%s" %(m,f,i,n,u))
    vm2 = nova.servers.create(
        name               = m,
        flavor             = f,
        image              = i,
        nics               = [{"net-id": n.id}],
        #key_name           = k,
        userdata           = u,
        #security_groups    = s,
        #config_drive       = v.id
    )
    # The injected script will shutdown the VM2 when the ping works
    # The console-log method is more consistent but doesn't work yet

    waitVmActive(nova,vm2)
    """
    logger.info("Waiting for ping, timeout is %d sec..." % PING_TIMEOUT)
    sec = 0
    while True:
        status = get_status(nova, vm2)
        #print status
        if status == "SHUTOFF" :
            EXIT_CODE = 0
            logger.info("vPing SUCCESSFUL after %d sec" % sec)
            break
        if sec == PING_TIMEOUT:
            logger.info("Timeout. vPing UNSUCCESSFUL.")
            break
        time.sleep(1)
        sec+=1

    """
    # I leave this here until we fix the console-log output
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

    if EXIT_CODE = 0 :
        logger.info("vPing OK")
    else :
        logger.error("vPing FAILED")

    exit(EXIT_CODE)


if __name__ == '__main__':
    main()
