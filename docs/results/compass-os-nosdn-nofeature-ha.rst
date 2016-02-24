.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for compass-os-nosdn-nofeature-ha
-------------------------------------------------------

VIM
---

vping_ssh
^^^^^^^^^
::

  FUNCTEST.info: Running vPing-SSH test...
  vPing_ssh- INFO - Creating image 'functest-vping' from '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img'...
  vPing_ssh- INFO - Creating neutron network vping-net...
  vPing_ssh- INFO - Creating security group  'vPing-sg'...
  vPing_ssh- INFO - Using existing Flavor 'm1.small'...
  vPing_ssh- INFO - vPing Start Time:'2016-02-23 04:35:47'
  vPing_ssh- INFO - Creating instance 'opnfv-vping-1'...
   name=opnfv-vping-1
   flavor=<Flavor: m1.small>
   image=193891f9-6644-4668-9ac4-bd9336610a99
   network=999caa31-8f28-4737-aa6e-3981e28a7e55

  vPing_ssh- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  vPing_ssh- INFO - Adding 'opnfv-vping-1' to security group 'vPing-sg'...
  vPing_ssh- INFO - Creating instance 'opnfv-vping-2'...
   name=opnfv-vping-2
   flavor=<Flavor: m1.small>
   image=193891f9-6644-4668-9ac4-bd9336610a99
   network=999caa31-8f28-4737-aa6e-3981e28a7e55

  vPing_ssh- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  vPing_ssh- INFO - Adding 'opnfv-vping-2' to security group 'vPing-sg'...
  vPing_ssh- INFO - Creating floating IP for VM 'opnfv-vping-2'...
  vPing_ssh- INFO - Floating IP created: '192.168.10.101'
  vPing_ssh- INFO - Associating floating ip: '192.168.10.101' to VM 'opnfv-vping-2'
  vPing_ssh- INFO - Trying to establish SSH connection to 192.168.10.101...
  vPing_ssh- INFO - Waiting for ping...
  vPing_ssh- INFO - vPing detected!
  vPing_ssh- INFO - vPing duration:'43.2' s.
  vPing_ssh- INFO - Cleaning up...
  vPing_ssh- INFO - vPing OK


vping_userdata
^^^^^^^^^^^^^^
::

  FUNCTEST.info: Running vPing-userdata test...
  vPing_userdata- INFO - Creating image 'functest-vping' from '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img'...
  vPing_userdata- INFO - Creating neutron network vping-net...
  vPing_userdata- INFO - Creating security group  'vPing-sg'...
  vPing_userdata- INFO - Flavor found 'm1.small'
  vPing_userdata- INFO - vPing Start Time:'2016-02-23 04:36:44'
  vPing_userdata- INFO - Creating instance 'opnfv-vping-1'...
   name=opnfv-vping-1
   flavor=<Flavor: m1.small>
   image=53004632-aa69-4868-8234-2ef945681fcd
   network=bf5529b1-1cb7-4ea6-93b8-5ff436c5ed3c

  vPing_userdata- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  vPing_userdata- INFO - Creating instance 'opnfv-vping-2'...
   name=opnfv-vping-2
   flavor=<Flavor: m1.small>
   image=53004632-aa69-4868-8234-2ef945681fcd
   network=bf5529b1-1cb7-4ea6-93b8-5ff436c5ed3c
   userdata=
  #!/bin/sh

  while true; do
   ping -c 1 192.168.130.3 2>&1 >/dev/null
   RES=$?
   if [ "Z$RES" = "Z0" ] ; then
    echo 'vPing OK'
   break
   else
    echo 'vPing KO'
   fi
   sleep 1
  done

  vPing_userdata- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  vPing_userdata- INFO - Waiting for ping...
  vPing_userdata- INFO - vPing detected!
  vPing_userdata- INFO - vPing duration:'24.4'
  vPing_userdata- INFO - vPing OK
  vPing_userdata- INFO - Cleaning up...
  vPing_userdata- INFO - Deleting network 'vping-net'...


Tempest
^^^^^^^
::

  FUNCTEST.info: Running Tempest tests...
  run_tempest - INFO - Creating tenant and user for Tempest suite
  2016-02-23 04:37:19.865 23855 INFO rally.verification.tempest.tempest [-] Starting: Creating configuration file for Tempest.
  2016-02-23 04:37:24.332 23855 INFO rally.verification.tempest.tempest [-] Completed: Creating configuration file for Tempest.

  run_tempest - INFO - Starting Tempest test suite: '--tests-file /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/custom_tests/test_list.txt'.
  Total results of verification:

  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | UUID                                 | Deployment UUID                      | Set name | Tests | Failures | Created at                 | Status   |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | 28be74fb-34e0-4247-833c-a8c5b3fd85d2 | d2a31b24-70b3-48ab-bd03-8d7a0dab20bd |          | 210   | 0        | 2016-02-23 04:37:25.793306 | finished |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+

  Tests:

  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | name                                                                                                                                     | time      | status  |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.20837   | success |
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.20097   | success |
  | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 27.41889  | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 6.64765   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 7.27470   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.06285   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.06897   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.06414   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.11873   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.06762   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.06739   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.06986   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.06254   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.05104   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.12018   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.07818   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.10564   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.06481   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 0.30634   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 1.20722   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.13093   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 0.38276   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 0.54540   | success |
  | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 3.33321   | success |
  | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 17.36469  | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 3.15517   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.06856   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.18377   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 0.16882   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.00068   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 3.15690   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.07962   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.15120   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 0.18218   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.00110   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.06973   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 6.27398   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.20951   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.18499   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.15917   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.31948   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.14946   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.07635   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.07788   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.06447   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.05937   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.07365   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.19332   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00071   | skip    |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.15138   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.06312   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.01957   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.07095   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.08593   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.01455   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.01158   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.04029   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.06225   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.06189   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.26184   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.02082   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.06492   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.00083   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 3.32560   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 8.17266   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 8.58619   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.29429   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 79.87435  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 14.54175  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 23.12381  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 6.94824   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.08712   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.16214   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.68228   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.29523   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.35906   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.68377   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.54206   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.55368   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 2.45879   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 29.40153  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 25.63768  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 14.29183  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 12.85255  | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 0.59683   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 0.78070   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 0.64926   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 0.79184   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 0.62816   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 0.67889   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 0.91872   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 0.67651   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 0.39363   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.50851   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 0.57311   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 0.45111   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 0.39532   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 0.43734   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.62367   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 0.59665   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.38844   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 1.29632   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 0.34865   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 0.46513   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 0.41424   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.08979   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.01101   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 0.07763   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.01368   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 0.50557   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.08336   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.23059   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.05377   | success |
  | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 42.94954  | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.65627   | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.08496   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.09567   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.00685   | success |
  | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.20509   | success |
  | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.12058   | success |
  | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.13306   | success |
  | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.03344   | success |
  | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 0.28451   | success |
  | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.15089   | success |
  | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 0.93789   | success |
  | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.11553   | success |
  | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.11774   | success |
  | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.20859   | success |
  | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.15701   | success |
  | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 0.84413   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.02197   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.01614   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.01513   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.01626   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.01377   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.01219   | success |
  | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.06385   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 0.74490   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 0.30669   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 0.42703   | success |
  | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 0.46679   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 1.11398   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 1.40153   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 0.62250   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 1.06048   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 3.64767   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 1.05674   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 1.46703   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 1.15288   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 1.19505   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.18705   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.16809   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.06150   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.06589   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.03918   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 1.09078   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.12778   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.04437   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.07037   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.08725   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.03485   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 0.94866   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 1.57085   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 0.63361   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.05208   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.04959   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 1.22772   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 1.51603   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 0.89179   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.16512   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.05618   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 4.21613   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 1.92424   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 1.44097   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 1.08964   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 3.05695   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 1.48158   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 1.24519   | success |
  | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 1.01040   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 0.40816   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 0.55388   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.02194   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 0.51425   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 0.62336   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.02465   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.31894   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 6.32025   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.02302   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 0.66552   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.40307   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.43128   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.50089   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.47817   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.50681   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 3.37768   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.07322   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 0.82997   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 1.47396   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 2.64936   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 1.83658   | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 12.39640  | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 11.41953  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 11.27254  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 11.80658  | success |
  | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.05079   | success |
  | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.05690   | success |
  | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 44.43032  | success |
  | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 21.90475  | success |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 121.16825 | success |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 117.34801 | success |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  run_tempest - INFO - Results: {'timestart': '2016-02-2304:37:25.793306', 'duration': 261, 'tests': 210, 'failures': 0}
  run_tempest - INFO - Pushing results to DB: 'http://testresults.opnfv.org/testapi/results'.
  run_tempest - INFO - Deleting tenant and user for Tempest suite)


Rally
^^^^^
::

  FUNCTEST.info: Running Rally benchmark suite...
  run_rally - INFO - Starting test scenario "authenticate" ...
  run_rally - INFO -
   Preparing input task
   Task  d78a7e66-b2a5-42de-ac0c-cc6145aaa77a: started
  Task d78a7e66-b2a5-42de-ac0c-cc6145aaa77a: finished

  test scenario Authenticate.validate_glance
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_glance     | 0.122 | 0.136  | 0.153  | 0.155  | 0.158 | 0.138 | 100.0%  | 10    |
  | authenticate.validate_glance (2) | 0.039 | 0.045  | 0.056  | 0.06   | 0.064 | 0.047 | 100.0%  | 10    |
  | total                            | 0.227 | 0.264  | 0.28   | 0.283  | 0.285 | 0.26  | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.795955181122
  Full duration: 2.89371585846

  test scenario Authenticate.keystone
  +-----------------------------------------------------------------------------+
  |                            Response Times (sec)                             |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | total  | 0.064 | 0.077  | 0.097  | 0.114  | 0.131 | 0.081 | 100.0%  | 10    |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.246862888336
  Full duration: 2.44218397141

  test scenario Authenticate.validate_heat
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_heat     | 0.127 | 0.151  | 0.186  | 0.195  | 0.205 | 0.157 | 100.0%  | 10    |
  | authenticate.validate_heat (2) | 0.026 | 0.09   | 0.113  | 0.133  | 0.153 | 0.08  | 100.0%  | 10    |
  | total                          | 0.228 | 0.319  | 0.383  | 0.402  | 0.422 | 0.321 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.963713884354
  Full duration: 3.11927700043

  test scenario Authenticate.validate_nova
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_nova     | 0.104 | 0.122  | 0.133  | 0.139  | 0.144 | 0.121 | 100.0%  | 10    |
  | authenticate.validate_nova (2) | 0.028 | 0.031  | 0.04   | 0.041  | 0.042 | 0.034 | 100.0%  | 10    |
  | total                          | 0.2   | 0.243  | 0.249  | 0.256  | 0.263 | 0.235 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.704430103302
  Full duration: 2.78888607025

  test scenario Authenticate.validate_cinder
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_cinder     | 0.102 | 0.117  | 0.131  | 0.139  | 0.147 | 0.119 | 100.0%  | 10    |
  | authenticate.validate_cinder (2) | 0.019 | 0.076  | 0.083  | 0.085  | 0.087 | 0.071 | 100.0%  | 10    |
  | total                            | 0.229 | 0.263  | 0.304  | 0.317  | 0.331 | 0.269 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.82511305809
  Full duration: 2.97128987312

  test scenario Authenticate.validate_neutron
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_neutron     | 0.111 | 0.12   | 0.134  | 0.135  | 0.135 | 0.123 | 100.0%  | 10    |
  | authenticate.validate_neutron (2) | 0.03  | 0.086  | 0.104  | 0.104  | 0.104 | 0.084 | 100.0%  | 10    |
  | total                             | 0.22  | 0.28   | 0.307  | 0.31   | 0.312 | 0.278 | 100.0%  | 10    |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.855668067932
  Full duration: 3.13501811028

  run_rally - INFO - Test scenario: "authenticate" OK.
  run_rally - INFO - Starting test scenario "glance" ...
  run_rally - INFO -
   Preparing input task
   Task  3234c959-6176-4a4f-adf4-50f3f3083d67: started
  Task 3234c959-6176-4a4f-adf4-50f3f3083d67: finished

  test scenario GlanceImages.list_images
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.list_images | 0.189 | 0.215  | 0.246  | 0.252  | 0.258 | 0.218 | 100.0%  | 10    |
  | total              | 0.189 | 0.215  | 0.246  | 0.252  | 0.258 | 0.218 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.649740934372
  Full duration: 3.67985486984

  test scenario GlanceImages.create_image_and_boot_instances
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | glance.create_image | 2.782  | 3.177  | 3.617  | 3.638  | 3.659  | 3.198  | 100.0%  | 10    |
  | nova.boot_servers   | 9.48   | 13.931 | 17.26  | 17.274 | 17.287 | 13.824 | 100.0%  | 10    |
  | total               | 12.296 | 16.956 | 20.848 | 20.857 | 20.866 | 17.022 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 49.9618289471
  Full duration: 73.9044458866

  test scenario GlanceImages.create_and_list_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 2.779 | 3.406  | 3.655  | 3.673  | 3.692 | 3.306 | 100.0%  | 10    |
  | glance.list_images  | 0.039 | 0.046  | 0.048  | 0.049  | 0.049 | 0.045 | 100.0%  | 10    |
  | total               | 2.82  | 3.453  | 3.703  | 3.722  | 3.741 | 3.351 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.77695393562
  Full duration: 14.4172940254

  test scenario GlanceImages.create_and_delete_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 2.788 | 3.69   | 3.785  | 3.83   | 3.876 | 3.489 | 100.0%  | 10    |
  | glance.delete_image | 0.129 | 0.146  | 0.203  | 0.239  | 0.275 | 0.166 | 100.0%  | 10    |
  | total               | 2.933 | 3.884  | 3.951  | 3.986  | 4.02  | 3.655 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 10.762845993
  Full duration: 13.6261451244

  run_rally - INFO - Test scenario: "glance" OK.
  run_rally - INFO - Starting test scenario "cinder" ...
  run_rally - INFO -
   Preparing input task
   Task  21cb74f0-6bd9-44e3-aff3-99085ad0525f: started
  Task 21cb74f0-6bd9-44e3-aff3-99085ad0525f: finished

  test scenario CinderVolumes.create_and_attach_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server     | 7.723  | 10.184 | 13.839 | 13.936 | 14.032 | 10.913 | 100.0%  | 10    |
  | cinder.create_volume | 2.731  | 2.833  | 2.935  | 3.005  | 3.076  | 2.847  | 100.0%  | 10    |
  | nova.attach_volume   | 7.613  | 7.977  | 8.755  | 9.542  | 10.33  | 8.197  | 100.0%  | 10    |
  | nova.detach_volume   | 3.034  | 3.429  | 5.352  | 5.414  | 5.476  | 4.052  | 100.0%  | 10    |
  | cinder.delete_volume | 2.44   | 2.495  | 2.591  | 2.6    | 2.609  | 2.503  | 100.0%  | 10    |
  | nova.delete_server   | 2.423  | 2.508  | 2.823  | 3.661  | 4.499  | 2.704  | 100.0%  | 10    |
  | total                | 28.081 | 29.986 | 35.858 | 36.584 | 37.309 | 31.218 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 93.1938638687
  Full duration: 105.67930007

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.887 | 5.424  | 5.581  | 5.636  | 5.69  | 4.98  | 100.0%  | 10    |
  | cinder.list_volumes  | 0.079 | 0.157  | 0.177  | 0.182  | 0.186 | 0.147 | 100.0%  | 10    |
  | total                | 2.966 | 5.594  | 5.745  | 5.781  | 5.817 | 5.127 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.3176538944
  Full duration: 25.6212191582

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.813 | 2.965  | 3.036  | 3.048  | 3.059 | 2.962 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.08  | 0.127  | 0.142  | 0.161  | 0.18  | 0.128 | 100.0%  | 10    |
  | total                | 2.893 | 3.093  | 3.178  | 3.209  | 3.239 | 3.09  | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.30827403069
  Full duration: 19.9378697872

  test scenario CinderVolumes.create_and_list_snapshots
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.438 | 2.526  | 2.593  | 2.593  | 2.593 | 2.528 | 100.0%  | 10    |
  | cinder.list_snapshots  | 0.018 | 0.088  | 0.099  | 0.104  | 0.109 | 0.083 | 100.0%  | 10    |
  | total                  | 2.523 | 2.613  | 2.683  | 2.687  | 2.692 | 2.611 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 7.79824590683
  Full duration: 31.6265990734

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.891 | 3.012  | 3.068  | 3.069  | 3.069 | 2.987 | 100.0%  | 10    |
  | cinder.delete_volume | 2.505 | 2.583  | 2.686  | 2.713  | 2.739 | 2.598 | 100.0%  | 10    |
  | total                | 5.445 | 5.6    | 5.697  | 5.7    | 5.703 | 5.586 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.8130619526
  Full duration: 23.3862919807

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 3.06  | 5.419  | 5.676  | 5.725  | 5.774 | 4.793 | 100.0%  | 10    |
  | cinder.delete_volume | 2.457 | 2.536  | 2.613  | 2.63   | 2.648 | 2.548 | 100.0%  | 10    |
  | total                | 5.557 | 7.997  | 8.239  | 8.276  | 8.313 | 7.341 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 21.6966080666
  Full duration: 28.6927661896

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.819 | 2.943  | 3.235  | 3.249  | 3.264 | 3.001 | 100.0%  | 10    |
  | cinder.delete_volume | 2.545 | 2.581  | 2.665  | 2.684  | 2.702 | 2.603 | 100.0%  | 10    |
  | total                | 5.375 | 5.546  | 5.826  | 5.896  | 5.966 | 5.604 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.8036949635
  Full duration: 23.085185051

  test scenario CinderVolumes.create_and_upload_volume_to_image
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume          | 2.833  | 3.116  | 3.438  | 3.496  | 3.553  | 3.134  | 100.0%  | 10    |
  | cinder.upload_volume_to_image | 25.838 | 62.678 | 78.019 | 78.434 | 78.85  | 55.7   | 100.0%  | 10    |
  | cinder.delete_volume          | 2.358  | 2.511  | 2.619  | 2.684  | 2.749  | 2.531  | 100.0%  | 10    |
  | nova.delete_image             | 0.221  | 0.371  | 3.025  | 13.33  | 23.635 | 2.707  | 100.0%  | 10    |
  | total                         | 31.573 | 68.573 | 83.845 | 84.418 | 84.99  | 64.072 | 100.0%  | 10    |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 182.231485128
  Full duration: 189.13320303

  test scenario CinderVolumes.create_and_delete_snapshot
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.43  | 2.545  | 2.599  | 2.6    | 2.602 | 2.539 | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.326 | 2.495  | 2.611  | 2.675  | 2.739 | 2.493 | 100.0%  | 10    |
  | total                  | 4.887 | 5.04   | 5.173  | 5.186  | 5.199 | 5.032 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.9942228794
  Full duration: 33.8261451721

  test scenario CinderVolumes.create_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.829 | 2.973  | 3.402  | 3.412  | 3.422 | 3.063 | 100.0%  | 10    |
  | total                | 2.829 | 2.973  | 3.403  | 3.412  | 3.422 | 3.063 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.0781109333
  Full duration: 18.1423990726

  test scenario CinderVolumes.create_volume
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +----------------------+------+--------+--------+--------+------+-------+---------+-------+
  | action               | min  | median | 90%ile | 95%ile | max  | avg   | success | count |
  +----------------------+------+--------+--------+--------+------+-------+---------+-------+
  | cinder.create_volume | 2.85 | 2.939  | 2.978  | 2.984  | 2.99 | 2.932 | 100.0%  | 10    |
  | total                | 2.85 | 2.94   | 2.978  | 2.984  | 2.99 | 2.932 | 100.0%  | 10    |
  +----------------------+------+--------+--------+--------+------+-------+---------+-------+
  Load duration: 8.73497700691
  Full duration: 19.4855289459

  test scenario CinderVolumes.list_volumes
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.list_volumes | 0.211 | 0.266  | 0.312  | 0.327  | 0.342 | 0.274 | 100.0%  | 10    |
  | total               | 0.211 | 0.266  | 0.312  | 0.327  | 0.342 | 0.275 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.827063083649
  Full duration: 47.6483559608

  test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.852  | 3.009  | 3.091  | 3.106  | 3.122  | 3.005  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.321  | 2.392  | 2.404  | 2.404  | 2.405  | 2.377  | 100.0%  | 10    |
  | nova.attach_volume     | 5.473  | 7.981  | 11.399 | 12.215 | 13.031 | 8.96   | 100.0%  | 10    |
  | nova.detach_volume     | 3.035  | 5.168  | 5.603  | 5.772  | 5.941  | 4.587  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.209  | 2.347  | 2.41   | 2.417  | 2.424  | 2.349  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.412  | 2.494  | 2.582  | 2.616  | 2.65   | 2.508  | 100.0%  | 10    |
  | total                  | 21.417 | 23.884 | 26.577 | 26.903 | 27.228 | 24.098 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 70.9750390053
  Full duration: 126.263324976

  test scenario CinderVolumes.create_from_volume_and_delete_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 9.872  | 12.204 | 17.525 | 19.351 | 21.177 | 13.167 | 100.0%  | 10    |
  | cinder.delete_volume | 2.325  | 2.554  | 2.928  | 3.924  | 4.92   | 2.779  | 100.0%  | 10    |
  | total                | 12.426 | 14.781 | 20.202 | 21.897 | 23.592 | 15.947 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 43.4407100677
  Full duration: 62.327357769

  test scenario CinderVolumes.create_and_extend_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.858 | 2.94   | 3.074  | 3.087  | 3.1   | 2.956 | 100.0%  | 10    |
  | cinder.extend_volume | 2.572 | 2.848  | 2.884  | 2.919  | 2.954 | 2.8   | 100.0%  | 10    |
  | cinder.delete_volume | 2.433 | 2.567  | 2.67   | 2.693  | 2.716 | 2.567 | 100.0%  | 10    |
  | total                | 7.982 | 8.292  | 8.558  | 8.616  | 8.674 | 8.323 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.9033889771
  Full duration: 31.5932898521

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.882  | 2.947  | 3.229  | 3.231  | 3.233  | 3.005  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.268  | 2.345  | 2.421  | 2.456  | 2.491  | 2.36   | 100.0%  | 10    |
  | nova.attach_volume     | 7.593  | 8.071  | 12.707 | 13.727 | 14.747 | 9.373  | 100.0%  | 10    |
  | nova.detach_volume     | 2.962  | 5.331  | 5.412  | 5.491  | 5.57   | 5.076  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.185  | 2.286  | 2.366  | 2.374  | 2.381  | 2.298  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.425  | 2.524  | 2.593  | 2.61   | 2.627  | 2.52   | 100.0%  | 10    |
  | total                  | 21.713 | 23.963 | 28.368 | 29.657 | 30.947 | 24.974 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 73.7474370003
  Full duration: 132.963656902

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.739  | 2.89   | 3.033  | 3.058  | 3.084  | 2.914  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.247  | 2.401  | 2.466  | 2.485  | 2.503  | 2.388  | 100.0%  | 10    |
  | nova.attach_volume     | 7.882  | 8.891  | 10.439 | 11.312 | 12.186 | 9.222  | 100.0%  | 10    |
  | nova.detach_volume     | 2.94   | 5.373  | 5.635  | 5.661  | 5.687  | 4.764  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.283  | 2.332  | 2.481  | 2.585  | 2.688  | 2.381  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.425  | 2.495  | 2.547  | 2.558  | 2.569  | 2.489  | 100.0%  | 10    |
  | total                  | 21.386 | 24.555 | 26.13  | 26.247 | 26.365 | 24.746 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 76.0001449585
  Full duration: 139.533368111

  run_rally - INFO - Test scenario: "cinder" OK.
  run_rally - INFO - Starting test scenario "heat" ...
  run_rally - INFO -
   Preparing input task
   Task  7d1551b5-51d4-480b-816d-571bc61773ac: started
  Task 7d1551b5-51d4-480b-816d-571bc61773ac: finished

  test scenario HeatStacks.create_suspend_resume_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack  | 2.896 | 3.025  | 3.297  | 3.342  | 3.386 | 3.075 | 100.0%  | 10    |
  | heat.suspend_stack | 0.444 | 1.622  | 1.791  | 1.817  | 1.844 | 1.332 | 100.0%  | 10    |
  | heat.resume_stack  | 1.365 | 1.657  | 1.701  | 1.755  | 1.809 | 1.598 | 100.0%  | 10    |
  | heat.delete_stack  | 0.499 | 1.531  | 1.644  | 1.655  | 1.665 | 1.451 | 100.0%  | 10    |
  | total              | 5.782 | 7.652  | 8.146  | 8.28   | 8.414 | 7.455 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 21.9193868637
  Full duration: 25.3411290646

  test scenario HeatStacks.create_and_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 3.023 | 3.144  | 3.331  | 3.531  | 3.73  | 3.206 | 100.0%  | 10    |
  | heat.delete_stack | 0.437 | 0.646  | 1.617  | 1.676  | 1.734 | 0.972 | 100.0%  | 10    |
  | total             | 3.54  | 3.767  | 4.914  | 5.114  | 5.314 | 4.178 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 12.2326231003
  Full duration: 15.3595271111

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 14.933 | 16.348 | 17.828 | 18.321 | 18.813 | 16.471 | 100.0%  | 10    |
  | heat.delete_stack | 6.665  | 8.038  | 8.335  | 8.772  | 9.208  | 7.711  | 100.0%  | 10    |
  | total             | 22.386 | 24.346 | 25.661 | 25.74  | 25.818 | 24.182 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 72.8466770649
  Full duration: 76.0618572235

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 16.663 | 19.357 | 20.553 | 21.32  | 22.088 | 19.17  | 100.0%  | 10    |
  | heat.delete_stack | 9.144  | 9.269  | 10.036 | 10.227 | 10.417 | 9.461  | 100.0%  | 10    |
  | total             | 25.982 | 28.953 | 30.462 | 30.847 | 31.232 | 28.631 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 84.6888990402
  Full duration: 88.1814341545

  test scenario HeatStacks.list_stacks_and_resources
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.list_stacks                | 0.219 | 0.246  | 0.383  | 0.4    | 0.417 | 0.287 | 100.0%  | 10    |
  | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0   | 0.0   | 100.0%  | 10    |
  | total                           | 0.219 | 0.246  | 0.383  | 0.4    | 0.418 | 0.287 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.863615989685
  Full duration: 3.55412602425

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.866 | 3.102  | 3.266  | 3.29   | 3.314 | 3.097 | 100.0%  | 10    |
  | heat.update_stack | 2.641 | 3.637  | 3.803  | 3.813  | 3.822 | 3.497 | 100.0%  | 10    |
  | heat.delete_stack | 1.394 | 1.515  | 1.651  | 1.666  | 1.681 | 1.534 | 100.0%  | 10    |
  | total             | 7.247 | 8.255  | 8.454  | 8.543  | 8.631 | 8.127 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.2989928722
  Full duration: 27.7337241173

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.799 | 3.033  | 3.19   | 3.306  | 3.422 | 3.046 | 100.0%  | 10    |
  | heat.update_stack | 2.509 | 3.732  | 3.845  | 3.847  | 3.849 | 3.321 | 100.0%  | 10    |
  | heat.delete_stack | 1.302 | 1.538  | 1.641  | 1.733  | 1.824 | 1.542 | 100.0%  | 10    |
  | total             | 7.14  | 8.084  | 8.351  | 8.371  | 8.39  | 7.909 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 23.4465420246
  Full duration: 27.0243220329

  test scenario HeatStacks.create_update_delete_stack
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 2.894 | 3.127  | 3.22   | 3.399  | 3.579  | 3.129  | 100.0%  | 10    |
  | heat.update_stack | 4.739 | 5.169  | 6.092  | 6.105  | 6.119  | 5.309  | 100.0%  | 10    |
  | heat.delete_stack | 1.422 | 1.839  | 2.562  | 2.565  | 2.567  | 1.989  | 100.0%  | 10    |
  | total             | 9.674 | 10.622 | 10.9   | 10.921 | 10.941 | 10.427 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 30.9374701977
  Full duration: 34.6409509182

  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 6.25441002846
  Full duration: 14.2524240017

  test scenario HeatStacks.create_update_delete_stack
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 2.776 | 3.256  | 3.502  | 3.878  | 4.255  | 3.292  | 100.0%  | 10    |
  | heat.update_stack | 4.632 | 4.964  | 5.353  | 5.818  | 6.284  | 5.076  | 100.0%  | 10    |
  | heat.delete_stack | 1.439 | 2.134  | 2.645  | 2.668  | 2.691  | 2.088  | 100.0%  | 10    |
  | total             | 9.373 | 10.496 | 11.129 | 11.584 | 12.039 | 10.455 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 31.1429200172
  Full duration: 34.8937320709

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.804 | 3.071  | 3.166  | 3.186  | 3.206 | 3.026 | 100.0%  | 10    |
  | heat.update_stack | 2.737 | 3.748  | 4.018  | 4.043  | 4.068 | 3.617 | 100.0%  | 10    |
  | heat.delete_stack | 1.31  | 1.555  | 1.823  | 1.832  | 1.841 | 1.569 | 100.0%  | 10    |
  | total             | 7.424 | 8.294  | 8.696  | 8.74   | 8.783 | 8.212 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.5028841496
  Full duration: 28.3026170731

  test scenario HeatStacks.create_and_list_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.956 | 3.13   | 3.324  | 3.341  | 3.359 | 3.141 | 100.0%  | 10    |
  | heat.list_stacks  | 0.033 | 0.168  | 0.248  | 0.276  | 0.304 | 0.14  | 100.0%  | 10    |
  | total             | 3.124 | 3.262  | 3.41   | 3.453  | 3.497 | 3.281 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 10.0396568775
  Full duration: 17.6087501049

  test scenario HeatStacks.create_check_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.922 | 3.155  | 3.412  | 3.413  | 3.415 | 3.159 | 100.0%  | 10    |
  | heat.check_stack  | 0.418 | 0.518  | 1.02   | 1.361  | 1.702 | 0.701 | 100.0%  | 10    |
  | heat.delete_stack | 0.687 | 1.665  | 1.773  | 1.786  | 1.799 | 1.56  | 100.0%  | 10    |
  | total             | 4.445 | 5.362  | 5.863  | 6.138  | 6.413 | 5.42  | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.1680779457
  Full duration: 20.0481300354

  run_rally - INFO - Test scenario: "heat" Failed.
  run_rally - INFO - Starting test scenario "keystone" ...
  run_rally - INFO -
   Preparing input task
   Task  5cfc1b63-088e-4840-a525-13064451e8d6: started
  Task 5cfc1b63-088e-4840-a525-13064451e8d6: finished

  test scenario KeystoneBasic.create_tenant_with_users
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.105 | 0.119  | 0.16   | 0.16   | 0.161 | 0.125 | 100.0%  | 10    |
  | keystone.create_users  | 0.592 | 0.653  | 0.694  | 0.719  | 0.744 | 0.657 | 100.0%  | 10    |
  | total                  | 0.706 | 0.77   | 0.844  | 0.874  | 0.905 | 0.782 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.32407808304
  Full duration: 12.4144320488

  test scenario KeystoneBasic.create_add_and_list_user_roles
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.116 | 0.119  | 0.144  | 0.149  | 0.154 | 0.125 | 100.0%  | 10    |
  | keystone.add_role    | 0.088 | 0.099  | 0.107  | 0.107  | 0.107 | 0.099 | 100.0%  | 10    |
  | keystone.list_roles  | 0.054 | 0.058  | 0.095  | 0.097  | 0.1   | 0.067 | 100.0%  | 10    |
  | total                | 0.27  | 0.28   | 0.345  | 0.35   | 0.355 | 0.292 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.863723993301
  Full duration: 6.29958295822

  test scenario KeystoneBasic.add_and_remove_user_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.121 | 0.217  | 0.274  | 0.281  | 0.288 | 0.2   | 100.0%  | 10    |
  | keystone.add_role    | 0.089 | 0.092  | 0.098  | 0.098  | 0.099 | 0.093 | 100.0%  | 10    |
  | keystone.remove_role | 0.058 | 0.061  | 0.156  | 0.161  | 0.167 | 0.081 | 100.0%  | 10    |
  | total                | 0.274 | 0.371  | 0.497  | 0.517  | 0.537 | 0.373 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.090020895
  Full duration: 6.37877011299

  test scenario KeystoneBasic.create_update_and_delete_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.123 | 0.223  | 0.286  | 0.291  | 0.296 | 0.209 | 100.0%  | 10    |
  | keystone.update_tenant | 0.052 | 0.056  | 0.065  | 0.066  | 0.068 | 0.057 | 100.0%  | 10    |
  | keystone.delete_tenant | 0.125 | 0.135  | 0.286  | 0.307  | 0.327 | 0.18  | 100.0%  | 10    |
  | total                  | 0.302 | 0.416  | 0.63   | 0.632  | 0.634 | 0.446 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.29043102264
  Full duration: 5.07875084877

  test scenario KeystoneBasic.create_and_delete_service
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_service | 0.109 | 0.123  | 0.128  | 0.132  | 0.135 | 0.122 | 100.0%  | 10    |
  | keystone.delete_service | 0.059 | 0.07   | 0.121  | 0.128  | 0.134 | 0.079 | 100.0%  | 10    |
  | total                   | 0.174 | 0.196  | 0.234  | 0.245  | 0.255 | 0.201 | 100.0%  | 10    |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.603389024734
  Full duration: 4.27351093292

  test scenario KeystoneBasic.create_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.118 | 0.133  | 0.186  | 0.187  | 0.188 | 0.142 | 100.0%  | 10    |
  | total                  | 0.118 | 0.133  | 0.186  | 0.187  | 0.188 | 0.142 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.428766012192
  Full duration: 4.18886899948

  test scenario KeystoneBasic.create_user
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +----------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg  | success | count |
  +----------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | keystone.create_user | 0.137 | 0.138  | 0.145  | 0.145  | 0.146 | 0.14 | 100.0%  | 10    |
  | total                | 0.137 | 0.138  | 0.145  | 0.145  | 0.146 | 0.14 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+------+---------+-------+
  Load duration: 0.443462133408
  Full duration: 4.19236207008

  test scenario KeystoneBasic.create_and_list_tenants
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.111 | 0.117  | 0.165  | 0.178  | 0.191 | 0.132 | 100.0%  | 10    |
  | keystone.list_tenants  | 0.046 | 0.055  | 0.065  | 0.066  | 0.067 | 0.055 | 100.0%  | 10    |
  | total                  | 0.163 | 0.179  | 0.214  | 0.231  | 0.247 | 0.187 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.561487913132
  Full duration: 5.7246799469

  test scenario KeystoneBasic.create_and_delete_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.12  | 0.232  | 0.282  | 0.289  | 0.296 | 0.206 | 100.0%  | 10    |
  | keystone.delete_role | 0.104 | 0.117  | 0.133  | 0.169  | 0.206 | 0.124 | 100.0%  | 10    |
  | total                | 0.239 | 0.342  | 0.401  | 0.452  | 0.502 | 0.33  | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.990566015244
  Full duration: 4.97686004639

  test scenario KeystoneBasic.get_entities
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.106 | 0.133  | 0.16   | 0.174  | 0.187 | 0.139 | 100.0%  | 10    |
  | keystone.create_user   | 0.058 | 0.066  | 0.07   | 0.071  | 0.071 | 0.065 | 100.0%  | 10    |
  | keystone.create_role   | 0.046 | 0.053  | 0.07   | 0.086  | 0.103 | 0.059 | 100.0%  | 10    |
  | keystone.get_tenant    | 0.044 | 0.048  | 0.055  | 0.076  | 0.098 | 0.053 | 100.0%  | 10    |
  | keystone.get_user      | 0.051 | 0.057  | 0.063  | 0.063  | 0.063 | 0.057 | 100.0%  | 10    |
  | keystone.get_role      | 0.044 | 0.047  | 0.055  | 0.056  | 0.058 | 0.049 | 100.0%  | 10    |
  | keystone.service_list  | 0.045 | 0.049  | 0.06   | 0.081  | 0.101 | 0.054 | 100.0%  | 10    |
  | keystone.get_service   | 0.043 | 0.049  | 0.062  | 0.079  | 0.097 | 0.053 | 100.0%  | 10    |
  | total                  | 0.475 | 0.518  | 0.577  | 0.6    | 0.622 | 0.529 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.58831310272
  Full duration: 9.76444888115

  test scenario KeystoneBasic.create_and_list_users
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.13  | 0.145  | 0.177  | 0.195  | 0.213 | 0.152 | 100.0%  | 10    |
  | keystone.list_users  | 0.052 | 0.055  | 0.08   | 0.093  | 0.106 | 0.062 | 100.0%  | 10    |
  | total                | 0.183 | 0.2    | 0.269  | 0.274  | 0.279 | 0.214 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.642003059387
  Full duration: 4.59805297852

  run_rally - INFO - Test scenario: "keystone" OK.
  run_rally - INFO - Starting test scenario "neutron" ...
  run_rally - INFO -
   Preparing input task
   Task  aa890d07-7f64-4bf2-9cc1-adb8d5a95c9e: started
  Task aa890d07-7f64-4bf2-9cc1-adb8d5a95c9e: finished

  test scenario NeutronNetworks.create_and_delete_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.42  | 0.516  | 0.669  | 0.677  | 0.684 | 0.538 | 100.0%  | 10    |
  | neutron.delete_port | 0.149 | 0.287  | 0.338  | 0.344  | 0.349 | 0.274 | 100.0%  | 10    |
  | total               | 0.65  | 0.787  | 0.989  | 0.992  | 0.996 | 0.812 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.28342914581
  Full duration: 25.3548538685

  test scenario NeutronNetworks.create_and_list_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.389 | 0.492  | 0.542  | 0.564  | 0.587 | 0.479 | 100.0%  | 10    |
  | neutron.create_router        | 0.034 | 0.165  | 0.179  | 0.18   | 0.181 | 0.118 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.273 | 0.398  | 0.459  | 0.475  | 0.492 | 0.378 | 100.0%  | 10    |
  | neutron.list_routers         | 0.042 | 0.111  | 0.208  | 0.214  | 0.219 | 0.12  | 100.0%  | 10    |
  | total                        | 0.873 | 1.083  | 1.266  | 1.32   | 1.373 | 1.095 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.14495706558
  Full duration: 27.2623529434

  test scenario NeutronNetworks.create_and_delete_routers
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet           | 0.421 | 0.528  | 0.576  | 0.593  | 0.609 | 0.516 | 100.0%  | 10    |
  | neutron.create_router           | 0.037 | 0.174  | 0.193  | 0.194  | 0.196 | 0.138 | 100.0%  | 10    |
  | neutron.add_interface_router    | 0.372 | 0.44   | 0.726  | 0.729  | 0.732 | 0.499 | 100.0%  | 10    |
  | neutron.remove_interface_router | 0.231 | 0.385  | 0.445  | 0.495  | 0.545 | 0.365 | 100.0%  | 10    |
  | neutron.delete_router           | 0.155 | 0.243  | 0.363  | 0.374  | 0.385 | 0.257 | 100.0%  | 10    |
  | total                           | 1.492 | 1.722  | 2.126  | 2.135  | 2.145 | 1.776 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 5.06723308563
  Full duration: 27.7173280716

  test scenario NeutronNetworks.create_and_list_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.429 | 0.479  | 0.682  | 0.709  | 0.736 | 0.518 | 100.0%  | 10    |
  | neutron.list_ports  | 0.101 | 0.302  | 0.368  | 0.377  | 0.386 | 0.267 | 100.0%  | 10    |
  | total               | 0.565 | 0.819  | 0.9    | 0.971  | 1.042 | 0.785 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.22692918777
  Full duration: 25.9097590446

  test scenario NeutronNetworks.create_and_delete_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.383 | 0.414  | 0.558  | 0.562  | 0.565 | 0.439 | 100.0%  | 10    |
  | neutron.delete_subnet | 0.134 | 0.271  | 0.307  | 0.34   | 0.372 | 0.235 | 100.0%  | 10    |
  | total                 | 0.522 | 0.677  | 0.872  | 0.901  | 0.93  | 0.674 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.97971510887
  Full duration: 24.8733260632

  test scenario NeutronNetworks.create_and_delete_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.3   | 0.32   | 0.403  | 0.407  | 0.411 | 0.338 | 100.0%  | 10    |
  | neutron.delete_network | 0.107 | 0.248  | 0.316  | 0.32   | 0.325 | 0.228 | 100.0%  | 10    |
  | total                  | 0.411 | 0.556  | 0.697  | 0.698  | 0.699 | 0.566 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.71673607826
  Full duration: 13.4693968296

  test scenario NeutronNetworks.create_and_list_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.279 | 0.326  | 0.389  | 0.406  | 0.423 | 0.334 | 100.0%  | 10    |
  | neutron.list_networks  | 0.043 | 0.11   | 0.18   | 0.187  | 0.194 | 0.112 | 100.0%  | 10    |
  | total                  | 0.328 | 0.437  | 0.564  | 0.59   | 0.617 | 0.446 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.4160130024
  Full duration: 15.1821639538

  test scenario NeutronNetworks.create_and_update_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.401 | 0.436  | 0.454  | 0.473  | 0.492 | 0.433 | 100.0%  | 10    |
  | neutron.create_router        | 0.035 | 0.175  | 0.181  | 0.186  | 0.191 | 0.123 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.293 | 0.416  | 0.46   | 0.461  | 0.461 | 0.401 | 100.0%  | 10    |
  | neutron.update_router        | 0.131 | 0.215  | 0.311  | 0.331  | 0.35  | 0.219 | 100.0%  | 10    |
  | total                        | 1.012 | 1.171  | 1.336  | 1.359  | 1.381 | 1.176 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.52523398399
  Full duration: 28.7934508324

  test scenario NeutronNetworks.create_and_update_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.299 | 0.338  | 0.397  | 0.408  | 0.418 | 0.346 | 100.0%  | 10    |
  | neutron.update_network | 0.095 | 0.24   | 0.297  | 0.299  | 0.302 | 0.202 | 100.0%  | 10    |
  | total                  | 0.41  | 0.543  | 0.699  | 0.707  | 0.714 | 0.549 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.61482715607
  Full duration: 15.459831953

  test scenario NeutronNetworks.create_and_update_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.436 | 0.465  | 0.588  | 0.595  | 0.601 | 0.487 | 100.0%  | 10    |
  | neutron.update_port | 0.114 | 0.282  | 0.317  | 0.326  | 0.335 | 0.255 | 100.0%  | 10    |
  | total               | 0.576 | 0.751  | 0.862  | 0.899  | 0.936 | 0.742 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.15260481834
  Full duration: 25.8613479137

  test scenario NeutronNetworks.create_and_list_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.4   | 0.495  | 0.538  | 0.551  | 0.564 | 0.483 | 100.0%  | 10    |
  | neutron.list_subnets  | 0.065 | 0.217  | 0.28   | 0.319  | 0.357 | 0.22  | 100.0%  | 10    |
  | total                 | 0.563 | 0.718  | 0.793  | 0.798  | 0.802 | 0.703 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.06506896019
  Full duration: 25.971654892

  test scenario NeutronNetworks.create_and_update_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.398 | 0.465  | 0.543  | 0.564  | 0.584 | 0.475 | 100.0%  | 10    |
  | neutron.update_subnet | 0.152 | 0.178  | 0.348  | 0.366  | 0.383 | 0.234 | 100.0%  | 10    |
  | total                 | 0.557 | 0.693  | 0.85   | 0.867  | 0.883 | 0.709 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.06711506844
  Full duration: 25.9731898308

  run_rally - INFO - Test scenario: "neutron" OK.
  run_rally - INFO - Starting test scenario "nova" ...
  run_rally - INFO -
   Preparing input task
   Task  84ecab73-326c-41f9-9d80-ffb7b41c7f0d: started
  Task 84ecab73-326c-41f9-9d80-ffb7b41c7f0d: finished

  test scenario NovaKeypair.create_and_delete_keypair
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.374 | 0.484  | 0.667  | 0.672  | 0.678 | 0.503 | 100.0%  | 10    |
  | nova.delete_keypair | 0.016 | 0.021  | 0.025  | 0.027  | 0.028 | 0.021 | 100.0%  | 10    |
  | total               | 0.399 | 0.51   | 0.687  | 0.692  | 0.698 | 0.524 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.59278798103
  Full duration: 15.4121351242

  test scenario NovaServers.snapshot_server
  +--------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                       |
  +------------------------+--------+--------+---------+---------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile  | 95%ile  | max    | avg    | success | count |
  +------------------------+--------+--------+---------+---------+--------+--------+---------+-------+
  | nova.boot_server       | 9.938  | 10.314 | 11.977  | 12.384  | 12.791 | 10.711 | 100.0%  | 10    |
  | nova.create_image      | 33.802 | 39.898 | 69.264  | 70.135  | 71.005 | 45.583 | 100.0%  | 10    |
  | nova.delete_server     | 2.408  | 2.848  | 3.266   | 4.121   | 4.975  | 2.967  | 100.0%  | 10    |
  | nova.boot_server (2)   | 19.438 | 33.013 | 43.809  | 46.043  | 48.276 | 33.839 | 100.0%  | 10    |
  | nova.delete_server (2) | 2.395  | 2.453  | 4.821   | 4.891   | 4.961  | 3.009  | 100.0%  | 10    |
  | nova.delete_image      | 0.264  | 0.373  | 0.749   | 1.036   | 1.323  | 0.484  | 100.0%  | 10    |
  | total                  | 70.267 | 96.724 | 117.768 | 118.599 | 119.43 | 96.593 | 100.0%  | 10    |
  +------------------------+--------+--------+---------+---------+--------+--------+---------+-------+
  Load duration: 280.300797939
  Full duration: 304.846863985

  test scenario NovaKeypair.boot_and_delete_server_with_keypair
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_keypair | 0.406  | 0.458  | 0.533  | 0.575  | 0.616  | 0.474  | 100.0%  | 10    |
  | nova.boot_server    | 8.324  | 10.158 | 11.335 | 11.766 | 12.197 | 10.115 | 100.0%  | 10    |
  | nova.delete_server  | 2.382  | 2.425  | 2.618  | 2.621  | 2.625  | 2.456  | 100.0%  | 10    |
  | nova.delete_keypair | 0.014  | 0.019  | 0.028  | 0.029  | 0.029  | 0.02   | 100.0%  | 10    |
  | total               | 11.352 | 13.038 | 14.228 | 14.667 | 15.107 | 13.066 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 39.3250300884
  Full duration: 62.0274989605

  test scenario NovaKeypair.create_and_list_keypairs
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.389 | 0.483  | 0.646  | 0.673  | 0.701 | 0.503 | 100.0%  | 10    |
  | nova.list_keypairs  | 0.013 | 0.018  | 0.021  | 0.024  | 0.027 | 0.018 | 100.0%  | 10    |
  | total               | 0.405 | 0.504  | 0.659  | 0.688  | 0.716 | 0.521 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.55672502518
  Full duration: 16.8414058685

  test scenario NovaServers.list_servers
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.list_servers | 0.604 | 0.661  | 0.751  | 0.753  | 0.755 | 0.667 | 100.0%  | 10    |
  | total             | 0.604 | 0.661  | 0.751  | 0.753  | 0.755 | 0.667 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.98178386688
  Full duration: 66.4639019966

  test scenario NovaServers.resize_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 8.516  | 10.952 | 12.492 | 12.717 | 12.943 | 11.085 | 100.0%  | 10    |
  | nova.resize         | 21.055 | 26.446 | 42.177 | 42.263 | 42.349 | 29.612 | 100.0%  | 10    |
  | nova.resize_confirm | 2.392  | 2.451  | 2.573  | 2.592  | 2.611  | 2.47   | 100.0%  | 10    |
  | nova.delete_server  | 2.375  | 2.427  | 2.595  | 2.673  | 2.751  | 2.475  | 100.0%  | 10    |
  | total               | 34.884 | 42.48  | 59.742 | 59.88  | 60.019 | 45.642 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 133.771182775
  Full duration: 147.319270134

  test scenario NovaServers.boot_server_from_volume_and_delete
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.421  | 5.82   | 6.128  | 6.151  | 6.173  | 5.197  | 100.0%  | 10    |
  | nova.boot_server     | 13.462 | 15.116 | 17.314 | 17.513 | 17.711 | 15.217 | 100.0%  | 10    |
  | nova.delete_server   | 4.532  | 4.689  | 6.776  | 6.8    | 6.823  | 5.275  | 100.0%  | 10    |
  | total                | 21.563 | 26.332 | 28.183 | 28.315 | 28.446 | 25.689 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 76.1264929771
  Full duration: 105.501106024

  test scenario NovaServers.boot_and_migrate_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 8.668  | 10.279 | 12.669 | 12.746 | 12.824 | 10.808 | 100.0%  | 10    |
  | nova.stop_server    | 4.695  | 14.48  | 15.73  | 15.737 | 15.745 | 11.929 | 100.0%  | 10    |
  | nova.migrate        | 16.259 | 18.003 | 25.275 | 25.347 | 25.419 | 19.085 | 100.0%  | 10    |
  | nova.resize_confirm | 2.394  | 2.416  | 2.564  | 2.604  | 2.644  | 2.46   | 100.0%  | 10    |
  | nova.delete_server  | 2.383  | 2.408  | 2.55   | 2.58   | 2.61   | 2.448  | 100.0%  | 10    |
  | total               | 35.744 | 47.034 | 56.397 | 57.427 | 58.457 | 46.73  | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 131.940564156
  Full duration: 145.82509613

  test scenario NovaServers.boot_and_delete_server
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action             | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server   | 8.359  | 10.277 | 11.312 | 11.367 | 11.422 | 10.063 | 100.0%  | 10    |
  | nova.delete_server | 2.388  | 2.607  | 4.826  | 4.853  | 4.881  | 3.21   | 100.0%  | 10    |
  | total              | 11.023 | 12.798 | 15.929 | 16.116 | 16.303 | 13.273 | 100.0%  | 10    |
  +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 39.1904668808
  Full duration: 62.8628950119

  test scenario NovaServers.boot_and_rebuild_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 8.636  | 9.789  | 12.354 | 12.414 | 12.474 | 10.12  | 100.0%  | 10    |
  | nova.rebuild_server | 11.032 | 13.82  | 21.821 | 22.321 | 22.821 | 16.342 | 100.0%  | 10    |
  | nova.delete_server  | 2.382  | 2.461  | 2.664  | 2.759  | 2.854  | 2.524  | 100.0%  | 10    |
  | total               | 24.342 | 28.632 | 33.812 | 34.242 | 34.671 | 28.986 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 82.0937809944
  Full duration: 105.129650116

  test scenario NovaSecGroup.create_and_list_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.596  | 2.105  | 2.35   | 2.351  | 2.352  | 2.061  | 100.0%  | 10    |
  | nova.create_100_rules          | 8.873  | 10.349 | 10.555 | 10.65  | 10.745 | 10.067 | 100.0%  | 10    |
  | nova.list_security_groups      | 0.129  | 0.183  | 0.281  | 0.318  | 0.354  | 0.201  | 100.0%  | 10    |
  | total                          | 11.189 | 12.51  | 12.822 | 12.823 | 12.823 | 12.329 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 36.4927339554
  Full duration: 63.6400220394

  test scenario NovaSecGroup.create_and_delete_secgroups
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +--------------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.326 | 1.779  | 1.959  | 1.983  | 2.006  | 1.748  | 100.0%  | 10    |
  | nova.create_100_rules          | 9.29  | 10.389 | 10.656 | 10.731 | 10.805 | 10.241 | 100.0%  | 10    |
  | nova.delete_10_security_groups | 0.833 | 0.896  | 1.02   | 1.03   | 1.04   | 0.918  | 100.0%  | 10    |
  | total                          | 11.55 | 13.143 | 13.488 | 13.549 | 13.611 | 12.907 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 38.0758161545
  Full duration: 52.9351670742

  test scenario NovaServers.boot_and_bounce_server
  +----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                        |
  +-------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | action                  | min    | median | 90%ile  | 95%ile  | max     | avg    | success | count |
  +-------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | nova.boot_server        | 8.49   | 12.054 | 12.335  | 12.336  | 12.338  | 11.077 | 100.0%  | 10    |
  | nova.reboot_server      | 4.412  | 4.746  | 6.676   | 6.794   | 6.912   | 5.252  | 100.0%  | 10    |
  | nova.soft_reboot_server | 6.592  | 7.729  | 125.626 | 125.9   | 126.174 | 31.142 | 100.0%  | 10    |
  | nova.stop_server        | 4.709  | 4.817  | 4.999   | 5.006   | 5.013   | 4.835  | 100.0%  | 10    |
  | nova.start_server       | 2.636  | 3.348  | 4.108   | 4.153   | 4.198   | 3.361  | 100.0%  | 10    |
  | nova.rescue_server      | 6.613  | 6.787  | 17.596  | 17.726  | 17.855  | 11.037 | 100.0%  | 10    |
  | nova.unrescue_server    | 2.324  | 4.485  | 6.647   | 6.653   | 6.659   | 4.948  | 100.0%  | 10    |
  | nova.delete_server      | 2.375  | 2.416  | 4.666   | 4.731   | 4.797   | 3.1    | 100.0%  | 10    |
  | total                   | 39.617 | 54.891 | 166.239 | 170.845 | 175.451 | 74.764 | 100.0%  | 10    |
  +-------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  Load duration: 241.107405901
  Full duration: 264.433083773

  test scenario NovaServers.boot_server
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action           | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server | 9.537 | 9.723  | 12.302 | 12.597 | 12.891 | 10.539 | 100.0%  | 10    |
  | total            | 9.537 | 9.723  | 12.302 | 12.597 | 12.891 | 10.539 | 100.0%  | 10    |
  +------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 31.5377810001
  Full duration: 56.3936619759

  test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
  +-----------------------------------------------------------------------------------------------------------+
  |                                           Response Times (sec)                                            |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups    | 1.677  | 1.957  | 2.26   | 2.317  | 2.373  | 1.975  | 100.0%  | 10    |
  | nova.create_100_rules             | 9.032  | 10.031 | 10.512 | 10.585 | 10.658 | 9.992  | 100.0%  | 10    |
  | nova.boot_server                  | 8.152  | 11.436 | 11.645 | 11.66  | 11.675 | 10.446 | 100.0%  | 10    |
  | nova.get_attached_security_groups | 0.145  | 0.154  | 0.17   | 0.185  | 0.2    | 0.158  | 100.0%  | 10    |
  | nova.delete_server                | 2.412  | 4.581  | 4.637  | 4.667  | 4.696  | 3.741  | 100.0%  | 10    |
  | nova.delete_10_security_groups    | 0.791  | 0.902  | 0.983  | 0.993  | 1.003  | 0.901  | 100.0%  | 10    |
  | total                             | 22.687 | 29.402 | 29.574 | 29.639 | 29.704 | 27.213 | 100.0%  | 10    |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 81.6792809963
  Full duration: 106.045881033

  test scenario NovaServers.pause_and_unpause_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 9.557  | 11.959 | 12.616 | 12.617 | 12.618 | 11.399 | 100.0%  | 10    |
  | nova.pause_server   | 2.3    | 2.488  | 2.647  | 2.73   | 2.813  | 2.485  | 100.0%  | 10    |
  | nova.unpause_server | 2.313  | 2.338  | 2.459  | 2.519  | 2.579  | 2.376  | 100.0%  | 10    |
  | nova.delete_server  | 2.379  | 4.554  | 4.593  | 4.6    | 4.608  | 3.72   | 100.0%  | 10    |
  | total               | 16.731 | 21.47  | 21.938 | 22.069 | 22.201 | 19.98  | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 60.1143479347
  Full duration: 84.1553788185

  test scenario NovaServers.boot_server_from_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.296  | 3.584  | 6.23   | 6.254  | 6.278  | 4.296  | 100.0%  | 10    |
  | nova.boot_server     | 13.316 | 14.103 | 15.99  | 16.029 | 16.068 | 14.371 | 100.0%  | 10    |
  | total                | 16.8   | 18.338 | 20.779 | 21.536 | 22.293 | 18.667 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 55.7340800762
  Full duration: 89.9920220375

  test scenario NovaServers.boot_and_list_server
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server  | 8.714 | 10.615 | 12.468 | 12.501 | 12.535 | 10.613 | 100.0%  | 10    |
  | nova.list_servers | 0.14  | 0.241  | 0.434  | 0.454  | 0.474  | 0.274  | 100.0%  | 10    |
  | total             | 8.854 | 10.943 | 12.715 | 12.756 | 12.798 | 10.887 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 30.5609071255
  Full duration: 64.9602191448

  run_rally - INFO - Test scenario: "nova" OK.

  run_rally - INFO - Starting test scenario "quotas" ...
  run_rally - INFO -
   Preparing input task
   Task  98d9ffba-dd50-429a-ab90-4549e00b19cf: started
  Task 98d9ffba-dd50-429a-ab90-4549e00b19cf: finished

  test scenario Quotas.cinder_update
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.58 | 0.646  | 0.661  | 0.671  | 0.682 | 0.636 | 100.0%  | 10    |
  | total                | 0.58 | 0.646  | 0.661  | 0.671  | 0.682 | 0.636 | 100.0%  | 10    |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.98423290253
  Full duration: 7.3744559288

  test scenario Quotas.neutron_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.232 | 0.251  | 0.276  | 0.281  | 0.286 | 0.254 | 100.0%  | 10    |
  | total                | 0.295 | 0.324  | 0.348  | 0.352  | 0.355 | 0.325 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.987355947495
  Full duration: 6.55621004105

  test scenario Quotas.cinder_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.609 | 0.648  | 0.736  | 0.755  | 0.775 | 0.663 | 100.0%  | 10    |
  | quotas.delete_quotas | 0.267 | 0.474  | 0.498  | 0.518  | 0.539 | 0.454 | 100.0%  | 10    |
  | total                | 0.95  | 1.099  | 1.254  | 1.262  | 1.271 | 1.117 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.2654209137
  Full duration: 8.84793901443

  test scenario Quotas.nova_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.319 | 0.353  | 0.393  | 0.4    | 0.408 | 0.358 | 100.0%  | 8     |
  | quotas.delete_quotas | 0.015 | 0.025  | 0.031  | 0.032  | 0.033 | 0.025 | 75.0%   | 8     |
  | total                | 0.351 | 0.366  | 0.405  | 0.416  | 0.428 | 0.374 | 75.0%   | 8     |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.80732011795
  Full duration: 6.24122095108

  test scenario Quotas.nova_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.346 | 0.366  | 0.413  | 0.414  | 0.416 | 0.373 | 100.0%  | 10    |
  | total                | 0.346 | 0.366  | 0.413  | 0.414  | 0.416 | 0.373 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.10930514336
  Full duration: 6.21793103218

  run_rally - INFO - Test scenario: "quotas" Failed.
  run_rally - INFO - Starting test scenario "requests" ...
  run_rally - INFO -
   Preparing input task
   Task  712d1722-52e2-4e3a-93dc-515e3fea5977: started
  Task 712d1722-52e2-4e3a-93dc-515e3fea5977: finished

  test scenario HttpRequests.check_random_request
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg  | success | count |
  +------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | requests.check_request | 5.462 | 5.488  | 5.976  | 5.991  | 6.006 | 5.59 | 100.0%  | 10    |
  | total                  | 5.462 | 5.488  | 5.976  | 5.991  | 6.006 | 5.59 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  Load duration: 16.976375103
  Full duration: 19.3119690418

  test scenario HttpRequests.check_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 5.466 | 5.48   | 5.487  | 5.491  | 5.496 | 5.479 | 100.0%  | 10    |
  | total                  | 5.466 | 5.48   | 5.487  | 5.491  | 5.496 | 5.479 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.4575350285
  Full duration: 18.7219369411

  run_rally - INFO - Test scenario: "requests" OK.
  run_rally - INFO -

                       Rally Summary Report
  +===================+============+===============+===========+
  | Module            | Duration   | nb. Test Run  | Success   |
  +===================+============+===============+===========+
  | authenticate      | 00:17      | 10            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | glance            | 01:45      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | cinder            | 17:38      | 50            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | heat              | 06:53      | 32            | 92.31%    |
  +-------------------+------------+---------------+-----------+
  | keystone          | 01:07      | 29            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | neutron           | 04:41      | 31            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | nova              | 30:14      | 61            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | quotas            | 00:35      | 7             | 95.00%    |
  +-------------------+------------+---------------+-----------+
  | requests          | 00:38      | 2             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  +===================+============+===============+===========+
  | TOTAL:            | 01:03:52   | 229           | 98.59%    |
  +===================+============+===============+===========+



Feature tests
-------------

vIMS
^^^^
::

  FUNCTEST.info: Running vIMS test...
  vIMS - INFO - Prepare OpenStack plateform (create tenant and user)
  vIMS - INFO - Update OpenStack creds informations
  vIMS - INFO - Upload some OS images if it doesn't exist
  vIMS - INFO - centos_7 image doesn't exist on glance repository.
                              Try downloading this image and upload on glance !
  vIMS - INFO - ubuntu_14.04 image doesn't exist on glance repository.
                              Try downloading this image and upload on glance !
  vIMS - INFO - Update security group quota for this tenant
  vIMS - INFO - Update cinder quota for this tenant
  vIMS - INFO - Collect flavor id for cloudify manager server
  vIMS - INFO - Prepare virtualenv for cloudify-cli
  vIMS - INFO - Downloading the cloudify manager server blueprint
  vIMS - INFO - Cloudify deployment Start Time:'2016-02-23 04:47:07'
  vIMS - INFO - Writing the inputs file
  vIMS - INFO - Launching the cloudify-manager deployment
  vIMS - INFO - Cloudify-manager server is UP !
  vIMS - INFO - Cloudify deployment duration:'432.5'
  vIMS - INFO - Collect flavor id for all clearwater vm
  vIMS - INFO - vIMS VNF deployment Start Time:'2016-02-23 04:54:20'
  vIMS - INFO - Downloading the openstack-blueprint.yaml blueprint
  vIMS - INFO - Writing the inputs file
  vIMS - INFO - Launching the clearwater deployment
  vIMS - INFO - The deployment of clearwater-opnfv is ended
  vIMS - INFO - vIMS VNF deployment duration:'616.2'
  vIMS - INFO - vIMS functional test Start Time:'2016-02-23 05:07:44'
  vIMS - INFO - vIMS functional test duration:'3.5'
  vIMS - INFO - Launching the clearwater-opnfv undeployment
  vIMS - ERROR - Error when executing command /bin/bash -c 'source /home/opnfv/functest/data/vIMS/venv_cloudify/bin/activate; cd /home/opnfv/functest/data/vIMS/; cfy executions start -w uninstall -d clearwater-opnfv --timeout 1800 ; cfy deployments delete -d clearwater-opnfv; '
  vIMS - INFO - Launching the cloudify-manager undeployment
  vIMS - INFO - Cloudify-manager server has been successfully removed!
  vIMS - INFO - Removing vIMS tenant ..
  vIMS - INFO - Removing vIMS user ..
