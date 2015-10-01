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
# This script is used to build json files for the dashboard
# for the ODL test case
#
# v0.1: basic example
#
import logging
import argparse
import pprint
# import json
# import dashboard_utils
import os
import yaml

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


def format_tempest_for_dashboard(criteria):
    logger.debug("generate dashboard json files for ODL suite")
