#!/bin/bash
#
# Simple script to check the basic OpenStack clients
#
# Author:
#    jose.lausuch@ericsson.com
#

declare -A service_cmd_array
service_cmd_array['nova']='openstack server list'
service_cmd_array['neutron']='openstack network list'
service_cmd_array['keystone']='openstack endpoint list'
service_cmd_array['cinder']='openstack volume list'
service_cmd_array['glance']='openstack image list'

MANDATORY_SERVICES='nova neutron keystone glance'
OPTIONAL_SERVICES='cinder'

verify_connectivity() {
    for i in $(seq 0 9); do
        if echo "test" | nc -v -w 10 $1 $2 &>/dev/null; then
            return 0
        fi
        sleep 1
    done
    return 1
}

verify_SSL_connectivity() {
    openssl s_client -connect $1:$2 &>/dev/null
    return $?
}

check_service() {
    local service cmd
    service=$1
    cmd=${service_cmd_array[$service]}
    if [ -z "$2" ]; then
        required='false'
    else
        required=$2
    fi
    echo ">>Checking ${service} service..."
    if ! openstack service list | grep -i ${service} > /dev/null; then
        if [ "$required" == 'false' ]; then
            echo "WARN: Optional Service ${service} is not enabled!"
            return
        else
            echo "ERROR: Required Service ${service} is not enabled!"
            exit 1
        fi
    fi
    $cmd &>/dev/null
    result=$?
    if [ $result -ne 0 ]; then
        echo "ERROR: Failed execution $cmd. The $service does not seem to be working."
        exit 1
    else
        echo "  ...OK"
    fi
}

if [ -z $OS_AUTH_URL ];then
    echo "ERROR: OS_AUTH_URL environment variable missing... Have you sourced the OpenStack credentials?"
    exit 1
fi


echo "Checking OpenStack endpoints:"
publicURL=$(openstack catalog show  identity |awk '/public/ {print $4}')
publicIP=$(echo $publicURL|sed 's/^.*http.*\:\/\///'|sed 's/.[^:]*$//')
publicPort=$(echo $publicURL|sed 's/^.*://'|sed 's/\/.*$//')
https_enabled=$(echo $publicURL | grep 'https')
if [[ -n $https_enabled ]]; then
    echo ">>Verifying SSL connectivity to the public endpoint $publicIP:$publicPort..."
    verify_SSL_connectivity $publicIP $publicPort
else
    echo ">>Verifying connectivity to the public endpoint $publicIP:$publicPort..."
    verify_connectivity $publicIP $publicPort
fi
RETVAL=$?
if [ $RETVAL -ne 0 ]; then
    echo "ERROR: Cannot talk to the public endpoint $publicIP:$publicPort ."
    echo "OS_AUTH_URL=$OS_AUTH_URL"
    exit 1
fi
echo "  ...OK"

adminURL=$(openstack catalog show  identity |awk '/admin/ {print $4}')
if [ -z ${adminURL} ]; then
    echo "ERROR: Cannot determine the admin URL."
    openstack catalog show identity
    exit 1
fi
adminIP=$(echo $adminURL|sed 's/^.*http.*\:\/\///'|sed 's/.[^:]*$//')
adminPort=$(echo $adminURL|sed 's/^.*://'|sed 's/.[^\/]*$//')
https_enabled=$(echo $adminURL | grep 'https')
if [[ -n $https_enabled ]]; then
    echo ">>Verifying SSL connectivity to the admin endpoint $adminIP:$adminPort..."
    verify_SSL_connectivity $adminIP $adminPort
else
    echo ">>Verifying connectivity to the admin endpoint $adminIP:$adminPort..."
    verify_connectivity $adminIP $adminPort
fi
RETVAL=$?
if [ $RETVAL -ne 0 ]; then
    echo "ERROR: Cannot talk to the admin endpoint $adminIP:$adminPort ."
    echo "$adminURL"
    exit 1
fi
echo "  ...OK"


echo "Checking Required OpenStack services:"
for service in $MANDATORY_SERVICES; do
    check_service $service "true"
done
echo "Required OpenStack services are OK."

echo "Checking Optional OpenStack services:"
for service in $OPTIONAL_SERVICES; do
    check_service $service
done

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
