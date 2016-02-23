.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for compass-os-odl_l2-nofeature-ha
========================================================

Running test case: vping_ssh
----------------------------

::
  FUNCTEST.info: Running vPing-SSH test...
  2016-02-10 22:41:11,118 - vPing_ssh- DEBUG - Creating image 'functest-vping' from '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img'...
  2016-02-10 22:41:11,947 - vPing_ssh- DEBUG - Image 'functest-vping' with ID=e900cadf-5723-426e-b269-df5aee4a8af3 created successfully.
  2016-02-10 22:41:12,053 - vPing_ssh- INFO - Creating neutron network vping-net...
  2016-02-10 22:41:12,551 - vPing_ssh- DEBUG - Network '91e17a47-73f4-4e27-bcc3-345ad77b4e95' created successfully
  2016-02-10 22:41:12,551 - vPing_ssh- DEBUG - Creating Subnet....
  2016-02-10 22:41:12,935 - vPing_ssh- DEBUG - Subnet '2ef1274b-31b7-4f19-8acc-be0e756ee9fd' created successfully
  2016-02-10 22:41:12,935 - vPing_ssh- DEBUG - Creating Router...
  2016-02-10 22:41:12,990 - vPing_ssh- DEBUG - Router '16002c8b-fd20-49d5-a36c-97c7f30c0578' created successfully
  2016-02-10 22:41:12,990 - vPing_ssh- DEBUG - Adding router to subnet...
  2016-02-10 22:41:13,262 - vPing_ssh- DEBUG - Interface added successfully.
  2016-02-10 22:41:13,262 - vPing_ssh- DEBUG - Adding gateway to router...
  2016-02-10 22:41:13,737 - vPing_ssh- DEBUG - Gateway added successfully.
  2016-02-10 22:41:13,912 - vPing_ssh- INFO - Flavor found 'm1.small'
  2016-02-10 22:41:14,703 - vPing_ssh- INFO - Creating security group  'vPing-sg'...
  2016-02-10 22:41:14,859 - vPing_ssh- DEBUG - Security group 'vPing-sg' with ID=78dd100f-bdf4-44bc-8794-cc5b22a42ef6 created successfully.
  2016-02-10 22:41:14,859 - vPing_ssh- DEBUG - Adding ICMP rules in security group 'vPing-sg'...
  2016-02-10 22:41:14,930 - vPing_ssh- DEBUG - Adding SSH rules in security group 'vPing-sg'...
  2016-02-10 22:41:15,089 - vPing_ssh- INFO - vPing Start Time:'2016-02-10 22:41:15'
  2016-02-10 22:41:15,089 - vPing_ssh- DEBUG - Creating port 'vping-port-1' with IP 192.168.130.30...
  2016-02-10 22:41:15,284 - vPing_ssh- INFO - Creating instance 'opnfv-vping-1' with IP 192.168.130.30...
  2016-02-10 22:41:15,284 - vPing_ssh- DEBUG - Configuration:
   name=opnfv-vping-1
   flavor=<Flavor: m1.small>
   image=e900cadf-5723-426e-b269-df5aee4a8af3
   network=91e17a47-73f4-4e27-bcc3-345ad77b4e95

  2016-02-10 22:41:16,649 - vPing_ssh- DEBUG - Status: BUILD
  2016-02-10 22:41:20,440 - vPing_ssh- DEBUG - Status: ACTIVE
  2016-02-10 22:41:20,440 - vPing_ssh- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  2016-02-10 22:41:20,440 - vPing_ssh- DEBUG - Instance 'opnfv-vping-1' got 192.168.130.30
  2016-02-10 22:41:20,440 - vPing_ssh- INFO - Adding 'opnfv-vping-1' to security group 'vPing-sg'...
  2016-02-10 22:41:20,834 - vPing_ssh- DEBUG - Creating port 'vping-port-2' with IP 192.168.130.40...
  2016-02-10 22:41:21,370 - vPing_ssh- INFO - Creating instance 'opnfv-vping-2' with IP 192.168.130.40...
  2016-02-10 22:41:21,371 - vPing_ssh- DEBUG - Configuration:
   name=opnfv-vping-2
   flavor=<Flavor: m1.small>
   image=e900cadf-5723-426e-b269-df5aee4a8af3
   network=91e17a47-73f4-4e27-bcc3-345ad77b4e95

  2016-02-10 22:41:22,575 - vPing_ssh- DEBUG - Status: BUILD
  2016-02-10 22:41:26,400 - vPing_ssh- DEBUG - Status: ACTIVE
  2016-02-10 22:41:26,400 - vPing_ssh- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  2016-02-10 22:41:26,400 - vPing_ssh- INFO - Adding 'opnfv-vping-2' to security group 'vPing-sg'...
  2016-02-10 22:41:27,208 - vPing_ssh- INFO - Creating floating IP for VM 'opnfv-vping-2'...
  2016-02-10 22:41:27,625 - vPing_ssh- INFO - Floating IP created: '192.168.10.101'
  2016-02-10 22:41:27,626 - vPing_ssh- INFO - Associating floating ip: '192.168.10.101' to VM 'opnfv-vping-2'
  2016-02-10 22:41:28,113 - vPing_ssh- INFO - Trying to establish SSH connection to 192.168.10.101...
  2016-02-10 22:41:30,115 - vPing_ssh- DEBUG - Waiting for 192.168.10.101...
  2016-02-10 22:41:36,254 - vPing_ssh- DEBUG - SSH connection established to 192.168.10.101.
  2016-02-10 22:41:37,330 - vPing_ssh- INFO - Waiting for ping...
  2016-02-10 22:41:38,340 - vPing_ssh- INFO - vPing detected!
  2016-02-10 22:41:38,340 - vPing_ssh- INFO - vPing duration:'23.3' s.
  2016-02-10 22:41:38,340 - vPing_ssh- INFO - Cleaning up...
  2016-02-10 22:41:38,341 - vPing_ssh- DEBUG - Deleting image...
  2016-02-10 22:41:38,933 - vPing_ssh- DEBUG - Deleting 'opnfv-vping-1'...
  2016-02-10 22:41:43,182 - vPing_ssh- DEBUG - Instance opnfv-vping-1 terminated.
  2016-02-10 22:41:43,987 - vPing_ssh- DEBUG - Deleting 'opnfv-vping-2'...
  2016-02-10 22:41:47,579 - vPing_ssh- DEBUG - Instance opnfv-vping-2 terminated.
  2016-02-10 22:41:47,579 - vPing_ssh- DEBUG - Deleting network 'vping-net'...
  2016-02-10 22:41:47,733 - vPing_ssh- DEBUG - Port 'ce5f4b77-b1db-4b71-9064-b6808d2c7276' removed successfully
  2016-02-10 22:41:47,981 - vPing_ssh- DEBUG - Port '2448f8c7-242e-48d2-944b-6472c61e6140' removed successfully
  2016-02-10 22:41:48,261 - vPing_ssh- DEBUG - Interface removed successfully
  2016-02-10 22:41:48,462 - vPing_ssh- DEBUG - Router deleted successfully
  2016-02-10 22:41:48,735 - vPing_ssh- DEBUG - Subnet 'vping-subnet' deleted successfully
  2016-02-10 22:41:48,933 - vPing_ssh- DEBUG - Network 'vping-net' deleted successfully
  2016-02-10 22:41:49,030 - vPing_ssh- DEBUG - Security group '78dd100f-bdf4-44bc-8794-cc5b22a42ef6' deleted successfully
  2016-02-10 22:41:49,030 - vPing_ssh- INFO - vPing OK
  2016-02-10 22:41:49,030 - vPing_ssh- DEBUG - Pushing result into DB...
  2016-02-10 22:41:49,711 - vPing_ssh- DEBUG - <Response [200]>
::

Running test case: vping_userdata
---------------------------------

::
  FUNCTEST.info: Running vPing-userdata test...
  2016-02-10 22:41:50,210 - vPing_userdata- DEBUG - Creating image 'functest-vping' from '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img'...
  2016-02-10 22:41:51,069 - vPing_userdata- INFO - Creating neutron network vping-net...
  2016-02-10 22:41:51,283 - vPing_userdata- DEBUG - Network '7162ccaa-ea23-4309-ba80-3e03715361bc' created successfully
  2016-02-10 22:41:51,283 - vPing_userdata- DEBUG - Creating Subnet....
  2016-02-10 22:41:51,414 - vPing_userdata- DEBUG - Subnet '6cbdc816-707c-4e14-9766-76a557ef1ee1' created successfully
  2016-02-10 22:41:51,414 - vPing_userdata- DEBUG - Creating Router...
  2016-02-10 22:41:51,457 - vPing_userdata- DEBUG - Router 'bd344d4b-e382-4368-a7a4-8d14f8e1b280' created successfully
  2016-02-10 22:41:51,457 - vPing_userdata- DEBUG - Adding router to subnet...
  2016-02-10 22:41:51,680 - vPing_userdata- DEBUG - Interface added successfully.
  2016-02-10 22:41:51,969 - vPing_userdata- INFO - Flavor found 'm1.small'
  2016-02-10 22:41:52,020 - vPing_userdata- INFO - vPing Start Time:'2016-02-10 22:41:52'
  2016-02-10 22:41:52,020 - vPing_userdata- DEBUG - Creating port 'vping-port-1' with IP 192.168.130.30...
  2016-02-10 22:41:52,278 - vPing_userdata- INFO - Creating instance 'opnfv-vping-1' with IP 192.168.130.30...
  2016-02-10 22:41:52,278 - vPing_userdata- DEBUG - Configuration:
   name=opnfv-vping-1
   flavor=<Flavor: m1.small>
   image=5bea5f62-77dc-4abe-b538-8770356f678e
   network=7162ccaa-ea23-4309-ba80-3e03715361bc

  2016-02-10 22:41:53,720 - vPing_userdata- DEBUG - Status: BUILD
  2016-02-10 22:41:56,836 - vPing_userdata- DEBUG - Status: ACTIVE
  2016-02-10 22:41:56,836 - vPing_userdata- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  2016-02-10 22:41:56,836 - vPing_userdata- DEBUG - Instance 'opnfv-vping-1' got 192.168.130.30
  2016-02-10 22:41:56,837 - vPing_userdata- DEBUG - Creating port 'vping-port-2' with IP 192.168.130.40...
  2016-02-10 22:41:57,048 - vPing_userdata- INFO - Creating instance 'opnfv-vping-2' with IP 192.168.130.40...
  2016-02-10 22:41:57,049 - vPing_userdata- DEBUG - Configuration:
   name=opnfv-vping-2
   flavor=<Flavor: m1.small>
   image=5bea5f62-77dc-4abe-b538-8770356f678e
   network=7162ccaa-ea23-4309-ba80-3e03715361bc
   userdata=
  #!/bin/sh

  while true; do
   ping -c 1 192.168.130.30 2>&1 >/dev/null
   RES=$?
   if [ "Z$RES" = "Z0" ] ; then
    echo 'vPing OK'
   break
   else
    echo 'vPing KO'
   fi
   sleep 1
  done

  2016-02-10 22:41:58,941 - vPing_userdata- DEBUG - Status: BUILD
  2016-02-10 22:42:02,084 - vPing_userdata- DEBUG - Status: ACTIVE
  2016-02-10 22:42:02,084 - vPing_userdata- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  2016-02-10 22:42:02,084 - vPing_userdata- INFO - Waiting for ping...
  2016-02-10 22:42:03,473 - vPing_userdata- DEBUG - Pinging 192.168.130.40. Waiting for response...
  2016-02-10 22:42:06,431 - vPing_userdata- INFO - vPing detected!
  2016-02-10 22:42:06,431 - vPing_userdata- INFO - vPing duration:'14.4'
  2016-02-10 22:42:06,431 - vPing_userdata- INFO - vPing OK
  2016-02-10 22:42:06,431 - vPing_userdata- INFO - Cleaning up...
  2016-02-10 22:42:06,431 - vPing_userdata- DEBUG - Deleting image...
  2016-02-10 22:42:06,911 - vPing_userdata- DEBUG - Deleting 'opnfv-vping-1'...
  2016-02-10 22:42:10,262 - vPing_userdata- DEBUG - Instance opnfv-vping-1 terminated.
  2016-02-10 22:42:11,054 - vPing_userdata- DEBUG - Deleting 'opnfv-vping-2'...
  2016-02-10 22:42:15,311 - vPing_userdata- DEBUG - Instance opnfv-vping-2 terminated.
  2016-02-10 22:42:15,311 - vPing_userdata- INFO - Deleting network 'vping-net'...
  2016-02-10 22:42:15,457 - vPing_userdata- DEBUG - Port 'ddc5ecfa-6678-432e-aad0-51d1c1c94dfd' removed successfully
  2016-02-10 22:42:15,611 - vPing_userdata- DEBUG - Port '0ebb366d-2e52-4dc6-9c3f-34d0c8c01a00' removed successfully
  2016-02-10 22:42:15,817 - vPing_userdata- DEBUG - Interface removed successfully
  2016-02-10 22:42:16,011 - vPing_userdata- DEBUG - Router deleted successfully
  2016-02-10 22:42:16,222 - vPing_userdata- DEBUG - Subnet 'vping-subnet' deleted successfully
  2016-02-10 22:42:16,443 - vPing_userdata- DEBUG - Network 'vping-net' deleted successfully
  2016-02-10 22:42:16,443 - vPing_userdata- DEBUG - Pushing result into DB...
  2016-02-10 22:42:17,319 - vPing_userdata- DEBUG - <Response [200]>
::

Running test case: tempest
--------------------------
::
  FUNCTEST.info: Running Tempest tests...
  2016-02-10 22:42:17,647 - run_tempest - INFO - Creating tenant and user for Tempest suite
  2016-02-10 22:42:17,798 - run_tempest - DEBUG - Generating tempest.conf file...
  2016-02-10 22:42:17,798 - run_tempest - DEBUG - Executing command : rally verify genconfig
  2016-02-10 22:42:24,250 - run_tempest - DEBUG - 2016-02-10 22:42:18.326 23844 INFO rally.verification.tempest.tempest [-] Tempest is not configured.
  2016-02-10 22:42:18.326 23844 INFO rally.verification.tempest.tempest [-] Starting: Creating configuration file for Tempest.
  2016-02-10 22:42:24.194 23844 INFO rally.verification.tempest.tempest [-] Completed: Creating configuration file for Tempest.

  2016-02-10 22:42:24,250 - run_tempest - DEBUG - Resolving deployment UUID...
  2016-02-10 22:42:24,825 - run_tempest - DEBUG - Finding tempest.conf file...
  2016-02-10 22:42:24,826 - run_tempest - DEBUG -   Updating fixed_network_name...
  2016-02-10 22:42:25,075 - run_tempest - DEBUG - Executing command : crudini --set /home/opnfv/.rally/tempest/for-deployment-e76f88e3-5f6d-4757-8755-8dd8a09c6870/tempest.conf compute fixed_network_name functest-net
  2016-02-10 22:42:25,115 - run_tempest - DEBUG -   Updating non-admin credentials...
  2016-02-10 22:42:25,115 - run_tempest - DEBUG - Executing command : crudini --set /home/opnfv/.rally/tempest/for-deployment-e76f88e3-5f6d-4757-8755-8dd8a09c6870/tempest.conf identity tenant_name tempest
  2016-02-10 22:42:25,142 - run_tempest - DEBUG - Executing command : crudini --set /home/opnfv/.rally/tempest/for-deployment-e76f88e3-5f6d-4757-8755-8dd8a09c6870/tempest.conf identity username tempest
  2016-02-10 22:42:25,168 - run_tempest - DEBUG - Executing command : crudini --set /home/opnfv/.rally/tempest/for-deployment-e76f88e3-5f6d-4757-8755-8dd8a09c6870/tempest.conf identity password tempest
  2016-02-10 22:42:25,195 - run_tempest - DEBUG - Executing command : sed -i 's/.*ssh_user_regex.*/ssh_user_regex = [["^.*[Cc]irros.*$", "cirros"], ["^.*[Tt]est[VvMm].*$", "cirros"], ["^.*rally_verify.*$", "cirros"]]/' /home/opnfv/.rally/tempest/for-deployment-e76f88e3-5f6d-4757-8755-8dd8a09c6870/tempest.conf
  2016-02-10 22:42:25,199 - run_tempest - INFO - Starting Tempest test suite: '--tests-file /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/custom_tests/test_list.txt'.
  2016-02-10 22:42:25,199 - run_tempest - DEBUG - Executing command : rally verify start --tests-file /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/custom_tests/test_list.txt
  Total results of verification:

  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | UUID                                 | Deployment UUID                      | Set name | Tests | Failures | Created at                 | Status   |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | b11691a3-df31-4681-8493-e8e723d76da2 | e76f88e3-5f6d-4757-8755-8dd8a09c6870 |          | 210   | 0        | 2016-02-10 22:42:25.742171 | finished |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+

  Tests:

  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | name                                                                                                                                     | time      | status  |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.14508   | success |
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.20886   | success |
  | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 8.74633   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 10.96331  | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 6.91667   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.06609   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.05652   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.05475   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.11525   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.06320   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.06529   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.07598   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.07994   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.05164   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.17071   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.07382   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.12124   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.07097   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 0.35923   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 0.05248   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 1.12419   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 0.44629   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 0.81959   | success |
  | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 2.61632   | success |
  | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 6.64787   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 60.19994  | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.06927   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.17946   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 0.20048   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.00062   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 69.94540  | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.05355   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.15865   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 0.42541   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.00108   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.06548   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 4.28395   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.23946   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.19532   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.15850   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.30121   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.15893   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.08980   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.06970   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.07757   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.10192   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.11599   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.30575   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00066   | skip    |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.17553   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.06515   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.01091   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.06001   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.07683   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.01042   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.01260   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.04293   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.07701   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.07658   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.17401   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.01225   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.06247   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.00063   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 6.81169   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 8.35726   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 9.24775   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.34307   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 17.09147  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 13.46313  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 17.64490  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 6.85623   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.08484   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.16624   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.67482   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.34319   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.49805   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.69403   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.70458   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.57632   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 2.37325   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 12.72787  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 14.59892  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 8.81944   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 7.57375   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 0.68768   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 1.03345   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 0.69325   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 1.61747   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 0.74262   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 1.62312   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 0.63504   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 0.44757   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 0.44857   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.41970   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 1.59286   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 0.41213   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 0.53150   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 0.47482   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.32116   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 0.74411   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.37262   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 0.39655   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 0.56090   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 0.54267   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 0.32880   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.21189   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.00958   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 0.06951   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.01997   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 0.49170   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.23047   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.14871   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.05185   | success |
  | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 40.10260  | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.10161   | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.73083   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.13569   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.01176   | success |
  | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.17854   | success |
  | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.09300   | success |
  | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.14146   | success |
  | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.03207   | success |
  | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 0.36702   | success |
  | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.15345   | success |
  | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 0.90773   | success |
  | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.11017   | success |
  | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.09102   | success |
  | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.14059   | success |
  | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.20332   | success |
  | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 0.78806   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.04671   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.03335   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.02244   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.02764   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.01660   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.04047   | success |
  | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.05473   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 0.45763   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 0.29059   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 0.43753   | success |
  | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 0.58785   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 2.37173   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 1.16911   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 0.68115   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 1.12936   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 3.57963   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 0.78922   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 1.65769   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 1.83194   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 1.68524   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.11621   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.04856   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.06497   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.04008   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.03337   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 1.32422   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.26639   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.03927   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.05712   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.02959   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.03932   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 1.19901   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 1.25554   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 0.92929   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.08330   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.05240   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 1.45070   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 1.52472   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 0.77372   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.07141   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.07359   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 3.13508   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 1.71626   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 1.62675   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 1.30657   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 3.14422   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 2.10530   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 1.26380   | success |
  | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 0.96604   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 0.42206   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 0.53726   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.02176   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 0.62941   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 0.73604   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.08043   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.52518   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 6.69041   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.02086   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 0.59957   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.42389   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.35662   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.31285   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.41824   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.44749   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 2.48091   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.02451   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 11.01904  | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 1.56618   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 2.39593   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 2.90553   | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 10.69341  | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 10.81400  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 9.37884   | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 11.22059  | success |
  | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.12832   | success |
  | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.10186   | success |
  | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 27.37465  | success |
  | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 13.36483  | success |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 79.30317  | success |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 101.24914 | success |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  2016-02-10 22:45:16,505 - run_tempest - DEBUG - Executing command : rally verify list
  2016-02-10 22:45:17,075 - run_tempest - INFO - Results: {'timestart': '2016-02-1022:42:25.742171', 'duration': 170, 'tests': 210, 'failures': 0}
  2016-02-10 22:45:17,076 - run_tempest - DEBUG - Push result into DB
  2016-02-10 22:45:17,076 - run_tempest - INFO - Pushing results to DB: 'http://testresults.opnfv.org/testapi/results'.
  2016-02-10 22:45:17,875 - run_tempest - DEBUG - <Response [200]>
  2016-02-10 22:45:17,875 - run_tempest - INFO - Deleting tenant and user for Tempest suite)
::

Running test case: odl
----------------------

::
  FUNCTEST.info: Running ODL test...
  [0;32mCurrent environment parameters for ODL suite.[0m
  + ODL_IP=192.168.10.51
  + ODL_PORT=8181
  + USR_NAME=admin
  + PASS=console
  + NEUTRON_IP=192.168.10.51
  + KEYSTONE_IP=192.168.10.51
  + set +x
  '/home/opnfv/repos/functest/testcases/Controllers/ODL/CI/custom_tests/neutron/010__networks.robot' -> '/home/opnfv/repos/odl_integration/test/csit/suites/openstack/neutron/010__networks.robot'
  '/home/opnfv/repos/functest/testcases/Controllers/ODL/CI/custom_tests/neutron/020__subnets.robot' -> '/home/opnfv/repos/odl_integration/test/csit/suites/openstack/neutron/020__subnets.robot'
  '/home/opnfv/repos/functest/testcases/Controllers/ODL/CI/custom_tests/neutron/030__ports.robot' -> '/home/opnfv/repos/odl_integration/test/csit/suites/openstack/neutron/030__ports.robot'
  '/home/opnfv/repos/functest/testcases/Controllers/ODL/CI/custom_tests/neutron/040__delete_ports.txt' -> '/home/opnfv/repos/odl_integration/test/csit/suites/openstack/neutron/040__delete_ports.txt'
  '/home/opnfv/repos/functest/testcases/Controllers/ODL/CI/custom_tests/neutron/050__delete_subnets.txt' -> '/home/opnfv/repos/odl_integration/test/csit/suites/openstack/neutron/050__delete_subnets.txt'
  '/home/opnfv/repos/functest/testcases/Controllers/ODL/CI/custom_tests/neutron/060__delete_networks.txt' -> '/home/opnfv/repos/odl_integration/test/csit/suites/openstack/neutron/060__delete_networks.txt'
  ==============================================================================
  Basic
  ==============================================================================
  Basic.010 Restconf OK :: Test suite to verify Restconf is OK
  ==============================================================================
  Get Controller Modules :: Get the controller modules via Restconf     | PASS |
  ------------------------------------------------------------------------------
  Basic.010 Restconf OK :: Test suite to verify Restconf is OK          | PASS |
  1 critical test, 1 passed, 0 failed
  1 test total, 1 passed, 0 failed
  ==============================================================================
  Basic                                                                 | PASS |
  1 critical test, 1 passed, 0 failed
  1 test total, 1 passed, 0 failed
  ==============================================================================
  Output:  /home/opnfv/repos/functest/output.xml
  Log:     /home/opnfv/repos/functest/log.html
  Report:  /home/opnfv/repos/functest/report.html
  ==============================================================================
  Neutron :: Test suite for Neutron Plugin
  ==============================================================================
  Neutron.Networks :: Checking Network created in OpenStack are pushed to Ope...
  ==============================================================================
  Check OpenStack Networks :: Checking OpenStack Neutron for known n... | PASS |
  ------------------------------------------------------------------------------
  Check OpenDaylight Networks :: Checking OpenDaylight Neutron API f... | PASS |
  ------------------------------------------------------------------------------
  Create Network :: Create new network in OpenStack                     | PASS |
  ------------------------------------------------------------------------------
  Check Network :: Check Network created in OpenDaylight                | PASS |
  ------------------------------------------------------------------------------
  Neutron.Networks :: Checking Network created in OpenStack are push... | PASS |
  4 critical tests, 4 passed, 0 failed
  4 tests total, 4 passed, 0 failed
  ==============================================================================
  Neutron.Subnets :: Checking Subnets created in OpenStack are pushed to Open...
  ==============================================================================
  Check OpenStack Subnets :: Checking OpenStack Neutron for known Su... | PASS |
  ------------------------------------------------------------------------------
  Check OpenDaylight subnets :: Checking OpenDaylight Neutron API fo... | PASS |
  ------------------------------------------------------------------------------
  Create New subnet :: Create new subnet in OpenStack                   | PASS |
  ------------------------------------------------------------------------------
  Check New subnet :: Check new subnet created in OpenDaylight          | PASS |
  ------------------------------------------------------------------------------
  Neutron.Subnets :: Checking Subnets created in OpenStack are pushe... | PASS |
  4 critical tests, 4 passed, 0 failed
  4 tests total, 4 passed, 0 failed
  ==============================================================================
  Neutron.Ports :: Checking Port created in OpenStack are pushed to OpenDaylight
  ==============================================================================
  Check OpenStack ports :: Checking OpenStack Neutron for known ports   | PASS |
  ------------------------------------------------------------------------------
  Check OpenDaylight ports :: Checking OpenDaylight Neutron API for ... | PASS |
  ------------------------------------------------------------------------------
  Create New Port :: Create new port in OpenStack                       | PASS |
  ------------------------------------------------------------------------------
  Check New Port :: Check new subnet created in OpenDaylight            | PASS |
  ------------------------------------------------------------------------------
  Neutron.Ports :: Checking Port created in OpenStack are pushed to ... | PASS |
  4 critical tests, 4 passed, 0 failed
  4 tests total, 4 passed, 0 failed
  ==============================================================================
  Neutron.Delete Ports :: Checking Port deleted in OpenStack are deleted also...
  ==============================================================================
  Delete New Port :: Delete previously created port in OpenStack        | PASS |
  ------------------------------------------------------------------------------
  Check Port Deleted :: Check port deleted in OpenDaylight              | PASS |
  ------------------------------------------------------------------------------
  Neutron.Delete Ports :: Checking Port deleted in OpenStack are del... | PASS |
  2 critical tests, 2 passed, 0 failed
  2 tests total, 2 passed, 0 failed
  ==============================================================================
  Neutron.Delete Subnets :: Checking Subnets deleted in OpenStack are deleted...
  ==============================================================================
  Delete New subnet :: Delete previously created subnet in OpenStack    | PASS |
  ------------------------------------------------------------------------------
  Check New subnet deleted :: Check subnet deleted in OpenDaylight      | PASS |
  ------------------------------------------------------------------------------
  Neutron.Delete Subnets :: Checking Subnets deleted in OpenStack ar... | PASS |
  2 critical tests, 2 passed, 0 failed
  2 tests total, 2 passed, 0 failed
  ==============================================================================
  Neutron.Delete Networks :: Checking Network deleted in OpenStack are delete...
  ==============================================================================
  Delete Network :: Delete network in OpenStack                         | PASS |
  ------------------------------------------------------------------------------
  Check Network deleted :: Check Network deleted in OpenDaylight        | PASS |
  ------------------------------------------------------------------------------
  Neutron.Delete Networks :: Checking Network deleted in OpenStack a... | PASS |
  2 critical tests, 2 passed, 0 failed
  2 tests total, 2 passed, 0 failed
  ==============================================================================
  Neutron :: Test suite for Neutron Plugin                              | PASS |
  18 critical tests, 18 passed, 0 failed
  18 tests total, 18 passed, 0 failed
  ==============================================================================
  Output:  /home/opnfv/repos/functest/output.xml
  Log:     /home/opnfv/repos/functest/log.html
  Report:  /home/opnfv/repos/functest/report.html
  Log:     /home/opnfv/repos/functest/log.html
  Report:  /home/opnfv/repos/functest/report.html
::

Running test case: vims
-----------------------

::
  FUNCTEST.info: Running vIMS test...
  2016-02-10 22:45:37,147 - vIMS - INFO - Prepare OpenStack plateform (create tenant and user)
  2016-02-10 22:45:37,406 - vIMS - INFO - Update OpenStack creds informations
  2016-02-10 22:45:37,406 - vIMS - INFO - Upload some OS images if it doesn't exist
  2016-02-10 22:45:37,529 - vIMS - INFO - centos_7 image doesn't exist on glance repository.
                              Try downloading this image and upload on glance !
  2016-02-10 22:48:29,605 - vIMS - INFO - ubuntu_14.04 image doesn't exist on glance repository.
                              Try downloading this image and upload on glance !
  2016-02-10 22:49:31,380 - vIMS - INFO - Update security group quota for this tenant
  2016-02-10 22:49:31,609 - vIMS - INFO - Update cinder quota for this tenant
  2016-02-10 22:49:32,080 - vIMS - INFO - Collect flavor id for cloudify manager server
  2016-02-10 22:49:32,529 - vIMS - INFO - Prepare virtualenv for cloudify-cli
  2016-02-10 22:50:07,340 - vIMS - INFO - Downloading the cloudify manager server blueprint
  2016-02-10 22:50:12,979 - vIMS - INFO - Cloudify deployment Start Time:'2016-02-10 22:50:12'
  2016-02-10 22:50:12,979 - vIMS - INFO - Writing the inputs file
  2016-02-10 22:50:12,981 - vIMS - INFO - Launching the cloudify-manager deployment
  2016-02-10 22:59:18,207 - vIMS - INFO - Cloudify-manager server is UP !
  2016-02-10 22:59:18,207 - vIMS - INFO - Cloudify deployment duration:'545.2'
  2016-02-10 22:59:18,208 - vIMS - INFO - Collect flavor id for all clearwater vm
  2016-02-10 22:59:18,674 - vIMS - INFO - vIMS VNF deployment Start Time:'2016-02-10 22:59:18'
  2016-02-10 22:59:18,674 - vIMS - INFO - Downloading the openstack-blueprint.yaml blueprint
  2016-02-10 22:59:23,285 - vIMS - INFO - Writing the inputs file
  2016-02-10 22:59:23,287 - vIMS - INFO - Launching the clearwater deployment
  2016-02-10 23:10:25,235 - vIMS - INFO - The deployment of clearwater-opnfv is ended
  2016-02-10 23:10:25,235 - vIMS - INFO - vIMS VNF deployment duration:'666.6'
  2016-02-10 23:13:32,648 - vIMS - INFO - vIMS functional test Start Time:'2016-02-10 23:13:32'
  2016-02-10 23:13:35,583 - vIMS - INFO - vIMS functional test duration:'2.9'
  2016-02-10 23:13:36,745 - vIMS - INFO - Launching the clearwater-opnfv undeployment
  2016-02-10 23:17:11,897 - vIMS - ERROR - Error when executing command /bin/bash -c 'source /home/opnfv/functest/data/vIMS/venv_cloudify/bin/activate; cd /home/opnfv/functest/data/vIMS/; cfy executions start -w uninstall -d clearwater-opnfv --timeout 1800 ; cfy deployments delete -d clearwater-opnfv; '
  2016-02-10 23:17:11,898 - vIMS - INFO - Launching the cloudify-manager undeployment
  2016-02-10 23:17:59,430 - vIMS - INFO - Cloudify-manager server has been successfully removed!
  2016-02-10 23:17:59,499 - vIMS - INFO - Removing vIMS tenant ..
  2016-02-10 23:18:00,350 - vIMS - INFO - Removing vIMS user ..
::

Running test case: rally
------------------------

::
  FUNCTEST.info: Running Rally benchmark suite...
  2016-02-10 23:18:03,367 - run_rally - DEBUG - Volume type 'volume_test' created succesfully...
  2016-02-10 23:18:03,490 - run_rally - DEBUG - Creating image 'functest-img' from '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img'...
  2016-02-10 23:18:04,074 - run_rally - DEBUG - Image 'functest-img' with ID 'a4efc793-1195-482b-9da6-87299b33d650' created succesfully .
  2016-02-10 23:18:04,074 - run_rally - INFO - Starting test scenario "authenticate" ...
  2016-02-10 23:18:04,075 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-authenticate.yaml
  2016-02-10 23:18:04,257 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '5333b06c-91ae-407b-8a20-a5c0adff52ee', 'service_list': ['authenticate'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}"
  2016-02-10 23:18:31,567 - run_rally - INFO -
   Preparing input task
   Task  70024948-2531-471d-9c30-9fdc69d0e1e4: started
  Task 70024948-2531-471d-9c30-9fdc69d0e1e4: finished

  test scenario Authenticate.validate_glance
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_glance     | 0.116 | 0.148  | 0.228  | 0.254  | 0.279 | 0.168 | 100.0%  | 10    |
  | authenticate.validate_glance (2) | 0.035 | 0.041  | 0.06   | 0.075  | 0.09  | 0.047 | 100.0%  | 10    |
  | total                            | 0.219 | 0.297  | 0.353  | 0.376  | 0.399 | 0.292 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.857667922974
  Full duration: 3.24089407921

  test scenario Authenticate.keystone
  +-----------------------------------------------------------------------------+
  |                            Response Times (sec)                             |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | total  | 0.064 | 0.074  | 0.084  | 0.11   | 0.135 | 0.079 | 100.0%  | 10    |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.234832048416
  Full duration: 2.53488898277

  test scenario Authenticate.validate_heat
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_heat     | 0.123 | 0.162  | 0.298  | 0.343  | 0.387 | 0.194 | 100.0%  | 10    |
  | authenticate.validate_heat (2) | 0.025 | 0.077  | 0.111  | 0.13   | 0.148 | 0.071 | 100.0%  | 10    |
  | total                          | 0.217 | 0.316  | 0.482  | 0.495  | 0.508 | 0.344 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.990710020065
  Full duration: 3.20668816566

  test scenario Authenticate.validate_nova
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_nova     | 0.11  | 0.129  | 0.156  | 0.16   | 0.163 | 0.132 | 100.0%  | 10    |
  | authenticate.validate_nova (2) | 0.024 | 0.032  | 0.041  | 0.041  | 0.041 | 0.032 | 100.0%  | 10    |
  | total                          | 0.212 | 0.233  | 0.268  | 0.273  | 0.278 | 0.238 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.725275993347
  Full duration: 2.92799592018

  test scenario Authenticate.validate_cinder
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_cinder     | 0.094 | 0.107  | 0.115  | 0.116  | 0.117 | 0.107 | 100.0%  | 10    |
  | authenticate.validate_cinder (2) | 0.06  | 0.072  | 0.082  | 0.091  | 0.099 | 0.073 | 100.0%  | 10    |
  | total                            | 0.223 | 0.254  | 0.293  | 0.302  | 0.311 | 0.261 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.787709951401
  Full duration: 3.0150449276

  test scenario Authenticate.validate_neutron
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_neutron     | 0.105 | 0.126  | 0.162  | 0.168  | 0.173 | 0.132 | 100.0%  | 10    |
  | authenticate.validate_neutron (2) | 0.071 | 0.087  | 0.109  | 0.117  | 0.124 | 0.091 | 100.0%  | 10    |
  | total                             | 0.255 | 0.304  | 0.327  | 0.327  | 0.327 | 0.297 | 100.0%  | 10    |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.891720056534
  Full duration: 2.96198296547

  2016-02-10 23:18:31,567 - run_rally - DEBUG - task_id : 70024948-2531-471d-9c30-9fdc69d0e1e4
  2016-02-10 23:18:31,567 - run_rally - DEBUG - running command line : rally task report 70024948-2531-471d-9c30-9fdc69d0e1e4 --out /home/opnfv/functest/results/rally/opnfv-authenticate.html
  2016-02-10 23:18:32,178 - run_rally - DEBUG - running command line : rally task results 70024948-2531-471d-9c30-9fdc69d0e1e4
  2016-02-10 23:18:32,759 - run_rally - DEBUG - saving json file
  2016-02-10 23:18:32,761 - run_rally - DEBUG - Push result into DB
  2016-02-10 23:18:38,906 - run_rally - DEBUG - <Response [200]>
  2016-02-10 23:18:38,907 - run_rally - INFO - Test scenario: "authenticate" OK.

  2016-02-10 23:18:38,907 - run_rally - INFO - Starting test scenario "glance" ...
  2016-02-10 23:18:38,907 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-glance.yaml
  2016-02-10 23:18:39,085 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '5333b06c-91ae-407b-8a20-a5c0adff52ee', 'service_list': ['glance'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}"
  2016-02-10 23:20:14,436 - run_rally - INFO -
   Preparing input task
   Task  ea3d6cbe-0d37-4f26-8030-7096d3db372f: started
  Task ea3d6cbe-0d37-4f26-8030-7096d3db372f: finished

  test scenario GlanceImages.list_images
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.list_images | 0.188 | 0.24   | 0.276  | 0.284  | 0.292 | 0.238 | 100.0%  | 10    |
  | total              | 0.188 | 0.24   | 0.276  | 0.284  | 0.292 | 0.238 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.762142896652
  Full duration: 3.6355650425

  test scenario GlanceImages.create_image_and_boot_instances
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | glance.create_image | 2.794 | 3.209  | 3.48   | 3.489  | 3.497  | 3.171  | 100.0%  | 10    |
  | nova.boot_servers   | 6.0   | 8.224  | 9.515  | 9.569  | 9.623  | 8.214  | 100.0%  | 10    |
  | total               | 8.795 | 11.646 | 12.43  | 12.637 | 12.843 | 11.385 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 32.6185789108
  Full duration: 56.808437109

  test scenario GlanceImages.create_and_list_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 3.004 | 3.141  | 3.359  | 3.379  | 3.399 | 3.183 | 100.0%  | 10    |
  | glance.list_images  | 0.039 | 0.045  | 0.052  | 0.052  | 0.053 | 0.046 | 100.0%  | 10    |
  | total               | 3.044 | 3.186  | 3.409  | 3.426  | 3.443 | 3.229 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.54856610298
  Full duration: 14.0860719681

  test scenario GlanceImages.create_and_delete_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 2.785 | 3.041  | 3.554  | 3.569  | 3.584 | 3.099 | 100.0%  | 10    |
  | glance.delete_image | 0.135 | 0.154  | 0.322  | 0.33   | 0.338 | 0.193 | 100.0%  | 10    |
  | total               | 2.921 | 3.202  | 3.718  | 3.72   | 3.722 | 3.292 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.6310031414
  Full duration: 12.5532770157

  2016-02-10 23:20:14,436 - run_rally - DEBUG - task_id : ea3d6cbe-0d37-4f26-8030-7096d3db372f
  2016-02-10 23:20:14,436 - run_rally - DEBUG - running command line : rally task report ea3d6cbe-0d37-4f26-8030-7096d3db372f --out /home/opnfv/functest/results/rally/opnfv-glance.html
  2016-02-10 23:20:15,028 - run_rally - DEBUG - running command line : rally task results ea3d6cbe-0d37-4f26-8030-7096d3db372f
  2016-02-10 23:20:15,597 - run_rally - DEBUG - saving json file
  2016-02-10 23:20:15,598 - run_rally - DEBUG - Push result into DB
  2016-02-10 23:20:21,300 - run_rally - DEBUG - <Response [200]>
  2016-02-10 23:20:21,301 - run_rally - INFO - Test scenario: "glance" OK.

  2016-02-10 23:20:21,301 - run_rally - INFO - Starting test scenario "cinder" ...
  2016-02-10 23:20:21,301 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-cinder.yaml
  2016-02-10 23:20:21,503 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '5333b06c-91ae-407b-8a20-a5c0adff52ee', 'service_list': ['cinder'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}"
  2016-02-10 23:36:46,743 - run_rally - INFO -
   Preparing input task
   Task  c4bf15f0-eb49-4723-9aa9-81d6ea24dc2f: started
  Task c4bf15f0-eb49-4723-9aa9-81d6ea24dc2f: finished

  test scenario CinderVolumes.create_and_attach_volume
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
  +----------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | nova.boot_server     | 3.178  | 4.424  | 5.766  | 5.877  | 5.988  | 4.733 | 100.0%  | 10    |
  | cinder.create_volume | 2.542  | 2.787  | 2.835  | 2.848  | 2.861  | 2.767 | 100.0%  | 10    |
  | nova.attach_volume   | 5.467  | 7.793  | 8.194  | 9.28   | 10.367 | 7.799 | 100.0%  | 10    |
  | nova.detach_volume   | 3.029  | 4.298  | 5.62   | 5.643  | 5.665  | 4.322 | 100.0%  | 10    |
  | cinder.delete_volume | 2.392  | 2.493  | 2.58   | 2.583  | 2.586  | 2.498 | 100.0%  | 10    |
  | nova.delete_server   | 2.388  | 2.444  | 2.56   | 2.6    | 2.639  | 2.47  | 100.0%  | 10    |
  | total                | 20.696 | 23.97  | 27.209 | 28.172 | 29.135 | 24.59 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 72.9981839657
  Full duration: 85.4548120499

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 5.187 | 5.33   | 5.429  | 5.456  | 5.483 | 5.334 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.059 | 0.112  | 0.177  | 0.185  | 0.194 | 0.118 | 100.0%  | 10    |
  | total                | 5.341 | 5.465  | 5.527  | 5.557  | 5.587 | 5.452 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.3163900375
  Full duration: 28.575948

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.838 | 2.956  | 3.08   | 3.084  | 3.087 | 2.969 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.053 | 0.114  | 0.138  | 0.143  | 0.147 | 0.112 | 100.0%  | 10    |
  | total                | 2.986 | 3.065  | 3.185  | 3.195  | 3.204 | 3.081 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.18667793274
  Full duration: 20.0336208344

  test scenario CinderVolumes.create_and_list_snapshots
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.442 | 2.523  | 2.591  | 2.618  | 2.645 | 2.524 | 100.0%  | 10    |
  | cinder.list_snapshots  | 0.016 | 0.083  | 0.108  | 0.124  | 0.14  | 0.085 | 100.0%  | 10    |
  | total                  | 2.524 | 2.612  | 2.668  | 2.679  | 2.69  | 2.609 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 7.86018610001
  Full duration: 30.7561271191

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.759 | 2.905  | 3.103  | 3.117  | 3.131 | 2.942 | 100.0%  | 10    |
  | cinder.delete_volume | 2.41  | 2.503  | 2.632  | 2.653  | 2.675 | 2.522 | 100.0%  | 10    |
  | total                | 5.203 | 5.482  | 5.651  | 5.689  | 5.727 | 5.464 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.1656489372
  Full duration: 22.7390818596

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 3.117 | 5.408  | 5.501  | 5.525  | 5.55  | 4.983 | 100.0%  | 10    |
  | cinder.delete_volume | 2.409 | 2.505  | 2.582  | 2.597  | 2.611 | 2.509 | 100.0%  | 10    |
  | total                | 5.606 | 7.887  | 8.077  | 8.079  | 8.081 | 7.493 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 21.5610911846
  Full duration: 28.1375927925

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.814 | 2.926  | 3.051  | 3.073  | 3.095 | 2.928 | 100.0%  | 10    |
  | cinder.delete_volume | 2.41  | 2.549  | 2.65   | 2.673  | 2.697 | 2.549 | 100.0%  | 10    |
  | total                | 5.352 | 5.455  | 5.622  | 5.663  | 5.704 | 5.477 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.3862950802
  Full duration: 22.6357138157

  test scenario CinderVolumes.create_and_upload_volume_to_image
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume          | 2.833  | 2.963  | 3.129  | 3.234  | 3.338  | 3.004  | 100.0%  | 10    |
  | cinder.upload_volume_to_image | 25.735 | 58.927 | 69.934 | 72.964 | 75.993 | 54.211 | 100.0%  | 10    |
  | cinder.delete_volume          | 2.334  | 2.516  | 2.645  | 2.672  | 2.699  | 2.509  | 100.0%  | 10    |
  | nova.delete_image             | 0.372  | 0.524  | 1.216  | 3.884  | 6.553  | 1.093  | 100.0%  | 10    |
  | total                         | 31.617 | 64.977 | 75.831 | 78.899 | 81.966 | 60.818 | 100.0%  | 10    |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 160.993555069
  Full duration: 168.269435883

  test scenario CinderVolumes.create_and_delete_snapshot
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.442 | 2.556  | 2.583  | 2.604  | 2.626 | 2.537 | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.27  | 2.415  | 2.466  | 2.505  | 2.543 | 2.398 | 100.0%  | 10    |
  | total                  | 4.819 | 4.941  | 5.014  | 5.018  | 5.023 | 4.935 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.7615189552
  Full duration: 34.2201139927

  test scenario CinderVolumes.create_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.817 | 2.994  | 3.104  | 3.11   | 3.117 | 3.002 | 100.0%  | 10    |
  | total                | 2.817 | 2.994  | 3.104  | 3.11   | 3.117 | 3.002 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.08546304703
  Full duration: 18.2949140072

  test scenario CinderVolumes.create_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.832 | 2.912  | 2.992  | 3.008  | 3.024 | 2.923 | 100.0%  | 10    |
  | total                | 2.832 | 2.912  | 2.992  | 3.008  | 3.024 | 2.924 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 8.71728801727
  Full duration: 19.7889790535

  test scenario CinderVolumes.list_volumes
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.list_volumes | 0.227 | 0.247  | 0.356  | 0.361  | 0.366 | 0.266 | 100.0%  | 10    |
  | total               | 0.227 | 0.247  | 0.356  | 0.361  | 0.366 | 0.266 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.759625911713
  Full duration: 46.0351030827

  test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.773  | 2.893  | 3.164  | 3.194  | 3.225  | 2.949  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.253  | 2.369  | 2.477  | 2.49   | 2.502  | 2.386  | 100.0%  | 10    |
  | nova.attach_volume     | 7.591  | 10.702 | 13.689 | 15.195 | 16.702 | 10.764 | 100.0%  | 10    |
  | nova.detach_volume     | 3.011  | 5.222  | 5.741  | 6.526  | 7.311  | 4.85   | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.194  | 2.285  | 2.418  | 2.46   | 2.501  | 2.305  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.361  | 2.489  | 2.6    | 2.604  | 2.608  | 2.479  | 100.0%  | 10    |
  | total                  | 21.273 | 25.722 | 28.871 | 29.897 | 30.924 | 26.045 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 77.9808602333
  Full duration: 116.938727856

  test scenario CinderVolumes.create_from_volume_and_delete_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 9.917  | 12.187 | 19.547 | 21.624 | 23.7   | 14.261 | 100.0%  | 10    |
  | cinder.delete_volume | 2.394  | 2.493  | 2.568  | 2.578  | 2.589  | 2.491  | 100.0%  | 10    |
  | total                | 12.495 | 14.721 | 22.041 | 24.068 | 26.095 | 16.752 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 48.7536959648
  Full duration: 67.4493231773

  test scenario CinderVolumes.create_and_extend_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.771 | 2.913  | 3.041  | 3.063  | 3.085 | 2.927 | 100.0%  | 10    |
  | cinder.extend_volume | 2.697 | 2.781  | 2.903  | 2.93   | 2.956 | 2.795 | 100.0%  | 10    |
  | cinder.delete_volume | 2.34  | 2.51   | 2.59   | 2.642  | 2.694 | 2.497 | 100.0%  | 10    |
  | total                | 7.894 | 8.268  | 8.419  | 8.459  | 8.5   | 8.219 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.6035699844
  Full duration: 31.5182521343

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.784  | 2.988  | 3.085  | 3.115  | 3.144  | 2.97   | 100.0%  | 10    |
  | cinder.create_snapshot | 2.237  | 2.369  | 2.43   | 2.51   | 2.589  | 2.363  | 100.0%  | 10    |
  | nova.attach_volume     | 7.638  | 7.847  | 12.52  | 12.525 | 12.531 | 8.973  | 100.0%  | 10    |
  | nova.detach_volume     | 2.933  | 3.436  | 5.288  | 5.554  | 5.82   | 4.018  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.181  | 2.279  | 2.323  | 2.335  | 2.347  | 2.266  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.357  | 2.56   | 2.744  | 2.749  | 2.754  | 2.569  | 100.0%  | 10    |
  | total                  | 21.343 | 23.631 | 26.003 | 26.089 | 26.175 | 23.505 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 69.038891077
  Full duration: 113.245260954

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.584  | 2.826  | 2.916  | 2.939  | 2.961  | 2.795  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.241  | 2.314  | 2.41   | 2.42   | 2.43   | 2.327  | 100.0%  | 10    |
  | nova.attach_volume     | 7.565  | 7.759  | 10.721 | 11.639 | 12.557 | 8.502  | 100.0%  | 10    |
  | nova.detach_volume     | 2.942  | 5.21   | 5.401  | 5.552  | 5.704  | 4.438  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.184  | 2.317  | 2.388  | 2.423  | 2.458  | 2.308  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.337  | 2.526  | 2.603  | 2.635  | 2.667  | 2.515  | 100.0%  | 10    |
  | total                  | 20.941 | 23.531 | 25.945 | 26.128 | 26.31  | 23.419 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 68.828496933
  Full duration: 109.817329884

  2016-02-10 23:36:46,743 - run_rally - DEBUG - task_id : c4bf15f0-eb49-4723-9aa9-81d6ea24dc2f
  2016-02-10 23:36:46,744 - run_rally - DEBUG - running command line : rally task report c4bf15f0-eb49-4723-9aa9-81d6ea24dc2f --out /home/opnfv/functest/results/rally/opnfv-cinder.html
  2016-02-10 23:36:47,453 - run_rally - DEBUG - running command line : rally task results c4bf15f0-eb49-4723-9aa9-81d6ea24dc2f
  2016-02-10 23:36:48,043 - run_rally - DEBUG - saving json file
  2016-02-10 23:36:48,049 - run_rally - DEBUG - Push result into DB
  2016-02-10 23:36:54,688 - run_rally - DEBUG - <Response [200]>
  2016-02-10 23:36:54,691 - run_rally - INFO - Test scenario: "cinder" OK.

  2016-02-10 23:36:54,691 - run_rally - INFO - Starting test scenario "heat" ...
  2016-02-10 23:36:54,691 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-heat.yaml
  2016-02-10 23:36:54,959 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '5333b06c-91ae-407b-8a20-a5c0adff52ee', 'service_list': ['heat'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}"
  2016-02-10 23:43:35,907 - run_rally - INFO -
   Preparing input task
   Task  b51e2f18-5a6b-4dfe-a8d1-c70fe9c89809: started
  Task b51e2f18-5a6b-4dfe-a8d1-c70fe9c89809: finished

  test scenario HeatStacks.create_suspend_resume_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack  | 2.705 | 3.144  | 3.332  | 3.38   | 3.429 | 3.107 | 100.0%  | 10    |
  | heat.suspend_stack | 0.51  | 0.746  | 1.69   | 1.77   | 1.849 | 1.06  | 100.0%  | 10    |
  | heat.resume_stack  | 0.575 | 1.511  | 1.753  | 1.755  | 1.758 | 1.484 | 100.0%  | 10    |
  | heat.delete_stack  | 1.294 | 1.509  | 1.637  | 1.669  | 1.701 | 1.49  | 100.0%  | 10    |
  | total              | 6.41  | 7.029  | 7.873  | 8.014  | 8.155 | 7.142 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 21.2204399109
  Full duration: 24.590711832

  test scenario HeatStacks.create_and_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.801 | 2.965  | 3.344  | 3.35   | 3.355 | 3.031 | 100.0%  | 10    |
  | heat.delete_stack | 0.298 | 1.513  | 1.627  | 1.666  | 1.705 | 1.42  | 100.0%  | 10    |
  | total             | 3.641 | 4.476  | 4.797  | 4.861  | 4.924 | 4.451 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 13.2714350224
  Full duration: 16.4613649845

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 10.292 | 11.433 | 13.021 | 13.279 | 13.538 | 11.632 | 100.0%  | 10    |
  | heat.delete_stack | 6.906  | 8.131  | 10.135 | 10.169 | 10.203 | 8.488  | 100.0%  | 10    |
  | total             | 18.35  | 20.557 | 21.396 | 21.472 | 21.548 | 20.12  | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 58.9332971573
  Full duration: 62.2598938942

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 12.909 | 13.935 | 16.654 | 17.691 | 18.729 | 14.656 | 100.0%  | 10    |
  | heat.delete_stack | 7.878  | 9.348  | 10.069 | 10.137 | 10.205 | 9.303  | 100.0%  | 10    |
  | total             | 21.856 | 23.051 | 26.606 | 27.304 | 28.002 | 23.959 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 71.925632
  Full duration: 75.6575791836

  test scenario HeatStacks.list_stacks_and_resources
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.list_stacks                | 0.225 | 0.243  | 0.265  | 0.273  | 0.282 | 0.246 | 100.0%  | 10    |
  | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0   | 0.0   | 100.0%  | 10    |
  | total                           | 0.226 | 0.243  | 0.265  | 0.273  | 0.282 | 0.247 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.744506120682
  Full duration: 3.46860694885

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.813 | 3.014  | 3.162  | 3.185  | 3.208 | 3.005 | 100.0%  | 10    |
  | heat.update_stack | 2.615 | 3.625  | 3.829  | 3.855  | 3.882 | 3.569 | 100.0%  | 10    |
  | heat.delete_stack | 1.297 | 1.459  | 1.597  | 1.69   | 1.783 | 1.476 | 100.0%  | 10    |
  | total             | 6.833 | 8.129  | 8.414  | 8.465  | 8.515 | 8.049 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.4935848713
  Full duration: 27.9353289604

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.712 | 2.948  | 3.15   | 3.177  | 3.203 | 2.968 | 100.0%  | 10    |
  | heat.update_stack | 2.505 | 2.769  | 3.755  | 3.798  | 3.841 | 2.978 | 100.0%  | 10    |
  | heat.delete_stack | 0.41  | 1.398  | 1.579  | 1.602  | 1.626 | 1.239 | 100.0%  | 10    |
  | total             | 5.681 | 7.006  | 8.392  | 8.423  | 8.454 | 7.185 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 22.0256738663
  Full duration: 25.4327590466

  test scenario HeatStacks.create_update_delete_stack
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 2.851 | 3.082  | 3.313  | 3.327  | 3.34   | 3.094  | 100.0%  | 10    |
  | heat.update_stack | 4.859 | 5.059  | 5.825  | 5.846  | 5.867  | 5.181  | 100.0%  | 10    |
  | heat.delete_stack | 1.459 | 2.448  | 2.821  | 2.894  | 2.968  | 2.222  | 100.0%  | 10    |
  | total             | 9.546 | 10.498 | 11.42  | 11.439 | 11.457 | 10.497 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 31.3824648857
  Full duration: 35.0282361507

  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 6.58436203003
  Full duration: 13.4351229668

  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg    | success | count |
  +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
  | heat.create_stack | 3.053 | 3.139  | 3.256  | 3.339  | 3.422 | 3.161  | 100.0%  | 10    |
  | heat.update_stack | 4.769 | 4.927  | 5.262  | 5.626  | 5.989 | 5.053  | 100.0%  | 10    |
  | heat.delete_stack | 1.405 | 2.531  | 2.685  | 2.73   | 2.775 | 2.201  | 100.0%  | 10    |
  | total             | 9.427 | 10.614 | 11.08  | 11.32  | 11.56 | 10.415 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
  Load duration: 31.9777891636
  Full duration: 35.6663069725

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.863 | 2.98   | 3.296  | 3.358  | 3.42  | 3.049 | 100.0%  | 10    |
  | heat.update_stack | 3.505 | 3.801  | 3.997  | 4.081  | 4.165 | 3.804 | 100.0%  | 10    |
  | heat.delete_stack | 1.338 | 1.583  | 1.668  | 1.68   | 1.691 | 1.568 | 100.0%  | 10    |
  | total             | 7.943 | 8.385  | 8.655  | 8.755  | 8.855 | 8.421 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 25.0527100563
  Full duration: 28.7379829884

  test scenario HeatStacks.create_and_list_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.845 | 3.135  | 3.391  | 3.404  | 3.418 | 3.147 | 100.0%  | 10    |
  | heat.list_stacks  | 0.036 | 0.162  | 0.205  | 0.239  | 0.272 | 0.131 | 100.0%  | 10    |
  | total             | 3.014 | 3.266  | 3.453  | 3.517  | 3.581 | 3.278 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.90862584114
  Full duration: 17.3963320255

  test scenario HeatStacks.create_check_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.902 | 3.042  | 3.151  | 3.168  | 3.186 | 3.037 | 100.0%  | 10    |
  | heat.check_stack  | 0.317 | 0.552  | 0.774  | 0.918  | 1.062 | 0.597 | 100.0%  | 10    |
  | heat.delete_stack | 1.314 | 1.551  | 1.784  | 1.868  | 1.952 | 1.601 | 100.0%  | 10    |
  | total             | 4.91  | 5.201  | 5.487  | 5.636  | 5.784 | 5.236 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 15.5446360111
  Full duration: 19.7330510616

  2016-02-10 23:43:35,907 - run_rally - DEBUG - task_id : b51e2f18-5a6b-4dfe-a8d1-c70fe9c89809
  2016-02-10 23:43:35,907 - run_rally - DEBUG - running command line : rally task report b51e2f18-5a6b-4dfe-a8d1-c70fe9c89809 --out /home/opnfv/functest/results/rally/opnfv-heat.html
  2016-02-10 23:43:36,536 - run_rally - DEBUG - running command line : rally task results b51e2f18-5a6b-4dfe-a8d1-c70fe9c89809
  2016-02-10 23:43:37,131 - run_rally - DEBUG - saving json file
  2016-02-10 23:43:37,133 - run_rally - DEBUG - Push result into DB
  2016-02-10 23:43:43,814 - run_rally - DEBUG - <Response [200]>
  2016-02-10 23:43:43,816 - run_rally - INFO - Test scenario: "heat" Failed.

  2016-02-10 23:43:43,816 - run_rally - INFO - Starting test scenario "keystone" ...
  2016-02-10 23:43:43,816 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-keystone.yaml
  2016-02-10 23:43:44,240 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '5333b06c-91ae-407b-8a20-a5c0adff52ee', 'service_list': ['keystone'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}"
  2016-02-10 23:45:10,505 - run_rally - INFO -
   Preparing input task
   Task  a2dc597b-35dc-4b85-a214-5ff65687a80d: started
  Task a2dc597b-35dc-4b85-a214-5ff65687a80d: finished

  test scenario KeystoneBasic.create_tenant_with_users
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.108 | 0.12   | 0.133  | 0.144  | 0.154 | 0.122 | 100.0%  | 10    |
  | keystone.create_users  | 0.627 | 0.66   | 0.746  | 0.753  | 0.759 | 0.679 | 100.0%  | 10    |
  | total                  | 0.746 | 0.783  | 0.882  | 0.891  | 0.899 | 0.8   | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.38129496574
  Full duration: 12.5912969112

  test scenario KeystoneBasic.create_add_and_list_user_roles
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.108 | 0.123  | 0.137  | 0.139  | 0.142 | 0.123 | 100.0%  | 10    |
  | keystone.add_role    | 0.088 | 0.094  | 0.105  | 0.11   | 0.115 | 0.096 | 100.0%  | 10    |
  | keystone.list_roles  | 0.051 | 0.053  | 0.057  | 0.06   | 0.062 | 0.054 | 100.0%  | 10    |
  | total                | 0.252 | 0.275  | 0.287  | 0.294  | 0.301 | 0.274 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.828149080276
  Full duration: 6.11214399338

  test scenario KeystoneBasic.add_and_remove_user_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.124 | 0.223  | 0.305  | 0.336  | 0.367 | 0.218 | 100.0%  | 10    |
  | keystone.add_role    | 0.088 | 0.1    | 0.111  | 0.111  | 0.111 | 0.101 | 100.0%  | 10    |
  | keystone.remove_role | 0.057 | 0.068  | 0.098  | 0.137  | 0.177 | 0.079 | 100.0%  | 10    |
  | total                | 0.284 | 0.411  | 0.525  | 0.555  | 0.585 | 0.398 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.2285490036
  Full duration: 6.55177402496

  test scenario KeystoneBasic.create_update_and_delete_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.13  | 0.238  | 0.275  | 0.281  | 0.287 | 0.213 | 100.0%  | 10    |
  | keystone.update_tenant | 0.05  | 0.06   | 0.197  | 0.2    | 0.203 | 0.093 | 100.0%  | 10    |
  | keystone.delete_tenant | 0.126 | 0.131  | 0.243  | 0.27   | 0.297 | 0.158 | 100.0%  | 10    |
  | total                  | 0.307 | 0.431  | 0.616  | 0.642  | 0.667 | 0.464 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.3783249855
  Full duration: 5.19503498077

  test scenario KeystoneBasic.create_and_delete_service
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_service | 0.125 | 0.13   | 0.149  | 0.159  | 0.169 | 0.136 | 100.0%  | 10    |
  | keystone.delete_service | 0.057 | 0.07   | 0.086  | 0.088  | 0.091 | 0.073 | 100.0%  | 10    |
  | total                   | 0.187 | 0.209  | 0.233  | 0.237  | 0.241 | 0.209 | 100.0%  | 10    |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.616975784302
  Full duration: 4.38122606277

  test scenario KeystoneBasic.create_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.118 | 0.142  | 0.156  | 0.161  | 0.167 | 0.141 | 100.0%  | 10    |
  | total                  | 0.118 | 0.142  | 0.156  | 0.162  | 0.167 | 0.141 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.460291147232
  Full duration: 4.38871192932

  test scenario KeystoneBasic.create_user
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.12 | 0.141  | 0.17   | 0.178  | 0.185 | 0.148 | 100.0%  | 10    |
  | total                | 0.12 | 0.141  | 0.17   | 0.178  | 0.185 | 0.148 | 100.0%  | 10    |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.443107843399
  Full duration: 4.33838415146

  test scenario KeystoneBasic.create_and_list_tenants
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.12  | 0.124  | 0.17   | 0.178  | 0.186 | 0.136 | 100.0%  | 10    |
  | keystone.list_tenants  | 0.05  | 0.054  | 0.071  | 0.088  | 0.106 | 0.06  | 100.0%  | 10    |
  | total                  | 0.175 | 0.179  | 0.231  | 0.242  | 0.254 | 0.196 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.603140115738
  Full duration: 5.95085787773

  test scenario KeystoneBasic.create_and_delete_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.109 | 0.202  | 0.275  | 0.311  | 0.347 | 0.205 | 100.0%  | 10    |
  | keystone.delete_role | 0.105 | 0.12   | 0.231  | 0.237  | 0.243 | 0.142 | 100.0%  | 10    |
  | total                | 0.236 | 0.352  | 0.43   | 0.503  | 0.576 | 0.348 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.02657985687
  Full duration: 4.95588898659

  test scenario KeystoneBasic.get_entities
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.113 | 0.129  | 0.165  | 0.166  | 0.167 | 0.136 | 100.0%  | 10    |
  | keystone.create_user   | 0.06  | 0.069  | 0.08   | 0.097  | 0.115 | 0.071 | 100.0%  | 10    |
  | keystone.create_role   | 0.047 | 0.053  | 0.094  | 0.095  | 0.097 | 0.061 | 100.0%  | 10    |
  | keystone.get_tenant    | 0.045 | 0.047  | 0.054  | 0.056  | 0.058 | 0.049 | 100.0%  | 10    |
  | keystone.get_user      | 0.051 | 0.054  | 0.059  | 0.06   | 0.062 | 0.055 | 100.0%  | 10    |
  | keystone.get_role      | 0.043 | 0.049  | 0.06   | 0.079  | 0.099 | 0.053 | 100.0%  | 10    |
  | keystone.service_list  | 0.047 | 0.06   | 0.099  | 0.105  | 0.111 | 0.067 | 100.0%  | 10    |
  | keystone.get_service   | 0.041 | 0.048  | 0.055  | 0.061  | 0.067 | 0.049 | 100.0%  | 10    |
  | total                  | 0.491 | 0.543  | 0.573  | 0.582  | 0.591 | 0.541 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.64348506927
  Full duration: 9.77697682381

  test scenario KeystoneBasic.create_and_list_users
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.133 | 0.142  | 0.187  | 0.192  | 0.196 | 0.151 | 100.0%  | 10    |
  | keystone.list_users  | 0.05  | 0.056  | 0.068  | 0.068  | 0.069 | 0.057 | 100.0%  | 10    |
  | total                | 0.183 | 0.202  | 0.244  | 0.25   | 0.257 | 0.208 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.625062942505
  Full duration: 4.61658096313

  2016-02-10 23:45:10,506 - run_rally - DEBUG - task_id : a2dc597b-35dc-4b85-a214-5ff65687a80d
  2016-02-10 23:45:10,506 - run_rally - DEBUG - running command line : rally task report a2dc597b-35dc-4b85-a214-5ff65687a80d --out /home/opnfv/functest/results/rally/opnfv-keystone.html
  2016-02-10 23:45:11,115 - run_rally - DEBUG - running command line : rally task results a2dc597b-35dc-4b85-a214-5ff65687a80d
  2016-02-10 23:45:11,706 - run_rally - DEBUG - saving json file
  2016-02-10 23:45:11,708 - run_rally - DEBUG - Push result into DB
  2016-02-10 23:45:17,896 - run_rally - DEBUG - <Response [200]>
  2016-02-10 23:45:17,900 - run_rally - INFO - Test scenario: "keystone" OK.

  2016-02-10 23:45:17,900 - run_rally - INFO - Starting test scenario "neutron" ...
  2016-02-10 23:45:17,900 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-neutron.yaml
  2016-02-10 23:45:18,243 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '5333b06c-91ae-407b-8a20-a5c0adff52ee', 'service_list': ['neutron'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}"
  2016-02-10 23:50:17,508 - run_rally - INFO -
   Preparing input task
   Task  9f432e5d-104a-4b3a-b844-aa338a0da828: started
  Task 9f432e5d-104a-4b3a-b844-aa338a0da828: finished

  test scenario NeutronNetworks.create_and_delete_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.427 | 0.554  | 0.614  | 0.643  | 0.673 | 0.536 | 100.0%  | 10    |
  | neutron.delete_port | 0.142 | 0.237  | 0.342  | 0.476  | 0.611 | 0.256 | 100.0%  | 10    |
  | total               | 0.569 | 0.743  | 0.925  | 1.104  | 1.283 | 0.792 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.1176700592
  Full duration: 24.8256268501

  test scenario NeutronNetworks.create_and_list_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.423 | 0.477  | 0.542  | 0.576  | 0.609 | 0.489 | 100.0%  | 10    |
  | neutron.create_router        | 0.037 | 0.106  | 0.208  | 0.212  | 0.217 | 0.116 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.283 | 0.413  | 0.456  | 0.492  | 0.527 | 0.403 | 100.0%  | 10    |
  | neutron.list_routers         | 0.032 | 0.094  | 0.183  | 0.188  | 0.193 | 0.103 | 100.0%  | 10    |
  | total                        | 0.953 | 1.114  | 1.232  | 1.246  | 1.261 | 1.11  | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.33451294899
  Full duration: 27.7111759186

  test scenario NeutronNetworks.create_and_delete_routers
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet           | 0.395 | 0.424  | 0.48   | 0.489  | 0.499 | 0.436 | 100.0%  | 10    |
  | neutron.create_router           | 0.039 | 0.189  | 0.242  | 0.345  | 0.448 | 0.176 | 100.0%  | 10    |
  | neutron.add_interface_router    | 0.281 | 0.434  | 0.596  | 0.618  | 0.641 | 0.424 | 100.0%  | 10    |
  | neutron.remove_interface_router | 0.252 | 0.36   | 0.398  | 0.4    | 0.402 | 0.341 | 100.0%  | 10    |
  | neutron.delete_router           | 0.147 | 0.172  | 0.315  | 0.358  | 0.401 | 0.213 | 100.0%  | 10    |
  | total                           | 1.34  | 1.578  | 1.726  | 1.746  | 1.765 | 1.589 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.79766583443
  Full duration: 28.1387701035

  test scenario NeutronNetworks.create_and_list_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.426 | 0.518  | 0.617  | 0.63   | 0.643 | 0.527 | 100.0%  | 10    |
  | neutron.list_ports  | 0.093 | 0.212  | 0.314  | 0.332  | 0.351 | 0.213 | 100.0%  | 10    |
  | total               | 0.522 | 0.731  | 0.94   | 0.953  | 0.966 | 0.74  | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.09701919556
  Full duration: 25.6951978207

  test scenario NeutronNetworks.create_and_delete_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.397 | 0.522  | 0.625  | 0.631  | 0.636 | 0.502 | 100.0%  | 10    |
  | neutron.delete_subnet | 0.14  | 0.314  | 0.383  | 0.398  | 0.413 | 0.308 | 100.0%  | 10    |
  | total                 | 0.537 | 0.83   | 0.98   | 0.992  | 1.004 | 0.809 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.3898100853
  Full duration: 25.9560959339

  test scenario NeutronNetworks.create_and_delete_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.321 | 0.355  | 0.463  | 0.468  | 0.472 | 0.371 | 100.0%  | 10    |
  | neutron.delete_network | 0.123 | 0.252  | 0.327  | 0.331  | 0.336 | 0.249 | 100.0%  | 10    |
  | total                  | 0.47  | 0.627  | 0.737  | 0.762  | 0.787 | 0.62  | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.76910996437
  Full duration: 13.8404121399

  test scenario NeutronNetworks.create_and_list_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.307 | 0.34   | 0.401  | 0.433  | 0.466 | 0.353 | 100.0%  | 10    |
  | neutron.list_networks  | 0.042 | 0.165  | 0.233  | 0.241  | 0.248 | 0.135 | 100.0%  | 10    |
  | total                  | 0.351 | 0.479  | 0.628  | 0.64   | 0.652 | 0.488 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.40053105354
  Full duration: 15.5931649208

  test scenario NeutronNetworks.create_and_update_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.375 | 0.475  | 0.507  | 0.549  | 0.592 | 0.469 | 100.0%  | 10    |
  | neutron.create_router        | 0.037 | 0.057  | 0.215  | 0.303  | 0.392 | 0.119 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.289 | 0.427  | 0.468  | 0.469  | 0.47  | 0.402 | 100.0%  | 10    |
  | neutron.update_router        | 0.119 | 0.135  | 0.264  | 0.265  | 0.266 | 0.17  | 100.0%  | 10    |
  | total                        | 0.998 | 1.14   | 1.363  | 1.364  | 1.366 | 1.16  | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.51950502396
  Full duration: 28.7816469669

  test scenario NeutronNetworks.create_and_update_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.306 | 0.352  | 0.562  | 0.585  | 0.609 | 0.395 | 100.0%  | 10    |
  | neutron.update_network | 0.105 | 0.264  | 0.323  | 0.353  | 0.383 | 0.241 | 100.0%  | 10    |
  | total                  | 0.41  | 0.658  | 0.751  | 0.752  | 0.753 | 0.635 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.86403417587
  Full duration: 16.0056118965

  test scenario NeutronNetworks.create_and_update_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.431 | 0.582  | 0.66   | 0.679  | 0.698 | 0.557 | 100.0%  | 10    |
  | neutron.update_port | 0.12  | 0.289  | 0.348  | 0.355  | 0.362 | 0.272 | 100.0%  | 10    |
  | total               | 0.569 | 0.834  | 1.002  | 1.003  | 1.003 | 0.829 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.53265404701
  Full duration: 26.9364058971

  test scenario NeutronNetworks.create_and_list_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.392 | 0.427  | 0.55   | 0.556  | 0.561 | 0.453 | 100.0%  | 10    |
  | neutron.list_subnets  | 0.058 | 0.194  | 0.283  | 0.287  | 0.291 | 0.173 | 100.0%  | 10    |
  | total                 | 0.477 | 0.627  | 0.753  | 0.786  | 0.819 | 0.626 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.75291109085
  Full duration: 25.8106958866

  test scenario NeutronNetworks.create_and_update_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.396 | 0.418  | 0.526  | 0.526  | 0.526 | 0.449 | 100.0%  | 10    |
  | neutron.update_subnet | 0.162 | 0.299  | 0.393  | 0.393  | 0.394 | 0.293 | 100.0%  | 10    |
  | total                 | 0.583 | 0.755  | 0.812  | 0.817  | 0.822 | 0.742 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.20696282387
  Full duration: 26.2696731091

  2016-02-10 23:50:17,509 - run_rally - DEBUG - task_id : 9f432e5d-104a-4b3a-b844-aa338a0da828
  2016-02-10 23:50:17,509 - run_rally - DEBUG - running command line : rally task report 9f432e5d-104a-4b3a-b844-aa338a0da828 --out /home/opnfv/functest/results/rally/opnfv-neutron.html
  2016-02-10 23:50:18,133 - run_rally - DEBUG - running command line : rally task results 9f432e5d-104a-4b3a-b844-aa338a0da828
  2016-02-10 23:50:18,739 - run_rally - DEBUG - saving json file
  2016-02-10 23:50:18,743 - run_rally - DEBUG - Push result into DB
  2016-02-10 23:50:25,367 - run_rally - DEBUG - <Response [200]>
  2016-02-10 23:50:25,369 - run_rally - INFO - Test scenario: "neutron" OK.

  2016-02-10 23:50:25,370 - run_rally - INFO - Starting test scenario "nova" ...
  2016-02-10 23:50:25,370 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-nova.yaml
  2016-02-10 23:50:25,701 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '5333b06c-91ae-407b-8a20-a5c0adff52ee', 'service_list': ['nova'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}"
  2016-02-11 00:19:05,621 - run_rally - INFO -
   Preparing input task
   Task  08b4bf35-51b4-464d-84ec-8b7381b19b6d: started
  Task 08b4bf35-51b4-464d-84ec-8b7381b19b6d: finished

  test scenario NovaKeypair.create_and_delete_keypair
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.373 | 0.448  | 0.655  | 0.661  | 0.667 | 0.492 | 100.0%  | 10    |
  | nova.delete_keypair | 0.011 | 0.016  | 0.021  | 0.022  | 0.024 | 0.017 | 100.0%  | 10    |
  | total               | 0.39  | 0.461  | 0.672  | 0.676  | 0.681 | 0.509 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.5162088871
  Full duration: 15.1700220108

  test scenario NovaServers.boot_and_live_migrate_server
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 10.2629051208
  Full duration: 30.6517119408

  test scenario NovaServers.resize_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.503  | 4.665  | 6.416  | 6.423  | 6.43   | 4.859  | 100.0%  | 10    |
  | nova.resize         | 21.142 | 31.559 | 41.868 | 42.148 | 42.428 | 30.669 | 100.0%  | 10    |
  | nova.resize_confirm | 2.369  | 2.404  | 2.581  | 2.608  | 2.635  | 2.45   | 100.0%  | 10    |
  | nova.delete_server  | 2.382  | 2.537  | 2.6    | 2.657  | 2.714  | 2.509  | 100.0%  | 10    |
  | total               | 30.071 | 41.459 | 53.105 | 53.46  | 53.814 | 40.487 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 103.749622822
  Full duration: 117.664920807

  test scenario NovaServers.snapshot_server
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | action                 | min    | median | 90%ile  | 95%ile  | max     | avg    | success | count |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | nova.boot_server       | 4.697  | 6.722  | 7.381   | 7.412   | 7.443   | 6.421  | 100.0%  | 10    |
  | nova.create_image      | 27.446 | 56.176 | 75.464  | 77.263  | 79.062  | 54.113 | 100.0%  | 10    |
  | nova.delete_server     | 2.392  | 2.567  | 2.878   | 3.031   | 3.183   | 2.647  | 100.0%  | 10    |
  | nova.boot_server (2)   | 14.757 | 28.959 | 37.432  | 44.257  | 51.082  | 28.154 | 100.0%  | 10    |
  | nova.delete_server (2) | 2.427  | 4.698  | 4.989   | 5.204   | 5.419   | 3.966  | 100.0%  | 10    |
  | nova.delete_image      | 0.318  | 0.432  | 0.622   | 0.654   | 0.687   | 0.46   | 100.0%  | 10    |
  | total                  | 62.068 | 97.916 | 124.362 | 125.622 | 126.882 | 95.762 | 100.0%  | 10    |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  Load duration: 263.444504976
  Full duration: 287.171573877

  test scenario NovaKeypair.boot_and_delete_server_with_keypair
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | nova.create_keypair | 0.4   | 0.479  | 0.545  | 0.548  | 0.551  | 0.473 | 100.0%  | 10    |
  | nova.boot_server    | 3.185 | 4.612  | 5.917  | 5.941  | 5.965  | 4.6   | 100.0%  | 10    |
  | nova.delete_server  | 2.378 | 2.573  | 4.795  | 4.817  | 4.839  | 3.194 | 100.0%  | 10    |
  | nova.delete_keypair | 0.012 | 0.016  | 0.021  | 0.022  | 0.023  | 0.016 | 100.0%  | 10    |
  | total               | 6.115 | 7.563  | 11.095 | 11.205 | 11.315 | 8.283 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 24.9650418758
  Full duration: 48.4524579048

  test scenario NovaKeypair.create_and_list_keypairs
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.38  | 0.482  | 0.568  | 0.573  | 0.577 | 0.477 | 100.0%  | 10    |
  | nova.list_keypairs  | 0.012 | 0.016  | 0.022  | 0.024  | 0.026 | 0.017 | 100.0%  | 10    |
  | total               | 0.393 | 0.501  | 0.584  | 0.587  | 0.59  | 0.494 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.60101890564
  Full duration: 16.9254760742

  test scenario NovaServers.list_servers
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.list_servers | 0.578 | 0.653  | 0.856  | 0.868  | 0.879 | 0.695 | 100.0%  | 10    |
  | total             | 0.578 | 0.653  | 0.856  | 0.868  | 0.879 | 0.695 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.03527998924
  Full duration: 49.9647991657

  test scenario NovaServers.boot_server_attach_created_volume_and_live_migrate
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 36.9445459843
  Full duration: 71.067373991

  test scenario NovaServers.boot_server_from_volume_and_delete
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.284  | 4.347  | 5.917  | 5.935  | 5.953  | 4.57   | 100.0%  | 10    |
  | nova.boot_server     | 8.656  | 8.975  | 11.751 | 12.822 | 13.894 | 9.979  | 100.0%  | 10    |
  | nova.delete_server   | 4.469  | 4.629  | 4.902  | 5.77   | 6.637  | 4.795  | 100.0%  | 10    |
  | total                | 16.705 | 18.797 | 22.17  | 23.265 | 24.359 | 19.344 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 56.6653358936
  Full duration: 86.5513851643

  test scenario NovaServers.boot_and_migrate_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.545  | 5.453  | 6.379  | 6.388  | 6.397  | 5.304  | 100.0%  | 10    |
  | nova.stop_server    | 4.889  | 5.218  | 15.761 | 15.837 | 15.913 | 8.914  | 100.0%  | 10    |
  | nova.migrate        | 16.4   | 33.87  | 34.769 | 37.772 | 40.775 | 29.605 | 100.0%  | 10    |
  | nova.resize_confirm | 2.374  | 2.413  | 2.564  | 2.628  | 2.693  | 2.457  | 100.0%  | 10    |
  | nova.delete_server  | 2.375  | 2.505  | 2.571  | 2.596  | 2.622  | 2.49   | 100.0%  | 10    |
  | total               | 31.462 | 49.989 | 59.92  | 62.401 | 64.881 | 48.769 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 139.907422066
  Full duration: 153.807698965

  test scenario NovaServers.boot_and_delete_server
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | nova.boot_server   | 3.504 | 4.938  | 6.215  | 6.23   | 6.245  | 4.81  | 100.0%  | 10    |
  | nova.delete_server | 2.413 | 2.601  | 2.875  | 3.698  | 4.52   | 2.761 | 100.0%  | 10    |
  | total              | 5.933 | 7.491  | 9.071  | 9.902  | 10.733 | 7.571 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 22.7597670555
  Full duration: 46.605672121

  test scenario NovaServers.boot_and_rebuild_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.637  | 6.025  | 6.449  | 6.453  | 6.457  | 5.483  | 100.0%  | 10    |
  | nova.rebuild_server | 6.436  | 7.77   | 15.755 | 15.76  | 15.766 | 9.178  | 100.0%  | 10    |
  | nova.delete_server  | 2.369  | 2.424  | 2.61   | 2.678  | 2.747  | 2.483  | 100.0%  | 10    |
  | total               | 13.692 | 16.387 | 21.826 | 21.969 | 22.111 | 17.143 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 47.7669019699
  Full duration: 71.1696259975

  test scenario NovaSecGroup.create_and_list_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.519  | 1.756  | 1.917  | 1.969  | 2.021  | 1.735  | 100.0%  | 10    |
  | nova.create_100_rules          | 9.199  | 10.422 | 10.663 | 10.758 | 10.853 | 10.254 | 100.0%  | 10    |
  | nova.list_security_groups      | 0.093  | 0.136  | 0.157  | 0.158  | 0.159  | 0.132  | 100.0%  | 10    |
  | total                          | 10.904 | 12.348 | 12.613 | 12.632 | 12.652 | 12.121 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 35.5776119232
  Full duration: 63.5648519993

  test scenario NovaSecGroup.create_and_delete_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.885  | 2.052  | 2.253  | 2.296  | 2.338  | 2.073  | 100.0%  | 10    |
  | nova.create_100_rules          | 8.876  | 10.379 | 10.859 | 10.946 | 11.032 | 10.212 | 100.0%  | 10    |
  | nova.delete_10_security_groups | 0.846  | 0.986  | 1.172  | 1.231  | 1.289  | 1.008  | 100.0%  | 10    |
  | total                          | 12.057 | 13.517 | 13.809 | 13.925 | 14.042 | 13.293 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 39.1708610058
  Full duration: 53.6136760712

  test scenario NovaServers.boot_and_bounce_server
  +----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                        |
  +-------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | action                  | min    | median | 90%ile  | 95%ile  | max     | avg    | success | count |
  +-------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | nova.boot_server        | 3.443  | 3.823  | 6.488   | 6.515   | 6.543   | 4.601  | 100.0%  | 10    |
  | nova.reboot_server      | 2.592  | 4.623  | 6.671   | 6.813   | 6.955   | 4.866  | 100.0%  | 10    |
  | nova.soft_reboot_server | 4.646  | 6.73   | 126.895 | 127.35  | 127.805 | 30.601 | 100.0%  | 10    |
  | nova.stop_server        | 4.646  | 4.94   | 15.518  | 15.693  | 15.867  | 7.046  | 100.0%  | 10    |
  | nova.start_server       | 2.619  | 2.794  | 2.96    | 3.449   | 3.939   | 2.861  | 100.0%  | 10    |
  | nova.rescue_server      | 6.623  | 11.184 | 17.613  | 17.639  | 17.665  | 11.717 | 100.0%  | 10    |
  | nova.unrescue_server    | 2.299  | 3.39   | 4.596   | 4.626   | 4.655   | 3.421  | 100.0%  | 10    |
  | nova.delete_server      | 2.374  | 2.396  | 2.532   | 2.554   | 2.575   | 2.437  | 100.0%  | 10    |
  | total                   | 33.772 | 47.069 | 161.92  | 168.976 | 176.031 | 67.561 | 100.0%  | 10    |
  +-------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  Load duration: 176.050487041
  Full duration: 199.794572115

  test scenario NovaServers.boot_server
  +---------------------------------------------------------------------------------------+
  |                                 Response Times (sec)                                  |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server | 3.535 | 3.971  | 6.359  | 6.504  | 6.649 | 4.691 | 100.0%  | 10    |
  | total            | 3.535 | 3.971  | 6.359  | 6.504  | 6.649 | 4.691 | 100.0%  | 10    |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 13.4904000759
  Full duration: 36.8076519966

  test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
  +-----------------------------------------------------------------------------------------------------------+
  |                                           Response Times (sec)                                            |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups    | 1.778  | 2.057  | 2.4    | 2.444  | 2.487  | 2.078  | 100.0%  | 10    |
  | nova.create_100_rules             | 9.291  | 10.066 | 10.404 | 10.686 | 10.967 | 10.061 | 100.0%  | 10    |
  | nova.boot_server                  | 3.293  | 4.462  | 6.701  | 6.838  | 6.974  | 5.006  | 100.0%  | 10    |
  | nova.get_attached_security_groups | 0.142  | 0.159  | 0.188  | 0.199  | 0.209  | 0.164  | 100.0%  | 10    |
  | nova.delete_server                | 2.412  | 2.535  | 4.677  | 4.713  | 4.749  | 3.154  | 100.0%  | 10    |
  | nova.delete_10_security_groups    | 0.818  | 0.916  | 1.001  | 1.014  | 1.027  | 0.911  | 100.0%  | 10    |
  | total                             | 17.852 | 20.4   | 24.95  | 25.046 | 25.142 | 21.375 | 100.0%  | 10    |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 62.7762010098
  Full duration: 86.571160078

  test scenario NovaServers.pause_and_unpause_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.511  | 4.668  | 6.119  | 6.135  | 6.15   | 4.767  | 100.0%  | 10    |
  | nova.pause_server   | 2.307  | 2.47   | 2.577  | 2.655  | 2.732  | 2.457  | 100.0%  | 10    |
  | nova.unpause_server | 2.32   | 2.461  | 2.57   | 2.585  | 2.601  | 2.458  | 100.0%  | 10    |
  | nova.delete_server  | 2.381  | 2.591  | 4.596  | 4.613  | 4.631  | 2.953  | 100.0%  | 10    |
  | total               | 10.769 | 12.136 | 15.599 | 15.6   | 15.601 | 12.635 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 36.0108971596
  Full duration: 59.3288369179

  test scenario NovaServers.boot_server_from_volume_and_live_migrate
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 41.4217681885
  Full duration: 71.6037459373

  test scenario NovaServers.boot_server_from_volume
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
  +----------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | cinder.create_volume | 3.252  | 3.677  | 5.937  | 5.975  | 6.013  | 4.432 | 100.0%  | 10    |
  | nova.boot_server     | 8.451  | 8.987  | 11.258 | 11.268 | 11.279 | 9.688 | 100.0%  | 10    |
  | total                | 11.839 | 13.981 | 17.047 | 17.065 | 17.084 | 14.12 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 40.1873419285
  Full duration: 75.1306819916

  test scenario NovaServers.boot_and_list_server
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server  | 3.455 | 4.931  | 6.206  | 6.338  | 6.471 | 4.88  | 100.0%  | 10    |
  | nova.list_servers | 0.147 | 0.36   | 0.432  | 0.434  | 0.436 | 0.307 | 100.0%  | 10    |
  | total             | 3.886 | 5.15   | 6.374  | 6.601  | 6.828 | 5.187 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 15.448579073
  Full duration: 49.2652499676

  2016-02-11 00:19:05,622 - run_rally - DEBUG - task_id : 08b4bf35-51b4-464d-84ec-8b7381b19b6d
  2016-02-11 00:19:05,622 - run_rally - DEBUG - running command line : rally task report 08b4bf35-51b4-464d-84ec-8b7381b19b6d --out /home/opnfv/functest/results/rally/opnfv-nova.html
  2016-02-11 00:19:06,337 - run_rally - DEBUG - running command line : rally task results 08b4bf35-51b4-464d-84ec-8b7381b19b6d
  2016-02-11 00:19:06,947 - run_rally - DEBUG - saving json file
  2016-02-11 00:19:06,954 - run_rally - DEBUG - Push result into DB
  2016-02-11 00:19:14,145 - run_rally - DEBUG - <Response [200]>
  2016-02-11 00:19:14,149 - run_rally - INFO - Test scenario: "nova" Failed.

  2016-02-11 00:19:14,150 - run_rally - INFO - Starting test scenario "quotas" ...
  2016-02-11 00:19:14,150 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-quotas.yaml
  2016-02-11 00:19:14,610 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '5333b06c-91ae-407b-8a20-a5c0adff52ee', 'service_list': ['quotas'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}"
  2016-02-11 00:19:58,886 - run_rally - INFO -
   Preparing input task
   Task  4b88c6b5-6d04-41f1-b7bf-0530d1460380: started
  Task 4b88c6b5-6d04-41f1-b7bf-0530d1460380: finished

  test scenario Quotas.cinder_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.571 | 0.661  | 0.724  | 0.726  | 0.728 | 0.653 | 100.0%  | 10    |
  | total                | 0.571 | 0.661  | 0.724  | 0.726  | 0.728 | 0.654 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.99102902412
  Full duration: 7.71833896637

  test scenario Quotas.neutron_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.22  | 0.241  | 0.351  | 0.373  | 0.396 | 0.268 | 100.0%  | 10    |
  | total                | 0.276 | 0.305  | 0.415  | 0.441  | 0.467 | 0.331 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.942007064819
  Full duration: 6.36414504051

  test scenario Quotas.cinder_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.587 | 0.616  | 0.682  | 0.704  | 0.726 | 0.629 | 100.0%  | 10    |
  | quotas.delete_quotas | 0.41  | 0.461  | 0.544  | 0.562  | 0.579 | 0.472 | 100.0%  | 10    |
  | total                | 1.006 | 1.112  | 1.204  | 1.235  | 1.267 | 1.101 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.30020499229
  Full duration: 9.0813190937

  test scenario Quotas.nova_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.327 | 0.339  | 0.357  | 0.358  | 0.359 | 0.342 | 100.0%  | 8     |
  | quotas.delete_quotas | 0.016 | 0.023  | 0.027  | 0.027  | 0.028 | 0.022 | 75.0%   | 8     |
  | total                | 0.353 | 0.356  | 0.372  | 0.374  | 0.377 | 0.361 | 75.0%   | 8     |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.749735832214
  Full duration: 5.99576282501

  test scenario Quotas.nova_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.321 | 0.364  | 0.452  | 0.48   | 0.507 | 0.379 | 100.0%  | 10    |
  | total                | 0.321 | 0.364  | 0.452  | 0.48   | 0.507 | 0.379 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.10366201401
  Full duration: 6.54270100594

  2016-02-11 00:19:58,886 - run_rally - DEBUG - task_id : 4b88c6b5-6d04-41f1-b7bf-0530d1460380
  2016-02-11 00:19:58,886 - run_rally - DEBUG - running command line : rally task report 4b88c6b5-6d04-41f1-b7bf-0530d1460380 --out /home/opnfv/functest/results/rally/opnfv-quotas.html
  2016-02-11 00:19:59,507 - run_rally - DEBUG - running command line : rally task results 4b88c6b5-6d04-41f1-b7bf-0530d1460380
  2016-02-11 00:20:00,092 - run_rally - DEBUG - saving json file
  2016-02-11 00:20:00,093 - run_rally - DEBUG - Push result into DB
  2016-02-11 00:20:06,245 - run_rally - DEBUG - <Response [200]>
  2016-02-11 00:20:06,246 - run_rally - INFO - Test scenario: "quotas" Failed.

  2016-02-11 00:20:06,246 - run_rally - INFO - Starting test scenario "requests" ...
  2016-02-11 00:20:06,246 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-requests.yaml
  2016-02-11 00:20:06,678 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '5333b06c-91ae-407b-8a20-a5c0adff52ee', 'service_list': ['requests'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}"
  2016-02-11 00:20:50,664 - run_rally - INFO -
   Preparing input task
   Task  f71c7e36-d999-42c9-affb-028670a5b248: started
  Task f71c7e36-d999-42c9-affb-028670a5b248: finished

  test scenario HttpRequests.check_random_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 5.458 | 5.495  | 5.881  | 5.973  | 6.065 | 5.612 | 100.0%  | 10    |
  | total                  | 5.458 | 5.495  | 5.881  | 5.973  | 6.065 | 5.612 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.8338370323
  Full duration: 19.1276738644

  test scenario HttpRequests.check_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 5.435 | 5.459  | 5.504  | 5.521  | 5.537 | 5.472 | 100.0%  | 10    |
  | total                  | 5.435 | 5.459  | 5.504  | 5.521  | 5.537 | 5.472 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.4511258602
  Full duration: 18.9822120667

  2016-02-11 00:20:50,664 - run_rally - DEBUG - task_id : f71c7e36-d999-42c9-affb-028670a5b248
  2016-02-11 00:20:50,664 - run_rally - DEBUG - running command line : rally task report f71c7e36-d999-42c9-affb-028670a5b248 --out /home/opnfv/functest/results/rally/opnfv-requests.html
  2016-02-11 00:20:51,254 - run_rally - DEBUG - running command line : rally task results f71c7e36-d999-42c9-affb-028670a5b248
  2016-02-11 00:20:51,824 - run_rally - DEBUG - saving json file
  2016-02-11 00:20:51,825 - run_rally - DEBUG - Push result into DB
  2016-02-11 00:20:57,506 - run_rally - DEBUG - <Response [200]>
  2016-02-11 00:20:57,507 - run_rally - INFO - Test scenario: "requests" OK.

  2016-02-11 00:20:57,507 - run_rally - INFO -

                       Rally Summary Report
  +===================+============+===============+===========+
  | Module            | Duration   | nb. Test Run  | Success   |
  +===================+============+===============+===========+
  | authenticate      | 00:17      | 10            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | glance            | 01:27      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | cinder            | 16:03      | 50            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | heat              | 06:25      | 32            | 92.31%    |
  +-------------------+------------+---------------+-----------+
  | keystone          | 01:08      | 29            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | neutron           | 04:45      | 31            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | nova              | 28:10      | 61            | 85.71%    |
  +-------------------+------------+---------------+-----------+
  | quotas            | 00:35      | 7             | 95.00%    |
  +-------------------+------------+---------------+-----------+
  | requests          | 00:38      | 2             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  +===================+============+===============+===========+
  | TOTAL:            | 00:59:33   | 229           | 97.00%    |
  +===================+============+===============+===========+

  2016-02-11 00:20:57,507 - run_rally - DEBUG - Pushing Rally summary into DB...
  2016-02-11 00:21:03,070 - run_rally - DEBUG - <Response [200]>
  2016-02-11 00:21:03,071 - run_rally - DEBUG - Deleting image 'functest-img' with ID 'a4efc793-1195-482b-9da6-87299b33d650'...
  2016-02-11 00:21:03,614 - run_rally - DEBUG - Deleting volume type 'volume_test'...
::
