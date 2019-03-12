#!/bin/bash

set -ex

wget_opts="-N --tries=1 --connect-timeout=30"
[ -t 1 ] || wget_opts="${wget_opts} --progress=dot:giga"

cat << EOF  | wget ${wget_opts} -i - -P ${1:-/home/opnfv/functest/images}
http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
https://cloud-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img
https://cloud-images.ubuntu.com/releases/16.04/release/ubuntu-16.04-server-cloudimg-amd64-disk1.img
http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-aarch64-disk.img
https://cloud-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-arm64-uefi1.img
http://repository.cloudifysource.org/cloudify/19.01.24/community-release/cloudify-docker-manager-community-19.01.24.tar
http://testresults.opnfv.org/functest/vyos-1.1.8-amd64.qcow2
http://testresults.opnfv.org/functest/shaker-image.qcow2
http://testresults.opnfv.org/functest/shaker-image-arm64.qcow2
EOF
