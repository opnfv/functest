#!/usr/bin/env python
#
# Description:
#  Generates a list of the current Openstack objects in the deployment:
#       - Nova instances
#       - Glance images
#       - Cinder volumes
#       - Floating IPs
#       - Neutron networks, subnets and ports
#       - Routers
#       - Users and tenants
#
# Author:
#    jose.lausuch@ericsson.com
#
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import argparse
import logging
import os
import re
import sys
import time
import yaml

from novaclient import client as novaclient
from neutronclient.v2_0 import client as neutronclient
from keystoneclient.v2_0 import client as keystoneclient
from cinderclient import client as cinderclient

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
args = parser.parse_args()


""" logging configuration """
logger = logging.getLogger('clean_openstack')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

REPO_PATH=os.environ['repos_dir']+'/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)
sys.path.append(REPO_PATH + "testcases/")
import functest_utils

DEFAULTS_FILE = '/home/opnfv/functest/conf/os_defaults.yaml'


def separator():
    logger.info("-------------------------------------------")

def get_instances(nova_client):
    logger.debug("Getting instances...")
    dic_instances = {}
    instances = functest_utils.get_instances(nova_client)
    if not (instances is None or len(instances) == 0):
        for instance in instances:
            dic_instances.update({getattr(instance, 'id'):getattr(instance, 'name')})
    return {'instances': dic_instances}


def get_images(nova_client):
    logger.debug("Getting images...")
    dic_images = {}
    images = functest_utils.get_images(nova_client)
    if not (images is None or len(images) == 0):
        for image in images:
            dic_images.update({getattr(image, 'id'):getattr(image, 'name')})
    return {'images': dic_images}


def get_networks(neutron_client):
    logger.info("Getting networks")
    dic_networks = {}
    networks = functest_utils.get_network_list(neutron_client)
    if networks != None:
        for network in networks:
            dic_networks.update({network['id']:network['name']})
    return {'networks': dic_networks}

def get_routers(neutron_client):
    logger.info("Getting routers")
    dic_routers = {}
    routers = functest_utils.get_router_list(neutron_client)
    if routers != None:
        for router in routers:
            dic_routers.update({router['id']:router['name']})
    return {'routers': dic_routers}


def get_security_groups(neutron_client):
    logger.info("Getting Security groups...")
    dic_secgroups = {}
    secgroups = functest_utils.get_security_groups(neutron_client)
    if not (secgroups is None or len(secgroups) == 0):
        for secgroup in secgroups:
            dic_secgroups.update({secgroup['id']:secgroup['name']})
    return {'secgroups': dic_secgroups}


def get_users(keystone_client):
    logger.debug("Getting users...")
    dic_users = {}
    users = functest_utils.get_users(keystone_client)
    if not (users is None or len(users) == 0):
        for user in users:
            dic_users.update({getattr(user, 'id'):getattr(user, 'name')})
    return {'users': dic_users}


def get_tenants(keystone_client):
    logger.debug("Getting users...")
    dic_tenants = {}
    tenants = functest_utils.get_tenants(keystone_client)
    if not (tenants is None or len(tenants) == 0):
        for tenant in tenants:
            dic_tenants.update({getattr(tenant, 'id'):getattr(tenant, 'name')})
    return {'tenants': dic_tenants}


def main():
    creds_nova = functest_utils.get_credentials("nova")
    nova_client = novaclient.Client('2',**creds_nova)

    creds_neutron = functest_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)

    creds_keystone = functest_utils.get_credentials("keystone")
    keystone_client = keystoneclient.Client(**creds_keystone)

    creds_cinder = functest_utils.get_credentials("cinder")
    cinder_client = cinderclient.Client('1',creds_cinder['username'],
                                        creds_cinder['api_key'],
                                        creds_cinder['project_id'],
                                        creds_cinder['auth_url'],
                                        service_type="volume")

    if not functest_utils.check_credentials():
        logger.error("Please source the openrc credentials and run the script again.")
        exit(-1)

    defaults = {}
    defaults.update(get_instances(nova_client))
    defaults.update(get_images(nova_client))
    defaults.update(get_networks(neutron_client))
    defaults.update(get_routers(neutron_client))
    defaults.update(get_security_groups(neutron_client))
    defaults.update(get_users(keystone_client))
    defaults.update(get_tenants(keystone_client))

    with open(DEFAULTS_FILE, 'r+') as yaml_file:
        yaml_file.write(yaml.dump(defaults, default_flow_style=False))
        yaml_file.seek(0)
        print yaml_file.read()

    exit(0)


if __name__ == '__main__':
    main()
