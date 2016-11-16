#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

import functest.utils.functest_logger as ft_logger
from functest.core import TestCasesBase
from vrouter.vRouter import vRouter

class vRouterTestCases(TestCasesBase.TestCasesBase):

    def __init__(self):
        self.case_name = "vrouter"
        self.logger = ft_logger.Logger("vRouter").getLogger()

    def main(self):
        vrouter = vRouter(self.logger)
        result_data = vrouter.main()
        self.set_results(result_data)

        if result_data["status"] == "FAIL":
            self.logger.error("return EX_RUN_ERROR")
            return self.EX_RUN_ERROR

        self.logger.info("return EX_OK")
        return self.EX_OK

    def set_results(self, result_data):
        self.start_time = result_data['start_time']
        self.stop_time = result_data['stop_time']
        self.criteria = result_data['status']
        self.details = result_data['results']

    def run(self):
        return self.main()
