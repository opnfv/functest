#!/bin/bash
set -e
ssh_options='-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'

ip=`sshpass -p r00tme ssh $ssh_options root@10.20.0.2 'fuel node'|grep controller|awk '{print $10}' | head -1`
echo $ip
sshpass -p r00tme scp set-up-tacker.sh 10.20.0.2:/root
sshpass -p r00tme ssh $ssh_options root@10.20.0.2 'scp set-up-tacker.sh '"$ip"':/root'
sshpass -p r00tme ssh $ssh_options root@10.20.0.2 'ssh root@'"$ip"' bash set-up-tacker.sh'
sshpass -p r00tme ssh $ssh_options root@10.20.0.2 'scp '"$ip"':/root/tackerc .'
sshpass -p r00tme scp 10.20.0.2:/root/tackerc .
