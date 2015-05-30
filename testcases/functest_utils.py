#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import re, json, os, urllib2, shutil, subprocess, sys


def check_credentials():
    """
    Check if the OpenStack credentials (openrc) are sourced
    """
    #TODO: there must be a short way to do this, doing if os.environ["something"] == "" throws an error
    try:
       os.environ['OS_AUTH_URL']
    except KeyError:
        return False
    try:
       os.environ['OS_USERNAME']
    except KeyError:
        return False
    try:
       os.environ['OS_PASSWORD']
    except KeyError:
        return False
    try:
       os.environ['OS_TENANT_NAME']
    except KeyError:
        return False
    try:
       os.environ['OS_REGION_NAME']
    except KeyError:
        return False
    return True


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
        "username": os.environ.get('OS_USERNAME', "admin"),                                # add your cloud username details
        password: os.environ.get("OS_PASSWORD", 'admin'),                                # add password
        "auth_url": os.environ.get("OS_AUTH_URL","http://192.168.20.71:5000/v2.0"),        # Auth URL
        tenant: os.environ.get("OS_TENANT_NAME", "admin"),
    })

    return creds



def get_instance_status(nova_client,instance):
    try:
        instance = nova_client.servers.get(instance.id)
        return instance.status
    except:
        return None


def get_instance_by_name(nova_client, instance_name):
    try:
        instance = nova_client.servers.find(name=instance_name)
        return instance
    except:
        return None



def create_neutron_net(neutron_client, name):
    json_body = {'network': {'name': name,
                    'admin_state_up': True}}
    try:
        network = neutron_client.create_network(body=json_body)
        network_dict = network['network']
        return network_dict['id']
    except:
        print "Error:", sys.exc_info()[0]
        return False

def delete_neutron_net(neutron_client, network_id):
    try:
        neutron_client.delete_network(network_id)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False

def create_neutron_subnet(neutron_client, name, cidr, net_id):
    json_body = {'subnets': [{'name': name, 'cidr': cidr,
                           'ip_version': 4, 'network_id': net_id}]}
    try:
        subnet = neutron_client.create_subnet(body=json_body)
        return subnet['subnets'][0]['id']
    except:
        print "Error:", sys.exc_info()[0]
        return False

def delete_neutron_subnet(neutron_client, subnet_id):
    try:
        neutron_client.delete_subnet(subnet_id)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False

def create_neutron_router(neutron_client, name):
    json_body = {'router': {'name': name, 'admin_state_up': True}}
    try:
        router = neutron_client.create_router(json_body)
        return router['router']['id']
    except:
        print "Error:", sys.exc_info()[0]
        return False

def delete_neutron_router(neutron_client, router_id):
    json_body = {'router': {'id': router_id}}
    try:
        neutron_client.delete_router(router=router_id)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False


def add_interface_router(neutron_client, router_id, subnet_id):
    json_body = {"subnet_id": subnet_id}
    try:
        neutron_client.add_interface_router(router=router_id, body=json_body)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False


def remove_interface_router(neutron_client, router_id, subnet_id):
    json_body = {"subnet_id": subnet_id}
    try:
        neutron_client.remove_interface_router(router=router_id, body=json_body)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False


def get_network_id(neutron_client, network_name):
    networks = neutron_client.list_networks()['networks']
    id  = ''
    for n in networks:
        if n['name'] == network_name:
            id = n['id']
            break
    return id

def check_neutron_net(neutron_client, net_name):
    for network in neutron_client.list_networks()['networks']:
        if network['name'] == net_name :
            for subnet in network['subnets']:
                return True
    return False



def check_internet_connectivity(url='http://www.google.com/'):
    """
    Check if there is access to the internet
    """
    try:
        urllib2.urlopen(url, timeout=5)
        return True
    except urllib.request.URLError:
        return False


def download_url(url, dest_path):
    """
    Download a file to a destination path given a URL
    """
    name = url.rsplit('/')[-1]
    dest = dest_path + name
    try:
        response = urllib2.urlopen(url)
    except (urllib2.HTTPError, urllib2.URLError):
        return False

    with open(dest, 'wb') as f:
        f.write(response.read())
    return True


def execute_command(cmd, logger=None):
    """
    Execute Linux command
    """
    if logger:
        logger.debug('Executing command : {}'.format(cmd))
    output_file = "output.txt"
    f = open(output_file, 'w+')
    p = subprocess.call(cmd,shell=True, stdout=f, stderr=subprocess.STDOUT)
    f.close()
    f = open(output_file, 'r')
    result = f.read()
    if result != "" and logger:
        logger.debug(result)
    if p == 0 :
        return True
    else:
        if loger:
            logger.error("Error when executing command %s" %cmd)
        exit(-1)
