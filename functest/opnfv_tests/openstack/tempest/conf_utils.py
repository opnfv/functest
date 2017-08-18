#!/usr/bin/env python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
import ConfigParser
import logging
import os
import pkg_resources
import shutil
import subprocess

import yaml

from functest.utils.constants import CONST
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils


IMAGE_ID_ALT = None
FLAVOR_ID_ALT = None
GLANCE_IMAGE_PATH = os.path.join(
    CONST.__getattribute__('dir_functest_images'),
    CONST.__getattribute__('openstack_image_file_name'))
TEMPEST_RESULTS_DIR = os.path.join(CONST.__getattribute__('dir_results'),
                                   'tempest')
TEMPEST_CUSTOM = pkg_resources.resource_filename(
    'functest', 'opnfv_tests/openstack/tempest/custom_tests/test_list.txt')
TEMPEST_BLACKLIST = pkg_resources.resource_filename(
    'functest', 'opnfv_tests/openstack/tempest/custom_tests/blacklist.txt')
TEMPEST_DEFCORE = pkg_resources.resource_filename(
    'functest',
    'opnfv_tests/openstack/tempest/custom_tests/defcore_req.txt')
TEMPEST_RAW_LIST = os.path.join(TEMPEST_RESULTS_DIR, 'test_raw_list.txt')
TEMPEST_LIST = os.path.join(TEMPEST_RESULTS_DIR, 'test_list.txt')
REFSTACK_RESULTS_DIR = os.path.join(CONST.__getattribute__('dir_results'),
                                    'refstack')
TEMPEST_CONF_YAML = pkg_resources.resource_filename(
    'functest', 'opnfv_tests/openstack/tempest/custom_tests/tempest_conf.yaml')

CI_INSTALLER_TYPE = CONST.__getattribute__('INSTALLER_TYPE')
CI_INSTALLER_IP = CONST.__getattribute__('INSTALLER_IP')

""" logging configuration """
logger = logging.getLogger(__name__)


def create_tempest_resources(use_custom_images=False,
                             use_custom_flavors=False):
    keystone_client = os_utils.get_keystone_client()

    logger.debug("Creating tenant and user for Tempest suite")
    tenant_id = os_utils.create_tenant(
        keystone_client,
        CONST.__getattribute__('tempest_identity_tenant_name'),
        CONST.__getattribute__('tempest_identity_tenant_description'))
    if not tenant_id:
        logger.error("Failed to create %s tenant"
                     % CONST.__getattribute__('tempest_identity_tenant_name'))

    user_id = os_utils.create_user(
        keystone_client,
        CONST.__getattribute__('tempest_identity_user_name'),
        CONST.__getattribute__('tempest_identity_user_password'),
        None, tenant_id)
    if not user_id:
        logger.error("Failed to create %s user" %
                     CONST.__getattribute__('tempest_identity_user_name'))

    logger.debug("Creating private network for Tempest suite")
    network_dic = os_utils.create_shared_network_full(
        CONST.__getattribute__('tempest_private_net_name'),
        CONST.__getattribute__('tempest_private_subnet_name'),
        CONST.__getattribute__('tempest_router_name'),
        CONST.__getattribute__('tempest_private_subnet_cidr'))
    if network_dic is None:
        raise Exception('Failed to create private network')

    image_id = ""
    image_id_alt = ""
    flavor_id = ""
    flavor_id_alt = ""

    if (CONST.__getattribute__('tempest_use_custom_images') or
       use_custom_images):
        # adding alternative image should be trivial should we need it
        logger.debug("Creating image for Tempest suite")
        _, image_id = os_utils.get_or_create_image(
            CONST.__getattribute__('openstack_image_name'),
            GLANCE_IMAGE_PATH,
            CONST.__getattribute__('openstack_image_disk_format'))
        if image_id is None:
            raise Exception('Failed to create image')

    if use_custom_images:
        logger.debug("Creating 2nd image for Tempest suite")
        _, image_id_alt = os_utils.get_or_create_image(
            CONST.__getattribute__('openstack_image_name_alt'),
            GLANCE_IMAGE_PATH,
            CONST.__getattribute__('openstack_image_disk_format'))
        if image_id_alt is None:
            raise Exception('Failed to create image')

    if (CONST.__getattribute__('tempest_use_custom_flavors') or
       use_custom_flavors):
        # adding alternative flavor should be trivial should we need it
        logger.debug("Creating flavor for Tempest suite")
        _, flavor_id = os_utils.get_or_create_flavor(
            CONST.__getattribute__('openstack_flavor_name'),
            CONST.__getattribute__('openstack_flavor_ram'),
            CONST.__getattribute__('openstack_flavor_disk'),
            CONST.__getattribute__('openstack_flavor_vcpus'))
        if flavor_id is None:
            raise Exception('Failed to create flavor')

    if use_custom_flavors:
        logger.debug("Creating 2nd flavor for tempest_defcore")
        _, flavor_id_alt = os_utils.get_or_create_flavor(
            CONST.__getattribute__('openstack_flavor_name_alt'),
            CONST.__getattribute__('openstack_flavor_ram'),
            CONST.__getattribute__('openstack_flavor_disk'),
            CONST.__getattribute__('openstack_flavor_vcpus'))
        if flavor_id_alt is None:
            raise Exception('Failed to create flavor')

    img_flavor_dict = {}
    img_flavor_dict['image_id'] = image_id
    img_flavor_dict['image_id_alt'] = image_id_alt
    img_flavor_dict['flavor_id'] = flavor_id
    img_flavor_dict['flavor_id_alt'] = flavor_id_alt

    return img_flavor_dict


def get_verifier_id():
    """
    Returns verifer id for current Tempest
    """
    cmd = ("rally verify list-verifiers | awk '/" +
           CONST.__getattribute__('tempest_deployment_name') +
           "/ {print $2}'")
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    deployment_uuid = p.stdout.readline().rstrip()
    if deployment_uuid == "":
        logger.error("Tempest verifier not found.")
        raise Exception('Error with command:%s' % cmd)
    return deployment_uuid


def get_verifier_deployment_id():
    """
    Returns deployment id for active Rally deployment
    """
    cmd = ("rally deployment list | awk '/" +
           CONST.__getattribute__('rally_deployment_name') +
           "/ {print $2}'")
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    deployment_uuid = p.stdout.readline().rstrip()
    if deployment_uuid == "":
        logger.error("Rally deployment not found.")
        raise Exception('Error with command:%s' % cmd)
    return deployment_uuid


def get_verifier_repo_dir(verifier_id):
    """
    Returns installed verfier repo directory for Tempest
    """
    if not verifier_id:
        verifier_id = get_verifier_id()

    return os.path.join(CONST.__getattribute__('dir_rally_inst'),
                        'verification',
                        'verifier-{}'.format(verifier_id),
                        'repo')


def get_verifier_deployment_dir(verifier_id, deployment_id):
    """
    Returns Rally deployment directory for current verifier
    """
    if not verifier_id:
        verifier_id = get_verifier_id()

    if not deployment_id:
        deployment_id = get_verifier_deployment_id()

    return os.path.join(CONST.__getattribute__('dir_rally_inst'),
                        'verification',
                        'verifier-{}'.format(verifier_id),
                        'for-deployment-{}'.format(deployment_id))


def get_repo_tag(repo):
    """
    Returns last tag of current branch
    """
    cmd = ("git -C {0} describe --abbrev=0 HEAD".format(repo))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    tag = p.stdout.readline().rstrip()

    return str(tag)


def backup_tempest_config(conf_file):
    """
    Copy config file to tempest results directory
    """
    if not os.path.exists(TEMPEST_RESULTS_DIR):
        os.makedirs(TEMPEST_RESULTS_DIR)

    shutil.copyfile(conf_file,
                    os.path.join(TEMPEST_RESULTS_DIR, 'tempest.conf'))


def configure_tempest(deployment_dir, IMAGE_ID=None, FLAVOR_ID=None,
                      MODE=None):
    """
    Calls rally verify and updates the generated tempest.conf with
    given parameters
    """
    conf_file = configure_verifier(deployment_dir)
    configure_tempest_update_params(conf_file,
                                    IMAGE_ID, FLAVOR_ID)


def configure_tempest_defcore(deployment_dir, img_flavor_dict):
    """
    Add/update needed parameters into tempest.conf file
    """
    conf_file = configure_verifier(deployment_dir)
    configure_tempest_update_params(conf_file,
                                    img_flavor_dict.get("image_id"),
                                    img_flavor_dict.get("flavor_id"))

    logger.debug("Updating selected tempest.conf parameters for defcore...")
    config = ConfigParser.RawConfigParser()
    config.read(conf_file)
    config.set('DEFAULT', 'log_file', '{}/tempest.log'.format(deployment_dir))
    config.set('oslo_concurrency', 'lock_path',
               '{}/lock_files'.format(deployment_dir))
    config.set('scenario', 'img_dir', '{}'.format(deployment_dir))
    config.set('scenario', 'img_file', 'tempest-image')
    config.set('compute', 'image_ref', img_flavor_dict.get("image_id"))
    config.set('compute', 'image_ref_alt',
               img_flavor_dict['image_id_alt'])
    config.set('compute', 'flavor_ref', img_flavor_dict.get("flavor_id"))
    config.set('compute', 'flavor_ref_alt',
               img_flavor_dict['flavor_id_alt'])

    with open(conf_file, 'wb') as config_file:
        config.write(config_file)

    confpath = pkg_resources.resource_filename(
        'functest',
        'opnfv_tests/openstack/refstack_client/refstack_tempest.conf')
    shutil.copyfile(conf_file, confpath)


def configure_tempest_update_params(tempest_conf_file,
                                    IMAGE_ID=None, FLAVOR_ID=None):
    """
    Add/update needed parameters into tempest.conf file
    """
    logger.debug("Updating selected tempest.conf parameters...")
    config = ConfigParser.RawConfigParser()
    config.read(tempest_conf_file)
    config.set(
        'compute',
        'fixed_network_name',
        CONST.__getattribute__('tempest_private_net_name'))
    config.set('compute', 'volume_device_name',
               CONST.__getattribute__('tempest_volume_device_name'))
    if CONST.__getattribute__('tempest_use_custom_images'):
        if IMAGE_ID is not None:
            config.set('compute', 'image_ref', IMAGE_ID)
        if IMAGE_ID_ALT is not None:
            config.set('compute', 'image_ref_alt', IMAGE_ID_ALT)
    if CONST.__getattribute__('tempest_use_custom_flavors'):
        if FLAVOR_ID is not None:
            config.set('compute', 'flavor_ref', FLAVOR_ID)
        if FLAVOR_ID_ALT is not None:
            config.set('compute', 'flavor_ref_alt', FLAVOR_ID_ALT)
    config.set('identity', 'tenant_name',
               CONST.__getattribute__('tempest_identity_tenant_name'))
    config.set('identity', 'username',
               CONST.__getattribute__('tempest_identity_user_name'))
    config.set('identity', 'password',
               CONST.__getattribute__('tempest_identity_user_password'))
    config.set('identity', 'region', 'RegionOne')
    if os_utils.is_keystone_v3():
        auth_version = 'v3'
    else:
        auth_version = 'v2'
    config.set('identity', 'auth_version', auth_version)
    config.set(
        'validation', 'ssh_timeout',
        CONST.__getattribute__('tempest_validation_ssh_timeout'))
    config.set('object-storage', 'operator_role',
               CONST.__getattribute__('tempest_object_storage_operator_role'))

    if CONST.__getattribute__('OS_ENDPOINT_TYPE') is not None:
        sections = config.sections()
        if os_utils.is_keystone_v3():
            config.set('identity', 'v3_endpoint_type',
                       CONST.__getattribute__('OS_ENDPOINT_TYPE'))
            if 'identity-feature-enabled' not in sections:
                config.add_section('identity-feature-enabled')
                config.set('identity-feature-enabled', 'api_v2', False)
                config.set('identity-feature-enabled', 'api_v2_admin', False)
        services_list = ['compute',
                         'volume',
                         'image',
                         'network',
                         'data-processing',
                         'object-storage',
                         'orchestration']
        for service in services_list:
            if service not in sections:
                config.add_section(service)
            config.set(service, 'endpoint_type',
                       CONST.__getattribute__('OS_ENDPOINT_TYPE'))

    logger.debug('Add/Update required params defined in tempest_conf.yaml '
                 'into tempest.conf file')
    with open(TEMPEST_CONF_YAML) as f:
        conf_yaml = yaml.safe_load(f)
    if conf_yaml:
        sections = config.sections()
        for section in conf_yaml:
            if section not in sections:
                config.add_section(section)
            sub_conf = conf_yaml.get(section)
            for key, value in sub_conf.items():
                config.set(section, key, value)

    with open(tempest_conf_file, 'wb') as config_file:
        config.write(config_file)

    backup_tempest_config(tempest_conf_file)


def configure_verifier(deployment_dir):
    """
    Execute rally verify configure-verifier, which generates tempest.conf
    """
    tempest_conf_file = os.path.join(deployment_dir, "tempest.conf")
    if os.path.isfile(tempest_conf_file):
        logger.debug("Verifier is already configured.")
        logger.debug("Reconfiguring the current verifier...")
        cmd = "rally verify configure-verifier --reconfigure"
    else:
        logger.info("Configuring the verifier...")
        cmd = "rally verify configure-verifier"
    ft_utils.execute_command(cmd)

    logger.debug("Looking for tempest.conf file...")
    if not os.path.isfile(tempest_conf_file):
        logger.error("Tempest configuration file %s NOT found."
                     % tempest_conf_file)
        raise Exception("Tempest configuration file %s NOT found."
                        % tempest_conf_file)
    else:
        return tempest_conf_file
