#!/bin/bash
#
# Simple script to check the basic OpenStack clients
#
# Author:
#    jose.lausuch@ericsson.com
#

if [ -z $OS_AUTH_URL ];then
    echo "ERROR: OS_AUTH_URL environment variable missing... Have you sourced the OpenStack credentials?"
    exit 1
fi

echo "Checking OpenStack basic services:"

ip=$(echo $OS_AUTH_URL|sed 's/^.*http\:\/\///'|sed 's/.[^:]*$//')
port=$(echo $OS_AUTH_URL|sed 's/^.*://'|sed 's/.[^\/]*$//')
echo ">>Pinging public keystone endpoint $ip..."
timeout=5
for i in `seq 1 $timeout`; do
    nc -vz $ip $port
    RETVAL=$?
    if [ $RETVAL -eq 0 ]; then
        break
    fi
done
if [ $i -eq $timeout ]; then
    echo "ERROR: Cannot ping the endpoint $ip defined as env variable OS_AUTH_URL."
    echo "OS_AUTH_URL=$OS_AUTH_URL"
    exit 1
fi
echo "  ...OK"

commands=('keystone endpoint-list' 'nova list' 'neutron net-list' \
            'glance image-list' 'cinder list')
for cmd in "${commands[@]}"
do
    service=$(echo $cmd | awk '{print $1}')
    echo ">>Checking $service service..."
    $cmd &>/dev/null
    result=$?
    if [ $result -ne 0 ];
    then

        echo "ERROR: Failed execution $cmd. The $service does not seem to be working."
        exit 1
    else
        echo "  ...OK"
    fi
done

echo "OpenStack services are OK."
exit 0
