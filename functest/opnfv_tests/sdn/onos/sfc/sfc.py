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
"""Script to Test the SFC scenarios in ONOS."""

import logging
import time
import functest.utils.functest_utils as ft_utils
from sfc_onos import SfcOnos

logger = logging.getLogger(__name__)
Sfc_obj = SfcOnos()

OK = 200
CREATED = 201
ACCEPTED = 202
NO_CONTENT = 204

start_time = time.time()


def PreConfig():
    logger.info("Testcase 1 : Prerequisites configuration for SFC")
    logger.info("1.1 Creation of Auth-Token")
    check(Sfc_obj.getToken, OK, "Creation of Token")
    logger.info("1.2 Creation of Network")
    check(Sfc_obj.createNetworks, CREATED, "Creation of network")
    logger.info("1.3 Creation of Subnetwork")
    check(Sfc_obj.createSubnets, CREATED, "Creation of Subnetwork")


def CreateNodes():
    logger.info("Testcase 2 : Creation of 3 VNF Nodes and Attaching Ports")
    logger.info("2.1 Creation of Ports")
    check(Sfc_obj.createPorts, CREATED, "Creation of Port")
    logger.info("2.2 Creation of VM-Compute-Node")
    check(Sfc_obj.createVm, ACCEPTED, "Creation of VM")
    logger.info("2.3 Check VM Status")
    check(Sfc_obj.checkVmState, OK, "Vm statue check")
    logger.info("2.4 Router Creation")
    check(Sfc_obj.createRouter, CREATED, "Creation of Router")
    logger.info("2.5 Attachement of Interface to VM")
    check(Sfc_obj.attachInterface, OK, "Interface attached to VM")
    logger.info("2.6 Attachement of FLoating Ip to VM")
    check(Sfc_obj.addFloatingIp, ACCEPTED, "Floating Ip attached to VM")


def ConfigSfc():
    logger.info(
        "Testcase 3 : Configure SFC [Portair,PortGroup,Flow classifer]")
    logger.info("3.1 Creation of Port Pair")
    check(Sfc_obj.createPortPair, CREATED, "Creation of Port Pair")
    logger.info("3.2 Getting the  Port Pair ID")
    check(Sfc_obj.getPortPair, OK, "Getting Port Pair ID")
    logger.info("3.3 Creation of Port Pair Group")
    check(Sfc_obj.createPortGroup, CREATED, "Creation of Port Pair Group")
    logger.info("3.4 Getting Port Pair Group ID ")
    check(Sfc_obj.getPortGroup, OK, "Getting Port Pair Group ID")
    logger.info("3.5 Creation of Flow Classifier")
    check(Sfc_obj.createFlowClassifier, CREATED, "Creation of Flow Classifier")
    logger.info(
        "Testcase 4 : Configure Port Chain and verify flows are added")
    logger.info("4.1 Creation of Port Chain")
    check(Sfc_obj.createPortChain, CREATED, "Creation of Port Chain")


def VerifySfcTraffic():
    status = "PASS"
    logger.info("Testcase 5 : Verify  traffic with VNF node.")
    if (Sfc_obj.loginToVM() == "1"):
        logger.info("SFC function Working")
    else:
        logger.error("SFC function not working")
        status = "FAIL"

    logger.info("Testcase 6 : Remove the Port Chain and Verify the traffic")
    if (Sfc_obj.deletePortChain() == NO_CONTENT):
        if (Sfc_obj.loginToVM() == "0"):
            logger.info("SFC function is removed Successfully")
        else:
            logger.error("SFC function not Removed. Have some problem")
            status = "FAIL"
        if (Sfc_obj.deleteFlowClassifier() == NO_CONTENT):
            if (Sfc_obj.deletePortGroup() == NO_CONTENT):
                if (Sfc_obj.deletePortPair() == NO_CONTENT):
                    logger.info(
                        "SFC configuration is deleted successfully")
                else:
                    logger.error("Port pair is deleted successfully")
                    status = "FAIL"
            else:
                logger.error("Port Group is NOT deleted successfully")
                status = "FAIL"
        else:
            logger.error("Flow classifier is NOT deleted successfully")
            status = "FAIL"
    else:
        logger.error("PortChain configuration is NOT deleted successfully")
        status = "FAIL"
    if (status == "FAIL"):
        fail("Traffic for SFC is NOT verified successfully")


def CleanUp():
    logger.info("Testcase 7 : Cleanup")
    if (Sfc_obj.cleanup() == NO_CONTENT):
        logger.info("CleanUp is successfull")
    else:
        logger.error("CleanUp is NOT successfull")


def check(method, criteria, msg):
    if (method() == criteria):
        logger.info(msg + 'is Successful')
    else:
        fail(msg + 'is not successful')


def fail(fail_info):
    logger.error(fail_info)
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
        ft_utils.push_results_to_db("functest",
                                    "onos_sfc",
                                    start_time,
                                    stop_time,
                                    status,
                                    details={'duration': duration,
                                             'error': info})
    except:
        logger.error("Error pushing results into Database")


def main():
    """Script to Test the SFC scenarios in ONOS."""
    logging.basicConfig()
    PreConfig()
    CreateNodes()
    ConfigSfc()
    VerifySfcTraffic()
    CleanUp()
    PushDB("PASS", "")


if __name__ == '__main__':
    main()
