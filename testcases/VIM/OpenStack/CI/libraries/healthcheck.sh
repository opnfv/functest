#
# OpenStack Health Check
# This script is meant for really basic API operations on OpenStack
# Services tested: Keystone, Glance, Cinder, Neutron, Nova
#
#
# Author:
#    jose.lausuch@ericsson.com
#
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

set -e

if [ -z $OS_AUTH_URL ]; then
    echo "Source credentials first."
    exit 1
fi

#Redirect all the output (stdout) to a log file and show only possible errors.
LOG_FILE=/home/opnfv/functest/results/healthcheck.log
exec 1<>$LOG_FILE

echo "Using following credentials:"
env | grep OS

## Variables:
project_1="opnfv-tenant1"
project_2="opnfv-tenant2"
user_1="opnfv_user1"
user_2="opnfv_user2"
user_3="opnfv_user3"
user_4="opnfv_user4"
user_5="opnfv_user5"
user_6="opnfv_user6"
image_1="opnfv-image1"
image_2="opnfv-image2"
volume_1="opnfv-volume1"
volume_2="opnfv-volume2"
net_1="opnfv-network1"
net_2="opnfv-network2"
subnet_1="opnfv-subnet1"
subnet_2="opnfv-subnet2"
port_1="opnfv-port1"
port_2="opnfv-port2"
router_1="opnfv-router1"
router_2="opnfv-router2"
instance_1="opnfv-instance1"
instance_2="opnfv-instance2"
instance_3="opnfv-instance3"
instance_4="opnfv-instance4"



function wait_for_ip() {
    # $1 is the instance name
    # $2 is the first octet of the subnet ip
    timeout=60
    while [[ ${timeout} > 0 ]]; do
        if [[ $(nova console-log $1|grep "No lease, failing") ]]; then
            echo "ERROR: The instance $1 couldn't get an IP from the DHCP agent." | tee -a $LOG_FILE 1>&2
            exit 1
        elif [[ $(nova console-log $1|grep "^Lease"|grep "obtained") ]]; then
            echo "The instance $1 got an IP successfully from the DHCP agent."
            break
        fi
        let timeout=timeout-1
        sleep 1
    done
}


#################################
echo "Testing Keystone API..." | tee -a $LOG_FILE 1>&2
#################################
openstack project create ${project_1}
openstack project create ${project_2}

openstack user create ${user_1} --project ${project_1}
openstack user create ${user_2} --project ${project_1}
openstack user create ${user_3} --project ${project_1}
openstack user create ${user_4} --project ${project_2}
openstack user create ${user_5} --project ${project_2}
openstack user create ${user_6} --project ${project_2}

echo "...OK" | tee -a $LOG_FILE 1>&2

#################################
echo "Testing Glance API..." | tee -a $LOG_FILE 1>&2
#################################
image=/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img
glance image-create --name ${image_1} --disk-format qcow2 --container-format bare < ${image}
glance image-create --name ${image_2} --disk-format qcow2 --container-format bare < ${image}

echo "...OK" | tee -a $LOG_FILE 1>&2

#################################
echo "Testing Cinder API..." | tee -a $LOG_FILE 1>&2
#################################
cinder create --display_name ${volume_1} 1
cinder create --display_name ${volume_2} 10

echo "...OK" | tee -a $LOG_FILE 1>&2

#################################
echo "Testing Neutron API..." | tee -a $LOG_FILE 1>&2
#################################

network_ids=($(neutron net-list|grep -v "+"|grep -v name|awk '{print $2}'))
for id in ${network_ids[@]}; do
    [[ $(neutron net-show ${id}|grep 'router:external'|grep -i "true") != "" ]] && ext_net_id=${id}
done
if [[ "${ext_net_id}" == "" ]]; then
    echo "ERROR: No external network found. Exiting Health Check..." | tee -a $LOG_FILE 1>&2
    exit 1
else
    echo "External network found. ${ext_net_id}"
fi

echo "1. Create Networks..."
neutron net-create ${net_1}
neutron net-create ${net_2}
net1_id=$(neutron net-list | grep ${net_1} | awk '{print $2}')
net2_id=$(neutron net-list | grep ${net_2} | awk '{print $2}')

echo "2. Create subnets..."
neutron subnet-create --name ${subnet_1} --allocation-pool start=10.6.0.2,end=10.6.0.253 --gateway 10.6.0.254 ${net_1} 10.6.0.0/24
neutron subnet-create --name ${subnet_2} --allocation-pool start=10.7.0.2,end=10.7.0.253 --gateway 10.7.0.254 ${net_2} 10.7.0.0/24

echo "4. Create Routers..."
neutron router-create ${router_1}
neutron router-create ${router_2}

neutron router-gateway-set ${router_1} ${ext_net_id}
neutron router-gateway-set ${router_2} ${ext_net_id}

neutron router-interface-add ${router_1} ${subnet_1}
neutron router-interface-add ${router_2} ${subnet_2}

echo "...OK" | tee -a $LOG_FILE 1>&2

#################################
echo "Testing Nova API..." | tee -a $LOG_FILE 1>&2
#################################

nova boot --flavor 2 --image ${image_1} --nic net-id=${net1_id} ${instance_1}
nova boot --flavor 2 --image ${image_1} --nic net-id=${net1_id} ${instance_2}
nova boot --flavor 2 --image ${image_2} --nic net-id=${net2_id} ${instance_3}
nova boot --flavor 2 --image ${image_2} --nic net-id=${net2_id} ${instance_4}

vm1_id=$(nova list | grep ${instance_1} | awk '{print $2}')
vm2_id=$(nova list | grep ${instance_2} | awk '{print $2}')
vm3_id=$(nova list | grep ${instance_3} | awk '{print $2}')
vm4_id=$(nova list | grep ${instance_4} | awk '{print $2}')

echo "...OK" | tee -a $LOG_FILE 1>&2

echo "Checking if instances get an IP from DHCP..." | tee -a $LOG_FILE 1>&2

wait_for_ip ${instance_1} "10.6"
wait_for_ip ${instance_2} "10.6"
wait_for_ip ${instance_3} "10.7"
wait_for_ip ${instance_4} "10.7"

echo "Health check passed!" | tee -a $LOG_FILE 1>&2
exit 0
