#!/bin/sh

set -ex

initdir=$(pwd)

cd "${1:-/home/opnfv/functest/images}"

for i in *.img *.qcow2; do
    qemu-img convert -f qcow2 -O vmdk "$i" "${i%.*}.vmdk"
done

cd $initdir
