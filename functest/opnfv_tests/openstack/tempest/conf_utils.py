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
import fileinput
import os
import pkg_resources
import shutil
import subprocess

import yaml

from functest.utils.constants import CONST
import functest.utils.functest_utils as ft_utils


IMAGE_ID_ALT = None
FLAVOR_ID_ALT = None
RALLY_CONF_PATH = "/etc/rally/rally.conf"
RALLY_AARCH64_PATCH_PATH = pkg_resources.resource_filename(
    'functest', 'ci/rally_aarch64_patch.conf')
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
TEST_ACCOUNTS_FILE = pkg_resources.resource_filename(
    'functest',
    'opnfv_tests/openstack/tempest/custom_tests/test_accounts.yaml')

CI_INSTALLER_TYPE = CONST.__getattribute__('INSTALLER_TYPE')
CI_INSTALLER_IP = CONST.__getattribute__('INSTALLER_IP')

""" logging configuration """
logger = logging.getLogger(__name__)


def create_rally_deployment():
    # set the architecture to default
    pod_arch = os.getenv("POD_ARCH", None)
    arch_filter = ['aarch64']

    if pod_arch and pod_arch in arch_filter:
        logger.info("Apply aarch64 specific to rally config...")
        with open(RALLY_AARCH64_PATCH_PATH, "r") as f:
            rally_patch_conf = f.read()

        for line in fileinput.input(RALLY_CONF_PATH, inplace=1):
            print line,
            if "cirros|testvm" in line:
                print rally_patch_conf

    logger.info("Creating Rally environment...")

    cmd = "rally deployment destroy opnfv-rally"
    ft_utils.execute_command(cmd, error_msg=(
        "Deployment %s does not exist."
        % CONST.__getattribute__('rally_deployment_name')),
        verbose=False)

    cmd = ("rally deployment create --fromenv --name={0}"
           .format(CONST.__getattribute__('rally_deployment_name')))
    error_msg = "Problem while creating Rally deployment"
    ft_utils.execute_command_raise(cmd, error_msg=error_msg)

    cmd = "rally deployment check"
    error_msg = "OpenStack not responding or faulty Rally deployment."
    ft_utils.execute_command_raise(cmd, error_msg=error_msg)


def create_verifier():
    logger.info("Create verifier from existing repo...")
    cmd = ("rally verify delete-verifier --id '{0}' --force").format(
        CONST.__getattribute__('tempest_verifier_name'))
    ft_utils.execute_command(cmd, error_msg=(
        "Verifier %s does not exist."
        % CONST.__getattribute__('tempest_verifier_name')),
        verbose=False)
    cmd = ("rally verify create-verifier --source {0} "
           "--name {1} --type tempest --system-wide"
           .format(CONST.__getattribute__('dir_repo_tempest'),
                   CONST.__getattribute__('tempest_verifier_name')))
    ft_utils.execute_command_raise(cmd,
                                   error_msg='Problem while creating verifier')


def get_verifier_id():
    """
    Returns verifier id for current Tempest
    """
    create_rally_deployment()
    create_verifier()
    cmd = ("rally verify list-verifiers | awk '/" +
           CONST.__getattribute__('tempest_verifier_name') +
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
    Returns installed verifier repo directory for Tempest
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


def backup_tempest_config(conf_file):
    """
    Copy config file to tempest results directory
    """
    if not os.path.exists(TEMPEST_RESULTS_DIR):
        os.makedirs(TEMPEST_RESULTS_DIR)
    shutil.copyfile(conf_file,
                    os.path.join(TEMPEST_RESULTS_DIR, 'tempest.conf'))


def configure_tempest(deployment_dir, image_id=None, flavor_id=None,
                      compute_cnt=None):
    """
    Calls rally verify and updates the generated tempest.conf with
    given parameters
    """
    conf_file = configure_verifier(deployment_dir)
    configure_tempest_update_params(conf_file, image_id, flavor_id,
                                    compute_cnt)


def configure_tempest_defcore(deployment_dir, image_id, flavor_id,
                              image_id_alt, flavor_id_alt, tenant_id):
    """
    Add/update needed parameters into tempest.conf file
    """
    conf_file = configure_verifier(deployment_dir)
    configure_tempest_update_params(conf_file, image_id, flavor_id)

    logger.debug("Updating selected tempest.conf parameters for defcore...")
    config = ConfigParser.RawConfigParser()
    config.read(conf_file)
    config.set('DEFAULT', 'log_file', '{}/tempest.log'.format(deployment_dir))
    config.set('oslo_concurrency', 'lock_path',
               '{}/lock_files'.format(deployment_dir))
    generate_test_accounts_file(tenant_id=tenant_id)
    config.set('auth', 'test_accounts_file', TEST_ACCOUNTS_FILE)
    config.set('scenario', 'img_dir', '{}'.format(deployment_dir))
    config.set('scenario', 'img_file', 'tempest-image')
    config.set('compute', 'image_ref', image_id)
    config.set('compute', 'image_ref_alt', image_id_alt)
    config.set('compute', 'flavor_ref', flavor_id)
    config.set('compute', 'flavor_ref_alt', flavor_id_alt)

    with open(conf_file, 'wb') as config_file:
        config.write(config_file)

    confpath = pkg_resources.resource_filename(
        'functest',
        'opnfv_tests/openstack/refstack_client/refstack_tempest.conf')
    shutil.copyfile(conf_file, confpath)


def generate_test_accounts_file(tenant_id):
    """
    Add needed tenant and user params into test_accounts.yaml
    """

    logger.debug("Add needed params into test_accounts.yaml...")
    accounts_list = [
        {
            'tenant_name':
                CONST.__getattribute__('tempest_identity_tenant_name'),
            'tenant_id': str(tenant_id),
            'username': CONST.__getattribute__('tempest_identity_user_name'),
            'password':
                CONST.__getattribute__('tempest_identity_user_password')
        }
    ]

    with open(TEST_ACCOUNTS_FILE, "w") as f:
        yaml.dump(accounts_list, f, default_flow_style=False)


def configure_tempest_update_params(tempest_conf_file, image_id=None,
                                    flavor_id=None, compute_cnt=1):
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

    if image_id is not None:
        config.set('compute', 'image_ref', image_id)
    if IMAGE_ID_ALT is not None:
        config.set('compute', 'image_ref_alt', IMAGE_ID_ALT)
    if CONST.__getattribute__('tempest_use_custom_flavors'):
        if flavor_id is not None:
            config.set('compute', 'flavor_ref', flavor_id)
        if FLAVOR_ID_ALT is not None:
            config.set('compute', 'flavor_ref_alt', FLAVOR_ID_ALT)
    if compute_cnt > 1:
        # enable multinode tests
        config.set('compute', 'min_compute_nodes', compute_cnt)
        config.set('compute-feature-enabled', 'live_migration', True)

    config.set('identity', 'region', 'RegionOne')
    identity_api_version = os.getenv(
        "OS_IDENTITY_API_VERSION", os.getenv("IDENTITY_API_VERSION"))
    if (identity_api_version == '3'):
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
        if (identity_api_version == '3'):
            config.set('identity', 'v3_endpoint_type',
                       CONST.__getattribute__('OS_ENDPOINT_TYPE'))
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
