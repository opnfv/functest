#!/bin/bash

set -e

pushd "${1:-/home/opnfv/functest/images}" > /dev/null

images=${images-"\
cloudify-manager-premium-4.0.1.qcow2 \
ubuntu-14.04-server-cloudimg-amd64-disk1.img \
ubuntu-16.04-server-cloudimg-amd64-disk1.img"}

add_proxy () {
    cat << EOF >> "$1"
http_proxy=${http_proxy:-http://proxy:8080}
HTTP_PROXY=${http_proxy:-http://proxy:8080}
https_proxy=${https_proxy:-${http_proxy:-http://proxy:8080}}
HTTPS_PROXY=${https_proxy:-${http_proxy:-http://proxy:8080}}
ftp_proxy=${ftp_proxy:-${http_proxy:-http://proxy:8080}}
FTP_PROXY=${ftp_proxy:-${http_proxy:-http://proxy:8080}}
no_proxy=${no_proxy:-"10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"}
NO_PROXY=${no_proxy:-"10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"}
EOF
}

add_proxy_apt () {
    cat << EOF >> "$1"
Acquire::http::Proxy "${http_proxy:-http://proxy:8080}";
Acquire::https::Proxy "${https_proxy:-http://proxy:8080}";
EOF
}

tmpdir=$(mktemp -d)
for image in $images; do
    if [ ! -f "$image" ]; then
        echo "skip ${image} ($(pwd)/${image} not found)"
        continue
    fi
    guestmount -a "${image}" -i --rw "${tmpdir}"
    add_proxy "${tmpdir}/etc/environment"
    if [[ ${image} == *"cloudify-manager"* ]]; then
        echo >> "${tmpdir}/etc/sysconfig/cloudify-mgmtworker"
        add_proxy "${tmpdir}/etc/sysconfig/cloudify-mgmtworker"
        echo >> "${tmpdir}/etc/sysconfig/cloudify-restservice"
        add_proxy "${tmpdir}/etc/sysconfig/cloudify-restservice"
    fi
    if [[ ${image} == "ubuntu"* ]]; then
        add_proxy_apt "${tmpdir}/etc/apt/apt.conf"
    fi
    guestunmount "${tmpdir}"
done

rmdir "${tmpdir}"
popd > /dev/null
