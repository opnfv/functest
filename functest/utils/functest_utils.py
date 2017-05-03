#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# valentin.boucher@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
import functools
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib2
from datetime import datetime as dt

import dns.resolver
import requests
import yaml
from git import Repo

from functest.utils import decorators
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("functest_utils").getLogger()


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


def get_installer_type():
    """
    Get installer type (fuel, apex, joid, compass)
    """
    try:
        installer = os.environ['INSTALLER_TYPE']
    except KeyError:
        logger.error("Impossible to retrieve the installer type")
        installer = "Unknown_installer"

    return installer


def get_scenario():
    """
    Get scenario
    """
    try:
        scenario = os.environ['DEPLOY_SCENARIO']
    except KeyError:
        logger.info("Impossible to retrieve the scenario."
                    "Use default os-nosdn-nofeature-noha")
        scenario = "os-nosdn-nofeature-noha"

    return scenario


def get_version():
    """
    Get version
    """
    # Use the build tag to retrieve the version
    # By default version is unknown
    # if launched through CI the build tag has the following format
    # jenkins-<project>-<installer>-<pod>-<job>-<branch>-<id>
    # e.g. jenkins-functest-fuel-opnfv-jump-2-daily-master-190
    # jenkins-functest-fuel-baremetal-weekly-master-8
    # use regex to match branch info
    rule = "(dai|week)ly-(.+?)-[0-9]*"
    build_tag = get_build_tag()
    m = re.search(rule, build_tag)
    if m:
        return m.group(2)
    else:
        return "unknown"


def get_pod_name():
    """
    Get PoD Name from env variable NODE_NAME
    """
    try:
        return os.environ['NODE_NAME']
    except KeyError:
        logger.info(
            "Unable to retrieve the POD name from environment. " +
            "Using pod name 'unknown-pod'")
        return "unknown-pod"


def get_build_tag():
    """
    Get build tag of jenkins jobs
    """
    try:
        build_tag = os.environ['BUILD_TAG']
    except KeyError:
        logger.info("Impossible to retrieve the build tag")
        build_tag = "none"

    return build_tag


def get_db_url():
    """
    Returns DB URL
    """
    # TODO use CONST mechanism
    try:
        # if TEST_DB_URL declared in env variable, use it!
        db_url = os.environ['TEST_DB_URL']
    except KeyError:
        db_url = get_functest_config('results.test_db_url')
    return db_url


def logger_test_results(project, case_name, status, details):
    pod_name = get_pod_name()
    scenario = get_scenario()
    version = get_version()
    build_tag = get_build_tag()

    logger.info(
        "\n"
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
        % {'p': project,
            'n': case_name,
            'db': get_db_url(),
            'pod': pod_name,
            'v': version,
            's': scenario,
            'c': status,
            'b': build_tag,
            'd': details})


@decorators.can_dump_request_to_file
def push_results_to_db(project, case_name,
                       start_date, stop_date, criteria, details):
    """
    POST results to the Result target DB
    """
    # Retrieve params from CI and conf
    url = get_db_url()

    try:
        installer = os.environ['INSTALLER_TYPE']
        scenario = os.environ['DEPLOY_SCENARIO']
        pod_name = os.environ['NODE_NAME']
        build_tag = os.environ['BUILD_TAG']
    except KeyError as e:
        logger.error("Please set env var: " + str(e))
        return False
    version = get_version()
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
            logger.error(error)
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
            resolver.nameservers = [ip.group(0)]
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


def execute_command_raise(cmd, info=False, error_msg="",
                          verbose=True, output_file=None):
    ret = execute_command(cmd, info, error_msg, verbose, output_file)
    if ret != 0:
        raise Exception(error_msg)


def execute_command(cmd, info=False, error_msg="",
                    verbose=True, output_file=None):
    if not error_msg:
        error_msg = ("The command '%s' failed." % cmd)
    msg_exec = ("Executing command: '%s'" % cmd)
    if verbose:
        if info:
            logger.info(msg_exec)
        else:
            logger.debug(msg_exec)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    if output_file:
        f = open(output_file, "w")
    for line in iter(p.stdout.readline, b''):
        if output_file:
            f.write(line)
        else:
            line = line.replace('\n', '')
            print line
            sys.stdout.flush()
    if output_file:
        f.close()
    p.stdout.close()
    returncode = p.wait()
    if returncode != 0:
        if verbose:
            logger.error(error_msg)

    return returncode


def get_dict_by_test(testname):
    with open(get_testcases_file_dir()) as f:
        testcases_yaml = yaml.safe_load(f)

    for dic_tier in testcases_yaml.get("tiers"):
        for dic_testcase in dic_tier['testcases']:
            if dic_testcase['name'] == testname:
                return dic_testcase

    logger.error('Project %s is not defined in testcases.yaml' % testname)
    return None


def get_criteria_by_test(testname):
    dict = get_dict_by_test(testname)
    if dict:
        return dict['criteria']
    return None


# ----------------------------------------------------------
#
#               YAML UTILS
#
# -----------------------------------------------------------
def get_parameter_from_yaml(parameter, file):
    """
    Returns the value of a given parameter in file.yaml
    parameter must be given in string format with dots
    Example: general.openstack.image_name
    """
    with open(file) as f:
        file_yaml = yaml.safe_load(f)
    f.close()
    value = file_yaml
    for element in parameter.split("."):
        value = value.get(element)
        if value is None:
            raise ValueError("The parameter %s is not defined in"
                             " %s" % (parameter, file))
    return value


def get_functest_config(parameter):
    yaml_ = os.environ["CONFIG_FUNCTEST_YAML"]
    return get_parameter_from_yaml(parameter, yaml_)


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


def get_testcases_file_dir():
    return get_functest_config('general.functest.testcases_yaml')


def get_functest_yaml():
    with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
        functest_yaml = yaml.safe_load(f)
    f.close()
    return functest_yaml


def print_separator():
    logger.info("==============================================")


def timethis(func):
    """Measure the time it takes for a function to complete"""
    @functools.wraps(func)
    def timed(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()
        elapsed = '{0}'.format(te - ts)
        logger.info('{f}(*{a}, **{kw}) took: {t} sec'.format(
            f=func.__name__, a=args, kw=kwargs, t=elapsed))
        return result, elapsed
    return timed
