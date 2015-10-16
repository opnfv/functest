#!/bin/bash
##############################################################################
# Copyright (c) 2015 Ericsson AB and others.
# jose.lausuch@ericsson.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


CMD_ODL="/opt/opendaylight/bin/client -u karaf info 2>/dev/null | grep -i opendaylight | wc -l"
CMD_ONOS="/opt/opendaylight/bin/client -u karaf info 2>/dev/null | grep -i onos | wc -l"
CMD_CONTRAIL="/opt/opendaylight/bin/client -u karaf info 2>/dev/null | grep -i contrail | wc -l"

usage() {
    echo "usage: $0 -i <installer_type> -a <installer_ip>" >&2
}

info ()  {
    logger -s -t "get_sdn_type.info" "$*"
}


error () {
    logger -s -t "get_sdn_type.error" "$*"
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
        i) installer_type=${OPTARG} ;;
        a) installer_ip=${OPTARG} ;;
        *) echo "Non-option argument: '-${OPTARG}'" >&2
           usage
           exit 2
           ;;
    esac
done

# set vars from env if not provided by user as options
installer_type=${installer_type:-$INSTALLER_TYPE}
installer_ip=${installer_ip:-$INSTALLER_IP}

if [ -z $installer_type ] || [ -z $installer_ip ]; then
    usage
    exit 2
fi


ssh_options="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"

# Start fetching the files
if [ "$installer_type" == "fuel" ]; then
    #ip_fuel="10.20.0.2"
    verify_connectivity $installer_ip

    # Check if controller is alive (online='True')
    controller_ips=$(sshpass -p r00tme ssh 2>/dev/null $ssh_options root@${installer_ip} \
        'fuel node | grep controller | grep True | awk "{print \$10}"') &> /dev/null

    if [ -z "$controller_ips" ]; then
        error "Controller IPs not found. Please check that the POD is correctly deployed."
    fi


    info "Checking Karaf in each controller..."
    for ip in $controller_ips;
    do
        info "Checking type of controller ${ip}.."
        result=$(sshpass -p r00tme ssh 2>/dev/null $ssh_options root@${installer_ip} \
        "ssh ${ssh_options} ${ip} ${CMD_ODL}")
        if [ $result -gt 0 ]; then
            info "ODL controller found!"
            exit 0
        fi
        result=$(sshpass -p r00tme ssh 2>/dev/null $ssh_options root@${installer_ip} \
        "ssh ${ssh_options} ${ip} ${CMD_ONOS}")
        if [ $result -gt 0 ]; then
            info "ONOS controller found!"
            exit 0
        fi
        result=$(sshpass -p r00tme ssh 2>/dev/null $ssh_options root@${installer_ip} \
        "ssh ${ssh_options} ${ip} ${CMD_CONTRAIL}")
        if [ $result -gt 0 ]; then
            info "OpenContrail controller found!"
            exit 0
        fi
    done
    info "None of the 3 supported controllers has been found."

elif [ "$installer_type" == "foreman" ]; then
    # TO BE DONE
    echo "not implemented"

elif [ "$installer_type" == "compass" ]; then
    # TO BE DONE
    echo "not implemented"

else
    error "Installer $installer is not supported by this script"
fi



exit 0
