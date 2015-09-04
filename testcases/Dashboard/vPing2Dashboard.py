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
import requests

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
args = parser.parse_args()

""" logging configuration """
logger = logging.getLogger('vPing2DashBoard')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter  # retrieve info from DB
('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_data(test_project, testcase, pod_id, days, version, installerType):
    # ugly hard coding => TODO use yaml config file
    url = "http://213.77.62.197:80/results"

    # use param to filter request to result DB
    # if not precised => no filter
    # filter criteria:
    # - POD
    # - versions
    # - installers
    # - testcase
    # - test projects
    # - timeframe (last 30 days, 365 days, since beginning of the project)
    # e.g.
    # - vPing tests since 2 months
    # - Tempest tests on LF POD2 fuel based / Arno stable since the beginning
    # - yardstick tests on any POD since 30 days
    # - Qtip tests on dell-test1 POD
    #
    # params = {"pod_id":pod_id, "testcase":testcase}
    # filter_date = days # data from now - days

    # TODO complete params (installer type, testcase, version )
    params = {"pod_id": 1}

    # Build headers
    headers = {'Content-Type': 'application/json'}

    # Send Request to Test DB
    myData = requests.get(url, data=json.dumps(params), headers=headers)
    # Get result as a json object
    myNewData = json.loads(myData.text)

    # Get results
    myDataResults = myNewData['test_results']

    # Depending on the use case, json for dashboarding is customized
    # depending on the graph you want to show

    test_data = [{'description': 'vPing results for Dashboard'}]

    # Graph 1: Duration = f(time)
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
    nbTest = 0
    nbTestOk = 0

    for data in myDataResults:
        nbTest += 1
        if data['details']['status'] == "OK":
            nbTestOk += 1

    # Generate json file
    # TODO complete with other criteria
    fileName = "result-" + test_project + "-" + testcase + "-" + str(days) + "-" + str(pod_id) + "-status.json"

    test_data.append({'name': "vPing status",
                      'info': {"type": "bar"},
                      'data_set': [{'Nb tests': nbTest,
                                    'Nb Success': nbTestOk}]})

    fileName = "result-" + test_project + "-" + testcase + ".json"

    with open(fileName, "w") as outfile:
        json.dump(test_data, outfile, indent=4)


def main():
    get_data('functest', 'vPing', 1, 30, 'Arno master', 'fuel')


if __name__ == '__main__':
    main()
