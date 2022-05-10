#!/bin/sh

set -e

initdir=$(pwd)
cd "${1:-/home/opnfv/functest/images}"

http_proxy_host=${http_proxy_host:-proxy}
http_proxy_port=${http_proxy_port:-8080}

http_proxy=http://${http_proxy_host}:${http_proxy_port}
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

add_proxy_juju_env () {
    cat << EOF >> "$1"
export no_proxy="${no_proxy}";
export NO_PROXY="${no_proxy}";
EOF
}

add_proxy_juju_systemd () {
    cat << EOF >> "$1"
[Manager]
DefaultEnvironment="no_proxy='${no_proxy}'" "NO_PROXY='${no_proxy}'"
EOF
}

add_proxy_maven () {
    cat << EOF >> "$1"
<settings>
   <proxies>
      <proxy>
        <id>example-proxy</id>
        <active>true</active>
        <protocol>http</protocol>
        <host>"${http_proxy_host}"</host>
        <port>"${http_proxy_port}"</port>
      </proxy>
   </proxies>
</settings>
EOF
}

add_proxy_svn ()  {
    cat << EOF >> "$1"
[global]
http-proxy-host = "${http_proxy_host}"
http-proxy-port = "${http_proxy_port}"
EOF
}

add_proxy_pip ()  {
    cat << EOF >> "$1"
[global]
proxy="${http_proxy}"
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
    if expr "$image" : 'ubuntu' ; then
        add_proxy_apt "${tmpdir}/etc/apt/apt.conf"
        add_proxy_juju_env "${tmpdir}/etc/juju-proxy.conf"
        add_proxy_juju_systemd "${tmpdir}/etc/juju-proxy-systemd.conf"
        mkdir -p ${tmpdir}/root/.m2
        mkdir -p ${tmpdir}/root/.subversion
        add_proxy_maven "${tmpdir}/root/.m2/settings.xml"
        add_proxy_svn "${tmpdir}/root/.subversion/servers"
        add_proxy_pip "${tmpdir}/etc/pip.conf"
    fi
    guestunmount "${tmpdir}"
done

if [ -f cloudify-docker-manager-community-19.01.24.tar ]; then
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
else
    echo "skip cloudify-docker-manager-community-19.01.24.tar \
        ($(pwd)/cloudify-docker-manager-community-19.01.24.tar not found)"
fi

rmdir "${tmpdir}"
cd initdir

