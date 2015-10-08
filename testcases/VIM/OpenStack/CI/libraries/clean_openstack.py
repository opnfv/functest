#!/usr/bin/env python
#   
# Description:  
#   Cleans possible leftovers after running functest tests:
#       - Nova instances
#       - Neutron networks, subnets and ports
#       - Routers
#       - Cinder volumes
#       - Glance images
#
# Author:
#    jose.lausuch@ericsson.com
#


import re, json, os, urllib2, argparse, logging, shutil, yaml, subprocess, sys, getpass
import functest_utils
from git import Repo
from os import stat
from pwd import getpwuid
from neutronclient.v2_0 import client as neutronclient

parser = argparse.ArgumentParser()
parser.add_argument("repo_path", help="Path to the repository")
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
args = parser.parse_args()


""" logging configuration """
logger = logging.getLogger('clean_openstack')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

if not os.path.exists(args.repo_path):
    logger.error("Repo directory not found '%s'" % args.repo_path)
    exit(-1)

with open(args.repo_path+"testcases/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()






def main():

    if not functest_utils.check_credentials():
        logger.error("Please source the openrc credentials and run the script again.")
        exit(-1)

    # Remove instances
    

    exit(0)


if __name__ == '__main__':
    main()
