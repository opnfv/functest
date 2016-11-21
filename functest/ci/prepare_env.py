#!/usr/bin/env python
#
# Author: Jose Lausuch (jose.lausuch@ericsson.com)
#
# Installs the Functest framework within the Docker container
# and run the tests automatically
#
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#


import json
import os
import re
import subprocess
import sys

import argparse
import yaml

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
import functest.utils.functest_constants as ft_constants

actions = ['start', 'check']
parser = argparse.ArgumentParser()
parser.add_argument("action", help="Possible actions are: "
                    "'{d[0]}|{d[1]}' ".format(d=actions))
parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
args = parser.parse_args()


""" logging configuration """
logger = ft_logger.Logger("prepare_env").getLogger()


CONFIG_FUNCTEST_PATH = ft_constants.CONFIG_FUNCTEST_YAML
CONFIG_PATCH_PATH = os.path.join(os.path.dirname(
    CONFIG_FUNCTEST_PATH), "config_patch.yaml")

with open(CONFIG_PATCH_PATH) as f:
    functest_patch_yaml = yaml.safe_load(f)


def print_separator():
    logger.info("==============================================")


class GlobalVariables:
    CI_INSTALLER_TYPE = ft_constants.CI_INSTALLER_TYPE
    CI_INSTALLER_IP = ft_constants.CI_INSTALLER_IP
    CI_SCENARIO = ft_constants.CI_SCENARIO
    CI_DEBUG = ft_constants.CI_DEBUG
    CI_NODE = ft_constants.CI_NODE
    CI_BUILD_TAG = ft_constants.CI_BUILD_TAG
    INSTALLERS = ft_constants.INSTALLERS
    IS_CI_RUN = ft_constants.IS_CI_RUN
    FUNCTEST_CONF_DIR = ft_constants.FUNCTEST_CONF_DIR
    ENV_FILE = FUNCTEST_CONF_DIR + "/env_active"
    FUNCTEST_DATA_DIR = ft_constants.FUNCTEST_DATA_DIR
    FUNCTEST_RESULTS_DIR = ft_constants.FUNCTEST_RESULTS_DIR
    DEPLOYMENT_NAME = ft_constants.RALLY_DEPLOYMENT_NAME
    TEMPEST_REPO_DIR = ft_constants.TEMPEST_REPO_DIR
    OPENSTACK_RC_FILE = ft_constants.OPENSTACK_CREDS
    FUNCTEST_REPO_DIR = ft_constants.FUNCTEST_REPO_DIR


def check_env_variables():
    print_separator()
    logger.info("Checking environment variables...")

    if GlobalVariables.CI_INSTALLER_TYPE is None:
        logger.warning("The env variable 'INSTALLER_TYPE' is not defined.")
        GlobalVariables.CI_INSTALLER_TYPE = "undefined"
    else:
        if GlobalVariables.CI_INSTALLER_TYPE not in GlobalVariables.INSTALLERS:
            logger.warning("INSTALLER_TYPE=%s is not a valid OPNFV installer. "
                           "Available OPNFV Installers are : %s. "
                           "Setting INSTALLER_TYPE=undefined."
                           % (GlobalVariables.CI_INSTALLER_TYPE,
                              GlobalVariables.INSTALLERS))
            GlobalVariables.CI_INSTALLER_TYPE = "undefined"
        else:
            logger.info("    INSTALLER_TYPE=%s"
                        % GlobalVariables.CI_INSTALLER_TYPE)

    if GlobalVariables.CI_INSTALLER_IP is None:
        logger.warning("The env variable 'INSTALLER_IP' is not defined. "
                       "It is needed to fetch the OpenStack credentials. "
                       "If the credentials are not provided to the "
                       "container as a volume, please add this env variable "
                       "to the 'docker run' command.")
    else:
        logger.info("    INSTALLER_IP=%s" % GlobalVariables.CI_INSTALLER_IP)

    if GlobalVariables.CI_SCENARIO is None:
        logger.warning("The env variable 'DEPLOY_SCENARIO' is not defined. "
                       "Setting CI_SCENARIO=undefined.")
        GlobalVariables.CI_SCENARIO = "undefined"
    else:
        logger.info("    DEPLOY_SCENARIO=%s" % GlobalVariables.CI_SCENARIO)
    if GlobalVariables.CI_DEBUG:
        logger.info("    CI_DEBUG=%s" % GlobalVariables.CI_DEBUG)

    if GlobalVariables.CI_NODE:
        logger.info("    NODE_NAME=%s" % GlobalVariables.CI_NODE)

    if GlobalVariables.CI_BUILD_TAG:
        logger.info("    BUILD_TAG=%s" % GlobalVariables.CI_BUILD_TAG)

    if GlobalVariables.IS_CI_RUN:
        logger.info("    IS_CI_RUN=%s" % GlobalVariables.IS_CI_RUN)


def create_directories():
    print_separator()
    logger.info("Creating needed directories...")
    if not os.path.exists(GlobalVariables.FUNCTEST_CONF_DIR):
        os.makedirs(GlobalVariables.FUNCTEST_CONF_DIR)
        logger.info("    %s created." % GlobalVariables.FUNCTEST_CONF_DIR)
    else:
        logger.debug("   %s already exists."
                     % GlobalVariables.FUNCTEST_CONF_DIR)

    if not os.path.exists(GlobalVariables.FUNCTEST_DATA_DIR):
        os.makedirs(GlobalVariables.FUNCTEST_DATA_DIR)
        logger.info("    %s created." % GlobalVariables.FUNCTEST_DATA_DIR)
    else:
        logger.debug("   %s already exists."
                     % GlobalVariables.FUNCTEST_DATA_DIR)


def source_rc_file():
    print_separator()
    logger.info("Fetching RC file...")

    if GlobalVariables.OPENSTACK_RC_FILE is None:
        logger.warning("The environment variable 'creds' must be set and"
                       "pointing to the local RC file. Using default: "
                       "/home/opnfv/functest/conf/openstack.creds ...")
        GlobalVariables.OPENSTACK_RC_FILE = \
            "/home/opnfv/functest/conf/openstack.creds"

    if not os.path.isfile(GlobalVariables.OPENSTACK_RC_FILE):
        logger.info("RC file not provided. "
                    "Fetching it from the installer...")
        if GlobalVariables.CI_INSTALLER_IP is None:
            logger.error("The env variable CI_INSTALLER_IP must be provided in"
                         " order to fetch the credentials from the installer.")
            sys.exit("Missing CI_INSTALLER_IP.")
        if GlobalVariables.CI_INSTALLER_TYPE not in GlobalVariables.INSTALLERS:
            logger.error("Cannot fetch credentials. INSTALLER_TYPE=%s is "
                         "not a valid OPNFV installer. Available "
                         "installers are : %s." % GlobalVariables.INSTALLERS)
            sys.exit("Wrong INSTALLER_TYPE.")

        cmd = ("/home/opnfv/repos/releng/utils/fetch_os_creds.sh "
               "-d %s -i %s -a %s"
               % (GlobalVariables.OPENSTACK_RC_FILE,
                  GlobalVariables.CI_INSTALLER_TYPE,
                  GlobalVariables.CI_INSTALLER_IP))
        logger.debug("Executing command: %s" % cmd)
        p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output = p.communicate()[0]
        logger.debug("\n%s" % output)
        if p.returncode != 0:
            logger.error("Failed to fetch credentials from installer.")
            sys.exit(1)
    else:
        logger.info("RC file provided in %s."
                    % GlobalVariables.OPENSTACK_RC_FILE)
        if os.path.getsize(GlobalVariables.OPENSTACK_RC_FILE) == 0:
            logger.error("The file %s is empty."
                         % GlobalVariables.OPENSTACK_RC_FILE)
            sys.exit(1)

    logger.info("Sourcing the OpenStack RC file...")
    creds = os_utils.source_credentials(GlobalVariables.OPENSTACK_RC_FILE)
    str = ""
    for key, value in creds.iteritems():
        if re.search("OS_", key):
            str += "\n\t\t\t\t\t\t   " + key + "=" + value
            if key == 'OS_AUTH_URL':
                ft_constants.OS_AUTH_URL = value
            elif key == 'OS_USERNAME':
                ft_constants.OS_USERNAME = value
            elif key == 'OS_TENANT_NAME':
                ft_constants.OS_TENANT_NAME = value
            elif key == 'OS_PASSWORD':
                ft_constants.OS_PASSWORD = value
    logger.debug("Used credentials: %s" % str)
    logger.debug("OS_AUTH_URL:%s" % ft_constants.OS_AUTH_URL)
    logger.debug("OS_USERNAME:%s" % ft_constants.OS_USERNAME)
    logger.debug("OS_TENANT_NAME:%s" % ft_constants.OS_TENANT_NAME)
    logger.debug("OS_PASSWORD:%s" % ft_constants.OS_PASSWORD)


def patch_config_file():
    updated = False
    for key in functest_patch_yaml:
        if key in GlobalVariables.CI_SCENARIO:
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
    cmd = ("%s/functest/ci/check_os.sh" % GlobalVariables.FUNCTEST_REPO_DIR)

    logger.debug("Executing command: %s" % cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    while p.poll() is None:
        line = p.stdout.readline().rstrip()
        if "ERROR" in line:
            logger.error(line)
            sys.exit("Problem while running 'check_os.sh'.")
        logger.info(line)


def install_rally():
    print_separator()
    logger.info("Creating Rally environment...")

    cmd = "rally deployment destroy opnfv-rally"
    ft_utils.execute_command(cmd,
                             error_msg=("Deployment %s does not exist."
                                        % GlobalVariables.DEPLOYMENT_NAME),
                             verbose=False)
    rally_conf = os_utils.get_credentials_for_rally()
    with open('rally_conf.json', 'w') as fp:
        json.dump(rally_conf, fp)
    cmd = "rally deployment create --file=rally_conf.json --name="
    cmd += GlobalVariables.DEPLOYMENT_NAME
    ft_utils.execute_command(cmd,
                             error_msg="Problem creating Rally deployment")

    logger.info("Installing tempest from existing repo...")
    cmd = ("rally verify install --source " +
           GlobalVariables.TEMPEST_REPO_DIR +
           " --system-wide")
    ft_utils.execute_command(cmd,
                             error_msg="Problem installing Tempest.")

    cmd = "rally deployment check"
    ft_utils.execute_command(cmd,
                             error_msg=("OpenStack not responding or "
                                        "faulty Rally deployment."))

    cmd = "rally show images"
    ft_utils.execute_command(cmd,
                             error_msg=("Problem while listing "
                                        "OpenStack images."))

    cmd = "rally show flavors"
    ft_utils.execute_command(cmd,
                             error_msg=("Problem while showing "
                                        "OpenStack flavors."))


def check_environment():
    msg_not_active = "The Functest environment is not installed."
    if not os.path.isfile(GlobalVariables.ENV_FILE):
        logger.error(msg_not_active)
        sys.exit(1)

    with open(GlobalVariables.ENV_FILE, "r") as env_file:
        s = env_file.read()
        if not re.search("1", s):
            logger.error(msg_not_active)
            sys.exit(1)

    logger.info("Functest environment installed.")


def main():
    if not (args.action in actions):
        logger.error('Argument not valid.')
        sys.exit()

    if args.action == "start":
        logger.info("######### Preparing Functest environment #########\n")
        check_env_variables()
        create_directories()
        source_rc_file()
        patch_config_file()
        verify_deployment()
        install_rally()

        with open(GlobalVariables.ENV_FILE, "w") as env_file:
            env_file.write("1")

        check_environment()

    if args.action == "check":
        check_environment()

    exit(0)


if __name__ == '__main__':
    main()
