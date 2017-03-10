##############################################################################
# Copyright (c) 2017 Huawei Technologies Co.,Ltd and others.
# matthew.lijun@huawei.com wangwulin@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
import ConfigParser
import shutil
import os

from functest.utils.constants import CONST
from functest.opnfv_tests.openstack.tempest import conf_utils
import functest.utils.functest_logger as ft_logger
import functest.utils.openstack_utils as os_utils


GLANCE_IMAGE_PATH = os.path.join(CONST.dir_functest_data,
                                 CONST.openstack_image_file_name)


""" logging configuration """
logger = ft_logger.Logger("Tempest_defcore").getLogger()


def create_tempest_resources():
    keystone_client = os_utils.get_keystone_client()

    logger.debug("Creating tenant and user for Tempest suite")
    tenant_id = os_utils.create_tenant(
        keystone_client,
        CONST.tempest_identity_tenant_name,
        CONST.tempest_identity_tenant_description)
    if not tenant_id:
        logger.error("Failed to create %s tenant"
                     % CONST.tempest_identity_tenant_name)

    user_id = os_utils.create_user(keystone_client,
                                   CONST.tempest_identity_user_name,
                                   CONST.tempest_identity_user_password,
                                   None, tenant_id)
    if not user_id:
        logger.error("Failed to create %s user" %
                     CONST.tempest_identity_user_name)

    logger.debug("Creating private network for Tempest suite")
    network_dic = os_utils.create_shared_network_full(
        CONST.tempest_private_net_name,
        CONST.tempest_private_subnet_name,
        CONST.tempest_router_name,
        CONST.tempest_private_subnet_cidr)
    if network_dic is None:
        raise Exception('Failed to create private network')

    logger.debug("Creating image for tempest_defcore")
    _, IMAGE_ID = os_utils.get_or_create_image(
        CONST.openstack_image_name, GLANCE_IMAGE_PATH,
        CONST.openstack_image_disk_format)
    _, IMAGE_ID_ALT = os_utils.get_or_create_image(
        CONST.openstack_image_name_alt, GLANCE_IMAGE_PATH,
        CONST.openstack_image_disk_format)
    if IMAGE_ID is None or IMAGE_ID_ALT is None:
        raise Exception('Failed to create image')
    return IMAGE_ID, IMAGE_ID_ALT


def configure_tempest(deployment_dir, IMAGE_ID=None, IMAGE_ID_ALT=None):
    conf_file = conf_utils.configure_verifier(deployment_dir)
    configure_tempest_defcore_params(conf_file,
                                     IMAGE_ID, IMAGE_ID_ALT)


def configure_tempest_defcore_params(tempest_conf_file, IMAGE_ID=None,
                                     IMAGE_ID_ALT=None):
    """
    Add/update needed parameters into tempest.conf file
    """
    logger.debug("Updating selected tempest.conf parameters...")
    config = ConfigParser.RawConfigParser()
    config.read(tempest_conf_file)
    config.set('compute', 'fixed_network_name', CONST.tempest_private_net_name)
    config.set('compute', 'image_ref', IMAGE_ID)
    config.set('compute', 'image_ref_alt', IMAGE_ID_ALT)
    FLAVOR_ID = 1
    FLAVOR_ID_ALT = 2
    config.set('compute', 'flavor_ref', FLAVOR_ID)
    config.set('compute', 'flavor_ref_alt', FLAVOR_ID_ALT)
    config.set('identity', 'tenant_name', CONST.tempest_identity_tenant_name)
    config.set('identity', 'username', CONST.tempest_identity_user_name)
    config.set('identity', 'password', CONST.tempest_identity_user_password)
    config.set(
        'validation', 'ssh_timeout', CONST.tempest_validation_ssh_timeout)

    if CONST.OS_ENDPOINT_TYPE is not None:
        services_list = ['compute',
                         'volume',
                         'image',
                         'network',
                         'data-processing',
                         'object-storage',
                         'orchestration']
        sections = config.sections()
        for service in services_list:
            if service not in sections:
                config.add_section(service)
            config.set(service, 'endpoint_type',
                       CONST.OS_ENDPOINT_TYPE)

    with open(tempest_conf_file, 'wb') as config_file:
        config.write(config_file)

    shutil.copyfile(tempest_conf_file,
                    CONST.refstack_tempest_conf_path)
