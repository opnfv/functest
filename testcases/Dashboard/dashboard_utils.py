# copyrighi (c) 2015 Orange

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
import json
import requests
from vPing2Dashboard import format_vPing_for_dashboard


class TestCriteria:

    """ describes the test criteria platform """
    def __init__(self):
        self.project = ''
        self.testcase = ''
        self.pod_name = 'all'
        self.duration = 'all'
        self.version = 'all'
        self.installer = 'all'

    def setCriteria(self, project, testcase, pod_name,
                    duration, version, installer):
        self.project = project
        self.testcase = testcase
        self.pod_name = pod_name
        self.duration = duration
        self.version = version
        self.installer = installer

    def format_criteria(self, name):
        if(name == 'all' or name == 0):
            return ""
        else:
            if(type(name) == int):
                return "_" + str(name)
            else:
                return "_" + name

    def format(self):
        pod_name = self.format_criteria(self.pod_name)
        version_name = self.format_criteria(self.version)
        installer_name = self.format_criteria(self.installer)
        duration_name = self.format_criteria(self.duration)
        try:
            fileName = "result_" + self.project + "_" + self.testcase + \
                       pod_name + version_name + installer_name + \
                       duration_name + ".json"
        except:
            print "Impossible to format json file name"
        return fileName


def get_pods(db_url):
    # retrieve the list of pods
    url = db_url + "/pods"
    # Build headers
    headers = {'Content-Type': 'application/json'}

    try:
        db_data = requests.get(url, headers=headers)
        # Get result as a json object
        pods_data = json.loads(db_data.text)
        # Get results
        pods = pods_data['pods']
        pods_table = []
        for pod in pods:
            # cast int becase otherwise API retrieve 1.0
            # TODO check format with API
            pods_table.append(pod['name'])

        pods_table.append('all')
        return pods_table
    except:
        print "Error retrieving the list of PODs"
        return None


def get_versions(db_url):
    # retrieve the list of versions
    # TODO not supported in API yet
    url = db_url + "/results"
    # Build headers
    headers = {'Content-Type': 'application/json'}

    try:
        db_data = requests.get(url, headers=headers)
        # Get result as a json object
        versions_data = json.loads(db_data.text)
        # Get results
        versions = versions_data['test_results']
        versions_table = []
        for version in versions:
            if (version['version'] is not None):
                versions_table.append(version['version'])

        versions_table.append('all')
        versions_table = sorted(set(versions_table))
        return versions_table
    except:
        print "Error retrieving the list of OPNFV versions"
        return None


def get_installers(db_url):
    # retrieve the list of installers
    # TODO not supported in API yet
    url = db_url + "/results"
    # Build headers
    headers = {'Content-Type': 'application/json'}

    try:
        db_data = requests.get(url, headers=headers)
        # Get result as a json object
        installers_data = json.loads(db_data.text)
        # Get results
        installers = installers_data['test_results']

        installers_table = []
        for installer in installers:
            if (installer['installer'] is not None):
                installers_table.append(installer['installer'])

        installers_table.append('all')
        installers_table = sorted(set(installers_table))
        return installers_table
    except:
        print "Error retrieving the list of OPNFV installers"
        return None


def get_testcases(db_url, project):
    # retrieve the list of pods
    url = db_url + "/test_projects/" + project + "/cases"
    # Build headers
    headers = {'Content-Type': 'application/json'}

    try:
        db_data = requests.get(url, headers=headers)
        # Get result as a json object
        testcases_data = json.loads(db_data.text)
        # Get results
        testcases = testcases_data['test_cases']
        testcases_table = []
        for testcase in testcases:
            testcases_table.append(testcase['name'])

        testcases_table.append('all')

        return testcases_table
    except:
        print "Error retrieving the list of testcases"
        return None


def get_results(db_url, test_criteria):

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
    # params = {"pod_name":pod, "testcase":testcase}
    # filter_date = days # data from now - days

    test_project = test_criteria.project
    testcase = test_criteria.testcase
    period = test_criteria.duration
    version = test_criteria.version
    installer = test_criteria.installer
    pod = test_criteria.pod_name

    # TODO complete params (installer type, testcase, version )
    # need API to be up to date
    # we assume that criteria could be used at the API level
    # no need to processing on date for instance
    #  params = {"pod_name": pod_name}

    # Build headers
    headers = {'Content-Type': 'application/json'}

    # build the request
    # if criteria is all => remove criteria
    url = db_url + "/results?project=" + test_project + "&case=" + testcase

    if (pod != "all"):
        url += "&pod=" + pod
    if (installer != "all"):
        url += "&installer=" + installer
    if (version != "all"):
        url += "&version=" + version
    url += "&period=" + str(period)

    # Send Request to Test DB
    myData = requests.get(url, headers=headers)

    # Get result as a json object
    myNewData = json.loads(myData.text)

    # Get results
    myDataResults = myNewData['test_results']

    return myDataResults


def generateJson(test_name, test_case, db_url):
    # pod_id = "opnfv-jump-1'
    # test_version = 'Arno master'
    # test_installer = 'fuel'
    # test_retention = 30

    pods = get_pods(db_url)
    versions = get_versions(db_url)
    installers = get_installers(db_url)

    test_durations = [90, 365, 0]  # 0 means since the beginning

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


def format_data_for_dashboard(criteria):

    # Depending on the use case, json for dashboarding is customized
    # depending on the graph you want to show

    if (criteria.testcase == "vPing"):
        format_vPing_for_dashboard(criteria)
