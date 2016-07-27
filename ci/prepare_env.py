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


import argparse
import os
import re
import subprocess
import sys
import json

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as os_utils
import yaml


actions = ['start', 'check']
parser = argparse.ArgumentParser()
parser.add_argument("action", help="Possible actions are: "
                    "'{d[0]}|{d[1]}' ".format(d=actions))
parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
args = parser.parse_args()


""" logging configuration """
logger = ft_logger.Logger("prepare_env").getLogger()


""" global variables """
INSTALLERS = ['fuel', 'compass', 'apex', 'joid']
CI_INSTALLER_TYPE = ""
CI_INSTALLER_IP = ""
CI_SCENARIO = ""
CI_DEBUG = False
REPOS_DIR = os.getenv('repos_dir')
FUNCTEST_REPO = REPOS_DIR + '/functest/'

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)

FUNCTEST_CONF_DIR = functest_yaml.get("general").get(
    "directories").get("dir_functest_conf")

FUNCTEST_DATA_DIR = functest_yaml.get("general").get(
    "directories").get("dir_functest_data")
FUNCTEST_RESULTS_DIR = functest_yaml.get("general").get(
    "directories").get("dir_results")
DEPLOYMENT_MAME = functest_yaml.get("rally").get("deployment_name")
TEMPEST_REPO_DIR = functest_yaml.get("general").get(
    "directories").get("dir_repo_tempest")

ENV_FILE = FUNCTEST_CONF_DIR + "/env_active"


def print_separator():
    logger.info("==============================================")


def check_env_variables():
    print_separator()
    logger.info("Checking environment variables...")
    global CI_INSTALLER_TYPE
    global CI_INSTALLER_IP
    global CI_DEBUG
    global CI_SCENARIO
    CI_INSTALLER_TYPE = os.getenv('INSTALLER_TYPE')
    CI_INSTALLER_IP = os.getenv('INSTALLER_IP')
    CI_SCENARIO = os.getenv('DEPLOY_SCENARIO')
    CI_NODE = os.getenv('NODE_NAME')
    CI_BUILD_TAG = os.getenv('BUILD_TAG')
    CI_DEBUG = os.getenv('CI_DEBUG')

    if CI_INSTALLER_TYPE is None:
        logger.warning("The env variable 'INSTALLER_TYPE' is not defined.")
        CI_INSTALLER_TYPE = "undefined"
    else:
        if os.getenv('INSTALLER_TYPE') not in INSTALLERS:
            logger.warning("INSTALLER_TYPE=%s is not a valid OPNFV installer. "
                           "Available OPNFV Installers are : %s."
                           "Setting INSTALLER_TYPE=undefined." % INSTALLERS)
            CI_INSTALLER_TYPE = "undefined"
        else:
            logger.info("    INSTALLER_TYPE=%s" % CI_INSTALLER_TYPE)

    if CI_INSTALLER_IP is None:
        logger.warning("The env variable 'INSTALLER_IP' is not defined. "
                       "It is needed to fetch the OpenStack credentials. "
                       "If the credentials are not provided to the "
                       "container as a volume, please add this env variable "
                       "to the 'docker run' command.")
    else:
        logger.info("    INSTALLER_IP=%s" % CI_INSTALLER_IP)

    if CI_SCENARIO is None:
        logger.warning("The env variable 'DEPLOY_SCENARIO' is not defined. "
                       "Setting CE_SCENARIO=undefined.")
        CI_SCENARIO = "undefined"
    else:
        logger.info("    DEPLOY_SCENARIO=%s" % CI_SCENARIO)
    if CI_DEBUG:
        logger.info("    CI_DEBUG=%s" % CI_DEBUG)

    if CI_NODE:
        logger.info("    NODE_NAME=%s" % CI_NODE)

    if CI_BUILD_TAG:
        logger.info("    BUILD_TAG=%s" % CI_BUILD_TAG)


def create_directories():
    print_separator()
    logger.info("Creating needed directories...")
    if not os.path.exists(FUNCTEST_CONF_DIR):
        os.makedirs(FUNCTEST_CONF_DIR)
        logger.info("    %s created." % FUNCTEST_CONF_DIR)
    else:
        logger.debug("   %s already exists." % FUNCTEST_CONF_DIR)

    if not os.path.exists(FUNCTEST_DATA_DIR):
        os.makedirs(FUNCTEST_DATA_DIR)
        logger.info("    %s created." % FUNCTEST_DATA_DIR)
    else:
        logger.debug("   %s already exists." % FUNCTEST_DATA_DIR)


def source_rc_file():
    print_separator()
    logger.info("Fetching RC file...")
    rc_file = os.getenv('creds')
    if rc_file is None:
        logger.warning("The environment variable 'creds' must be set and"
                       "pointing to the local RC file. Using default: "
                       "/home/opnfv/functest/conf/openstack.creds ...")
        rc_file = "/home/opnfv/functest/conf/openstack.creds"

    if not os.path.isfile(rc_file):
        logger.info("RC file not provided. "
                    "Fetching it from the installer...")
        if CI_INSTALLER_IP is None:
            logger.error("The env variable CI_INSTALLER_IP must be provided in"
                         " order to fetch the credentials from the installer.")
            sys.exit("Missing CI_INSTALLER_IP.")
        if CI_INSTALLER_TYPE not in INSTALLERS:
            logger.error("Cannot fetch credentials. INSTALLER_TYPE=%s is "
                         "not a valid OPNFV installer. Available "
                         "installers are : %s." % INSTALLERS)
            sys.exit("Wrong INSTALLER_TYPE.")

        cmd = ("/home/opnfv/repos/releng/utils/fetch_os_creds.sh "
               "-d %s -i %s -a %s"
               % (rc_file, CI_INSTALLER_TYPE, CI_INSTALLER_IP))
        logger.debug("Executing command: %s" % cmd)
        p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output = p.communicate()[0]
        logger.debug("\n%s" % output)
        if p.returncode != 0:
            logger.error("Failed to fetch credentials from installer.")
            sys.exit(1)
    else:
        logger.info("RC file provided in %s." % rc_file)
        if os.path.getsize(rc_file) == 0:
            logger.error("The file %s is empty." % rc_file)
            sys.exit(1)

    logger.info("Sourcing the OpenStack RC file...")
    creds = os_utils.source_credentials(rc_file)
    str = ""
    for key, value in creds.iteritems():
        if re.search("OS_", key):
            str += "\n\t\t\t\t\t\t   " + key + "=" + value
    logger.debug("Used credentials: %s" % str)


def verify_deployment():
    print_separator()
    logger.info("Verifying OpenStack services...")
    cmd = ("%s/ci/check_os.sh" % FUNCTEST_REPO)

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
    ft_utils.execute_command(cmd, logger=logger, exit_on_error=False,
                             error_msg=("Deployment %s does not exist."
                                        % DEPLOYMENT_MAME), verbose=False)
    rally_conf = os_utils.get_credentials_for_rally()
    with open('rally_conf.json', 'w') as fp:
        json.dump(rally_conf, fp)
    cmd = "rally deployment create --file=rally_conf.json --name="
    cmd += DEPLOYMENT_MAME
    ft_utils.execute_command(cmd, logger,
                             error_msg="Problem creating Rally deployment")

    logger.info("Installing tempest from existing repo...")
    cmd = ("rally verify install --source " + TEMPEST_REPO_DIR +
           " --system-wide")
    ft_utils.execute_command(cmd, logger,
                             error_msg="Problem installing Tempest.")

    cmd = "rally deployment check"
    ft_utils.execute_command(cmd, logger,
                             error_msg=("OpenStack not responding or "
                                        "faulty Rally deployment."))

    cmd = "rally show images"
    ft_utils.execute_command(cmd, logger,
                             error_msg=("Problem while listing "
                                        "OpenStack images."))

    cmd = "rally show flavors"
    ft_utils.execute_command(cmd, logger,
                             error_msg=("Problem while showing "
                                        "OpenStack flavors."))


def check_environment():
    msg_not_active = "The Functest environment is not installed."
    if not os.path.isfile(ENV_FILE):
        logger.error(msg_not_active)
        sys.exit(1)

    with open(ENV_FILE, "r") as env_file:
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
        verify_deployment()
        install_rally()

        with open(ENV_FILE, "w") as env_file:
            env_file.write("1")

        check_environment()

    if args.action == "check":
        check_environment()

    exit(0)

if __name__ == '__main__':
    main()
