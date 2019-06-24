#!/bin/bash

set -e

pushd "${1:-/home/opnfv/functest/images}" > /dev/null

http_proxy=${http_proxy:-http://proxy:8080}
https_proxy=${https_proxy:-${http_proxy:-http://proxy:8080}}
ftp_proxy=${ftp_proxy:-${http_proxy:-http://proxy:8080}}
no_proxy=${no_proxy:-"10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"}

images=${images-"\
ubuntu-14.04-server-cloudimg-amd64-disk1.img \
ubuntu-16.04-server-cloudimg-amd64-disk1.img"}

add_proxy () {
    cat << EOF >> "$1"
http_proxy=${http_proxy}
HTTP_PROXY=${http_proxy}
https_proxy=${https_proxy}
HTTPS_PROXY=${https_proxy}
ftp_proxy=${ftp_proxy}
FTP_PROXY=${ftp_proxy}
no_proxy=${no_proxy}
NO_PROXY=${no_proxy}
EOF
}

add_proxy_apt () {
    cat << EOF >> "$1"
Acquire::http::Proxy "${http_proxy}";
Acquire::https::Proxy "${https_proxy}";
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
    if [[ ${image} == "ubuntu"* ]]; then
        add_proxy_apt "${tmpdir}/etc/apt/apt.conf"
    fi
    guestunmount "${tmpdir}"
done

sudo docker load -i cloudify-docker-manager-community-19.01.24.tar
dockerfile=${tmpdir}/Dockerfile
cat << EOF > $dockerfile
FROM docker-cfy-manager:latest
ENV HTTP_PROXY "${http_proxy}"
ENV HTTPS_PROXY "${https_proxy}"
ENV NO_PROXY "${no_proxy}"
EOF
for f in /etc/sysconfig/cloudify-mgmtworker /etc/sysconfig/cloudify-restservice; do \
    cat << EOF >> $dockerfile
RUN echo >> $f
RUN echo "http_proxy=${http_proxy}" >> $f
RUN echo "https_proxy=${https_proxy}" >> $f
RUN echo "HTTP_PROXY=${http_proxy}" >> $f
RUN echo "HTTPS_PROXY=${https_proxy}" >> $f
RUN echo "no_proxy=${no_proxy}" >> $f
EOF
done
sudo docker build -t docker-cfy-manager -f $dockerfile ${tmpdir}
sudo docker save \
    docker-cfy-manager > cloudify-docker-manager-community-19.01.24.tar
sudo docker rmi docker-cfy-manager

rm "${dockerfile}"
rmdir "${tmpdir}"
popd > /dev/null
