#!/usr/bin/python
#
# Authors:
# - peter.bandzi@cisco.com
# - morgan.richomme@orange.com
#
# src: Peter Bandzi
# https://github.com/pbandzi/parse-robot/blob/master/convert_robot_to_json.py
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# 0.1: This script boots the VM1 and allocates IP address from Nova
# Later, the VM2 boots then execute cloud-init to ping VM1.
# After successful ping, both the VMs are deleted.
# 0.2: measure test duration and publish results under json format
# 0.3: adapt push 2 DB after Test API refacroting
#
#

import getopt
import json
import sys
import time
import xmltodict

import functest.utils.functest_utils as functest_utils


def usage():
    print """Usage:
    python odlreport2db.py --xml=<output.xml> --pod=<pod name>
                           --installer=<installer> --database=<database url>
                           --scenario=<scenario>
    -x, --xml   xml file generated by robot test
    -p, --pod   POD name where the test come from
    -i, --installer
    -s, --scenario
    -h, --help  this message
    """
    sys.exit(2)


def populate_detail(test):
    detail = {}
    detail['test_name'] = test['@name']
    detail['test_status'] = test['status']
    detail['test_doc'] = test['doc']
    return detail


def parse_test(tests, details):
    try:
        for test in tests:
            details.append(populate_detail(test))
    except TypeError:
        # tests is not iterable
        details.append(populate_detail(tests))
    return details


def parse_suites(suites):
    data = {}
    details = []
    for suite in suites:
        a = suite['suite']
        if type(a) == list:
            for b in a:
                data['details'] = parse_test(b['test'], details)
        else:
            data['details'] = parse_test(a['test'], details)

        # data['details'] = parse_test(suite['test'], details)
    # suites is not iterable
    return data


def main(argv):
    (xml_file, pod, installer, scenario) = None, None, None, None
    try:
        opts, args = getopt.getopt(argv,
                                   'x:p:i:s:h',
                                   ['xml=', 'pod=',
                                    'installer=',
                                    'scenario=',
                                    'help'])
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-x', '--xml'):
            xml_file = arg
        elif opt in ('-p', '--pod'):
            pod = arg
        elif opt in ('-i', '--installer'):
            installer = arg
        elif opt in ('-s', '--scenario'):
            scenario = arg
        else:
            usage()

    if not all(x is not None for x in (xml_file, pod, installer, scenario)):
        usage()

    with open(xml_file, "r") as myfile:
        xml_input = myfile.read().replace('\n', '')

    # dictionary populated with data from xml file
    all_data = xmltodict.parse(xml_input)['robot']

    try:
        data = parse_suites(all_data['suite']['suite'])
        data['description'] = all_data['suite']['@name']
        data['version'] = all_data['@generator']
        data['test_project'] = "functest"
        data['case_name'] = "odl"
        data['pod_name'] = pod
        data['installer'] = installer

        json.dumps(data, indent=4, separators=(',', ': '))

        # example:
        # python odlreport2db.py -x ~/Pictures/Perso/odl/output3.xml
        #                        -i fuel
        #                        -p opnfv-jump-2
        #                        -s os-odl_l2-ha

        # success criteria for ODL = 100% of tests OK
        status = "FAIL"
        # TODO as part of the tests are executed before in the bash
        # start and stoptime have no real meaning
        start_time = time.time()
        stop_time = start_time
        tests_passed = 0
        tests_failed = 0
        for v in data['details']:
            if v['test_status']['@status'] == "PASS":
                tests_passed += 1
            else:
                tests_failed += 1

        if (tests_failed < 1):
            status = "PASS"

        functest_utils.push_results_to_db(data['test_project'],
                                          data['case_name'],
                                          None,
                                          start_time,
                                          stop_time,
                                          status,
                                          data)

    except:
        print("Error pushing ODL results into DB '%s'" % sys.exc_info()[0])


if __name__ == "__main__":
    main(sys.argv[1:])
