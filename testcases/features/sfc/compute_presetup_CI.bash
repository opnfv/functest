#!/bin/bash

# This script must be use with vxlan-gpe + nsh. Once we have eth + nsh support
# in ODL, we will not need it anymore

set -e
ssh_options='-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
BASEDIR=`dirname $0`
INSTALLER_IP=${INSTALLER_IP:-10.20.0.2}

pushd $BASEDIR
ip=`sshpass -p r00tme ssh $ssh_options root@${INSTALLER_IP} 'fuel node'|grep compute|awk '{print $10}' | head -1`
echo $ip
sshpass -p r00tme scp $ssh_options correct_classifier.bash ${INSTALLER_IP}:/root
sshpass -p r00tme ssh $ssh_options root@${INSTALLER_IP} 'scp correct_classifier.bash '"$ip"':/root'
sshpass -p r00tme ssh $ssh_options root@${INSTALLER_IP} 'ssh root@'"$ip"' bash correct_classifier.bash'
sshpass -p r00tme ssh $ssh_options root@${INSTALLER_IP} 'ssh root@'"$ip"' ifconfig br-int up'
sshpass -p r00tme ssh $ssh_options root@${INSTALLER_IP} 'ssh root@'"$ip"' ip route add 11.0.0.0/24 dev br-int'
