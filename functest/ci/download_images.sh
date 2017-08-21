#!/bin/bash

set -e

cat << EOF  | wget -i - -P ${1:-/home/opnfv/functest/images}
http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img
https://cloud-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img
https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
https://cloud-images.ubuntu.com/releases/16.04/release/ubuntu-16.04-server-cloudimg-amd64-disk1.img
http://repository.cloudifysource.org/cloudify/4.0.1/sp-release/cloudify-manager-premium-4.0.1.qcow2
http://marketplace.openbaton.org:8082/api/v1/images/52e2ccc0-1dce-4663-894d-28aab49323aa/img
http://cloud-images.ubuntu.com/trusty/current/trusty-server-cloudimg-amd64-disk1.img
http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-lxc.tar.gz
http://download.cirros-cloud.net/daily/20161201/cirros-d161201-aarch64-disk.img
http://download.cirros-cloud.net/daily/20161201/cirros-d161201-aarch64-initramfs
http://download.cirros-cloud.net/daily/20161201/cirros-d161201-aarch64-kernel
http://uec-images.ubuntu.com/releases/trusty/14.04/ubuntu-14.04-server-cloudimg-arm64-disk1.img
http://cloud.centos.org/altarch/7/images/aarch64/CentOS-7-aarch64-GenericCloud.qcow2.xz
EOF

xz --decompress ${1:-/home/opnfv/functest/images}/CentOS-7-aarch64-GenericCloud.qcow2.xz

exit $?
