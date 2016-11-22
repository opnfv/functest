#!/usr/bin/python
#
# Copyright 2016 ZTE Corporation
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
import time

import argparse

import functest.core.TestCasesBase as base
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils


class Parser(base.TestCasesBase):
    def __init__(self):
        super(Parser, self).__init__()
        self.project_name = "parser"
        self.case_name = "parser-basics"
        self.parser_repo = self.get_conf('general.directories.dir_repo_parser')
        self.logger = ft_logger.Logger("parser").getLogger()
        self.log_file = self.results_dir + '/parser.log'

    def run(self, **kwargs):
        cmd = 'cd %s/tests && ./functest_run.sh' % self.parser_repo

        self.start_time = time.time()
        ret = functest_utils.execute_command(cmd,
                                             info=True,
                                             output_file=self.log_file)
        self.stop_time = time.time()

        self.criteria, details = self.parser_results(self.project_name,
                                                     ret,
                                                     self.start_time,
                                                     self.stop_time)

        functest_utils.logger_test_results(self.project_name,
                                           self.case_name,
                                           self.criteria,
                                           details)

        return ret


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-r", "--report",
                             help="Create json result file",
                             action="store_true")
    Parser.main(args_parser)
