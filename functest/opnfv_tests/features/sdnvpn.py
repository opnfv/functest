#!/usr/bin/python
#
# Copyright (c) 2016 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#


import argparse
import os
import sys
import time

from functest.core import TestCasesBase
import functest.utils.functest_constants as ft_constants
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils


class SdnVpnTests(TestCasesBase.TestCasesBase):
    SDNVPN_REPO_TESTS = os.path.join(
        ft_constants.SDNVPN_REPO_DIR, "tests/functest")
    logger = ft_logger.Logger("sdnvpn").getLogger()

    def __init__(self):
        super(SdnVpnTests, self).__init__()
        self.project_name = "sdnvpn"
        self.case_name = "bgpvpn"

    def main(self, **kwargs):
        os.chdir(self.SDNVPN_REPO_TESTS)
        cmd = 'run_tests.py'
        log_file = os.path.join(
            ft_constants.FUNCTEST_RESULTS_DIR, "sdnvpn.log")
        start_time = time.time()

        ret = ft_utils.execute_command(cmd,
                                       output_file=log_file)

        stop_time = time.time()
        if ret == 0:
            self.logger.info("%s OK" % self.case_name)
            status = 'PASS'
        else:
            self.logger.info("%s FAILED" % self.case_name)
            status = "FAIL"

        # report status only if tests run (FAIL OR PASS)
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
    args = vars(parser.parse_args())
    sdnvpn = SdnVpnTests()
    try:
        result = sdnvpn.main(**args)
        if result != TestCasesBase.TestCasesBase.EX_OK:
            sys.exit(result)
        if args['report']:
            sys.exit(sdnvpn.push_to_db())
    except Exception:
        sys.exit(TestCasesBase.TestCasesBase.EX_RUN_ERROR)
