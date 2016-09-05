"""Script to Test the SFC scenarios in ONOS."""
# !/usr/bin/python
#
# Copyright (c) 2015 All rights reserved
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

import functest.utils.functest_logger as ft_logger
import functest.utils.functest_utils as functest_utils
import time
from Sfc_fun import Sfc_fun

logger = ft_logger.Logger("sfc").getLogger()
Sfc_obj = Sfc_fun()


def PreConfig():
    status = "PASS"
    logger.info("Testcase 1 : Prerequisites configuration for SFC")
    logger.info("\t1.1 Creation of Auth-Token")
    if (Sfc_obj.getToken() == 200):
        logger.info("\t\tCreation of Token is successfull")
    else:
        status = "FAIL"
        logger.error("\t\t  :  Creation of Token is NOT successfull")
    logger.info("\t1.2 Creation of Network")
    if (Sfc_obj.createNetworks() == 201):
        logger.info("\t\tCreation of network is successfull")
    else:
        status = "FAIL"
        logger.error("\t\t  :  Creation of network is NOT successfull")
    logger.info("\t1.3 Creation of Subnetwork")

    if (Sfc_obj.createSubnets() == 201):
        logger.info("\t\tCreation of Subnetwork is successfull")
    else:
        status = "FAIL"
        logger.error("\t\t  :  Creation of Subnetwork is NOT successfull")
    return status


def CreateNodes():
    status = "PASS"
    logger.info("Testcase 2 : Creation of 3 VNF Nodes and Attaching Ports")
    logger.info("\t2.1 Creation of Ports")
    if (Sfc_obj.createPorts() == 201):
        logger.info("\t\tCreation of Port is successfull")
    else:
        status = "FAIL"
        logger.error("\t\t  :  Creation of Port is NOT successfull")
    logger.info("\t2.2 Creation of VM-Compute-Node")
    if (Sfc_obj.createVm() == 202):
        logger.info("\t\tCreation of VM is successfull")
    else:
        status = "FAIL"
        logger.error("\t\t  :  Creation of VM is NOT successfull")
    logger.info("\t2.3 Check VM Status")
    if (Sfc_obj.checkVmState() == 200):
        logger.info("\t\tVM are in active state")
    else:
        status = "FAIL"
        logger.error("\t\t  :   VM is NOT Active")
    logger.info("\t2.4 Router Creation")
    if (Sfc_obj.createRouter() == 201):
        logger.info("\t\tCreation of Router is Successful")
    else:
        status = "FAIL"
        logger.error("\t\t  :   Router Creation is NOT Successful")
    logger.info("\t2.5 Attachement of Interface to VM")
    if (Sfc_obj.attachInterface() == 200):
        logger.info("\t\tInterface attached to VM")
    else:
        status = "FAIL"
        logger.error("\t\t  :   Interface NOT attached to VM")
    logger.info("\t2.6 Attachement of FLoating Ip to VM")
    if (Sfc_obj.addFloatingIp() == 202):
        logger.info("\t\tFloating Ip attached to VM SUccessful")
    else:
        status = "FAIL"
        logger.error("\t\t  :   Floating Ip NOT attached to VM ")
    return status


def ConfigSfc():
    status = "PASS"
    logger.info(
        "Testcase 3 : Configure SFC [Portair,PortGroup,Flow classifer]")
    logger.info("\t3.1 Creation of Port Pair")
    if (Sfc_obj.createPortPair() == 201):
        logger.info("\t\tCreation of Port pair is successful")
    else:
        status = "FAIL"
        logger.error("\t\t  :  Creation of Port pair is NOT successful")
    logger.info("\t3.2 Getting the  Port Pair ID")
    if (Sfc_obj.getPortPair() == 200):
        logger.info("\t\tPort Pair ID is successfully got")
    else:
        status = "FAIL"
        logger.error("\t\t  :  UnSuccessfully got Port Pair ID")
    logger.info("\t3.3 Creation of Port Pair Group")
    if (Sfc_obj.createPortGroup() == 201):
        logger.info("\t\tCreation of Port Pair Group is successful")
    else:
        status = "FAIL"
        logger.error("\t\t  :  Creation of Port Pair Group is NOT successful")
    logger.info("\t3.4 Getting Port Pair Group ID ")
    if (Sfc_obj.getPortGroup() == 200):
        logger.info("\t\tPort Pair Group ID is successfully received")
    else:
        status = "FAIL"
        logger.error("\t\t  :  Port Pair Group ID is NOT successfully got")
    logger.info("\t3.5 Creation of Flow Classifier")
    if (Sfc_obj.createFlowClassifier() == 201):
        logger.info("\t\tCreation of Flow Classifier is successful")
    else:
        status = "FAIL"
        logger.error("\t\t  :  Creation of Flow Classifier is NOT successful")

    logger.info(
        "Testcase 4 : Configure Port Chain and verify flows are added")
    logger.info("\t4.1 Creation of Port Chain")
    if (Sfc_obj.createPortChain() == 201):
        logger.info("\t\tCreation of Port Chain is successful")
    else:
        status = "FAIL"
        logger.error("\t\tCreation of Port Chain is NOT successful")
    return status


def VerifyiSfcTraffic():
    status = "PASS"
    logger.info("\tTestcase 5 : Verify  traffic with VNF node.")
    if (Sfc_obj.loginToVM() == "1"):
        logger.info("\t\tSFC function Working")
    else:
        status = "FAIL"
        logger.error("\t\t  :  SFC function not working")
    return status


def VerifyNoSfcTraffic():
    status = "PASS"
    logger.info("Testcase 6 : Remove the Port Chain and Verify the traffic")
    if (Sfc_obj.deletePortChain() == 204):
        if (Sfc_obj.loginToVM() == "0"):
            logger.info("\t\tSFC function is removed Successfully")
        else:
            status = "FAIL"
            logger.error("\t\t:SFC function not Removed. Have some problem")
        if (Sfc_obj.deleteFlowClassifier() == 204):
            if (Sfc_obj.deletePortGroup() == 204):
                if (Sfc_obj.deletePortPair() == 204):
                    logger.info(
                        "\t\tSFC configuration is deleted successfully")
                else:
                    status = "FAIL"
                    logger.error("\t\t  :  Port pair configuration is NOT\
                                  deleted successfully")
            else:
                status = "FAIL"
                logger.error("\t\t  :  Port Group configuration is NOT \
                             deleted successfully")
        else:
                status = "FAIL"
                logger.error("\t\t  :  Flow classifier configuration is NOT \
                             deleted successfully")
    else:
        status = "FAIL"
        logger.error("\t\t:PortChain configuration is NOT deleted \
                     successfully")
    return status


def CleanUp():
    logger.info("Testcase 7 : Cleanup")
    if (Sfc_obj.cleanup() == 204):
        logger.info("\t\tCleanUp is successfull")
    else:
        logger.error("\t\t  :  CleanUp is NOT successfull")


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
