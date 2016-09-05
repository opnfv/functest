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


def PreConfig():
    status = "PASS"
    logger.info("Testcase 1 : Prerequisites configuration for SFC")
    logger.info("1.1 Creation of Auth-Token")
    if (Sfc_obj.getToken() == OK):
        logger.info("Creation of Token is successfull")
    else:
        status = "FAIL"
        logger.error("  :  Creation of Token is NOT successfull")
    logger.info("1.2 Creation of Network")
    if (Sfc_obj.createNetworks() == CREATED):
        logger.info("Creation of network is successfull")
    else:
        status = "FAIL"
        logger.error("  :  Creation of network is NOT successfull")
    logger.info("1.3 Creation of Subnetwork")

    if (Sfc_obj.createSubnets() == CREATED):
        logger.info("Creation of Subnetwork is successfull")
    else:
        status = "FAIL"
        logger.error("  :  Creation of Subnetwork is NOT successfull")
    return status


def CreateNodes():
    status = "PASS"
    logger.info("Testcase 2 : Creation of 3 VNF Nodes and Attaching Ports")
    logger.info("2.1 Creation of Ports")
    if (Sfc_obj.createPorts() == CREATED):
        logger.info("Creation of Port is successfull")
    else:
        status = "FAIL"
        logger.error("  :  Creation of Port is NOT successfull")
    logger.info("2.2 Creation of VM-Compute-Node")
    if (Sfc_obj.createVm() == ACCEPTED):
        logger.info("Creation of VM is successfull")
    else:
        status = "FAIL"
        logger.error("  :  Creation of VM is NOT successfull")
    logger.info("2.3 Check VM Status")
    if (Sfc_obj.checkVmState() == OK):
        logger.info("VM are in active state")
    else:
        status = "FAIL"
        logger.error("  :   VM is NOT Active")
    logger.info("2.4 Router Creation")
    if (Sfc_obj.createRouter() == CREATED):
        logger.info("Creation of Router is Successful")
    else:
        status = "FAIL"
        logger.error("  :   Router Creation is NOT Successful")
    logger.info("2.5 Attachement of Interface to VM")
    if (Sfc_obj.attachInterface() == OK):
        logger.info("Interface attached to VM")
    else:
        status = "FAIL"
        logger.error("  :   Interface NOT attached to VM")
    logger.info("2.6 Attachement of FLoating Ip to VM")
    if (Sfc_obj.addFloatingIp() == ACCEPTED):
        logger.info("Floating Ip attached to VM SUccessful")
    else:
        status = "FAIL"
        logger.error("  :   Floating Ip NOT attached to VM ")
    return status


def ConfigSfc():
    status = "PASS"
    logger.info(
        "Testcase 3 : Configure SFC [Portair,PortGroup,Flow classifer]")
    logger.info("3.1 Creation of Port Pair")
    if (Sfc_obj.createPortPair() == CREATED):
        logger.info("Creation of Port pair is successful")
    else:
        status = "FAIL"
        logger.error("  :  Creation of Port pair is NOT successful")
    logger.info("3.2 Getting the  Port Pair ID")
    if (Sfc_obj.getPortPair() == OK):
        logger.info("Port Pair ID is successfully got")
    else:
        status = "FAIL"
        logger.error("  :  UnSuccessfully got Port Pair ID")
    logger.info("3.3 Creation of Port Pair Group")
    if (Sfc_obj.createPortGroup() == CREATED):
        logger.info("Creation of Port Pair Group is successful")
    else:
        status = "FAIL"
        logger.error("  :  Creation of Port Pair Group is NOT successful")
    logger.info("3.4 Getting Port Pair Group ID ")
    if (Sfc_obj.getPortGroup() == OK):
        logger.info("Port Pair Group ID is successfully received")
    else:
        status = "FAIL"
        logger.error("  :  Port Pair Group ID is NOT successfully got")
    logger.info("3.5 Creation of Flow Classifier")
    if (Sfc_obj.createFlowClassifier() == CREATED):
        logger.info("Creation of Flow Classifier is successful")
    else:
        status = "FAIL"
        logger.error("  :  Creation of Flow Classifier is NOT successful")

    logger.info(
        "Testcase 4 : Configure Port Chain and verify flows are added")
    logger.info("4.1 Creation of Port Chain")
    if (Sfc_obj.createPortChain() == CREATED):
        logger.info("Creation of Port Chain is successful")
    else:
        status = "FAIL"
        logger.error("Creation of Port Chain is NOT successful")
    return status


def VerifyiSfcTraffic():
    status = "PASS"
    logger.info("Testcase 5 : Verify  traffic with VNF node.")
    if (Sfc_obj.loginToVM() == "1"):
        logger.info("SFC function Working")
    else:
        status = "FAIL"
        logger.error("  :  SFC function not working")
    return status


def VerifyNoSfcTraffic():
    status = "PASS"
    logger.info("Testcase 6 : Remove the Port Chain and Verify the traffic")
    if (Sfc_obj.deletePortChain() == NO_CONTENT):
        if (Sfc_obj.loginToVM() == "0"):
            logger.info("SFC function is removed Successfully")
        else:
            status = "FAIL"
            logger.error(":SFC function not Removed. Have some problem")
        if (Sfc_obj.deleteFlowClassifier() == NO_CONTENT):
            if (Sfc_obj.deletePortGroup() == NO_CONTENT):
                if (Sfc_obj.deletePortPair() == NO_CONTENT):
                    logger.info(
                        "SFC configuration is deleted successfully")
                else:
                    status = "FAIL"
                    logger.error("  :  Port pair configuration is NOT\
                                  deleted successfully")
            else:
                status = "FAIL"
                logger.error("  :  Port Group configuration is NOT \
                             deleted successfully")
        else:
                status = "FAIL"
                logger.error("  :  Flow classifier configuration is NOT \
                             deleted successfully")
    else:
        status = "FAIL"
        logger.error(":PortChain configuration is NOT deleted \
                     successfully")
    return status


def CleanUp():
    logger.info("Testcase 7 : Cleanup")
    if (Sfc_obj.cleanup() == NO_CONTENT):
        logger.info("CleanUp is successfull")
    else:
        logger.error("  :  CleanUp is NOT successfull")


def isFail(status):
    if status == "FAIL":
        CleanUp()
        exit(-1)


def main():
    """Script to Test the SFC scenarios in ONOS."""
    start_time = time.time()
    isFail(PreConfig())
    isFail(CreateNodes())
    isFail(ConfigSfc())
    isFail(VerifyiSfcTraffic())
    isFail(VerifyNoSfcTraffic())
    CleanUp()
    status = "PASS"
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
                                          details={'timestart': start_time,
                                                   'duration': duration,
                                                   'status': status})
    except:
        logger.error("Error pushing results into Database")

if __name__ == '__main__':
    main()
