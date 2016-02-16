.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for compass-os-onos-nofeature-ha
======================================================

Running test case: vping_ssh
-----------------------------

::
  FUNCTEST.info: Running vPing-SSH test...
  2016-02-12 19:05:40,043 - vPing_ssh- DEBUG - Creating image 'functest-vping' from '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img'...
  2016-02-12 19:05:41,030 - vPing_ssh- DEBUG - Image 'functest-vping' with ID=60da5df9-daa1-47de-816f-b9886ab67d71 created successfully.
  2016-02-12 19:05:41,076 - vPing_ssh- INFO - Creating neutron network vping-net...
  2016-02-12 19:05:41,354 - vPing_ssh- DEBUG - Network 'd45d7f71-10bf-45b1-9d86-94425f8fe21c' created successfully
  2016-02-12 19:05:41,355 - vPing_ssh- DEBUG - Creating Subnet....
  2016-02-12 19:05:41,634 - vPing_ssh- DEBUG - Subnet 'ad01de12-9720-40e8-b5ec-3e59c3a783d3' created successfully
  2016-02-12 19:05:41,634 - vPing_ssh- DEBUG - Creating Router...
  2016-02-12 19:05:41,687 - vPing_ssh- DEBUG - Router '7196b873-8686-4940-b169-7c004f5a48dc' created successfully
  2016-02-12 19:05:41,687 - vPing_ssh- DEBUG - Adding router to subnet...
  2016-02-12 19:05:41,922 - vPing_ssh- DEBUG - Interface added successfully.
  2016-02-12 19:05:41,922 - vPing_ssh- DEBUG - Adding gateway to router...
  2016-02-12 19:05:42,396 - vPing_ssh- DEBUG - Gateway added successfully.
  2016-02-12 19:05:42,741 - vPing_ssh- INFO - Flavor found 'm1.small'
  2016-02-12 19:05:43,450 - vPing_ssh- INFO - Creating security group  'vPing-sg'...
  2016-02-12 19:05:43,567 - vPing_ssh- DEBUG - Security group 'vPing-sg' with ID=93ac4559-82df-4b73-9eef-0a4d2a2d7b6e created successfully.
  2016-02-12 19:05:43,567 - vPing_ssh- DEBUG - Adding ICMP rules in security group 'vPing-sg'...
  2016-02-12 19:05:43,724 - vPing_ssh- DEBUG - Adding SSH rules in security group 'vPing-sg'...
  2016-02-12 19:05:44,008 - vPing_ssh- INFO - vPing Start Time:'2016-02-12 19:05:44'
  2016-02-12 19:05:44,008 - vPing_ssh- DEBUG - Creating port 'vping-port-1' with IP 192.168.130.30...
  2016-02-12 19:05:44,510 - vPing_ssh- INFO - Creating instance 'opnfv-vping-1' with IP 192.168.130.30...
  2016-02-12 19:05:44,510 - vPing_ssh- DEBUG - Configuration:
   name=opnfv-vping-1 
   flavor=<Flavor: m1.small> 
   image=60da5df9-daa1-47de-816f-b9886ab67d71 
   network=d45d7f71-10bf-45b1-9d86-94425f8fe21c 

  2016-02-12 19:05:46,752 - vPing_ssh- DEBUG - Status: BUILD
  2016-02-12 19:05:49,993 - vPing_ssh- DEBUG - Status: BUILD
  2016-02-12 19:05:53,271 - vPing_ssh- DEBUG - Status: ACTIVE
  2016-02-12 19:05:53,271 - vPing_ssh- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  2016-02-12 19:05:53,271 - vPing_ssh- DEBUG - Instance 'opnfv-vping-1' got 192.168.130.30
  2016-02-12 19:05:53,271 - vPing_ssh- INFO - Adding 'opnfv-vping-1' to security group 'vPing-sg'...
  2016-02-12 19:05:53,924 - vPing_ssh- DEBUG - Creating port 'vping-port-2' with IP 192.168.130.40...
  2016-02-12 19:05:54,241 - vPing_ssh- INFO - Creating instance 'opnfv-vping-2' with IP 192.168.130.40...
  2016-02-12 19:05:54,241 - vPing_ssh- DEBUG - Configuration:
   name=opnfv-vping-2 
   flavor=<Flavor: m1.small> 
   image=60da5df9-daa1-47de-816f-b9886ab67d71 
   network=d45d7f71-10bf-45b1-9d86-94425f8fe21c 

  2016-02-12 19:05:56,816 - vPing_ssh- DEBUG - Status: BUILD
  2016-02-12 19:06:00,048 - vPing_ssh- DEBUG - Status: ACTIVE
  2016-02-12 19:06:00,048 - vPing_ssh- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  2016-02-12 19:06:00,048 - vPing_ssh- INFO - Adding 'opnfv-vping-2' to security group 'vPing-sg'...
  2016-02-12 19:06:00,391 - vPing_ssh- INFO - Creating floating IP for VM 'opnfv-vping-2'...
  2016-02-12 19:06:00,625 - vPing_ssh- INFO - Floating IP created: '192.168.10.102'
  2016-02-12 19:06:00,625 - vPing_ssh- INFO - Associating floating ip: '192.168.10.102' to VM 'opnfv-vping-2' 
  2016-02-12 19:06:01,848 - vPing_ssh- INFO - Trying to establish SSH connection to 192.168.10.102...
  2016-02-12 19:06:01,850 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:06:07,856 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:06:13,864 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:06:19,872 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:06:25,879 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:06:31,884 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:06:37,892 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:06:43,899 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:06:49,906 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:06:55,913 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:07:01,920 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:07:07,925 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:07:13,933 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:07:19,940 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:07:25,948 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:07:31,955 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:07:37,962 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:07:43,964 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:07:49,971 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:07:55,978 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:08:01,983 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:08:07,990 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:08:13,997 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:08:20,004 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:08:26,012 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:08:32,019 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:08:38,026 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:08:44,032 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:08:50,039 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:08:56,047 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:09:02,050 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:09:08,058 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:09:14,065 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:09:20,072 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:09:26,080 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:09:32,087 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:09:38,094 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:09:44,101 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:09:50,109 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:09:56,116 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:10:02,123 - vPing_ssh- DEBUG - Waiting for 192.168.10.102...
  2016-02-12 19:10:08,257 - vPing_ssh- DEBUG - SSH connection established to 192.168.10.102.
  2016-02-12 19:10:09,335 - vPing_ssh- INFO - Waiting for ping...
  2016-02-12 19:10:10,344 - vPing_ssh- INFO - vPing detected!
  2016-02-12 19:10:10,344 - vPing_ssh- INFO - vPing duration:'266.3' s.
  2016-02-12 19:10:10,344 - vPing_ssh- INFO - Cleaning up...
  2016-02-12 19:10:10,344 - vPing_ssh- DEBUG - Deleting image...
  2016-02-12 19:10:11,945 - vPing_ssh- DEBUG - Deleting 'opnfv-vping-1'...
  2016-02-12 19:10:16,110 - vPing_ssh- DEBUG - Instance opnfv-vping-1 terminated.
  2016-02-12 19:10:16,350 - vPing_ssh- DEBUG - Deleting 'opnfv-vping-2'...
  2016-02-12 19:10:21,539 - vPing_ssh- DEBUG - Instance opnfv-vping-2 terminated.
  2016-02-12 19:10:21,539 - vPing_ssh- DEBUG - Deleting network 'vping-net'...
  2016-02-12 19:10:21,730 - vPing_ssh- DEBUG - Port '23ea5cbc-d075-4f75-8839-55877d217d09' removed successfully
  2016-02-12 19:10:21,903 - vPing_ssh- DEBUG - Port '1cbcac3d-fea8-4ca1-98d7-4c2b6d2a655b' removed successfully
  2016-02-12 19:10:22,121 - vPing_ssh- DEBUG - Interface removed successfully
  2016-02-12 19:10:22,341 - vPing_ssh- DEBUG - Router deleted successfully
  2016-02-12 19:10:22,569 - vPing_ssh- DEBUG - Subnet 'vping-subnet' deleted successfully
  2016-02-12 19:10:22,801 - vPing_ssh- DEBUG - Network 'vping-net' deleted successfully
  2016-02-12 19:10:22,851 - vPing_ssh- DEBUG - Security group '93ac4559-82df-4b73-9eef-0a4d2a2d7b6e' deleted successfully
  2016-02-12 19:10:22,851 - vPing_ssh- INFO - vPing OK
  2016-02-12 19:10:22,851 - vPing_ssh- DEBUG - Pushing result into DB...
  2016-02-12 19:10:23,533 - vPing_ssh- DEBUG - <Response [200]>
::

Running test case: tempest
--------------------------
::
  FUNCTEST.info: Running Tempest tests...
  2016-02-12 19:10:23,939 - run_tempest - INFO - Creating tenant and user for Tempest suite
  2016-02-12 19:10:24,296 - run_tempest - DEBUG - Generating tempest.conf file...
  2016-02-12 19:10:24,296 - run_tempest - DEBUG - Executing command : rally verify genconfig
  2016-02-12 19:10:29,268 - run_tempest - DEBUG - 2016-02-12 19:10:24.832 23856 INFO rally.verification.tempest.tempest [-] Tempest is not configured.
  2016-02-12 19:10:24.832 23856 INFO rally.verification.tempest.tempest [-] Starting: Creating configuration file for Tempest.
  2016-02-12 19:10:29.226 23856 INFO rally.verification.tempest.tempest [-] Completed: Creating configuration file for Tempest.

  2016-02-12 19:10:29,268 - run_tempest - DEBUG - Resolving deployment UUID...
  2016-02-12 19:10:29,837 - run_tempest - DEBUG - Finding tempest.conf file...
  2016-02-12 19:10:29,837 - run_tempest - DEBUG -   Updating fixed_network_name...
  2016-02-12 19:10:30,116 - run_tempest - DEBUG - Executing command : crudini --set /home/opnfv/.rally/tempest/for-deployment-ea712793-ba5c-425c-adcb-f830168264e4/tempest.conf compute fixed_network_name functest-net
  2016-02-12 19:10:30,146 - run_tempest - DEBUG -   Updating non-admin credentials...
  2016-02-12 19:10:30,146 - run_tempest - DEBUG - Executing command : crudini --set /home/opnfv/.rally/tempest/for-deployment-ea712793-ba5c-425c-adcb-f830168264e4/tempest.conf identity tenant_name tempest
  2016-02-12 19:10:30,182 - run_tempest - DEBUG - Executing command : crudini --set /home/opnfv/.rally/tempest/for-deployment-ea712793-ba5c-425c-adcb-f830168264e4/tempest.conf identity username tempest
  2016-02-12 19:10:30,210 - run_tempest - DEBUG - Executing command : crudini --set /home/opnfv/.rally/tempest/for-deployment-ea712793-ba5c-425c-adcb-f830168264e4/tempest.conf identity password tempest
  2016-02-12 19:10:30,242 - run_tempest - DEBUG - Executing command : sed -i 's/.*ssh_user_regex.*/ssh_user_regex = [["^.*[Cc]irros.*$", "cirros"], ["^.*[Tt]est[VvMm].*$", "cirros"], ["^.*rally_verify.*$", "cirros"]]/' /home/opnfv/.rally/tempest/for-deployment-ea712793-ba5c-425c-adcb-f830168264e4/tempest.conf
  2016-02-12 19:10:30,247 - run_tempest - INFO - Starting Tempest test suite: '--tests-file /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/custom_tests/test_list.txt'.
  2016-02-12 19:10:30,247 - run_tempest - DEBUG - Executing command : rally verify start --tests-file /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/custom_tests/test_list.txt
  Total results of verification:

  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | UUID                                 | Deployment UUID                      | Set name | Tests | Failures | Created at                 | Status   |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | 818d3bed-1209-4161-a009-d67b5d4b1a5b | ea712793-ba5c-425c-adcb-f830168264e4 |          | 210   | 11       | 2016-02-12 19:10:30.775632 | finished |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+

  Tests:

  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | name                                                                                                                                     | time      | status  |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.38798   | success |
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.06897   | success |
  | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 8.66954   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 13.05485  | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 8.17642   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.06398   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.05311   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.06698   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.12086   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.07949   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.06849   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.06627   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.06681   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.05412   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.17846   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.07675   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.10191   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.06990   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 0.15930   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 0.10904   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.10306   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 0.32255   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 0.56048   | success |
  | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 1.42311   | success |
  | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 7.28776   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 337.23588 | fail    |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.13741   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.23680   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 316.30761 | fail    |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.00084   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 319.97246 | fail    |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.12007   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.22505   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 322.15364 | fail    |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.00083   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.06292   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 3.00411   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.20017   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.19477   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.14907   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.22243   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.15516   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.07558   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.06317   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.05484   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.06197   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.05894   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.19611   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00056   | skip    |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.13860   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.05872   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.01695   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.07035   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.21809   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.01841   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.01089   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.02861   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.05638   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.05798   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.30626   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.01272   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.06264   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.00050   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 5.67273   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 9.07361   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 310.89730 | fail    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.39781   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 327.97278 | fail    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 13.09878  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 19.25586  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 6.97419   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.05925   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.13748   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.48860   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.51186   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.27618   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 1.44356   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.56153   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.61749   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 2.23577   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 14.27026  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 13.23885  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 8.66286   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 5.49453   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 0.50988   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 0.58228   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 0.73942   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 1.62280   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 1.40931   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 1.41580   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 0.50300   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 0.39170   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 0.41128   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.48554   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 0.56803   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 0.50901   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 0.58968   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 0.47930   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.34199   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 0.57965   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.41263   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 1.07127   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 0.34228   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 0.43989   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 0.30970   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.10400   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.01156   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 0.08172   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.02068   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 0.54532   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.18789   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.12172   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.05132   | success |
  | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 339.95221 | fail    |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.07032   | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.06840   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.13918   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.01148   | success |
  | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.22616   | success |
  | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.11317   | success |
  | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.14866   | success |
  | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.02954   | success |
  | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 0.43616   | success |
  | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.19924   | success |
  | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 0.82300   | success |
  | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.11213   | success |
  | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.08933   | success |
  | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.15558   | success |
  | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.14961   | success |
  | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 0.76717   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.02573   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.01676   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.02202   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.02597   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.01541   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.01451   | success |
  | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.05174   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 0.29017   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 0.42424   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 0.68054   | success |
  | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 0.47508   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 0.71112   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 0.73746   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 0.67128   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 1.08614   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 3.40037   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 0.58717   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 1.30633   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 1.63105   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 1.03824   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.20400   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.08155   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.15349   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.02530   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.05855   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 1.25511   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.10543   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.06155   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.12005   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.03140   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.03071   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 1.80504   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 1.23140   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 0.78307   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.04927   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.05300   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 1.16549   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 1.18066   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 0.77082   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.06872   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.05677   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 2.80443   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 1.63531   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 1.35836   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 1.03564   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 2.80813   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 1.34980   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 1.44477   | success |
  | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 0.84429   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 0.43816   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 0.56186   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.02541   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 0.42898   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 0.57004   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.03255   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.37517   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 5.10610   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.02256   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 0.72815   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.37456   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.61271   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.69521   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.68138   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.39513   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 2.32413   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.02259   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 0.75379   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 1.52753   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 2.53395   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 2.66529   | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 11.60002  | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 11.02724  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 10.53925  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 10.81895  | success |
  | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.13870   | success |
  | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.13807   | success |
  | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 363.10201 | fail    |
  | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 75.16093  | fail    |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 507.93579 | fail    |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 507.54584 | fail    |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  2016-02-12 19:28:37,433 - run_tempest - DEBUG - Executing command : rally verify list
  2016-02-12 19:28:37,991 - run_tempest - INFO - Results: {'timestart': '2016-02-1219:10:30.775632', 'duration': 1086, 'tests': 210, 'failures': 11}
  2016-02-12 19:28:37,991 - run_tempest - DEBUG - Push result into DB
  2016-02-12 19:28:37,992 - run_tempest - INFO - Pushing results to DB: 'http://testresults.opnfv.org/testapi/results'.
  2016-02-12 19:28:38,675 - run_tempest - DEBUG - <Response [200]>
  2016-02-12 19:28:38,675 - run_tempest - INFO - Deleting tenant and user for Tempest suite)
  None
::

Running test case: onos
-----------------------

::
  FUNCTEST.info: Running ONOS test case...
  2016-02-12 19:28:41,069 - onos- DEBUG - Download Onos Teston codes https://github.com/sunyulin/OnosSystemTest.git
  Cloning into '/home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest'...
  2016-02-12 19:28:53,296 - onos- DEBUG - ONOS IP is 192.168.10.51
  2016-02-12 19:28:53,296 - onos- DEBUG - Run script FUNCvirNetNB
  2016-02-12 19:28:53,399 - FUNCvirNetNB - INFO - Creating component Handle: ONOSrest

                                  +----------------+
  ------------------------------ { Script And Files }  ------------------------------
                                  +----------------+

  	Script Log File : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNB_12_Feb_2016_19_28_53/FUNCvirNetNB_12_Feb_2016_19_28_53.log
  	Report Log File : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNB_12_Feb_2016_19_28_53/FUNCvirNetNB_12_Feb_2016_19_28_53.rpt
  	ONOSrest Session Log : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNB_12_Feb_2016_19_28_53/ONOSrest.session
  	Test Script :/home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/Tests/FUNCvirNetNB.py
  	Test Params : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/Tests/FUNCvirNetNB.params
  	Topology : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/Tests/FUNCvirNetNB.topo
                                +------------------+
  ---------------------------  { Script Exec Params }  ---------------------------
                                +------------------+

  	'MININET': 
  	'switch': '7'
  	 'links': '20'

  	 'GIT': 
  	'pull': 'False'
  	 'branch': 'master'

  	 'HTTP': 
  	'path': '/onos/vtn/'
  	 'port': '8181'

  	 'CTRL': 
  	'ip1': 'OC1'
  	 'port1': '6633'

  	 'testcases': '2
  	3
  	4
  	5
  	6
  	7
  	8
  	9
  	10'
  	 'SLEEP': 
  	'startup': '15'

  	 'ENV': 
  	'cellApps': 'drivers
  	openflow
  	proxyarp
  	mobility'
  	 'cellName': 'singlenode'

                                 +---------------+
  ----------------------------- { Components Used }  -----------------------------
                                 +---------------+
  	ONOSrest

                                +--------+
  ---------------------------- { Topology }  ----------------------------
                                +--------+

  	'ONOSrest': 
  	'connect_order': '4'
  	 'host': 'OC1'
  	 'user': 'root'
  	 'COMPONENTS': ''
  	 'password': 'r00tme'
  	 'type': 'OnosRestDriver'

  ------------------------------------------------------------

  ******************************
   CASE INIT 
  ******************************

  ['ONOSrest']

  ******************************
   Result summary for Testcase2
  ******************************

  [2016-02-12 19:28:53.480315] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Network Post
  [2016-02-12 19:28:53.480532] [FUNCvirNetNB] [STEP]  2.1: Generate Post Data
  [2016-02-12 19:28:53.480839] [FUNCvirNetNB] [STEP]  2.2: Post Data via HTTP
  [2016-02-12 19:28:53.673391] [FUNCvirNetNB] [STEP]  2.3: Get Data via HTTP
  [2016-02-12 19:28:53.681088] [FUNCvirNetNB] [STEP]  2.4: Compare Send Id and Get Id

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase3
  ******************************

  [2016-02-12 19:28:53.688351] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Network Update
  [2016-02-12 19:28:53.688588] [FUNCvirNetNB] [STEP]  3.1: Generate Post Data
  [2016-02-12 19:28:53.688953] [FUNCvirNetNB] [STEP]  3.2: Post Data via HTTP
  [2016-02-12 19:28:53.695867] [FUNCvirNetNB] [STEP]  3.3: Update Data via HTTP
  [2016-02-12 19:28:53.704924] [FUNCvirNetNB] [STEP]  3.4: Get Data via HTTP
  [2016-02-12 19:28:53.709109] [FUNCvirNetNB] [STEP]  3.5: Compare Update data.

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase4
  ******************************

  [2016-02-12 19:28:53.720293] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Network Delete
  [2016-02-12 19:28:53.720510] [FUNCvirNetNB] [STEP]  4.1: Generate Post Data
  [2016-02-12 19:28:53.720819] [FUNCvirNetNB] [STEP]  4.2: Post Data via HTTP
  [2016-02-12 19:28:53.726943] [FUNCvirNetNB] [STEP]  4.3: Delete Data via HTTP
  [2016-02-12 19:28:53.731614] [FUNCvirNetNB] [STEP]  4.4: Get Data is NULL

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase5
  ******************************

  [2016-02-12 19:28:58.748088] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Subnet Post
  [2016-02-12 19:28:58.748345] [FUNCvirNetNB] [STEP]  5.1: Generate Post Data
  [2016-02-12 19:28:58.748742] [FUNCvirNetNB] [STEP]  5.2: Post Network Data via HTTP(Post Subnet need post network)
  [2016-02-12 19:28:58.760851] [FUNCvirNetNB] [STEP]  5.3: Post Subnet Data via HTTP
  [2016-02-12 19:28:58.797496] [FUNCvirNetNB] [STEP]  5.4: Get Subnet Data via HTTP
  [2016-02-12 19:28:58.806663] [FUNCvirNetNB] [STEP]  5.5: Compare Post Subnet Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase6
  ******************************

  [2016-02-12 19:28:58.813611] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Subnet Update
  [2016-02-12 19:28:58.813885] [FUNCvirNetNB] [STEP]  6.1: Generate Post Data
  [2016-02-12 19:28:58.814422] [FUNCvirNetNB] [STEP]  6.2: Post Network Data via HTTP(Post Subnet need post network)
  [2016-02-12 19:28:58.821242] [FUNCvirNetNB] [STEP]  6.3: Post Subnet Data via HTTP
  [2016-02-12 19:28:58.827664] [FUNCvirNetNB] [STEP]  6.4: Update Subnet Data via HTTP
  [2016-02-12 19:28:58.855303] [FUNCvirNetNB] [STEP]  6.5: Get Subnet Data via HTTP
  [2016-02-12 19:28:58.859648] [FUNCvirNetNB] [STEP]  6.6: Compare Subnet Data
  [2016-02-12 19:28:58.859965] [FUNCvirNetNB] [STEP]  6.7: Delete Subnet via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase7
  ******************************

  [2016-02-12 19:28:58.865645] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Subnet Delete
  [2016-02-12 19:28:58.865877] [FUNCvirNetNB] [STEP]  7.1: Generate Post Data
  [2016-02-12 19:28:58.866330] [FUNCvirNetNB] [STEP]  7.2: Post Network Data via HTTP(Post Subnet need post network)
  [2016-02-12 19:28:58.874618] [FUNCvirNetNB] [STEP]  7.3: Post Subnet Data via HTTP
  [2016-02-12 19:28:58.880254] [FUNCvirNetNB] [STEP]  7.4: Delete Subnet Data via HTTP
  [2016-02-12 19:28:58.884603] [FUNCvirNetNB] [STEP]  7.5: Get Subnet Data is NULL

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase8
  ******************************

  [2016-02-12 19:29:03.902255] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Port Post
  [2016-02-12 19:29:03.902540] [FUNCvirNetNB] [STEP]  8.1: Generate Post Data
  [2016-02-12 19:29:03.903021] [FUNCvirNetNB] [STEP]  8.2: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:03.914466] [FUNCvirNetNB] [STEP]  8.3: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:03.923591] [FUNCvirNetNB] [STEP]  8.4: Post Port Data via HTTP
  [2016-02-12 19:29:03.949876] [FUNCvirNetNB] [STEP]  8.5: Get Port Data via HTTP
  [2016-02-12 19:29:03.957954] [FUNCvirNetNB] [STEP]  8.6: Compare Post Port Data
  [2016-02-12 19:29:03.958632] [FUNCvirNetNB] [STEP]  8.7: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase9
  ******************************

  [2016-02-12 19:29:03.964924] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Port Update
  [2016-02-12 19:29:03.965218] [FUNCvirNetNB] [STEP]  9.1: Generate Post Data
  [2016-02-12 19:29:03.965870] [FUNCvirNetNB] [STEP]  9.2: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:03.971829] [FUNCvirNetNB] [STEP]  9.3: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:03.978163] [FUNCvirNetNB] [STEP]  9.4: Post Port Data via HTTP
  [2016-02-12 19:29:03.983378] [FUNCvirNetNB] [STEP]  9.5: Update Port Data via HTTP
  [2016-02-12 19:29:03.989288] [FUNCvirNetNB] [STEP]  9.6: Get Port Data via HTTP
  [2016-02-12 19:29:03.993426] [FUNCvirNetNB] [STEP]  9.7: Compare Update Port Data
  [2016-02-12 19:29:03.993978] [FUNCvirNetNB] [STEP]  9.8: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase10
  ******************************

  [2016-02-12 19:29:04.000036] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Port Delete
  [2016-02-12 19:29:04.000338] [FUNCvirNetNB] [STEP]  10.1: Generate Post Data
  [2016-02-12 19:29:04.000802] [FUNCvirNetNB] [STEP]  10.2: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:04.005815] [FUNCvirNetNB] [STEP]  10.3: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:04.011511] [FUNCvirNetNB] [STEP]  10.4: Post Port Data via HTTP
  [2016-02-12 19:29:04.016942] [FUNCvirNetNB] [STEP]  10.5: Delete Port Data via HTTP
  [2016-02-12 19:29:04.023147] [FUNCvirNetNB] [STEP]  10.6: Get Port Data is NULL
  [2016-02-12 19:29:09.043011] [FUNCvirNetNB] [STEP]  10.7: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  *************************************
  	Test Execution Summary

  ************************************* 

   Test Start           : 12 Feb 2016 19:28:53
   Test End             : 12 Feb 2016 19:29:09
   Execution Time       : 0:00:15.653141
   Total tests planned  : 9
   Total tests RUN      : 9
   Total Pass           : 9
   Total Fail           : 0
   Total No Result      : 0
   Success Percentage   : 100%
   Execution Result     : 100%
  Disconnecting from ONOSrest: <drivers.common.api.controller.onosrestdriver.OnosRestDriver object at 0x7f055d67ea90>
  2016-02-12 19:29:09,098 - onos- DEBUG - Run script FUNCvirNetNBL3
  2016-02-12 19:29:09,185 - FUNCvirNetNBL3 - INFO - Creating component Handle: ONOSrest

                                  +----------------+
  ------------------------------ { Script And Files }  ------------------------------
                                  +----------------+

  	Script Log File : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNBL3_12_Feb_2016_19_29_09/FUNCvirNetNBL3_12_Feb_2016_19_29_09.log
  	Report Log File : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNBL3_12_Feb_2016_19_29_09/FUNCvirNetNBL3_12_Feb_2016_19_29_09.rpt
  	ONOSrest Session Log : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNBL3_12_Feb_2016_19_29_09/ONOSrest.session
  	Test Script :/home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/Tests/FUNCvirNetNBL3.py
  	Test Params : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/Tests/FUNCvirNetNBL3.params
  	Topology : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/Tests/FUNCvirNetNBL3.topo
                                +------------------+
  ---------------------------  { Script Exec Params }  ---------------------------
                                +------------------+

  	'MININET': 
  	'switch': '7'
  	 'links': '20'

  	 'GIT': 
  	'pull': 'False'
  	 'branch': 'master'

  	 'HTTP': 
  	'path': '/onos/vtn/'
  	 'port': '8181'

  	 'CTRL': 
  	'ip1': 'OC1'
  	 'port1': '6653'

  	 'testcases': '2
  	3
  	4
  	5
  	6
  	7
  	8
  	9
  	10
  	11
  	12'
  	 'SLEEP': 
  	'startup': '15'

  	 'ENV': 
  	'cellApps': 'drivers
  	openflow
  	proxyarp
  	mobility'
  	 'cellName': 'singlenode'

                                 +---------------+
  ----------------------------- { Components Used }  -----------------------------
                                 +---------------+
  	ONOSrest

                                +--------+
  ---------------------------- { Topology }  ----------------------------
                                +--------+

  	'ONOSrest': 
  	'connect_order': '4'
  	 'host': 'OC1'
  	 'user': 'root'
  	 'COMPONENTS': ''
  	 'password': 'root'
  	 'type': 'OnosRestDriver'

  ------------------------------------------------------------

  ******************************
   CASE INIT 
  ******************************

  ['ONOSrest']

  ******************************
   Result summary for Testcase2
  ******************************

  [2016-02-12 19:29:09.253891] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Router Post
  [2016-02-12 19:29:09.254426] [FUNCvirNetNBL3] [STEP]  2.1: Post Network Data via HTTP(Post Router need post network)
  [2016-02-12 19:29:09.277464] [FUNCvirNetNBL3] [STEP]  2.2: Post Router Data via HTTP
  [2016-02-12 19:29:09.286749] [FUNCvirNetNBL3] [STEP]  2.3: Get Router Data via HTTP
  [2016-02-12 19:29:09.292011] [FUNCvirNetNBL3] [STEP]  2.4: Compare Post Router Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase3
  ******************************

  [2016-02-12 19:29:09.304490] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Router Update
  [2016-02-12 19:29:09.305193] [FUNCvirNetNBL3] [STEP]  3.1: Post Network Data via HTTP(Post Router need post network)
  [2016-02-12 19:29:09.310364] [FUNCvirNetNBL3] [STEP]  3.2: Post Router Data via HTTP
  [2016-02-12 19:29:09.314733] [FUNCvirNetNBL3] [STEP]  3.3: Update Router Data via HTTP
  [2016-02-12 19:29:09.318528] [FUNCvirNetNBL3] [STEP]  3.4: Get Router Data via HTTP
  [2016-02-12 19:29:09.321779] [FUNCvirNetNBL3] [STEP]  3.5: Compare Router Data
  [2016-02-12 19:29:09.322160] [FUNCvirNetNBL3] [STEP]  3.6: Delete Router via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase4
  ******************************

  [2016-02-12 19:29:09.326335] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Router Delete
  [2016-02-12 19:29:09.326694] [FUNCvirNetNBL3] [STEP]  4.1: Post Network Data via HTTP(Post Router need post network)
  [2016-02-12 19:29:09.331266] [FUNCvirNetNBL3] [STEP]  4.2: Post Router Data via HTTP
  [2016-02-12 19:29:09.334749] [FUNCvirNetNBL3] [STEP]  4.3: Delete Router Data via HTTP
  [2016-02-12 19:29:09.338576] [FUNCvirNetNBL3] [STEP]  4.4: Get Router Data is NULL
  Verify the Router status

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase5
  ******************************

  [2016-02-12 19:29:14.353712] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - RouterInterface Post
  [2016-02-12 19:29:14.354333] [FUNCvirNetNBL3] [STEP]  5.1: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:14.362760] [FUNCvirNetNBL3] [STEP]  5.2: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:14.370550] [FUNCvirNetNBL3] [STEP]  5.3: Post Port Data via HTTP
  [2016-02-12 19:29:14.377722] [FUNCvirNetNBL3] [STEP]  5.4: Post Router Data via HTTP
  [2016-02-12 19:29:14.382048] [FUNCvirNetNBL3] [STEP]  5.5: Put RouterInterface Data via HTTP
  [2016-02-12 19:29:14.390960] [FUNCvirNetNBL3] [STEP]  5.6: Get RouterInterface Data via HTTP
  [2016-02-12 19:29:14.396121] [FUNCvirNetNBL3] [STEP]  5.7: Compare Post Port Data
  [2016-02-12 19:29:14.396706] [FUNCvirNetNBL3] [STEP]  5.8: Del RouterInterface Data via HTTP
  [2016-02-12 19:29:14.402504] [FUNCvirNetNBL3] [STEP]  5.9: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase6
  ******************************

  [2016-02-12 19:29:14.414994] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - RouterInterface Delete
  [2016-02-12 19:29:14.415949] [FUNCvirNetNBL3] [STEP]  6.1: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:14.423498] [FUNCvirNetNBL3] [STEP]  6.2: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:14.429906] [FUNCvirNetNBL3] [STEP]  6.3: Post Port Data via HTTP
  [2016-02-12 19:29:14.435831] [FUNCvirNetNBL3] [STEP]  6.4: Post Router Data via HTTP
  [2016-02-12 19:29:14.440530] [FUNCvirNetNBL3] [STEP]  6.5: Post RouterInterface Data via HTTP
  [2016-02-12 19:29:14.446879] [FUNCvirNetNBL3] [STEP]  6.6: Del RouterInterface Data via HTTP
  [2016-02-12 19:29:14.451643] [FUNCvirNetNBL3] [STEP]  6.7: Delete Port Data via HTTP
  [2016-02-12 19:29:14.456442] [FUNCvirNetNBL3] [STEP]  6.8: Get Port Data is NULL
  [2016-02-12 19:29:19.470955] [FUNCvirNetNBL3] [STEP]  6.9: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase7
  ******************************

  [2016-02-12 19:29:19.490054] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - FloatingIp Post
  [2016-02-12 19:29:19.491154] [FUNCvirNetNBL3] [STEP]  7.1: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:19.498986] [FUNCvirNetNBL3] [STEP]  7.2: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:19.506140] [FUNCvirNetNBL3] [STEP]  7.3: Post Port Data via HTTP
  [2016-02-12 19:29:19.513307] [FUNCvirNetNBL3] [STEP]  7.4: Post Router Data via HTTP
  [2016-02-12 19:29:19.518189] [FUNCvirNetNBL3] [STEP]  7.5: Get Port Data via HTTP
  [2016-02-12 19:29:19.524948] [FUNCvirNetNBL3] [STEP]  7.6: Post FloatingIp Data via HTTP
  [2016-02-12 19:29:19.533344] [FUNCvirNetNBL3] [STEP]  7.7: Get Port Data via HTTP
  [2016-02-12 19:29:19.539749] [FUNCvirNetNBL3] [STEP]  7.8: Get FloatingIp Data via HTTP
  [2016-02-12 19:29:19.545027] [FUNCvirNetNBL3] [STEP]  7.9: Get FloatingIp Data via HTTP
  [2016-02-12 19:29:19.549383] [FUNCvirNetNBL3] [STEP]  7.10: Compare Post FloatingIp Data
  [2016-02-12 19:29:19.549818] [FUNCvirNetNBL3] [STEP]  7.11: Post FloatingIp Clean Data via HTTP
  [2016-02-12 19:29:19.554862] [FUNCvirNetNBL3] [STEP]  7.12: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase8
  ******************************

  [2016-02-12 19:29:19.570354] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - FloatingIp Update
  [2016-02-12 19:29:19.571070] [FUNCvirNetNBL3] [STEP]  8.1: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:19.576537] [FUNCvirNetNBL3] [STEP]  8.2: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:19.581859] [FUNCvirNetNBL3] [STEP]  8.3: Post Port Data via HTTP
  [2016-02-12 19:29:19.586976] [FUNCvirNetNBL3] [STEP]  8.4: Post Router Data via HTTP
  [2016-02-12 19:29:19.590621] [FUNCvirNetNBL3] [STEP]  8.5: Post FloatingIp Data via HTTP
  [2016-02-12 19:29:19.594786] [FUNCvirNetNBL3] [STEP]  8.6: Post Delete Data via HTTP
  [2016-02-12 19:29:19.598961] [FUNCvirNetNBL3] [STEP]  8.7: Post NewPort Data via HTTP
  [2016-02-12 19:29:19.604343] [FUNCvirNetNBL3] [STEP]  8.8: Post NewFloatingIp Data via HTTP
  [2016-02-12 19:29:19.608924] [FUNCvirNetNBL3] [STEP]  8.9: Get NewFloatingIp Data via HTTP
  [2016-02-12 19:29:19.612110] [FUNCvirNetNBL3] [STEP]  8.10: Compare Post FloatingIp Data
  [2016-02-12 19:29:19.612553] [FUNCvirNetNBL3] [STEP]  8.11: Post FloatingIp Clean Data via HTTP
  [2016-02-12 19:29:19.616988] [FUNCvirNetNBL3] [STEP]  8.12: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase9
  ******************************

  [2016-02-12 19:29:19.628499] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - FloatingIp Delete
  [2016-02-12 19:29:19.629101] [FUNCvirNetNBL3] [STEP]  9.1: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:19.633446] [FUNCvirNetNBL3] [STEP]  9.2: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:19.639341] [FUNCvirNetNBL3] [STEP]  9.3: Post Port Data via HTTP
  [2016-02-12 19:29:19.644221] [FUNCvirNetNBL3] [STEP]  9.4: Post Router Data via HTTP
  [2016-02-12 19:29:19.647812] [FUNCvirNetNBL3] [STEP]  9.5: Post FloatingIp Data via HTTP
  [2016-02-12 19:29:19.652083] [FUNCvirNetNBL3] [STEP]  9.6: Post FloatingIp Clean Data via HTTP
  [2016-02-12 19:29:19.658294] [FUNCvirNetNBL3] [STEP]  9.7: Get FloatingIp Data is NULL
  [2016-02-12 19:29:24.671790] [FUNCvirNetNBL3] [STEP]  9.8: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase10
  ******************************

  [2016-02-12 19:29:24.687368] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Gateway Post
  [2016-02-12 19:29:24.687942] [FUNCvirNetNBL3] [STEP]  10.1: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:24.694589] [FUNCvirNetNBL3] [STEP]  10.2: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:24.702207] [FUNCvirNetNBL3] [STEP]  10.3: Post Port Data via HTTP
  [2016-02-12 19:29:24.708359] [FUNCvirNetNBL3] [STEP]  10.4: Post Router Data via HTTP
  [2016-02-12 19:29:24.714159] [FUNCvirNetNBL3] [STEP]  10.5: Get Gateway Data via HTTP
  [2016-02-12 19:29:24.719097] [FUNCvirNetNBL3] [STEP]  10.6: Compare Post Gateway Data
  [2016-02-12 19:29:24.719529] [FUNCvirNetNBL3] [STEP]  10.7: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase11
  ******************************

  [2016-02-12 19:29:24.729627] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Gateway Update
  [2016-02-12 19:29:24.730471] [FUNCvirNetNBL3] [STEP]  11.1: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:24.735199] [FUNCvirNetNBL3] [STEP]  11.2: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:24.740390] [FUNCvirNetNBL3] [STEP]  11.3: Post Port Data via HTTP
  [2016-02-12 19:29:24.744907] [FUNCvirNetNBL3] [STEP]  11.4: Post Router Data via HTTP
  [2016-02-12 19:29:24.748738] [FUNCvirNetNBL3] [STEP]  11.5: Post New Router Data via HTTP
  [2016-02-12 19:29:24.753672] [FUNCvirNetNBL3] [STEP]  11.6: Get Gateway Data via HTTP
  [2016-02-12 19:29:24.756529] [FUNCvirNetNBL3] [STEP]  11.7: Compare Post Gateway Data
  [2016-02-12 19:29:24.756959] [FUNCvirNetNBL3] [STEP]  11.8: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  ******************************
   Result summary for Testcase12
  ******************************

  [2016-02-12 19:29:24.765973] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Gateway Delete
  [2016-02-12 19:29:24.766668] [FUNCvirNetNBL3] [STEP]  12.1: Post Network Data via HTTP(Post port need post network)
  [2016-02-12 19:29:24.771315] [FUNCvirNetNBL3] [STEP]  12.2: Post Subnet Data via HTTP(Post port need post subnet)
  [2016-02-12 19:29:24.776222] [FUNCvirNetNBL3] [STEP]  12.3: Post Port Data via HTTP
  [2016-02-12 19:29:24.781123] [FUNCvirNetNBL3] [STEP]  12.4: Post Router Data via HTTP
  [2016-02-12 19:29:24.787724] [FUNCvirNetNBL3] [STEP]  12.5: Post Del Gateway Data via HTTP
  [2016-02-12 19:29:24.791889] [FUNCvirNetNBL3] [STEP]  12.6: Get Gateway Data via HTTP
  [2016-02-12 19:29:24.794703] [FUNCvirNetNBL3] [STEP]  12.7: If Gateway Data is NULL
  [2016-02-12 19:29:29.800513] [FUNCvirNetNBL3] [STEP]  12.8: Clean Data via HTTP

  *****************************
   Result: Pass 
  *****************************

  *************************************
  	Test Execution Summary

  ************************************* 

   Test Start           : 12 Feb 2016 19:29:09
   Test End             : 12 Feb 2016 19:29:29
   Execution Time       : 0:00:20.634178
   Total tests planned  : 11
   Total tests RUN      : 11
   Total Pass           : 11
   Total Fail           : 0
   Total No Result      : 0
   Success Percentage   : 100%
   Execution Result     : 100%
  Disconnecting from ONOSrest: <drivers.common.api.controller.onosrestdriver.OnosRestDriver object at 0x7f4d848b7b10>
  2016-02-12 19:29:29,836 - onos- DEBUG - Push result into DB
  2016-02-12 19:29:31,842 - onos- DEBUG - Testcases Success
  2016-02-12 19:29:32,716 - onos- DEBUG - <Response [200]>
  2016-02-12 19:29:34,774 - onos- DEBUG - Clean ONOS Teston
::

Running test case: rally
------------------------

::
  FUNCTEST.info: Running Rally benchmark suite...
  2016-02-12 19:29:35,590 - run_rally - DEBUG - Volume type 'volume_test' created succesfully...
  2016-02-12 19:29:35,715 - run_rally - DEBUG - Creating image 'functest-img' from '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img'...
  2016-02-12 19:29:36,257 - run_rally - DEBUG - Image 'functest-img' with ID '0c74bd9e-0ac2-4332-8e03-e00c266752ad' created succesfully .
  2016-02-12 19:29:36,257 - run_rally - INFO - Starting test scenario "authenticate" ...
  2016-02-12 19:29:36,257 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-authenticate.yaml
  2016-02-12 19:29:36,561 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': 'daf5424b-3efa-4514-8ece-af4597ba0ad2', 'service_list': ['authenticate'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'live_migration': False, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-12 19:30:03,978 - run_rally - INFO - 
   Preparing input task
   Task  12233c47-6a06-4a69-9fda-761eae3e8dbd: started
  Task 12233c47-6a06-4a69-9fda-761eae3e8dbd: finished

  test scenario Authenticate.validate_glance
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_glance     | 0.119 | 0.14   | 0.174  | 0.193  | 0.213 | 0.148 | 100.0%  | 10    |
  | authenticate.validate_glance (2) | 0.038 | 0.043  | 0.049  | 0.05   | 0.052 | 0.044 | 100.0%  | 10    |
  | total                            | 0.239 | 0.27   | 0.287  | 0.324  | 0.36  | 0.273 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.824501037598
  Full duration: 3.16589784622

  test scenario Authenticate.keystone
  +-----------------------------------------------------------------------------+
  |                            Response Times (sec)                             |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | total  | 0.065 | 0.075  | 0.13   | 0.137  | 0.144 | 0.085 | 100.0%  | 10    |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.295313119888
  Full duration: 2.90179300308

  test scenario Authenticate.validate_heat
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_heat     | 0.11  | 0.135  | 0.274  | 0.305  | 0.336 | 0.165 | 100.0%  | 10    |
  | authenticate.validate_heat (2) | 0.022 | 0.036  | 0.112  | 0.26   | 0.407 | 0.081 | 100.0%  | 10    |
  | total                          | 0.212 | 0.258  | 0.484  | 0.567  | 0.649 | 0.324 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.13559103012
  Full duration: 3.52405309677

  test scenario Authenticate.validate_nova
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_nova     | 0.104 | 0.133  | 0.155  | 0.159  | 0.163 | 0.134 | 100.0%  | 10    |
  | authenticate.validate_nova (2) | 0.023 | 0.043  | 0.054  | 0.057  | 0.06  | 0.041 | 100.0%  | 10    |
  | total                          | 0.212 | 0.264  | 0.271  | 0.273  | 0.275 | 0.251 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.771644115448
  Full duration: 3.15462398529

  test scenario Authenticate.validate_cinder
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_cinder     | 0.09  | 0.112  | 0.167  | 0.19   | 0.214 | 0.125 | 100.0%  | 10    |
  | authenticate.validate_cinder (2) | 0.013 | 0.096  | 0.137  | 0.264  | 0.391 | 0.107 | 100.0%  | 10    |
  | total                            | 0.188 | 0.296  | 0.465  | 0.536  | 0.606 | 0.321 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.861793994904
  Full duration: 3.20478820801

  test scenario Authenticate.validate_neutron
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_neutron     | 0.118 | 0.147  | 0.172  | 0.173  | 0.174 | 0.146 | 100.0%  | 10    |
  | authenticate.validate_neutron (2) | 0.03  | 0.081  | 0.091  | 0.104  | 0.118 | 0.07  | 100.0%  | 10    |
  | total                             | 0.278 | 0.313  | 0.37   | 0.392  | 0.414 | 0.32  | 100.0%  | 10    |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.945325136185
  Full duration: 3.43176603317

  2016-02-12 19:30:03,978 - run_rally - DEBUG - task_id : 12233c47-6a06-4a69-9fda-761eae3e8dbd
  2016-02-12 19:30:03,978 - run_rally - DEBUG - running command line : rally task report 12233c47-6a06-4a69-9fda-761eae3e8dbd --out /home/opnfv/functest/results/rally/opnfv-authenticate.html
  2016-02-12 19:30:04,619 - run_rally - DEBUG - running command line : rally task results 12233c47-6a06-4a69-9fda-761eae3e8dbd
  2016-02-12 19:30:05,200 - run_rally - DEBUG - saving json file
  2016-02-12 19:30:05,202 - run_rally - DEBUG - Push result into DB
  2016-02-12 19:30:06,227 - run_rally - DEBUG - <Response [200]>
  2016-02-12 19:30:06,229 - run_rally - INFO - Test scenario: "authenticate" OK.

  2016-02-12 19:30:06,229 - run_rally - INFO - Starting test scenario "glance" ...
  2016-02-12 19:30:06,229 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-glance.yaml
  2016-02-12 19:30:06,294 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': 'daf5424b-3efa-4514-8ece-af4597ba0ad2', 'service_list': ['glance'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'live_migration': False, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-12 19:31:37,895 - run_rally - INFO - 
   Preparing input task
   Task  a6ff81f3-d30b-42ca-afc7-a782a1b0ab87: started
  Task a6ff81f3-d30b-42ca-afc7-a782a1b0ab87: finished

  test scenario GlanceImages.list_images
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.list_images | 0.194 | 0.227  | 0.287  | 0.298  | 0.308 | 0.233 | 100.0%  | 10    |
  | total              | 0.194 | 0.228  | 0.288  | 0.298  | 0.308 | 0.233 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.686240911484
  Full duration: 3.71551012993

  test scenario GlanceImages.create_image_and_boot_instances
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | glance.create_image | 2.802 | 2.97   | 3.613  | 3.651  | 3.689  | 3.103 | 100.0%  | 10    |
  | nova.boot_servers   | 4.931 | 6.467  | 7.729  | 7.951  | 8.172  | 6.422 | 100.0%  | 10    |
  | total               | 7.743 | 9.551  | 10.989 | 11.078 | 11.167 | 9.526 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 27.7058939934
  Full duration: 54.5110180378

  test scenario GlanceImages.create_and_list_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 2.794 | 2.942  | 3.667  | 3.74   | 3.813 | 3.135 | 100.0%  | 10    |
  | glance.list_images  | 0.037 | 0.047  | 0.052  | 0.054  | 0.057 | 0.047 | 100.0%  | 10    |
  | total               | 2.839 | 2.987  | 3.705  | 3.783  | 3.86  | 3.182 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.32158112526
  Full duration: 13.9724760056

  test scenario GlanceImages.create_and_delete_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 3.063 | 3.609  | 3.646  | 3.66   | 3.674 | 3.494 | 100.0%  | 10    |
  | glance.delete_image | 0.133 | 0.147  | 0.157  | 0.159  | 0.161 | 0.147 | 100.0%  | 10    |
  | total               | 3.211 | 3.766  | 3.799  | 3.807  | 3.815 | 3.641 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 10.6368820667
  Full duration: 13.9659121037

  2016-02-12 19:31:37,895 - run_rally - DEBUG - task_id : a6ff81f3-d30b-42ca-afc7-a782a1b0ab87
  2016-02-12 19:31:37,895 - run_rally - DEBUG - running command line : rally task report a6ff81f3-d30b-42ca-afc7-a782a1b0ab87 --out /home/opnfv/functest/results/rally/opnfv-glance.html
  2016-02-12 19:31:38,502 - run_rally - DEBUG - running command line : rally task results a6ff81f3-d30b-42ca-afc7-a782a1b0ab87
  2016-02-12 19:31:39,084 - run_rally - DEBUG - saving json file
  2016-02-12 19:31:39,086 - run_rally - DEBUG - Push result into DB
  2016-02-12 19:31:39,820 - run_rally - DEBUG - <Response [200]>
  2016-02-12 19:31:39,821 - run_rally - INFO - Test scenario: "glance" OK.

  2016-02-12 19:31:39,821 - run_rally - INFO - Starting test scenario "cinder" ...
  2016-02-12 19:31:39,821 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-cinder.yaml
  2016-02-12 19:31:40,044 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': 'daf5424b-3efa-4514-8ece-af4597ba0ad2', 'service_list': ['cinder'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'live_migration': False, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-12 19:48:49,804 - run_rally - INFO - 
   Preparing input task
   Task  a9edf9cf-40a7-49be-8eb6-a24ec3b12338: started
  Task a9edf9cf-40a7-49be-8eb6-a24ec3b12338: finished

  test scenario CinderVolumes.create_and_attach_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server     | 3.002  | 4.449  | 6.528  | 6.555  | 6.583  | 4.869  | 100.0%  | 10    |
  | cinder.create_volume | 2.706  | 2.801  | 3.066  | 3.158  | 3.25   | 2.858  | 100.0%  | 10    |
  | nova.attach_volume   | 5.722  | 7.845  | 8.271  | 9.318  | 10.365 | 7.896  | 100.0%  | 10    |
  | nova.detach_volume   | 2.981  | 5.17   | 5.585  | 5.667  | 5.75   | 4.488  | 100.0%  | 10    |
  | cinder.delete_volume | 2.34   | 2.572  | 2.711  | 2.76   | 2.81   | 2.557  | 100.0%  | 10    |
  | nova.delete_server   | 2.392  | 2.47   | 2.55   | 2.552  | 2.553  | 2.468  | 100.0%  | 10    |
  | total                | 22.934 | 25.388 | 26.924 | 27.647 | 28.37  | 25.135 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 75.2977118492
  Full duration: 89.5739550591

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 5.219 | 5.39   | 5.468  | 5.482  | 5.496 | 5.379 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.103 | 0.12   | 0.172  | 0.211  | 0.25  | 0.136 | 100.0%  | 10    |
  | total                | 5.342 | 5.503  | 5.6    | 5.606  | 5.612 | 5.516 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.5520820618
  Full duration: 28.6927659512

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.716 | 2.921  | 2.992  | 3.007  | 3.021 | 2.913 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.056 | 0.122  | 0.156  | 0.193  | 0.23  | 0.124 | 100.0%  | 10    |
  | total                | 2.779 | 3.079  | 3.147  | 3.149  | 3.151 | 3.037 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.16054606438
  Full duration: 20.3591618538

  test scenario CinderVolumes.create_and_list_snapshots
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.345 | 2.529  | 2.599  | 2.602  | 2.604 | 2.5   | 100.0%  | 10    |
  | cinder.list_snapshots  | 0.019 | 0.087  | 0.111  | 0.152  | 0.194 | 0.092 | 100.0%  | 10    |
  | total                  | 2.428 | 2.602  | 2.703  | 2.717  | 2.73  | 2.592 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 7.66090703011
  Full duration: 31.241134882

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.859 | 2.963  | 3.097  | 3.119  | 3.141 | 2.987 | 100.0%  | 10    |
  | cinder.delete_volume | 2.479 | 2.572  | 2.647  | 2.692  | 2.737 | 2.571 | 100.0%  | 10    |
  | total                | 5.459 | 5.542  | 5.642  | 5.653  | 5.664 | 5.558 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.6256108284
  Full duration: 23.5103900433

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.963 | 5.375  | 5.534  | 5.577  | 5.62  | 4.921 | 100.0%  | 10    |
  | cinder.delete_volume | 2.46  | 2.531  | 2.574  | 2.579  | 2.585 | 2.53  | 100.0%  | 10    |
  | total                | 5.535 | 7.886  | 8.07   | 8.075  | 8.08  | 7.452 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 21.419508934
  Full duration: 28.6083099842

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.847 | 3.004  | 3.162  | 3.163  | 3.164 | 2.998 | 100.0%  | 10    |
  | cinder.delete_volume | 2.468 | 2.621  | 2.777  | 2.815  | 2.854 | 2.642 | 100.0%  | 10    |
  | total                | 5.424 | 5.595  | 5.871  | 5.944  | 6.018 | 5.641 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 17.0380129814
  Full duration: 24.2403891087

  test scenario CinderVolumes.create_and_upload_volume_to_image
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume          | 2.866  | 2.999  | 3.171  | 3.29   | 3.408  | 3.018  | 100.0%  | 10    |
  | cinder.upload_volume_to_image | 23.67  | 57.563 | 78.789 | 79.793 | 80.797 | 56.738 | 100.0%  | 10    |
  | cinder.delete_volume          | 2.349  | 2.495  | 2.622  | 2.633  | 2.644  | 2.499  | 100.0%  | 10    |
  | nova.delete_image             | 0.312  | 0.391  | 0.562  | 0.637  | 0.713  | 0.426  | 100.0%  | 10    |
  | total                         | 29.568 | 63.477 | 84.729 | 85.718 | 86.707 | 62.682 | 100.0%  | 10    |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 177.551611185
  Full duration: 185.510534048

  test scenario CinderVolumes.create_and_delete_snapshot
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.439 | 2.557  | 2.66   | 2.678  | 2.696 | 2.563 | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.272 | 2.36   | 2.526  | 2.557  | 2.588 | 2.387 | 100.0%  | 10    |
  | total                  | 4.799 | 4.98   | 5.034  | 5.066  | 5.098 | 4.95  | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.8108210564
  Full duration: 34.6716730595

  test scenario CinderVolumes.create_volume
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max  | avg   | success | count |
  +----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | cinder.create_volume | 2.772 | 2.879  | 2.953  | 2.997  | 3.04 | 2.879 | 100.0%  | 10    |
  | total                | 2.772 | 2.879  | 2.953  | 2.997  | 3.04 | 2.879 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  Load duration: 8.63443613052
  Full duration: 19.1983139515

  test scenario CinderVolumes.create_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.791 | 3.074  | 3.225  | 3.318  | 3.411 | 3.066 | 100.0%  | 10    |
  | total                | 2.791 | 3.074  | 3.225  | 3.318  | 3.411 | 3.066 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.021474123
  Full duration: 21.064909935

  test scenario CinderVolumes.list_volumes
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.list_volumes | 0.238 | 0.261  | 0.299  | 0.329  | 0.359 | 0.269 | 100.0%  | 10    |
  | total               | 0.238 | 0.261  | 0.299  | 0.329  | 0.359 | 0.27  | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.793784856796
  Full duration: 48.040571928

  test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
  +-----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
  +------------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | cinder.create_volume   | 2.854  | 3.038  | 3.084  | 3.107  | 3.129  | 3.016 | 100.0%  | 10    |
  | cinder.create_snapshot | 2.308  | 2.414  | 2.44   | 2.444  | 2.449  | 2.402 | 100.0%  | 10    |
  | nova.attach_volume     | 7.678  | 7.886  | 12.033 | 12.294 | 12.555 | 8.94  | 100.0%  | 10    |
  | nova.detach_volume     | 3.108  | 4.554  | 5.993  | 6.787  | 7.581  | 4.673 | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.213  | 2.342  | 2.485  | 2.5    | 2.514  | 2.362 | 100.0%  | 10    |
  | cinder.delete_volume   | 2.346  | 2.506  | 2.582  | 2.646  | 2.711  | 2.513 | 100.0%  | 10    |
  | total                  | 21.386 | 23.562 | 28.488 | 28.571 | 28.655 | 24.21 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 70.4934530258
  Full duration: 114.824916124

  test scenario CinderVolumes.create_from_volume_and_delete_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 7.69   | 13.562 | 19.985 | 21.954 | 23.923 | 14.049 | 100.0%  | 10    |
  | cinder.delete_volume | 2.371  | 2.493  | 2.866  | 3.881  | 4.895  | 2.733  | 100.0%  | 10    |
  | total                | 10.109 | 15.989 | 22.556 | 24.512 | 26.469 | 16.782 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 48.6095311642
  Full duration: 68.2930941582

  test scenario CinderVolumes.create_and_extend_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.789 | 2.985  | 3.108  | 3.14   | 3.172 | 2.99  | 100.0%  | 10    |
  | cinder.extend_volume | 2.644 | 2.745  | 2.831  | 2.838  | 2.845 | 2.753 | 100.0%  | 10    |
  | cinder.delete_volume | 2.484 | 2.576  | 2.624  | 2.627  | 2.63  | 2.566 | 100.0%  | 10    |
  | total                | 8.091 | 8.294  | 8.471  | 8.523  | 8.576 | 8.309 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.7742590904
  Full duration: 32.1246640682

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.785  | 3.006  | 3.052  | 3.053  | 3.054  | 2.967  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.339  | 2.436  | 2.475  | 2.481  | 2.486  | 2.419  | 100.0%  | 10    |
  | nova.attach_volume     | 7.797  | 7.994  | 11.939 | 13.348 | 14.758 | 9.194  | 100.0%  | 10    |
  | nova.detach_volume     | 3.106  | 5.458  | 5.926  | 6.833  | 7.741  | 5.44   | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.187  | 2.348  | 2.417  | 2.439  | 2.462  | 2.348  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.389  | 2.565  | 2.659  | 2.729  | 2.8    | 2.561  | 100.0%  | 10    |
  | total                  | 21.737 | 24.472 | 27.817 | 29.344 | 30.87  | 25.253 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 74.3525400162
  Full duration: 122.11897397

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.84   | 2.872  | 2.934  | 2.988  | 3.042  | 2.889  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.259  | 2.392  | 2.46   | 2.465  | 2.47   | 2.392  | 100.0%  | 10    |
  | nova.attach_volume     | 7.656  | 7.785  | 13.181 | 16.282 | 19.382 | 9.416  | 100.0%  | 10    |
  | nova.detach_volume     | 2.927  | 4.342  | 5.298  | 5.387  | 5.477  | 4.199  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.258  | 2.35   | 2.466  | 2.476  | 2.486  | 2.362  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.334  | 2.597  | 2.665  | 2.671  | 2.678  | 2.553  | 100.0%  | 10    |
  | total                  | 21.266 | 23.837 | 27.072 | 30.307 | 33.542 | 24.349 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 69.1618478298
  Full duration: 114.061968088

  2016-02-12 19:48:49,805 - run_rally - DEBUG - task_id : a9edf9cf-40a7-49be-8eb6-a24ec3b12338
  2016-02-12 19:48:49,805 - run_rally - DEBUG - running command line : rally task report a9edf9cf-40a7-49be-8eb6-a24ec3b12338 --out /home/opnfv/functest/results/rally/opnfv-cinder.html
  2016-02-12 19:48:50,531 - run_rally - DEBUG - running command line : rally task results a9edf9cf-40a7-49be-8eb6-a24ec3b12338
  2016-02-12 19:48:51,132 - run_rally - DEBUG - saving json file
  2016-02-12 19:48:51,138 - run_rally - DEBUG - Push result into DB
  2016-02-12 19:48:52,768 - run_rally - DEBUG - <Response [200]>
  2016-02-12 19:48:52,771 - run_rally - INFO - Test scenario: "cinder" OK.

  2016-02-12 19:48:52,772 - run_rally - INFO - Starting test scenario "heat" ...
  2016-02-12 19:48:52,772 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-heat.yaml
  2016-02-12 19:48:52,982 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': 'daf5424b-3efa-4514-8ece-af4597ba0ad2', 'service_list': ['heat'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'live_migration': False, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-12 19:55:40,270 - run_rally - INFO - 
   Preparing input task
   Task  797423eb-9306-44f7-ac18-2f292a59a933: started
  Task 797423eb-9306-44f7-ac18-2f292a59a933: finished

  test scenario HeatStacks.create_suspend_resume_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack  | 2.744 | 3.193  | 3.515  | 3.614  | 3.714 | 3.186 | 100.0%  | 10    |
  | heat.suspend_stack | 0.363 | 0.757  | 1.601  | 1.669  | 1.737 | 1.01  | 100.0%  | 10    |
  | heat.resume_stack  | 0.465 | 1.026  | 1.542  | 1.641  | 1.741 | 1.035 | 100.0%  | 10    |
  | heat.delete_stack  | 0.658 | 1.516  | 1.583  | 1.647  | 1.71  | 1.434 | 100.0%  | 10    |
  | total              | 4.822 | 6.805  | 8.108  | 8.133  | 8.158 | 6.665 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 19.812101841
  Full duration: 23.279335022

  test scenario HeatStacks.create_and_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 3.014 | 3.189  | 3.303  | 3.33   | 3.356 | 3.191 | 100.0%  | 10    |
  | heat.delete_stack | 0.399 | 1.326  | 1.648  | 1.671  | 1.693 | 1.121 | 100.0%  | 10    |
  | total             | 3.696 | 4.497  | 4.87   | 4.935  | 5.0   | 4.312 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 12.8518810272
  Full duration: 16.4311740398

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 10.344 | 11.705 | 12.412 | 12.901 | 13.39  | 11.743 | 100.0%  | 10    |
  | heat.delete_stack | 6.739  | 7.311  | 8.145  | 8.368  | 8.591  | 7.526  | 100.0%  | 10    |
  | total             | 17.421 | 19.452 | 20.394 | 20.56  | 20.727 | 19.269 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 56.5501990318
  Full duration: 60.2050161362

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 12.973 | 14.566 | 16.672 | 17.288 | 17.904 | 14.923 | 100.0%  | 10    |
  | heat.delete_stack | 8.332  | 9.406  | 10.315 | 10.366 | 10.416 | 9.442  | 100.0%  | 10    |
  | total             | 22.036 | 24.111 | 25.932 | 26.489 | 27.045 | 24.365 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 72.41437006
  Full duration: 76.2519450188

  test scenario HeatStacks.list_stacks_and_resources
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max  | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | heat.list_stacks                | 0.216 | 0.243  | 0.27   | 0.28   | 0.29 | 0.247 | 100.0%  | 10    |
  | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0  | 0.0   | 100.0%  | 10    |
  | total                           | 0.216 | 0.243  | 0.27   | 0.28   | 0.29 | 0.247 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+------+-------+---------+-------+
  Load duration: 0.760275125504
  Full duration: 3.68153595924

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.849 | 3.147  | 3.247  | 3.272  | 3.296 | 3.108 | 100.0%  | 10    |
  | heat.update_stack | 2.571 | 3.687  | 3.897  | 3.931  | 3.965 | 3.344 | 100.0%  | 10    |
  | heat.delete_stack | 1.19  | 1.508  | 1.705  | 1.818  | 1.931 | 1.527 | 100.0%  | 10    |
  | total             | 7.073 | 8.308  | 8.701  | 8.819  | 8.937 | 7.979 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.4536459446
  Full duration: 28.0561339855

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.875 | 3.107  | 3.277  | 3.281  | 3.285 | 3.099 | 100.0%  | 10    |
  | heat.update_stack | 2.49  | 2.629  | 3.689  | 3.697  | 3.704 | 2.919 | 100.0%  | 10    |
  | heat.delete_stack | 1.189 | 1.625  | 1.69   | 1.692  | 1.694 | 1.567 | 100.0%  | 10    |
  | total             | 7.152 | 7.293  | 8.468  | 8.516  | 8.565 | 7.585 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 23.0466270447
  Full duration: 26.991339922

  test scenario HeatStacks.create_update_delete_stack
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 2.94  | 3.24   | 3.417  | 3.516  | 3.616  | 3.249  | 100.0%  | 10    |
  | heat.update_stack | 4.858 | 5.085  | 6.009  | 6.069  | 6.128  | 5.318  | 100.0%  | 10    |
  | heat.delete_stack | 1.554 | 2.41   | 2.605  | 2.609  | 2.613  | 2.141  | 100.0%  | 10    |
  | total             | 9.806 | 10.624 | 11.784 | 11.86  | 11.936 | 10.708 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 32.2090818882
  Full duration: 36.5297718048

  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 7.52663493156
  Full duration: 15.8856461048

  test scenario HeatStacks.create_update_delete_stack
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 2.829 | 3.098  | 3.332  | 3.388  | 3.444  | 3.119  | 100.0%  | 10    |
  | heat.update_stack | 4.893 | 5.104  | 6.156  | 6.213  | 6.271  | 5.286  | 100.0%  | 10    |
  | heat.delete_stack | 1.53  | 2.418  | 2.801  | 2.839  | 2.878  | 2.229  | 100.0%  | 10    |
  | total             | 9.528 | 10.794 | 11.094 | 11.558 | 12.022 | 10.634 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 31.4142270088
  Full duration: 35.4717001915

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 3.073 | 3.16   | 3.387  | 3.39   | 3.394 | 3.199 | 100.0%  | 10    |
  | heat.update_stack | 2.579 | 3.762  | 3.901  | 3.912  | 3.923 | 3.576 | 100.0%  | 10    |
  | heat.delete_stack | 0.54  | 1.554  | 1.659  | 1.678  | 1.696 | 1.462 | 100.0%  | 10    |
  | total             | 7.205 | 8.538  | 8.665  | 8.713  | 8.76  | 8.236 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 25.6365950108
  Full duration: 29.4618060589

  test scenario HeatStacks.create_and_list_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.834 | 3.106  | 3.308  | 3.311  | 3.315 | 3.112 | 100.0%  | 10    |
  | heat.list_stacks  | 0.034 | 0.109  | 0.181  | 0.183  | 0.186 | 0.108 | 100.0%  | 10    |
  | total             | 2.882 | 3.243  | 3.368  | 3.425  | 3.483 | 3.22  | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.69428515434
  Full duration: 17.0273709297

  test scenario HeatStacks.create_check_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.933 | 3.189  | 3.295  | 3.297  | 3.3   | 3.159 | 100.0%  | 10    |
  | heat.check_stack  | 0.457 | 0.663  | 1.713  | 1.74   | 1.766 | 0.853 | 100.0%  | 10    |
  | heat.delete_stack | 0.719 | 1.632  | 1.905  | 1.912  | 1.92  | 1.593 | 100.0%  | 10    |
  | total             | 5.137 | 5.514  | 6.021  | 6.188  | 6.355 | 5.605 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.9900569916
  Full duration: 21.1466290951

  2016-02-12 19:55:40,271 - run_rally - DEBUG - task_id : 797423eb-9306-44f7-ac18-2f292a59a933
  2016-02-12 19:55:40,271 - run_rally - DEBUG - running command line : rally task report 797423eb-9306-44f7-ac18-2f292a59a933 --out /home/opnfv/functest/results/rally/opnfv-heat.html
  2016-02-12 19:55:40,950 - run_rally - DEBUG - running command line : rally task results 797423eb-9306-44f7-ac18-2f292a59a933
  2016-02-12 19:55:41,547 - run_rally - DEBUG - saving json file
  2016-02-12 19:55:41,552 - run_rally - DEBUG - Push result into DB
  2016-02-12 19:55:43,174 - run_rally - DEBUG - <Response [200]>
  2016-02-12 19:55:43,177 - run_rally - INFO - Test scenario: "heat" Failed.

  2016-02-12 19:55:43,178 - run_rally - INFO - Starting test scenario "keystone" ...
  2016-02-12 19:55:43,178 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-keystone.yaml
  2016-02-12 19:55:43,626 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': 'daf5424b-3efa-4514-8ece-af4597ba0ad2', 'service_list': ['keystone'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'live_migration': False, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-12 19:57:11,993 - run_rally - INFO - 
   Preparing input task
   Task  57d9692e-4def-4ee3-9b86-bfff622dc8d6: started
  Task 57d9692e-4def-4ee3-9b86-bfff622dc8d6: finished

  test scenario KeystoneBasic.create_tenant_with_users
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +------------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max  | avg   | success | count |
  +------------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | keystone.create_tenant | 0.108 | 0.122  | 0.148  | 0.164  | 0.18 | 0.129 | 100.0%  | 10    |
  | keystone.create_users  | 0.649 | 0.69   | 0.75   | 0.755  | 0.76 | 0.694 | 100.0%  | 10    |
  | total                  | 0.767 | 0.802  | 0.898  | 0.919  | 0.94 | 0.823 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+------+-------+---------+-------+
  Load duration: 2.42953491211
  Full duration: 12.7415950298

  test scenario KeystoneBasic.create_add_and_list_user_roles
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.104 | 0.121  | 0.149  | 0.15   | 0.151 | 0.126 | 100.0%  | 10    |
  | keystone.add_role    | 0.087 | 0.095  | 0.124  | 0.129  | 0.134 | 0.101 | 100.0%  | 10    |
  | keystone.list_roles  | 0.051 | 0.058  | 0.072  | 0.075  | 0.078 | 0.062 | 100.0%  | 10    |
  | total                | 0.259 | 0.286  | 0.314  | 0.318  | 0.321 | 0.289 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.864060878754
  Full duration: 6.40814208984

  test scenario KeystoneBasic.add_and_remove_user_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.115 | 0.222  | 0.285  | 0.305  | 0.325 | 0.207 | 100.0%  | 10    |
  | keystone.add_role    | 0.086 | 0.113  | 0.147  | 0.18   | 0.213 | 0.121 | 100.0%  | 10    |
  | keystone.remove_role | 0.058 | 0.072  | 0.18   | 0.188  | 0.196 | 0.108 | 100.0%  | 10    |
  | total                | 0.281 | 0.453  | 0.574  | 0.586  | 0.599 | 0.436 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.40016198158
  Full duration: 7.08734297752

  test scenario KeystoneBasic.create_update_and_delete_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.125 | 0.222  | 0.273  | 0.274  | 0.274 | 0.2   | 100.0%  | 10    |
  | keystone.update_tenant | 0.049 | 0.057  | 0.076  | 0.12   | 0.164 | 0.067 | 100.0%  | 10    |
  | keystone.delete_tenant | 0.121 | 0.141  | 0.208  | 0.247  | 0.286 | 0.158 | 100.0%  | 10    |
  | total                  | 0.319 | 0.414  | 0.545  | 0.582  | 0.619 | 0.426 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.2874519825
  Full duration: 5.71538686752

  test scenario KeystoneBasic.create_and_delete_service
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_service | 0.114 | 0.128  | 0.16   | 0.16   | 0.16  | 0.131 | 100.0%  | 10    |
  | keystone.delete_service | 0.058 | 0.062  | 0.071  | 0.089  | 0.108 | 0.066 | 100.0%  | 10    |
  | total                   | 0.177 | 0.194  | 0.222  | 0.223  | 0.223 | 0.198 | 100.0%  | 10    |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.619410991669
  Full duration: 4.71141886711

  test scenario KeystoneBasic.create_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.113 | 0.132  | 0.165  | 0.166  | 0.166 | 0.133 | 100.0%  | 10    |
  | total                  | 0.113 | 0.132  | 0.165  | 0.166  | 0.166 | 0.133 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.391160011292
  Full duration: 4.46575784683

  test scenario KeystoneBasic.create_user
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.129 | 0.145  | 0.188  | 0.188  | 0.188 | 0.156 | 100.0%  | 10    |
  | total                | 0.129 | 0.145  | 0.188  | 0.188  | 0.188 | 0.156 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.482604026794
  Full duration: 4.4991080761

  test scenario KeystoneBasic.create_and_list_tenants
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.116 | 0.144  | 0.167  | 0.169  | 0.171 | 0.144 | 100.0%  | 10    |
  | keystone.list_tenants  | 0.047 | 0.056  | 0.096  | 0.099  | 0.101 | 0.064 | 100.0%  | 10    |
  | total                  | 0.172 | 0.214  | 0.227  | 0.227  | 0.228 | 0.208 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.628124952316
  Full duration: 6.31660103798

  test scenario KeystoneBasic.create_and_delete_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.124 | 0.242  | 0.282  | 0.293  | 0.304 | 0.21  | 100.0%  | 10    |
  | keystone.delete_role | 0.112 | 0.131  | 0.174  | 0.203  | 0.231 | 0.142 | 100.0%  | 10    |
  | total                | 0.24  | 0.369  | 0.429  | 0.469  | 0.509 | 0.352 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.05624604225
  Full duration: 5.52495193481

  test scenario KeystoneBasic.get_entities
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.115 | 0.129  | 0.16   | 0.172  | 0.183 | 0.139 | 100.0%  | 10    |
  | keystone.create_user   | 0.062 | 0.074  | 0.106  | 0.11   | 0.114 | 0.082 | 100.0%  | 10    |
  | keystone.create_role   | 0.048 | 0.055  | 0.096  | 0.101  | 0.106 | 0.064 | 100.0%  | 10    |
  | keystone.get_tenant    | 0.043 | 0.045  | 0.061  | 0.071  | 0.081 | 0.051 | 100.0%  | 10    |
  | keystone.get_user      | 0.047 | 0.055  | 0.066  | 0.069  | 0.071 | 0.056 | 100.0%  | 10    |
  | keystone.get_role      | 0.046 | 0.051  | 0.065  | 0.066  | 0.067 | 0.054 | 100.0%  | 10    |
  | keystone.service_list  | 0.045 | 0.052  | 0.063  | 0.064  | 0.065 | 0.054 | 100.0%  | 10    |
  | keystone.get_service   | 0.042 | 0.055  | 0.068  | 0.079  | 0.089 | 0.058 | 100.0%  | 10    |
  | total                  | 0.53  | 0.553  | 0.58   | 0.597  | 0.615 | 0.557 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.73635601997
  Full duration: 10.0342190266

  test scenario KeystoneBasic.create_and_list_users
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.13  | 0.142  | 0.157  | 0.165  | 0.173 | 0.145 | 100.0%  | 10    |
  | keystone.list_users  | 0.046 | 0.053  | 0.084  | 0.089  | 0.095 | 0.059 | 100.0%  | 10    |
  | total                | 0.178 | 0.202  | 0.229  | 0.232  | 0.234 | 0.203 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.646016120911
  Full duration: 4.92132210732

  2016-02-12 19:57:11,994 - run_rally - DEBUG - task_id : 57d9692e-4def-4ee3-9b86-bfff622dc8d6
  2016-02-12 19:57:11,994 - run_rally - DEBUG - running command line : rally task report 57d9692e-4def-4ee3-9b86-bfff622dc8d6 --out /home/opnfv/functest/results/rally/opnfv-keystone.html
  2016-02-12 19:57:12,654 - run_rally - DEBUG - running command line : rally task results 57d9692e-4def-4ee3-9b86-bfff622dc8d6
  2016-02-12 19:57:13,252 - run_rally - DEBUG - saving json file
  2016-02-12 19:57:13,256 - run_rally - DEBUG - Push result into DB
  2016-02-12 19:57:14,454 - run_rally - DEBUG - <Response [200]>
  2016-02-12 19:57:14,456 - run_rally - INFO - Test scenario: "keystone" OK.

  2016-02-12 19:57:14,457 - run_rally - INFO - Starting test scenario "neutron" ...
  2016-02-12 19:57:14,457 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-neutron.yaml
  2016-02-12 19:57:14,836 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': 'daf5424b-3efa-4514-8ece-af4597ba0ad2', 'service_list': ['neutron'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'live_migration': False, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-12 20:02:28,457 - run_rally - INFO - 
   Preparing input task
   Task  e48913d0-c413-4744-83ec-2b67e8f0ed62: started
  Task e48913d0-c413-4744-83ec-2b67e8f0ed62: finished

  test scenario NeutronNetworks.create_and_delete_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.399 | 0.535  | 0.643  | 0.664  | 0.686 | 0.532 | 100.0%  | 10    |
  | neutron.delete_port | 0.144 | 0.157  | 0.316  | 0.392  | 0.469 | 0.215 | 100.0%  | 10    |
  | total               | 0.552 | 0.731  | 0.93   | 0.959  | 0.989 | 0.747 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.22487306595
  Full duration: 26.1480481625

  test scenario NeutronNetworks.create_and_list_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.419 | 0.483  | 0.566  | 0.57   | 0.574 | 0.482 | 100.0%  | 10    |
  | neutron.create_router        | 0.035 | 0.041  | 0.191  | 0.201  | 0.211 | 0.086 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.233 | 0.256  | 0.532  | 0.563  | 0.595 | 0.323 | 100.0%  | 10    |
  | neutron.list_routers         | 0.032 | 0.162  | 0.183  | 0.256  | 0.329 | 0.141 | 100.0%  | 10    |
  | total                        | 0.752 | 1.012  | 1.399  | 1.433  | 1.467 | 1.032 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.85454916954
  Full duration: 28.7914018631

  test scenario NeutronNetworks.create_and_delete_routers
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet           | 0.388 | 0.454  | 0.651  | 0.652  | 0.654 | 0.493 | 100.0%  | 10    |
  | neutron.create_router           | 0.033 | 0.106  | 0.186  | 0.193  | 0.2   | 0.109 | 100.0%  | 10    |
  | neutron.add_interface_router    | 0.229 | 0.371  | 0.412  | 0.421  | 0.43  | 0.34  | 100.0%  | 10    |
  | neutron.remove_interface_router | 0.16  | 0.23   | 0.415  | 0.474  | 0.532 | 0.276 | 100.0%  | 10    |
  | neutron.delete_router           | 0.117 | 0.128  | 0.266  | 0.272  | 0.277 | 0.174 | 100.0%  | 10    |
  | total                           | 1.101 | 1.28   | 1.776  | 1.813  | 1.851 | 1.392 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.21995615959
  Full duration: 29.2232439518

  test scenario NeutronNetworks.create_and_list_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.438 | 0.52   | 0.742  | 0.744  | 0.747 | 0.57  | 100.0%  | 10    |
  | neutron.list_ports  | 0.125 | 0.284  | 0.421  | 0.448  | 0.474 | 0.279 | 100.0%  | 10    |
  | total               | 0.664 | 0.793  | 1.036  | 1.092  | 1.149 | 0.849 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.59459614754
  Full duration: 27.4613380432

  test scenario NeutronNetworks.create_and_delete_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.401 | 0.455  | 0.489  | 0.518  | 0.547 | 0.457 | 100.0%  | 10    |
  | neutron.delete_subnet | 0.14  | 0.286  | 0.324  | 0.365  | 0.406 | 0.25  | 100.0%  | 10    |
  | total                 | 0.544 | 0.726  | 0.858  | 0.86   | 0.862 | 0.707 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.16699886322
  Full duration: 25.9957101345

  test scenario NeutronNetworks.create_and_delete_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.321 | 0.349  | 0.389  | 0.39   | 0.391 | 0.355 | 100.0%  | 10    |
  | neutron.delete_network | 0.109 | 0.126  | 0.269  | 0.31   | 0.351 | 0.171 | 100.0%  | 10    |
  | total                  | 0.431 | 0.495  | 0.617  | 0.679  | 0.741 | 0.526 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.58180904388
  Full duration: 15.3088929653

  test scenario NeutronNetworks.create_and_list_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.302 | 0.351  | 0.374  | 0.389  | 0.404 | 0.353 | 100.0%  | 10    |
  | neutron.list_networks  | 0.041 | 0.054  | 0.209  | 0.217  | 0.225 | 0.11  | 100.0%  | 10    |
  | total                  | 0.343 | 0.416  | 0.593  | 0.595  | 0.597 | 0.464 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.31170892715
  Full duration: 16.9302289486

  test scenario NeutronNetworks.create_and_update_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.398 | 0.445  | 0.598  | 0.664  | 0.729 | 0.483 | 100.0%  | 10    |
  | neutron.create_router        | 0.033 | 0.172  | 0.185  | 0.19   | 0.194 | 0.135 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.23  | 0.301  | 0.403  | 0.406  | 0.409 | 0.309 | 100.0%  | 10    |
  | neutron.update_router        | 0.082 | 0.168  | 0.286  | 0.305  | 0.323 | 0.179 | 100.0%  | 10    |
  | total                        | 0.888 | 1.115  | 1.258  | 1.267  | 1.276 | 1.106 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.1909840107
  Full duration: 29.4671947956

  test scenario NeutronNetworks.create_and_update_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.32  | 0.431  | 0.497  | 0.498  | 0.499 | 0.418 | 100.0%  | 10    |
  | neutron.update_network | 0.105 | 0.309  | 0.472  | 0.483  | 0.495 | 0.301 | 100.0%  | 10    |
  | total                  | 0.427 | 0.762  | 0.97   | 0.978  | 0.987 | 0.72  | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.14427304268
  Full duration: 18.0257649422

  test scenario NeutronNetworks.create_and_update_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.417 | 0.509  | 0.627  | 0.667  | 0.707 | 0.529 | 100.0%  | 10    |
  | neutron.update_port | 0.11  | 0.262  | 0.372  | 0.396  | 0.421 | 0.25  | 100.0%  | 10    |
  | total               | 0.571 | 0.756  | 1.042  | 1.058  | 1.073 | 0.779 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.27396202087
  Full duration: 27.3324229717

  test scenario NeutronNetworks.create_and_list_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.426 | 0.51   | 0.568  | 0.569  | 0.57  | 0.502 | 100.0%  | 10    |
  | neutron.list_subnets  | 0.059 | 0.063  | 0.223  | 0.234  | 0.245 | 0.111 | 100.0%  | 10    |
  | total                 | 0.487 | 0.62   | 0.712  | 0.758  | 0.803 | 0.613 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.74596190453
  Full duration: 27.4602999687

  test scenario NeutronNetworks.create_and_update_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.411 | 0.435  | 0.536  | 0.56   | 0.584 | 0.46  | 100.0%  | 10    |
  | neutron.update_subnet | 0.16  | 0.182  | 0.338  | 0.411  | 0.484 | 0.246 | 100.0%  | 10    |
  | total                 | 0.588 | 0.674  | 0.905  | 0.915  | 0.924 | 0.706 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.05780911446
  Full duration: 27.6062719822

  2016-02-12 20:02:28,458 - run_rally - DEBUG - task_id : e48913d0-c413-4744-83ec-2b67e8f0ed62
  2016-02-12 20:02:28,458 - run_rally - DEBUG - running command line : rally task report e48913d0-c413-4744-83ec-2b67e8f0ed62 --out /home/opnfv/functest/results/rally/opnfv-neutron.html
  2016-02-12 20:02:29,109 - run_rally - DEBUG - running command line : rally task results e48913d0-c413-4744-83ec-2b67e8f0ed62
  2016-02-12 20:02:29,699 - run_rally - DEBUG - saving json file
  2016-02-12 20:02:29,704 - run_rally - DEBUG - Push result into DB
  2016-02-12 20:02:31,476 - run_rally - DEBUG - <Response [200]>
  2016-02-12 20:02:31,478 - run_rally - INFO - Test scenario: "neutron" OK.

  2016-02-12 20:02:31,479 - run_rally - INFO - Starting test scenario "nova" ...
  2016-02-12 20:02:31,479 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-nova.yaml
  2016-02-12 20:02:31,983 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': 'daf5424b-3efa-4514-8ece-af4597ba0ad2', 'service_list': ['nova'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'live_migration': False, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-12 20:28:19,817 - run_rally - INFO - 
   Preparing input task
   Task  86ea3837-f2e0-40c9-94c4-4716ca177f60: started
  Task 86ea3837-f2e0-40c9-94c4-4716ca177f60: finished

  test scenario NovaKeypair.create_and_delete_keypair
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.372 | 0.481  | 0.526  | 0.528  | 0.53  | 0.465 | 100.0%  | 10    |
  | nova.delete_keypair | 0.012 | 0.017  | 0.019  | 0.02   | 0.02  | 0.016 | 100.0%  | 10    |
  | total               | 0.393 | 0.497  | 0.539  | 0.544  | 0.549 | 0.482 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.48728299141
  Full duration: 15.9261510372

  test scenario NovaServers.snapshot_server
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | action                 | min    | median | 90%ile  | 95%ile  | max     | avg    | success | count |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | nova.boot_server       | 3.667  | 5.588  | 6.458   | 6.579   | 6.699   | 5.6    | 100.0%  | 10    |
  | nova.create_image      | 28.485 | 46.423 | 73.882  | 74.768  | 75.654  | 50.445 | 100.0%  | 10    |
  | nova.delete_server     | 2.402  | 2.583  | 2.776   | 2.814   | 2.853   | 2.602  | 100.0%  | 10    |
  | nova.boot_server (2)   | 15.754 | 21.941 | 36.956  | 38.716  | 40.476  | 25.503 | 100.0%  | 10    |
  | nova.delete_server (2) | 2.387  | 3.643  | 4.941   | 5.086   | 5.23    | 3.723  | 100.0%  | 10    |
  | nova.delete_image      | 0.196  | 0.611  | 1.169   | 1.896   | 2.624   | 0.787  | 100.0%  | 10    |
  | total                  | 64.165 | 80.28  | 120.393 | 124.468 | 128.543 | 88.661 | 100.0%  | 10    |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  Load duration: 251.648657084
  Full duration: 276.949105024

  test scenario NovaKeypair.boot_and_delete_server_with_keypair
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | nova.create_keypair | 0.35  | 0.468  | 0.647  | 0.703  | 0.758  | 0.502 | 100.0%  | 10    |
  | nova.boot_server    | 3.271 | 4.466  | 5.648  | 5.68   | 5.712  | 4.477 | 100.0%  | 10    |
  | nova.delete_server  | 2.357 | 2.413  | 4.727  | 4.771  | 4.815  | 2.907 | 100.0%  | 10    |
  | nova.delete_keypair | 0.013 | 0.017  | 0.02   | 0.024  | 0.028  | 0.017 | 100.0%  | 10    |
  | total               | 6.086 | 7.272  | 10.906 | 11.005 | 11.104 | 7.903 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 21.4185590744
  Full duration: 44.9553050995

  test scenario NovaKeypair.create_and_list_keypairs
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.347 | 0.435  | 0.529  | 0.575  | 0.622 | 0.446 | 100.0%  | 10    |
  | nova.list_keypairs  | 0.012 | 0.017  | 0.021  | 0.021  | 0.021 | 0.017 | 100.0%  | 10    |
  | total               | 0.36  | 0.451  | 0.549  | 0.596  | 0.644 | 0.463 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.30683994293
  Full duration: 17.9540309906

  test scenario NovaServers.list_servers
  +--------------------------------------------------------------------------------------+
  |                                 Response Times (sec)                                 |
  +-------------------+------+--------+--------+--------+-------+------+---------+-------+
  | action            | min  | median | 90%ile | 95%ile | max   | avg  | success | count |
  +-------------------+------+--------+--------+--------+-------+------+---------+-------+
  | nova.list_servers | 0.57 | 0.656  | 0.724  | 0.726  | 0.728 | 0.66 | 100.0%  | 10    |
  | total             | 0.57 | 0.656  | 0.724  | 0.726  | 0.728 | 0.66 | 100.0%  | 10    |
  +-------------------+------+--------+--------+--------+-------+------+---------+-------+
  Load duration: 1.95767593384
  Full duration: 50.1962890625

  test scenario NovaServers.resize_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.571  | 5.812  | 6.108  | 6.218  | 6.328  | 5.346  | 100.0%  | 10    |
  | nova.resize         | 21.133 | 41.802 | 41.975 | 42.053 | 42.131 | 33.688 | 100.0%  | 10    |
  | nova.resize_confirm | 2.372  | 2.391  | 2.549  | 2.554  | 2.56   | 2.441  | 100.0%  | 10    |
  | nova.delete_server  | 2.414  | 2.599  | 4.526  | 4.579  | 4.633  | 3.318  | 100.0%  | 10    |
  | total               | 30.002 | 52.747 | 55.047 | 55.073 | 55.1   | 44.793 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 122.701140881
  Full duration: 137.509846926

  test scenario NovaServers.boot_server_from_volume_and_delete
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.383  | 4.734  | 6.038  | 6.054  | 6.069  | 4.777  | 100.0%  | 10    |
  | nova.boot_server     | 8.153  | 9.391  | 11.581 | 12.372 | 13.164 | 9.722  | 100.0%  | 10    |
  | nova.delete_server   | 4.524  | 4.692  | 5.062  | 6.058  | 7.053  | 4.935  | 100.0%  | 10    |
  | total                | 16.523 | 19.055 | 22.314 | 23.115 | 23.916 | 19.435 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 56.2685899734
  Full duration: 88.1011340618

  test scenario NovaServers.boot_and_migrate_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.51   | 4.767  | 6.246  | 6.247  | 6.248  | 5.033  | 100.0%  | 10    |
  | nova.stop_server    | 4.665  | 13.7   | 15.919 | 16.024 | 16.129 | 10.667 | 100.0%  | 10    |
  | nova.migrate        | 14.448 | 18.934 | 31.729 | 31.889 | 32.049 | 21.453 | 100.0%  | 10    |
  | nova.resize_confirm | 2.392  | 2.41   | 2.476  | 2.523  | 2.57   | 2.431  | 100.0%  | 10    |
  | nova.delete_server  | 2.361  | 2.393  | 2.47   | 2.508  | 2.545  | 2.413  | 100.0%  | 10    |
  | total               | 30.988 | 37.377 | 58.67  | 58.979 | 59.289 | 41.999 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 120.644536018
  Full duration: 135.838603973

  test scenario NovaServers.boot_and_delete_server
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | nova.boot_server   | 3.511 | 6.17   | 7.23   | 7.245  | 7.259  | 5.929 | 100.0%  | 10    |
  | nova.delete_server | 2.401 | 4.626  | 4.875  | 4.9    | 4.924  | 3.876 | 100.0%  | 10    |
  | total              | 6.099 | 10.839 | 11.973 | 12.035 | 12.097 | 9.805 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 28.1878061295
  Full duration: 53.0389208794

  test scenario NovaServers.boot_and_rebuild_server
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.396 | 4.751  | 5.961  | 5.997  | 6.033  | 4.765  | 100.0%  | 10    |
  | nova.rebuild_server | 6.412 | 11.396 | 17.143 | 17.212 | 17.281 | 11.678 | 100.0%  | 10    |
  | nova.delete_server  | 2.381 | 2.432  | 2.57   | 2.572  | 2.575  | 2.465  | 100.0%  | 10    |
  | total               | 13.56 | 18.646 | 24.603 | 25.08  | 25.558 | 18.908 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 51.1383721828
  Full duration: 74.9763679504

  test scenario NovaSecGroup.create_and_list_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.405  | 1.683  | 1.794  | 1.824  | 1.855  | 1.669  | 100.0%  | 10    |
  | nova.create_100_rules          | 8.981  | 10.227 | 10.547 | 10.572 | 10.598 | 9.996  | 100.0%  | 10    |
  | nova.list_security_groups      | 0.089  | 0.152  | 0.208  | 0.216  | 0.225  | 0.158  | 100.0%  | 10    |
  | total                          | 10.845 | 11.986 | 12.358 | 12.45  | 12.541 | 11.823 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 34.9436230659
  Full duration: 63.4042258263

  test scenario NovaSecGroup.create_and_delete_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.574  | 1.855  | 2.164  | 2.264  | 2.363  | 1.899  | 100.0%  | 10    |
  | nova.create_100_rules          | 8.508  | 9.445  | 10.081 | 10.164 | 10.247 | 9.476  | 100.0%  | 10    |
  | nova.delete_10_security_groups | 0.751  | 0.892  | 1.01   | 1.038  | 1.066  | 0.897  | 100.0%  | 10    |
  | total                          | 11.131 | 12.394 | 12.807 | 12.865 | 12.923 | 12.272 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 36.2206399441
  Full duration: 51.0607750416

  test scenario NovaServers.boot_and_bounce_server
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  | action                  | min    | median | 90%ile | 95%ile  | max     | avg    | success | count |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  | nova.boot_server        | 3.685  | 4.768  | 5.396  | 5.806   | 6.216   | 4.714  | 100.0%  | 10    |
  | nova.reboot_server      | 4.412  | 4.608  | 4.722  | 4.792   | 4.863   | 4.599  | 100.0%  | 10    |
  | nova.soft_reboot_server | 6.743  | 6.895  | 18.97  | 72.539  | 126.108 | 18.82  | 100.0%  | 10    |
  | nova.stop_server        | 4.633  | 4.808  | 5.936  | 10.708  | 15.48   | 5.83   | 100.0%  | 10    |
  | nova.start_server       | 2.619  | 2.688  | 2.818  | 2.84    | 2.861   | 2.717  | 100.0%  | 10    |
  | nova.rescue_server      | 6.606  | 11.129 | 17.669 | 17.772  | 17.876  | 11.753 | 100.0%  | 10    |
  | nova.unrescue_server    | 2.314  | 4.496  | 4.579  | 4.626   | 4.673   | 4.086  | 100.0%  | 10    |
  | nova.delete_server      | 2.369  | 2.395  | 2.543  | 2.544   | 2.546   | 2.437  | 100.0%  | 10    |
  | total                   | 36.138 | 44.417 | 61.416 | 114.546 | 167.676 | 54.996 | 100.0%  | 10    |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  Load duration: 167.702675819
  Full duration: 192.379112959

  test scenario NovaServers.boot_server
  +---------------------------------------------------------------------------------------+
  |                                 Response Times (sec)                                  |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server | 3.314 | 4.815  | 5.794  | 5.963  | 6.131 | 4.735 | 100.0%  | 10    |
  | total            | 3.314 | 4.815  | 5.795  | 5.963  | 6.131 | 4.735 | 100.0%  | 10    |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.9615139961
  Full duration: 39.9092509747

  test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
  +-----------------------------------------------------------------------------------------------------------+
  |                                           Response Times (sec)                                            |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups    | 1.442  | 1.794  | 2.113  | 2.16   | 2.206  | 1.86   | 100.0%  | 10    |
  | nova.create_100_rules             | 8.824  | 9.984  | 10.299 | 10.317 | 10.336 | 9.856  | 100.0%  | 10    |
  | nova.boot_server                  | 4.38   | 5.129  | 5.811  | 5.833  | 5.855  | 5.079  | 100.0%  | 10    |
  | nova.get_attached_security_groups | 0.145  | 0.156  | 0.198  | 0.202  | 0.205  | 0.164  | 100.0%  | 10    |
  | nova.delete_server                | 2.402  | 2.436  | 4.511  | 4.525  | 4.539  | 2.875  | 100.0%  | 10    |
  | nova.delete_10_security_groups    | 0.768  | 0.857  | 1.079  | 1.122  | 1.165  | 0.907  | 100.0%  | 10    |
  | total                             | 18.735 | 20.708 | 22.726 | 22.988 | 23.251 | 20.742 | 100.0%  | 10    |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 60.3526058197
  Full duration: 85.4367339611

  test scenario NovaServers.pause_and_unpause_server
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +---------------------+--------+--------+--------+--------+-------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max   | avg    | success | count |
  +---------------------+--------+--------+--------+--------+-------+--------+---------+-------+
  | nova.boot_server    | 3.714  | 5.72   | 6.358  | 6.413  | 6.467 | 5.32   | 100.0%  | 10    |
  | nova.pause_server   | 2.307  | 2.482  | 2.535  | 2.587  | 2.64  | 2.443  | 100.0%  | 10    |
  | nova.unpause_server | 2.302  | 2.363  | 2.541  | 2.584  | 2.628 | 2.415  | 100.0%  | 10    |
  | nova.delete_server  | 2.408  | 2.612  | 4.806  | 4.912  | 5.018 | 3.413  | 100.0%  | 10    |
  | total               | 10.752 | 13.334 | 16.041 | 16.05  | 16.06 | 13.592 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+-------+--------+---------+-------+
  Load duration: 41.5451591015
  Full duration: 66.7291839123

  test scenario NovaServers.boot_server_from_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.333  | 3.526  | 5.986  | 6.114  | 6.242  | 4.458  | 100.0%  | 10    |
  | nova.boot_server     | 8.493  | 8.945  | 11.959 | 12.295 | 12.632 | 9.727  | 100.0%  | 10    |
  | total                | 11.903 | 13.604 | 17.765 | 18.139 | 18.513 | 14.185 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 41.6071519852
  Full duration: 78.2099730968

  test scenario NovaServers.boot_and_list_server
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server  | 3.63  | 5.537  | 6.197  | 6.233  | 6.268 | 5.191 | 100.0%  | 10    |
  | nova.list_servers | 0.144 | 0.215  | 0.381  | 0.418  | 0.456 | 0.252 | 100.0%  | 10    |
  | total             | 3.87  | 5.823  | 6.499  | 6.572  | 6.645 | 5.443 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 17.032296896
  Full duration: 51.2773780823

  2016-02-12 20:28:19,817 - run_rally - DEBUG - task_id : 86ea3837-f2e0-40c9-94c4-4716ca177f60
  2016-02-12 20:28:19,817 - run_rally - DEBUG - running command line : rally task report 86ea3837-f2e0-40c9-94c4-4716ca177f60 --out /home/opnfv/functest/results/rally/opnfv-nova.html
  2016-02-12 20:28:20,475 - run_rally - DEBUG - running command line : rally task results 86ea3837-f2e0-40c9-94c4-4716ca177f60
  2016-02-12 20:28:21,078 - run_rally - DEBUG - saving json file
  2016-02-12 20:28:21,083 - run_rally - DEBUG - Push result into DB
  2016-02-12 20:28:22,764 - run_rally - DEBUG - <Response [200]>
  2016-02-12 20:28:22,768 - run_rally - INFO - Test scenario: "nova" OK.

  2016-02-12 20:28:22,769 - run_rally - INFO - Starting test scenario "quotas" ...
  2016-02-12 20:28:22,769 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-quotas.yaml
  2016-02-12 20:28:23,212 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': 'daf5424b-3efa-4514-8ece-af4597ba0ad2', 'service_list': ['quotas'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'live_migration': False, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-12 20:29:11,586 - run_rally - INFO - 
   Preparing input task
   Task  41e42442-c6ae-405a-9194-f4fc4f499859: started
  Task 41e42442-c6ae-405a-9194-f4fc4f499859: finished

  test scenario Quotas.cinder_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.584 | 0.641  | 0.717  | 0.767  | 0.817 | 0.657 | 100.0%  | 10    |
  | total                | 0.584 | 0.641  | 0.717  | 0.767  | 0.817 | 0.657 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.94293808937
  Full duration: 8.03202700615

  test scenario Quotas.neutron_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.239 | 0.278  | 0.402  | 0.423  | 0.444 | 0.313 | 100.0%  | 10    |
  | total                | 0.302 | 0.342  | 0.469  | 0.493  | 0.517 | 0.379 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.991186857224
  Full duration: 6.27371191978

  test scenario Quotas.cinder_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.579 | 0.621  | 0.709  | 0.717  | 0.725 | 0.638 | 100.0%  | 10    |
  | quotas.delete_quotas | 0.425 | 0.457  | 0.537  | 0.549  | 0.561 | 0.47  | 100.0%  | 10    |
  | total                | 1.03  | 1.105  | 1.183  | 1.193  | 1.203 | 1.108 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.31679296494
  Full duration: 9.39453291893

  test scenario Quotas.nova_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.317 | 0.343  | 0.381  | 0.384  | 0.387 | 0.346 | 100.0%  | 8     |
  | quotas.delete_quotas | 0.018 | 0.02   | 0.024  | 0.024  | 0.024 | 0.021 | 75.0%   | 8     |
  | total                | 0.335 | 0.354  | 0.4    | 0.403  | 0.405 | 0.365 | 75.0%   | 8     |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.788276195526
  Full duration: 6.69773983955

  test scenario Quotas.nova_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.324 | 0.38   | 0.454  | 0.456  | 0.459 | 0.387 | 100.0%  | 10    |
  | total                | 0.324 | 0.38   | 0.454  | 0.456  | 0.459 | 0.387 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.2254319191
  Full duration: 6.98697400093

  2016-02-12 20:29:11,586 - run_rally - DEBUG - task_id : 41e42442-c6ae-405a-9194-f4fc4f499859
  2016-02-12 20:29:11,587 - run_rally - DEBUG - running command line : rally task report 41e42442-c6ae-405a-9194-f4fc4f499859 --out /home/opnfv/functest/results/rally/opnfv-quotas.html
  2016-02-12 20:29:12,197 - run_rally - DEBUG - running command line : rally task results 41e42442-c6ae-405a-9194-f4fc4f499859
  2016-02-12 20:29:12,775 - run_rally - DEBUG - saving json file
  2016-02-12 20:29:12,777 - run_rally - DEBUG - Push result into DB
  2016-02-12 20:29:14,148 - run_rally - DEBUG - <Response [200]>
  2016-02-12 20:29:14,149 - run_rally - INFO - Test scenario: "quotas" Failed.

  2016-02-12 20:29:14,149 - run_rally - INFO - Starting test scenario "requests" ...
  2016-02-12 20:29:14,149 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-requests.yaml
  2016-02-12 20:29:14,227 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': 'daf5424b-3efa-4514-8ece-af4597ba0ad2', 'service_list': ['requests'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'live_migration': False, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-12 20:29:28,298 - run_rally - INFO - 
   Preparing input task
   Task  69b780f0-daca-4fbe-b9d6-45abe7cd9985: started
  Task 69b780f0-daca-4fbe-b9d6-45abe7cd9985: finished

  test scenario HttpRequests.check_random_request
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +------------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 0.44 | 0.577  | 1.063  | 1.074  | 1.084 | 0.694 | 100.0%  | 10    |
  | total                  | 0.44 | 0.577  | 1.063  | 1.074  | 1.084 | 0.694 | 100.0%  | 10    |
  +------------------------+------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.00274682045
  Full duration: 4.5990281105

  test scenario HttpRequests.check_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 0.444 | 0.46   | 0.482  | 0.483  | 0.483 | 0.464 | 100.0%  | 10    |
  | total                  | 0.444 | 0.46   | 0.482  | 0.483  | 0.483 | 0.464 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.41119194031
  Full duration: 3.8915681839

  2016-02-12 20:29:28,298 - run_rally - DEBUG - task_id : 69b780f0-daca-4fbe-b9d6-45abe7cd9985
  2016-02-12 20:29:28,298 - run_rally - DEBUG - running command line : rally task report 69b780f0-daca-4fbe-b9d6-45abe7cd9985 --out /home/opnfv/functest/results/rally/opnfv-requests.html
  2016-02-12 20:29:28,895 - run_rally - DEBUG - running command line : rally task results 69b780f0-daca-4fbe-b9d6-45abe7cd9985
  2016-02-12 20:29:29,467 - run_rally - DEBUG - saving json file
  2016-02-12 20:29:29,468 - run_rally - DEBUG - Push result into DB
  2016-02-12 20:29:30,190 - run_rally - DEBUG - <Response [200]>
  2016-02-12 20:29:30,190 - run_rally - INFO - Test scenario: "requests" OK.

  2016-02-12 20:29:30,191 - run_rally - INFO - 

                       Rally Summary Report
  +===================+============+===============+===========+
  | Module            | Duration   | nb. Test Run  | Success   |
  +===================+============+===============+===========+
  | authenticate      | 00:19      | 10            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | glance            | 01:26      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | cinder            | 16:46      | 50            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | heat              | 06:30      | 32            | 92.31%    |
  +-------------------+------------+---------------+-----------+
  | keystone          | 01:12      | 29            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | neutron           | 04:59      | 31            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | nova              | 25:23      | 61            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | quotas            | 00:37      | 7             | 95.00%    |
  +-------------------+------------+---------------+-----------+
  | requests          | 00:08      | 2             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  +===================+============+===============+===========+
  | TOTAL:            | 00:57:24   | 229           | 98.59%    |
  +===================+============+===============+===========+

  2016-02-12 20:29:30,191 - run_rally - DEBUG - Pushing Rally summary into DB...
  2016-02-12 20:29:30,860 - run_rally - DEBUG - <Response [200]>
  2016-02-12 20:29:30,860 - run_rally - DEBUG - Deleting image 'functest-img' with ID '0c74bd9e-0ac2-4332-8e03-e00c266752ad'...
  2016-02-12 20:29:31,444 - run_rally - DEBUG - Deleting volume type 'volume_test'...
::
