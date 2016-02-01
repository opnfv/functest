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

import os
import time
import sys
import logging
import yaml
import datetime
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--installer", help="Installer type")
args = parser.parse_args()
""" logging configuration """

logger = logging.getLogger('onos')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()


formatter = logging.Formatter('%(asctime)s - %(name)s'
                              '- %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)

with open("/home/opnfv/functest/conf/config_functest.yaml") as f:
    functest_yaml = yaml.safe_load(f)
f.close()

# onos parameters
TEST_DB = functest_yaml.get("results").get("test_db_url")
ONOS_REPO_PATH = functest_yaml.get("general").get("directories").get("dir_repos")
ONOS_CONF_DIR = functest_yaml.get("general").get("directories").get("dir_functest_conf")
REPO_PATH = ONOS_REPO_PATH + '/functest/'
if not os.path.exists(REPO_PATH):
    logger.error("Functest repository directory not found '%s'" % REPO_PATH)
    exit(-1)
sys.path.append(REPO_PATH + "testcases/")
import functest_utils

ONOSCI_PATH= REPO_PATH+'testcases/Controllers/ONOS/Teston/CI/'
starttime = datetime.datetime.now()

HOME = os.environ['HOME'] + "/"

def RunScript(testname):
    """
    Run ONOS Test Script
    Parameters:
    testname: ONOS Testcase Name
    """
    runtest = ONOSCI_PATH + "OnosSystemTest/TestON/bin/cli.py run " + testname
    logger.debug( "Run script " + testname )
    os.system(runtest)

def DownloadCodes(url="https://github.com/sunyulin/OnosSystemTest.git"):
    """
    Download Onos Teston codes
    Parameters:
    url: github url
    """
    downloadcode = "git clone " + url + " " + ONOSCI_PATH + "OnosSystemTest"
    logger.debug( "Download Onos Teston codes " + url)
    os.system(downloadcode)

def GetResult():
    LOGPATH = ONOSCI_PATH + "OnosSystemTest/TestON/logs"
    cmd = "grep -rnh " + "Fail" + " " + LOGPATH
    Resultbuffer = os.popen(cmd).read()
    duration = datetime.datetime.now() - starttime
    time.sleep(2)

    if re.search("\s+[1-9]+\s+", Resultbuffer):
        logger.debug("Testcase Fails\n" + Resultbuffer)
        Result = "Failed"
    else:
        logger.debug("Testcases Success")
        Result = "Success"
    #payload={'timestart': str(starttime),
    #          'duration': str(duration),
    #            'status': Result}
    cmd = "grep -rnh 'Execution Time' " + LOGPATH
    Resultbuffer = os.popen(cmd).read()
    time1 = Resultbuffer[114:128] 
    time2 = Resultbuffer[28:42] 
    cmd = "grep -rnh 'Success Percentage' " + LOGPATH + "/FUNCvirNetNB_*"
    Resultbuffer = os.popen(cmd).read()
    if Resultbuffer.find('100%') >= 0: 
        result1='Success'
    else:
        result1='Failed'
    cmd = "grep -rnh 'Success Percentage' " + LOGPATH + "/FUNCvirNetNBL3*"
    Resultbuffer = os.popen(cmd).read()
    if Resultbuffer.find('100%') >= 0:
        result2='Success'
    else:
        result2='Failed'
    payload={'FUNCvirNet':{'duration': time1,
                           'result': result1},
             'FUNCvirNetL3':{'duration': time2,
                           'result': result2}}
    return payload

def SetOnosIp():
    cmd = "keystone catalog --service network | grep publicURL"
    cmd_output = os.popen(cmd).read()
    OC1=re.search(r"\d+\.\d+\.\d+\.\d+",cmd_output).group()
    os.environ['OC1'] = OC1
    time.sleep(2)
    logger.debug( "ONOS IP is " + OC1)

def SetOnosIpForJoid():
    cmd = "env | grep SDN_CONTROLLER"
    cmd_output = os.popen(cmd).read()
    OC1=re.search(r"\d+\.\d+\.\d+\.\d+",cmd_output).group()
    os.environ['OC1'] = OC1
    time.sleep(2)
    logger.debug( "ONOS IP is " + OC1)

def CleanOnosTest():
    TESTONPATH = ONOSCI_PATH + "OnosSystemTest/"
    cmd = "rm -rf " + TESTONPATH
    os.system(cmd)
    time.sleep(2)
    logger.debug( "Clean ONOS Teston" )

def main():

    DownloadCodes()
    if args.installer == "joid":
        logger.debug( "Installer is Joid")
        SetOnosIpForJoid()
    else:
        SetOnosIp()
    RunScript("FUNCvirNetNB")
    RunScript("FUNCvirNetNBL3")

    try:
        logger.debug("Push result into DB")
        # TODO check path result for the file
        scenario = functest_utils.get_scenario(logger)
        pod_name = functest_utils.get_pod_name(logger)
        result = GetResult()
        functest_utils.push_results_to_db(TEST_DB,
                                          "ONOS",
                                          logger, pod_name, scenario,
                                          payload=result)
    except:
        logger.error("Error pushing results into Database")

    CleanOnosTest()


if __name__ == '__main__':
    main()
