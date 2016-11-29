#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import os

import glanceclient.client as glance_client

import keystone
#import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("glance").getLogger()

DEFAULT_API_VERSION = '2'
API_NAME = 'image'


def get_client_version():
    api_version = os.getenv('OS_IMAGE_API_VERSION')
    if api_version is not None:
        logger.info("OS_IMAGE_API_VERSION is set in env as '%s'", api_version)
        return api_version
    return DEFAULT_API_VERSION


def get_glance_client():
    keystone_client = keystone.get_keystone_client()
    glance_endpoint_type = 'publicURL'
    os_endpoint_type = os.getenv('OS_ENDPOINT_TYPE')
    if os_endpoint_type is not None:
        glance_endpoint_type = os_endpoint_type
    glance_endpoint = keystone_client.service_catalog.url_for(
        service_type='image', endpoint_type=glance_endpoint_type)

    return glance_client.Client(get_client_version(), glance_endpoint,
                                token=keystone_client.auth_token)


def get_images(nova_client):
    try:
        images = nova_client.images.list()
        return images
    except Exception, e:
        logger.error("Error [get_images]: %s" % e)
        return None


def get_image_id(glance_client, image_name):
    images = glance_client.images.list()
    id = ''
    for i in images:
        if i.name == image_name:
            id = i.id
            break
    return id


def create_glance_image(glance_client, image_name, file_path, disk="qcow2",
                        container="bare", public="public"):
    # TODO (Helen) need to refactor the file_path to image_url
    # file_path = ("http://download.cirros-cloud.net"
    #              "/0.3.4/cirros-0.3.4-x86_64-disk.img")
    if not os.path.isfile(file_path):
        logger.error("Error: file %s does not exist." % file_path)
        return None
    try:
        image_id = get_image_id(glance_client, image_name)
        if image_id != '':
            if logger:
                logger.info("Image %s already exists." % image_name)
        else:
            if logger:
                logger.info("Creating image '%s' from '%s'..." % (image_name,
                                                                  file_path))

            # TODO (Helen) verify why there is no general.image_properties
            # try:
            #     properties = ft_utils.get_functest_config(
            #         'general.image_properties')
            # except ValueError:
            #     # image properties are not configured
            #     # therefore don't add any properties
            #     properties = {}
            image = glance_client.images.create(name=image_name,
                                                visibility=public,
                                                disk_format=disk,
                                                container_format=container)
            image_id = image.id
        return image_id
    except Exception, e:
        logger.error("Error [create_glance_image(glance_client, '%s', '%s', "
                     "'%s')]: %s" % (image_name, file_path, str(public), e))
        return None


def get_or_create_image(name, path, format):
    image_exists = False
    glance_client = get_glance_client()

    image_id = get_image_id(glance_client, name)
    if image_id != '':
        logger.info("Using existing image '%s'..." % name)
        image_exists = True
    else:
        logger.info("Creating image '%s' from '%s'..." % (name, path))
        image_id = create_glance_image(glance_client, name, path, format)
        if not image_id:
            logger.error("Failed to create a Glance image...")
        else:
            logger.debug("Image '%s' with ID=%s created successfully."
                         % (name, image_id))

    return image_exists, image_id


def delete_glance_image(nova_client, image_id):
    try:
        nova_client.images.delete(image_id)
        return True
    except Exception, e:
        logger.error("Error [delete_glance_image(nova_client, '%s')]: %s"
                     % (image_id, e))
        return False


def get_image_data_by_id(glance_client, image_id):
    return glance_client.images.get(image_id)
