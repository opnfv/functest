#!/usr/bin/env python
#
# Copyright (c) 2015 Orange
# guyrodrigue.koffi@orange.com
# morgan.richomme@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import re, json, os, urllib2, argparse, logging

""" tests configuration """
tests = ['authenticate', 'glance', 'heat', 'keystone', 'neutron', 'nova', 'tempest', 'vm', 'all']
parser = argparse.ArgumentParser()
parser.add_argument("test_name", help="The name of the test you want to perform with rally. "
                                      "Possible values are : "
                                      "[ {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} | {d[5]} | {d[6]} "
                                      "| {d[7]} | {d[8]} ]. The 'all' value performs all the tests scenarios "
                                      "except 'tempest'".format(d=tests))

parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
args = parser.parse_args()

""" logging configuration """
logger = logging.getLogger('run_rally')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_task_id(cmd_raw):
    """
    get task id from command rally result
    :param cmd_raw:
    :return: task_id as string
    """
    taskid_re = re.compile('^Task +(.*): started$')
    for line in cmd_raw.splitlines(True):
        line = line.strip()
        match = taskid_re.match(line)
        if match:
            return match.group(1)
    return None


def task_succeed(json_raw):
    """
    Parse JSON from rally JSON results
    :param json_raw:
    :return: Bool
    """
    rally_report = json.loads(json_raw)
    rally_report = rally_report[0]
    if rally_report is None:
        return False
    if rally_report.get('result') is None:
        return False
 
    for result in rally_report.get('result'):
        if len(result.get('error')) > 0:
            return False
 
    return True
 
 
def run_task(test_name):
    """
    the "main" function of the script who lunch rally for a task
    :param test_name: name for the rally test
    :return: void
    """
    logger.info('starting {} test ...'.format(test_name))
 
    """ get the date """
    cmd = os.popen("date '+%d%m%Y_%H%M'")
    test_date = cmd.read().rstrip()
 
    """ check directory for scenarios test files or retrieve from git otherwise"""
    proceed_test = True
    tests_path = "./scenarios"
    test_file_name = '{}/opnfv-{}.json'.format(tests_path, test_name)
    if not os.path.exists(test_file_name):
        logger.debug('{} does not exists'.format(test_file_name))
        proceed_test = retrieve_test_cases_file(test_name, tests_path)
        logger.debug('successfully downloaded to : {}'.format(test_file_name))
 
    """ we do the test only if we have a scenario test file """
    if proceed_test:
        cmd_line = "rally task start --abort-on-sla-failure %s" % test_file_name
        logger.debug('running command line : {}'.format(cmd_line))
        cmd = os.popen(cmd_line)
        task_id = get_task_id(cmd.read())
        logger.debug('task_id : {}'.format(task_id))
 
        if task_id is None:
            logger.error("failed to retrieve task_id")
            exit(-1)
 
        """ check for result directory and create it otherwise """
        report_path = "./results"
        if not os.path.exists(report_path):
            logger.debug('does not exists, we create it'.format(report_path))
            os.makedirs(report_path)
 
        """ write html report file """
        report_file_name = '{}/opnfv-{}-{}.html'.format(report_path, test_name, test_date)
        cmd_line = "rally task report %s --out %s" % (task_id, report_file_name)
        logger.debug('running command line : {}'.format(cmd_line))
        os.popen(cmd_line)
 
        """ get and save rally operation JSON result """
        cmd_line = "rally task results %s" % task_id
        logger.debug('running command line : {}'.format(cmd_line))
        cmd = os.popen(cmd_line)
        json_results = cmd.read()
        with open('{}/opnfv-{}-{}.json'.format(report_path, test_name, test_date), 'w') as f:
            logger.debug('saving json file')
            f.write(json_results)
 
        """ parse JSON operation result """
        if task_succeed(json_results):
            print '{} OK'.format(test_date)
        else:
            print '{} KO'.format(test_date)
    else:
        logger.error('{} test failed, unable to find a scenario test file'.format(test_name))
 
 
def retrieve_test_cases_file(test_name, tests_path):
    """
    Retrieve from github the sample test files
    :return: Boolean that indicates the retrieval status
    """
 
    """ do not add the "/" at the end """
    url_base = "https://git.opnfv.org/cgit/functest/plain/testcases/VIM/OpenStack/CI/suites"
 
    test_file_name = 'opnfv-{}.json'.format(test_name)
    logger.info('fetching {}/{} ...'.format(url_base, test_file_name))
 
    try:
        response = urllib2.urlopen('{}/{}'.format(url_base, test_file_name))
    except (urllib2.HTTPError, urllib2.URLError):
        return False
    file_raw = response.read()
 
    """ check if the test path exist otherwise we create it """
    if not os.path.exists(tests_path):
        os.makedirs(tests_path)
 
    with open('{}/{}'.format(tests_path, test_file_name), 'w') as f:
        f.write(file_raw)
    return True


def main():
    """ configure script """
    if not (args.test_name in tests):
        logger.error('argument not valid')
        exit(-1)

    if args.test_name == "all":
        for test_name in tests:
            if not (test_name == 'all' or test_name == 'tempest'):
                print(test_name)
                run_task(test_name)
    else:
        run_task(args.test_name)

if __name__ == '__main__':
    main()
