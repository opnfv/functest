#!/usr/bin/python
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
import re
import shutil
import subprocess

from functest.utils.constants import CONST
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils


IMAGE_ID_ALT = None
FLAVOR_ID_ALT = None
REPO_PATH = CONST.dir_repo_functest
GLANCE_IMAGE_PATH = os.path.join(CONST.dir_functest_data,
                                 CONST.openstack_image_file_name)
TEMPEST_TEST_LIST_DIR = CONST.dir_tempest_cases
TEMPEST_RESULTS_DIR = os.path.join(CONST.dir_results,
                                   'tempest')
TEMPEST_CUSTOM = os.path.join(REPO_PATH, TEMPEST_TEST_LIST_DIR,
                              'test_list.txt')
TEMPEST_BLACKLIST = os.path.join(REPO_PATH, TEMPEST_TEST_LIST_DIR,
                                 'blacklist.txt')
TEMPEST_DEFCORE = os.path.join(REPO_PATH, TEMPEST_TEST_LIST_DIR,
                               'defcore_req.txt')
TEMPEST_RAW_LIST = os.path.join(TEMPEST_RESULTS_DIR, 'test_raw_list.txt')
TEMPEST_LIST = os.path.join(TEMPEST_RESULTS_DIR, 'test_list.txt')
REFSTACK_RESULTS_DIR = os.path.join(CONST.dir_results,
                                    'refstack')

CI_INSTALLER_TYPE = CONST.INSTALLER_TYPE
CI_INSTALLER_IP = CONST.INSTALLER_IP

""" logging configuration """
logger = logging.getLogger(__name__)


def create_tempest_resources(use_custom_images=False,
                             use_custom_flavors=False):
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

    image_id = ""
    image_id_alt = ""
    flavor_id = ""
    flavor_id_alt = ""

    if CONST.tempest_use_custom_images or use_custom_images:
        # adding alternative image should be trivial should we need it
        logger.debug("Creating image for Tempest suite")
        _, image_id = os_utils.get_or_create_image(
            CONST.openstack_image_name, GLANCE_IMAGE_PATH,
            CONST.openstack_image_disk_format)
        if image_id is None:
            raise Exception('Failed to create image')

    if use_custom_images:
        logger.debug("Creating 2nd image for Tempest suite")
        _, image_id_alt = os_utils.get_or_create_image(
            CONST.openstack_image_name_alt, GLANCE_IMAGE_PATH,
            CONST.openstack_image_disk_format)
        if image_id_alt is None:
            raise Exception('Failed to create image')

    if CONST.tempest_use_custom_flavors or use_custom_flavors:
        # adding alternative flavor should be trivial should we need it
        logger.debug("Creating flavor for Tempest suite")
        _, flavor_id = os_utils.get_or_create_flavor(
            CONST.openstack_flavor_name,
            CONST.openstack_flavor_ram,
            CONST.openstack_flavor_disk,
            CONST.openstack_flavor_vcpus)
        if flavor_id is None:
            raise Exception('Failed to create flavor')

    if use_custom_flavors:
        logger.debug("Creating 2nd flavor for tempest_defcore")
        _, flavor_id_alt = os_utils.get_or_create_flavor(
            CONST.openstack_flavor_name_alt,
            CONST.openstack_flavor_ram,
            CONST.openstack_flavor_disk,
            CONST.openstack_flavor_vcpus)
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
           CONST.tempest_deployment_name +
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
           CONST.rally_deployment_name +
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

    return os.path.join(CONST.dir_rally_inst,
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

    return os.path.join(CONST.dir_rally_inst,
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
    if MODE == 'feature_multisite':
        configure_tempest_multisite_params(conf_file)


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
    config.set('compute', 'image_ref', img_flavor_dict.get("image_id"))
    config.set('compute', 'image_ref_alt',
               img_flavor_dict['image_id_alt'])
    config.set('compute', 'flavor_ref', img_flavor_dict.get("flavor_id"))
    config.set('compute', 'flavor_ref_alt',
               img_flavor_dict['flavor_id_alt'])

    with open(conf_file, 'wb') as config_file:
        config.write(config_file)

    confpath = os.path.join(CONST.dir_functest_test,
                            CONST.refstack_tempest_conf_path)
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
        CONST.tempest_private_net_name)
    config.set('compute', 'volume_device_name',
               CONST.tempest_volume_device_name)
    if CONST.tempest_use_custom_images:
        if IMAGE_ID is not None:
            config.set('compute', 'image_ref', IMAGE_ID)
        if IMAGE_ID_ALT is not None:
            config.set('compute', 'image_ref_alt', IMAGE_ID_ALT)
    if CONST.tempest_use_custom_flavors:
        if FLAVOR_ID is not None:
            config.set('compute', 'flavor_ref', FLAVOR_ID)
        if FLAVOR_ID_ALT is not None:
            config.set('compute', 'flavor_ref_alt', FLAVOR_ID_ALT)
    config.set('identity', 'tenant_name', CONST.tempest_identity_tenant_name)
    config.set('identity', 'username', CONST.tempest_identity_user_name)
    config.set('identity', 'password', CONST.tempest_identity_user_password)
    config.set('identity', 'region', 'RegionOne')
    config.set(
        'validation', 'ssh_timeout', CONST.tempest_validation_ssh_timeout)
    config.set('object-storage', 'operator_role',
               CONST.tempest_object_storage_operator_role)

    if CONST.OS_ENDPOINT_TYPE is not None:
        sections = config.sections()
        if os_utils.is_keystone_v3():
            config.set('identity', 'v3_endpoint_type', CONST.OS_ENDPOINT_TYPE)
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
                       CONST.OS_ENDPOINT_TYPE)

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


def configure_tempest_multisite_params(tempest_conf_file):
    """
    Add/update multisite parameters into tempest.conf file generated by Rally
    """
    logger.debug("Updating multisite tempest.conf parameters...")
    config = ConfigParser.RawConfigParser()
    config.read(tempest_conf_file)

    config.set('service_available', 'kingbird', 'true')
    # cmd = ("openstack endpoint show kingbird | grep publicurl |"
    #       "awk '{print $4}' | awk -F '/' '{print $4}'")
    # kingbird_api_version = os.popen(cmd).read()
    # kingbird_api_version = os_utils.get_endpoint(service_type='multisite')

    if CI_INSTALLER_TYPE == 'fuel':
        # For MOS based setup, the service is accessible
        # via bind host
        kingbird_conf_path = "/etc/kingbird/kingbird.conf"
        installer_type = CI_INSTALLER_TYPE
        installer_ip = CI_INSTALLER_IP
        installer_username = CONST.__getattribute__(
            'multisite_{}_installer_username'.format(installer_type))
        installer_password = CONST.__getattribute__(
            'multisite_{}_installer_password'.format(installer_type))

        ssh_options = ("-o UserKnownHostsFile=/dev/null -o "
                       "StrictHostKeyChecking=no")

        # Get the controller IP from the fuel node
        cmd = 'sshpass -p %s ssh 2>/dev/null %s %s@%s \
                \'fuel node --env 1| grep controller | grep "True\|  1" \
                | awk -F\| "{print \$5}"\'' % (installer_password,
                                               ssh_options,
                                               installer_username,
                                               installer_ip)
        multisite_controller_ip = "".join(os.popen(cmd).read().split())

        # Login to controller and get bind host details
        cmd = 'sshpass -p %s ssh 2>/dev/null  %s %s@%s "ssh %s \\" \
            grep -e "^bind_" %s  \\""' % (installer_password,
                                          ssh_options,
                                          installer_username,
                                          installer_ip,
                                          multisite_controller_ip,
                                          kingbird_conf_path)
        bind_details = os.popen(cmd).read()
        bind_details = "".join(bind_details.split())
        # Extract port number from the bind details
        bind_port = re.findall(r"\D(\d{4})", bind_details)[0]
        # Extract ip address from the bind details
        bind_host = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
                               bind_details)[0]
        kingbird_endpoint_url = "http://%s:%s/" % (bind_host, bind_port)
    else:
        # cmd = "openstack endpoint show kingbird | grep publicurl |\
        #       awk '{print $4}' | awk -F '/' '{print $3}'"
        # kingbird_endpoint_url = os.popen(cmd).read()
        kingbird_endpoint_url = os_utils.get_endpoint(service_type='kingbird')

    try:
        config.add_section("kingbird")
    except Exception:
        logger.info('kingbird section exist')

    # set the domain id
    config.set('auth', 'admin_domain_name', 'default')

    config.set('kingbird', 'endpoint_type', 'publicURL')
    config.set('kingbird', 'TIME_TO_SYNC', '120')
    config.set('kingbird', 'endpoint_url', kingbird_endpoint_url)
    config.set('kingbird', 'api_version', 'v1.0')
    with open(tempest_conf_file, 'wb') as config_file:
        config.write(config_file)

    backup_tempest_config(tempest_conf_file)


def install_verifier_ext(path):
    """
    Install extension to active verifier
    """
    logger.info("Installing verifier from existing repo...")
    tag = get_repo_tag(path)
    cmd = ("rally verify add-verifier-ext --source {0} "
           "--version {1}"
           .format(path, tag))
    error_msg = ("Problem while adding verifier extension from %s" % path)
    ft_utils.execute_command_raise(cmd, error_msg=error_msg)
