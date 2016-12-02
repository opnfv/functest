#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Execute Multisite Tempest test cases
##

import ConfigParser
import os
import re
import shutil
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger
from run_tempest import configure_tempest
from run_tempest import TEMPEST_RESULTS_DIR
import functest.utils.functest_constants as ft_constants

logger = ft_logger.Logger("gen_tempest_conf").getLogger()

CI_INSTALLER_TYPE = ft_constants.CI_INSTALLER_TYPE
CI_INSTALLER_IP = ft_constants.CI_INSTALLER_IP


def configure_tempest_multisite(deployment_dir):
    """
    Add/update needed parameters into tempest.conf file generated by Rally
    """
    logger.debug("configure the tempest")
    configure_tempest(deployment_dir)

    logger.debug("Finding tempest.conf file...")
    tempest_conf_old = os.path.join(deployment_dir, '/tempest.conf')
    if not os.path.isfile(tempest_conf_old):
        logger.error("Tempest configuration file %s NOT found."
                     % tempest_conf_old)
        exit(-1)

    # Copy tempest.conf to /home/opnfv/functest/results/tempest/
    cur_path = os.path.split(os.path.realpath(__file__))[0]
    tempest_conf_file = os.path.join(cur_path, '/tempest_multisite.conf')
    shutil.copyfile(tempest_conf_old, tempest_conf_file)

    logger.debug("Updating selected tempest.conf parameters...")
    config = ConfigParser.RawConfigParser()
    config.read(tempest_conf_file)

    config.set('service_available', 'kingbird', 'true')
    cmd = ("openstack endpoint show kingbird | grep publicurl |"
           "awk '{print $4}' | awk -F '/' '{print $4}'")
    kingbird_api_version = os.popen(cmd).read()
    if CI_INSTALLER_TYPE == 'fuel':
        # For MOS based setup, the service is accessible
        # via bind host
        kingbird_conf_path = "/etc/kingbird/kingbird.conf"
        installer_type = CI_INSTALLER_TYPE
        installer_ip = CI_INSTALLER_IP
        installer_username = ft_utils.get_functest_config(
            "multisite." + installer_type +
            "_environment.installer_username")
        installer_password = ft_utils.get_functest_config(
            "multisite." + installer_type +
            "_environment.installer_password")

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
        cmd = "openstack endpoint show kingbird | grep publicurl |\
               awk '{print $4}' | awk -F '/' '{print $3}'"
        kingbird_endpoint_url = os.popen(cmd).read()

    try:
        config.add_section("kingbird")
    except Exception:
        logger.info('kingbird section exist')
    config.set('kingbird', 'endpoint_type', 'publicURL')
    config.set('kingbird', 'TIME_TO_SYNC', '20')
    config.set('kingbird', 'endpoint_url', kingbird_endpoint_url)
    config.set('kingbird', 'api_version', kingbird_api_version)
    with open(tempest_conf_file, 'wb') as config_file:
        config.write(config_file)

    return True


def main():

    if not os.path.exists(TEMPEST_RESULTS_DIR):
        os.makedirs(TEMPEST_RESULTS_DIR)

    deployment_dir = ft_utils.get_deployment_dir()
    configure_tempest_multisite(deployment_dir)


if __name__ == '__main__':
    main()
