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

import os
import pprint
import subprocess
import time
import novaclient.v1_1.client as novaclient
import cinderclient.v1.client as cinderclient
pp = pprint.PrettyPrinter(indent=4)

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
        password: os.environ.get("OS_PASSWORD", "test"),								# add password
        "auth_url": os.environ.get("OS_AUTH_URL","http://192.168.20.71:5000/v2.0"),		# Auth URL
        tenant: os.environ.get("OS_TENANT_NAME", "invisible_to_admin"),
    })

    return creds


def get_server(creds, servername):
    nova = novaclient.Client(**creds)
    return nova.servers.find(name=servername)


def waitVmActive(nova,vm):
    # sleep and wait for VM status change
    pMsg(vm.status)
    while vm.status == "BUILD":
        time.sleep(1)
        vm = nova.servers.get(vm.id)
        pMsg(vm.status)

def main():
    creds = get_credentials("nova")
    nova = novaclient.Client(**creds)
    cinder = cinderclient.Client(**creds)
    
    #print images and server resources
    print_title("images list")
    pMsg(nova.images.list())
    
    print_title("servers list")
    pMsg(nova.servers.list())
    

    # boot VM 1
    # basic boot
	# tune (e.g. flavor, images, network) to your specific openstack configuration here
    f = nova.flavors.find(name = 'm1.small')
    i = nova.images.find(name = 'Ubuntu 14.04 (amd64)')
    n = nova.networks.find(label = 'private')
    u = "#cloud-config\npassword: opnfv\nchpasswd: { expire: False }\nssh_pwauth: True"
    #k = "demo-key"

    # create VM
    vm1 = nova.servers.create(
        name               = "opnfv-vping-1",
        flavor             = f,
        image              = i,
        nics               = [{"net-id": n.id}],
        #key_name           = k,
        userdata           = u,
    )

    pMsg(vm1)


    #wait until VM status is active
    waitVmActive(nova,vm1)
    
    #retrieve IP of first VM
    server = get_server(creds, "opnfv-vping-1")
    pMsg(server.networks)
    # theoretically there is only one IP address so we take the first element of the table
    test_ip = server.networks.get('private')[0]
    test_cmd = '/tmp/vping.sh %s'%test_ip

   
    # boot VM 2 
    # we will boot then execute a ping script with cloud-init
    # the long chain corresponds to the ping procedure converted with base 64
	# tune (e.g. flavor, images, network) to your specific openstack configuration here
    f = nova.flavors.find(name = 'm1.small')
    i = nova.images.find(name = 'Ubuntu 14.04 (amd64)')
    n = nova.networks.find(label = 'private')
    # use base 64 format becaus bad surprises with sh script with cloud-init but script is just pinging
    u = "#cloud-config\npassword: opnfv\nchpasswd: { expire: False }\nssh_pwauth: True\nwrite_files:\n-  encoding: b64\n   path: /tmp/vping.sh\n   permissions: '0777'\n   owner: root:root\n   content: IyEvYmluL2Jhc2gKCgoKcGluZyAtYyAxICQxIDI+JjEgPi9kZXYvbnVsbApSRVM9JD8KaWYgWyAiWiRSRVMiID0gIlowIiBdIDsgdGhlbgogIGVjaG8gInZQaW5nIE9LIgplbHNlCiAgZWNobyAidlBpbmcgS08iCmZpCg==\nruncmd:\n - [ sh, -c, %s]"%test_cmd
    #k = "demo-key"
    
    # create VM
    vm2 = nova.servers.create(
        name               = "opnfv-vping-2", 
        flavor             = f,
        image              = i,
        nics               = [{"net-id": n.id}],
        #key_name           = k,
        userdata           = u,
        #security_groups    = s,
        #config_drive       = v.id
    )
    
    pMsg(vm2)
   
    waitVmActive(nova,vm2)
 
    console_log = vm2.get_console_output()
    

    while not ("vPing" in console_log):
        time.sleep(1)
        console_log = vm2.get_console_output()

        # report if the test is failed
        if "vPing" in console_log:
            pMsg("vPing is OK")
        else:
            pMsg("no vPing detected....")

    # delete both VMs
    nova.servers.delete(vm1)
    nova.servers.delete(vm2)
    pMsg ("VM instances have been terminated!")


if __name__ == '__main__':
    main()
