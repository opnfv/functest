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
import re
import subprocess
import sys
from datetime import datetime as dt

import requests

from constants import CONST
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("functest_utils").getLogger()


def push_results_to_db(project, case_name,
                       start_date, stop_date, criteria, details):
    """
    POST results to the Result target DB
    """
    # Retrieve params from CI and conf
    url = CONST.results_test_db_url + "/results"

    try:
        installer = os.environ['INSTALLER_TYPE']
        scenario = os.environ['DEPLOY_SCENARIO']
        pod_name = os.environ['NODE_NAME']
        build_tag = os.environ['BUILD_TAG']
    except KeyError as e:
        logger.error("Please set env var: " + str(e))
        return False
    rule = "daily-(.+?)-[0-9]*"
    m = re.search(rule, build_tag)
    if m:
        version = m.group(1)
    else:
        logger.error("Please fix BUILD_TAG env var: " + build_tag)
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


def print_separator():
    logger.info("==============================================")
