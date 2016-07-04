"""
Description: This test is to run onos Teston VTN scripts

List of test cases:
CASE1 - Northbound NBI test network/subnet/ports
CASE2 - Ovsdb test&Default configuration&Vm go online

lanqinglong@huawei.com
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
"""

# import argparse
import datetime
import os
import re
import time
import yaml

from keystoneclient.v2_0 import client as keystoneclient
from glanceclient import client as glanceclient

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils
import functest.utils.openstack_utils as openstack_utils

# parser = argparse.ArgumentParser()
# parser.add_argument("-i", "--installer", help="Installer type")
# args = parser.parse_args()
""" logging configuration """
logger = ft_logger.Logger("onos").getLogger()

with open(os.environ["CONFIG_FUNCTEST_YAML"]) as f:
    functest_yaml = yaml.safe_load(f)
f.close()

# onos parameters
TEST_DB = functest_yaml.get("results").get("test_db_url")
ONOS_REPO_PATH = functest_yaml.get("general").get("directories").get(
    "dir_repos")
ONOS_CONF_DIR = functest_yaml.get("general").get("directories").get(
    "dir_functest_conf")
REPO_PATH = ONOS_REPO_PATH + '/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)

ONOSCI_PATH = ONOS_REPO_PATH + "/"
starttime = datetime.datetime.now()

HOME = os.environ['HOME'] + "/"
INSTALLER_TYPE = os.environ['INSTALLER_TYPE']
DEPLOY_SCENARIO = os.environ['DEPLOY_SCENARIO']
ONOSCI_PATH = ONOS_REPO_PATH + "/"
GLANCE_IMAGE_NAME = functest_yaml.get("onos_sfc").get("image_name")
GLANCE_IMAGE_FILENAME = functest_yaml.get("onos_sfc").get("image_file_name")
GLANCE_IMAGE_FORMAT = functest_yaml.get("general").get("openstack").get(
    "image_disk_format")
GLANCE_IMAGE_PATH = functest_yaml.get("general").get("directories").get(
    "dir_functest_data") + "/" + GLANCE_IMAGE_FILENAME
SFC_PATH = REPO_PATH + functest_yaml.get("general").get("directories").get(
    "dir_onos_sfc")


def RunScript(testname):
    """
    Run ONOS Test Script
    Parameters:
    testname: ONOS Testcase Name
    """
    runtest = ONOSCI_PATH + "onos/TestON/bin/cli.py run " + testname
    logger.debug("Run script " + testname)
    os.system(runtest)


def DownloadCodes(url="https://github.com/wuwenbin2/OnosSystemTest.git"):
    """
    Download Onos Teston codes
    Parameters:
    url: github url
    """
    downloadcode = "git clone " + url + " " + ONOSCI_PATH + "OnosSystemTest"
    logger.debug("Download Onos Teston codes " + url)
    os.system(downloadcode)


def GetResult():
    LOGPATH = ONOSCI_PATH + "onos/TestON/logs"
    cmd = "grep -rnh " + "Fail" + " " + LOGPATH
    Resultbuffer = os.popen(cmd).read()
    # duration = datetime.datetime.now() - starttime
    time.sleep(2)

    if re.search("\s+[1-9]+\s+", Resultbuffer):
        logger.debug("Testcase Fails\n" + Resultbuffer)
        # Result = "Failed"
    else:
        logger.debug("Testcases Success")
        # Result = "Success"
    # payload={'timestart': str(starttime),
    #          'duration': str(duration),
    #            'status': Result}
    cmd = "grep -rnh 'Execution Time' " + LOGPATH
    Resultbuffer = os.popen(cmd).read()
    time1 = Resultbuffer[114:128]
    time2 = Resultbuffer[28:42]
    cmd = "grep -rnh 'Success Percentage' " + LOGPATH + "/FUNCvirNetNB_*"
    Resultbuffer = os.popen(cmd).read()
    if Resultbuffer.find('100%') >= 0:
        result1 = 'Success'
    else:
        result1 = 'Failed'
    cmd = "grep -rnh 'Success Percentage' " + LOGPATH + "/FUNCvirNetNBL3*"
    Resultbuffer = os.popen(cmd).read()
    if Resultbuffer.find('100%') >= 0:
        result2 = 'Success'
    else:
        result2 = 'Failed'
    status1 = []
    status2 = []
    cmd = "grep -rnh 'h3' " + LOGPATH + "/FUNCvirNetNB_*"
    Resultbuffer = os.popen(cmd).read()
    pattern = re.compile("<h3>([^-]+) - ([^-]+) - (\S*)</h3>")
    # res = pattern.search(Resultbuffer).groups()
    res = pattern.findall(Resultbuffer)
    i = 0
    for index in range(len(res)):
        status1.append({'Case name:': res[i][0] + res[i][1],
                        'Case result': res[i][2]})
        i = i + 1
    cmd = "grep -rnh 'h3' " + LOGPATH + "/FUNCvirNetNBL3*"
    Resultbuffer = os.popen(cmd).read()
    pattern = re.compile("<h3>([^-]+) - ([^-]+) - (\S*)</h3>")
    # res = pattern.search(Resultbuffer).groups()
    res = pattern.findall(Resultbuffer)
    i = 0
    for index in range(len(res)):
        status2.append({'Case name:': res[i][0] + res[i][1],
                        'Case result': res[i][2]})
        i = i + 1
    payload = {'timestart': str(starttime),
               'FUNCvirNet': {'duration': time1,
                              'result': result1,
                              'status': status1},
               'FUNCvirNetL3': {'duration': time2,
                                'result': result2,
                                'status': status2}}
    return payload


def SetOnosIp():
    cmd = "openstack catalog show network | grep publicURL"
    cmd_output = os.popen(cmd).read()
    OC1 = re.search(r"\d+\.\d+\.\d+\.\d+", cmd_output).group()
    os.environ['OC1'] = OC1
    time.sleep(2)
    logger.debug("ONOS IP is " + OC1)


def SetOnosIpForJoid():
    cmd = "env | grep SDN_CONTROLLER"
    cmd_output = os.popen(cmd).read()
    OC1 = re.search(r"\d+\.\d+\.\d+\.\d+", cmd_output).group()
    os.environ['OC1'] = OC1
    time.sleep(2)
    logger.debug("ONOS IP is " + OC1)


def CleanOnosTest():
    TESTONPATH = ONOSCI_PATH + "onos/"
    cmd = "rm -rf " + TESTONPATH
    os.system(cmd)
    time.sleep(2)
    logger.debug("Clean ONOS Teston")


def CreateImage():
    creds_keystone = openstack_utils.get_credentials("keystone")
    keystone_client = keystoneclient.Client(**creds_keystone)
    glance_endpoint = keystone_client.service_catalog.url_for(
        service_type='image', endpoint_type='publicURL')
    glance_client = glanceclient.Client(1, glance_endpoint,
                                        token=keystone_client.auth_token)
    EXIT_CODE = -1
    # Check if the given image exists
    image_id = openstack_utils.get_image_id(glance_client, GLANCE_IMAGE_NAME)
    if image_id != '':
        logger.info("Using existing image '%s'..." % GLANCE_IMAGE_NAME)
        global image_exists
        image_exists = True
    else:
        logger.info("Creating image '%s' from '%s'..." % (GLANCE_IMAGE_NAME,
                                                          GLANCE_IMAGE_PATH))
        image_id = openstack_utils.create_glance_image(glance_client,
                                                       GLANCE_IMAGE_NAME,
                                                       GLANCE_IMAGE_PATH)
        if not image_id:
            logger.error("Failed to create a Glance image...")
            return(EXIT_CODE)
        logger.debug("Image '%s' with ID=%s created successfully."
                     % (GLANCE_IMAGE_NAME, image_id))


def SfcTest():
    cmd = "python " + SFC_PATH + "Sfc.py"
    logger.debug("Run sfc tests")
    os.system(cmd)


def SetSfcIp():
    cmd = "openstack catalog show network | grep publicURL"
    cmd_output = os.popen(cmd).read()
    ip = re.search(r"\d+\.\d+\.\d+\.\d+", cmd_output).group()
    cmd_onos_ip = "sed -i 's/onos_ip/" + ip + "/g' " + SFC_PATH + "Sfc_fun.py"
    cmd_openstack_ip = "sed -i 's/openstack_ip/" + ip\
                       + "/g' " + SFC_PATH + "Sfc_fun.py"
    logger.info("Modify ip for SFC")
    os.system(cmd_onos_ip)
    os.system(cmd_openstack_ip)


def main():
    start_time = time.time()
    stop_time = start_time
    # DownloadCodes()
    # if args.installer == "joid":
    if INSTALLER_TYPE == "joid":
        logger.debug("Installer is Joid")
        SetOnosIpForJoid()
    else:
        SetOnosIp()
    RunScript("FUNCvirNetNB")
    RunScript("FUNCvirNetNBL3")
    if DEPLOY_SCENARIO == "os-onos-sfc-ha":
        CreateImage()
        SetSfcIp()
        SfcTest()
    try:
        logger.debug("Push ONOS results into DB")
        # TODO check path result for the file
        result = GetResult()
        stop_time = time.time()

        # ONOS success criteria = all tests OK
        # i.e. FUNCvirNet & FUNCvirNetL3
        status = "failed"
        try:
            if (result['FUNCvirNet']['result'] == "Success" and
                    result['FUNCvirNetL3']['result'] == "Success"):
                    status = "passed"
        except:
            logger.error("Unable to set ONOS criteria")

        functest_utils.push_results_to_db("functest",
                                          "onos",
                                          logger,
                                          start_time,
                                          stop_time,
                                          status,
                                          result)

    except:
        logger.error("Error pushing results into Database")

    # CleanOnosTest()


if __name__ == '__main__':
    main()
