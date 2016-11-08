#!/bin/bash

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

ODL_SFC_LOG=/home/opnfv/functest/results/odl-sfc.log
ODL_SFC_DIR=${FUNCTEST_REPO_DIR}/opnfv_tests/features/sfc

# Split the output to the log file and redirect STDOUT and STDERR to /dev/null
bash ${ODL_SFC_DIR}/server_presetup_CI.bash |& \
    tee -a ${ODL_SFC_LOG} 1>/dev/null 2>&1

# Get return value from PIPESTATUS array (bash specific feature)
ret_val=${PIPESTATUS[0]}
if [ $ret_val != 0 ]; then
    echo "The tacker server deployment failed"
    exit $ret_val
fi
echo "The tacker server was deployed successfully"

bash ${ODL_SFC_DIR}/compute_presetup_CI.bash |& \
    tee -a ${ODL_SFC_LOG} 1>/dev/null 2>&1

ret_val=${PIPESTATUS[0]}
if [ $ret_val != 0 ]; then
    exit $ret_val
fi

exit 0
