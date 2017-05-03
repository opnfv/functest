#!/usr/bin/env python
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import json
import logging
import re
import sys
import urllib2

import functest.utils.functest_utils as ft_utils
from functest.utils.constants import CONST

COL_1_LEN = 25
COL_2_LEN = 15
COL_3_LEN = 12
COL_4_LEN = 15
COL_5_LEN = 75

# If we run from CI (Jenkins) we will push the results to the DB
# and then we can print the url to the specific test result


logger = logging.getLogger(__name__)


def init(tiers_to_run=[]):
    test_cases_arr = []
    for tier in tiers_to_run:
        for test in tier.get_tests():
            test_cases_arr.append({'test_name': test.get_name(),
                                   'tier_name': tier.get_name(),
                                   'result': 'Not executed',
                                   'duration': '0',
                                   'url': ''})
    return test_cases_arr


def get_results_from_db():
    url = "%s/results?build_tag=%s" % (ft_utils.get_db_url(),
                                       CONST.BUILD_TAG)
    logger.debug("Query to rest api: %s" % url)
    try:
        data = json.load(urllib2.urlopen(url))
        return data['results']
    except:
        logger.error("Cannot read content from the url: %s" % url)
        return None


def get_data(test, results):
    test_result = test['result']
    url = ''
    for test_db in results:
        if test['test_name'] in test_db['case_name']:
            id = test_db['_id']
            url = ft_utils.get_db_url() + '/results/' + id
            test_result = test_db['criteria']

    return {"url": url, "result": test_result}


def print_line(w1, w2='', w3='', w4='', w5=''):
    str = ('| ' + w1.ljust(COL_1_LEN - 1) +
           '| ' + w2.ljust(COL_2_LEN - 1) +
           '| ' + w3.ljust(COL_3_LEN - 1) +
           '| ' + w4.ljust(COL_4_LEN - 1))
    if CONST.IS_CI_RUN:
        str += ('| ' + w5.ljust(COL_5_LEN - 1))
    str += '|\n'
    return str


def print_line_no_columns(str):
    TOTAL_LEN = COL_1_LEN + COL_2_LEN + COL_3_LEN + COL_4_LEN + 2
    if CONST.IS_CI_RUN:
        TOTAL_LEN += COL_5_LEN + 1
    return ('| ' + str.ljust(TOTAL_LEN) + "|\n")


def print_separator(char="=", delimiter="+"):
    str = ("+" + char * COL_1_LEN +
           delimiter + char * COL_2_LEN +
           delimiter + char * COL_3_LEN +
           delimiter + char * COL_4_LEN)
    if CONST.IS_CI_RUN:
        str += (delimiter + char * COL_5_LEN)
    str += '+\n'
    return str


def main(args=[]):
    executed_test_cases = args

    if CONST.IS_CI_RUN:
        results = get_results_from_db()
        if results is not None:
            for test in executed_test_cases:
                data = get_data(test, results)
                test.update({"url": data['url'],
                             "result": data['result']})

    TOTAL_LEN = COL_1_LEN + COL_2_LEN + COL_3_LEN + COL_4_LEN
    if CONST.IS_CI_RUN:
        TOTAL_LEN += COL_5_LEN
    MID = TOTAL_LEN / 2

    if CONST.BUILD_TAG is not None:
        if re.search("daily", CONST.BUILD_TAG) is not None:
            CONST.CI_LOOP = "daily"
        else:
            CONST.CI_LOOP = "weekly"

    str = ''
    str += print_separator('=', delimiter="=")
    str += print_line_no_columns(' ' * (MID - 8) + 'FUNCTEST REPORT')
    str += print_separator('=', delimiter="=")
    str += print_line_no_columns(' ')
    str += print_line_no_columns(" Deployment description:")
    str += print_line_no_columns("   INSTALLER: %s"
                                 % CONST.INSTALLER_TYPE)
    if CONST.DEPLOY_SCENARIO is not None:
        str += print_line_no_columns("   SCENARIO:  %s"
                                     % CONST.DEPLOY_SCENARIO)
    if CONST.BUILD_TAG is not None:
        str += print_line_no_columns("   BUILD TAG: %s"
                                     % CONST.BUILD_TAG)
    if CONST.CI_LOOP is not None:
        str += print_line_no_columns("   CI LOOP:   %s"
                                     % CONST.CI_LOOP)
    str += print_line_no_columns(' ')
    str += print_separator('=')
    if CONST.IS_CI_RUN:
        str += print_line('TEST CASE', 'TIER', 'DURATION', 'RESULT', 'URL')
    else:
        str += print_line('TEST CASE', 'TIER', 'DURATION', 'RESULT')
    str += print_separator('=')
    for test in executed_test_cases:
        str += print_line(test['test_name'],
                          test['tier_name'],
                          test['duration'],
                          test['result'],
                          test['url'])
        str += print_separator('-')

    logger.info("\n\n\n%s" % str)


if __name__ == '__main__':
    logging.basicConfig()
    main(sys.argv[1:])
