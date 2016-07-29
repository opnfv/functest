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

import datetime
import os
import re
import time
import argparse

from neutronclient.v2_0 import client as neutronclient

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils
import functest.utils.openstack_utils as openstack_utils

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--testcase", help="Testcase name")
args = parser.parse_args()


""" logging configuration """
logger = ft_logger.Logger("onos").getLogger()

# onos parameters
TEST_DB = functest_utils.get_parameter_from_yaml(
    "results.test_db_url")
ONOS_REPO_PATH = functest_utils.get_parameter_from_yaml(
    "general.directories.dir_repos")
ONOS_CONF_DIR = functest_utils.get_parameter_from_yaml(
    "general.directories.dir_functest_conf")
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
GLANCE_IMAGE_NAME = functest_utils.get_parameter_from_yaml(
    "onos_sfc.image_name")
GLANCE_IMAGE_FILENAME = functest_utils.get_parameter_from_yaml(
    "onos_sfc.image_file_name")
GLANCE_IMAGE_PATH = functest_utils.get_parameter_from_yaml(
    "general.directories.dir_functest_data") + "/" + GLANCE_IMAGE_FILENAME
SFC_PATH = REPO_PATH + functest_utils.get_parameter_from_yaml(
    "general.directories.dir_onos_sfc")


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
    glance_client = openstack_utils.get_glance_client()
    image_id = openstack_utils.create_glance_image(glance_client,
                                                   GLANCE_IMAGE_NAME,
                                                   GLANCE_IMAGE_PATH)
    EXIT_CODE = -1
    if not image_id:
        logger.error("Failed to create a Glance image...")
        return(EXIT_CODE)
    logger.debug("Image '%s' with ID=%s created successfully."
                 % (GLANCE_IMAGE_NAME, image_id))


def SfcTest():
    cmd = "python " + SFC_PATH + "Sfc.py"
    logger.debug("Run sfc tests")
    os.system(cmd)


def GetIp(type):
    cmd = "openstack catalog show " + type + " | grep publicURL"
    cmd_output = os.popen(cmd).read()
    ip = re.search(r"\d+\.\d+\.\d+\.\d+", cmd_output).group()
    return ip


def Replace(before, after):
    file = "Sfc_fun.py"
    cmd = "sed -i 's/" + before + "/" + after + "/g' " + SFC_PATH + file
    os.system(cmd)


def SetSfcConf():
    Replace("keystone_ip", GetIp("keystone"))
    Replace("neutron_ip", GetIp("neutron"))
    Replace("nova_ip", GetIp("nova"))
    Replace("glance_ip", GetIp("glance"))
    pwd = os.environ['OS_PASSWORD']
    Replace("console", pwd)
    creds_neutron = openstack_utils.get_credentials("neutron")
    neutron_client = neutronclient.Client(**creds_neutron)
    ext_net = openstack_utils.get_external_net(neutron_client)
    Replace("admin_floating_net", ext_net)
    logger.info("Modify configuration for SFC")


def OnosTest():
    start_time = time.time()
    stop_time = start_time
    if INSTALLER_TYPE == "joid":
        logger.debug("Installer is Joid")
        SetOnosIpForJoid()
    else:
        SetOnosIp()
    RunScript("FUNCvirNetNB")
    RunScript("FUNCvirNetNBL3")
    try:
        logger.debug("Push ONOS results into DB")
        # TODO check path result for the file
        result = GetResult()
        stop_time = time.time()

        # ONOS success criteria = all tests OK
        # i.e. FUNCvirNet & FUNCvirNetL3
        status = "FAIL"
        try:
            if (result['FUNCvirNet']['result'] == "Success" and
                    result['FUNCvirNetL3']['result'] == "Success"):
                    status = "PASS"
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

    if status == "FAIL":
        EXIT_CODE = -1
        exit(EXIT_CODE)


def main():

    if args.testcase == "sfc":
        CreateImage()
        SetSfcConf()
        SfcTest()
    else:
        OnosTest()

if __name__ == '__main__':
    main()
