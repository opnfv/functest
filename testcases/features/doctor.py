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
import argparse
import os
import time
import yaml

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
args = parser.parse_args()

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)

dirs = functest_yaml.get('general').get('directories')
FUNCTEST_REPO = dirs.get('dir_repo_functest')
DOCTOR_REPO = dirs.get('dir_repo_doctor')

logger = ft_logger.Logger("doctor").getLogger()


def main():
    exit_code = -1
    cmd = 'cd %s/tests && ./run.sh' % DOCTOR_REPO
    start_time = time.time()

    ret = functest_utils.execute_command(cmd, logger, info=True,
                                         exit_on_error=False)

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
    status = "FAIL"
    if details['status'] == "OK":
        status = "PASS"
    functest_utils.logger_test_results(logger, "Doctor",
                                       "doctor-notification",
                                       status, details)
    if args.report:
        functest_utils.push_results_to_db("doctor",
                                          "doctor-notification",
                                          logger,
                                          start_time,
                                          stop_time,
                                          status,
                                          details)
        logger.info("Doctor results pushed to DB")

    exit(exit_code)

if __name__ == '__main__':
    main()
