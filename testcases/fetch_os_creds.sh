#!/bin/bash
##############################################################################
# Copyright (c) 2015 Ericsson AB and others.
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


usage() {
    echo "usage: $0 -d <destination> -i <installer_type> -a <installer_ip>" >&2
}

info ()  {
    logger -s -t "retrieve_rc.info" "$*"
}


error () {
    logger -s -t "retrieve_rc.error" "$*"
    exit 1
}


verify_connectivity() {
    local ip=$1
    info "Verifying connectivity to $ip..."
    for i in $(seq 0 10); do
        if ping -c 1 -W 1 $ip > /dev/null; then
            info "$ip is reachable!"
            return 0
        fi
        sleep 1
    done
    error "Can not talk to $ip."
}



#Get options
while getopts ":d:i:a:h:" optchar; do
    case "${optchar}" in
        d) dest_path=${OPTARG} ;;
        i) installer_type=${OPTARG} ;;
        a) installer_ip=${OPTARG} ;;
        *) echo "Non-option argument: '-${OPTARG}'" >&2
           usage
           exit 2
           ;;
    esac
done

if [ -z $dest_path ] || [ -z $installer_type ] || [ -z $installer_ip ]; then
    usage
    exit 2
fi


# Checking if destination path is valid
if [ -d $dest_path ]; then
    error "Please provide the full destination path for the credentials file including the filename"
fi

touch $dest_path || error "Cannot create the file specified. Check that the path is correct and run the script again."
echo "">$dest_path $empty the file

if [ "$installer_type" == "fuel" ]; then
    #ip_fuel="10.20.0.2"
    echo "Fetching openrc from a Fuel Controller and storing it in $dest_path"
    verify_connectivity $installer_ip
    sshpass -p r00tme ssh 2>/dev/null -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@${installer_ip} 'scp $(fuel node | grep controller | grep True | awk "{print \$10}" | tail -1):/root/openrc .'
    sshpass -p r00tme scp 2>/dev/null -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@${installer_ip}:~/openrc $dest_path

elif [ "$installer" == "foreman" ]; then
    #ip_foreman="172.30.10.73"
    echo "Fetching openrc from a Foreman Controller and storing it in $dest_path"
    verify_connectivity $installer_ip
    sshpass -p vagrant ssh root@${installer_ip} "sshpass -p Op3nStack scp root@oscontroller1.opnfv.com:~/keystonerc_admin ."
    sshpass -p vagrant scp root@${installer_ip}:~/keystonerc_admin $dest_path

else
    error "Installer $installer is not supported by this script"
fi
