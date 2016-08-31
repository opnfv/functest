#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# valentin.boucher@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

""" global variables """

from datetime import datetime as dt
import json
import os
import os.path
import re
import shutil
import subprocess
import sys
import urllib2
import dns.resolver

import functest.ci.tier_builder as tb
from git import Repo
import requests
import yaml


REPOS_DIR = os.getenv('repos_dir')
FUNCTEST_REPO = ("%s/functest/" % REPOS_DIR)


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


def get_db_url(logger=None):
    """
    Returns DB URL
    """
    with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
        functest_yaml = yaml.safe_load(f)
    f.close()
    db_url = functest_yaml.get("results").get("test_db_url")
    return db_url


def logger_test_results(logger, project, case_name, status, details):
    pod_name = get_pod_name(logger)
    scenario = get_scenario(logger)
    version = get_version(logger)
    build_tag = get_build_tag(logger)

    logger.info("\n"
                "****************************************\n"
                "\t %(p)s/%(n)s results \n\n"
                "****************************************\n"
                "DB:\t%(db)s\n"
                "pod:\t%(pod)s\n"
                "version:\t%(v)s\n"
                "scenario:\t%(s)s\n"
                "status:\t%(c)s\n"
                "build tag:\t%(b)s\n"
                "details:\t%(d)s\n"
                % {
                    'p': project,
                    'n': case_name,
                    'db': get_db_url(),
                    'pod': pod_name,
                    'v': version,
                    's': scenario,
                    'c': status,
                    'b': build_tag,
                    'd': details,
                })


def push_results_to_db(project, case_name, logger,
                       start_date, stop_date, criteria, details):
    """
    POST results to the Result target DB
    """
    # Retrieve params from CI and conf
    url = get_db_url(logger) + "/results"

    try:
        installer = os.environ['INSTALLER_TYPE']
        scenario = os.environ['DEPLOY_SCENARIO']
        pod_name = os.environ['NODE_NAME']
        build_tag = os.environ['BUILD_TAG']
    except KeyError as e:
        msg = "Please set env var: " + str(e)
        if logger:
            logger.error(msg)
        else:
            print(msg)
        return False
    rule = "daily-(.+?)-[0-9]*"
    m = re.search(rule, build_tag)
    if m:
        version = m.group(1)
    else:
        msg = "Please fix BUILD_TAG env var: " + build_tag
        if logger:
            logger.error(msg)
        else:
            print(msg)
        return False
    test_start = dt.fromtimestamp(start_date).strftime('%Y-%m-%d %H:%M:%S')
    test_stop = dt.fromtimestamp(stop_date).strftime('%Y-%m-%d %H:%M:%S')

    params = {"project_name": project, "case_name": case_name,
              "pod_name": pod_name, "installer": installer,
              "version": version, "scenario": scenario, "criteria": criteria,
              "build_tag": build_tag, "start_date": test_start,
              "stop_date": test_stop, "details": details}

    error = None
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url, data=json.dumps(params), headers=headers)
        if logger:
            logger.debug(r)
        r.raise_for_status()
    except requests.RequestException as exc:
        if 'r' in locals():
            error = ("Pushing Result to DB(%s) failed: %s" %
                     (r.url, r.content))
        else:
            error = ("Pushing Result to DB(%s) failed: %s" % (url, exc))
    except Exception as e:
        error = ("Error [push_results_to_db("
                 "DB: '%(db)s', "
                 "project: '%(project)s', "
                 "case: '%(case)s', "
                 "pod: '%(pod)s', "
                 "version: '%(v)s', "
                 "scenario: '%(s)s', "
                 "criteria: '%(c)s', "
                 "build_tag: '%(t)s', "
                 "details: '%(d)s')]: "
                 "%(error)s" %
                 {
                     'db': url,
                     'project': project,
                     'case': case_name,
                     'pod': pod_name,
                     'v': version,
                     's': scenario,
                     'c': criteria,
                     't': build_tag,
                     'd': details,
                     'error': e
                 })
    finally:
        if error:
            if logger:
                logger.error(error)
            else:
                print error
            return False
        return True


def get_resolvconf_ns():
    """
    Get nameservers from current resolv.conf
    """
    nameservers = []
    rconf = open("/etc/resolv.conf", "r")
    line = rconf.readline()
    resolver = dns.resolver.Resolver()
    while line:
        ip = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
        if ip:
            resolver.nameservers = [str(ip)]
            try:
                result = resolver.query('opnfv.org')[0]
                if result != "":
                    nameservers.append(ip.group())
            except dns.exception.Timeout:
                pass
        line = rconf.readline()
    return nameservers


def get_ci_envvars():
    """
    Get the CI env variables
    """
    ci_env_var = {
        "installer": os.environ.get('INSTALLER_TYPE'),
        "scenario": os.environ.get('DEPLOY_SCENARIO')}
    return ci_env_var


def execute_command(cmd, logger=None,
                    exit_on_error=True,
                    info=False,
                    error_msg="",
                    verbose=True):
    if not error_msg:
        error_msg = ("The command '%s' failed." % cmd)
    msg_exec = ("Executing command: '%s'" % cmd)
    if verbose:
        if logger:
            if info:
                logger.info(msg_exec)
            else:
                logger.debug(msg_exec)
        else:
            print(msg_exec)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        line = line.replace('\n', '')
        if logger:
            if info:
                logger.info(line)
            else:
                logger.debug(line)
        else:
            print line
            sys.stdout.flush()
    p.stdout.close()
    returncode = p.wait()
    if returncode != 0:
        if verbose:
            if logger:
                logger.error(error_msg)
            else:
                print(error_msg)
        if exit_on_error:
            sys.exit(1)

    return returncode


def get_deployment_dir(logger=None):
    """
    Returns current Rally deployment directory
    """
    with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
        functest_yaml = yaml.safe_load(f)
    f.close()
    deployment_name = functest_yaml.get("rally").get("deployment_name")
    rally_dir = functest_yaml.get("general").get("directories").get(
        "dir_rally_inst")
    cmd = ("rally deployment list | awk '/" + deployment_name +
           "/ {print $2}'")
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    deployment_uuid = p.stdout.readline().rstrip()
    if deployment_uuid == "":
        if logger:
            logger.error("Rally deployment not found.")
        exit(-1)
    deployment_dir = (rally_dir + "/tempest/for-deployment-" +
                      deployment_uuid)
    return deployment_dir


def get_criteria_by_test(testname):
    criteria = ""
    file = get_testcases_file()
    tiers = tb.TierBuilder("", "", file)
    for tier in tiers.get_tiers():
        for test in tier.get_tests():
            if test.get_name() == testname:
                criteria = test.get_criteria()

    return criteria


# ----------------------------------------------------------
#
#               YAML UTILS
#
# -----------------------------------------------------------
def get_parameter_from_yaml(parameter, file=None):
    """
    Returns the value of a given parameter in config_functest.yaml
    parameter must be given in string format with dots
    Example: general.openstack.image_name
    """
    if file is None:
        file = os.environ["CONFIG_FUNCTEST_YAML"]
    with open(file) as f:
        functest_yaml = yaml.safe_load(f)
    f.close()
    value = functest_yaml
    for element in parameter.split("."):
        value = value.get(element)
        if value is None:
            raise ValueError("The parameter %s is not defined in"
                             " config_functest.yaml" % parameter)
    return value


def check_success_rate(case_name, success_rate):
    success_rate = float(success_rate)
    criteria = get_criteria_by_test(case_name)

    def get_criteria_value(op):
        return float(criteria.split(op)[1].rstrip('%'))

    status = 'FAIL'
    ops = ['==', '>=']
    for op in ops:
        if op in criteria:
            c_value = get_criteria_value(op)
            if eval("%s %s %s" % (success_rate, op, c_value)):
                status = 'PASS'
            break

    return status


def merge_dicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(merge_dicts(dict1[k], dict2[k])))
            else:
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


def check_test_result(test_name, ret, start_time, stop_time):
    def get_criteria_value():
        return get_criteria_by_test(test_name).split('==')[1].strip()

    status = 'FAIL'
    if str(ret) == get_criteria_value():
        status = 'PASS'

    details = {
        'timestart': start_time,
        'duration': round(stop_time - start_time, 1),
        'status': status,
    }

    return status, details


def get_testcases_file():
    return FUNCTEST_REPO + "/ci/testcases.yaml"
