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
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
import yaml


logger = ft_logger.Logger("openstack_snapshot").getLogger()

REPO_PATH = os.environ['repos_dir'] + '/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)


OS_SNAPSHOT_FILE = ft_utils.get_parameter_from_yaml(
    "general.openstack.snapshot_file")


def separator():
    logger.info("-------------------------------------------")


def get_instances(nova_client):
    logger.debug("Getting instances...")
    dic_instances = {}
    instances = os_utils.get_instances(nova_client)
    if not (instances is None or len(instances) == 0):
        for instance in instances:
            dic_instances.update({getattr(instance, 'id'): getattr(instance,
                                                                   'name')})
    return {'instances': dic_instances}


def get_images(nova_client):
    logger.debug("Getting images...")
    dic_images = {}
    images = os_utils.get_images(nova_client)
    if not (images is None or len(images) == 0):
        for image in images:
            dic_images.update({getattr(image, 'id'): getattr(image, 'name')})
    return {'images': dic_images}


def get_volumes(cinder_client):
    logger.debug("Getting volumes...")
    dic_volumes = {}
    volumes = os_utils.get_volumes(cinder_client)
    if volumes is not None:
        for volume in volumes:
            dic_volumes.update({volume.id: volume.display_name})
    return {'volumes': dic_volumes}


def get_networks(neutron_client):
    logger.debug("Getting networks")
    dic_networks = {}
    networks = os_utils.get_network_list(neutron_client)
    if networks is not None:
        for network in networks:
            dic_networks.update({network['id']: network['name']})
    return {'networks': dic_networks}


def get_routers(neutron_client):
    logger.debug("Getting routers")
    dic_routers = {}
    routers = os_utils.get_router_list(neutron_client)
    if routers is not None:
        for router in routers:
            dic_routers.update({router['id']: router['name']})
    return {'routers': dic_routers}


def get_security_groups(neutron_client):
    logger.debug("Getting Security groups...")
    dic_secgroups = {}
    secgroups = os_utils.get_security_groups(neutron_client)
    if not (secgroups is None or len(secgroups) == 0):
        for secgroup in secgroups:
            dic_secgroups.update({secgroup['id']: secgroup['name']})
    return {'secgroups': dic_secgroups}


def get_floatinips(nova_client):
    logger.debug("Getting Floating IPs...")
    dic_floatingips = {}
    floatingips = os_utils.get_floating_ips(nova_client)
    if not (floatingips is None or len(floatingips) == 0):
        for floatingip in floatingips:
            dic_floatingips.update({floatingip.id: floatingip.ip})
    return {'floatingips': dic_floatingips}


def get_users(keystone_client):
    logger.debug("Getting users...")
    dic_users = {}
    users = os_utils.get_users(keystone_client)
    if not (users is None or len(users) == 0):
        for user in users:
            dic_users.update({getattr(user, 'id'): getattr(user, 'name')})
    return {'users': dic_users}


def get_tenants(keystone_client):
    logger.debug("Getting tenants...")
    dic_tenants = {}
    tenants = os_utils.get_tenants(keystone_client)
    if not (tenants is None or len(tenants) == 0):
        for tenant in tenants:
            dic_tenants.update({getattr(tenant, 'id'):
                                getattr(tenant, 'name')})
    return {'tenants': dic_tenants}


def main():
    logger.info("Generating OpenStack snapshot...")

    nova_client = os_utils.get_nova_client()
    neutron_client = os_utils.get_neutron_client()
    keystone_client = os_utils.get_keystone_client()
    cinder_client = os_utils.get_cinder_client()

    if not os_utils.check_credentials():
        logger.error("Please source the openrc credentials and run the" +
                     "script again.")
        exit(-1)

    snapshot = {}
    snapshot.update(get_instances(nova_client))
    snapshot.update(get_images(nova_client))
    snapshot.update(get_volumes(cinder_client))
    snapshot.update(get_networks(neutron_client))
    snapshot.update(get_routers(neutron_client))
    snapshot.update(get_security_groups(neutron_client))
    snapshot.update(get_floatinips(nova_client))
    snapshot.update(get_users(keystone_client))
    snapshot.update(get_tenants(keystone_client))

    with open(OS_SNAPSHOT_FILE, 'w+') as yaml_file:
        yaml_file.write(yaml.safe_dump(snapshot, default_flow_style=False))
        yaml_file.seek(0)
        logger.debug("Openstack Snapshot found in the deployment:\n%s"
                     % yaml_file.read())
        logger.debug("NOTE: These objects will NOT be deleted after " +
                     "running the test.")


if __name__ == '__main__':
    main()
