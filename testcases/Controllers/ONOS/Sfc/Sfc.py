"""Script to Test the SFC scenarios in ONOS."""
# !/usr/bin/python
#
# Copyright (c) CREATED5 All rights reserved
# This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# ###########################################################################
#                          OPNFV SFC Script
# **** Scripted by Antony Silvester  - antony.silvester@huawei.com ******
# ###########################################################################

# Testcase 1 : Prerequisites configuration for SFC
# Testcase 2 : Creation of 3 VNF Nodes and Attaching Ports
# Testcase 3 : Configure  SFC [Port pair,Port Group ,Flow classifer
# Testcase 4 : Configure Port Chain and verify the flows are added.
# Testcase 5 : Verify  traffic with VNF node.
# Testcase 6 : Remove the Port Chain and Verify the traffic.
# Testcase 7 : Cleanup
# ###########################################################################
#

import time
import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils
from Sfc_fun import Sfc_fun

logger = ft_logger.Logger("sfc").getLogger()
Sfc_obj = Sfc_fun()

OK = 200
CREATED = 201
ACCEPTED = 202
NO_CONTENT = 204

start_time = time.time()


def PreConfig():
    logger.info("Testcase 1 : Prerequisites configuration for SFC")
    logger.info("1.1 Creation of Auth-Token")
    if (Sfc_obj.getToken() == OK):
        logger.info("Creation of Token is successfull")
    else:
        fail_info = "Creation of Token is NOT successfull"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("1.2 Creation of Network")
    if (Sfc_obj.createNetworks() == CREATED):
        logger.info("Creation of network is successfull")
    else:
        fail_info = "Creation of network is NOT successfull"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("1.3 Creation of Subnetwork")

    if (Sfc_obj.createSubnets() == CREATED):
        logger.info("Creation of Subnetwork is successfull")
    else:
        fail_info = "Creation of Subnetwork is NOT successfull"
        logger.error(fail_info)
        fail(fail_info)


def CreateNodes():
    logger.info("Testcase 2 : Creation of 3 VNF Nodes and Attaching Ports")
    logger.info("2.1 Creation of Ports")
    if (Sfc_obj.createPorts() == CREATED):
        logger.info("Creation of Port is successfull")
    else:
        fail_info = "Creation of Port is NOT successfull"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("2.2 Creation of VM-Compute-Node")
    if (Sfc_obj.createVm() == ACCEPTED):
        logger.info("Creation of VM is successfull")
    else:
        fail_info = "Creation of VM is NOT successfull"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("2.3 Check VM Status")
    if (Sfc_obj.checkVmState() == OK):
        logger.info("VM are in active state")
    else:
        fail_info = "VM is NOT Active"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("2.4 Router Creation")
    if (Sfc_obj.createRouter() == CREATED):
        logger.info("Creation of Router is Successful")
    else:
        fail_info = "Router Creation is NOT Successful"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("2.5 Attachement of Interface to VM")
    if (Sfc_obj.attachInterface() == OK):
        logger.info("Interface attached to VM")
    else:
        fail_info = "Interface NOT attached to VM"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("2.6 Attachement of FLoating Ip to VM")
    if (Sfc_obj.addFloatingIp() == ACCEPTED):
        logger.info("Floating Ip attached to VM SUccessful")
    else:
        fail_info = "Floating Ip NOT attached to VM"
        logger.error(fail_info)
        fail(fail_info)


def ConfigSfc():
    logger.info(
        "Testcase 3 : Configure SFC [Portair,PortGroup,Flow classifer]")
    logger.info("3.1 Creation of Port Pair")
    if (Sfc_obj.createPortPair() == CREATED):
        logger.info("Creation of Port pair is successful")
    else:
        fail_info = "Creation of Port pair is NOT successful"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("3.2 Getting the  Port Pair ID")
    if (Sfc_obj.getPortPair() == OK):
        logger.info("Port Pair ID is successfully got")
    else:
        fail_info = "UnSuccessfully got Port Pair ID"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("3.3 Creation of Port Pair Group")
    if (Sfc_obj.createPortGroup() == CREATED):
        logger.info("Creation of Port Pair Group is successful")
    else:
        fail_info = "Creation of Port Pair Group is NOT successful"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("3.4 Getting Port Pair Group ID ")
    if (Sfc_obj.getPortGroup() == OK):
        logger.info("Port Pair Group ID is successfully received")
    else:
        fail_info = "Port Pair Group ID is NOT successfully got"
        logger.error(fail_info)
        fail(fail_info)
    logger.info("3.5 Creation of Flow Classifier")
    if (Sfc_obj.createFlowClassifier() == CREATED):
        logger.info("Creation of Flow Classifier is successful")
    else:
        fail_info = "Creation of Flow Classifier is NOT successful"
        logger.error(fail_info)
        fail(fail_info)
    logger.info(
        "Testcase 4 : Configure Port Chain and verify flows are added")
    logger.info("4.1 Creation of Port Chain")
    if (Sfc_obj.createPortChain() == CREATED):
        logger.info("Creation of Port Chain is successful")
    else:
        fail_info = "Creation of Port Chain is NOT successful"
        logger.error(fail_info)
        fail(fail_info)


def VerifySfcTraffic():
    status = "PASS"
    logger.info("Testcase 5 : Verify  traffic with VNF node.")
    if (Sfc_obj.loginToVM() == "1"):
        logger.info("SFC function Working")
    else:
        fail_info = "SFC function not working"
        logger.error(fail_info)
        status = "FAIL"

    logger.info("Testcase 6 : Remove the Port Chain and Verify the traffic")
    if (Sfc_obj.deletePortChain() == NO_CONTENT):
        if (Sfc_obj.loginToVM() == "0"):
            logger.info("SFC function is removed Successfully")
        else:
            fail_info = "SFC function not Removed. Have some problem"
            logger.error(fail_info)
            status = "FAIL"
        if (Sfc_obj.deleteFlowClassifier() == NO_CONTENT):
            if (Sfc_obj.deletePortGroup() == NO_CONTENT):
                if (Sfc_obj.deletePortPair() == NO_CONTENT):
                    logger.info(
                        "SFC configuration is deleted successfully")
                else:
                    fail_info = "Port pair configuration deleted successfully"
                    logger.error(fail_info)
                    status = "FAIL"
            else:
                fail_info = "Port Group is NOT deleted successfully"
                logger.error(fail_info)
                status = "FAIL"
        else:
            fail_info = "Flow classifier is NOT deleted successfully"
            logger.error(fail_info)
            status = "FAIL"
    else:
        fail_info = "PortChain configuration is NOT deleted successfully"
        logger.error(fail_info)
        status = "FAIL"
    if (status == "FAIL"):
        fail("Traffic for SFC is NOT verified successfully")


def CleanUp():
    logger.info("Testcase 7 : Cleanup")
    if (Sfc_obj.cleanup() == NO_CONTENT):
        logger.info("CleanUp is successfull")
    else:
        logger.error("CleanUp is NOT successfull")


def fail(fail_info):
    CleanUp()
    PushDB("FAIL", fail_info)
    exit(-1)


def PushDB(status, info):
    logger.info("Summary :")
    try:
        logger.debug("Push ONOS SFC results into DB")
        stop_time = time.time()

        # ONOS SFC success criteria = all tests OK
        duration = round(stop_time - start_time, 1)
        logger.info("Result is " + status)
        functest_utils.push_results_to_db("functest",
                                          "onos_sfc",
                                          start_time,
                                          stop_time,
                                          status,
                                          details={'duration': duration,
                                                   'status': status,
                                                   'error': info})
    except:
        logger.error("Error pushing results into Database")


def main():
    """Script to Test the SFC scenarios in ONOS."""
    PreConfig()
    CreateNodes()
    ConfigSfc()
    VerifySfcTraffic()
    CleanUp()
    PushDB("PASS", "")


if __name__ == '__main__':
    main()
