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
import sys
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
COPPER_REPO = dirs.get('dir_repo_copper')

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
    functest_utils.logger_test_results(logger, "Copper",
                                       "copper-notification",
                                       details['status'], details)
    try:
        if args.report:
            functest_utils.push_results_to_db("copper",
                                              "copper-notification",
                                              logger,
                                              start_time,
                                              stop_time,
                                              details['status'],
                                              details)
            logger.info("COPPER results pushed to DB")
    except:
        logger.error("Error pushing results into Database '%s'"
                     % sys.exc_info()[0])

    if ret_val != 0:
        sys.exit(-1)

    sys.exit(0)

if __name__ == '__main__':
    main()
