#!/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Maintainer : jose.lausuch@ericsson.com
#
import argparse
import json
import logging
import os
import requests
import subprocess
import yaml

import keystoneclient.v2_0.client as ksclient
import glanceclient.client as glclient
import novaclient.client as nvclient
from neutronclient.v2_0 import client as ntclient

import functest_utils
import openstack_utils

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
args = parser.parse_args()

with open('/home/opnfv/functest/conf/config_functest.yaml') as f:
    functest_yaml = yaml.safe_load(f)

dirs = functest_yaml.get('general').get('directories')
FUNCTEST_REPO = dirs.get('dir_repo_functest')
PROMISE_REPO = dirs.get('dir_repo_promise')
TEST_DB = functest_yaml.get('results').get('test_db_url')

TENANT_NAME = functest_yaml.get('promise').get('general').get('tenant_name')
TENANT_DESCRIPTION = functest_yaml.get('promise').get(
    'general').get('tenant_description')
USER_NAME = functest_yaml.get('promise').get('general').get('user_name')
USER_PWD = functest_yaml.get('promise').get('general').get('user_pwd')
IMAGE_NAME = functest_yaml.get('promise').get('general').get('image_name')
FLAVOR_NAME = functest_yaml.get('promise').get('general').get('flavor_name')
FLAVOR_VCPUS = functest_yaml.get('promise').get('general').get('flavor_vcpus')
FLAVOR_RAM = functest_yaml.get('promise').get('general').get('flavor_ram')
FLAVOR_DISK = functest_yaml.get('promise').get('general').get('flavor_disk')


GLANCE_IMAGE_FILENAME = functest_yaml.get('general'). \
    get('openstack').get('image_file_name')
GLANCE_IMAGE_FORMAT = functest_yaml.get('general'). \
    get('openstack').get('image_disk_format')
GLANCE_IMAGE_PATH = functest_yaml.get('general'). \
    get('directories').get('dir_functest_data') + "/" + GLANCE_IMAGE_FILENAME

""" logging configuration """
logger = logging.getLogger('Promise')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()

if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s'
                              '- %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    ks_creds = openstack_utils.get_credentials("keystone")
    nv_creds = openstack_utils.get_credentials("nova")
    nt_creds = openstack_utils.get_credentials("neutron")

    keystone = ksclient.Client(**ks_creds)

    user_id = openstack_utils.get_user_id(keystone, ks_creds['username'])
    if user_id == '':
        logger.error("Error : Failed to get id of %s user" %
                     ks_creds['username'])
        exit(-1)

    logger.info("Creating tenant '%s'..." % TENANT_NAME)
    tenant_id = openstack_utils.create_tenant(
        keystone, TENANT_NAME, TENANT_DESCRIPTION)
    if tenant_id == '':
        logger.error("Error : Failed to create %s tenant" % TENANT_NAME)
        exit(-1)
    logger.debug("Tenant '%s' created successfully." % TENANT_NAME)

    roles_name = ["admin", "Admin"]
    role_id = ''
    for role_name in roles_name:
        if role_id == '':
            role_id = openstack_utils.get_role_id(keystone, role_name)

    if role_id == '':
        logger.error("Error : Failed to get id for %s role" % role_name)
        exit(-1)

    logger.info("Adding role '%s' to tenant '%s'..." % (role_id, TENANT_NAME))
    if not openstack_utils.add_role_user(keystone, user_id,
                                         role_id, tenant_id):
        logger.error("Error : Failed to add %s on tenant %s" %
                     (ks_creds['username'], TENANT_NAME))
        exit(-1)
    logger.debug("Role added successfully.")

    logger.info("Creating user '%s'..." % USER_NAME)
    user_id = openstack_utils.create_user(
        keystone, USER_NAME, USER_PWD, None, tenant_id)

    if user_id == '':
        logger.error("Error : Failed to create %s user" % USER_NAME)
        exit(-1)
    logger.debug("User '%s' created successfully." % USER_NAME)

    logger.info("Updating OpenStack credentials...")
    ks_creds.update({
        "username": TENANT_NAME,
        "password": TENANT_NAME,
        "tenant_name": TENANT_NAME,
    })

    nt_creds.update({
        "tenant_name": TENANT_NAME,
    })

    nv_creds.update({
        "project_id": TENANT_NAME,
    })

    glance_endpoint = keystone.\
        service_catalog.url_for(service_type='image',
                                endpoint_type='publicURL')
    glance = glclient.Client(1, glance_endpoint, token=keystone.auth_token)
    nova = nvclient.Client("2", **nv_creds)

    logger.info("Creating image '%s' from '%s'..." % (IMAGE_NAME,
                                                      GLANCE_IMAGE_PATH))
    image_id = openstack_utils.create_glance_image(glance,
                                                   IMAGE_NAME,
                                                   GLANCE_IMAGE_PATH)
    if not image_id:
        logger.error("Failed to create the Glance image...")
        exit(-1)
    logger.debug("Image '%s' with ID '%s' created successfully." % (IMAGE_NAME,
                                                                    image_id))
    flavor_id = openstack_utils.get_flavor_id(nova, FLAVOR_NAME)
    if flavor_id == '':
        logger.info("Creating flavor '%s'..." % FLAVOR_NAME)
        flavor_id = openstack_utils.create_flavor(nova,
                                                  FLAVOR_NAME,
                                                  FLAVOR_RAM,
                                                  FLAVOR_DISK,
                                                  FLAVOR_VCPUS)
        if not flavor_id:
            logger.error("Failed to create the Flavor...")
            exit(-1)
        logger.debug("Flavor '%s' with ID '%s' created successfully." %
                     (FLAVOR_NAME, flavor_id))
    else:
        logger.debug("Using existing flavor '%s' with ID '%s'..."
                     % (FLAVOR_NAME, flavor_id))

    neutron = ntclient.Client(**nt_creds)
    private_net = openstack_utils.get_private_net(neutron)
    if private_net is None:
        logger.error("There is no private network in the deployment."
                     "Aborting...")
        exit(-1)
    logger.debug("Using private network '%s' (%s)." % (private_net['name'],
                                                       private_net['id']))

    logger.info("Exporting environment variables...")
    os.environ["NODE_ENV"] = "functest"
    os.environ["OS_TENANT_NAME"] = TENANT_NAME
    os.environ["OS_USERNAME"] = USER_NAME
    os.environ["OS_PASSWORD"] = USER_PWD
    os.environ["OS_TEST_IMAGE"] = image_id
    os.environ["OS_TEST_FLAVOR"] = flavor_id
    os.environ["OS_TEST_NETWORK"] = private_net['id']

    os.chdir(PROMISE_REPO)
    results_file_name = 'promise-results.json'
    results_file = open(results_file_name, 'w+')
    cmd = 'npm run -s test -- --reporter json'

    logger.info("Running command: %s" % cmd)
    ret = subprocess.call(cmd, shell=True, stdout=results_file,
                          stderr=subprocess.STDOUT)
    results_file.close()

    if ret == 0:
        logger.info("The test succeeded.")
        # test_status = 'OK'
    else:
        logger.info("The command '%s' failed." % cmd)
        # test_status = "Failed"

    # Print output of file
    with open(results_file_name, 'r') as results_file:
        data = results_file.read()
        logger.debug("\n%s" % data)
        json_data = json.loads(data)

        suites = json_data["stats"]["suites"]
        tests = json_data["stats"]["tests"]
        passes = json_data["stats"]["passes"]
        pending = json_data["stats"]["pending"]
        failures = json_data["stats"]["failures"]
        start_time = json_data["stats"]["start"]
        end_time = json_data["stats"]["end"]
        duration = float(json_data["stats"]["duration"]) / float(1000)

    logger.info("\n"
                "****************************************\n"
                "          Promise test report\n\n"
                "****************************************\n"
                " Suites:  \t%s\n"
                " Tests:   \t%s\n"
                " Passes:  \t%s\n"
                " Pending: \t%s\n"
                " Failures:\t%s\n"
                " Start:   \t%s\n"
                " End:     \t%s\n"
                " Duration:\t%s\n"
                "****************************************\n\n"
                % (suites, tests, passes, pending, failures,
                   start_time, end_time, duration))

    if args.report:
        pod_name = functest_utils.get_pod_name(logger)
        installer = functest_utils.get_installer_type(logger)
        scenario = functest_utils.get_scenario(logger)
        version = functest_utils.get_version(logger)
        build_tag = functest_utils.get_build_tag(logger)
        # git_version = functest_utils.get_git_branch(PROMISE_REPO)
        url = TEST_DB + "/results"

        json_results = {"timestart": start_time, "duration": duration,
                        "tests": int(tests), "failures": int(failures)}
        logger.debug("Results json: " + str(json_results))

        # criteria for Promise in Release B was 100% of tests OK
        status = "failed"
        if int(tests) > 32 and int(failures) < 1:
            status = "passed"

        params = {"project_name": "promise", "case_name": "promise",
                  "pod_name": str(pod_name), 'installer': installer,
                  "version": version, "scenario": scenario,
                  "criteria": status, "build_tag": build_tag,
                  'details': json_results}
        headers = {'Content-Type': 'application/json'}

        logger.info("Pushing results to DB...")
        r = requests.post(url, data=json.dumps(params), headers=headers)
        logger.debug(r)


if __name__ == '__main__':
    main()
