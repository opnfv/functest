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

from __future__ import print_function

import logging
import fileinput
import os
import subprocess

import pkg_resources
from six.moves import configparser
import yaml

from functest.utils import config
from functest.utils import env


RALLY_CONF_PATH = "/etc/rally/rally.conf"
RALLY_AARCH64_PATCH_PATH = pkg_resources.resource_filename(
    'functest', 'ci/rally_aarch64_patch.conf')
GLANCE_IMAGE_PATH = os.path.join(
    getattr(config.CONF, 'dir_functest_images'),
    getattr(config.CONF, 'openstack_image_file_name'))
TEMPEST_CUSTOM = pkg_resources.resource_filename(
    'functest', 'opnfv_tests/openstack/tempest/custom_tests/test_list.txt')
TEMPEST_BLACKLIST = pkg_resources.resource_filename(
    'functest', 'opnfv_tests/openstack/tempest/custom_tests/blacklist.txt')
TEMPEST_CONF_YAML = pkg_resources.resource_filename(
    'functest', 'opnfv_tests/openstack/tempest/custom_tests/tempest_conf.yaml')

CI_INSTALLER_TYPE = env.get('INSTALLER_TYPE')

""" logging configuration """
LOGGER = logging.getLogger(__name__)


def create_rally_deployment(environ=None):
    """Create new rally deployment"""
    # set the architecture to default
    pod_arch = env.get("POD_ARCH")
    arch_filter = ['aarch64']

    if pod_arch and pod_arch in arch_filter:
        LOGGER.info("Apply aarch64 specific to rally config...")
        with open(RALLY_AARCH64_PATCH_PATH, "r") as pfile:
            rally_patch_conf = pfile.read()

        for line in fileinput.input(RALLY_CONF_PATH, inplace=1):
            print(line, end=' ')
            if "cirros|testvm" in line:
                print(rally_patch_conf)

    LOGGER.info("Creating Rally environment...")

    try:
        cmd = ['rally', 'deployment', 'destroy',
               '--deployment',
               str(getattr(config.CONF, 'rally_deployment_name'))]
        output = subprocess.check_output(cmd)
        LOGGER.info("%s\n%s", " ".join(cmd), output)
    except subprocess.CalledProcessError:
        pass

    cmd = ['rally', 'deployment', 'create', '--fromenv',
           '--name', str(getattr(config.CONF, 'rally_deployment_name'))]
    output = subprocess.check_output(cmd, env=environ)
    LOGGER.info("%s\n%s", " ".join(cmd), output)

    cmd = ['rally', 'deployment', 'check']
    output = subprocess.check_output(cmd)
    LOGGER.info("%s\n%s", " ".join(cmd), output)


def create_verifier():
    """Create new verifier"""
    LOGGER.info("Create verifier from existing repo...")
    cmd = ['rally', 'verify', 'delete-verifier',
           '--id', str(getattr(config.CONF, 'tempest_verifier_name')),
           '--force']
    try:
        output = subprocess.check_output(cmd)
        LOGGER.info("%s\n%s", " ".join(cmd), output)
    except subprocess.CalledProcessError:
        pass

    cmd = ['rally', 'verify', 'create-verifier',
           '--source', str(getattr(config.CONF, 'dir_repo_tempest')),
           '--name', str(getattr(config.CONF, 'tempest_verifier_name')),
           '--type', 'tempest', '--system-wide']
    output = subprocess.check_output(cmd)
    LOGGER.info("%s\n%s", " ".join(cmd), output)


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


def configure_tempest_update_params(
        tempest_conf_file, network_name=None, image_id=None, flavor_id=None,
        compute_cnt=1, image_alt_id=None, flavor_alt_id=None):
    # pylint: disable=too-many-branches, too-many-arguments
    """
    Add/update needed parameters into tempest.conf file
    """
    LOGGER.debug("Updating selected tempest.conf parameters...")
    rconfig = configparser.RawConfigParser()
    rconfig.read(tempest_conf_file)
    rconfig.set('compute', 'fixed_network_name', network_name)
    rconfig.set('compute', 'volume_device_name', env.get('VOLUME_DEVICE_NAME'))
    if image_id is not None:
        rconfig.set('compute', 'image_ref', image_id)
    if image_alt_id is not None:
        rconfig.set('compute', 'image_ref_alt', image_alt_id)
    if flavor_id is not None:
        rconfig.set('compute', 'flavor_ref', flavor_id)
    if flavor_alt_id is not None:
        rconfig.set('compute', 'flavor_ref_alt', flavor_alt_id)
    if compute_cnt > 1:
        # enable multinode tests
        rconfig.set('compute', 'min_compute_nodes', compute_cnt)
        rconfig.set('compute-feature-enabled', 'live_migration', True)
    if os.environ.get('OS_REGION_NAME'):
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

    rconfig.set(
        'identity', 'v3_endpoint_type',
        os.environ.get('OS_INTERFACE', 'public'))

    sections = rconfig.sections()
    services_list = [
        'compute', 'volume', 'image', 'network', 'data-processing',
        'object-storage', 'orchestration']
    for service in services_list:
        if service not in sections:
            rconfig.add_section(service)
        rconfig.set(
            service, 'endpoint_type', os.environ.get('OS_INTERFACE', 'public'))

    LOGGER.debug('Add/Update required params defined in tempest_conf.yaml '
                 'into tempest.conf file')
    update_tempest_conf_file(tempest_conf_file, rconfig)


def configure_verifier(deployment_dir):
    """
    Execute rally verify configure-verifier, which generates tempest.conf
    """
    cmd = ['rally', 'verify', 'configure-verifier', '--reconfigure',
           '--id', str(getattr(config.CONF, 'tempest_verifier_name'))]
    output = subprocess.check_output(cmd)
    LOGGER.info("%s\n%s", " ".join(cmd), output)

    LOGGER.debug("Looking for tempest.conf file...")
    tempest_conf_file = os.path.join(deployment_dir, "tempest.conf")
    if not os.path.isfile(tempest_conf_file):
        LOGGER.error("Tempest configuration file %s NOT found.",
                     tempest_conf_file)
        raise Exception("Tempest configuration file %s NOT found."
                        % tempest_conf_file)
    else:
        return tempest_conf_file
