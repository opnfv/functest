#!/usr/bin/python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0


import time

from functest.core import testcase_base
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils

from baro_tests import collectd


class BarometerCollectd(testcase_base.TestcaseBase):
    '''
    Class for executing barometercollectd testcase.
    '''

    def __init__(self):
        super(BarometerCollectd, self).__init__()
        self.project_name = "barometer"
        self.case_name = "barometercollectd"

    def run(self, **kwargs):
        logger = ft_logger.Logger("BarometerCollectd").getLogger()

        self.start_time = time.time()

        ret = collectd.main(logger)

        self.stop_time = time.time()

        if ret == 0:
            self.criteria = 'PASS'
            result = testcase_base.TestcaseBase.EX_OK
        else:
            self.criteria = 'FAIL'
            result = testcase_base.TestcaseBase.EX_TESTCASE_FAILED

        functest_utils.logger_test_results(
            self.project_name, self.case_name, self.criteria, self.details)

        return result
