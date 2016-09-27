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
import json
import os
import subprocess
import time

import argparse
import keystoneclient.v2_0.client as ksclient
import novaclient.client as nvclient
from neutronclient.v2_0 import client as ntclient

import functest.utils.config_functest as config_functest
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as openstack_utils

CONF = config_functest.CONF

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
args = parser.parse_args()


TENANT_NAME = CONF.promise_tenant_name
USER_NAME = CONF.promise_username


GLANCE_IMAGE_PATH = CONF.functest_data_dir + "/" + CONF.os_image_file


""" logging configuration """
logger = ft_logger.Logger("promise").getLogger()


def main():
    exit_code = -1
    start_time = time.time()
    ks_creds = openstack_utils.get_credentials("keystone")
    nv_creds = openstack_utils.get_credentials("nova")
    nt_creds = openstack_utils.get_credentials("neutron")

    keystone = ksclient.Client(**ks_creds)

    user_id = openstack_utils.get_user_id(keystone, ks_creds['username'])
    if user_id == '':
        logger.error("Error : Failed to get id of %s user" %
                     ks_creds['username'])
        exit(-1)

    logger.info("Creating tenant '%s'..." % CONF.promise_tenant_name)
    tenant_id = openstack_utils.create_tenant(
        keystone, CONF.promise_tenant_name, CONF.promise_tenant_description)
    if not tenant_id:
        logger.error("Error : Failed to create %s tenant" %
                     CONF.promise_tenant_name)
        exit(-1)
    logger.debug("Tenant '%s' created successfully." %
                 CONF.promise_tenant_name)

    roles_name = ["admin", "Admin"]
    role_id = ''
    for role_name in roles_name:
        if role_id == '':
            role_id = openstack_utils.get_role_id(keystone, role_name)

    if role_id == '':
        logger.error("Error : Failed to get id for %s role" % role_name)
        exit(-1)

    logger.info("Adding role '%s' to tenant '%s'..." %
                (role_id, CONF.promise_tenant_name))
    if not openstack_utils.add_role_user(keystone, user_id,
                                         role_id, tenant_id):
        logger.error("Error : Failed to add %s on tenant %s" %
                     (ks_creds['username'], CONF.promise_tenant_name))
        exit(-1)
    logger.debug("Role added successfully.")

    logger.info("Creating user '%s'..." % USER_NAME)
    user_id = openstack_utils.create_user(
        keystone, USER_NAME, CONF.promise_password, None, tenant_id)

    if not user_id:
        logger.error("Error : Failed to create %s user" % USER_NAME)
        exit(-1)
    logger.debug("User '%s' created successfully." % USER_NAME)

    logger.info("Updating OpenStack credentials...")
    ks_creds.update({
        "username": CONF.promise_tenant_name,
        "password": CONF.promise_tenant_name,
        "tenant_name": CONF.promise_tenant_name,
    })

    nt_creds.update({
        "tenant_name": CONF.promise_tenant_name,
    })

    nv_creds.update({
        "project_id": CONF.promise_tenant_name,
    })

    glance = openstack_utils.get_glance_client()
    nova = nvclient.Client("2", **nv_creds)

    logger.info("Creating image '%s' from '%s'..." % (CONF.promise_image_name,
                                                      GLANCE_IMAGE_PATH))
    image_id = openstack_utils.create_glance_image(glance,
                                                   CONF.promise_image_name,
                                                   GLANCE_IMAGE_PATH)
    if not image_id:
        logger.error("Failed to create the Glance image...")
        exit(-1)
    logger.debug("Image '%s' with ID '%s' created successfully." %
                 (CONF.promise_image_name, image_id))
    flavor_id = openstack_utils.get_flavor_id(nova, CONF.promise_flavor_name)
    if flavor_id == '':
        logger.info("Creating flavor '%s'..." % CONF.promise_flavor_name)
        flavor_id = openstack_utils.create_flavor(nova,
                                                  CONF.promise_flavor_name,
                                                  CONF.promise_flavor_ram,
                                                  CONF.promise_flavor_disk,
                                                  CONF.promise_flavor_cpus)
        if not flavor_id:
            logger.error("Failed to create the Flavor...")
            exit(-1)
        logger.debug("Flavor '%s' with ID '%s' created successfully." %
                     (CONF.promise_flavor_name, flavor_id))
    else:
        logger.debug("Using existing flavor '%s' with ID '%s'..."
                     % (CONF.promise_flavor_name, flavor_id))

    neutron = ntclient.Client(**nt_creds)

    network_dic = \
        openstack_utils.create_network_full(neutron,
                                            CONF.promise_network_name,
                                            CONF.promise_subnet_name,
                                            CONF.promise_router_name,
                                            CONF.promise_subnet_name)
    if not network_dic:
        logger.error("Failed to create the private network...")
        exit(-1)

    logger.info("Exporting environment variables...")
    os.environ["NODE_ENV"] = "functest"
    os.environ["OS_TENANT_NAME"] = CONF.promise_tenant_name
    os.environ["OS_USERNAME"] = USER_NAME
    os.environ["OS_PASSWORD"] = CONF.promise_password
    os.environ["OS_TEST_IMAGE"] = image_id
    os.environ["OS_TEST_FLAVOR"] = flavor_id
    os.environ["OS_TEST_NETWORK"] = network_dic["net_id"]

    os.chdir(CONF.promise_repo)
    results_file_name = CONF.results_dir + '/' + 'promise-results.json'
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
        start_time_json = json_data["stats"]["start"]
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
                   start_time_json, end_time, duration))

    if args.report:
        stop_time = time.time()
        json_results = {"timestart": start_time, "duration": duration,
                        "tests": int(tests), "failures": int(failures)}
        logger.debug("Promise Results json: " + str(json_results))

        # criteria for Promise in Release B was 100% of tests OK
        status = "FAIL"
        if int(tests) > 32 and int(failures) < 1:
            status = "PASS"
            exit_code = 0

        ft_utils.push_results_to_db("promise",
                                    "promise",
                                    start_time,
                                    stop_time,
                                    status,
                                    json_results)

    exit(exit_code)


if __name__ == '__main__':
    main()
