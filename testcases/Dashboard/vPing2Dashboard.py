#!/usr/bin/python
#
# Copyright (c) 2015 Orange
# morgan.richomme@orange.com
#
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# This script is used to get data from test DB
# and format them into a json format adapted for a dashboard
#
# v0.1: basic example
#
import logging
import argparse
import pprint
import json
import dashboard_utils
import os
import yaml
from dashboard_utils import TestCriteria

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser()
parser.add_argument("repo_path", help="Path to the repository")
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
args = parser.parse_args()

""" logging configuration """
logger = logging.getLogger('config_functest')
logger.setLevel(logging.DEBUG)

if not os.path.exists(args.repo_path):
    logger.error("Repo directory not found '%s'" % args.repo_path)
    exit(-1)

with open(args.repo_path+"testcases/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

""" global variables """
# Directories
HOME = os.environ['HOME']+"/"
REPO_PATH = args.repo_path
TEST_DB = functest_yaml.get("results").get("test_db_url")


def format_data_for_dashboard(criteria):

    # Get results
    myDataResults = dashboard_utils.get_results(TEST_DB, criteria)

    # Depending on the use case, json for dashboarding is customized
    # depending on the graph you want to show

    test_data = [{'description': 'vPing results for Dashboard'}]

    # Graph 1: Duration = f(time)
    # ***************************
    new_element = []
    for data in myDataResults:
        new_element.append({'x': data['creation_date'],
                            'y': data['details']['duration']})

    test_data.append({'name': "vPing duration",
                      'info': {'type': "graph",
                               'xlabel': 'time',
                               'ylabel': 'duration (s)'},
                      'data_set': new_element})

    # Graph 2: bar
    # ************
    nbTest = 0
    nbTestOk = 0

    for data in myDataResults:
        nbTest += 1
        if data['details']['status'] == "OK":
            nbTestOk += 1

    test_data.append({'name': "vPing status",
                      'info': {"type": "bar"},
                      'data_set': [{'Nb tests': nbTest,
                                    'Nb Success': nbTestOk}]})

    # Generate json file

    fileName = criteria.format()
    logger.debug("Generate json file:" + fileName)

    with open(fileName, "w") as outfile:
        json.dump(test_data, outfile, indent=4)


def generateJson():
    # TODO create the loop to provide all the json files
    test_name = 'functest'
    test_case = 'vPing'
    # pod_id = 1
    # test_version = 'Arno master'
    # test_installer = 'fuel'
    # test_retention = 30

    pods = dashboard_utils.get_pods(TEST_DB)
    versions = ['ArnoR1', 'ArnoSR1', 'all']
    installers = ['fuel', 'foreman', 'all']
    test_durations = [90, 365, 'all']  # not available through the API yet

    # For all the PoDs
    for pod in pods:
        # all the versions
        for version in versions:
            # all the installers
            for installer in installers:
                # all the retention time
                for test_duration in test_durations:

                    criteria = TestCriteria()
                    criteria.setCriteria(test_name, test_case, pod,
                                         test_duration, version, installer)
                    format_data_for_dashboard(criteria)
