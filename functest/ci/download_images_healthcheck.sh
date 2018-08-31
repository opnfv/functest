#!/bin/bash

set -ex

wget_opts="-N --tries=1 --connect-timeout=30"
[ -t 1 ] || wget_opts="${wget_opts} --progress=dot:giga"

cat << EOF  | wget ${wget_opts} -i - -P ${1:-/home/opnfv/functest/images}
http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
EOF
