#!/usr/bin/env python
#
# yaohelan@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import os

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils

logger = ft_logger.Logger("functest_constants").getLogger()


""" global variables """
INSTALLERS = ['fuel', 'compass', 'apex', 'joid']
CI_INSTALLER_TYPE = os.getenv('INSTALLER_TYPE')
CI_INSTALLER_IP = os.getenv('INSTALLER_IP')
CI_SCENARIO = os.getenv('DEPLOY_SCENARIO')
CI_NODE = os.getenv('NODE_NAME')
CI_BUILD_TAG = os.getenv('BUILD_TAG')
CI_DEBUG = os.getenv('CI_DEBUG')
CI_LOOP = os.getenv('CI_LOOP')
OS_AUTH_URL = os.getenv('OS_AUTH_URL')
OS_USERNAME = os.getenv('OS_USERNAME')
OS_TENANT_NAME = os.getenv('OS_TENANT_NAME')
OS_PASSWORD = os.getenv('OS_PASSWORD')
OS_ENDPOINT_TYPE = os.getenv('OS_ENDPOINT_TYPE')
OS_REGION_NAME = os.getenv('OS_REGION_NAME')
OS_CACERT = os.getenv('OS_CACERT')
FUEL_ENV = os.getenv('FUEL_ENV')
SDN_CONTROLLER_IP = os.getenv('SDN_CONTROLLER_IP')
SDN_CONTROLLER = os.getenv('SDN_CONTROLLER')

if CI_BUILD_TAG is not None:
    IS_CI_RUN = True
else:
    IS_CI_RUN = False

CONFIG_FUNCTEST_YAML = os.getenv("CONFIG_FUNCTEST_YAML")


def get_value(functest_config_key, env_variable):
    try:
        constant = ft_utils.get_functest_config(functest_config_key)
        # logger.debug("%s is defined in config_functest.yaml as [%s]"
        #             % (env_variable, constant))
        return constant
    except ValueError:
        logger.warning("%s is not defined in config_functest.yaml"
                       % functest_config_key)
        constant = os.getenv(env_variable)
        if constant is None:
            raise ValueError("%s is neither defined in config_functest.yaml"
                             " nor environment variable" % env_variable)
        else:
            logger.debug("%s is defined as environment variable as [%s]"
                         % (env_variable, constant))
            return constant


HOME = get_value('general.dir.home', 'HOME')
REPOS_DIR = get_value('general.dir.repos', 'REPOS_DIR')
FUNCTEST_BASE_DIR = get_value('general.dir.functest',
                              'FUNCTEST_BASE_DIR')
FUNCTEST_REPO_DIR = get_value('general.dir.repo_functest',
                              'FUNCTEST_REPO_DIR')
FUNCTEST_TEST_DIR = get_value('general.dir.functest_test',
                              'FUNCTEST_TEST_DIR')
FUNCTEST_CONF_DIR = get_value('general.dir.functest_conf',
                              'FUNCTEST_CONF_DIR')
FUNCTEST_DATA_DIR = get_value('general.dir.functest_data',
                              'FUNCTEST_DATA_DIR')
FUNCTEST_RESULTS_DIR = get_value('general.dir.results',
                                 'FUNCTEST_RESULTS_DIR')
FUNCTEST_TESTCASES_YAML = get_value('general.functest.testcases_yaml',
                                    'FUNCTEST_TESTCASES_YAML')
RALLY_DEPLOYMENT_NAME = get_value('rally.deployment_name',
                                  'RALLY_DEPLOYMENT_NAME')
TEMPEST_REPO_DIR = get_value('general.dir.repo_tempest',
                             'TEMPEST_REPO_DIR')

ENV_FILE = os.path.join(FUNCTEST_CONF_DIR, "env_active")

OPENSTACK_CREDS = get_value('general.openstack.creds', 'creds')
OPENSTACK_SNAPSHOT_FILE = get_value('general.openstack.snapshot_file',
                                    'OPENSTACK_SNAPSHOT_FILE')

DOMINO_REPO_DIR = get_value('general.dir.repo_domino',
                            'DOMINO_REPO_DIR')
SDNVPN_REPO_DIR = get_value('general.dir.repo_sdnvpn',
                            'SDNVPN_REPO_DIR')
SFC_REPO_DIR = get_value('general.dir.repo_sfc',
                         'SFC_REPO_DIR')
RALLY_RELATIVE_PATH = get_value('general.dir.rally',
                                'RALLY_RELATIVE_PATH')
RALLY_PRIVATE_NET_NAME = get_value('rally.network_name',
                                   'RALLY_PRIVATE_NET_NAME')
RALLY_PRIVATE_SUBNET_NAME = get_value('rally.subnet_name',
                                      'RALLY_PRIVATE_SUBNET_NAME')
RALLY_PRIVATE_SUBNET_CIDR = get_value('rally.subnet_cidr',
                                      'RALLY_PRIVATE_SUBNET_CIDR')
RALLY_ROUTER_NAME = get_value('rally.router_name', 'RALLY_ROUTER_NAME')
RALLY_INSTALLATION_DIR = get_value('general.dir.rally_inst',
                                   'RALLY_INSTALLATION_DIR')
GLANCE_IMAGE_NAME = get_value('general.openstack.image_name',
                              'GLANCE_IMAGE_NAME')
GLANCE_IMAGE_FILENAME = get_value('general.openstack.image_file_name',
                                  'GLANCE_IMAGE_FILENAME')
GLANCE_IMAGE_FORMAT = get_value('general.openstack.image_disk_format',
                                'GLANCE_IMAGE_FORMAT')
GLANCE_IMAGE_HW_FIRMWARE_TYPE = get_value(
                                'general.openstack.image_hw_firmware_type',
                                'GLANCE_IMAGE_HW_FIRMWARE_TYPE')
GLANCE_IMAGE_SHORT_ID = get_value('general.openstack.image_short_id',
                                'GLANCE_IMAGE_SHORT_ID')
FLAVOR_NAME = get_value('general.openstack.flavor_name',
                        'FLAVOR_NAME')
FLAVOR_RAM = get_value('general.openstack.flavor_ram',
                       'FLAVOR_RAM')
FLAVOR_DISK = get_value('general.openstack.flavor_disk',
                        'FLAVOR_DISK')
FLAVOR_VCPUS = get_value('general.openstack.flavor_vcpus',
                         'FLAVOR_VCPUS')
TEMPEST_PRIVATE_NET_NAME = get_value('tempest.private_net_name',
                                     'TEMPEST_PRIVATE_NET_NAME')
TEMPEST_PRIVATE_SUBNET_NAME = get_value('tempest.private_subnet_name',
                                        'TEMPEST_PRIVATE_SUBNET_NAME')
TEMPEST_PRIVATE_SUBNET_CIDR = get_value('tempest.private_subnet_cidr',
                                        'TEMPEST_PRIVATE_SUBNET_CIDR')
TEMPEST_ROUTER_NAME = get_value('tempest.router_name',
                                'TEMPEST_ROUTER_NAME')
TEMPEST_TENANT_NAME = get_value('tempest.identity.tenant_name',
                                'TEMPEST_TENANT_NAME')
TEMPEST_TENANT_DESCRIPTION = get_value('tempest.identity.tenant_description',
                                       'TEMPEST_TENANT_DESCRIPTION')
TEMPEST_USER_NAME = get_value('tempest.identity.user_name',
                              'TEMPEST_USER_NAME')
TEMPEST_USER_PASSWORD = get_value('tempest.identity.user_password',
                                  'TEMPEST_USER_PASSWORD')
TEMPEST_SSH_TIMEOUT = get_value('tempest.validation.ssh_timeout',
                                'TEMPEST_SSH_TIMEOUT')
TEMPEST_OPERATOR_ROLE = get_value('tempest.object_storage.operator_role',
                                  'TEMPEST_OPERATOR_ROLE')
TEMPEST_USE_CUSTOM_IMAGES = get_value('tempest.use_custom_images',
                                      'TEMPEST_USE_CUSTOM_IMAGES')
TEMPEST_USE_CUSTOM_FLAVORS = get_value('tempest.use_custom_flavors',
                                       'TEMPEST_USE_CUSTOM_FLAVORS')
TEMPEST_TEST_LIST_DIR = get_value('general.dir.tempest_cases',
                                  'TEMPEST_TEST_LIST_DIR')
NAME_VM_1 = get_value('vping.vm_name_1', 'NAME_VM_1')
NAME_VM_2 = get_value('vping.vm_name_2', 'NAME_VM_2')
PING_TIMEOUT = get_value('vping.ping_timeout', 'PING_TIMEOUT')
VPING__IMAGE_NAME = get_value('vping.image_name', 'VPING__IMAGE_NAME')
VPING_VM_FLAVOR = get_value('vping.vm_flavor', 'VPING_VM_FLAVOR')
VPING_PRIVATE_NET_NAME = get_value('vping.private_net_name',
                                   'VPING_PRIVATE_NET_NAME')
VPING_PRIVATE_SUBNET_NAME = get_value('vping.private_subnet_name',
                                      'VPING_PRIVATE_SUBNET_NAME')
VPING_PRIVATE_SUBNET_CIDR = get_value('vping.private_subnet_cidr',
                                      'VPING_PRIVATE_SUBNET_CIDR')
VPING_ROUTER_NAME = get_value('vping.router_name',
                              'VPING_ROUTER_NAME')
VPING_SECGROUP_NAME = get_value('vping.sg_name',
                                'VPING_SECGROUP_NAME')
VPING_SECGROUP_DESCR = get_value('vping.sg_desc',
                                 'VPING_SECGROUP_DESCR')
ONOSBENCH_USERNAME = get_value('ONOS.general.onosbench_username',
                               'ONOSBENCH_USERNAME')
ONOSBENCH_PASSWORD = get_value('ONOS.general.onosbench_password',
                               'ONOSBENCH_PASSWORD')
ONOSCLI_USERNAME = get_value('ONOS.general.onoscli_username',
                             'ONOSCLI_USERNAME')
ONOSCLI_PASSWORD = get_value('ONOS.general.onoscli_password',
                             'ONOSCLI_PASSWORD')
ONOS_RUNTIMEOUT = get_value('ONOS.general.runtimeout',
                            'ONOS_RUNTIMEOUT')
ONOS_OCT = get_value('ONOS.environment.OCT', 'ONOS_OCT')
ONOS_OC1 = get_value('ONOS.environment.OC1', 'ONOS_OC1')
ONOS_OC2 = get_value('ONOS.environment.OC2', 'ONOS_OC2')
ONOS_OC3 = get_value('ONOS.environment.OC3', 'ONOS_OC3')
ONOS_OCN = get_value('ONOS.environment.OCN', 'ONOS_OCN')
ONOS_OCN2 = get_value('ONOS.environment.OCN2', 'ONOS_OCN2')
ONOS_INSTALLER_MASTER = get_value('ONOS.environment.installer_master',
                                  'ONOS_INSTALLER_MASTER')
ONOS_INSTALLER_MASTER_USERNAME = get_value(
    'ONOS.environment.installer_master_username',
    'ONOS_INSTALLER_MASTER_USERNAME')
ONOS_INSTALLER_MASTER_PASSWORD = get_value(
    'ONOS.environment.installer_master_password',
    'ONOS_INSTALLER_MASTER_PASSWORD')
EXAMPLE_INSTANCE_NAME = get_value('example.vm_name',
                                  'EXAMPLE_INSTANCE_NAME')
EXAMPLE_FLAVOR = get_value('example.flavor', 'EXAMPLE_FLAVOR')
EXAMPLE_IMAGE_NAME = get_value('example.image_name',
                               'EXAMPLE_IMAGE_NAME')
EXAMPLE_PRIVATE_NET_NAME = get_value('example.private_net_name',
                                     'EXAMPLE_PRIVATE_NET_NAME')
EXAMPLE_PRIVATE_SUBNET_NAME = get_value(
    'example.private_subnet_name',
    'EXAMPLE_PRIVATE_SUBNET_NAME')
EXAMPLE_PRIVATE_SUBNET_CIDR = get_value(
    'example.private_subnet_cidr',
    'EXAMPLE_PRIVATE_SUBNET_CIDR')
EXAMPLE_ROUTER_NAME = get_value('example.router_name',
                                'EXAMPLE_ROUTER_NAME')
EXAMPLE_SECGROUP_NAME = get_value('example.sg_name',
                                  'EXAMPLE_SECGROUP_NAME')
EXAMPLE_SECGROUP_DESCR = get_value('example.sg_desc',
                                   'EXAMPLE_SECGROUP_DESCR')
PARSER_REPO_DIR = get_value('general.dir.repo_parser',
                            'PARSER_REPO_DIR')
