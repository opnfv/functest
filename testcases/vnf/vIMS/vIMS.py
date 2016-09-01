#!/usr/bin/python
# coding: utf8
#######################################################################
#
#   Copyright (c) 2015 Orange
#   valentin.boucher@orange.com
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
########################################################################

import datetime
import json
import os
import pprint
import subprocess
import time

import argparse
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils
import functest.utils.openstack_utils as os_utils
import keystoneclient.v2_0.client as ksclient
import novaclient.client as nvclient
import requests
from functest.utils.functest_utils import FUNCTEST_REPO as REPO_PATH
from neutronclient.v2_0 import client as ntclient

from clearwater import clearwater
from orchestrator import orchestrator

pp = pprint.PrettyPrinter(indent=4)


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
parser.add_argument("-n", "--noclean",
                    help="Don't clean the created resources for this test.",
                    action="store_true")
args = parser.parse_args()

""" logging configuration """
logger = ft_logger.Logger("vIMS").getLogger()


functest_yaml = functest_utils.get_functest_yaml()

# Cloudify parameters
VIMS_DIR = (REPO_PATH + '/' +
            functest_yaml.get("general").get("directories").get("dir_vIMS"))
VIMS_DATA_DIR = functest_yaml.get("general").get(
    "directories").get("dir_vIMS_data") + "/"
VIMS_TEST_DIR = functest_yaml.get("general").get(
    "directories").get("dir_repo_vims_test") + "/"
DB_URL = functest_yaml.get("results").get("test_db_url")

TENANT_NAME = functest_yaml.get("vIMS").get("general").get("tenant_name")
TENANT_DESCRIPTION = functest_yaml.get("vIMS").get(
    "general").get("tenant_description")
IMAGES = functest_yaml.get("vIMS").get("general").get("images")

CFY_MANAGER_BLUEPRINT = functest_yaml.get(
    "vIMS").get("cloudify").get("blueprint")
CFY_MANAGER_REQUIERMENTS = functest_yaml.get(
    "vIMS").get("cloudify").get("requierments")
CFY_INPUTS = functest_yaml.get("vIMS").get("cloudify").get("inputs")

CW_BLUEPRINT = functest_yaml.get("vIMS").get("clearwater").get("blueprint")
CW_DEPLOYMENT_NAME = functest_yaml.get("vIMS").get(
    "clearwater").get("deployment-name")
CW_INPUTS = functest_yaml.get("vIMS").get("clearwater").get("inputs")
CW_REQUIERMENTS = functest_yaml.get("vIMS").get(
    "clearwater").get("requierments")

CFY_DEPLOYMENT_DURATION = 0
CW_DEPLOYMENT_DURATION = 0

TESTCASE_START_TIME = time.time()
RESULTS = {'orchestrator': {'duration': 0, 'result': ''},
           'vIMS': {'duration': 0, 'result': ''},
           'sig_test': {'duration': 0, 'result': ''}}


def download_and_add_image_on_glance(glance, image_name, image_url):
    dest_path = VIMS_DATA_DIR + "tmp/"
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    file_name = image_url.rsplit('/')[-1]
    if not functest_utils.download_url(image_url, dest_path):
        logger.error("Failed to download image %s" % file_name)
        return False

    image = os_utils.create_glance_image(
        glance, image_name, dest_path + file_name)
    if not image:
        logger.error("Failed to upload image on glance")
        return False

    return image


def step_failure(step_name, error_msg):
    logger.error(error_msg)
    set_result(step_name, 0, error_msg)
    status = "FAIL"
    # in case of failure starting and stoping time are not correct
    stop_time = time.time()
    if step_name == "sig_test":
        status = "PASS"
    functest_utils.push_results_to_db("functest",
                                      "vims",
                                      TESTCASE_START_TIME,
                                      stop_time,
                                      status,
                                      RESULTS)
    exit(-1)


def set_result(step_name, duration=0, result=""):
    RESULTS[step_name] = {'duration': duration, 'result': result}


def test_clearwater():
    script = "source " + VIMS_DATA_DIR + "venv_cloudify/bin/activate; "
    script += "cd " + VIMS_DATA_DIR + "; "
    script += "cfy status | grep -Eo \"([0-9]{1,3}\.){3}[0-9]{1,3}\""
    cmd = "/bin/bash -c '" + script + "'"

    try:
        logger.debug("Trying to get clearwater manager IP ... ")
        mgr_ip = os.popen(cmd).read()
        mgr_ip = mgr_ip.splitlines()[0]
    except:
        step_failure("sig_test", "Unable to retrieve the IP of the "
                     "cloudify manager server !")

    api_url = "http://" + mgr_ip + "/api/v2"
    dep_outputs = requests.get(api_url + "/deployments/" +
                               CW_DEPLOYMENT_NAME + "/outputs")
    dns_ip = dep_outputs.json()['outputs']['dns_ip']
    ellis_ip = dep_outputs.json()['outputs']['ellis_ip']

    ellis_url = "http://" + ellis_ip + "/"
    url = ellis_url + "accounts"

    params = {"password": "functest",
              "full_name": "opnfv functest user",
              "email": "functest@opnfv.fr",
              "signup_code": "secret"}

    rq = requests.post(url, data=params)
    i = 20
    while rq.status_code != 201 and i > 0:
        rq = requests.post(url, data=params)
        i = i - 1
        time.sleep(10)

    if rq.status_code == 201:
        url = ellis_url + "session"
        rq = requests.post(url, data=params)
        cookies = rq.cookies

    url = ellis_url + "accounts/" + params['email'] + "/numbers"
    if cookies != "":
        rq = requests.post(url, cookies=cookies)
        i = 24
        while rq.status_code != 200 and i > 0:
            rq = requests.post(url, cookies=cookies)
            i = i - 1
            time.sleep(25)

    if rq.status_code != 200:
        step_failure("sig_test", "Unable to create a number: %s"
                     % rq.json()['reason'])

    start_time_ts = time.time()
    end_time_ts = start_time_ts
    logger.info("vIMS functional test Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time_ts).strftime(
            '%Y-%m-%d %H:%M:%S')))
    nameservers = functest_utils.get_resolvconf_ns()
    resolvconf = ""
    for ns in nameservers:
        resolvconf += "\nnameserver " + ns

    if dns_ip != "":
        script = ('echo -e "nameserver ' + dns_ip + resolvconf +
                  '" > /etc/resolv.conf; ')
        script += 'source /etc/profile.d/rvm.sh; '
        script += 'cd ' + VIMS_TEST_DIR + '; '
        script += ('rake test[' + CW_INPUTS["public_domain"] +
                   '] SIGNUP_CODE="secret"')

        cmd = "/bin/bash -c '" + script + "'"
        output_file = "output.txt"
        f = open(output_file, 'w+')
        subprocess.call(cmd, shell=True, stdout=f,
                        stderr=subprocess.STDOUT)
        f.close()
        end_time_ts = time.time()
        duration = round(end_time_ts - start_time_ts, 1)
        logger.info("vIMS functional test duration:'%s'" % duration)
        f = open(output_file, 'r')
        result = f.read()
        if result != "" and logger:
            logger.debug(result)

        vims_test_result = ""
        try:
            logger.debug("Trying to load test results")
            with open(VIMS_TEST_DIR + "temp.json") as f:
                vims_test_result = json.load(f)
            f.close()
        except:
            logger.error("Unable to retrieve test results")

        set_result("sig_test", duration, vims_test_result)

        # success criteria for vIMS (for Brahmaputra)
        # - orchestrator deployed
        # - VNF deployed
        # TODO use test criteria defined in config file
        status = "FAIL"
        try:
            if (RESULTS['orchestrator']['duration'] > 0 and
                    RESULTS['vIMS']['duration'] > 0):
                status = "PASS"
        except:
            logger.error("Unable to set test status")

        functest_utils.push_results_to_db("functest",
                                          "vims",
                                          TESTCASE_START_TIME,
                                          end_time_ts,
                                          status,
                                          RESULTS)

        try:
            os.remove(VIMS_TEST_DIR + "temp.json")
        except:
            logger.error("Deleting file failed")


def main():

    # ############### GENERAL INITIALISATION ################

    if not os.path.exists(VIMS_DATA_DIR):
        os.makedirs(VIMS_DATA_DIR)

    ks_creds = os_utils.get_credentials("keystone")
    nv_creds = os_utils.get_credentials("nova")
    nt_creds = os_utils.get_credentials("neutron")

    logger.info("Prepare OpenStack plateform (create tenant and user)")
    keystone = ksclient.Client(**ks_creds)

    user_id = os_utils.get_user_id(keystone, ks_creds['username'])
    if user_id == '':
        step_failure("init", "Error : Failed to get id of " +
                     ks_creds['username'])

    tenant_id = os_utils.create_tenant(
        keystone, TENANT_NAME, TENANT_DESCRIPTION)
    if not tenant_id:
        step_failure("init", "Error : Failed to create " +
                     TENANT_NAME + " tenant")

    roles_name = ["admin", "Admin"]
    role_id = ''
    for role_name in roles_name:
        if role_id == '':
            role_id = os_utils.get_role_id(keystone, role_name)

    if role_id == '':
        logger.error("Error : Failed to get id for %s role" % role_name)

    if not os_utils.add_role_user(keystone, user_id, role_id, tenant_id):
        logger.error("Error : Failed to add %s on tenant" %
                     ks_creds['username'])

    user_id = os_utils.create_user(
        keystone, TENANT_NAME, TENANT_NAME, None, tenant_id)
    if not user_id:
        logger.error("Error : Failed to create %s user" % TENANT_NAME)

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
    glance = os_utils.get_glance_client()

    for img in IMAGES.keys():
        image_name = IMAGES[img]['image_name']
        image_url = IMAGES[img]['image_url']

        image_id = os_utils.get_image_id(glance, image_name)

        if image_id == '':
            logger.info("""%s image doesn't exist on glance repository. Try
            downloading this image and upload on glance !""" % image_name)
            image_id = download_and_add_image_on_glance(
                glance, image_name, image_url)

        if image_id == '':
            step_failure(
                "init",
                "Error : Failed to find or upload required OS "
                "image for this deployment")

    nova = nvclient.Client("2", **nv_creds)

    logger.info("Update security group quota for this tenant")
    neutron = ntclient.Client(**nt_creds)
    if not os_utils.update_sg_quota(neutron, tenant_id, 50, 100):
        step_failure(
            "init",
            "Failed to update security group quota for tenant " + TENANT_NAME)

    # ############### CLOUDIFY INITIALISATION ################
    public_auth_url = keystone.service_catalog.url_for(
        service_type='identity', endpoint_type='publicURL')

    cfy = orchestrator(VIMS_DATA_DIR, CFY_INPUTS)

    cfy.set_credentials(username=ks_creds['username'], password=ks_creds[
                        'password'], tenant_name=ks_creds['tenant_name'],
                        auth_url=public_auth_url)

    logger.info("Collect flavor id for cloudify manager server")
    nova = nvclient.Client("2", **nv_creds)

    flavor_name = "m1.large"
    flavor_id = os_utils.get_flavor_id(nova, flavor_name)
    for requirement in CFY_MANAGER_REQUIERMENTS:
        if requirement == 'ram_min':
            flavor_id = os_utils.get_flavor_id_by_ram_range(
                nova, CFY_MANAGER_REQUIERMENTS['ram_min'], 10000)

    if flavor_id == '':
        logger.error(
            "Failed to find %s flavor. "
            "Try with ram range default requirement !" % flavor_name)
        flavor_id = os_utils.get_flavor_id_by_ram_range(nova, 4000, 8196)

    if flavor_id == '':
        step_failure("orchestrator",
                     "Failed to find required flavor for this deployment")

    cfy.set_flavor_id(flavor_id)

    image_name = "centos_7"
    image_id = os_utils.get_image_id(glance, image_name)
    for requirement in CFY_MANAGER_REQUIERMENTS:
        if requirement == 'os_image':
            image_id = os_utils.get_image_id(
                glance, CFY_MANAGER_REQUIERMENTS['os_image'])

    if image_id == '':
        step_failure(
            "orchestrator",
            "Error : Failed to find required OS image for cloudify manager")

    cfy.set_image_id(image_id)

    ext_net = os_utils.get_external_net(neutron)
    if not ext_net:
        step_failure("orchestrator", "Failed to get external network")

    cfy.set_external_network_name(ext_net)

    ns = functest_utils.get_resolvconf_ns()
    if ns:
        cfy.set_nameservers(ns)

    if 'compute' in nova.client.services_url:
        cfy.set_nova_url(nova.client.services_url['compute'])
    if neutron.httpclient.endpoint_url is not None:
        cfy.set_neutron_url(neutron.httpclient.endpoint_url)

    logger.info("Prepare virtualenv for cloudify-cli")
    cmd = "chmod +x " + VIMS_DIR + "create_venv.sh"
    functest_utils.execute_command(cmd)
    time.sleep(3)
    cmd = VIMS_DIR + "create_venv.sh " + VIMS_DATA_DIR
    functest_utils.execute_command(cmd)

    cfy.download_manager_blueprint(
        CFY_MANAGER_BLUEPRINT['url'], CFY_MANAGER_BLUEPRINT['branch'])

    # ############### CLOUDIFY DEPLOYMENT ################
    start_time_ts = time.time()
    end_time_ts = start_time_ts
    logger.info("Cloudify deployment Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time_ts).strftime(
            '%Y-%m-%d %H:%M:%S')))

    error = cfy.deploy_manager()
    if error:
        step_failure("orchestrator", error)

    end_time_ts = time.time()
    duration = round(end_time_ts - start_time_ts, 1)
    logger.info("Cloudify deployment duration:'%s'" % duration)
    set_result("orchestrator", duration, "")

    # ############### CLEARWATER INITIALISATION ################

    cw = clearwater(CW_INPUTS, cfy, logger)

    logger.info("Collect flavor id for all clearwater vm")
    nova = nvclient.Client("2", **nv_creds)

    flavor_name = "m1.small"
    flavor_id = os_utils.get_flavor_id(nova, flavor_name)
    for requirement in CW_REQUIERMENTS:
        if requirement == 'ram_min' and flavor_id == '':
            flavor_id = os_utils.get_flavor_id_by_ram_range(
                nova, CW_REQUIERMENTS['ram_min'], 4500)

    if flavor_id == '':
        logger.error(
            "Failed to find %s flavor. Try with ram range "
            "default requirement !" % flavor_name)
        flavor_id = os_utils.get_flavor_id_by_ram_range(nova, 4000, 8196)

    if flavor_id == '':
        step_failure(
            "vIMS", "Failed to find required flavor for this deployment")

    cw.set_flavor_id(flavor_id)

    image_name = "ubuntu_14.04"
    image_id = os_utils.get_image_id(glance, image_name)
    for requirement in CW_REQUIERMENTS:
        if requirement == 'os_image':
            image_id = os_utils.get_image_id(
                glance, CW_REQUIERMENTS['os_image'])

    if image_id == '':
        step_failure(
            "vIMS",
            "Error : Failed to find required OS image for cloudify manager")

    cw.set_image_id(image_id)

    ext_net = os_utils.get_external_net(neutron)
    if not ext_net:
        step_failure("vIMS", "Failed to get external network")

    cw.set_external_network_name(ext_net)

    # ############### CLEARWATER DEPLOYMENT ################

    start_time_ts = time.time()
    end_time_ts = start_time_ts
    logger.info("vIMS VNF deployment Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time_ts).strftime(
            '%Y-%m-%d %H:%M:%S')))

    error = cw.deploy_vnf(CW_BLUEPRINT)
    if error:
        step_failure("vIMS", error)

    end_time_ts = time.time()
    duration = round(end_time_ts - start_time_ts, 1)
    logger.info("vIMS VNF deployment duration:'%s'" % duration)
    set_result("vIMS", duration, "")

    # ############### CLEARWATER TEST ################

    test_clearwater()

    # ########## CLEARWATER UNDEPLOYMENT ############

    cw.undeploy_vnf()

    # ########### CLOUDIFY UNDEPLOYMENT #############

    cfy.undeploy_manager()

    # ############## GENERAL CLEANUP ################
    if args.noclean:
        exit(0)

    ks_creds = os_utils.get_credentials("keystone")

    keystone = ksclient.Client(**ks_creds)

    logger.info("Removing %s tenant .." % CFY_INPUTS['keystone_tenant_name'])
    tenant_id = os_utils.get_tenant_id(
        keystone, CFY_INPUTS['keystone_tenant_name'])
    if tenant_id == '':
        logger.error("Error : Failed to get id of %s tenant" %
                     CFY_INPUTS['keystone_tenant_name'])
    else:
        if not os_utils.delete_tenant(keystone, tenant_id):
            logger.error("Error : Failed to remove %s tenant" %
                         CFY_INPUTS['keystone_tenant_name'])

    logger.info("Removing %s user .." % CFY_INPUTS['keystone_username'])
    user_id = os_utils.get_user_id(
        keystone, CFY_INPUTS['keystone_username'])
    if user_id == '':
        logger.error("Error : Failed to get id of %s user" %
                     CFY_INPUTS['keystone_username'])
    else:
        if not os_utils.delete_user(keystone, user_id):
            logger.error("Error : Failed to remove %s user" %
                         CFY_INPUTS['keystone_username'])


if __name__ == '__main__':
    main()
