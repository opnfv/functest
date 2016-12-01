#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import os
import glance
import nova
import neutron
import keystone
import cinder
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_constants as ft_constants

logger = ft_logger.Logger("demo").getLogger()
GLANCE_IMAGE_FILENAME = ft_constants.GLANCE_IMAGE_FILENAME
GLANCE_IMAGE_PATH = os.path.join(ft_constants.FUNCTEST_DATA_DIR,
                                 GLANCE_IMAGE_FILENAME)
FLAVOR_NAME = ft_constants.FLAVOR_NAME
FLAVOR_RAM = ft_constants.FLAVOR_RAM
FLAVOR_DISK = ft_constants.FLAVOR_DISK
FLAVOR_VCPUS = ft_constants.FLAVOR_VCPUS


def print_separator(id, service):
    logger.info("============DEMO %s: %s Client============" % (id, service))


def main():
    glance_client = glance.get_glance_client()
    keystone_client = keystone.get_keystone_client()
    neutron_client = neutron.get_neutron_client()
    nova_client = nova.get_nova_client()
    cinder_client = cinder.get_cinder_client()

    print_separator(1, 'Glance')
    images = glance.get_images(glance_client)
    logger.info("all images: %s" % images)

    if images:
        image_id = glance.get_image_id(glance_client, images[0].name)
        logger.info("first image_id: %s" % image_id)
    else:
        logger.info("no image exists")

    image_id = glance.create_glance_image(glance_client,
                                          'openstack_util_demo',
                                          GLANCE_IMAGE_PATH)
    logger.info("image_id: %s " % image_id)

    image_data = glance.get_image_data_by_id(glance_client, image_id)
    logger.info("image_data: %s " % image_data)

    print_separator(2, 'Keystone')
    users = keystone.get_users(keystone_client)
    logger.info("all users: %s" % users)

    if users:
        user_id = keystone.get_user_id(keystone_client, users[0].name)
        logger.info("first user_id: %s" % user_id)
    else:
        logger.info("no user exists")

    print_separator(3, 'Neutron')
    networks = neutron.get_network_list(neutron_client)
    logger.info("all networks: %s" % networks)

    routers = neutron.get_router_list(neutron_client)
    logger.info("all routers: %s" % routers)

    print_separator(4, 'Nova')
    flavor_id = nova.create_flavor(nova_client,
                                   FLAVOR_NAME,
                                   FLAVOR_RAM,
                                   FLAVOR_DISK,
                                   FLAVOR_VCPUS)
    logger.info('flavor_id: %s' % flavor_id)

    floating_ips = nova.get_floating_ips(nova_client)
    if floating_ips:
        logger.info('First floating ip: %s' % floating_ips[0])
    else:
        logger.info('No floating ip')

    # instance = nova.create_instance(FLAVOR_NAME,
    #                                 image_id,
    #                                 network_id)
    # logger.info('Instance: %s' % instance)

    instances = nova.get_instances(nova_client)
    logger.info("all instances: %s" % instances)

    if instances:
        instances_status = nova.get_instance_status(nova_client, instances[0])
        logger.info("first instances_status: %s" % instances_status)
    else:
        logger.info("no instance exists")


    print_separator(5, 'Cinder')
    volumes = cinder.get_volumes(cinder_client)
    logger.info("all volumes: %s" % volumes)

    volume_types = cinder.list_volume_types(cinder_client)
    logger.info("all volume_types: %s" % volume_types)

    print_separator(6, 'Cleanup - Mixed')
    deleted = glance.delete_image_by_id(glance_client, image_id)
    logger.info("deleted: %s" % deleted)

if __name__ == '__main__':
    main()
