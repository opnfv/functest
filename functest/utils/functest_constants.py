#!/usr/bin/env python
#
# yaohelan@huawei.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import os
import functest.utils.functest_utils as ft_utils

import functest.utils.functest_logger as ft_logger

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
FUNCTEST_TESTCASES_YAML = os.getenv('FUNCTEST_TESTCASES_YAML')

if CI_BUILD_TAG is not None:
    IS_CI_RUN = True
else:
    IS_CI_RUN = False

CONFIG_FUNCTEST_YAML = os.getenv("CONFIG_FUNCTEST_YAML")


def get_value(functest_config_key, env_variable):
    try:
        constant = ft_utils.get_functest_config(functest_config_key)
        logger.debug("%s is defined in config_functest.yaml as [%s]"
                     % (env_variable, constant))
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


HOME = \
    get_value('general.directories.dir_home', 'HOME')
REPOS_DIR = \
    get_value('general.directories.dir_repos', 'REPOS_DIR')
FUNCTEST_BASE_DIR = \
    get_value('general.directories.dir_functest', 'FUNCTEST_BASE_DIR')
FUNCTEST_REPO_DIR = \
    get_value('general.directories.dir_repo_functest', 'FUNCTEST_REPO_DIR')
FUNCTEST_TEST_DIR = \
    get_value('general.directories.dir_functest_test', 'FUNCTEST_TEST_DIR')
FUNCTEST_CONF_DIR = \
    get_value('general.directories.dir_functest_conf', 'FUNCTEST_CONF_DIR')
FUNCTEST_DATA_DIR = \
    get_value('general.directories.dir_functest_data', 'FUNCTEST_DATA_DIR')
FUNCTEST_RESULTS_DIR = \
    get_value('general.directories.dir_results', 'FUNCTEST_RESULTS_DIR')

RALLY_DEPLOYMENT_NAME = \
    get_value('rally.deployment_name', 'RALLY_DEPLOYMENT_NAME')
TEMPEST_REPO_DIR = \
    get_value('general.directories.dir_repo_tempest', 'TEMPEST_REPO_DIR')

OPENSTACK_CREDS = \
    get_value('general.openstack.creds', 'creds')
OPENSTACK_SNAPSHOT_FILE = \
    get_value('general.openstack.snapshot_file', 'OPENSTACK_SNAPSHOT_FILE')

DOMINO_REPO = \
    get_value('general.directories.dir_repo_domino', 'DOMINO_REPO')

ONOS_SFC_IMAGE_NAME = \
    get_value('onos_sfc.image_name', 'ONOS_SFC_IMAGE_NAME')
ONOS_SFC_IMAGE_FILENAME = \
    get_value('onos_sfc.image_file_name', 'ONOS_SFC_IMAGE_FILENAME')
ONOS_SFC_RELATIVE_PATH = \
    get_value('general.directories.dir_onos_sfc', 'ONOS_SFC_RELATIVE_PATH')
ONOS_SFC_IMAGE_BASE_URL = \
    get_value('onos_sfc.image_base_url', 'ONOS_SFC_IMAGE_BASE_URL')
RALLY_RELATIVE_PATH = \
    get_value('general.directories.dir_rally', 'RALLY_RELATIVE_PATH')
RALLY_PRIVATE_NET_NAME = \
    get_value('rally.network_name', 'RALLY_PRIVATE_NET_NAME')
RALLY_PRIVATE_SUBNET_NAME = \
    get_value('rally.subnet_name', 'RALLY_PRIVATE_SUBNET_NAME')
RALLY_PRIVATE_SUBNET_CIDR = \
    get_value('rally.subnet_cidr', 'RALLY_PRIVATE_SUBNET_CIDR')
RALLY_ROUTER_NAME = \
    get_value('rally.router_name', 'RALLY_ROUTER_NAME')
RALLY_INSTALLATION_DIR = \
    get_value('general.directories.dir_rally_inst', 'RALLY_INSTALLATION_DIR')
GLANCE_IMAGE_NAME = \
    get_value('general.openstack.image_name', 'GLANCE_IMAGE_NAME')
GLANCE_IMAGE_FILENAME = \
    get_value('general.openstack.image_file_name', 'GLANCE_IMAGE_FILENAME')
GLANCE_IMAGE_FORMAT = \
    get_value('general.openstack.image_disk_format', 'GLANCE_IMAGE_FORMAT')
FLAVOR_NAME = \
    get_value('general.openstack.flavor_name', 'FLAVOR_NAME')
FLAVOR_RAM = \
    get_value('general.openstack.flavor_ram', 'FLAVOR_RAM')
FLAVOR_DISK = \
    get_value('general.openstack.flavor_disk', 'FLAVOR_DISK')
FLAVOR_VCPUS = \
    get_value('general.openstack.flavor_vcpus', 'FLAVOR_VCPUS')
TEMPEST_PRIVATE_NET_NAME = \
    get_value('tempest.private_net_name', 'TEMPEST_PRIVATE_NET_NAME')
TEMPEST_PRIVATE_SUBNET_NAME = \
    get_value('tempest.private_subnet_name', 'TEMPEST_PRIVATE_SUBNET_NAME')
TEMPEST_PRIVATE_SUBNET_CIDR = \
    get_value('tempest.private_subnet_cidr', 'TEMPEST_PRIVATE_SUBNET_CIDR')
TEMPEST_ROUTER_NAME = \
    get_value('tempest.router_name', 'TEMPEST_ROUTER_NAME')
TEMPEST_TENANT_NAME = \
    get_value('tempest.identity.tenant_name', 'TEMPEST_TENANT_NAME')
TEMPEST_TENANT_DESCRIPTION = \
    get_value('tempest.identity.tenant_description',
              'TEMPEST_TENANT_DESCRIPTION')
TEMPEST_USER_NAME = \
    get_value('tempest.identity.user_name', 'TEMPEST_USER_NAME')
TEMPEST_USER_PASSWORD = \
    get_value('tempest.identity.user_password', 'TEMPEST_USER_PASSWORD')
TEMPEST_SSH_TIMEOUT = \
    get_value('tempest.validation.ssh_timeout', 'TEMPEST_SSH_TIMEOUT')
TEMPEST_USE_CUSTOM_IMAGES = \
    get_value('tempest.use_custom_images', 'TEMPEST_USE_CUSTOM_IMAGES')
TEMPEST_USE_CUSTOM_FLAVORS = \
    get_value('tempest.use_custom_flavors', 'TEMPEST_USE_CUSTOM_FLAVORS')
TEMPEST_TEST_LIST_DIR = \
    get_value('general.directories.dir_tempest_cases', 'TEMPEST_TEST_LIST_DIR')
NAME_VM_1 = \
    get_value('vping.vm_name_1', 'NAME_VM_1')
NAME_VM_2 = \
    get_value('vping.vm_name_2', 'NAME_VM_2')
PING_TIMEOUT = \
    get_value('vping.ping_timeout', 'PING_TIMEOUT')
VPING__IMAGE_NAME = \
    get_value('vping.image_name', 'VPING__IMAGE_NAME')
VPING_VM_FLAVOR = \
    get_value('vping.vm_flavor', 'VPING_VM_FLAVOR')
VPING_PRIVATE_NET_NAME = \
    get_value('vping.vping_private_net_name', 'VPING_PRIVATE_NET_NAME')
VPING_PRIVATE_SUBNET_NAME = \
    get_value('vping.vping_private_subnet_name', 'VPING_PRIVATE_SUBNET_NAME')
VPING_PRIVATE_SUBNET_CIDR = \
    get_value('vping.vping_private_subnet_cidr', 'VPING_PRIVATE_SUBNET_CIDR')
VPING_ROUTER_NAME = \
    get_value('vping.vping_router_name', 'VPING_ROUTER_NAME')
VPING_SECGROUP_NAME = \
    get_value('vping.vping_sg_name', 'VPING_SECGROUP_NAME')
VPING_SECGROUP_DESCR = \
    get_value('vping.vping_sg_descr', 'VPING_SECGROUP_DESCR')
ONOSBENCH_USERNAME = \
    get_value('ONOS.general.onosbench_username', 'ONOSBENCH_USERNAME')
ONOSBENCH_PASSWORD = \
    get_value('ONOS.general.onosbench_password', 'ONOSBENCH_PASSWORD')
ONOSCLI_USERNAME = \
    get_value('ONOS.general.onoscli_username', 'ONOSCLI_USERNAME')
ONOSCLI_PASSWORD = \
    get_value('ONOS.general.onoscli_password', 'ONOSCLI_PASSWORD')
ONOS_RUNTIMEOUT = \
    get_value('ONOS.general.runtimeout', 'ONOS_RUNTIMEOUT')
ONOS_OCT = \
    get_value('ONOS.environment.OCT', 'ONOS_OCT')
ONOS_OC1 = \
    get_value('ONOS.environment.OC1', 'ONOS_OC1')
ONOS_OC2 = \
    get_value('ONOS.environment.OC2', 'ONOS_OC2')
ONOS_OC3 = \
    get_value('ONOS.environment.OC3', 'ONOS_OC3')
ONOS_OCN = \
    get_value('ONOS.environment.OCN', 'ONOS_OCN')
ONOS_OCN2 = \
    get_value('ONOS.environment.OCN2', 'ONOS_OCN2')
ONOS_INSTALLER_MASTER = \
    get_value('ONOS.environment.installer_master', 'ONOS_INSTALLER_MASTER')
ONOS_INSTALLER_MASTER_USERNAME = \
    get_value('ONOS.environment.installer_master_username',
              'ONOS_INSTALLER_MASTER_USERNAME')
ONOS_INSTALLER_MASTER_PASSWORD = \
    get_value('ONOS.environment.installer_master_password',
              'ONOS_INSTALLER_MASTER_PASSWORD')
PROMISE_REPO_DIR = \
    get_value('general.directories.dir_repo_promise', 'PROMISE_REPO_DIR')
PROMISE_TENANT_NAME = \
    get_value('promise.tenant_name', 'PROMISE_TENANT_NAME')
TENANT_DESCRIPTION = \
    get_value('promise.tenant_description', 'TENANT_DESCRIPTION')
PROMISE_USER_NAME = \
    get_value('promise.user_name', 'PROMISE_USER_NAME')
PROMISE_USER_PWD = \
    get_value('promise.user_pwd', 'PROMISE_USER_PWD')
PROMISE_IMAGE_NAME = \
    get_value('promise.image_name', 'PROMISE_IMAGE_NAME')
PROMISE_FLAVOR_NAME = \
    get_value('promise.flavor_name', 'PROMISE_FLAVOR_NAME')
PROMISE_FLAVOR_VCPUS = \
    get_value('promise.flavor_vcpus', 'PROMISE_FLAVOR_VCPUS')
PROMISE_FLAVOR_RAM = \
    get_value('promise.flavor_ram', 'PROMISE_FLAVOR_RAM')
PROMISE_FLAVOR_DISK = \
    get_value('promise.flavor_disk', 'PROMISE_FLAVOR_DISK')
PROMISE_NET_NAME = \
    get_value('promise.network_name', 'PROMISE_NET_NAME')
PROMISE_SUBNET_NAME = \
    get_value('promise.subnet_name', 'PROMISE_SUBNET_NAME')
PROMISE_SUBNET_CIDR = \
    get_value('promise.subnet_cidr', 'PROMISE_SUBNET_CIDR')
PROMISE_ROUTER_NAME = \
    get_value('promise.router_name', 'PROMISE_ROUTER_NAME')
DOCTOR_REPO_DIR = \
    get_value('general.directories.dir_repo_doctor', 'DOCTOR_REPO_DIR')
COPPER_REPO_DIR = \
    get_value('general.directories.dir_repo_copper', 'COPPER_REPO_DIR')
EXAMPLE_INSTANCE_NAME = \
    get_value('example.example_vm_name', 'EXAMPLE_INSTANCE_NAME')
EXAMPLE_FLAVOR = \
    get_value('example.example_flavor', 'EXAMPLE_FLAVOR')
EXAMPLE_IMAGE_NAME = \
    get_value('example.example_image_name', 'EXAMPLE_IMAGE_NAME')
EXAMPLE_PRIVATE_NET_NAME = \
    get_value('example.example_private_net_name', 'EXAMPLE_PRIVATE_NET_NAME')
EXAMPLE_PRIVATE_SUBNET_NAME = \
    get_value('example.example_private_subnet_name',
              'EXAMPLE_PRIVATE_SUBNET_NAME')
EXAMPLE_PRIVATE_SUBNET_CIDR = \
    get_value('example.example_private_subnet_cidr',
              'EXAMPLE_PRIVATE_SUBNET_CIDR')
EXAMPLE_ROUTER_NAME = \
    get_value('example.example_router_name', 'EXAMPLE_ROUTER_NAME')
EXAMPLE_SECGROUP_NAME = \
    get_value('example.example_sg_name', 'EXAMPLE_SECGROUP_NAME')
EXAMPLE_SECGROUP_DESCR = \
    get_value('example.example_sg_descr', 'EXAMPLE_SECGROUP_DESCR')
VIMS_DATA_DIR = \
    get_value('general.directories.dir_vIMS_data', 'VIMS_DATA_DIR')
VIMS_TEST_DIR = \
    get_value('general.directories.dir_repo_vims_test', 'VIMS_TEST_DIR')
VIMS_TENANT_NAME = \
    get_value('vIMS.general.tenant_name', 'VIMS_TENANT_NAME')
VIMS_TENANT_DESCRIPTION = \
    get_value('vIMS.general.tenant_description', 'VIMS_TENANT_DESCRIPTION')
VIMS_IMAGES = get_value('vIMS.general.images', 'VIMS_IMAGES')
CFY_MANAGER_BLUEPRINT = \
    get_value('vIMS.cloudify.blueprint', 'CFY_MANAGER_BLUEPRINT')
CFY_MANAGER_REQUIERMENTS = \
    get_value('vIMS.cloudify.requierments', 'CFY_MANAGER_REQUIERMENTS')
CFY_INPUTS = \
    get_value('vIMS.cloudify.inputs', 'CFY_INPUTS')
CW_BLUEPRINT = \
    get_value('vIMS.clearwater.blueprint', 'CW_BLUEPRINT')
CW_DEPLOYMENT_NAME = \
    get_value('vIMS.clearwater.deployment-name', 'CW_DEPLOYMENT_NAME')
CW_INPUTS = \
    get_value('vIMS.clearwater.inputs', 'CW_INPUTS')
CW_REQUIERMENTS = \
    get_value('vIMS.clearwater.requierments', 'CW_REQUIERMENTS')
PARSER_REPO = \
    get_value('general.directories.dir_repo_parser', 'PARSER_REPO')
