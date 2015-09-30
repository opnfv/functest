#!/bin/bash

# 
# Author: Jose Lausuch (szilard.cserey@ericsson.com)
#
# Installs the Functest framework within the Docker container 
# and run the tests automatically
#


REPOS_DIR=/home/repos

info ()  {
    logger -s -t "start.info" "$*"
}


error () {
    logger -s -t "start.error" "$*"
    exit 1
}



# Check if environment variables are set
if [ -z ${INSTALLER_TYPE} ]; then 
    error "Environment variable 'INSTALLER_TYPE' is not defined."
elif [ "${INSTALLER_TYPE}" != "fuel" ] && [ "${INSTALLER_TYPE}" != "foreman" ]; then
    error "Invalid environment variable INSTALLER_TYPE=${INSTALLER_TYPE}"
fi

if [ -z ${INSTALLER_IP} ]; then 
    error "Environment variable 'INSTALLER_IP' is not defined."
fi




# Update repos
cd ${REPOS_DIR}/functest
git pull 
cd ${REPOS_DIR}/releng
git pull 


# Detect type of installer
# NOTE: this is tricky, since the IPs will have to be the same ALWAYS



# Create Openstack credentials file
${REPOS_DIR}/releng/utils/fetch_os_creds.sh -d /root/openstack.creds \
    -i ${INSTALLER_TYPE} -a ${INSTALLER_IP}
    
if [ $? -ne 0 ]; then
    error "Cannot retrieve credentials file from installation. Check logs."
    exit 1
fi

# Source credentials
source ~/openstack.creds


# Prepare Functest Environment

python ${REPOS_DIR}/functest/testcases/config_functest.py --debug /home/functest/ start
 
 
#4) run vPing
#5) run ODL tests
#6) run Rally bench 
#7) run Tempest
#