#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# valentin.boucher@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import json
import os
import os.path
import re
import requests
import shutil
import socket
import subprocess
import urllib2
from git import Repo


# ----------------------------------------------------------
#
#               INTERNET UTILS
#
# -----------------------------------------------------------
def check_internet_connectivity(url='http://www.opnfv.org/'):
    """
    Check if there is access to the internet
    """
    try:
        urllib2.urlopen(url, timeout=5)
        return True
    except urllib2.URLError:
        return False


def download_url(url, dest_path):
    """
    Download a file to a destination path given a URL
    """
    name = url.rsplit('/')[-1]
    dest = dest_path + "/" + name
    try:
        response = urllib2.urlopen(url)
    except (urllib2.HTTPError, urllib2.URLError):
        return False

    with open(dest, 'wb') as f:
        shutil.copyfileobj(response, f)
    return True


# ----------------------------------------------------------
#
#               CI UTILS
#
# -----------------------------------------------------------
def get_git_branch(repo_path):
    """
    Get git branch name
    """
    repo = Repo(repo_path)
    branch = repo.active_branch
    return branch.name


def get_installer_type(logger=None):
    """
    Get installer type (fuel, apex, joid, compass)
    """
    try:
        installer = os.environ['INSTALLER_TYPE']
    except KeyError:
        if logger:
            logger.error("Impossible to retrieve the installer type")
        installer = "Unknown_installer"

    return installer


def get_scenario(logger=None):
    """
    Get scenario
    """
    try:
        scenario = os.environ['DEPLOY_SCENARIO']
    except KeyError:
        if logger:
            logger.error("Impossible to retrieve the scenario")
        scenario = "Unknown_scenario"

    return scenario


def get_version(logger=None):
    """
    Get version
    """
    # Use the build tag to retrieve the version
    # By default version is unknown
    # if launched through CI the build tag has the following format
    # jenkins-<project>-<installer>-<pod>-<job>-<branch>-<id>
    # e.g. jenkins-functest-fuel-opnfv-jump-2-daily-master-190
    # use regex to match branch info
    rule = "daily-(.+?)-[0-9]*"
    build_tag = get_build_tag(logger)
    m = re.search(rule, build_tag)
    if m:
        return m.group(1)
    else:
        return "unknown"


def get_pod_name(logger=None):
    """
    Get PoD Name from env variable NODE_NAME
    """
    try:
        return os.environ['NODE_NAME']
    except KeyError:
        if logger:
            logger.error(
                "Unable to retrieve the POD name from environment. " +
                "Using pod name 'unknown-pod'")
        return "unknown-pod"


def get_build_tag(logger=None):
    """
    Get build tag of jenkins jobs
    """
    try:
        build_tag = os.environ['BUILD_TAG']
    except KeyError:
        if logger:
            logger.error("Impossible to retrieve the build tag")
        build_tag = "unknown_build_tag"

    return build_tag


def push_results_to_db(db_url, project, case_name, logger, pod_name,
                       version, scenario, criteria, build_tag, payload):
    """
    POST results to the Result target DB
    """
    url = db_url + "/results"
    installer = get_installer_type(logger)
    params = {"project_name": project, "case_name": case_name,
              "pod_name": pod_name, "installer": installer,
              "version": version, "scenario": scenario, "criteria": criteria,
              "build_tag": build_tag, "details": payload}

    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url, data=json.dumps(params), headers=headers)
        if logger:
            logger.debug(r)
        return True
    except Exception, e:
        print "Error [push_results_to_db('%s', '%s', '%s', " + \
              "'%s', '%s', '%s', '%s', '%s', '%s')]:" \
              % (db_url, project, case_name, pod_name, version,
                  scenario, criteria, build_tag, payload), e
        return False


def get_resolvconf_ns():
    """
    Get nameservers from current resolv.conf
    """
    nameservers = []
    rconf = open("/etc/resolv.conf", "r")
    line = rconf.readline()
    while line:
        ip = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ip:
            result = sock.connect_ex((ip.group(), 53))
            if result == 0:
                nameservers.append(ip.group())
        line = rconf.readline()
    return nameservers


def getTestEnv(test, functest_yaml):
    """
    Get the config of the testcase based on functest_config.yaml
      2 options
        - test = test project e.g; ovno
        - test = testcase e.g. functest/odl
       look for the / to see if it is a test project or a testcase
    """
    try:
        TEST_ENV = functest_yaml.get("test-dependencies")

        if test.find("/") < 0:
            config_test = TEST_ENV[test]
        else:
            test_split = test.split("/")
            testproject = test_split[0]
            testcase = test_split[1]
            config_test = TEST_ENV[testproject][testcase]
    except KeyError:
        # if not defined in dependencies => no dependencies
        config_test = ""
    except Exception, e:
        print "Error [getTestEnv]:", e

    return config_test


def get_ci_envvars():
    """
    Get the CI env variables
    """
    ci_env_var = {
        "installer": os.environ.get('INSTALLER_TYPE'),
        "scenario": os.environ.get('DEPLOY_SCENARIO')}
    return ci_env_var


def isTestRunnable(test, functest_yaml):
    """
    Return True if the test is runnable in the current scenario
    """
    # By default we assume that all the tests are always runnable...
    is_runnable = True
    # Retrieve CI environment
    ci_env = get_ci_envvars()
    # Retrieve test environement from config file
    test_env = getTestEnv(test, functest_yaml)

    # if test_env not empty => dependencies to be checked
    if test_env is not None and len(test_env) > 0:
        # possible criteria = ["installer", "scenario"]
        # consider test criteria from config file
        # compare towards CI env through CI en variable
        for criteria in test_env:
            if re.search(test_env[criteria], ci_env[criteria]) is None:
                # print "Test "+ test + " cannot be run on the environment"
                is_runnable = False
    return is_runnable


def generateTestcaseList(functest_yaml):
    """
    Generate a test file with the runnable test according to
    the current scenario
    """
    test_list = ""
    # get testcases
    testcase_list = functest_yaml.get("test-dependencies")
    projects = testcase_list.keys()

    for project in projects:
        testcases = testcase_list[project]
        # 1 or 2 levels for testcases project[/case]l
        # if only project name without controller or scenario
        # => shall be runnable on any controller/scenario
        if testcases is None:
            test_list += project + " "
        else:
            for testcase in testcases:
                if testcase == "installer" or testcase == "scenario":
                    # project (1 level)
                    if isTestRunnable(project, functest_yaml):
                        test_list += project + " "
                else:
                    # project/testcase (2 levels)
                    thetest = project + "/" + testcase
                    if isTestRunnable(thetest, functest_yaml):
                        test_list += testcase + " "

    # sort the list to execute the test in the right order
    test_order_list = functest_yaml.get("test_exec_priority")
    test_sorted_list = ""
    for test in test_order_list:
        if test_order_list[test] in test_list:
            test_sorted_list += test_order_list[test] + " "

    # create a file that could be consumed by run-test.sh
    # this method is used only for CI
    # so it can be run only in container
    # reuse default conf directory to store the list of runnable tests
    file = open("/home/opnfv/functest/conf/testcase-list.txt", 'w')
    file.write(test_sorted_list)
    file.close()

    return test_sorted_list


def execute_command(cmd, logger=None, exit_on_error=True):
    """
    Execute Linux command
        prints stdout to a file and depending on if there
        is a logger defined, it will print it or not.
    """
    if logger:
        logger.debug('Executing command : {}'.format(cmd))
    output_file = "output.txt"
    f = open(output_file, 'w+')
    p = subprocess.call(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)
    f.close()
    f = open(output_file, 'r')
    result = f.read()
    if result != "" and logger:
        logger.debug(result)
    if p == 0:
        return True
    else:
        if logger:
            logger.error("Error when executing command %s" % cmd)
        if exit_on_error:
            exit(-1)
        return False
