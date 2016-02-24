.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for apex-os-odl_l2-nofeature-ha
-----------------------------------------------------

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
  vPing_ssh- INFO - vPing Start Time:'2016-02-22 22:26:26'
  vPing_ssh- INFO - Creating instance 'opnfv-vping-1'...
   name=opnfv-vping-1
   flavor=<Flavor: m1.small>
   image=8588bf92-664e-46f0-ad4f-40347349b4db
   network=1e07302c-1060-4862-ac96-81db4c46b173

  vPing_ssh- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  vPing_ssh- INFO - Adding 'opnfv-vping-1' to security group 'vPing-sg'...
  vPing_ssh- INFO - Creating instance 'opnfv-vping-2'...
   name=opnfv-vping-2
   flavor=<Flavor: m1.small>
   image=8588bf92-664e-46f0-ad4f-40347349b4db
   network=1e07302c-1060-4862-ac96-81db4c46b173

  vPing_ssh- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  vPing_ssh- INFO - Adding 'opnfv-vping-2' to security group 'vPing-sg'...
  vPing_ssh- INFO - Creating floating IP for VM 'opnfv-vping-2'...
  vPing_ssh- INFO - Floating IP created: '192.168.10.101'
  vPing_ssh- INFO - Associating floating ip: '192.168.10.101' to VM 'opnfv-vping-2'
  vPing_ssh- INFO - Trying to establish SSH connection to 192.168.10.101...
  vPing_ssh- INFO - Waiting for ping...
  vPing_ssh- INFO - vPing detected!
  vPing_ssh- INFO - vPing duration:'26.0' s.
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
  vPing_userdata- INFO - vPing Start Time:'2016-02-22 22:27:09'
  vPing_userdata- INFO - Creating instance 'opnfv-vping-1'...
   name=opnfv-vping-1
   flavor=<Flavor: m1.small>
   image=4e085313-471b-4846-96f8-d89c5fcdb453
   network=f1c6e324-f469-4d43-a53e-3716a2075556

  vPing_userdata- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  vPing_userdata- INFO - Creating instance 'opnfv-vping-2'...
   name=opnfv-vping-2
   flavor=<Flavor: m1.small>
   image=4e085313-471b-4846-96f8-d89c5fcdb453
   network=f1c6e324-f469-4d43-a53e-3716a2075556
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
  vPing_userdata- INFO - vPing duration:'13.7'
  vPing_userdata- INFO - vPing OK
  vPing_userdata- INFO - Cleaning up...
  vPing_userdata- INFO - Deleting network 'vping-net'...


Tempest
^^^^^^^
::

  FUNCTEST.info: Running Tempest tests...
  run_tempest - INFO - Creating tenant and user for Tempest suite
  INFO rally.verification.tempest.tempest [-] Starting: Creating configuration file for Tempest.
  INFO rally.verification.tempest.tempest [-] Completed: Creating configuration file for Tempest.
  run_tempest - INFO - Starting Tempest test suite: '--tests-file /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/custom_tests/test_list.txt'.
  Total results of verification:

  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | UUID                                 | Deployment UUID                      | Set name | Tests | Failures | Created at                 | Status   |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | 3275e5cd-a0cd-4961-95c8-11c5eceaa6a6 | 94d6d0c4-f111-4f1a-a9ee-dee149fe7ce1 |          | 210   | 1        | 2016-02-22 22:27:42.722872 | finished |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+

  Tests:

  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | name                                                                                                                                     | time      | status  |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.24365   | success |
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.06964   | success |
  | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 8.22175   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 10.97975  | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 7.03882   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.06729   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.05931   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.06307   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.11320   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.06453   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.06586   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.06862   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.06207   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.05691   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.18730   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.07965   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.10485   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.06917   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 0.14038   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 0.10940   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.07005   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 0.52047   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 0.56007   | success |
  | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 1.36847   | success |
  | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 6.81057   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 2.10654   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.06566   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.16011   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 0.20656   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.00068   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 69.80953  | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.07774   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.17023   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 0.14159   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.00084   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.09269   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 5.41847   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.30351   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.24031   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.16460   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.23510   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.18628   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.07873   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.07850   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.05956   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.06586   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.09254   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.23073   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00060   | skip    |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.14221   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.05795   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.01868   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.06964   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.07267   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.01534   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.01306   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.03567   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.06330   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.05500   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.22976   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.01362   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.08669   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.00039   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 4.49759   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 10.29434  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 11.00534  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.31208   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 17.08686  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 12.94698  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 18.51575  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 7.22487   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.07714   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.15308   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.54182   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.31556   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.31066   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.53469   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.59802   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.53771   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 1.24685   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 17.18514  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 14.43669  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 6.66687   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 6.82712   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 0.87441   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 1.61025   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 0.77729   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 0.66808   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 0.66403   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 0.97748   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 0.53671   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 0.53750   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 0.48586   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.38319   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 1.47622   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 0.47227   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 0.53487   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 0.41419   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.37761   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 0.66937   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.40626   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 1.18956   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 0.41639   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 0.42068   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 0.32462   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.09822   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.01379   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 0.06999   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.01451   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 0.50159   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.06452   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.11341   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.05076   | success |
  | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 38.69512  | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.21321   | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.17329   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.18341   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.00759   | success |
  | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.24642   | success |
  | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.07626   | success |
  | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.08835   | success |
  | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.02633   | success |
  | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 0.37189   | success |
  | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.15162   | success |
  | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 0.86306   | success |
  | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.10101   | success |
  | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.12434   | success |
  | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.11215   | fail    |
  | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.12074   | success |
  | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 0.86182   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.06049   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.01891   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.01815   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.02941   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.02461   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.03987   | success |
  | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.05957   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 0.26863   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 0.41872   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 0.46002   | success |
  | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 0.68221   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 1.77595   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 2.72713   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 0.59088   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 1.16562   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 3.93480   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 1.01314   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 1.66236   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 1.72675   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 1.39541   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.13054   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.03480   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.05462   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.03106   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.03278   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 1.42674   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.18894   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.08396   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.11331   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.06513   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.04251   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 1.36723   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 1.36291   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 0.73091   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.20694   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.15012   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 1.36701   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 1.50158   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 0.70437   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.07769   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.06964   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 3.74936   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 1.65997   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 1.75798   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 1.38648   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 3.00947   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 1.91922   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 1.66228   | success |
  | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 1.09354   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 0.73626   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 0.59551   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.02945   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 0.47389   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 0.93740   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.02787   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.55494   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 6.50572   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.02163   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 0.82447   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.53325   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.38634   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.32465   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.55989   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.51489   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 3.86241   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.03735   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 11.17975  | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 1.67439   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 2.39084   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 2.38683   | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 12.07426  | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 11.07575  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 11.26088  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 11.66599  | success |
  | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.41386   | success |
  | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.39419   | success |
  | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 27.45308  | success |
  | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 13.84478  | success |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 85.32205  | success |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 100.83926 | success |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  run_tempest - INFO - Results: {'timestart': '2016-02-2222:27:42.722872', 'duration': 171, 'tests': 210, 'failures': 1}
  run_tempest - INFO - Pushing results to DB: 'http://testresults.opnfv.org/testapi/results'.
  run_tempest - INFO - Deleting tenant and user for Tempest suite)


Rally
^^^^^
::

  FUNCTEST.info: Running Rally benchmark suite...
  run_rally - INFO - Starting test scenario "authenticate" ...
  run_rally - INFO -
   Preparing input task
   Task  8ccbcb5f-32ba-4621-be0d-09b54fb1c9ea: started
  Task 8ccbcb5f-32ba-4621-be0d-09b54fb1c9ea: finished

  test scenario Authenticate.validate_glance
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_glance     | 0.112 | 0.132  | 0.201  | 0.201  | 0.201 | 0.143 | 100.0%  | 10    |
  | authenticate.validate_glance (2) | 0.039 | 0.046  | 0.107  | 0.111  | 0.115 | 0.063 | 100.0%  | 10    |
  | total                            | 0.226 | 0.257  | 0.386  | 0.389  | 0.391 | 0.286 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.860725164413
  Full duration: 3.2147500515

  test scenario Authenticate.keystone
  +-----------------------------------------------------------------------------+
  |                            Response Times (sec)                             |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | total  | 0.065 | 0.07   | 0.085  | 0.106  | 0.127 | 0.076 | 100.0%  | 10    |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.236154079437
  Full duration: 2.56328606606

  test scenario Authenticate.validate_heat
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_heat     | 0.106 | 0.121  | 0.259  | 0.268  | 0.277 | 0.148 | 100.0%  | 10    |
  | authenticate.validate_heat (2) | 0.022 | 0.028  | 0.122  | 0.18   | 0.237 | 0.065 | 100.0%  | 10    |
  | total                          | 0.212 | 0.25   | 0.426  | 0.429  | 0.431 | 0.294 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.876858949661
  Full duration: 3.099599123

  test scenario Authenticate.validate_nova
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_nova     | 0.108 | 0.125  | 0.144  | 0.144  | 0.144 | 0.126 | 100.0%  | 10    |
  | authenticate.validate_nova (2) | 0.025 | 0.034  | 0.039  | 0.04   | 0.04  | 0.034 | 100.0%  | 10    |
  | total                          | 0.214 | 0.242  | 0.258  | 0.263  | 0.268 | 0.239 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.719485044479
  Full duration: 2.89414715767

  test scenario Authenticate.validate_cinder
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_cinder     | 0.102 | 0.111  | 0.167  | 0.177  | 0.188 | 0.124 | 100.0%  | 10    |
  | authenticate.validate_cinder (2) | 0.014 | 0.075  | 0.098  | 0.147  | 0.195 | 0.07  | 100.0%  | 10    |
  | total                            | 0.197 | 0.261  | 0.37   | 0.39   | 0.41  | 0.281 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.842756032944
  Full duration: 3.36014580727

  test scenario Authenticate.validate_neutron
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_neutron     | 0.106 | 0.121  | 0.133  | 0.137  | 0.142 | 0.122 | 100.0%  | 10    |
  | authenticate.validate_neutron (2) | 0.029 | 0.088  | 0.109  | 0.11   | 0.111 | 0.087 | 100.0%  | 10    |
  | total                             | 0.218 | 0.286  | 0.32   | 0.324  | 0.328 | 0.281 | 100.0%  | 10    |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.860924005508
  Full duration: 3.14792895317

  run_rally - INFO - Test scenario: "authenticate" OK.
  run_rally - INFO - Starting test scenario "glance" ...
  run_rally - INFO -
   Preparing input task
   Task  e020cf98-caa0-4014-a28d-42748bf9dca3: started
  Task e020cf98-caa0-4014-a28d-42748bf9dca3: finished

  test scenario GlanceImages.list_images
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.list_images | 0.193 | 0.22   | 0.23   | 0.234  | 0.238 | 0.217 | 100.0%  | 10    |
  | total              | 0.193 | 0.22   | 0.23   | 0.234  | 0.238 | 0.217 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.657658100128
  Full duration: 3.69541883469

  test scenario GlanceImages.create_image_and_boot_instances
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | glance.create_image | 2.85  | 3.139  | 3.39   | 3.41   | 3.43   | 3.133 | 100.0%  | 10    |
  | nova.boot_servers   | 5.898 | 6.853  | 7.241  | 7.329  | 7.417  | 6.806 | 100.0%  | 10    |
  | total               | 8.797 | 10.039 | 10.461 | 10.534 | 10.607 | 9.94  | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 29.545609951
  Full duration: 55.3799848557

  test scenario GlanceImages.create_and_list_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 2.821 | 3.548  | 3.89   | 3.905  | 3.92  | 3.507 | 100.0%  | 10    |
  | glance.list_images  | 0.04  | 0.045  | 0.053  | 0.054  | 0.056 | 0.046 | 100.0%  | 10    |
  | total               | 2.873 | 3.599  | 3.934  | 3.948  | 3.962 | 3.553 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 10.4028940201
  Full duration: 15.1872868538

  test scenario GlanceImages.create_and_delete_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 2.876 | 3.678  | 3.734  | 3.742  | 3.75  | 3.507 | 100.0%  | 10    |
  | glance.delete_image | 0.141 | 0.148  | 0.209  | 0.217  | 0.226 | 0.162 | 100.0%  | 10    |
  | total               | 3.036 | 3.822  | 3.893  | 3.934  | 3.976 | 3.669 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 10.7681660652
  Full duration: 13.7783231735

  run_rally - INFO - Test scenario: "glance" OK.
  run_rally - INFO - Starting test scenario "cinder" ...
  run_rally - INFO -
   Preparing input task
   Task  d1dd9119-e59d-4e80-ad09-072f6300762b: started
  Task d1dd9119-e59d-4e80-ad09-072f6300762b: finished

  test scenario CinderVolumes.create_and_attach_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server     | 3.086  | 4.323  | 5.484  | 5.514  | 5.544  | 4.505  | 100.0%  | 10    |
  | cinder.create_volume | 2.703  | 2.882  | 2.961  | 2.969  | 2.978  | 2.865  | 100.0%  | 10    |
  | nova.attach_volume   | 7.55   | 7.801  | 10.194 | 10.345 | 10.495 | 8.292  | 100.0%  | 10    |
  | nova.detach_volume   | 2.967  | 5.217  | 5.602  | 5.694  | 5.786  | 4.468  | 100.0%  | 10    |
  | cinder.delete_volume | 2.393  | 2.51   | 2.562  | 2.572  | 2.582  | 2.497  | 100.0%  | 10    |
  | nova.delete_server   | 2.375  | 2.429  | 2.554  | 2.595  | 2.637  | 2.46   | 100.0%  | 10    |
  | total                | 21.586 | 25.034 | 28.962 | 29.376 | 29.79  | 25.088 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 74.0110630989
  Full duration: 87.3835339546

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 5.186 | 5.298  | 5.406  | 5.44   | 5.474 | 5.311 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.11  | 0.134  | 0.147  | 0.148  | 0.15  | 0.133 | 100.0%  | 10    |
  | total                | 5.336 | 5.425  | 5.529  | 5.575  | 5.62  | 5.444 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.3077280521
  Full duration: 27.7325429916

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.841 | 2.921  | 3.157  | 3.158  | 3.158 | 2.951 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.067 | 0.12   | 0.18   | 0.18   | 0.18  | 0.127 | 100.0%  | 10    |
  | total                | 2.954 | 3.036  | 3.281  | 3.282  | 3.283 | 3.078 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.12118315697
  Full duration: 19.8639061451

  test scenario CinderVolumes.create_and_list_snapshots
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.433 | 2.508  | 2.551  | 2.552  | 2.554 | 2.5   | 100.0%  | 10    |
  | cinder.list_snapshots  | 0.018 | 0.082  | 0.103  | 0.111  | 0.119 | 0.069 | 100.0%  | 10    |
  | total                  | 2.523 | 2.561  | 2.612  | 2.627  | 2.641 | 2.57  | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 7.76097297668
  Full duration: 31.5859258175

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.795 | 2.848  | 2.943  | 2.955  | 2.968 | 2.867 | 100.0%  | 10    |
  | cinder.delete_volume | 2.446 | 2.499  | 2.595  | 2.669  | 2.744 | 2.524 | 100.0%  | 10    |
  | total                | 5.295 | 5.374  | 5.521  | 5.53   | 5.539 | 5.391 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.1756019592
  Full duration: 23.199131012

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 5.287 | 5.38   | 5.424  | 5.439  | 5.454 | 5.365 | 100.0%  | 10    |
  | cinder.delete_volume | 2.394 | 2.549  | 2.687  | 2.699  | 2.711 | 2.555 | 100.0%  | 10    |
  | total                | 7.728 | 7.896  | 8.06   | 8.081  | 8.103 | 7.92  | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 23.6543819904
  Full duration: 30.6390721798

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.885 | 2.937  | 3.053  | 3.059  | 3.066 | 2.962 | 100.0%  | 10    |
  | cinder.delete_volume | 2.405 | 2.586  | 2.691  | 2.732  | 2.773 | 2.577 | 100.0%  | 10    |
  | total                | 5.421 | 5.531  | 5.59   | 5.691  | 5.793 | 5.539 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.603798151
  Full duration: 23.3788831234

  test scenario CinderVolumes.create_and_upload_volume_to_image
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume          | 2.792  | 2.951  | 3.369  | 3.545  | 3.721  | 3.036  | 100.0%  | 10    |
  | cinder.upload_volume_to_image | 26.207 | 65.967 | 78.731 | 83.94  | 89.149 | 62.382 | 100.0%  | 10    |
  | cinder.delete_volume          | 2.469  | 2.587  | 2.777  | 2.908  | 3.038  | 2.617  | 100.0%  | 10    |
  | nova.delete_image             | 0.306  | 0.602  | 1.075  | 1.085  | 1.095  | 0.679  | 100.0%  | 10    |
  | total                         | 32.909 | 73.046 | 84.953 | 90.036 | 95.118 | 68.714 | 100.0%  | 10    |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 183.403058052
  Full duration: 190.890599012

  test scenario CinderVolumes.create_and_delete_snapshot
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.494 | 2.541  | 2.623  | 2.662  | 2.701 | 2.563 | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.29  | 2.379  | 2.557  | 2.611  | 2.665 | 2.424 | 100.0%  | 10    |
  | total                  | 4.784 | 4.953  | 5.15   | 5.215  | 5.279 | 4.988 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.7655448914
  Full duration: 33.6425430775

  test scenario CinderVolumes.create_volume
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +----------------------+-------+--------+--------+--------+-----+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-----+-------+---------+-------+
  | cinder.create_volume | 2.789 | 2.912  | 3.076  | 3.088  | 3.1 | 2.933 | 100.0%  | 10    |
  | total                | 2.789 | 2.913  | 3.076  | 3.088  | 3.1 | 2.933 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-----+-------+---------+-------+
  Load duration: 8.82123494148
  Full duration: 18.1940879822

  test scenario CinderVolumes.create_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.807 | 2.927  | 3.035  | 3.036  | 3.036 | 2.926 | 100.0%  | 10    |
  | total                | 2.808 | 2.927  | 3.036  | 3.036  | 3.036 | 2.927 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 8.90417385101
  Full duration: 20.1418190002

  test scenario CinderVolumes.list_volumes
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.list_volumes | 0.226 | 0.251  | 0.27   | 0.282  | 0.293 | 0.253 | 100.0%  | 10    |
  | total               | 0.226 | 0.251  | 0.27   | 0.282  | 0.293 | 0.253 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.773681879044
  Full duration: 47.6445128918

  test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.752  | 2.933  | 3.066  | 3.089  | 3.112  | 2.943  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.319  | 2.388  | 2.432  | 2.437  | 2.441  | 2.387  | 100.0%  | 10    |
  | nova.attach_volume     | 7.626  | 9.641  | 12.934 | 14.634 | 16.334 | 10.372 | 100.0%  | 10    |
  | nova.detach_volume     | 3.067  | 5.326  | 5.451  | 5.507  | 5.563  | 4.908  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.261  | 2.317  | 2.419  | 2.448  | 2.476  | 2.333  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.339  | 2.491  | 2.583  | 2.615  | 2.647  | 2.486  | 100.0%  | 10    |
  | total                  | 21.617 | 24.353 | 28.724 | 30.338 | 31.953 | 25.746 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 72.4364318848
  Full duration: 113.83590889

  test scenario CinderVolumes.create_from_volume_and_delete_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 9.733  | 14.37  | 14.917 | 16.883 | 18.848 | 13.936 | 100.0%  | 10    |
  | cinder.delete_volume | 2.357  | 2.482  | 2.618  | 2.619  | 2.619  | 2.497  | 100.0%  | 10    |
  | total                | 12.277 | 16.823 | 17.514 | 19.491 | 21.468 | 16.433 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 46.032130003
  Full duration: 65.3552489281

  test scenario CinderVolumes.create_and_extend_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.81  | 2.879  | 3.049  | 3.065  | 3.082 | 2.923 | 100.0%  | 10    |
  | cinder.extend_volume | 2.584 | 2.789  | 2.943  | 2.951  | 2.958 | 2.782 | 100.0%  | 10    |
  | cinder.delete_volume | 2.402 | 2.564  | 2.615  | 2.633  | 2.65  | 2.54  | 100.0%  | 10    |
  | total                | 8.046 | 8.216  | 8.376  | 8.506  | 8.636 | 8.246 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.652312994
  Full duration: 31.6354629993

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +-----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                      |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.872 | 2.939  | 2.986  | 3.045  | 3.103  | 2.944  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.312 | 2.389  | 2.452  | 2.499  | 2.546  | 2.395  | 100.0%  | 10    |
  | nova.attach_volume     | 7.624 | 7.814  | 13.095 | 16.211 | 19.328 | 9.374  | 100.0%  | 10    |
  | nova.detach_volume     | 2.991 | 4.159  | 5.336  | 5.399  | 5.461  | 4.171  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.186 | 2.277  | 2.41   | 2.418  | 2.426  | 2.296  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.431 | 2.498  | 2.589  | 2.595  | 2.601  | 2.51   | 100.0%  | 10    |
  | total                  | 21.28 | 23.314 | 26.739 | 29.882 | 33.025 | 24.004 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 68.312828064
  Full duration: 112.127801895

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.617  | 2.833  | 2.941  | 2.982  | 3.022  | 2.823  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.282  | 2.375  | 2.445  | 2.47   | 2.494  | 2.384  | 100.0%  | 10    |
  | nova.attach_volume     | 7.58   | 7.741  | 13.508 | 16.698 | 19.888 | 9.501  | 100.0%  | 10    |
  | nova.detach_volume     | 3.07   | 5.287  | 5.408  | 5.463  | 5.518  | 4.882  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.254  | 2.326  | 2.432  | 2.435  | 2.438  | 2.343  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.339  | 2.475  | 2.593  | 2.625  | 2.656  | 2.483  | 100.0%  | 10    |
  | total                  | 21.236 | 23.663 | 29.169 | 32.362 | 35.555 | 24.955 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 71.8869941235
  Full duration: 117.904321909

  run_rally - INFO - Test scenario: "cinder" OK.
  run_rally - INFO - Starting test scenario "heat" ...
  run_rally - INFO -
   Preparing input task
   Task  e23e2615-b959-461f-9e63-973b9de00f98: started
  Task e23e2615-b959-461f-9e63-973b9de00f98: finished

  test scenario HeatStacks.create_suspend_resume_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack  | 2.856 | 3.146  | 3.227  | 3.244  | 3.262 | 3.087 | 100.0%  | 10    |
  | heat.suspend_stack | 0.525 | 1.615  | 1.756  | 1.822  | 1.888 | 1.284 | 100.0%  | 10    |
  | heat.resume_stack  | 0.549 | 1.6    | 1.663  | 1.673  | 1.682 | 1.296 | 100.0%  | 10    |
  | heat.delete_stack  | 1.312 | 1.491  | 1.655  | 1.659  | 1.662 | 1.501 | 100.0%  | 10    |
  | total              | 5.641 | 7.374  | 8.053  | 8.167  | 8.281 | 7.168 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 22.0507199764
  Full duration: 25.5707690716

  test scenario HeatStacks.create_and_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.923 | 3.085  | 3.286  | 3.309  | 3.331 | 3.115 | 100.0%  | 10    |
  | heat.delete_stack | 0.243 | 0.963  | 1.56   | 1.624  | 1.688 | 0.962 | 100.0%  | 10    |
  | total             | 3.166 | 4.127  | 4.666  | 4.735  | 4.803 | 4.076 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 13.0132920742
  Full duration: 16.5792620182

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 9.979  | 11.338 | 13.752 | 13.849 | 13.946 | 11.536 | 100.0%  | 10    |
  | heat.delete_stack | 7.092  | 8.228  | 8.71   | 8.871  | 9.033  | 8.149  | 100.0%  | 10    |
  | total             | 18.547 | 19.228 | 21.86  | 22.086 | 22.312 | 19.685 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 58.1043260098
  Full duration: 61.6377520561

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 11.918 | 13.906 | 16.154 | 16.286 | 16.418 | 13.895 | 100.0%  | 10    |
  | heat.delete_stack | 8.414  | 9.204  | 10.491 | 10.538 | 10.585 | 9.295  | 100.0%  | 10    |
  | total             | 21.347 | 22.82  | 25.491 | 26.247 | 27.003 | 23.19  | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 68.1649589539
  Full duration: 71.9318380356

  test scenario HeatStacks.list_stacks_and_resources
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.list_stacks                | 0.233 | 0.257  | 0.318  | 0.436  | 0.555 | 0.286 | 100.0%  | 10    |
  | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0   | 0.0   | 100.0%  | 10    |
  | total                           | 0.233 | 0.257  | 0.318  | 0.436  | 0.555 | 0.286 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.829450845718
  Full duration: 3.74743390083

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.703 | 2.996  | 3.064  | 3.184  | 3.304 | 2.981 | 100.0%  | 10    |
  | heat.update_stack | 2.487 | 3.644  | 3.84   | 3.918  | 3.996 | 3.387 | 100.0%  | 10    |
  | heat.delete_stack | 0.52  | 1.473  | 1.686  | 1.691  | 1.697 | 1.413 | 100.0%  | 10    |
  | total             | 6.639 | 8.102  | 8.301  | 8.486  | 8.671 | 7.781 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 23.5321931839
  Full duration: 26.9891970158

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.69  | 3.032  | 3.266  | 3.279  | 3.293 | 3.041 | 100.0%  | 10    |
  | heat.update_stack | 2.458 | 2.642  | 3.727  | 3.766  | 3.805 | 3.037 | 100.0%  | 10    |
  | heat.delete_stack | 0.556 | 1.511  | 1.586  | 1.632  | 1.678 | 1.419 | 100.0%  | 10    |
  | total             | 6.957 | 7.396  | 8.15   | 8.18   | 8.21  | 7.497 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 22.4653220177
  Full duration: 25.9613161087

  test scenario HeatStacks.create_update_delete_stack
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 2.936 | 3.18   | 3.4    | 3.735  | 4.069  | 3.237  | 100.0%  | 10    |
  | heat.update_stack | 4.79  | 5.132  | 6.045  | 6.06   | 6.076  | 5.308  | 100.0%  | 10    |
  | heat.delete_stack | 1.518 | 2.424  | 2.589  | 2.618  | 2.647  | 2.182  | 100.0%  | 10    |
  | total             | 9.624 | 10.703 | 11.721 | 11.781 | 11.842 | 10.727 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 31.7993149757
  Full duration: 35.7221229076

  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 7     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 6.70760798454
  Full duration: 15.0584180355

  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg    | success | count |
  +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
  | heat.create_stack | 2.893 | 3.127  | 3.179  | 3.194  | 3.209 | 3.079  | 100.0%  | 10    |
  | heat.update_stack | 4.695 | 5.02   | 5.189  | 5.193  | 5.197 | 5.007  | 100.0%  | 10    |
  | heat.delete_stack | 1.51  | 2.454  | 2.786  | 2.821  | 2.855 | 2.302  | 100.0%  | 10    |
  | total             | 9.334 | 10.621 | 10.981 | 10.985 | 10.99 | 10.388 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
  Load duration: 31.2812139988
  Full duration: 35.1641018391

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.885 | 3.01   | 3.24   | 3.311  | 3.381 | 3.05  | 100.0%  | 10    |
  | heat.update_stack | 2.83  | 3.881  | 3.936  | 3.968  | 4.0   | 3.777 | 100.0%  | 10    |
  | heat.delete_stack | 1.307 | 1.567  | 1.645  | 1.79   | 1.935 | 1.543 | 100.0%  | 10    |
  | total             | 7.316 | 8.436  | 8.859  | 8.868  | 8.876 | 8.37  | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.9058198929
  Full duration: 28.9196100235

  test scenario HeatStacks.create_and_list_stack
  +---------------------------------------------------------------------------------------+
  |                                 Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg  | success | count |
  +-------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | heat.create_stack | 2.882 | 3.04   | 3.213  | 3.318  | 3.423 | 3.07 | 100.0%  | 10    |
  | heat.list_stacks  | 0.037 | 0.16   | 0.174  | 0.178  | 0.182 | 0.14 | 100.0%  | 10    |
  | total             | 3.046 | 3.142  | 3.382  | 3.478  | 3.575 | 3.21 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+------+---------+-------+
  Load duration: 9.64803004265
  Full duration: 17.1896460056

  test scenario HeatStacks.create_check_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.808 | 3.191  | 3.252  | 3.281  | 3.311 | 3.148 | 100.0%  | 10    |
  | heat.check_stack  | 0.407 | 0.668  | 1.405  | 1.545  | 1.685 | 0.776 | 100.0%  | 10    |
  | heat.delete_stack | 0.678 | 1.561  | 1.687  | 1.707  | 1.726 | 1.474 | 100.0%  | 10    |
  | total             | 4.931 | 5.317  | 5.757  | 5.974  | 6.192 | 5.398 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.0285110474
  Full duration: 19.9199111462

  run_rally - INFO - Test scenario: "heat" Failed.
  run_rally - INFO - Starting test scenario "keystone" ...
  run_rally - INFO -
   Preparing input task
   Task  08dbf827-7838-43b0-9cd2-3d48c9632781: started
  Task 08dbf827-7838-43b0-9cd2-3d48c9632781: finished

  test scenario KeystoneBasic.create_tenant_with_users
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.113 | 0.12   | 0.158  | 0.176  | 0.195 | 0.13  | 100.0%  | 10    |
  | keystone.create_users  | 0.651 | 0.684  | 0.707  | 0.733  | 0.759 | 0.685 | 100.0%  | 10    |
  | total                  | 0.772 | 0.8    | 0.865  | 0.91   | 0.954 | 0.815 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.42733502388
  Full duration: 12.6668281555

  test scenario KeystoneBasic.create_add_and_list_user_roles
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.115 | 0.123  | 0.132  | 0.145  | 0.159 | 0.125 | 100.0%  | 10    |
  | keystone.add_role    | 0.09  | 0.101  | 0.122  | 0.137  | 0.151 | 0.106 | 100.0%  | 10    |
  | keystone.list_roles  | 0.049 | 0.057  | 0.062  | 0.065  | 0.067 | 0.057 | 100.0%  | 10    |
  | total                | 0.26  | 0.282  | 0.328  | 0.329  | 0.33  | 0.288 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.850867986679
  Full duration: 6.24242782593

  test scenario KeystoneBasic.add_and_remove_user_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.118 | 0.172  | 0.235  | 0.244  | 0.254 | 0.177 | 100.0%  | 10    |
  | keystone.add_role    | 0.095 | 0.115  | 0.16   | 0.162  | 0.165 | 0.122 | 100.0%  | 10    |
  | keystone.remove_role | 0.059 | 0.068  | 0.163  | 0.164  | 0.166 | 0.085 | 100.0%  | 10    |
  | total                | 0.281 | 0.407  | 0.444  | 0.447  | 0.451 | 0.385 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.1720468998
  Full duration: 6.63848996162

  test scenario KeystoneBasic.create_update_and_delete_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.125 | 0.19   | 0.247  | 0.268  | 0.289 | 0.191 | 100.0%  | 10    |
  | keystone.update_tenant | 0.052 | 0.063  | 0.11   | 0.111  | 0.113 | 0.07  | 100.0%  | 10    |
  | keystone.delete_tenant | 0.12  | 0.141  | 0.192  | 0.227  | 0.261 | 0.153 | 100.0%  | 10    |
  | total                  | 0.331 | 0.418  | 0.486  | 0.502  | 0.517 | 0.415 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.27042984962
  Full duration: 5.3805770874

  test scenario KeystoneBasic.create_and_delete_service
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_service | 0.111 | 0.117  | 0.13   | 0.139  | 0.147 | 0.121 | 100.0%  | 10    |
  | keystone.delete_service | 0.055 | 0.067  | 0.096  | 0.097  | 0.097 | 0.071 | 100.0%  | 10    |
  | total                   | 0.176 | 0.189  | 0.212  | 0.215  | 0.218 | 0.192 | 100.0%  | 10    |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.61040687561
  Full duration: 4.58190393448

  test scenario KeystoneBasic.create_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.114 | 0.128  | 0.136  | 0.16   | 0.183 | 0.131 | 100.0%  | 10    |
  | total                  | 0.114 | 0.128  | 0.137  | 0.16   | 0.183 | 0.131 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.400830030441
  Full duration: 4.4062628746

  test scenario KeystoneBasic.create_user
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.124 | 0.137  | 0.146  | 0.163  | 0.179 | 0.138 | 100.0%  | 10    |
  | total                | 0.125 | 0.137  | 0.146  | 0.163  | 0.179 | 0.138 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.42484498024
  Full duration: 4.1389541626

  test scenario KeystoneBasic.create_and_list_tenants
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.117 | 0.126  | 0.134  | 0.152  | 0.17  | 0.129 | 100.0%  | 10    |
  | keystone.list_tenants  | 0.046 | 0.059  | 0.104  | 0.104  | 0.105 | 0.069 | 100.0%  | 10    |
  | total                  | 0.166 | 0.19   | 0.231  | 0.233  | 0.235 | 0.198 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.600751876831
  Full duration: 6.1798210144

  test scenario KeystoneBasic.create_and_delete_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.118 | 0.227  | 0.298  | 0.3    | 0.302 | 0.204 | 100.0%  | 10    |
  | keystone.delete_role | 0.105 | 0.13   | 0.271  | 0.29   | 0.309 | 0.157 | 100.0%  | 10    |
  | total                | 0.238 | 0.346  | 0.573  | 0.59   | 0.607 | 0.362 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.21080708504
  Full duration: 5.530189991

  test scenario KeystoneBasic.get_entities
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.121 | 0.125  | 0.148  | 0.149  | 0.151 | 0.13  | 100.0%  | 10    |
  | keystone.create_user   | 0.062 | 0.078  | 0.103  | 0.121  | 0.139 | 0.084 | 100.0%  | 10    |
  | keystone.create_role   | 0.046 | 0.051  | 0.067  | 0.069  | 0.072 | 0.055 | 100.0%  | 10    |
  | keystone.get_tenant    | 0.04  | 0.05   | 0.054  | 0.057  | 0.06  | 0.049 | 100.0%  | 10    |
  | keystone.get_user      | 0.048 | 0.058  | 0.072  | 0.082  | 0.093 | 0.062 | 100.0%  | 10    |
  | keystone.get_role      | 0.042 | 0.047  | 0.053  | 0.058  | 0.064 | 0.048 | 100.0%  | 10    |
  | keystone.service_list  | 0.046 | 0.055  | 0.069  | 0.079  | 0.09  | 0.058 | 100.0%  | 10    |
  | keystone.get_service   | 0.041 | 0.048  | 0.057  | 0.072  | 0.088 | 0.051 | 100.0%  | 10    |
  | total                  | 0.483 | 0.541  | 0.568  | 0.584  | 0.599 | 0.538 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.66359400749
  Full duration: 10.0017409325

  test scenario KeystoneBasic.create_and_list_users
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.131 | 0.14   | 0.157  | 0.205  | 0.254 | 0.151 | 100.0%  | 10    |
  | keystone.list_users  | 0.051 | 0.057  | 0.065  | 0.078  | 0.091 | 0.06  | 100.0%  | 10    |
  | total                | 0.182 | 0.199  | 0.239  | 0.274  | 0.309 | 0.211 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.62369799614
  Full duration: 4.64324808121

  run_rally - INFO - Test scenario: "keystone" OK.
  run_rally - INFO - Starting test scenario "neutron" ...
  run_rally - INFO -
   Preparing input task
   Task  7a8d4b82-85d3-485c-996e-08dbd3787094: started
  Task 7a8d4b82-85d3-485c-996e-08dbd3787094: finished

  test scenario NeutronNetworks.create_and_delete_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.424 | 0.519  | 0.555  | 0.559  | 0.563 | 0.503 | 100.0%  | 10    |
  | neutron.delete_port | 0.148 | 0.283  | 0.32   | 0.339  | 0.358 | 0.259 | 100.0%  | 10    |
  | total               | 0.584 | 0.797  | 0.849  | 0.859  | 0.87  | 0.762 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.3002948761
  Full duration: 25.5696978569

  test scenario NeutronNetworks.create_and_list_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.421 | 0.453  | 0.541  | 0.55   | 0.56  | 0.472 | 100.0%  | 10    |
  | neutron.create_router        | 0.039 | 0.045  | 0.24   | 0.247  | 0.254 | 0.11  | 100.0%  | 10    |
  | neutron.add_interface_router | 0.28  | 0.297  | 0.417  | 0.427  | 0.438 | 0.32  | 100.0%  | 10    |
  | neutron.list_routers         | 0.043 | 0.163  | 0.181  | 0.185  | 0.189 | 0.122 | 100.0%  | 10    |
  | total                        | 0.795 | 1.045  | 1.115  | 1.243  | 1.372 | 1.024 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.85029602051
  Full duration: 27.2547390461

  test scenario NeutronNetworks.create_and_delete_routers
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet           | 0.399 | 0.476  | 0.542  | 0.561  | 0.579 | 0.479 | 100.0%  | 10    |
  | neutron.create_router           | 0.038 | 0.041  | 0.181  | 0.186  | 0.19  | 0.096 | 100.0%  | 10    |
  | neutron.add_interface_router    | 0.272 | 0.306  | 0.421  | 0.426  | 0.43  | 0.34  | 100.0%  | 10    |
  | neutron.remove_interface_router | 0.228 | 0.311  | 0.514  | 0.518  | 0.521 | 0.338 | 100.0%  | 10    |
  | neutron.delete_router           | 0.151 | 0.159  | 0.295  | 0.297  | 0.298 | 0.205 | 100.0%  | 10    |
  | total                           | 1.218 | 1.388  | 1.829  | 1.868  | 1.908 | 1.458 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.20906496048
  Full duration: 28.1987309456

  test scenario NeutronNetworks.create_and_list_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.429 | 0.5    | 0.612  | 0.626  | 0.639 | 0.521 | 100.0%  | 10    |
  | neutron.list_ports  | 0.108 | 0.282  | 0.352  | 0.372  | 0.392 | 0.262 | 100.0%  | 10    |
  | total               | 0.594 | 0.761  | 0.957  | 0.957  | 0.957 | 0.783 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.34113693237
  Full duration: 26.7457489967

  test scenario NeutronNetworks.create_and_delete_subnets
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max  | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | neutron.create_subnet | 0.402 | 0.436  | 0.542  | 0.566  | 0.59 | 0.463 | 100.0%  | 10    |
  | neutron.delete_subnet | 0.142 | 0.29   | 0.334  | 0.367  | 0.4  | 0.25  | 100.0%  | 10    |
  | total                 | 0.564 | 0.709  | 0.86   | 0.875  | 0.89 | 0.713 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  Load duration: 2.14902901649
  Full duration: 25.5031478405

  test scenario NeutronNetworks.create_and_delete_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.301 | 0.346  | 0.477  | 0.499  | 0.521 | 0.363 | 100.0%  | 10    |
  | neutron.delete_network | 0.105 | 0.112  | 0.289  | 0.29   | 0.291 | 0.161 | 100.0%  | 10    |
  | total                  | 0.411 | 0.457  | 0.766  | 0.789  | 0.812 | 0.524 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.52401685715
  Full duration: 14.2058041096

  test scenario NeutronNetworks.create_and_list_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.307 | 0.336  | 0.388  | 0.405  | 0.423 | 0.348 | 100.0%  | 10    |
  | neutron.list_networks  | 0.043 | 0.172  | 0.242  | 0.279  | 0.316 | 0.147 | 100.0%  | 10    |
  | total                  | 0.36  | 0.503  | 0.621  | 0.622  | 0.623 | 0.495 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.58333802223
  Full duration: 15.9647290707

  test scenario NeutronNetworks.create_and_update_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.434 | 0.497  | 0.576  | 0.576  | 0.577 | 0.499 | 100.0%  | 10    |
  | neutron.create_router        | 0.037 | 0.173  | 0.305  | 0.36   | 0.415 | 0.158 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.294 | 0.439  | 0.504  | 0.513  | 0.522 | 0.404 | 100.0%  | 10    |
  | neutron.update_router        | 0.131 | 0.272  | 0.316  | 0.359  | 0.402 | 0.263 | 100.0%  | 10    |
  | total                        | 0.93  | 1.355  | 1.47   | 1.584  | 1.698 | 1.324 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.98894906044
  Full duration: 29.5306479931

  test scenario NeutronNetworks.create_and_update_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.317 | 0.356  | 0.487  | 0.489  | 0.491 | 0.377 | 100.0%  | 10    |
  | neutron.update_network | 0.103 | 0.277  | 0.309  | 0.316  | 0.322 | 0.22  | 100.0%  | 10    |
  | total                  | 0.421 | 0.626  | 0.787  | 0.79   | 0.793 | 0.598 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.78881001472
  Full duration: 16.6285750866

  test scenario NeutronNetworks.create_and_update_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.435 | 0.471  | 0.575  | 0.578  | 0.58  | 0.49  | 100.0%  | 10    |
  | neutron.update_port | 0.124 | 0.245  | 0.349  | 0.375  | 0.402 | 0.237 | 100.0%  | 10    |
  | total               | 0.565 | 0.725  | 0.912  | 0.917  | 0.922 | 0.728 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.24334001541
  Full duration: 26.9849171638

  test scenario NeutronNetworks.create_and_list_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.428 | 0.456  | 0.539  | 0.544  | 0.549 | 0.476 | 100.0%  | 10    |
  | neutron.list_subnets  | 0.061 | 0.192  | 0.234  | 0.25   | 0.265 | 0.157 | 100.0%  | 10    |
  | total                 | 0.498 | 0.642  | 0.77   | 0.786  | 0.803 | 0.633 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.8174021244
  Full duration: 26.2954719067

  test scenario NeutronNetworks.create_and_update_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.396 | 0.432  | 0.523  | 0.543  | 0.562 | 0.444 | 100.0%  | 10    |
  | neutron.update_subnet | 0.157 | 0.226  | 0.355  | 0.395  | 0.434 | 0.256 | 100.0%  | 10    |
  | total                 | 0.554 | 0.688  | 0.876  | 0.892  | 0.909 | 0.7   | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.9577729702
  Full duration: 25.9509670734

  run_rally - INFO - Test scenario: "neutron" OK.
  run_rally - INFO - Starting test scenario "nova" ...
  run_rally - INFO -
   Preparing input task
   Task  c520ad11-229c-433c-9fbb-2ddc8152c608: started
  Task c520ad11-229c-433c-9fbb-2ddc8152c608: finished

  test scenario NovaKeypair.create_and_delete_keypair
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.423 | 0.517  | 0.708  | 1.052  | 1.396 | 0.61  | 100.0%  | 10    |
  | nova.delete_keypair | 0.013 | 0.018  | 0.02   | 0.023  | 0.025 | 0.018 | 100.0%  | 10    |
  | total               | 0.442 | 0.534  | 0.722  | 1.068  | 1.415 | 0.627 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.91971611977
  Full duration: 16.1851501465

  test scenario NovaServers.snapshot_server
  +----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                        |
  +------------------------+--------+---------+---------+---------+---------+--------+---------+-------+
  | action                 | min    | median  | 90%ile  | 95%ile  | max     | avg    | success | count |
  +------------------------+--------+---------+---------+---------+---------+--------+---------+-------+
  | nova.boot_server       | 3.327  | 5.71    | 6.47    | 7.233   | 7.996   | 5.669  | 100.0%  | 10    |
  | nova.create_image      | 35.707 | 57.482  | 68.949  | 70.89   | 72.832  | 55.735 | 100.0%  | 10    |
  | nova.delete_server     | 2.417  | 2.639   | 3.37    | 4.016   | 4.662   | 2.931  | 100.0%  | 10    |
  | nova.boot_server (2)   | 14.245 | 30.97   | 41.617  | 41.703  | 41.788  | 28.214 | 100.0%  | 10    |
  | nova.delete_server (2) | 2.702  | 4.558   | 6.714   | 6.78    | 6.847   | 4.351  | 100.0%  | 10    |
  | nova.delete_image      | 0.222  | 0.481   | 0.801   | 0.912   | 1.024   | 0.514  | 100.0%  | 10    |
  | total                  | 61.815 | 104.063 | 118.678 | 119.932 | 121.185 | 97.414 | 100.0%  | 10    |
  +------------------------+--------+---------+---------+---------+---------+--------+---------+-------+
  Load duration: 270.805267096
  Full duration: 295.748194933

  test scenario NovaKeypair.boot_and_delete_server_with_keypair
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | nova.create_keypair | 0.371 | 0.431  | 0.516  | 0.517  | 0.517  | 0.439 | 100.0%  | 10    |
  | nova.boot_server    | 3.04  | 4.457  | 5.757  | 5.786  | 5.815  | 4.552 | 100.0%  | 10    |
  | nova.delete_server  | 2.381 | 2.534  | 2.842  | 3.654  | 4.465  | 2.696 | 100.0%  | 10    |
  | nova.delete_keypair | 0.012 | 0.018  | 0.02   | 0.021  | 0.022  | 0.017 | 100.0%  | 10    |
  | total               | 5.958 | 7.497  | 9.018  | 9.735  | 10.452 | 7.704 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 22.5302600861
  Full duration: 46.1866869926

  test scenario NovaKeypair.create_and_list_keypairs
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.414 | 0.575  | 0.631  | 0.71   | 0.789 | 0.556 | 100.0%  | 10    |
  | nova.list_keypairs  | 0.013 | 0.018  | 0.02   | 0.021  | 0.021 | 0.018 | 100.0%  | 10    |
  | total               | 0.433 | 0.596  | 0.649  | 0.728  | 0.808 | 0.574 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.60233187675
  Full duration: 16.7130730152

  test scenario NovaServers.list_servers
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.list_servers | 0.587 | 0.606  | 0.69   | 0.722  | 0.755 | 0.631 | 100.0%  | 10    |
  | total             | 0.587 | 0.606  | 0.69   | 0.722  | 0.755 | 0.631 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.8859231472
  Full duration: 50.8739178181

  test scenario NovaServers.resize_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.363  | 3.918  | 6.304  | 6.779  | 7.255  | 4.596  | 100.0%  | 10    |
  | nova.resize         | 21.13  | 26.439 | 42.015 | 42.22  | 42.424 | 29.139 | 100.0%  | 10    |
  | nova.resize_confirm | 2.398  | 2.551  | 2.703  | 2.704  | 2.706  | 2.563  | 100.0%  | 10    |
  | nova.delete_server  | 2.37   | 2.395  | 2.798  | 3.721  | 4.644  | 2.648  | 100.0%  | 10    |
  | total               | 29.822 | 34.933 | 54.227 | 54.69  | 55.153 | 38.945 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 114.259507179
  Full duration: 128.127579927

  test scenario NovaServers.boot_server_from_volume_and_delete
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.235  | 5.567  | 6.045  | 6.052  | 6.06   | 4.919  | 100.0%  | 10    |
  | nova.boot_server     | 8.307  | 9.5    | 12.422 | 13.056 | 13.69  | 9.862  | 100.0%  | 10    |
  | nova.delete_server   | 4.461  | 4.62   | 4.671  | 4.692  | 4.714  | 4.589  | 100.0%  | 10    |
  | total                | 16.186 | 19.059 | 22.977 | 23.551 | 24.126 | 19.371 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 56.1163849831
  Full duration: 87.4642381668

  test scenario NovaServers.boot_and_migrate_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.453  | 4.707  | 6.199  | 6.246  | 6.293  | 4.887  | 100.0%  | 10    |
  | nova.stop_server    | 4.627  | 5.136  | 15.964 | 16.161 | 16.358 | 9.106  | 100.0%  | 10    |
  | nova.migrate        | 14.455 | 16.394 | 25.486 | 26.426 | 27.366 | 18.474 | 100.0%  | 10    |
  | nova.resize_confirm | 2.376  | 2.404  | 2.575  | 2.612  | 2.649  | 2.458  | 100.0%  | 10    |
  | nova.delete_server  | 2.351  | 2.377  | 2.42   | 2.479  | 2.538  | 2.394  | 100.0%  | 10    |
  | total               | 29.051 | 37.529 | 44.149 | 47.114 | 50.08  | 37.32  | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 101.067945957
  Full duration: 115.384446144

  test scenario NovaServers.boot_and_delete_server
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +--------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server   | 3.655 | 6.711  | 7.36   | 7.385  | 7.41   | 6.243  | 100.0%  | 10    |
  | nova.delete_server | 2.362 | 4.587  | 4.739  | 4.809  | 4.879  | 4.013  | 100.0%  | 10    |
  | total              | 6.017 | 10.937 | 11.962 | 12.02  | 12.078 | 10.256 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 29.3568899632
  Full duration: 52.9771959782

  test scenario NovaServers.boot_and_rebuild_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.859  | 4.72   | 6.26   | 6.315  | 6.369  | 5.06   | 100.0%  | 10    |
  | nova.rebuild_server | 6.283  | 7.559  | 9.599  | 12.803 | 16.006 | 8.2    | 100.0%  | 10    |
  | nova.delete_server  | 2.37   | 2.551  | 4.527  | 4.582  | 4.638  | 3.088  | 100.0%  | 10    |
  | total               | 13.383 | 16.01  | 18.944 | 20.596 | 22.249 | 16.348 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 55.2873470783
  Full duration: 79.1774559021

  test scenario NovaSecGroup.create_and_list_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.595  | 1.928  | 2.017  | 2.036  | 2.055  | 1.891  | 100.0%  | 10    |
  | nova.create_100_rules          | 9.581  | 10.462 | 10.693 | 10.803 | 10.913 | 10.36  | 100.0%  | 10    |
  | nova.list_security_groups      | 0.136  | 0.189  | 0.245  | 0.272  | 0.299  | 0.198  | 100.0%  | 10    |
  | total                          | 11.447 | 12.553 | 12.839 | 12.881 | 12.923 | 12.449 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 36.6872730255
  Full duration: 63.5205390453

  test scenario NovaSecGroup.create_and_delete_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.492  | 1.946  | 2.157  | 2.214  | 2.271  | 1.932  | 100.0%  | 10    |
  | nova.create_100_rules          | 9.298  | 10.497 | 10.608 | 10.624 | 10.64  | 10.256 | 100.0%  | 10    |
  | nova.delete_10_security_groups | 0.783  | 1.061  | 1.126  | 1.132  | 1.138  | 1.005  | 100.0%  | 10    |
  | total                          | 11.788 | 13.418 | 13.784 | 13.788 | 13.793 | 13.194 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 38.9264039993
  Full duration: 53.6155569553

  test scenario NovaServers.boot_and_bounce_server
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  | action                  | min    | median | 90%ile | 95%ile  | max     | avg    | success | count |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  | nova.boot_server        | 3.546  | 5.034  | 5.948  | 6.012   | 6.077   | 4.964  | 100.0%  | 10    |
  | nova.reboot_server      | 2.449  | 4.78   | 6.939  | 6.961   | 6.984   | 5.332  | 100.0%  | 10    |
  | nova.soft_reboot_server | 6.583  | 6.718  | 18.85  | 72.219  | 125.589 | 18.596 | 100.0%  | 10    |
  | nova.stop_server        | 4.622  | 4.796  | 15.736 | 15.861  | 15.986  | 6.96   | 100.0%  | 10    |
  | nova.start_server       | 2.662  | 2.828  | 3.001  | 3.04    | 3.078   | 2.849  | 100.0%  | 10    |
  | nova.rescue_server      | 6.77   | 15.566 | 17.493 | 17.544  | 17.595  | 12.874 | 100.0%  | 10    |
  | nova.unrescue_server    | 2.291  | 4.444  | 4.571  | 4.583   | 4.596   | 3.643  | 100.0%  | 10    |
  | nova.delete_server      | 2.372  | 2.397  | 2.507  | 2.528   | 2.55    | 2.424  | 100.0%  | 10    |
  | total                   | 35.205 | 49.523 | 70.623 | 110.831 | 151.04  | 57.653 | 100.0%  | 10    |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  Load duration: 193.802706003
  Full duration: 217.975458145

  test scenario NovaServers.boot_server
  +--------------------------------------------------------------------------------------+
  |                                 Response Times (sec)                                 |
  +------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | action           | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server | 3.41 | 4.816  | 6.024  | 6.056  | 6.089 | 4.692 | 100.0%  | 10    |
  | total            | 3.41 | 4.816  | 6.024  | 6.057  | 6.089 | 4.692 | 100.0%  | 10    |
  +------------------+------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 13.1493849754
  Full duration: 37.5227308273

  test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
  +----------------------------------------------------------------------------------------------------------+
  |                                           Response Times (sec)                                           |
  +-----------------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action                            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-----------------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups    | 1.487 | 1.851  | 2.252  | 2.299  | 2.345  | 1.876  | 100.0%  | 10    |
  | nova.create_100_rules             | 9.079 | 10.618 | 10.831 | 10.864 | 10.897 | 10.241 | 100.0%  | 10    |
  | nova.boot_server                  | 4.315 | 4.525  | 5.609  | 5.629  | 5.649  | 4.901  | 100.0%  | 10    |
  | nova.get_attached_security_groups | 0.137 | 0.156  | 0.289  | 0.312  | 0.334  | 0.183  | 100.0%  | 10    |
  | nova.delete_server                | 2.381 | 2.417  | 2.572  | 2.663  | 2.754  | 2.47   | 100.0%  | 10    |
  | nova.delete_10_security_groups    | 0.844 | 1.033  | 1.131  | 1.171  | 1.212  | 1.021  | 100.0%  | 10    |
  | total                             | 18.91 | 21.054 | 21.677 | 21.936 | 22.195 | 20.692 | 100.0%  | 10    |
  +-----------------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 61.2168090343
  Full duration: 85.7305738926

  test scenario NovaServers.pause_and_unpause_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.337  | 5.865  | 6.135  | 6.166  | 6.198  | 5.184  | 100.0%  | 10    |
  | nova.pause_server   | 2.311  | 2.468  | 2.511  | 2.528  | 2.545  | 2.422  | 100.0%  | 10    |
  | nova.unpause_server | 2.306  | 2.47   | 2.538  | 2.548  | 2.558  | 2.441  | 100.0%  | 10    |
  | nova.delete_server  | 2.37   | 2.623  | 4.832  | 4.882  | 4.932  | 3.392  | 100.0%  | 10    |
  | total               | 10.861 | 13.388 | 15.614 | 15.649 | 15.684 | 13.439 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 39.8893749714
  Full duration: 65.2461550236

  test scenario NovaServers.boot_server_from_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.172  | 3.51   | 6.009  | 6.055  | 6.102  | 4.387  | 100.0%  | 10    |
  | nova.boot_server     | 7.575  | 8.761  | 11.062 | 12.16  | 13.258 | 9.396  | 100.0%  | 10    |
  | total                | 10.812 | 12.565 | 17.043 | 18.063 | 19.083 | 13.783 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 40.4101068974
  Full duration: 76.4117758274

  test scenario NovaServers.boot_and_list_server
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server  | 3.891 | 4.847  | 6.169  | 6.267  | 6.365 | 5.093 | 100.0%  | 10    |
  | nova.list_servers | 0.163 | 0.201  | 0.418  | 0.475  | 0.533 | 0.268 | 100.0%  | 10    |
  | total             | 4.296 | 5.066  | 6.393  | 6.646  | 6.899 | 5.361 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 15.2852530479
  Full duration: 50.1823370457

  run_rally - INFO - Test scenario: "nova" OK.
  run_rally - INFO - Starting test scenario "quotas" ...
  run_rally - INFO -
   Preparing input task
   Task  4d0fc176-8b72-4789-8249-7ca3ed815669: started
  Task 4d0fc176-8b72-4789-8249-7ca3ed815669: finished

  test scenario Quotas.cinder_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.591 | 0.621  | 0.669  | 0.672  | 0.674 | 0.626 | 100.0%  | 10    |
  | total                | 0.591 | 0.621  | 0.669  | 0.672  | 0.674 | 0.626 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.86674189568
  Full duration: 7.90543198586

  test scenario Quotas.neutron_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.243 | 0.257  | 0.271  | 0.271  | 0.271 | 0.258 | 100.0%  | 10    |
  | total                | 0.308 | 0.328  | 0.36   | 0.367  | 0.374 | 0.331 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.996067047119
  Full duration: 6.61853408813

  test scenario Quotas.cinder_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.568 | 0.604  | 0.623  | 0.677  | 0.732 | 0.611 | 100.0%  | 10    |
  | quotas.delete_quotas | 0.415 | 0.442  | 0.477  | 0.501  | 0.526 | 0.449 | 100.0%  | 10    |
  | total                | 0.992 | 1.049  | 1.142  | 1.165  | 1.188 | 1.06  | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.19247508049
  Full duration: 9.27472686768

  test scenario Quotas.nova_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.323 | 0.35   | 0.371  | 0.38   | 0.39  | 0.349 | 100.0%  | 7     |
  | quotas.delete_quotas | 0.02  | 0.021  | 0.023  | 0.024  | 0.025 | 0.022 | 71.4%   | 7     |
  | total                | 0.344 | 0.369  | 0.378  | 0.378  | 0.379 | 0.363 | 71.4%   | 7     |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.752856969833
  Full duration: 6.31551885605

  test scenario Quotas.nova_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.307 | 0.354  | 0.396  | 0.43   | 0.463 | 0.361 | 100.0%  | 10    |
  | total                | 0.307 | 0.354  | 0.396  | 0.43   | 0.463 | 0.361 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.06656098366
  Full duration: 6.7101290226

  run_rally - INFO - Test scenario: "quotas" Failed.
  run_rally - INFO - Starting test scenario "requests" ...
  run_rally - INFO -
   Preparing input task
   Task  16778409-ff5d-4254-aa3b-b80de677272e: started
  Task 16778409-ff5d-4254-aa3b-b80de677272e: finished

  test scenario HttpRequests.check_random_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 5.446 | 5.5    | 5.982  | 5.983  | 5.984 | 5.611 | 100.0%  | 10    |
  | total                  | 5.446 | 5.5    | 5.982  | 5.983  | 5.984 | 5.611 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.9417049885
  Full duration: 19.4220340252

  test scenario HttpRequests.check_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 5.459 | 5.479  | 5.494  | 5.501  | 5.508 | 5.478 | 100.0%  | 10    |
  | total                  | 5.459 | 5.479  | 5.494  | 5.501  | 5.508 | 5.478 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.4412920475
  Full duration: 18.8327140808

  run_rally - INFO - Test scenario: "requests" OK.
  run_rally - INFO -

                       Rally Summary Report
  +===================+============+===============+===========+
  | Module            | Duration   | nb. Test Run  | Success   |
  +===================+============+===============+===========+
  | authenticate      | 00:18      | 10            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | glance            | 01:28      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | cinder            | 16:35      | 50            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | heat              | 06:24      | 32            | 92.31%    |
  +-------------------+------------+---------------+-----------+
  | keystone          | 01:10      | 29            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | neutron           | 04:48      | 31            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | nova              | 25:39      | 61            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | quotas            | 00:36      | 7             | 94.28%    |
  +-------------------+------------+---------------+-----------+
  | requests          | 00:38      | 2             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  +===================+============+===============+===========+
  | TOTAL:            | 00:57:39   | 229           | 98.51%    |
  +===================+============+===============+===========+


SDN Controller
--------------

ODL
^^^
::

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
  Output:  /home/opnfv/output.xml
  Log:     /home/opnfv/log.html
  Report:  /home/opnfv/report.html
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
  vIMS - INFO - Cloudify deployment Start Time:'2016-02-22 22:37:41'
  vIMS - INFO - Writing the inputs file
  vIMS - INFO - Launching the cloudify-manager deployment
  vIMS - INFO - Cloudify-manager server is UP !
  vIMS - INFO - Cloudify deployment duration:'745.0'
  vIMS - INFO - Collect flavor id for all clearwater vm
  vIMS - INFO - vIMS VNF deployment Start Time:'2016-02-22 22:50:07'
  vIMS - INFO - Downloading the openstack-blueprint.yaml blueprint
  vIMS - INFO - Writing the inputs file
  vIMS - INFO - Launching the clearwater deployment
  vIMS - INFO - The deployment of clearwater-opnfv is ended
  vIMS - INFO - vIMS VNF deployment duration:'633.6'
  vIMS - INFO - vIMS functional test Start Time:'2016-02-22 23:03:48'
  vIMS - INFO - vIMS functional test duration:'4.1'
  vIMS - INFO - Launching the clearwater-opnfv undeployment
  vIMS - ERROR - Error when executing command /bin/bash -c 'source /home/opnfv/functest/data/vIMS/venv_cloudify/bin/activate; cd /home/opnfv/functest/data/vIMS/; cfy executions start -w uninstall -d clearwater-opnfv --timeout 1800 ; cfy deployments delete -d clearwater-opnfv; '
  vIMS - INFO - Launching the cloudify-manager undeployment
  vIMS - INFO - Cloudify-manager server has been successfully removed!
  vIMS - INFO - Removing vIMS tenant ..
  vIMS - INFO - Removing vIMS user ..
