#!/usr/bin/env bash
#
# This script downloads the images that are used for testing
# and places them in the functest docker image

CIRROS_AARCH64_URL=http://download.cirros-cloud.net/daily/20160722
CIRROS_X86_64_URL=http://download.cirros-cloud.net/0.3.4
FUNCTEST_BASE_DIR=/home/opnfv/functest

wget ${CIRROS_X86_64_URL}/cirros-0.3.4-x86_64-disk.img -P ${FUNCTEST_BASE_DIR}/data/
wget ${CIRROS_X86_64_URL}/cirros-0.3.4-x86_64-lxc.tar.gz -P ${FUNCTEST_BASE_DIR}/data/
wget http://205.177.226.237:9999/onosfw/firewall_block_image.img -P ${FUNCTEST_BASE_DIR}/data/

# Add the 3-part image for aarch64, since functest can be run from an x86 machine to test an aarch64 POD
wget ${CIRROS_AARCH64_URL}/cirros-d160722-aarch64-disk.img -P ${FUNCTEST_BASE_DIR}/data/
wget ${CIRROS_AARCH64_URL}/cirros-d160722-aarch64-initramfs -P ${FUNCTEST_BASE_DIR}/data/
wget ${CIRROS_AARCH64_URL}/cirros-d160722-aarch64-kernel -P ${FUNCTEST_BASE_DIR}/data/

