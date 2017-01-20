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
import urlparse

import argparse
from neutronclient.v2_0 import client as neutronclient

import functest.utils.functest_constants as ft_constants
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as ft_utils
import functest.utils.openstack_utils as openstack_utils


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--testcase", help="Testcase name")
args = parser.parse_args()


""" logging configuration """
logger = ft_logger.Logger("onos").getLogger()

# onos parameters
ONOSCI_PATH = ft_constants.REPOS_DIR + "/"
starttime = datetime.datetime.now()

INSTALLER_TYPE = ft_constants.CI_INSTALLER_TYPE
ONOS_SFC_IMAGE_NAME = ft_constants.ONOS_SFC_IMAGE_NAME
ONOS_SFC_IMAGE_PATH = os.path.join(ft_constants.FUNCTEST_DATA_DIR,
                                   ft_constants.ONOS_SFC_IMAGE_FILENAME)
ONOS_SFC_PATH = os.path.join(ft_constants.FUNCTEST_REPO_DIR,
                             ft_constants.ONOS_SFC_RELATIVE_PATH)


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
    # cmd = "openstack catalog show network | grep publicURL"
    neutron_url = openstack_utils.get_endpoint(service_type='network')
    OC1 = urlparse.urlparse(neutron_url).hostname
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
                                                   ONOS_SFC_IMAGE_NAME,
                                                   ONOS_SFC_IMAGE_PATH)
    EXIT_CODE = -1
    if not image_id:
        logger.error("Failed to create a Glance image...")
        return(EXIT_CODE)
    logger.debug("Image '%s' with ID=%s created successfully."
                 % (ONOS_SFC_IMAGE_NAME, image_id))


def SfcTest():
    cmd = "python " + ONOS_SFC_PATH + "/sfc.py"
    logger.debug("Run sfc tests")
    os.system(cmd)


def GetIp(type):
    # cmd = "openstack catalog show " + type + " | grep publicURL"
    url = openstack_utils.get_endpoint(service_type=type)
    return urlparse.urlparse(url).hostname


def Replace(before, after):
    file = "/sfc_onos.py"
    cmd = "sed -i 's/" + before + "/" + after + "/g' " + ONOS_SFC_PATH + file
    os.system(cmd)


def SetSfcConf():
    Replace("keystone_ip", GetIp("keystone"))
    Replace("neutron_ip", GetIp("neutron"))
    Replace("nova_ip", GetIp("nova"))
    Replace("glance_ip", GetIp("glance"))
    pwd = ft_constants.OS_PASSWORD
    Replace("console", pwd)
    creds_neutron = openstack_utils.get_credentials()
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

        ft_utils.push_results_to_db("functest",
                                    "onos",
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
