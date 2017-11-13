#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import argparse
import json
import logging
import logging.config
import os
import pkg_resources
import re
import subprocess
import sys

import yaml

from functest.ci import check_deployment
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
from functest.utils.constants import CONST

from opnfv.utils import constants as opnfv_constants
from opnfv.deployment import factory

actions = ['start', 'check']

""" logging configuration """
logger = logging.getLogger('functest.ci.prepare_env')
handler = None
# set the architecture to default
pod_arch = os.getenv("POD_ARCH", None)
arch_filter = ['aarch64']

CONFIG_FUNCTEST_PATH = pkg_resources.resource_filename(
    'functest', 'ci/config_functest.yaml')
CONFIG_PATCH_PATH = pkg_resources.resource_filename(
    'functest', 'ci/config_patch.yaml')
CONFIG_AARCH64_PATCH_PATH = pkg_resources.resource_filename(
    'functest', 'ci/config_aarch64_patch.yaml')


class PrepareEnvParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("action", help="Possible actions are: "
                                 "'{d[0]}|{d[1]}' ".format(d=actions),
                                 choices=actions)
        self.parser.add_argument("-d", "--debug", help="Debug mode",
                                 action="store_true")

    def parse_args(self, argv=[]):
        return vars(self.parser.parse_args(argv))


def print_separator():
    logger.info("==============================================")


def check_env_variables():
    print_separator()
    logger.info("Checking environment variables...")

    if CONST.__getattribute__('INSTALLER_TYPE') is None:
        logger.warning("The env variable 'INSTALLER_TYPE' is not defined.")
        CONST.__setattr__('INSTALLER_TYPE', 'undefined')
    else:
        if (CONST.__getattribute__('INSTALLER_TYPE') not in
                opnfv_constants.INSTALLERS):
            logger.warning("INSTALLER_TYPE=%s is not a valid OPNFV installer. "
                           "Available OPNFV Installers are : %s. "
                           "Setting INSTALLER_TYPE=undefined."
                           % (CONST.__getattribute__('INSTALLER_TYPE'),
                              opnfv_constants.INSTALLERS))
            CONST.__setattr__('INSTALLER_TYPE', 'undefined')
        else:
            logger.info("    INSTALLER_TYPE=%s"
                        % CONST.__getattribute__('INSTALLER_TYPE'))

    if CONST.__getattribute__('INSTALLER_IP') is None:
        logger.warning(
            "The env variable 'INSTALLER_IP' is not defined. It is recommended"
            " to extract some information from the deployment")
    else:
        logger.info("    INSTALLER_IP=%s" %
                    CONST.__getattribute__('INSTALLER_IP'))

    if CONST.__getattribute__('DEPLOY_SCENARIO') is None:
        logger.warning("The env variable 'DEPLOY_SCENARIO' is not defined. "
                       "Setting CI_SCENARIO=undefined.")
        CONST.__setattr__('DEPLOY_SCENARIO', 'undefined')
    else:
        logger.info("    DEPLOY_SCENARIO=%s"
                    % CONST.__getattribute__('DEPLOY_SCENARIO'))
    if CONST.__getattribute__('CI_DEBUG'):
        logger.info("    CI_DEBUG=%s" % CONST.__getattribute__('CI_DEBUG'))

    if CONST.__getattribute__('NODE_NAME'):
        logger.info("    NODE_NAME=%s" % CONST.__getattribute__('NODE_NAME'))

    if CONST.__getattribute__('BUILD_TAG'):
        logger.info("    BUILD_TAG=%s" % CONST.__getattribute__('BUILD_TAG'))

    if CONST.__getattribute__('IS_CI_RUN'):
        logger.info("    IS_CI_RUN=%s" % CONST.__getattribute__('IS_CI_RUN'))


def get_deployment_handler():
    global handler
    global pod_arch

    installer_params_yaml = pkg_resources.resource_filename(
            'functest', 'ci/installer_params.yaml')
    if (CONST.__getattribute__('INSTALLER_IP') and
        CONST.__getattribute__('INSTALLER_TYPE') and
            CONST.__getattribute__('INSTALLER_TYPE') in
            opnfv_constants.INSTALLERS):
        try:
            installer_params = ft_utils.get_parameter_from_yaml(
                CONST.__getattribute__('INSTALLER_TYPE'),
                installer_params_yaml)
        except ValueError as e:
            logger.debug('Printing deployment info is not supported for %s' %
                         CONST.__getattribute__('INSTALLER_TYPE'))
            logger.debug(e)
        else:
            user = installer_params.get('user', None)
            password = installer_params.get('password', None)
            pkey = installer_params.get('pkey', None)
            try:
                handler = factory.Factory.get_handler(
                    installer=CONST.__getattribute__('INSTALLER_TYPE'),
                    installer_ip=CONST.__getattribute__('INSTALLER_IP'),
                    installer_user=user,
                    installer_pwd=password,
                    pkey_file=pkey)
                if handler:
                    pod_arch = handler.get_arch()
            except Exception as e:
                logger.debug("Cannot get deployment information. %s" % e)


def create_directories():
    print_separator()
    logger.info("Creating needed directories...")
    if not os.path.exists(CONST.__getattribute__('dir_functest_conf')):
        os.makedirs(CONST.__getattribute__('dir_functest_conf'))
        logger.info("    %s created." %
                    CONST.__getattribute__('dir_functest_conf'))
    else:
        logger.debug("   %s already exists." %
                     CONST.__getattribute__('dir_functest_conf'))

    if not os.path.exists(CONST.__getattribute__('dir_functest_data')):
        os.makedirs(CONST.__getattribute__('dir_functest_data'))
        logger.info("    %s created." %
                    CONST.__getattribute__('dir_functest_data'))
    else:
        logger.debug("   %s already exists." %
                     CONST.__getattribute__('dir_functest_data'))
    if not os.path.exists(CONST.__getattribute__('dir_functest_images')):
        os.makedirs(CONST.__getattribute__('dir_functest_images'))
        logger.info("    %s created." %
                    CONST.__getattribute__('dir_functest_images'))
    else:
        logger.debug("   %s already exists." %
                     CONST.__getattribute__('dir_functest_images'))


def source_rc_file():
    print_separator()

    logger.info("Sourcing the OpenStack RC file...")
    os_utils.source_credentials(CONST.__getattribute__('openstack_creds'))
    for key, value in os.environ.iteritems():
        if re.search("OS_", key):
            if key == 'OS_AUTH_URL':
                CONST.__setattr__('OS_AUTH_URL', value)
            elif key == 'OS_USERNAME':
                CONST.__setattr__('OS_USERNAME', value)
            elif key == 'OS_TENANT_NAME':
                CONST.__setattr__('OS_TENANT_NAME', value)
            elif key == 'OS_PASSWORD':
                CONST.__setattr__('OS_PASSWORD', value)


def update_config_file():
    patch_file(CONFIG_PATCH_PATH)

    if pod_arch and pod_arch in arch_filter:
        patch_file(CONFIG_AARCH64_PATCH_PATH)

    if "TEST_DB_URL" in os.environ:
        update_db_url()


def patch_file(patch_file_path):
    logger.debug('Updating file: %s', patch_file_path)
    with open(patch_file_path) as f:
        patch_file = yaml.safe_load(f)

    updated = False
    for key in patch_file:
        if key in CONST.__getattribute__('DEPLOY_SCENARIO'):
            new_functest_yaml = dict(ft_utils.merge_dicts(
                ft_utils.get_functest_yaml(), patch_file[key]))
            updated = True

    if updated:
        os.remove(CONFIG_FUNCTEST_PATH)
        with open(CONFIG_FUNCTEST_PATH, "w") as f:
            f.write(yaml.dump(new_functest_yaml, default_style='"'))


def update_db_url():
    with open(CONFIG_FUNCTEST_PATH) as f:
        functest_yaml = yaml.safe_load(f)

    with open(CONFIG_FUNCTEST_PATH, "w") as f:
        functest_yaml["results"]["test_db_url"] = os.environ.get('TEST_DB_URL')
        f.write(yaml.dump(functest_yaml, default_style='"'))


def verify_deployment():
    print_separator()
    logger.info("Verifying OpenStack deployment...")
    deployment = check_deployment.CheckDeployment()
    deployment.check_all()


def create_flavor():
    _, flavor_id = os_utils.get_or_create_flavor('m1.tiny',
                                                 '512',
                                                 '1',
                                                 '1',
                                                 public=True)
    if flavor_id is None:
        raise Exception('Failed to create flavor')


def check_environment():
    msg_not_active = "The Functest environment is not installed."
    if not os.path.isfile(CONST.__getattribute__('env_active')):
        raise Exception(msg_not_active)

    with open(CONST.__getattribute__('env_active'), "r") as env_file:
        s = env_file.read()
        if not re.search("1", s):
            raise Exception(msg_not_active)

    logger.info("Functest environment is installed.")


def print_deployment_info():
    if handler:
        logger.info('\n\nDeployment information:\n%s' %
                    handler.get_deployment_info())


def prepare_env(**kwargs):
    try:
        if not (kwargs['action'] in actions):
            logger.error('Argument not valid.')
            return -1
        elif kwargs['action'] == "start":
            logger.info("######### Preparing Functest environment #########\n")
            verify_deployment()
            check_env_variables()
            create_directories()
            source_rc_file()
            update_config_file()
            create_flavor()
            with open(CONST.__getattribute__('env_active'), "w") as env_file:
                env_file.write("1")
            check_environment()
        elif kwargs['action'] == "check":
            check_environment()
    except Exception as e:
        logger.error(e)
        return -1
    return 0


def main():
    logging.config.fileConfig(pkg_resources.resource_filename(
        'functest', 'ci/logging.ini'))
    logging.captureWarnings(True)
    parser = PrepareEnvParser()
    args = parser.parse_args(sys.argv[1:])
    return prepare_env(**args)
