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
import sys
import urllib2
import yaml
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
        print ("Error [push_results_to_db('%s', '%s', '%s', " +
               "'%s', '%s', '%s', '%s', '%s', '%s')]:" %
               (db_url, project, case_name, pod_name, version,
                scenario, criteria, build_tag, payload), e)
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
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while True:
        line = p.stdout.readline().replace('\n', '')
        if not line:
            break
        if logger:
            if info:
                logger.info(line)
            else:
                logger.debug(line)
        else:
            print line
    p.communicate()
    if p.returncode != 0:
        if verbose:
            if logger:
                logger.error(error_msg)
            else:
                print(error_msg)
        if exit_on_error:
            sys.exit(1)

    return p.returncode


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
