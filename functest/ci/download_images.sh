#!/bin/bash

CIRROS_REPO_URL=http://download.cirros-cloud.net
CIRROS_AARCH64_TAG=161201
CIRROS_X86_64_TAG=0.4.0

RED='\033[1;31m'
NC='\033[0m' # No Color

function usage(){
    echo -e "${RED}USAGE: $script <destination_folder> <scenario_name> [arch]${NC}"
    exit 0
}

script=`basename "$0"`
IMAGES_FOLDER_DIR=$1
SCENARIO=$2
ARCH=$3

if [[ -z $IMAGES_FOLDER_DIR ]]; then usage; fi;

set -ex
mkdir -p ${IMAGES_FOLDER_DIR}


wget_opts="-N --tries=1 --connect-timeout=30"

## 1. Cirros 0.4.0 for healthcheck,components and smoke tests(exclude odl tests)
if [[ ${ARCH} == "arm" ]] || [[ ${ARCH} == "aarch64" ]]; then
    # cirros
    wget ${wget_opts} http://download.cirros-cloud.net/daily/20161201/cirros-d161201-aarch64-disk.img -P ${IMAGES_FOLDER_DIR}
    wget ${wget_opts} http://download.cirros-cloud.net/daily/20161201/cirros-d161201-aarch64-initramfs -P ${IMAGES_FOLDER_DIR}
    wget ${wget_opts} http://download.cirros-cloud.net/daily/20161201/cirros-d161201-aarch64-kernel -P ${IMAGES_FOLDER_DIR}

    wget ${wget_opts} https://cloud-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-arm64-uefi1.img -P ${IMAGES_FOLDER_DIR}
    wget ${wget_opts} http://cloud.centos.org/altarch/7/images/aarch64/CentOS-7-aarch64-GenericCloud.qcow2.xz -P ${IMAGES_FOLDER_DIR}
    xz --decompress --force --keep ${IMAGES_FOLDER_DIR}/CentOS-7-aarch64-GenericCloud.qcow2.xz
else
    # cirros
    wget ${wget_opts} http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img -P ${IMAGES_FOLDER_DIR}
    # ubuntu (ubuntu-14.04 is also required by all vnf tests) and centos for snaps_smoke
    wget ${wget_opts} https://cloud-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img -P ${IMAGES_FOLDER_DIR}
    wget ${wget_opts} https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2 -P ${IMAGES_FOLDER_DIR}
    # 1.3 for lxd scenario
    if [[ ${SCENARIO} == *"lxd"* ]]; then
        wget ${wget_opts} http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-lxc.tar.gz -P ${IMAGES_FOLDER_DIR}
    fi
fi

## 3. for bgpvpn and juju_epc
if [[ ${SCENARIO} == *"bgpvpn"* ]] || [[ ${SCENARIO} == *"nosdn-nofeature"* ]]; then
    wget ${wget_opts} https://cloud-images.ubuntu.com/releases/16.04/release/ubuntu-16.04-server-cloudimg-amd64-disk1.img -P ${IMAGES_FOLDER_DIR}
fi

## 4. for VNF and Orchestrator
if [[ ${SCENARIO} == *"nosdn-nofeature"* ]]; then
    wget ${wget_opts} http://repository.cloudifysource.org/cloudify/4.0.1/sp-release/cloudify-manager-premium-4.0.1.qcow2 -P ${IMAGES_FOLDER_DIR}
    wget ${wget_opts} https://sourceforge.net/projects/ool-opnfv/files/vyos-1.1.7.img -P ${IMAGES_FOLDER_DIR}
fi
