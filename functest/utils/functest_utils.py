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
import logging
import os
import pkg_resources
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime as dt

import dns.resolver
import requests
from six.moves import urllib
import yaml

from functest.utils import constants
from functest.utils import decorators
from functest.utils.constants import CONST

logger = logging.getLogger(__name__)


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
        urllib.request.urlopen(url, timeout=5)
        return True
    except urllib.error.URLError:
        return False


def download_url(url, dest_path):
    """
    Download a file to a destination path given a URL
    """
    name = url.rsplit('/')[-1]
    dest = dest_path + "/" + name
    try:
        response = urllib.request.urlopen(url)
    except (urllib.error.HTTPError, urllib.error.URLError):
        return False

    with open(dest, 'wb') as f:
        shutil.copyfileobj(response, f)
    return True


# ----------------------------------------------------------
#
#               CI UTILS
#
# -----------------------------------------------------------
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
    build_tag = CONST.__getattribute__('BUILD_TAG')
    if not build_tag:
        build_tag = 'none'
    m = re.search(rule, build_tag)
    if m:
        return m.group(2)
    else:
        return "unknown"


def logger_test_results(project, case_name, status, details):
    """
    Format test case results for the logger
    """
    pod_name = CONST.__getattribute__('NODE_NAME')
    scenario = CONST.__getattribute__('DEPLOY_SCENARIO')
    version = get_version()
    build_tag = CONST.__getattribute__('BUILD_TAG')
    db_url = CONST.__getattribute__("results_test_db_url")

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
            'db': db_url,
            'pod': pod_name,
            'v': version,
            's': scenario,
            'c': status,
            'b': build_tag,
            'd': details})


@decorators.can_dump_request_to_file
def push_results_to_db(project, case_name,
                       start_date, stop_date, result, details):
    """
    POST results to the Result target DB
    """
    # Retrieve params from CI and conf
    if (hasattr(CONST, 'TEST_DB_URL')):
        url = CONST.__getattribute__('TEST_DB_URL')
    else:
        url = CONST.__getattribute__("results_test_db_url")

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
              "version": version, "scenario": scenario, "criteria": result,
              "build_tag": build_tag, "start_date": test_start,
              "stop_date": test_stop, "details": details}

    error = None
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url, data=json.dumps(params, sort_keys=True),
                          headers=headers)
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
                     'c': result,
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
            print(line)
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
    with open(pkg_resources.resource_filename(
            'functest', 'ci/testcases.yaml')) as f:
        testcases_yaml = yaml.safe_load(f)

    for dic_tier in testcases_yaml.get("tiers"):
        for dic_testcase in dic_tier['testcases']:
            if dic_testcase['case_name'] == testname:
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
    yaml_ = constants.CONST.__getattribute__('CONFIG_FUNCTEST_YAML')
    return get_parameter_from_yaml(parameter, yaml_)


def get_functest_yaml():
    with open(constants.CONST.__getattribute__('CONFIG_FUNCTEST_YAML')) as f:
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
