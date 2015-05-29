#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import re, json, os, urllib2, argparse, logging, shutil, subprocess, yaml, sys
from git import Repo

from neutronclient.v2_0 import client


""" logging configuration """
logger = logging.getLogger('config_functest')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)



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


def get_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d

def get_nova_credentials():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d



def create_neutron_net(neutron_client, json_body):
    try:
        network = neutron_client.create_network(body=json_body)
        network_dict = network['network']
        return network_dict['id']
    except:
        print "Error:", sys.exc_info()[0]
        return False


def create_neutron_subnet(neutron_client, json_body):
    try:
        subnet = neutron_client.create_subnet(body=json_body)
        return subnet['subnets'][0]['id']
    except:
        print "Error:", sys.exc_info()[0]
        return False
    
    
def create_neutron_router(neutron_client, json_body):
    try:
        router = neutron_client.create_router(json_body)
        return router['router']['id']
    except:
        print "Error:", sys.exc_info()[0]
        return False


def create_neutron_router(neutron_client, json_body):
    try:
        subnet = neutron_client.create_subnet(body=json_body)
        return subnet['subnets'][0]['id']
    except:
        print "Error:", sys.exc_info()[0]
        return False


def get_network_id(neutron, network_name):
    networks = neutron.list_networks()['networks']
    id  = ''
    for n in networks:
        if n['name'] == network_name:
            id = n['id']
            break
    return id

def check_neutron_net(neutron, net_name):
    for network in neutron.list_networks()['networks']:
        if network['name'] == net_name :
            for subnet in network['subnets']:
                return True
    return False


def delete_neutron_net(neutron):
    #TODO: remove router, ports
    try:
        #https://github.com/isginf/openstack_tools/blob/master/openstack_remove_tenant.py
        for network in neutron.list_networks()['networks']:
            if network['name'] == NEUTRON_PRIVATE_NET_NAME :
                for subnet in network['subnets']:
                    print "Deleting subnet " + subnet
                    neutron.delete_subnet(subnet)
                print "Deleting network " + network['name']
                neutron.delete_neutron_net(network['id'])
    finally:
        return True
    return False
