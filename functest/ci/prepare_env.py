#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import argparse
import json
import os
import re
import subprocess
import sys

import yaml
from opnfv.utils import constants as opnfv_constants

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
from functest.utils.constants import CONST

actions = ['start', 'check']

""" logging configuration """
logger = ft_logger.Logger("prepare_env").getLogger()


CONFIG_FUNCTEST_PATH = CONST.CONFIG_FUNCTEST_YAML
CONFIG_PATCH_PATH = os.path.join(os.path.dirname(
    CONFIG_FUNCTEST_PATH), "config_patch.yaml")

with open(CONFIG_PATCH_PATH) as f:
    functest_patch_yaml = yaml.safe_load(f)


class PrepareEnvParser():

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

    if CONST.INSTALLER_TYPE is None:
        logger.warning("The env variable 'INSTALLER_TYPE' is not defined.")
        CONST.INSTALLER_TYPE = "undefined"
    else:
        if CONST.INSTALLER_TYPE not in opnfv_constants.INSTALLERS:
            logger.warning("INSTALLER_TYPE=%s is not a valid OPNFV installer. "
                           "Available OPNFV Installers are : %s. "
                           "Setting INSTALLER_TYPE=undefined."
                           % (CONST.INSTALLER_TYPE,
                              opnfv_constants.INSTALLERS))
            CONST.INSTALLER_TYPE = "undefined"
        else:
            logger.info("    INSTALLER_TYPE=%s"
                        % CONST.INSTALLER_TYPE)

    if CONST.INSTALLER_IP is None:
        logger.warning("The env variable 'INSTALLER_IP' is not defined. "
                       "It is needed to fetch the OpenStack credentials. "
                       "If the credentials are not provided to the "
                       "container as a volume, please add this env variable "
                       "to the 'docker run' command.")
    else:
        logger.info("    INSTALLER_IP=%s" % CONST.INSTALLER_IP)

    if CONST.DEPLOY_SCENARIO is None:
        logger.warning("The env variable 'DEPLOY_SCENARIO' is not defined. "
                       "Setting CI_SCENARIO=undefined.")
        CONST.DEPLOY_SCENARIO = "undefined"
    else:
        logger.info("    DEPLOY_SCENARIO=%s" % CONST.DEPLOY_SCENARIO)
    if CONST.CI_DEBUG:
        logger.info("    CI_DEBUG=%s" % CONST.CI_DEBUG)

    if CONST.NODE_NAME:
        logger.info("    NODE_NAME=%s" % CONST.NODE_NAME)

    if CONST.BUILD_TAG:
        logger.info("    BUILD_TAG=%s" % CONST.BUILD_TAG)

    if CONST.IS_CI_RUN:
        logger.info("    IS_CI_RUN=%s" % CONST.IS_CI_RUN)


def create_directories():
    print_separator()
    logger.info("Creating needed directories...")
    if not os.path.exists(CONST.dir_functest_conf):
        os.makedirs(CONST.dir_functest_conf)
        logger.info("    %s created." % CONST.dir_functest_conf)
    else:
        logger.debug("   %s already exists."
                     % CONST.dir_functest_conf)

    if not os.path.exists(CONST.dir_functest_data):
        os.makedirs(CONST.dir_functest_data)
        logger.info("    %s created." % CONST.dir_functest_data)
    else:
        logger.debug("   %s already exists."
                     % CONST.dir_functest_data)


def source_rc_file():
    print_separator()
    logger.info("Fetching RC file...")

    if CONST.openstack_creds is None:
        logger.warning("The environment variable 'creds' must be set and"
                       "pointing to the local RC file. Using default: "
                       "/home/opnfv/functest/conf/openstack.creds ...")
        os.path.join(CONST.dir_functest_conf, 'openstack.creds')

    if not os.path.isfile(CONST.openstack_creds):
        logger.info("RC file not provided. "
                    "Fetching it from the installer...")
        if CONST.INSTALLER_IP is None:
            logger.error("The env variable CI_INSTALLER_IP must be provided in"
                         " order to fetch the credentials from the installer.")
            raise Exception("Missing CI_INSTALLER_IP.")
        if CONST.INSTALLER_TYPE not in opnfv_constants.INSTALLERS:
            logger.error("Cannot fetch credentials. INSTALLER_TYPE=%s is "
                         "not a valid OPNFV installer. Available "
                         "installers are : %s." %
                         (CONST.INSTALLER_TYPE,
                          opnfv_constants.INSTALLERS))
            raise Exception("Wrong INSTALLER_TYPE.")

        cmd = ("/home/opnfv/repos/releng/utils/fetch_os_creds.sh "
               "-d %s -i %s -a %s"
               % (CONST.openstack_creds,
                  CONST.INSTALLER_TYPE,
                  CONST.INSTALLER_IP))
        logger.debug("Executing command: %s" % cmd)
        p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output = p.communicate()[0]
        logger.debug("\n%s" % output)
        if p.returncode != 0:
            raise Exception("Failed to fetch credentials from installer.")
    else:
        logger.info("RC file provided in %s."
                    % CONST.openstack_creds)
        if os.path.getsize(CONST.openstack_creds) == 0:
            raise Exception("The file %s is empty." % CONST.openstack_creds)

    logger.info("Sourcing the OpenStack RC file...")
    os_utils.source_credentials(
        CONST.openstack_creds)
    for key, value in os.environ.iteritems():
        if re.search("OS_", key):
            if key == 'OS_AUTH_URL':
                CONST.OS_AUTH_URL = value
            elif key == 'OS_USERNAME':
                CONST.OS_USERNAME = value
            elif key == 'OS_TENANT_NAME':
                CONST.OS_TENANT_NAME = value
            elif key == 'OS_PASSWORD':
                CONST.OS_PASSWORD = value


def patch_config_file():
    updated = False
    for key in functest_patch_yaml:
        if key in CONST.DEPLOY_SCENARIO:
            new_functest_yaml = dict(ft_utils.merge_dicts(
                ft_utils.get_functest_yaml(), functest_patch_yaml[key]))
            updated = True

    if updated:
        os.remove(CONFIG_FUNCTEST_PATH)
        with open(CONFIG_FUNCTEST_PATH, "w") as f:
            f.write(yaml.dump(new_functest_yaml, default_style='"'))
        f.close()


def verify_deployment():
    print_separator()
    logger.info("Verifying OpenStack services...")
    cmd = ("%s/functest/ci/check_os.sh" % CONST.dir_repo_functest)

    logger.debug("Executing command: %s" % cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    while p.poll() is None:
        line = p.stdout.readline().rstrip()
        if "ERROR" in line:
            logger.error(line)
            raise Exception("Problem while running 'check_os.sh'.")
        logger.info(line)


def install_rally():
    print_separator()
    logger.info("Creating Rally environment...")

    cmd = "rally deployment destroy opnfv-rally"
    ft_utils.execute_command(cmd, error_msg=(
        "Deployment %s does not exist."
        % CONST.rally_deployment_name),
        verbose=False)

    rally_conf = os_utils.get_credentials_for_rally()
    with open('rally_conf.json', 'w') as fp:
        json.dump(rally_conf, fp)
    cmd = ("rally deployment create "
           "--file=rally_conf.json --name={0}"
           .format(CONST.rally_deployment_name))
    error_msg = "Problem while creating Rally deployment"
    ret = ft_utils.execute_command(cmd, error_msg=error_msg)
    if ret != 0:
        raise Exception(error_msg)

    cmd = "rally deployment check"
    error_msg = "OpenStack not responding or faulty Rally deployment."
    ret = ft_utils.execute_command(cmd, error_msg=error_msg)
    if ret != 0:
        raise Exception(error_msg)

    cmd = "rally deployment list"
    ft_utils.execute_command(cmd,
                             error_msg=("Problem while listing "
                                        "Rally deployment."))

    cmd = "rally plugin list | head -5"
    ft_utils.execute_command(cmd,
                             error_msg=("Problem while showing "
                                        "Rally plugins."))


def install_tempest():
    logger.info("Installing tempest from existing repo...")
    cmd = ("rally verify list-verifiers | "
           "grep '{0}' | wc -l".format(CONST.tempest_deployment_name))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    while p.poll() is None:
        line = p.stdout.readline().rstrip()
        if '0' in line:
            logger.debug("Tempest %s does not exist" %
                         CONST.tempest_deployment_name)
            cmd = ("rally verify create-verifier --source {0} "
                   "--name {1} --type tempest"
                   .format(CONST.dir_repo_tempest,
                           CONST.tempest_deployment_name))
            error_msg = "Problem while installing Tempest."
            ret = ft_utils.execute_command(cmd, error_msg=error_msg)
            if ret != 0:
                raise Exception(error_msg)


def create_flavor():
    flavor_id = os_utils.get_or_create_flavor('m1.tiny',
                                              '512',
                                              '1',
                                              '1',
                                              public=True)
    if flavor_id is None:
        raise Exception('Failed to create flavor')


def check_environment():
    msg_not_active = "The Functest environment is not installed."
    if not os.path.isfile(CONST.env_active):
        raise Exception(msg_not_active)

    with open(CONST.env_active, "r") as env_file:
        s = env_file.read()
        if not re.search("1", s):
            raise Exception(msg_not_active)

    logger.info("Functest environment is installed.")


def main(**kwargs):
    try:
        if not (kwargs['action'] in actions):
            logger.error('Argument not valid.')
            return -1
        elif kwargs['action'] == "start":
            logger.info("######### Preparing Functest environment #########\n")
            check_env_variables()
            create_directories()
            source_rc_file()
            patch_config_file()
            verify_deployment()
            install_rally()
            install_tempest()
            create_flavor()
            with open(CONST.env_active, "w") as env_file:
                env_file.write("1")
            check_environment()
        elif kwargs['action'] == "check":
            check_environment()
    except Exception as e:
        logger.error(e)
        return -1
    return 0


if __name__ == '__main__':
    parser = PrepareEnvParser()
    args = parser.parse_args(sys.argv[1:])
    sys.exit(main(**args))
