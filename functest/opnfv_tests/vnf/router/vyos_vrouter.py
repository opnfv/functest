#!/usr/bin/env python
#
#  Copyright 2017 Okinawa Open Laboratory
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import time
import json
import os
import functest.utils.functest_utils as ft_utils
import functest.utils.functest_logger as ft_logger
from functest.core import testcase_base
from functest.utils.constants import CONST

RESULT_DETAILS_FILE = "test_result.json"


class VrouterVnf(testcase_base.TestcaseBase):

    def __init__(self):
        self.case_name = "vrouter"
        self.logger = ft_logger.Logger("vRouter").getLogger()
        self.repo = CONST.__getattribute__("dir_repo_vrouter")
        self.cmd = 'cd %s && ./run.sh' % self.repo
        self.result_file = self.get_result_file()

    def parse_results(self, ret):
        if ret == 0:
            self.logger.info("{} OK".format(self.case_name))
            self.criteria = 'PASS'
            self.get_result_details()
        else:
            self.logger.info("{} FAILED".format(self.case_name))
            self.criteria = "FAIL"

    def run(self, **kwargs):
        self.start_time = time.time()
        ret = ft_utils.execute_command(self.cmd, output_file=self.result_file)
        self.stop_time = time.time()
        self.parse_results(ret)
        return testcase_base.TestcaseBase.EX_OK

    def get_result_file(self):
        return "{}/{}.log".format(CONST.dir_results, self.case_name)

    def get_result_details(self):
        filepath = self.repo + "/" + RESULT_DETAILS_FILE
        if os.path.exists(filepath):
            f = open(filepath, 'r')
            self.details = json.load(f)
            f.close()
