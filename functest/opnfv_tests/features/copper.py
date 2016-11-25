#!/usr/bin/python
#
# Copyright 2016 AT&T Intellectual Property, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import argparse
import os
import sys
import time

from functest.core import TestCasesBase
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_constants as ft_constants


class CopperTests(TestCasesBase.TestCasesBase):
    logger = ft_logger.Logger("copper").getLogger()

    def __init__(self):
        super(CopperTests, self).__init__()
        self.project_name = "copper"
        self.case_name = "copper-notification"

    def main(self, **kwargs):
        cmd = "%s/tests/run.sh %s/tests" % (ft_constants.COPPER_REPO_DIR,
                                            ft_constants.COPPER_REPO_DIR)
        log_file = os.path.join(
            ft_constants.FUNCTEST_RESULTS_DIR, "copper.log")
        start_time = time.time()
        ret = ft_utils.execute_command(cmd,
                                       output_file=log_file)

        stop_time = time.time()
        if ret == 0:
            self.logger.info("COPPER PASSED")
            test_status = 'PASS'
        else:
            self.logger.info("COPPER FAILED")
            test_status = 'FAIL'
        self.criteria = test_status
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
    copper = CopperTests()
    try:
        result = copper.main(**args)
        if result != TestCasesBase.TestCasesBase.EX_OK:
            sys.exit(result)
        if args['report']:
            sys.exit(copper.push_to_db())
    except Exception:
        sys.exit(TestCasesBase.TestCasesBase.EX_RUN_ERROR)
