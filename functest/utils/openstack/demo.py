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
# import neutron
import keystone
import cinder
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_constants as ft_constants

logger = ft_logger.Logger("demo").getLogger()
PROMISE_IMAGE_NAME = ft_constants.PROMISE_IMAGE_NAME
GLANCE_IMAGE_FILENAME = ft_constants.GLANCE_IMAGE_FILENAME
GLANCE_IMAGE_PATH = os.path.join(ft_constants.FUNCTEST_DATA_DIR,
                                 GLANCE_IMAGE_FILENAME)


def main():
    glance_client = glance.get_glance_client()
    keystone_client = keystone.get_keystone_client()
    # neutron_client = neutron.get_neutron_client()
    nova_client = nova.get_nova_client()
    cinder_client = cinder.get_cinder_client()

    image_id = glance.create_glance_image(glance_client,
                                          PROMISE_IMAGE_NAME,
                                          GLANCE_IMAGE_PATH)
    logger.info("image_id: %s " % image_id)

    image_data = glance.get_image_data_by_id(glance_client, image_id)
    logger.info("image_data: %s " % image_data)

    #deleted = glance.delete_glance_image(nova_client, image_id)
    #logger.info("deleted: %s" % deleted)

    images = glance.get_images(nova_client)
    logger.info("images: %s" % images)

    image_id = glance.get_image_id(glance_client, images[0].name)
    logger.info("image_id: %s" % image_id)

    users = keystone.get_users(keystone_client)
    logger.info("users: %s" % users)

    user_id = keystone.get_user_id(keystone_client, users[0].name)
    logger.info("user_id: %s" % user_id)

    instances = nova.get_instances(nova_client)
    logger.info("instances: %s" % instances)

    instances_status = nova.get_instance_status(nova_client, instances[0])
    logger.info("instances_status: %s" % instances_status)

    # networks = neutron.get_network_list(neutron_client)
    # logger.info("networks: %s" % networks)

    # routers = neutron.get_router_list(neutron_client)
    # logger.info("routers: %s" % routers)

    volumes = cinder.get_volumes(cinder_client)
    logger.info("volumes: %s" % volumes)

    volume_types = cinder.list_volume_types(cinder_client)
    logger.info("volume_types: %s" % volume_types)


if __name__ == '__main__':
    main()
