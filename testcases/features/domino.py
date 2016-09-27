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
# 0.3: add report flag to push results when needed
#

import time

import argparse

import functest.utils.config_functest as config_functest
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils

CONF = config_functest.CONF

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
args = parser.parse_args()


logger = ft_logger.Logger("domino").getLogger()


def main():
    cmd = 'cd %s && ./tests/run_multinode.sh' % CONF.domino_repo
    log_file = CONF.results_dir + "/domino.log"
    start_time = time.time()

    ret = ft_utils.execute_command(cmd,
                                   exit_on_error=False,
                                   output_file=log_file)

    stop_time = time.time()
    duration = round(stop_time - start_time, 1)
    if ret == 0 and duration > 1:
        logger.info("domino OK")
        test_status = 'OK'
    elif ret == 0 and duration <= 1:
        logger.info("domino TEST SKIPPED")
        test_status = 'SKIPPED'
    else:
        logger.info("domino FAILED")
        test_status = 'NOK'

    details = {
        'timestart': start_time,
        'duration': duration,
        'status': test_status,
    }

    status = "FAIL"
    if details['status'] == "OK":
        status = "PASS"
    elif details['status'] == "SKIPPED":
        status = "SKIP"

    ft_utils.logger_test_results("Domino",
                                 "domino-multinode",
                                 status,
                                 details)
    if args.report:
        if status is not "SKIP":
            ft_utils.push_results_to_db("domino",
                                        "domino-multinode",
                                        start_time,
                                        stop_time,
                                        status,
                                        details)
            logger.info("Domino results pushed to DB")


if __name__ == '__main__':
    main()
