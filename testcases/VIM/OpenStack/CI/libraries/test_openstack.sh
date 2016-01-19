#
# Script to test clean_openstack.py
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

if [ -z $OS_AUTH_URL ]; then
    echo "Source credentials first"
    exit 1
fi

echo "Using following credentials:"
env | grep OS

#################################
echo "Creating keystone stuff.."
#################################
keystone tenant-create --name tenant_test1
keystone tenant-create --name tenant_test2
tenant1_id=$(keystone tenant-list | grep tenant_test1 | awk '{print $2}')
tenant2_id=$(keystone tenant-list | grep tenant_test2 | awk '{print $2}')
keystone user-create --name user_test11 --tenant $tenant1_id
keystone user-create --name user_test12 --tenant $tenant1_id
keystone user-create --name user_test13 --tenant $tenant1_id
keystone user-create --name user_test21 --tenant $tenant2_id
keystone user-create --name user_test22 --tenant $tenant2_id


#################################
echo "Creating glance stuff.."
#################################
wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
glance image-create --name image_test1 --disk-format qcow2 --container-format bare < cirros-0.3.4-x86_64-disk.img
glance image-create --name image_test2 --disk-format qcow2 --container-format bare < cirros-0.3.4-x86_64-disk.img
#glance image-create --name test --visibility public --disk-format qcow2 --container-format bare --file cirros-0.3.4-x86_64-disk.img


#################################
echo "Creating cinder stuff.."
#################################
cinder create --display_name volume-test1 1
cinder create --display_name volume-test2 2


#################################
echo "Creating NEUTRON stuff.."
#################################
echo "1. Create Networks."
neutron net-create net-test1
neutron net-create net-test2

echo "2. Create subnets."
neutron subnet-create --name subnet-test11 --allocation-pool start=10.7.0.2,end=10.7.0.253 --gateway 10.7.0.254 net-test1 10.7.0.0/24
neutron subnet-create --name subnet-test21 --allocation-pool start=10.6.0.2,end=10.6.0.253 --gateway 10.6.0.254 net-test2 10.6.0.0/24

echo "3. Create Ports."
neutron port-create --name port-test11 --fixed-ip ip_address=10.7.0.10 net-test1
neutron port-create --name port-test21 --fixed-ip ip_address=10.6.0.60 net-test2


echo "4. Create Routers."
neutron router-create router-test1
neutron router-create router-test2
router1_id=$(neutron router-list | grep router-test1 | awk '{print $2}')
router1_id=$(neutron router-list | grep router-test2 | awk '{print $2}')

neutron router-gateway-set router-test1 net04_ext
neutron router-gateway-set router-test2 net04_ext

neutron router-interface-add router-test1 subnet-test11
neutron router-interface-add router-test2 subnet-test21

echo "5. Floating IPs."
neutron floatingip-create net04_ext
neutron floatingip-create net04_ext
neutron floatingip-create net04_ext
neutron floatingip-create net04_ext

floating_ip1_id=$(neutron floatingip-list | awk 'FNR == 4 {print}' | awk '{print $2}')
floating_ip2_id=$(neutron floatingip-list | awk 'FNR == 5 {print}' | awk '{print $2}')
floating_ip3_id=$(neutron floatingip-list | awk 'FNR == 6 {print}' | awk '{print $2}')
floating_ip4_id=$(neutron floatingip-list | awk 'FNR == 7 {print}' | awk '{print $2}')

floating_ip1=$(neutron floatingip-list | awk 'FNR == 4 {print}' | awk '{print $5}')
floating_ip2=$(neutron floatingip-list | awk 'FNR == 5 {print}' | awk '{print $5}')
floating_ip3=$(neutron floatingip-list | awk 'FNR == 6 {print}' | awk '{print $5}')
floating_ip4=$(neutron floatingip-list | awk 'FNR == 7 {print}' | awk '{print $5}')

#################################
echo "Creating NOVA stuff.."
#################################
net1_id=$(neutron net-list | grep net-test1 | awk '{print $2}')
net2_id=$(neutron net-list | grep net-test2 | awk '{print $2}')

nova boot --flavor 2 --image image_test1 --nic net-id=$net1_id nova-test11
nova boot --flavor 2 --image image_test1 --nic net-id=$net1_id nova-test12
nova boot --flavor 2 --image image_test2 --nic net-id=$net2_id nova-test21
nova boot --flavor 2 --image image_test2 --nic net-id=$net2_id nova-test22

vm1_id=$(nova list | grep nova-test11 | awk '{print $2}')
vm2_id=$(nova list | grep nova-test12 | awk '{print $2}')
vm3_id=$(nova list | grep nova-test21 | awk '{print $2}')
vm4_id=$(nova list | grep nova-test22 | awk '{print $2}')

nova floating-ip-associate $vm1_id $floating_ip1
nova floating-ip-associate $vm2_id $floating_ip2
nova floating-ip-associate $vm3_id $floating_ip3
nova floating-ip-associate $vm4_id $floating_ip4

#neutron floatingip-associate  --fixed-ip-address $floating_ip2 <PORT>
