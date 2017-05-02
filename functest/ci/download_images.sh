#!/bin/bash

CIRROS_REPO_URL=http://download.cirros-cloud.net
CIRROS_AARCH64_TAG=161201
CIRROS_X86_64_TAG=0.3.5

set -ex
IMAGES_FOLDER_DIR=$(pwd)/images
mkdir -p ${IMAGES_FOLDER_DIR}

wget -nc ${CIRROS_REPO_URL}/${CIRROS_X86_64_TAG}/cirros-${CIRROS_X86_64_TAG}-x86_64-disk.img -P ${IMAGES_FOLDER_DIR}
wget -nc ${CIRROS_REPO_URL}/${CIRROS_X86_64_TAG}/cirros-${CIRROS_X86_64_TAG}-x86_64-lxc.tar.gz -P ${IMAGES_FOLDER_DIR}
wget -nc http://artifacts.opnfv.org/sdnvpn/ubuntu-16.04-server-cloudimg-amd64-disk1.img -P ${IMAGES_FOLDER_DIR}

# Add the 3-part image for aarch64, since functest can be run from an x86 machine to test an aarch64 POD
wget -nc ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-disk.img -P ${IMAGES_FOLDER_DIR}
wget -nc ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-initramfs -P ${IMAGES_FOLDER_DIR}
wget -nc ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-kernel -P ${IMAGES_FOLDER_DIR}
set +ex
