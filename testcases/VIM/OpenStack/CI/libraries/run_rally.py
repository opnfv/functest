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
import re, json, os, urllib2, argparse, logging, yaml

HOME = os.environ['HOME']+"/"
with open(args.repo_path+"config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

""" get the date """
cmd = os.popen("date '+%d%m%Y_%H%M'")
test_date = cmd.read().rstrip()

HOME = os.environ['HOME']+"/"
SCENARIOS_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_rally_scn")
RESULTS_DIR = HOME + functest_yaml.get("general").get("directories").get("dir_rally_res") + test_date + "/"

""" tests configuration """
tests = ['authenticate', 'glance', 'cinder', 'heat', 'keystone', 'neutron', 'nova', 'quotas', 'requests', 'vm', 'tempest', 'all', 'smoke']
parser = argparse.ArgumentParser()
parser.add_argument("test_name", help="The name of the test you want to perform with rally. "
                                      "Possible values are : "
                                      "[ {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} | {d[5]} | {d[6]} "
                                      "| {d[7]} | {d[8]} | {d[9]} | {d[10]} | {d[11]} | {d[12]}]. The 'all' value performs all the  possible tests scenarios"
                                      "except 'tempest'".format(d=tests))

parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
parser.add_argument("test_mode", help="Tempest test mode", nargs='?', default="smoke")
args = parser.parse_args()
test_mode=args.test_mode

if not args.test_name == "tempest":
    if not args.test_mode == "smoke":
        parser.error("test_mode is only used with tempest")

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


def get_tempest_id(cmd_raw):
    """
    get task id from command rally result
    :param cmd_raw:
    :return: task_id as string
    """
    taskid_re = re.compile('^Verification UUID: (.*)$')
    for line in cmd_raw.splitlines(True):
        line = line.strip()
    match = taskid_re.match(line)

    if match:
        return match.group(1)
    return None

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

def run_tempest():
    """
    the function dedicated to Tempest (functional tests for OpenStack)
    :param test_mode: Tempest mode smoke (default), full, ..
    :return: void
    """
    logger.info('starting {} Tempest ...'.format(test_mode))

    cmd_line = "rally verify start {}".format(test_mode)
    logger.debug('running command line : {}'.format(cmd_line))
    cmd = os.popen(cmd_line)
    task_id = get_tempest_id(cmd.read())
    logger.debug('task_id : {}'.format(task_id))

    if task_id is None:
        logger.error("failed to retrieve task_id")
    exit(-1)

    """ check for result directory and create it otherwise """
    if not os.path.exists(RESULTS_DIR):
        logger.debug('does not exists, we create it'.format(RESULTS_DIR))
        os.makedirs(RESULTS_DIR)

    """ write log report file """
    report_file_name = '{}opnfv-tempest.log'.format(RESULTS_DIR)
    cmd_line = "rally verify detailed {} > {} ".format(task_id, report_file_name)
    logger.debug('running command line : {}'.format(cmd_line))
    os.popen(cmd_line)


def run_task(test_name):
    """
    the "main" function of the script who lunch rally for a task
    :param test_name: name for the rally test
    :return: void
    """
    logger.info('starting {} test ...'.format(test_name))

    """ check directory for scenarios test files or retrieve from git otherwise"""
    proceed_test = True
    test_file_name = '{}opnfv-{}.json'.format(SCENARIOS_DIR, test_name)
    if not os.path.exists(test_file_name):
        logger.debug('{} does not exists'.format(test_file_name))
        proceed_test = retrieve_test_cases_file(test_name, SCENARIOS_DIR)

    """ we do the test only if we have a scenario test file """
    if proceed_test:
        logger.debug('Scenario fetched from : {}'.format(test_file_name))
        cmd_line = "rally task start --abort-on-sla-failure %s" % test_file_name
        logger.debug('running command line : {}'.format(cmd_line))
        cmd = os.popen(cmd_line)
        task_id = get_task_id(cmd.read())
        logger.debug('task_id : {}'.format(task_id))

        if task_id is None:
            logger.error("failed to retrieve task_id")
            exit(-1)

        """ check for result directory and create it otherwise """
        if not os.path.exists(RESULTS_DIR):
            logger.debug('does not exists, we create it'.format(RESULTS_DIR))
            os.makedirs(RESULTS_DIR)

        """ write html report file """
        report_file_name = '{}opnfv-{}.html'.format(RESULTS_DIR, test_name)
        cmd_line = "rally task report %s --out %s" % (task_id, report_file_name)
        logger.debug('running command line : {}'.format(cmd_line))
        os.popen(cmd_line)

        """ get and save rally operation JSON result """
        cmd_line = "rally task results %s" % task_id
        logger.debug('running command line : {}'.format(cmd_line))
        cmd = os.popen(cmd_line)
        json_results = cmd.read()
        with open('{}opnfv-{}.json'.format(RESULTS_DIR, test_name), 'w') as f:
            logger.debug('saving json file')
            f.write(json_results)
            logger.debug('saving json file2')

        """ parse JSON operation result """
        if task_succeed(json_results):
            print 'Test OK'
        else:
            print 'Test KO'
    else:
        logger.error('{} test failed, unable to fetch a scenario test file'.format(test_name))


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
            if not (test_name == 'all' or test_name == 'tempest' or test_name == 'heat' or test_name == 'smoke' or test_name == 'vm' ):
                print(test_name)
                run_task(test_name)
    else:
        print(args.test_name)
        if args.test_name == 'tempest':
            run_tempest()
        else:
            run_task(args.test_name)

if __name__ == '__main__':
    main()
