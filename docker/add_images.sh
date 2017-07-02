#!/usr/bin/env bash
#
# This script downloads the images that are used for testing
# and places them in the functest docker image

CIRROS_REPO_URL=http://download.cirros-cloud.net
CIRROS_AARCH64_TAG=161201
CIRROS_X86_64_TAG=0.3.5

wget ${CIRROS_REPO_URL}/${CIRROS_X86_64_TAG}/cirros-${CIRROS_X86_64_TAG}-x86_64-disk.img -P ${FUNCTEST_IMAGES_DIR}
wget ${CIRROS_REPO_URL}/${CIRROS_X86_64_TAG}/cirros-${CIRROS_X86_64_TAG}-x86_64-lxc.tar.gz -P ${FUNCTEST_IMAGES_DIR}

# Add the 3-part image for aarch64, since functest can be run from an x86 machine to test an aarch64 POD
wget ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-disk.img -P ${FUNCTEST_IMAGES_DIR}
wget ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-initramfs -P ${FUNCTEST_IMAGES_DIR}
wget ${CIRROS_REPO_URL}/daily/20${CIRROS_AARCH64_TAG}/cirros-d${CIRROS_AARCH64_TAG}-aarch64-kernel -P ${FUNCTEST_IMAGES_DIR}
