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
import os
import time
import yaml

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)

dirs = functest_yaml.get('general').get('directories')
FUNCTEST_REPO = dirs.get('dir_repo_functest')
PARSER_REPO = dirs.get('dir_repo_parser')

logger = ft_logger.Logger("parser").getLogger()


def main():
    project = 'parser'
    case_name = 'parser-basics'
    cmd = 'cd %s/tests && ./functest_run.sh' % PARSER_REPO

    start_time = time.time()
    ret = functest_utils.execute_command(cmd, logger, exit_on_error=False)
    stop_time = time.time()

    status, details = functest_utils.check_test_result(case_name,
                                                       ret,
                                                       start_time,
                                                       stop_time)

    functest_utils.logger_test_results(logger,
                                       project,
                                       case_name,
                                       status,
                                       details)

    functest_utils.push_results_to_db(project,
                                      case_name,
                                      logger,
                                      start_time,
                                      stop_time,
                                      status,
                                      details)
    exit(ret)

if __name__ == '__main__':
    main()
