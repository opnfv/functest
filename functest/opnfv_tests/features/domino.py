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
# 0.4: refactoring to match Test abstraction class

import argparse
import sys
import time

from functest.core import TestCasesBase
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils


class DominoCases(TestCasesBase.TestCasesBase):
    DOMINO_REPO = \
        ft_utils.get_functest_config('general.directories.dir_repo_domino')
    RESULTS_DIR = \
        ft_utils.get_functest_config('general.directories.dir_results')
    logger = ft_logger.Logger("domino").getLogger()

    def __init__(self):
        self.project_name = "domino"
        self.case_name = "domino-multinode"

    def main(self, **kwargs):
        cmd = 'cd %s && ./tests/run_multinode.sh' % self.DOMINO_REPO
        log_file = self.RESULTS_DIR + "/domino.log"
        start_time = time.time()

        ret = ft_utils.execute_command(cmd,
                                       output_file=log_file)

        stop_time = time.time()
        duration = round(stop_time - start_time, 1)
        if ret == 0 and duration > 1:
            self.logger.info("domino OK")
            status = 'PASS'
        elif ret == 0 and duration <= 1:
            self.logger.info("domino TEST SKIPPED")
            status = 'SKIP'
        else:
            self.logger.info("domino FAILED")
            status = "FAIL"

        # report status only if tests run (FAIL OR PASS)
        if status is not "SKIP":
            self.criteria = status
            self.start_time = start_time
            self.stop_time = stop_time
            self.details = {}

    def run(self):
        kwargs = {}
        return self.main(**kwargs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--report",
                        help="Create json result file",
                        action="store_true")
    args = parser.parse_args()
    domino = DominoCases()
    try:
        result = domino.main(**args)
        if result != TestCasesBase.TestCasesBase.EX_OK:
            sys.exit(result)
        if args['report']:
            sys.exit(domino.push_to_db())
    except Exception:
        sys.exit(TestCasesBase.TestCasesBase.EX_RUN_ERROR)
