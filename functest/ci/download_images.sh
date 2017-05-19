#!/bin/bash

CIRROS_REPO_URL=http://download.cirros-cloud.net
CIRROS_AARCH64_TAG=161201
CIRROS_X86_64_TAG=0.3.5

RED='\033[1;31m'
NC='\033[0m' # No Color

function usage(){
    echo -e "${RED}USAGE: $script <destination_folder>${NC}"
    exit 0
}

script=`basename "$0"`
IMAGES_FOLDER_DIR=$1

if [[ -z $IMAGES_FOLDER_DIR ]]; then usage; fi;

set -ex
mkdir -p ${IMAGES_FOLDER_DIR}

wget -nc ${CIRROS_REPO_URL}/${CIRROS_X86_64_TAG}/cirros-${CIRROS_X86_64_TAG}-x86_64-disk.img -P ${IMAGES_FOLDER_DIR}
wget -nc ${CIRROS_REPO_URL}/${CIRROS_X86_64_TAG}/cirros-${CIRROS_X86_64_TAG}-x86_64-lxc.tar.gz -P ${IMAGES_FOLDER_DIR}
wget -nc http://artifacts.opnfv.org/sdnvpn/ubuntu-16.04-server-cloudimg-amd64-disk1.img -P ${IMAGES_FOLDER_DIR}

# Add 3rd-party images for aarch64, since Functest can be run on an x86 machine to test an aarch64 POD
wget -nc ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-disk.img -P ${IMAGES_FOLDER_DIR}
wget -nc ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-initramfs -P ${IMAGES_FOLDER_DIR}
wget -nc ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-kernel -P ${IMAGES_FOLDER_DIR}
set +ex