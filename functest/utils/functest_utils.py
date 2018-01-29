#!/usr/bin/env python
#
# jose.lausuch@ericsson.com
# valentin.boucher@orange.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

from __future__ import print_function
import logging
import os
import re
import shutil
import subprocess
import sys

import pkg_resources
import dns.resolver
from six.moves import urllib
import yaml

from functest.utils import constants

LOGGER = logging.getLogger(__name__)


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

    with open(dest, 'wb') as lfile:
        shutil.copyfileobj(response, lfile)
    return True


# ----------------------------------------------------------
#
#               CI UTILS
#
# -----------------------------------------------------------
def get_resolvconf_ns():
    """
    Get nameservers from current resolv.conf
    """
    nameservers = []
    rconf = open("/etc/resolv.conf", "r")
    line = rconf.readline()
    resolver = dns.resolver.Resolver()
    while line:
        addr_ip = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
        if addr_ip:
            resolver.nameservers = [addr_ip.group(0)]
            try:
                result = resolver.query('opnfv.org')[0]
                if result != "":
                    nameservers.append(addr_ip.group())
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
            LOGGER.info(msg_exec)
        else:
            LOGGER.debug(msg_exec)
    popen = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if output_file:
        ofd = open(output_file, "w")
    for line in iter(popen.stdout.readline, b''):
        if output_file:
            ofd.write(line)
        else:
            line = line.replace('\n', '')
            print (line)
            sys.stdout.flush()
    if output_file:
        ofd.close()
    popen.stdout.close()
    returncode = popen.wait()
    if returncode != 0:
        if verbose:
            LOGGER.error(error_msg)

    return returncode


def get_dict_by_test(testname):
    # pylint: disable=bad-continuation
    with open(pkg_resources.resource_filename(
            'functest', 'ci/testcases.yaml')) as tyaml:
        testcases_yaml = yaml.safe_load(tyaml)

    for dic_tier in testcases_yaml.get("tiers"):
        for dic_testcase in dic_tier['testcases']:
            if dic_testcase['case_name'] == testname:
                return dic_testcase

    LOGGER.error('Project %s is not defined in testcases.yaml', testname)
    return None


def get_criteria_by_test(testname):
    tdict = get_dict_by_test(testname)
    if tdict:
        return tdict['criteria']
    return None


# ----------------------------------------------------------
#
#               YAML UTILS
#
# -----------------------------------------------------------
def get_parameter_from_yaml(parameter, yfile):
    """
    Returns the value of a given parameter in file.yaml
    parameter must be given in string format with dots
    Example: general.openstack.image_name
    """
    with open(yfile) as yfd:
        file_yaml = yaml.safe_load(yfd)
    value = file_yaml
    for element in parameter.split("."):
        value = value.get(element)
        if value is None:
            raise ValueError("The parameter %s is not defined in"
                             " %s" % (parameter, yfile))
    return value


def get_functest_config(parameter):
    yaml_ = constants.CONST.__getattribute__('CONFIG_FUNCTEST_YAML')
    return get_parameter_from_yaml(parameter, yaml_)


def get_functest_yaml():
    # pylint: disable=bad-continuation
    with open(constants.CONST.__getattribute__(
            'CONFIG_FUNCTEST_YAML')) as yaml_fd:
        functest_yaml = yaml.safe_load(yaml_fd)
    return functest_yaml


def print_separator():
    LOGGER.info("==============================================")
