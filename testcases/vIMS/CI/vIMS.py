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

import os, time, subprocess, logging, argparse, yaml, pprint, sys, shutil, json, datetime
from git import Repo
import keystoneclient.v2_0.client as ksclient
import glanceclient.client as glclient
import novaclient.client as nvclient
from neutronclient.v2_0 import client as ntclient

from orchestrator import *
from clearwater import *

import urllib
pp = pprint.PrettyPrinter(indent=4)


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Debug mode",  action="store_true")
parser.add_argument("-r", "--report",
                    help="Create json result file",
                    action="store_true")
args = parser.parse_args()

""" logging configuration """
logger = logging.getLogger('vIMS')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
if args.debug:
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

REPO_PATH=os.environ['repos_dir']+'/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)
sys.path.append(REPO_PATH + "testcases/")
import functest_utils

with open( REPO_PATH + "testcases/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

# Cloudify parameters
VIMS_DIR = REPO_PATH + functest_yaml.get("general").get("directories").get("dir_vIMS")
VIMS_DATA_DIR = functest_yaml.get("general").get("directories").get("dir_vIMS_data")+"/"
VIMS_TEST_DIR = functest_yaml.get("general").get("directories").get("dir_repo_vims_test")+"/"
TEST_DB = functest_yaml.get("results").get("test_db_url")

TENANT_NAME = functest_yaml.get("vIMS").get("general").get("tenant_name")
TENANT_DESCRIPTION = functest_yaml.get("vIMS").get("general").get("tenant_description")
IMAGES = functest_yaml.get("vIMS").get("general").get("images")

CFY_MANAGER_BLUEPRINT = functest_yaml.get("vIMS").get("cloudify").get("blueprint")
CFY_MANAGER_REQUIERMENTS = functest_yaml.get("vIMS").get("cloudify").get("requierments")
CFY_INPUTS =  functest_yaml.get("vIMS").get("cloudify").get("inputs")

CW_BLUEPRINT = functest_yaml.get("vIMS").get("clearwater").get("blueprint")
CW_DEPLOYMENT_NAME = functest_yaml.get("vIMS").get("clearwater").get("deployment-name")
CW_INPUTS =  functest_yaml.get("vIMS").get("clearwater").get("inputs")
CW_REQUIERMENTS = functest_yaml.get("vIMS").get("clearwater").get("requierments")

CFY_DEPLOYMENT_DURATION = 0
CW_DEPLOYMENT_DURATION = 0


def download_and_add_image_on_glance(glance, image_name, image_url):
    dest_path = VIMS_DATA_DIR + "tmp/"
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    file_name = image_url.rsplit('/')[-1]
    if not functest_utils.download_url(image_url, dest_path):
        logger.error("Failed to download image %s" %file_name)
        return False

    image = functest_utils.create_glance_image(glance, image_name, dest_path + file_name)
    if not image:
        logger.error("Failed to upload image on glance")
        return False

    return image

def test_clearwater():

    time.sleep(180)

    script = "source " + VIMS_DATA_DIR + "venv_cloudify/bin/activate; "
    script += "cd " + VIMS_DATA_DIR + "; "
    script += "cfy deployments outputs -d " + CW_DEPLOYMENT_NAME + " | grep Value: | sed \"s/ *Value: //g\";"
    cmd = "/bin/bash -c '" + script + "'"

    try:
        logger.debug("Trying to get clearwater nameserver IP ... ")
        dns_ip = os.popen(cmd).read()
        dns_ip = dns_ip.splitlines()[0]
    except:
        logger.error("Unable to retrieve the IP of the DNS server !")

    start_time_ts = time.time()
    end_time_ts = start_time_ts
    logger.info("vIMS functional test Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time_ts).strftime(
            '%Y-%m-%d %H:%M:%S')))

    if dns_ip != "":
        script = 'echo -e "nameserver ' + dns_ip + '\nnameserver 8.8.8.8\nnameserver 8.8.4.4" > /etc/resolv.conf; '
        script += 'source /etc/profile.d/rvm.sh; '
        script += 'cd ' + VIMS_TEST_DIR + '; '
        script += 'rake test[' + CW_INPUTS["public_domain"] + '] SIGNUP_CODE="secret"'

        cmd = "/bin/bash -c '" + script + "'"
        output_file = "output.txt"
        f = open(output_file, 'w+')
        p = subprocess.call(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT)
        f.close()
        end_time_ts = time.time()
        duration = round(end_time_ts - start_time_ts, 1)
        logger.info("vIMS functional test duration:'%s'" %duration)
        f = open(output_file, 'r')
        result = f.read()
        if result != "" and logger:
            logger.debug(result)

        vims_test_result=""
        try:
            logger.debug("Trying to load test results")
            with open(VIMS_TEST_DIR + "temp.json") as f:
                vims_test_result = json.load(f)
            f.close()
        except:
            logger.error("Unable to retrieve test results")

        if vims_test_result != "":
            if args.report:
                logger.debug("Push result into DB")
                logger.debug("Pushing results to DB....")
                git_version = functest_utils.get_git_branch(args.repo_path)
                functest_utils.push_results_to_db(db_url=TEST_DB, case_name="vIMS",
                            logger=logger, pod_name="opnfv-jump-2", git_version=git_version,
                            payload={'orchestrator':{'duration': CFY_DEPLOYMENT_DURATION,
                            'result': ""},
                            'vIMS': {'duration': CW_DEPLOYMENT_DURATION,
                            'result': ""},
                            'sig_test': {'duration': duration,
                            'result': vims_test_result}})
        try:
            os.remove(VIMS_TEST_DIR + "temp.json")
        except:
            logger.error("Deleting file failed")

def main():

    ################ GENERAL INITIALISATION ################

    if not os.path.exists(VIMS_DATA_DIR):
        os.makedirs(VIMS_DATA_DIR)

    ks_creds = functest_utils.get_credentials("keystone")
    nv_creds = functest_utils.get_credentials("nova")
    nt_creds = functest_utils.get_credentials("neutron")

    logger.info("Prepare OpenStack plateform (create tenant and user)")
    keystone = ksclient.Client(**ks_creds)

    user_id = functest_utils.get_user_id(keystone, ks_creds['username'])
    if user_id == '':
        logger.error("Error : Failed to get id of %s user" %ks_creds['username'])
        exit(-1)

    tenant_id = functest_utils.create_tenant(keystone, TENANT_NAME, TENANT_DESCRIPTION)
    if tenant_id == '':
        logger.error("Error : Failed to create %s tenant" %TENANT_NAME)
        exit(-1)

    role_name = "admin"
    role_id = functest_utils.get_role_id(keystone, role_name)
    if role_id == '':
        logger.error("Error : Failed to get id for %s role" %role_name)

    if not functest_utils.add_role_user(keystone, user_id, role_id, tenant_id):
        logger.error("Error : Failed to add %s on tenant" %ks_creds['username'])

    user_id = functest_utils.create_user(keystone, TENANT_NAME, TENANT_NAME, None, tenant_id)
    if user_id == '':
        logger.error("Error : Failed to create %s user" %TENANT_NAME)

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

    for img in IMAGES.keys():
        image_name = IMAGES[img]['image_name']
        image_url = IMAGES[img]['image_url']

        image_id = functest_utils.get_image_id(glance, image_name)

        if image_id == '':
            logger.info("""%s image doesn't exist on glance repository.
                            Try downloading this image and upload on glance !""" %image_name)
            image_id = download_and_add_image_on_glance(glance, image_name, image_url)

        if image_id == '':
            logger.error("Error : Failed to find or upload required OS image for this deployment")
            exit(-1)

    nova = nvclient.Client("2", **nv_creds)

    logger.info("Update security group quota for this tenant")
    neutron = ntclient.Client(**nt_creds)
    if not functest_utils.update_sg_quota(neutron, tenant_id, 50, 100):
        logger.error("Failed to update security group quota for tenant %s" %TENANT_NAME)
        exit(-1)

    logger.info("Update cinder quota for this tenant")
    from cinderclient import client as cinderclient

    creds_cinder = functest_utils.get_credentials("cinder")
    cinder_client = cinderclient.Client('1',creds_cinder['username'],
                                        creds_cinder['api_key'],
                                        creds_cinder['project_id'],
                                        creds_cinder['auth_url'],
                                        service_type="volume")
    if not functest_utils.update_cinder_quota(cinder_client,tenant_id,20,50,1500):
        logger.error("Failed to update cinder quota for tenant %s" % TENANT_NAME)
        exit(-1)

    ################ CLOUDIFY INITIALISATION ################

    cfy = orchestrator(VIMS_DATA_DIR, CFY_INPUTS, logger)

    cfy.set_credentials(username=ks_creds['username'], password=ks_creds['password'], tenant_name=ks_creds['tenant_name'], auth_url=ks_creds['auth_url'])

    logger.info("Collect flavor id for cloudify manager server")
    nova = nvclient.Client("2", **nv_creds)

    flavor_name = "m1.medium"
    flavor_id = functest_utils.get_flavor_id(nova, flavor_name)
    for requirement in CFY_MANAGER_REQUIERMENTS:
        if requirement == 'ram_min':
            flavor_id = functest_utils.get_flavor_id_by_ram_range(nova, CFY_MANAGER_REQUIERMENTS['ram_min'], 8196)

    if flavor_id == '':
        logger.error("Failed to find %s flavor. Try with ram range default requirement !" %flavor_name)
        flavor_id = functest_utils.get_flavor_id_by_ram_range(nova, 4000, 8196)

    if flavor_id == '':
        logger.error("Failed to find required flavor for this deployment" %flavor_name)
        exit(-1)

    cfy.set_flavor_id(flavor_id)

    image_name = "centos_7"
    image_id = functest_utils.get_image_id(glance, image_name)
    for requirement in CFY_MANAGER_REQUIERMENTS:
        if requirement == 'os_image':
            image_id = functest_utils.get_image_id(glance, CFY_MANAGER_REQUIERMENTS['os_image'])

    if image_id == '':
        logger.error("Error : Failed to find required OS image for cloudify manager")
        exit(-1)

    cfy.set_image_id(image_id)

    ext_net = functest_utils.get_external_net(neutron)
    if not ext_net:
        logger.error("Failed to get external network")
        exit(-1)

    cfy.set_external_network_name(ext_net)

    logger.info("Prepare virtualenv for cloudify-cli")
    cmd = "chmod +x " + VIMS_DIR + "create_venv.sh"
    functest_utils.execute_command(cmd,logger)
    cmd = VIMS_DIR + "create_venv.sh " + VIMS_DATA_DIR
    functest_utils.execute_command(cmd,logger)

    cfy.download_manager_blueprint(CFY_MANAGER_BLUEPRINT['url'], CFY_MANAGER_BLUEPRINT['branch'])

     ################ CLOUDIFY DEPLOYMENT ################
    start_time_ts = time.time()
    end_time_ts = start_time_ts
    logger.info("Cloudify deployment Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time_ts).strftime(
            '%Y-%m-%d %H:%M:%S')))

    cfy.deploy_manager()

    global CFY_DEPLOYMENT_DURATION
    end_time_ts = time.time()
    CFY_DEPLOYMENT_DURATION = round(end_time_ts - start_time_ts, 1)
    logger.info("Cloudify deployment duration:'%s'" %CFY_DEPLOYMENT_DURATION)

     ################ CLEARWATER INITIALISATION ################

    cw = clearwater(CW_INPUTS, cfy, logger)

    logger.info("Collect flavor id for all clearwater vm")
    nova = nvclient.Client("2", **nv_creds)

    flavor_name = "m1.small"
    flavor_id = functest_utils.get_flavor_id(nova, flavor_name)
    for requirement in CW_REQUIERMENTS:
        if requirement == 'ram_min':
            flavor_id = functest_utils.get_flavor_id_by_ram_range(nova, CW_REQUIERMENTS['ram_min'], 8196)

    if flavor_id == '':
        logger.error("Failed to find %s flavor. Try with ram range default requirement !" %flavor_name)
        flavor_id = functest_utils.get_flavor_id_by_ram_range(nova, 4000, 8196)

    if flavor_id == '':
        logger.error("Failed to find required flavor for this deployment" %flavor_name)
        exit(-1)

    cw.set_flavor_id(flavor_id)

    image_name = "ubuntu_14.04"
    image_id = functest_utils.get_image_id(glance, image_name)
    for requirement in CW_REQUIERMENTS:
        if requirement == 'os_image':
            image_id = functest_utils.get_image_id(glance, CW_REQUIERMENTS['os_image'])

    if image_id == '':
        logger.error("Error : Failed to find required OS image for cloudify manager")
        exit(-1)

    cw.set_image_id(image_id)

    ext_net = functest_utils.get_external_net(neutron)
    if not ext_net:
        logger.error("Failed to get external network")
        exit(-1)

    cw.set_external_network_name(ext_net)

     ################ CLEARWATER DEPLOYMENT ################

    start_time_ts = time.time()
    end_time_ts = start_time_ts
    logger.info("vIMS VNF deployment Start Time:'%s'" % (
        datetime.datetime.fromtimestamp(start_time_ts).strftime(
            '%Y-%m-%d %H:%M:%S')))

    cw.deploy_vnf(CW_BLUEPRINT)

    global CW_DEPLOYMENT_DURATION
    end_time_ts = time.time()
    CW_DEPLOYMENT_DURATION = round(end_time_ts - start_time_ts, 1)
    logger.info("vIMS VNF deployment duration:'%s'" %CW_DEPLOYMENT_DURATION)

     ################ CLEARWATER TEST ################

    test_clearwater()

     ########### CLEARWATER UNDEPLOYMENT ############

    cw.undeploy_vnf()

     ############ CLOUDIFY UNDEPLOYMENT #############

    cfy.undeploy_manager()

     ############### GENERAL CLEANUP ################

    ks_creds = functest_utils.get_credentials("keystone")

    keystone = ksclient.Client(**ks_creds)

    logger.info("Removing %s tenant .." %CFY_INPUTS['keystone_tenant_name'])
    tenant_id = functest_utils.get_tenant_id(keystone, CFY_INPUTS['keystone_tenant_name'])
    if tenant_id == '':
        logger.error("Error : Failed to get id of %s tenant" %CFY_INPUTS['keystone_tenant_name'])
    else:
        if not functest_utils.delete_tenant(keystone, tenant_id):
            logger.error("Error : Failed to remove %s tenant" %CFY_INPUTS['keystone_tenant_name'])

    logger.info("Removing %s user .." %CFY_INPUTS['keystone_username'])
    user_id = functest_utils.get_user_id(keystone, CFY_INPUTS['keystone_username'])
    if user_id == '':
        logger.error("Error : Failed to get id of %s user" %CFY_INPUTS['keystone_username'])
    else:
        if not functest_utils.delete_user(keystone, user_id):
            logger.error("Error : Failed to remove %s user" %CFY_INPUTS['keystone_username'])


if __name__ == '__main__':
    main()
