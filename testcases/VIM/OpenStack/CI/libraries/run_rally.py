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
import re, json, os, sys, urllib2
 
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
 
    """ get the date """
    cmd = os.popen("date '+%d%m%Y_%H%M'")
    test_date = cmd.read().rstrip()
 
    """ check directory for test scenarios files or retrieve from git otherwise"""
    tests_path = "./scenarios"
    test_file_name = '{}/opnfv-{}.json'.format(tests_path, test_name)
    if not os.path.exists(test_file_name):
        retrieve_test_cases_file(test_name, tests_path)
	print "Scenario successfully downloaded"
 
    print "Start test..."
    cmd = os.popen("rally task start --abort-on-sla-failure %s" % test_file_name)
    task_id = get_task_id(cmd.read())
 
    if task_id is None:
        print "./run_rally : failed to retrieve task_id"
        exit(-1)
 
    """ check for result directory and create it otherwise """
    report_path = "./results"
    if not os.path.exists(report_path):
        os.makedirs(report_path)
 
    report_file_name = '{}/opnfv-{}-{}.html'.format(report_path, test_name, test_date)
    
    os.popen("rally task report %s --out %s" % (task_id, report_file_name))
    cmd = os.popen("rally task results %s" % task_id)
    if task_succeed(cmd.read()):
        print "OK"
    else:
        print "KO"
 
 
def retrieve_test_cases_file(test_name, tests_path):
    """
    Retrieve from github the sample test files
    :return: void
    """
 
    """ do not add the "/" at the end """
    url_base = "https://git.opnfv.org/cgit/functest/plain/testcases/VIM/OpenStack/CI/suites"
 
    test_file_name = 'opnfv-{}.json'.format(test_name)
    print 'fetching {}/{} ...'.format(url_base, test_file_name)
    response = urllib2.urlopen('{}/{}'.format(url_base, test_file_name))
    file_raw = response.read()
 
    """ check if the test path existe otherwise we create it """
    if not os.path.exists(tests_path):
        os.makedirs(tests_path)
 
    with open('{}/{}'.format(tests_path,test_file_name), 'w') as file:
        file.write(file_raw)
 
 
def main():
    """ configure script """
    tests = ['authenticate','glance','heat','keystone','neutron','nova','tempest','vm', 'all'];
 
 
    if len(sys.argv) != 2:
        options = '{d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} | {d[5]} | {d[6]} | {d[7]} | {d[8]}'.format(d=tests)
        print "./run_rally [", options, "]"
        exit(-1)
    test_name = sys.argv[1]
 
    if not (test_name in tests):
        print "argument not valid"
        exit(-1)
 
    if test_name == "all":
        for test_name in tests:
            if not (test_name == 'all' or test_name == 'tempest'):
                print(test_name)
                run_task(test_name)
 
    else:
        run_task(test_name)
 
 
if __name__ == '__main__':
    main()

