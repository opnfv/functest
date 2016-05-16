#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Execute BGPVPN Tempest test cases
#

import os
import yaml
import ConfigParser

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)

dirs = functest_yaml.get('general').get('directories')
FUNCTEST_REPO = dirs.get('dir_repo_functest')
BGPVPN_REPO = dirs.get('dir_repo_bgpvpn')
TEST_DB_URL = functest_yaml.get('results').get('test_db_url')

logger = ft_logger.Logger("bgpvpn").getLogger()


def main():
    logger.info("Running BGPVPN Tempest test case...")

    cmd = 'cd ' + BGPVPN_REPO + ';pip install --no-deps -e .'
    ft_utils.execute_command(cmd, logger, exit_on_error=False)

    src_tempest_dir = ft_utils.get_deployment_dir(logger)
    if not src_tempest_dir:
        logger.error("Rally deployment not found.")
        exit(-1)

    src_tempest_conf = src_tempest_dir + '/tempest.conf'
    dst_tempest_conf = src_tempest_dir + '/etc/tempest.conf'

    config = ConfigParser.RawConfigParser()
    config.read(src_tempest_conf)
    config.set('service_available', 'bgpvpn', 'True')
    with open(dst_tempest_conf, 'wb') as config_file:
        config.write(config_file)

    cmd = (src_tempest_dir +
           '/run_tempest.sh -t -N -- networking_bgpvpn_tempest;'
           'rm -rf ' + dst_tempest_conf)
    ft_utils.execute_command(cmd, logger, exit_on_error=False)


if __name__ == '__main__':
    main()
