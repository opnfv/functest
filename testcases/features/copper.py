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

import os
import sys
import time
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils
import yaml


with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)

dirs = functest_yaml.get('general').get('directories')
FUNCTEST_REPO = dirs.get('dir_repo_functest')
COPPER_REPO = dirs.get('dir_repo_copper')
TEST_DB_URL = functest_yaml.get('results').get('test_db_url')

logger = ft_logger.Logger("copper").getLogger()


def main():
    cmd = "%s/tests/run.sh %s/tests" % (COPPER_REPO, COPPER_REPO)

    start_time = time.time()

    ret_val = functest_utils.execute_command(cmd, logger, exit_on_error=False)

    stop_time = time.time()
    duration = round(stop_time - start_time, 1)
    if ret_val == 0:
        logger.info("COPPER PASSED")
        test_status = 'PASS'
    else:
        logger.info("COPPER FAILED")
        test_status = 'FAIL'

    details = {
        'timestart': start_time,
        'duration': duration,
        'status': test_status,
    }
    pod_name = functest_utils.get_pod_name(logger)
    scenario = functest_utils.get_scenario(logger)
    version = functest_utils.get_version(logger)
    build_tag = functest_utils.get_build_tag(logger)

    logger.info("Pushing COPPER results: TEST_DB_URL=%(db)s pod_name=%(pod)s "
                "version=%(v)s scenario=%(s)s criteria=%(c)s details=%(d)s" % {
                    'db': TEST_DB_URL,
                    'pod': pod_name,
                    'v': version,
                    's': scenario,
                    'c': details['status'],
                    'b': build_tag,
                    'd': details,
                })
    functest_utils.push_results_to_db("COPPER",
                                      "COPPER-notification",
                                      logger,
                                      start_time,
                                      stop_time,
                                      details['status'],
                                      details)
    if ret_val != 0:
        sys.exit(-1)

    sys.exit(0)

if __name__ == '__main__':
    main()
