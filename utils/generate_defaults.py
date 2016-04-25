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

import os
import yaml

from novaclient import client as novaclient
from neutronclient.v2_0 import client as neutronclient
from keystoneclient.v2_0 import client as keystoneclient
from cinderclient import client as cinderclient

import functest.utils.openstack_utils as openstack_utils
import functest.utils.functest_logger as ft_logger

""" logging configuration """
logger = ft_logger.Logger("generate_defaults").getLogger()

REPO_PATH = os.environ['repos_dir'] + '/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)


DEFAULTS_FILE = '/home/opnfv/functest/conf/os_defaults.yaml'


def separator():
    logger.info("-------------------------------------------")


def get_instances(nova_client):
    logger.debug("Getting instances...")
    dic_instances = {}
    instances = openstack_utils.get_instances(nova_client)
    if not (instances is None or len(instances) == 0):
        for instance in instances:
            dic_instances.update({getattr(instance, 'id'): getattr(instance,
                                                                   'name')})
    return {'instances': dic_instances}


def get_images(nova_client):
    logger.debug("Getting images...")
    dic_images = {}
    images = openstack_utils.get_images(nova_client)
    if not (images is None or len(images) == 0):
        for image in images:
            dic_images.update({getattr(image, 'id'): getattr(image, 'name')})
    return {'images': dic_images}


def get_volumes(cinder_client):
    logger.debug("Getting volumes...")
    dic_volumes = {}
    volumes = openstack_utils.get_volumes(cinder_client)
    if volumes is not None:
        for volume in volumes:
            dic_volumes.update({volume.id: volume.display_name})
    return {'volumes': dic_volumes}


def get_networks(neutron_client):
    logger.debug("Getting networks")
    dic_networks = {}
    networks = openstack_utils.get_network_list(neutron_client)
    if networks is not None:
        for network in networks:
            dic_networks.update({network['id']: network['name']})
    return {'networks': dic_networks}


def get_routers(neutron_client):
    logger.debug("Getting routers")
    dic_routers = {}
    routers = openstack_utils.get_router_list(neutron_client)
    if routers is not None:
        for router in routers:
            dic_routers.update({router['id']: router['name']})
    return {'routers': dic_routers}


def get_security_groups(neutron_client):
    logger.debug("Getting Security groups...")
    dic_secgroups = {}
    secgroups = openstack_utils.get_security_groups(neutron_client)
    if not (secgroups is None or len(secgroups) == 0):
        for secgroup in secgroups:
            dic_secgroups.update({secgroup['id']: secgroup['name']})
    return {'secgroups': dic_secgroups}


def get_floatinips(nova_client):
    logger.debug("Getting Floating IPs...")
    dic_floatingips = {}
    floatingips = openstack_utils.get_floating_ips(nova_client)
    if not (floatingips is None or len(floatingips) == 0):
        for floatingip in floatingips:
            dic_floatingips.update({floatingip.id: floatingip.ip})
    return {'floatingips': dic_floatingips}


def get_users(keystone_client):
    logger.debug("Getting users...")
    dic_users = {}
    users = openstack_utils.get_users(keystone_client)
    if not (users is None or len(users) == 0):
        for user in users:
            dic_users.update({getattr(user, 'id'): getattr(user, 'name')})
    return {'users': dic_users}


def get_tenants(keystone_client):
    logger.debug("Getting users...")
    dic_tenants = {}
    tenants = openstack_utils.get_tenants(keystone_client)
    if not (tenants is None or len(tenants) == 0):
        for tenant in tenants:
            dic_tenants.update({getattr(tenant, 'id'):
                                getattr(tenant, 'name')})
    return {'tenants': dic_tenants}


def main():
    creds_nova = openstack_utils.get_credentials("nova")
    nova_client = novaclient.Client('2', **creds_nova)

    creds_neutron = openstack_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)

    creds_keystone = openstack_utils.get_credentials("keystone")
    keystone_client = keystoneclient.Client(**creds_keystone)

    creds_cinder = openstack_utils.get_credentials("cinder")
    cinder_client = cinderclient.Client('1', creds_cinder['username'],
                                        creds_cinder['api_key'],
                                        creds_cinder['project_id'],
                                        creds_cinder['auth_url'],
                                        service_type="volume")

    if not openstack_utils.check_credentials():
        logger.error("Please source the openrc credentials and run the" +
                     "script again.")
        exit(-1)

    defaults = {}
    defaults.update(get_instances(nova_client))
    defaults.update(get_images(nova_client))
    defaults.update(get_volumes(cinder_client))
    defaults.update(get_networks(neutron_client))
    defaults.update(get_routers(neutron_client))
    defaults.update(get_security_groups(neutron_client))
    defaults.update(get_floatinips(nova_client))
    defaults.update(get_users(keystone_client))
    defaults.update(get_tenants(keystone_client))

    with open(DEFAULTS_FILE, 'w+') as yaml_file:
        yaml_file.write(yaml.safe_dump(defaults, default_flow_style=False))
        yaml_file.seek(0)
        logger.info("Openstack Defaults found in the deployment:")
        print yaml_file.read()
        logger.debug("NOTE: These objects will NOT be deleted after " +
                     "running the tests.")

    exit(0)


if __name__ == '__main__':
    main()
