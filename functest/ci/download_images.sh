#!/bin/bash

set -ex

wget_opts="-N --tries=1 --connect-timeout=30"

cat << EOF  | wget ${wget_opts} -i - -P ${1:-/home/opnfv/functest/images}
http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
https://cloud-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img
https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
https://cloud-images.ubuntu.com/releases/16.04/release/ubuntu-16.04-server-cloudimg-amd64-disk1.img
http://repository.cloudifysource.org/cloudify/4.0.1/sp-release/cloudify-manager-premium-4.0.1.qcow2
http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-aarch64-disk.img
https://cloud-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-arm64-uefi1.img
http://cloud.centos.org/altarch/7/images/aarch64/CentOS-7-aarch64-GenericCloud.qcow2.xz
https://sourceforge.net/projects/ool-opnfv/files/vyos-1.1.7.img
http://testresults.opnfv.org/functest/shaker-image.qcow2
http://testresults.opnfv.org/functest/shaker-image-arm64.qcow2
EOF

xz --decompress --force --keep \
    ${1:-/home/opnfv/functest/images}/CentOS-7-aarch64-GenericCloud.qcow2.xz
