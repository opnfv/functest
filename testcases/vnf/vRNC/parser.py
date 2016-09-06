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
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
args = parser.parse_args()

functest_yaml = functest_utils.get_functest_yaml()

dirs = functest_yaml.get('general').get('directories')
PARSER_REPO = dirs.get('dir_repo_parser')

logger = ft_logger.Logger("parser").getLogger()


def main():
    project = 'parser'
    case_name = 'parser-basics'
    cmd = 'cd %s/tests && ./functest_run.sh' % PARSER_REPO

    start_time = time.time()
    ret = functest_utils.execute_command(cmd,
                                         info=True,
                                         exit_on_error=False)
    stop_time = time.time()

    status, details = functest_utils.check_test_result(project,
                                                       ret,
                                                       start_time,
                                                       stop_time)

    functest_utils.logger_test_results(project,
                                       case_name,
                                       status,
                                       details)

    if args.report:
        logger.debug("Report Parser Results to DB......")
        functest_utils.push_results_to_db(project,
                                          case_name,
                                          start_time,
                                          stop_time,
                                          status,
                                          details)
    exit(ret)

if __name__ == '__main__':
    main()
