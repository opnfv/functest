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

import os
import time
import sys
import yaml
import keystoneclient.v2_0.client as ksclient
import glanceclient.client as glclient
import novaclient.client as nvclient

with open('/home/opnfv/functest/conf/config_functest.yaml') as f:
    functest_yaml = yaml.safe_load(f)

dirs = functest_yaml.get('general').get('directories')
FUNCTEST_REPO = dirs.get('dir_repo_functest')
PROMISE_REPO = dirs.get('dir_repo_promise')
TEST_DB_URL = functest_yaml.get('results').get('test_db_url')

TENANT_NAME = functest_yaml.get("promise").get("general").get("tenant_name")
TENANT_DESCRIPTION = functest_yaml.get("promise").get(
    "general").get("tenant_description")
USER_NAME = functest_yaml.get("promise").get("general").get("user_name")
USER_PWD = functest_yaml.get("promise").get("general").get("user_pwd")

GLANCE_IMAGE_FILENAME = functest_yaml.get("general"). \
    get("openstack").get("image_file_name")
GLANCE_IMAGE_FORMAT = functest_yaml.get("general"). \
    get("openstack").get("image_disk_format")
GLANCE_IMAGE_PATH = functest_yaml.get("general"). \
    get("directories").get("dir_functest_data") + "/" + GLANCE_IMAGE_FILENAME

sys.path.append('%s/testcases' % FUNCTEST_REPO)
import functest_utils

""" logging configuration """
logger = logging.getLogger('vPing')
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



def create_image(glance_client, name):

    return image_id


def main():
    ks_creds = functest_utils.get_credentials("keystone")
    nv_creds = functest_utils.get_credentials("nova")
    nt_creds = functest_utils.get_credentials("neutron")

    logger.info("Prepare OpenStack plateform (create tenant and user)")
    keystone = ksclient.Client(**ks_creds)

    user_id = functest_utils.get_user_id(keystone, ks_creds['username'])
    if user_id == '':
        logger.error("Error : Failed to get id of %s user" %
                     ks_creds['username'])
        exit(-1)

    tenant_id = functest_utils.create_tenant(
        keystone, TENANT_NAME, TENANT_DESCRIPTION)
    if tenant_id == '':
        logger.error("Error : Failed to create %s tenant" % TENANT_NAME)
        exit(-1)

    roles_name = ["admin", "Admin"]
    role_id = ''
    for role_name in roles_name:
        if role_id == '':
            role_id = functest_utils.get_role_id(keystone, role_name)

    if role_id == '':
        logger.error("Error : Failed to get id for %s role" % role_name)

    if not functest_utils.add_role_user(keystone, user_id, role_id, tenant_id):
        logger.error("Error : Failed to add %s on tenant" %
                     ks_creds['username'])

    user_id = functest_utils.create_user(
        keystone, USER_NAME, USER_NAME, None, tenant_id)
    if user_id == '':
        logger.error("Error : Failed to create %s user" % USER_NAME)

    logger.info("Update OpenStack creds informations")
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

    logger.info("Upload some OS images if it doesn't exist")
    glance_endpoint = keystone.service_catalog.url_for(service_type='image',
                                                       endpoint_type='publicURL')
    glance = glclient.Client(1, glance_endpoint, token=keystone.auth_token)
    nova = nvclient.Client("2", **nv_creds)


    image_name = "functest-promise-img"
    logger.debug("Creating image '%s' from '%s'..." % (image_name,
                                                       GLANCE_IMAGE_PATH))
    image_id = functest_utils.create_glance_image(glance,
                                                  name,
                                                  GLANCE_IMAGE_PATH)
    if not image_id:
        logger.error("Failed to create a Glance image...")
        exit(-1)

    FLAVOR = "m1.small"
    try:
        flavor_id = nova.flavors.find(name=FLAVOR)
        logger.info("Flavor found '%s'" % FLAVOR)
    except:
        logger.error("Flavor '%s' not found." % FLAVOR)
        logger.info("Available flavors are: ")
        pMsg(nova_client.flavor.list())
        return(-1)

    os.environ["NODE_ENV"] = "functest"
    os.environ["OS_TENANT_NAME"] = TENANT_NAME
    os.environ["OS_USERNAME"] = USER_NAME
    os.environ["OS_PASWORD"] = USER_PWD
    os.environ["OS_TEST_IMAGE"] = image_id
    os.environ["OS_TEST_FLAVOR"] = flavor_id

    cmd = PROMISE_REPO + 'npm run -s -- --reporter json'
    start_time_ts = time.time()

    ret = functest_utils.execute_command(cmd, exit_on_error=False)

    end_time_ts = time.time()
    duration = round(end_time_ts - start_time_ts, 1)
    if ret:
        test_status = 'OK'
    else:
        test_status = 'NOK'

    details = {
        'timestart': start_time_ts,
        'duration': duration,
        'status': test_status,
    }
    pod_name = functest_utils.get_pod_name()
    git_version = functest_utils.get_git_branch(PROMISE_REPO)
    #functest_utils.push_results_to_db(TEST_DB_URL,
    #                                  'promise',
    #                                  None,
    #                                  pod_name,
    #                                  git_version,
    #                                  details)
    #

if __name__ == '__main__':
    main()
