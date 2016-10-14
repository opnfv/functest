#
# Author: George Paraskevopoulos (geopar@intracom-telecom.com)
#         Manuel Buil (manuel.buil@ericsson.com)
# Prepares the controller and the compute nodes for the odl-sfc testcase
#
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

import os
import sys
import subprocess
import paramiko
import functest.utils.functest_logger as ft_logger

logger = ft_logger.Logger("ODL_SFC").getLogger()

try:
    FUNCTEST_REPO_DIR = os.environ['FUNCTEST_REPO_DIR']
except:
    logger.debug("FUNCTEST_REPO_DIR does not exist!!!!!")

FUNCTEST_REPO_DIR = "/home/opnfv/repos/functest"

try:
    INSTALLER_IP = os.environ['INSTALLER_IP']

except:
    logger.debug("INSTALLER_IP does not exist. We create 10.20.0.2")
    INSTALLER_IP = "10.20.0.2"

os.environ['ODL_SFC_LOG'] = "/home/opnfv/functest/results/odl-sfc.log"
os.environ['ODL_SFC_DIR'] = FUNCTEST_REPO_DIR + "/testcases/features/sfc"

command = os.environ['ODL_SFC_DIR'] + ("/server_presetup_CI.bash | "
                                       "tee -a ${ODL_SFC_LOG} "
                                       "1>/dev/null 2>&1")

output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

# This code is for debugging purposes
# for line in iter(output.stdout.readline, ''):
#    i = line.rstrip()
#    print(i)

# Make sure the process is finished before checking the returncode
if not output.poll():
    output.wait()

# Get return value
if output.returncode:
    print("The presetup of the server did not work")
    sys.exit(output.returncode)

logger.info("The presetup of the server worked ")

ssh_options = "-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(INSTALLER_IP, username="root",
                password="r00tme", timeout=2)
    command = "fuel node | grep compute | awk '{print $10}'"
    logger.info("Executing ssh to collect the compute IPs")
    (stdin, stdout, stderr) = ssh.exec_command(command)
except:
    logger.debug("Something went wrong in the ssh to collect the computes IP")

output = stdout.readlines()
for ip in output:
    command = os.environ['ODL_SFC_DIR'] + ("/compute_presetup_CI.bash "
                                           "" + ip.rstrip() + "| tee -a "
                                           "${ODL_SFC_LOG} 1>/dev/null 2>&1")

    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

# This code is for debugging purposes
#    for line in iter(output.stdout.readline, ''):
#        print(line)
#        sys.stdout.flush()

    output.stdout.close()

    if not (output.poll()):
        output.wait()

    # Get return value
    if output.returncode:
        print("The compute config did not work on compute %s" % ip)
        sys.exit(output.returncode)

sys.exit(0)
