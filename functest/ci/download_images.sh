#!/bin/bash

CIRROS_REPO_URL=http://download.cirros-cloud.net
CIRROS_AARCH64_TAG=161201
CIRROS_X86_64_TAG=0.3.5

RED='\033[1;31m'
NC='\033[0m' # No Color

function usage(){
    echo -e "${RED}USAGE: $script <download_dir> <scenario_name> [arch]${NC}"
    exit 0
}

script=`basename "$0"`
IMAGES_DIR=$1
SCENARIO=$2
ARCH=$3

if [[ -z $IMAGES_DIR ]]; then usage; fi;

set -ex
mkdir -p ${IMAGES_DIR}


####################
# MANDATORY IMAGES #
####################
# These images should be present in Functest for the tests to work

# Functest:
wget -nc ${CIRROS_REPO_URL}/${CIRROS_X86_64_TAG}/cirros-${CIRROS_X86_64_TAG}-x86_64-disk.img -P ${IMAGES_DIR}
wget -nc ${CIRROS_REPO_URL}/${CIRROS_X86_64_TAG}/cirros-${CIRROS_X86_64_TAG}-x86_64-lxc.tar.gz -P ${IMAGES_DIR}

# SNAPS:
wget -nc http://uec-images.ubuntu.com/releases/trusty/14.04/ubuntu-14.04-server-cloudimg-amd64-disk1.img -P ${IMAGES_DIR}
wget -nc http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2 -P ${IMAGES_DIR}


###################
# OPTIONAL IMAGES #
###################
# Optional images can be commented if they are not going to be used by the tests

# SDNVPN (odl-bgpvpn scenarios):
if [[ ${SCENARIO} == *"bgpvpn"* ]]; then
    wget -nc http://artifacts.opnfv.org/sdnvpn/ubuntu-16.04-server-cloudimg-amd64-disk1.img -P ${IMAGES_DIR}
fi

# ONOS (onos-sfc scenarios):
if [[ ${SCENARIO} == *"onos-sfc"* ]]; then
    wget -nc http://artifacts.opnfv.org/onosfw/images/firewall_block_image.img -P ${IMAGES_DIR}
fi

if [[ ${ARCH} == "arm" ]] || [[ ${ARCH} == "aarch64" ]]; then
    # ARM (aarch64 cirros images):
    wget -nc ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-disk.img -P ${IMAGES_DIR}
    wget -nc ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-initramfs -P ${IMAGES_DIR}
    wget -nc ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-kernel -P ${IMAGES_DIR}
fi

# PARSER
if [[ ! ${SCENARIO} == *"noha"* ]]; then
    wget -nc http://download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-disk.img -P ${IMAGES_DIR}
fi

set +ex