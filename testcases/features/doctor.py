#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# 0.1: This script boots the VM1 and allocates IP address from Nova
# Later, the VM2 boots then execute cloud-init to ping VM1.
# After successful ping, both the VMs are deleted.
# 0.2: measure test duration and publish results under json format
#
#

import os
import time
import yaml

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)

dirs = functest_yaml.get('general').get('directories')
FUNCTEST_REPO = dirs.get('dir_repo_functest')
DOCTOR_REPO = dirs.get('dir_repo_doctor')
TEST_DB_URL = functest_yaml.get('results').get('test_db_url')

logger = ft_logger.Logger("doctor").getLogger()


def main():
    exit_code = -1
    cmd = 'cd %s/tests && ./run.sh' % DOCTOR_REPO
    start_time = time.time()

    ret = functest_utils.execute_command(cmd, logger, exit_on_error=False)

    stop_time = time.time()
    duration = round(stop_time - start_time, 1)
    if ret == 0:
        logger.info("doctor OK")
        test_status = 'OK'
        exit_code = 0
    else:
        logger.info("doctor FAILED")
        test_status = 'NOK'

    details = {
        'timestart': start_time,
        'duration': duration,
        'status': test_status,
    }
    pod_name = functest_utils.get_pod_name(logger)
    scenario = functest_utils.get_scenario(logger)
    version = functest_utils.get_version(logger)
    build_tag = functest_utils.get_build_tag(logger)

    status = "FAIL"
    if details['status'] == "OK":
        status = "PASS"

    logger.info("Pushing Doctor results: TEST_DB_URL=%(db)s pod_name=%(pod)s "
                "version=%(v)s scenario=%(s)s criteria=%(c)s details=%(d)s" % {
                    'db': TEST_DB_URL,
                    'pod': pod_name,
                    'v': version,
                    's': scenario,
                    'c': status,
                    'b': build_tag,
                    'd': details,
                })
    functest_utils.push_results_to_db("doctor",
                                      "doctor-notification",
                                      logger,
                                      start_time,
                                      stop_time,
                                      status,
                                      details)

    exit(exit_code)

if __name__ == '__main__':
    main()
