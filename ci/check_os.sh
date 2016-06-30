#!/bin/bash
#
# Simple script to check the basic OpenStack clients
#
# Author:
#    jose.lausuch@ericsson.com
#

verify_connectivity() {
    for i in $(seq 0 9); do
        if echo "test" | nc -v -w 10 $1 $2 &>/dev/null; then
            return 0
        fi
        sleep 1
    done
    return 1
}


if [ -z $OS_AUTH_URL ];then
    echo "ERROR: OS_AUTH_URL environment variable missing... Have you sourced the OpenStack credentials?"
    exit 1
fi


echo "Checking OpenStack endpoints:"
publicURL=$OS_AUTH_URL
publicIP=$(echo $publicURL|sed 's/^.*http\:\/\///'|sed 's/.[^:]*$//')
publicPort=$(echo $publicURL|sed 's/^.*://'|sed 's/\/.*$//')
echo ">>Verifying connectivity to the public endpoint $publicIP:$publicPort..."
verify_connectivity $publicIP $publicPort
RETVAL=$?
if [ $RETVAL -ne 0 ]; then
    echo "ERROR: Cannot talk to the public endpoint $publicIP:$publicPort ."
    echo "OS_AUTH_URL=$OS_AUTH_URL"
    exit 1
fi
echo "  ...OK"

adminURL=$(openstack catalog show  identity |grep adminURL|awk '{print $4}')
adminIP=$(echo $adminURL|sed 's/^.*http\:\/\///'|sed 's/.[^:]*$//')
adminPort=$(echo $adminURL|sed 's/^.*://'|sed 's/.[^\/]*$//')
echo ">>Verifying connectivity to the admin endpoint $adminIP:$adminPort..."
verify_connectivity $adminIP $adminPort
RETVAL=$?
if [ $RETVAL -ne 0 ]; then
    echo "ERROR: Cannot talk to the admin endpoint $adminIP:$adminPort ."
    echo "$adminURL"
    exit 1
fi
echo "  ...OK"


echo "Checking OpenStack basic services:"
commands=('openstack endpoint list' 'nova list' 'neutron net-list' \
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

echo "Checking External network..."
networks=($(neutron net-list -F id | tail -n +4 | head -n -1 | awk '{print $2}'))
is_external=False
for net in "${networks[@]}"
do
    is_external=$(neutron net-show $net|grep "router:external"|awk '{print $4}')
    if [ $is_external == "True" ]; then
        echo "External network found: $net"
        break
    fi
done
if [ $is_external == "False" ]; then
    echo "ERROR: There are no external networks in the deployment."
    exit 1
fi

exit 0
