#!/bin/bash
# SPDX-license-identifier: Apache-2.0

# ******************************
# Script to update the docker host configuration
# to enable Docker Remote API
# ******************************

if [ -f /etc/lsb-release ]; then
    #tested on ubuntu 14.04 and 16.04
    if grep -q "#DOCKER_OPTS=" "/etc/default/docker"; then
        cp /etc/default/docker /etc/default/docker.bak
        sed -i 's/^#DOCKER_OPTS.*$/DOCKER_OPTS=\"-H unix:\/\/\/var\/run\/docker.sock -H tcp:\/\/0.0.0.0:2375\"/g' /etc/default/docker
    else
        echo DOCKER_OPTS=\"-H unix:///var/run/docker.sock -H tcp://0.0.0.0:2375\" >> /etc/default/docker
    fi
    service docker restart
    #docker start $(docker ps -aq)
elif [ -f /etc/system-release ]; then
        #tested on centos 7.2
    if grep -q "ExecStart=\/usr\/bin\/docker-current daemon" "/lib/systemd/system/docker.service"; then
            cp /lib/systemd/system/docker.service /lib/systemd/system/docker.service.bak
            sed -i 's/^ExecStart=.*$/ExecStart=\/usr\/bin\/docker daemon -H tcp:\/\/0.0.0.0:2375 -H unix:\/\/\/var\/run\/docker.sock  \\/g' /lib/systemd/system/docker.service
            systemctl daemon-reload
            systemctl restart docker
        else
            echo "to be implemented"
    fi
else
    echo "OS is not supported"
fi

# Issue Note for Ubuntu
# 1. If the configuration of the file /etc/default/docker does not take effect after restarting docker service,
#    you may try to modify /lib/systemd/system/docker.service
#    commands:
#    cp /lib/systemd/system/docker.service /lib/systemd/system/docker.service.bak
#    sed -i '/^ExecStart/i\EnvironmentFile=-/etc/default/docker' /lib/systemd/system/docker.service
#    sed -i '/ExecStart=\/usr\/bin\/dockerd/{;s/$/ \$DOCKER_OPTS/}' /lib/systemd/system/docker.service
#    systemctl daemon-reload
#    service docker restart
# 2. Systemd is a system and session manager for Linux, where systemctl is one tool for systemd to view and control systemd.
#    If the file /lib/systemd/system/docker.service is modified, systemd has to be reloaded to scan new or changed units.
#    1) systemd and related packages are available on the PPA. To use the PPA, first add it to your software sources list as follows.
#       add-apt-repository ppa:pitti/systemd
#       apt-get update
#    2) system can be installed from the PPS as follows.
#       apt-get install systemd libpam-systemd systemd-ui



