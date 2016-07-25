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

#Redirect all the output (stdout) to a log file and show only possible errors.
LOG_FILE=/home/opnfv/functest/results/healthcheck.log
YAML_FILE=${CONFIG_FUNCTEST_YAML}
echo "">$LOG_FILE
exec 1<>$LOG_FILE

info ()  {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S,%3N') - healtcheck - INFO - " "$*" | tee -a $LOG_FILE 1>&2
}

debug ()  {
    if [[ "${CI_DEBUG,,}" == "true" ]]; then
        echo -e "$(date '+%Y-%m-%d %H:%M:%S,%3N') - healtcheck - DEBUG - " "$*" | tee -a $LOG_FILE 1>&2
    fi
}

error () {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S,%3N') - healtcheck - ERROR - " "$*" | tee -a $LOG_FILE 1>&2
    exit 1
}

if [ -z $OS_AUTH_URL ]; then
    echo "Source credentials first."
    exit 1
fi


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
kernel_image="opnfv-kernel-img"
ramdisk_image="opnfv-ramdisk-img"
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
flavor="m1.tiny"
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
            error "The instance $1 couldn't get an IP from the DHCP agent." | tee -a $LOG_FILE 1>&2
            exit 1
        elif [[ $(nova console-log $1|grep "^Lease"|grep "obtained") ]]; then
            debug "The instance $1 got an IP successfully from the DHCP agent." | tee -a $LOG_FILE 1>&2
            break
        fi
        let timeout=timeout-1
        sleep 1
    done
}


#################################
info "Testing Keystone API..." | tee -a $LOG_FILE 1>&2
#################################
openstack project create ${project_1}
debug "project '${project_1}' created."
openstack project create ${project_2}
debug "project '${project_2}' created."
openstack user create ${user_1} --project ${project_1}
debug "user '${user_1}' created in project ${project_1}."
openstack user create ${user_2} --project ${project_1}
debug "user '${user_2}' created in project ${project_1}."
openstack user create ${user_3} --project ${project_1}
debug "user '${user_3}' created in project ${project_1}."
openstack user create ${user_4} --project ${project_2}
debug "user '${user_4}' created in project ${project_2}."
openstack user create ${user_5} --project ${project_2}
debug "user '${user_5}' created in project ${project_2}."
openstack user create ${user_6} --project ${project_2}
debug "user '${user_6}' created in project ${project_2}."
info "...Keystone OK!"

#################################
info "Testing Glance API..."
#################################
disk_img=$(cat ${YAML_FILE} | shyaml get-value healthcheck.disk_image 2> /dev/null || true)
kernel_img=$(cat ${YAML_FILE} | shyaml get-value healthcheck.kernel_image 2> /dev/null || true)
ramdisk_img=$(cat ${YAML_FILE} | shyaml get-value healthcheck.ramdisk_image 2> /dev/null || true)
extra_properties=$(cat ${YAML_FILE} | shyaml get-value healthcheck.extra_properties 2> /dev/null || true)

# Test if we need to create a 3part image
if [ "X$kernel_img" != "X" ]
then
    img_id=$(glance image-create --name ${kernel_image} --disk-format aki \
             --container-format bare < ${kernel_img} | awk '$2 == "id" { print $4 }')
    extra_opts="--property kernel_id=${img_id}"

    if [ "X$ramdisk_img" != "X" ]
    then
        img_id=$(glance image-create --name ${ramdisk_image} --disk-format ari \
                 --container-format bare < ${ramdisk_img} | awk '$2 == "id" { print $4 }')
        extra_opts="$extra_opts --property ramdisk_id=${img_id}"
    fi
fi

if [ "X$extra_properties" != "X" ]
then
    keys=$(cat ${YAML_FILE} | shyaml keys healthcheck.extra_properties)
    for key in ${keys}
    do
        value=$(cat ${YAML_FILE} | shyaml get-value healthcheck.extra_properties.${key})
        extra_opts="$extra_opts --property ${key}=\"${value}\""
    done
fi

debug "image extra_properties=${extra_properties}"

eval glance image-create --name ${image_1} --disk-format qcow2 --container-format bare \
             ${extra_opts} < ${disk_img}
debug "image '${image_1}' created."
eval glance image-create --name ${image_2} --disk-format qcow2 --container-format bare \
             ${extra_opts} < ${disk_img}
debug "image '${image_2}' created."
info "... Glance OK!"

#################################
info "Testing Cinder API..."
#################################
cinder create --display_name ${volume_1} 1
debug "volume '${volume_1}' created."
cinder create --display_name ${volume_2} 10
debug "volume '${volume_2}' created."
info "...Cinder OK!"

#################################
info "Testing Neutron API..."
#################################

network_ids=($(neutron net-list|grep -v "+"|grep -v name|awk '{print $2}'))
for id in ${network_ids[@]}; do
    [[ $(neutron net-show ${id}|grep 'router:external'|grep -i "true") != "" ]] && ext_net_id=${id}
done
if [[ "${ext_net_id}" == "" ]]; then
    error "No external network found. Exiting Health Check..."
    exit 1
else
    info "External network found. ${ext_net_id}"
fi

info "1. Create Networks..."
neutron net-create ${net_1}
debug "net '${net_1}' created."
neutron net-create ${net_2}
debug "net '${net_2}' created."
net1_id=$(neutron net-list | grep ${net_1} | awk '{print $2}')
net2_id=$(neutron net-list | grep ${net_2} | awk '{print $2}')

info "2. Create subnets..."
neutron subnet-create --name ${subnet_1} --allocation-pool start=10.6.0.2,end=10.6.0.253 --gateway 10.6.0.254 ${net_1} 10.6.0.0/24
debug "subnet '${subnet_1}' created."
neutron subnet-create --name ${subnet_2} --allocation-pool start=10.7.0.2,end=10.7.0.253 --gateway 10.7.0.254 ${net_2} 10.7.0.0/24
debug "subnet '${subnet_2}' created."

info "3. Create Routers..."
neutron router-create ${router_1}
debug "router '${router_1}' created."
neutron router-create ${router_2}
debug "router '${router_2}' created."

neutron router-gateway-set ${router_1} ${ext_net_id}
debug "router '${router_1}' gateway set to ${ext_net_id}."
neutron router-gateway-set ${router_2} ${ext_net_id}
debug "router '${router_2}' gateway set to ${ext_net_id}."

neutron router-interface-add ${router_1} ${subnet_1}
debug "router '${router_1}' interface added ${subnet_1}."
neutron router-interface-add ${router_2} ${subnet_2}
debug "router '${router_2}' interface added ${subnet_2}."

info "...Neutron OK!"

#################################
info "Testing Nova API..."
#################################

# This delay should be removed after resolving Jira case APEX-149.
# The purpose is to give some time to populate openflow rules
# by SDN controller in case of odl_l2 scenario.
sleep 60


# Check if flavor exists
if [[ -z $(nova flavor-list|grep $flavor) ]]; then
    # if given flavor doesn't exist, we create one
    debug "Flavor $flavor doesn't exist. Creating a new flavor."
    nova flavor-create --is-public false ${flavor} auto 512 1 1 --is-public True
fi
debug "Using flavor $flavor to boot the instances."


nova boot --flavor ${flavor} --image ${image_1} --nic net-id=${net1_id} ${instance_1}
debug "nova instance '${instance_1}' booted on ${net_1}."
nova boot --flavor ${flavor} --image ${image_1} --nic net-id=${net1_id} ${instance_2}
debug "nova instance '${instance_2}' booted on ${net_1}."
nova boot --flavor ${flavor} --image ${image_2} --nic net-id=${net2_id} ${instance_3}
debug "nova instance '${instance_3}' booted on ${net_2}."
nova boot --flavor ${flavor} --image ${image_2} --nic net-id=${net2_id} ${instance_4}
debug "nova instance '${instance_4}' booted on ${net_2}."

vm1_id=$(nova list | grep ${instance_1} | awk '{print $2}')
vm2_id=$(nova list | grep ${instance_2} | awk '{print $2}')
vm3_id=$(nova list | grep ${instance_3} | awk '{print $2}')
vm4_id=$(nova list | grep ${instance_4} | awk '{print $2}')
info "...Nova OK!"

info "Checking if instances get an IP from DHCP..."
wait_for_ip ${instance_1} "10.6"
wait_for_ip ${instance_2} "10.6"
wait_for_ip ${instance_3} "10.7"
wait_for_ip ${instance_4} "10.7"
info "...DHCP OK!"

info "Health check passed!"
exit 0
