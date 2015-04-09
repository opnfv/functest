#
# Copyright (c) 2015 Orange
# guyrodrigue.koffi@orange.com
# morgan.richomme@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
#!/usr/bin/python
import re, json, os, sys

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

    """ directory for test scenarios files"""
    test_dir = '/home/ubuntu/rally/samples/tasks/scenarios/opnfv'
    test_file_name = "/home/ubuntu/rally/samples/tasks/scenarios/opnfv/opnfv-%s.json" % test_name
    print test_file_name

    cmd = os.popen("rally task start --abort-on-sla-failure %s" % test_file_name)
    task_id = get_task_id(cmd.read())

    if task_id is None:
        print "./run_rally : failed to retrieve task_id"
        exit(-1)

    report_file_name = "/home/ubuntu/rally/opnfv-%s-%s.html" % (test_name, test_date)
    
    os.popen("rally task report %s --out %s" % (task_id, report_file_name))
    cmd = os.popen("rally task results %s" % task_id)
    if task_succeed(cmd.read()):
        print "OK"
    else:
        print "KO"


def main():
    """ configure script """
    tests = ('authenticate','glance','heat','keystone','neutron','nova','tempest','vm', 'all',)


    if len(sys.argv) != 2:
        print "./run_rally [", tests, "]"
        exit(-1)
    test_name = sys.argv[1]

    if not (test_name in tests):
        print "argument not valid"
        exit(-1)

    if test_name == "all":
        #run test for all tests
        pass
    else:
        run_task(test_name)


if __name__ == '__main__':
    main()


