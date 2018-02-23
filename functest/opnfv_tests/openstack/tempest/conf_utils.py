#!/usr/bin/env python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#

"""Tempest configuration utilities."""

import ConfigParser
import logging
import fileinput
import os
import shutil
import subprocess

import pkg_resources
import yaml

from functest.utils import config
from functest.utils import env
import functest.utils.functest_utils as ft_utils


IMAGE_ID_ALT = None
FLAVOR_ID_ALT = None
RALLY_CONF_PATH = "/etc/rally/rally.conf"
RALLY_AARCH64_PATCH_PATH = pkg_resources.resource_filename(
    'functest', 'ci/rally_aarch64_patch.conf')
GLANCE_IMAGE_PATH = os.path.join(
    getattr(config.CONF, 'dir_functest_images'),
    getattr(config.CONF, 'openstack_image_file_name'))
TEMPEST_RESULTS_DIR = os.path.join(
    getattr(config.CONF, 'dir_results'), 'tempest')
TEMPEST_CUSTOM = pkg_resources.resource_filename(
    'functest', 'opnfv_tests/openstack/tempest/custom_tests/test_list.txt')
TEMPEST_BLACKLIST = pkg_resources.resource_filename(
    'functest', 'opnfv_tests/openstack/tempest/custom_tests/blacklist.txt')
# NEW test case list - pkaralis
TEMPEST_NEUTRON = pkg_resources.resource_filename(
    'functest',
    'opnfv_tests/openstack/tempest/custom_tests/neutron_trunk_req.txt')
TEMPEST_RAW_LIST = os.path.join(TEMPEST_RESULTS_DIR, 'test_raw_list.txt')
TEMPEST_LIST = os.path.join(TEMPEST_RESULTS_DIR, 'test_list.txt')
TEMPEST_CONF_YAML = pkg_resources.resource_filename(
    'functest', 'opnfv_tests/openstack/tempest/custom_tests/tempest_conf.yaml')
TEST_ACCOUNTS_FILE = pkg_resources.resource_filename(
    'functest',
    'opnfv_tests/openstack/tempest/custom_tests/test_accounts.yaml')

CI_INSTALLER_TYPE = env.get('INSTALLER_TYPE')

""" logging configuration """
LOGGER = logging.getLogger(__name__)


def create_rally_deployment():
    """Create new rally deployment"""
    # set the architecture to default
    pod_arch = env.get("POD_ARCH")
    arch_filter = ['aarch64']

    if pod_arch and pod_arch in arch_filter:
        LOGGER.info("Apply aarch64 specific to rally config...")
        with open(RALLY_AARCH64_PATCH_PATH, "r") as pfile:
            rally_patch_conf = pfile.read()

        for line in fileinput.input(RALLY_CONF_PATH, inplace=1):
            print line,
            if "cirros|testvm" in line:
                print rally_patch_conf

    LOGGER.info("Creating Rally environment...")

    cmd = "rally deployment destroy opnfv-rally"
    ft_utils.execute_command(cmd, error_msg=(
        "Deployment %s does not exist."
        % getattr(config.CONF, 'rally_deployment_name')), verbose=False)

    cmd = ("rally deployment create --fromenv --name={0}"
           .format(getattr(config.CONF, 'rally_deployment_name')))
    error_msg = "Problem while creating Rally deployment"
    ft_utils.execute_command_raise(cmd, error_msg=error_msg)

    cmd = "rally deployment check"
    error_msg = "OpenStack not responding or faulty Rally deployment."
    ft_utils.execute_command_raise(cmd, error_msg=error_msg)


def create_verifier():
    """Create new verifier"""
    LOGGER.info("Create verifier from existing repo...")
    cmd = ("rally verify delete-verifier --id '{0}' --force").format(
        getattr(config.CONF, 'tempest_verifier_name'))
    ft_utils.execute_command(cmd, error_msg=(
        "Verifier %s does not exist."
        % getattr(config.CONF, 'tempest_verifier_name')),
                             verbose=False)
    cmd = ("rally verify create-verifier --source {0} "
           "--name {1} --type tempest --system-wide"
           .format(getattr(config.CONF, 'dir_repo_tempest'),
                   getattr(config.CONF, 'tempest_verifier_name')))
    ft_utils.execute_command_raise(cmd,
                                   error_msg='Problem while creating verifier')


def get_verifier_id():
    """
    Returns verifier id for current Tempest
    """
    create_rally_deployment()
    create_verifier()
    cmd = ("rally verify list-verifiers | awk '/" +
           getattr(config.CONF, 'tempest_verifier_name') +
           "/ {print $2}'")
    proc = subprocess.Popen(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    deployment_uuid = proc.stdout.readline().rstrip()
    if deployment_uuid == "":
        LOGGER.error("Tempest verifier not found.")
        raise Exception('Error with command:%s' % cmd)
    return deployment_uuid


def get_verifier_deployment_id():
    """
    Returns deployment id for active Rally deployment
    """
    cmd = ("rally deployment list | awk '/" +
           getattr(config.CONF, 'rally_deployment_name') +
           "/ {print $2}'")
    proc = subprocess.Popen(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    deployment_uuid = proc.stdout.readline().rstrip()
    if deployment_uuid == "":
        LOGGER.error("Rally deployment not found.")
        raise Exception('Error with command:%s' % cmd)
    return deployment_uuid


def get_verifier_repo_dir(verifier_id):
    """
    Returns installed verifier repo directory for Tempest
    """
    if not verifier_id:
        verifier_id = get_verifier_id()

    return os.path.join(getattr(config.CONF, 'dir_rally_inst'),
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

    return os.path.join(getattr(config.CONF, 'dir_rally_inst'),
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


def configure_tempest(deployment_dir, network_name=None, image_id=None,
                      flavor_id=None, compute_cnt=None):
    """
    Calls rally verify and updates the generated tempest.conf with
    given parameters
    """
    conf_file = configure_verifier(deployment_dir)
    configure_tempest_update_params(conf_file, network_name, image_id,
                                    flavor_id, compute_cnt)


def generate_test_accounts_file(tenant_id):
    """
    Add needed tenant and user params into test_accounts.yaml
    """

    LOGGER.debug("Add needed params into test_accounts.yaml...")
    accounts_list = [
        {
            'tenant_name': getattr(
                config.CONF, 'tempest_identity_tenant_name'),
            'tenant_id': str(tenant_id),
            'username': getattr(config.CONF, 'tempest_identity_user_name'),
            'password': getattr(config.CONF, 'tempest_identity_user_password')
        }
    ]

    with open(TEST_ACCOUNTS_FILE, "w") as tfile:
        yaml.dump(accounts_list, tfile, default_flow_style=False)


def update_tempest_conf_file(conf_file, rconfig):
    """Update defined paramters into tempest config file"""
    with open(TEMPEST_CONF_YAML) as yfile:
        conf_yaml = yaml.safe_load(yfile)
    if conf_yaml:
        sections = rconfig.sections()
        for section in conf_yaml:
            if section not in sections:
                rconfig.add_section(section)
            sub_conf = conf_yaml.get(section)
            for key, value in sub_conf.items():
                rconfig.set(section, key, value)

    with open(conf_file, 'wb') as config_file:
        rconfig.write(config_file)


def configure_tempest_update_params(tempest_conf_file, network_name=None,
                                    image_id=None, flavor_id=None,
                                    compute_cnt=1):
    """
    Add/update needed parameters into tempest.conf file
    """
    LOGGER.debug("Updating selected tempest.conf parameters...")
    rconfig = ConfigParser.RawConfigParser()
    rconfig.read(tempest_conf_file)
    rconfig.set('compute', 'fixed_network_name', network_name)
    rconfig.set('compute', 'volume_device_name',
                getattr(config.CONF, 'tempest_volume_device_name'))

    if image_id is not None:
        rconfig.set('compute', 'image_ref', image_id)
    if IMAGE_ID_ALT is not None:
        rconfig.set('compute', 'image_ref_alt', IMAGE_ID_ALT)
    if getattr(config.CONF, 'tempest_use_custom_flavors'):
        if flavor_id is not None:
            rconfig.set('compute', 'flavor_ref', flavor_id)
        if FLAVOR_ID_ALT is not None:
            rconfig.set('compute', 'flavor_ref_alt', FLAVOR_ID_ALT)
    if compute_cnt > 1:
        # enable multinode tests
        rconfig.set('compute', 'min_compute_nodes', compute_cnt)
        rconfig.set('compute-feature-enabled', 'live_migration', True)

    rconfig.set('identity', 'region', os.environ.get('OS_REGION_NAME'))
    identity_api_version = os.environ.get("OS_IDENTITY_API_VERSION", '3')
    if identity_api_version == '3':
        auth_version = 'v3'
        rconfig.set('identity-feature-enabled', 'api_v2', False)
    else:
        auth_version = 'v2'
    rconfig.set('identity', 'auth_version', auth_version)
    rconfig.set(
        'validation', 'ssh_timeout',
        getattr(config.CONF, 'tempest_validation_ssh_timeout'))
    rconfig.set('object-storage', 'operator_role',
                getattr(config.CONF, 'tempest_object_storage_operator_role'))

    if os.environ.get('OS_ENDPOINT_TYPE') is not None:
        rconfig.set('identity', 'v3_endpoint_type',
                    os.environ.get('OS_ENDPOINT_TYPE'))

    if os.environ.get('OS_ENDPOINT_TYPE') is not None:
        sections = rconfig.sections()
        services_list = [
            'compute', 'volume', 'image', 'network', 'data-processing',
            'object-storage', 'orchestration']
        for service in services_list:
            if service not in sections:
                rconfig.add_section(service)
            rconfig.set(service, 'endpoint_type',
                        os.environ.get('OS_ENDPOINT_TYPE'))

    LOGGER.debug('Add/Update required params defined in tempest_conf.yaml '
                 'into tempest.conf file')
    update_tempest_conf_file(tempest_conf_file, rconfig)

    backup_tempest_config(tempest_conf_file)


def configure_verifier(deployment_dir):
    """
    Execute rally verify configure-verifier, which generates tempest.conf
    """
    tempest_conf_file = os.path.join(deployment_dir, "tempest.conf")
    if os.path.isfile(tempest_conf_file):
        LOGGER.debug("Verifier is already configured.")
        LOGGER.debug("Reconfiguring the current verifier...")
        cmd = "rally verify configure-verifier --reconfigure"
    else:
        LOGGER.info("Configuring the verifier...")
        cmd = "rally verify configure-verifier"
    ft_utils.execute_command(cmd)

    LOGGER.debug("Looking for tempest.conf file...")
    if not os.path.isfile(tempest_conf_file):
        LOGGER.error("Tempest configuration file %s NOT found.",
                     tempest_conf_file)
        raise Exception("Tempest configuration file %s NOT found."
                        % tempest_conf_file)
    else:
        return tempest_conf_file
