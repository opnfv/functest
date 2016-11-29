#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import glance
import nova
# import neutron
import keystone
import cinder
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("demo").getLogger()


def main():
    glance_client = glance.get_glance_client()
    keystone_client = keystone.get_keystone_client()
    # neutron_client = neutron.get_neutron_client()
    nova_client = nova.get_nova_client()
    cinder_client = cinder.get_cinder_client()

    images = glance.get_images(nova_client)
    print "images: %s" % images

    image_id = glance.get_image_id(glance_client, images[0].name)
    print "image_id: %s" % image_id

    users = keystone.get_users(keystone_client)
    print "users: %s" % users

    user_id = keystone.get_user_id(keystone_client, users[0].name)
    print "user_id: %s" % user_id

    instances = nova.get_instances(nova_client)
    print "instances: %s" % instances

    instances_status = nova.get_instance_status(nova_client, instances[0])
    print "instances_status: %s" % instances_status

    # networks = neutron.get_network_list(neutron_client)
    # print "networks:%s" % networks

    # routers = neutron.get_router_list(neutron_client)
    # print "routers: %s" % routers

    volumes = cinder.get_volumes(cinder_client)
    print "volumes: %s" % volumes

    volume_types = cinder.list_volume_types(cinder_client)
    print "volume_types: %s" % volume_types


if __name__ == '__main__':
    main()
