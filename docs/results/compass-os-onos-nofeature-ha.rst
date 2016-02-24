.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for compass-os-onos-nofeature-ha
------------------------------------------------------

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
  vPing_ssh- INFO - vPing Start Time:'2016-02-22 16:24:22'
  vPing_ssh- INFO - Creating instance 'opnfv-vping-1'...
   name=opnfv-vping-1
   flavor=<Flavor: m1.small>
   image=defb6423-f831-4d2e-8a46-21171b471811
   network=47a5262f-1252-4ceb-b054-4d81216c1510

  vPing_ssh- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  vPing_ssh- INFO - Adding 'opnfv-vping-1' to security group 'vPing-sg'...
  vPing_ssh- INFO - Creating instance 'opnfv-vping-2'...
   name=opnfv-vping-2
   flavor=<Flavor: m1.small>
   image=defb6423-f831-4d2e-8a46-21171b471811
   network=47a5262f-1252-4ceb-b054-4d81216c1510

  vPing_ssh- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  vPing_ssh- INFO - Adding 'opnfv-vping-2' to security group 'vPing-sg'...
  vPing_ssh- INFO - Creating floating IP for VM 'opnfv-vping-2'...
  vPing_ssh- INFO - Floating IP created: '192.168.10.102'
  vPing_ssh- INFO - Associating floating ip: '192.168.10.102' to VM 'opnfv-vping-2'
  vPing_ssh- INFO - Trying to establish SSH connection to 192.168.10.102...
  vPing_ssh- INFO - Waiting for ping...
  vPing_ssh- INFO - vPing detected!
  vPing_ssh- INFO - vPing duration:'262.5' s.
  vPing_ssh- INFO - Cleaning up...
  vPing_ssh- INFO - vPing OK

Tempest
^^^^^^^
::

  FUNCTEST.info: Running Tempest tests...
  run_tempest - INFO - Creating tenant and user for Tempest suite
  2016-02-22 16:28:55.743 23855 INFO rally.verification.tempest.tempest [-] Starting: Creating configuration file for Tempest.
  2016-02-22 16:29:00.285 23855 INFO rally.verification.tempest.tempest [-] Completed: Creating configuration file for Tempest.

  run_tempest - INFO - Starting Tempest test suite: '--tests-file /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/custom_tests/test_list.txt'.
  Total results of verification:

  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | UUID                                 | Deployment UUID                      | Set name | Tests | Failures | Created at                 | Status   |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | ac98ac8a-e502-4828-ad00-5b6b9428c346 | 55a7fc58-ad0f-475c-88c7-369043ae2719 |          | 210   | 11       | 2016-02-22 16:29:01.778060 | finished |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+

  Tests:

  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | name                                                                                                                                     | time      | status  |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.38607   | success |
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.74194   | success |
  | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 8.91734   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 8.66925   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 10.63581  | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.06276   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.05257   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.05940   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.12623   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.06809   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.09008   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.06098   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.07950   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.05546   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.12715   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.12835   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.10113   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.06587   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 0.17079   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 0.11263   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.06114   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 0.52524   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 0.45980   | success |
  | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 0.95973   | success |
  | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 7.95218   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 302.25007 | fail    |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.10296   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.18670   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 342.44729 | fail    |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.00068   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 311.26623 | fail    |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.11079   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.20087   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 342.41636 | fail    |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.00101   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.07243   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 6.46736   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.16392   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.27404   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.17996   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 1.07085   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.17853   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.10615   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.09603   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.09373   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.09520   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.12248   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.51307   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00065   | skip    |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.14353   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.06854   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.01693   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.06418   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.06254   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.01346   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.01475   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.03419   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.06726   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.04958   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.26188   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.01624   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.06862   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.00048   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 7.97654   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 11.64967  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 310.79753 | fail    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.46854   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 326.22117 | fail    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 12.06790  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 19.04478  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 7.05743   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.07867   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.20214   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.59746   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.34277   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.33642   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.57047   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.60103   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.75531   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 2.75731   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 9.46973   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 13.28125  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 7.11541   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 7.96344   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 0.67669   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 1.77693   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 0.75065   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 1.78955   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 0.64498   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 1.71157   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 0.53460   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 0.49832   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 0.57201   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.46864   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 0.66619   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 0.72274   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 0.40295   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 0.58226   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.34041   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 0.75975   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.43415   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 0.42859   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 1.21474   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 1.25222   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 0.41021   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.09081   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.02184   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 0.96806   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.01307   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 0.46717   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.05568   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.09471   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.03604   | success |
  | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 340.34367 | fail    |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.43241   | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.11064   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.11956   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.01137   | success |
  | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.16401   | success |
  | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.05961   | success |
  | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.10927   | success |
  | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.02540   | success |
  | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 0.28040   | success |
  | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.14755   | success |
  | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 0.77153   | success |
  | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.12106   | success |
  | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.08473   | success |
  | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.12668   | success |
  | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.14400   | success |
  | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 0.91996   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.05010   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.02297   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.04885   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.01587   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.01260   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.01445   | success |
  | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.04696   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 0.60138   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 0.21576   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 0.42759   | success |
  | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 0.49116   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 0.79505   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 0.70780   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 0.56456   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 1.10523   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 3.54869   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 0.83123   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 1.58383   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 1.36920   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 1.08591   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.19026   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.07493   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.06495   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.02942   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.03500   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 1.05982   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.15572   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.10990   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.09926   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.04061   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.03720   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 1.04510   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 1.34649   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 0.59530   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.05189   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.04790   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 1.14770   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 1.11571   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 0.75502   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.04674   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.08023   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 3.25659   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 1.59393   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 1.18965   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 1.03248   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 2.64680   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 2.09130   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 1.43383   | success |
  | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 1.25843   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 0.66808   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 0.46888   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.03378   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 0.36912   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 0.76166   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.02877   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.36667   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 5.11422   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.02366   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 0.58931   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.43084   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.29860   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.48701   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.84124   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.35246   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 3.35082   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.02341   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 0.86551   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 1.65927   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 2.12480   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 2.76915   | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 12.56546  | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 9.57875   | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 11.23806  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 11.53830  | success |
  | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.09463   | success |
  | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.38766   | success |
  | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 358.88405 | fail    |
  | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 327.24468 | fail    |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 327.82000 | fail    |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 500.15877 | fail    |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  run_tempest - INFO - Results: {'timestart': '2016-02-2216:29:01.778060', 'duration': 1082, 'tests': 210, 'failures': 11}
  run_tempest - INFO - Pushing results to DB: 'http://testresults.opnfv.org/testapi/results'.
  run_tempest - INFO - Deleting tenant and user for Tempest suite)


Rally
^^^^^
::

  FUNCTEST.info: Running Rally benchmark suite...
  run_rally - INFO - Starting test scenario "authenticate" ...
  run_rally - INFO -
   Preparing input task
   Task  2944fcc5-089f-4ed8-851f-446508c45024: started
  Task 2944fcc5-089f-4ed8-851f-446508c45024: finished

  test scenario Authenticate.validate_glance
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_glance     | 0.122 | 0.162  | 0.216  | 0.225  | 0.234 | 0.169 | 100.0%  | 10    |
  | authenticate.validate_glance (2) | 0.039 | 0.042  | 0.052  | 0.072  | 0.092 | 0.047 | 100.0%  | 10    |
  | total                            | 0.258 | 0.3    | 0.34   | 0.34   | 0.341 | 0.299 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.893048048019
  Full duration: 3.09276199341

  test scenario Authenticate.keystone
  +-----------------------------------------------------------------------------+
  |                            Response Times (sec)                             |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | total  | 0.066 | 0.072  | 0.074  | 0.074  | 0.074 | 0.071 | 100.0%  | 10    |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.233579874039
  Full duration: 2.32735109329

  test scenario Authenticate.validate_heat
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_heat     | 0.113 | 0.133  | 0.255  | 0.267  | 0.28  | 0.161 | 100.0%  | 10    |
  | authenticate.validate_heat (2) | 0.021 | 0.09   | 0.147  | 0.163  | 0.179 | 0.085 | 100.0%  | 10    |
  | total                          | 0.254 | 0.338  | 0.389  | 0.402  | 0.415 | 0.327 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.968546152115
  Full duration: 3.10294985771

  test scenario Authenticate.validate_nova
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_nova     | 0.111 | 0.119  | 0.17   | 0.179  | 0.187 | 0.133 | 100.0%  | 10    |
  | authenticate.validate_nova (2) | 0.023 | 0.035  | 0.042  | 0.048  | 0.054 | 0.036 | 100.0%  | 10    |
  | total                          | 0.214 | 0.225  | 0.291  | 0.291  | 0.292 | 0.243 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.725472211838
  Full duration: 2.86061501503

  test scenario Authenticate.validate_cinder
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_cinder     | 0.098 | 0.112  | 0.138  | 0.14   | 0.143 | 0.118 | 100.0%  | 10    |
  | authenticate.validate_cinder (2) | 0.058 | 0.071  | 0.077  | 0.078  | 0.078 | 0.07  | 100.0%  | 10    |
  | total                            | 0.221 | 0.256  | 0.312  | 0.313  | 0.313 | 0.267 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.797883033752
  Full duration: 2.91927695274

  test scenario Authenticate.validate_neutron
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_neutron     | 0.108 | 0.124  | 0.192  | 0.195  | 0.198 | 0.138 | 100.0%  | 10    |
  | authenticate.validate_neutron (2) | 0.028 | 0.08   | 0.102  | 0.102  | 0.102 | 0.074 | 100.0%  | 10    |
  | total                             | 0.207 | 0.273  | 0.346  | 0.353  | 0.359 | 0.281 | 100.0%  | 10    |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.847912073135
  Full duration: 3.07389783859

  run_rally - INFO - Test scenario: "authenticate" OK.

  run_rally - INFO - Starting test scenario "glance" ...
  run_rally - INFO -
   Preparing input task
   Task  2fff3869-9689-44d4-b372-dd41fa2a38ec: started
  Task 2fff3869-9689-44d4-b372-dd41fa2a38ec: finished

  test scenario GlanceImages.list_images
  +---------------------------------------------------------------------------------------+
  |                                 Response Times (sec)                                  |
  +--------------------+-------+--------+--------+--------+-----+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-----+-------+---------+-------+
  | glance.list_images | 0.177 | 0.232  | 0.296  | 0.298  | 0.3 | 0.241 | 100.0%  | 10    |
  | total              | 0.177 | 0.232  | 0.296  | 0.298  | 0.3 | 0.241 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-----+-------+---------+-------+
  Load duration: 0.697636127472
  Full duration: 3.5939040184

  test scenario GlanceImages.create_image_and_boot_instances
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | glance.create_image | 2.763 | 2.903  | 3.45   | 3.45   | 3.45   | 3.052 | 100.0%  | 10    |
  | nova.boot_servers   | 4.51  | 6.909  | 7.772  | 7.907  | 8.042  | 6.735 | 100.0%  | 10    |
  | total               | 7.273 | 10.244 | 10.662 | 10.752 | 10.842 | 9.787 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 28.153493166
  Full duration: 53.9921939373

  test scenario GlanceImages.create_and_list_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 3.066 | 3.262  | 3.685  | 3.718  | 3.751 | 3.328 | 100.0%  | 10    |
  | glance.list_images  | 0.04  | 0.047  | 0.059  | 0.063  | 0.066 | 0.049 | 100.0%  | 10    |
  | total               | 3.107 | 3.324  | 3.734  | 3.767  | 3.8   | 3.376 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.83786201477
  Full duration: 14.2525467873

  test scenario GlanceImages.create_and_delete_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 2.758 | 3.01   | 3.624  | 3.641  | 3.658 | 3.096 | 100.0%  | 10    |
  | glance.delete_image | 0.119 | 0.159  | 0.282  | 0.338  | 0.394 | 0.189 | 100.0%  | 10    |
  | total               | 2.887 | 3.164  | 3.878  | 3.884  | 3.89  | 3.285 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.57883381844
  Full duration: 12.357642889

  run_rally - INFO - Test scenario: "glance" OK.

  run_rally - INFO - Starting test scenario "cinder" ...
  run_rally - INFO -
   Preparing input task
   Task  76a5a912-68db-4001-b4a1-9beac5ae37ea: started
  Task 76a5a912-68db-4001-b4a1-9beac5ae37ea: finished

  test scenario CinderVolumes.create_and_attach_volume
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
  +----------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | nova.boot_server     | 3.805  | 4.389  | 5.707  | 6.126  | 6.546  | 4.733 | 100.0%  | 10    |
  | cinder.create_volume | 2.687  | 2.841  | 2.929  | 2.954  | 2.978  | 2.833 | 100.0%  | 10    |
  | nova.attach_volume   | 7.618  | 7.963  | 8.416  | 9.348  | 10.28  | 8.167 | 100.0%  | 10    |
  | nova.detach_volume   | 2.997  | 3.285  | 5.265  | 5.314  | 5.362  | 3.992 | 100.0%  | 10    |
  | cinder.delete_volume | 2.425  | 2.506  | 2.557  | 2.658  | 2.759  | 2.516 | 100.0%  | 10    |
  | nova.delete_server   | 2.379  | 2.447  | 2.618  | 2.639  | 2.659  | 2.478 | 100.0%  | 10    |
  | total                | 23.106 | 25.014 | 25.886 | 26.355 | 26.825 | 24.72 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 75.3569400311
  Full duration: 87.994022131

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 5.261 | 5.355  | 5.486  | 5.512  | 5.539 | 5.367 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.069 | 0.121  | 0.135  | 0.151  | 0.168 | 0.12  | 100.0%  | 10    |
  | total                | 5.351 | 5.501  | 5.595  | 5.626  | 5.658 | 5.487 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.505685091
  Full duration: 27.6703879833

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.758 | 2.928  | 3.178  | 3.185  | 3.192 | 2.955 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.11  | 0.124  | 0.158  | 0.159  | 0.161 | 0.128 | 100.0%  | 10    |
  | total                | 2.878 | 3.071  | 3.319  | 3.327  | 3.334 | 3.084 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.14664101601
  Full duration: 20.325412035

  test scenario CinderVolumes.create_and_list_snapshots
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.401 | 2.521  | 2.599  | 2.615  | 2.632 | 2.517 | 100.0%  | 10    |
  | cinder.list_snapshots  | 0.022 | 0.083  | 0.12   | 0.15   | 0.18  | 0.089 | 100.0%  | 10    |
  | total                  | 2.474 | 2.588  | 2.729  | 2.753  | 2.776 | 2.606 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 7.73569321632
  Full duration: 31.2840220928

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.796 | 2.999  | 3.144  | 3.15   | 3.156 | 2.996 | 100.0%  | 10    |
  | cinder.delete_volume | 2.455 | 2.614  | 2.708  | 2.725  | 2.742 | 2.616 | 100.0%  | 10    |
  | total                | 5.328 | 5.602  | 5.851  | 5.868  | 5.885 | 5.612 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.477782011
  Full duration: 22.7058889866

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.919 | 5.48   | 5.628  | 5.639  | 5.649 | 5.227 | 100.0%  | 10    |
  | cinder.delete_volume | 2.526 | 2.693  | 2.72   | 2.755  | 2.79  | 2.663 | 100.0%  | 10    |
  | total                | 5.62  | 8.087  | 8.341  | 8.375  | 8.409 | 7.89  | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.1292200089
  Full duration: 30.4960770607

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.85  | 2.948  | 3.049  | 3.07   | 3.09  | 2.953 | 100.0%  | 10    |
  | cinder.delete_volume | 2.464 | 2.529  | 2.614  | 2.615  | 2.615 | 2.54  | 100.0%  | 10    |
  | total                | 5.325 | 5.506  | 5.652  | 5.656  | 5.661 | 5.493 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.3896708488
  Full duration: 22.6766388416

  test scenario CinderVolumes.create_and_upload_volume_to_image
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume          | 2.872  | 3.051  | 3.667  | 3.678  | 3.688  | 3.15   | 100.0%  | 10    |
  | cinder.upload_volume_to_image | 28.915 | 62.489 | 77.495 | 77.616 | 77.736 | 60.612 | 100.0%  | 10    |
  | cinder.delete_volume          | 2.362  | 2.491  | 2.538  | 2.611  | 2.684  | 2.494  | 100.0%  | 10    |
  | nova.delete_image             | 0.209  | 0.455  | 0.893  | 0.906  | 0.919  | 0.514  | 100.0%  | 10    |
  | total                         | 35.229 | 68.483 | 83.109 | 83.228 | 83.346 | 66.77  | 100.0%  | 10    |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 193.43104291
  Full duration: 200.303003073

  test scenario CinderVolumes.create_and_delete_snapshot
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.422 | 2.503  | 2.568  | 2.571  | 2.575 | 2.507 | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.313 | 2.444  | 2.482  | 2.492  | 2.501 | 2.427 | 100.0%  | 10    |
  | total                  | 4.793 | 4.964  | 5.013  | 5.018  | 5.024 | 4.935 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.7233128548
  Full duration: 33.1759068966

  test scenario CinderVolumes.create_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.844 | 2.948  | 3.269  | 3.319  | 3.369 | 3.015 | 100.0%  | 10    |
  | total                | 2.844 | 2.948  | 3.269  | 3.319  | 3.369 | 3.015 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 8.9167098999
  Full duration: 18.3895540237

  test scenario CinderVolumes.create_volume
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +----------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg  | success | count |
  +----------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | cinder.create_volume | 2.854 | 2.953  | 3.096  | 3.121  | 3.146 | 2.98 | 100.0%  | 10    |
  | total                | 2.854 | 2.953  | 3.096  | 3.121  | 3.146 | 2.98 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+------+---------+-------+
  Load duration: 8.90475797653
  Full duration: 20.1169910431

  test scenario CinderVolumes.list_volumes
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.list_volumes | 0.228 | 0.266  | 0.286  | 0.317  | 0.348 | 0.268 | 100.0%  | 10    |
  | total               | 0.228 | 0.266  | 0.287  | 0.317  | 0.348 | 0.268 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.792151927948
  Full duration: 47.0951080322

  test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.829  | 2.905  | 2.967  | 2.969  | 2.971  | 2.899  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.302  | 2.402  | 2.432  | 2.455  | 2.478  | 2.392  | 100.0%  | 10    |
  | nova.attach_volume     | 7.72   | 7.953  | 11.462 | 12.036 | 12.61  | 8.943  | 100.0%  | 10    |
  | nova.detach_volume     | 2.903  | 4.153  | 5.343  | 5.534  | 5.724  | 4.179  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.258  | 2.311  | 2.403  | 2.446  | 2.49   | 2.331  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.387  | 2.497  | 2.6    | 2.623  | 2.647  | 2.496  | 100.0%  | 10    |
  | total                  | 21.145 | 23.329 | 26.38  | 26.678 | 26.977 | 23.543 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 68.2392091751
  Full duration: 106.915300131

  test scenario CinderVolumes.create_from_volume_and_delete_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 7.712  | 12.285 | 17.231 | 18.187 | 19.144 | 12.995 | 100.0%  | 10    |
  | cinder.delete_volume | 2.494  | 2.633  | 4.76   | 4.808  | 4.856  | 3.025  | 100.0%  | 10    |
  | total                | 10.216 | 16.032 | 19.868 | 20.756 | 21.645 | 16.019 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 44.5057139397
  Full duration: 63.1546430588

  test scenario CinderVolumes.create_and_extend_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.887 | 2.994  | 3.283  | 3.324  | 3.364 | 3.038 | 100.0%  | 10    |
  | cinder.extend_volume | 2.593 | 2.748  | 2.812  | 2.924  | 3.037 | 2.754 | 100.0%  | 10    |
  | cinder.delete_volume | 2.417 | 2.569  | 2.707  | 2.724  | 2.74  | 2.562 | 100.0%  | 10    |
  | total                | 8.03  | 8.369  | 8.538  | 8.631  | 8.723 | 8.353 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.8781170845
  Full duration: 31.6701009274

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.736  | 2.972  | 3.155  | 3.173  | 3.19   | 2.98   | 100.0%  | 10    |
  | cinder.create_snapshot | 2.321  | 2.38   | 2.392  | 2.399  | 2.406  | 2.369  | 100.0%  | 10    |
  | nova.attach_volume     | 7.503  | 7.861  | 12.563 | 13.795 | 15.028 | 9.196  | 100.0%  | 10    |
  | nova.detach_volume     | 3.269  | 5.314  | 5.356  | 5.366  | 5.375  | 4.908  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.21   | 2.305  | 2.435  | 2.442  | 2.45   | 2.323  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.413  | 2.499  | 2.584  | 2.597  | 2.611  | 2.505  | 100.0%  | 10    |
  | total                  | 21.356 | 23.78  | 28.296 | 29.607 | 30.917 | 24.594 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 70.9472367764
  Full duration: 114.492169142

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.736  | 2.845  | 3.037  | 3.081  | 3.125  | 2.876  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.343  | 2.399  | 2.462  | 2.479  | 2.495  | 2.405  | 100.0%  | 10    |
  | nova.attach_volume     | 7.59   | 7.737  | 13.073 | 16.133 | 19.193 | 9.585  | 100.0%  | 10    |
  | nova.detach_volume     | 2.916  | 5.205  | 5.382  | 5.39   | 5.397  | 4.608  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.203  | 2.364  | 2.427  | 2.455  | 2.483  | 2.347  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.421  | 2.547  | 2.613  | 2.662  | 2.71   | 2.55   | 100.0%  | 10    |
  | total                  | 21.034 | 23.722 | 27.391 | 31.314 | 35.237 | 24.898 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 73.5739891529
  Full duration: 116.225493908

  run_rally - INFO - Test scenario: "cinder" OK.

  run_rally - INFO - Starting test scenario "heat" ...
  run_rally - INFO -
   Preparing input task
   Task  c9827201-74f8-41fc-8510-938cca773ec1: started
  Task c9827201-74f8-41fc-8510-938cca773ec1: finished

  test scenario HeatStacks.create_suspend_resume_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack  | 2.872 | 3.106  | 3.406  | 3.484  | 3.562 | 3.155 | 100.0%  | 10    |
  | heat.suspend_stack | 0.442 | 0.625  | 1.717  | 1.738  | 1.759 | 0.931 | 100.0%  | 10    |
  | heat.resume_stack  | 0.537 | 1.658  | 1.746  | 1.816  | 1.886 | 1.424 | 100.0%  | 10    |
  | heat.delete_stack  | 0.502 | 1.432  | 1.591  | 1.6    | 1.609 | 1.362 | 100.0%  | 10    |
  | total              | 5.462 | 6.793  | 8.103  | 8.346  | 8.589 | 6.872 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 19.5646238327
  Full duration: 22.7670919895

  test scenario HeatStacks.create_and_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.903 | 3.075  | 3.47   | 3.485  | 3.501 | 3.168 | 100.0%  | 10    |
  | heat.delete_stack | 0.399 | 1.444  | 1.664  | 1.668  | 1.672 | 1.316 | 100.0%  | 10    |
  | total             | 3.367 | 4.479  | 4.942  | 5.031  | 5.12  | 4.484 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 13.5260851383
  Full duration: 16.6767499447

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 10.422 | 12.344 | 12.812 | 13.47  | 14.128 | 12.097 | 100.0%  | 10    |
  | heat.delete_stack | 6.869  | 8.251  | 9.518  | 9.918  | 10.317 | 8.407  | 100.0%  | 10    |
  | total             | 18.742 | 20.619 | 22.144 | 22.228 | 22.313 | 20.504 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 60.1647601128
  Full duration: 63.2413249016

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 12.861 | 14.13  | 16.111 | 16.328 | 16.545 | 14.294 | 100.0%  | 10    |
  | heat.delete_stack | 8.256  | 8.951  | 9.675  | 9.958  | 10.241 | 8.968  | 100.0%  | 10    |
  | total             | 21.289 | 22.778 | 24.964 | 25.875 | 26.786 | 23.262 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 70.9971709251
  Full duration: 74.4355139732

  test scenario HeatStacks.list_stacks_and_resources
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg  | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | heat.list_stacks                | 0.221 | 0.269  | 0.393  | 0.397  | 0.401 | 0.29 | 100.0%  | 10    |
  | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0   | 0.0  | 100.0%  | 10    |
  | total                           | 0.221 | 0.269  | 0.393  | 0.397  | 0.401 | 0.29 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  Load duration: 0.845721006393
  Full duration: 3.40288186073

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.871 | 3.088  | 3.407  | 3.415  | 3.422 | 3.124 | 100.0%  | 10    |
  | heat.update_stack | 2.568 | 3.106  | 3.925  | 3.953  | 3.981 | 3.187 | 100.0%  | 10    |
  | heat.delete_stack | 1.369 | 1.555  | 1.647  | 1.686  | 1.724 | 1.55  | 100.0%  | 10    |
  | total             | 7.072 | 7.871  | 8.535  | 8.749  | 8.963 | 7.861 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.2382650375
  Full duration: 27.7685508728

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.836 | 3.105  | 3.233  | 3.257  | 3.281 | 3.098 | 100.0%  | 10    |
  | heat.update_stack | 2.501 | 2.628  | 3.613  | 3.804  | 3.995 | 2.859 | 100.0%  | 10    |
  | heat.delete_stack | 0.298 | 0.994  | 1.511  | 1.565  | 1.62  | 1.001 | 100.0%  | 10    |
  | total             | 5.886 | 6.758  | 8.232  | 8.564  | 8.895 | 6.957 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 20.5952920914
  Full duration: 23.9688129425

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.896 | 3.156  | 3.462  | 3.752  | 4.042 | 3.241 | 100.0%  | 10    |
  | heat.update_stack | 4.942 | 5.218  | 5.956  | 6.09   | 6.224 | 5.42  | 100.0%  | 10    |
  | heat.delete_stack | 1.551 | 1.665  | 2.721  | 2.788  | 2.856 | 2.038 | 100.0%  | 10    |
  | total             | 9.408 | 10.658 | 11.602 | 11.761 | 11.92 | 10.7  | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 31.6187429428
  Full duration: 35.1271891594

  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 6.39157295227
  Full duration: 14.0238859653

  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg    | success | count |
  +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
  | heat.create_stack | 2.944 | 3.08   | 3.202  | 3.309  | 3.415 | 3.09   | 100.0%  | 10    |
  | heat.update_stack | 4.794 | 5.017  | 5.255  | 5.579  | 5.904 | 5.077  | 100.0%  | 10    |
  | heat.delete_stack | 1.435 | 1.866  | 2.632  | 2.657  | 2.682 | 1.998  | 100.0%  | 10    |
  | total             | 9.394 | 10.052 | 10.876 | 10.903 | 10.93 | 10.165 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
  Load duration: 30.0142600536
  Full duration: 33.6354219913

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.874 | 3.099  | 3.257  | 3.296  | 3.334 | 3.084 | 100.0%  | 10    |
  | heat.update_stack | 3.576 | 3.724  | 4.103  | 4.118  | 4.132 | 3.804 | 100.0%  | 10    |
  | heat.delete_stack | 0.597 | 1.497  | 1.641  | 1.685  | 1.73  | 1.368 | 100.0%  | 10    |
  | total             | 7.498 | 8.373  | 8.618  | 8.72   | 8.823 | 8.256 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.9089329243
  Full duration: 28.905012846

  test scenario HeatStacks.create_and_list_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.986 | 3.186  | 3.26   | 3.309  | 3.358 | 3.166 | 100.0%  | 10    |
  | heat.list_stacks  | 0.035 | 0.163  | 0.192  | 0.205  | 0.218 | 0.128 | 100.0%  | 10    |
  | total             | 3.039 | 3.305  | 3.472  | 3.495  | 3.518 | 3.294 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.91034293175
  Full duration: 16.8483679295

  test scenario HeatStacks.create_check_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.822 | 3.0    | 3.403  | 3.446  | 3.489 | 3.098 | 100.0%  | 10    |
  | heat.check_stack  | 0.309 | 0.676  | 0.899  | 0.908  | 0.917 | 0.632 | 100.0%  | 10    |
  | heat.delete_stack | 0.504 | 1.466  | 1.619  | 1.685  | 1.751 | 1.235 | 100.0%  | 10    |
  | total             | 3.978 | 5.166  | 5.376  | 5.433  | 5.49  | 4.964 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 15.3095350266
  Full duration: 19.0696201324

  run_rally - INFO - Test scenario: "heat" Failed.

  run_rally - INFO - Starting test scenario "keystone" ...
  run_rally - INFO -
   Preparing input task
   Task  b0246610-2dd7-4817-be66-9315ab169066: started
  Task b0246610-2dd7-4817-be66-9315ab169066: finished

  test scenario KeystoneBasic.create_tenant_with_users
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.11  | 0.13   | 0.144  | 0.153  | 0.161 | 0.131 | 100.0%  | 10    |
  | keystone.create_users  | 0.628 | 0.692  | 0.803  | 0.847  | 0.89  | 0.717 | 100.0%  | 10    |
  | total                  | 0.755 | 0.826  | 0.934  | 0.979  | 1.025 | 0.849 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.49157500267
  Full duration: 12.6573908329

  test scenario KeystoneBasic.create_add_and_list_user_roles
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.11  | 0.114  | 0.125  | 0.127  | 0.129 | 0.117 | 100.0%  | 10    |
  | keystone.add_role    | 0.087 | 0.099  | 0.117  | 0.134  | 0.152 | 0.105 | 100.0%  | 10    |
  | keystone.list_roles  | 0.049 | 0.053  | 0.068  | 0.084  | 0.101 | 0.059 | 100.0%  | 10    |
  | total                | 0.261 | 0.277  | 0.302  | 0.307  | 0.313 | 0.281 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.859135150909
  Full duration: 5.88745498657

  test scenario KeystoneBasic.add_and_remove_user_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.109 | 0.188  | 0.253  | 0.27   | 0.287 | 0.184 | 100.0%  | 10    |
  | keystone.add_role    | 0.087 | 0.1    | 0.119  | 0.125  | 0.13  | 0.103 | 100.0%  | 10    |
  | keystone.remove_role | 0.06  | 0.069  | 0.173  | 0.196  | 0.218 | 0.102 | 100.0%  | 10    |
  | total                | 0.263 | 0.393  | 0.518  | 0.556  | 0.594 | 0.39  | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.32334089279
  Full duration: 6.50031495094

  test scenario KeystoneBasic.create_update_and_delete_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.108 | 0.217  | 0.267  | 0.272  | 0.277 | 0.192 | 100.0%  | 10    |
  | keystone.update_tenant | 0.05  | 0.057  | 0.062  | 0.068  | 0.074 | 0.058 | 100.0%  | 10    |
  | keystone.delete_tenant | 0.119 | 0.132  | 0.141  | 0.142  | 0.142 | 0.132 | 100.0%  | 10    |
  | total                  | 0.289 | 0.392  | 0.46   | 0.462  | 0.465 | 0.381 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.16795897484
  Full duration: 5.16257286072

  test scenario KeystoneBasic.create_and_delete_service
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_service | 0.105 | 0.121  | 0.153  | 0.169  | 0.185 | 0.13  | 100.0%  | 10    |
  | keystone.delete_service | 0.053 | 0.06   | 0.065  | 0.072  | 0.079 | 0.061 | 100.0%  | 10    |
  | total                   | 0.169 | 0.182  | 0.23   | 0.234  | 0.239 | 0.191 | 100.0%  | 10    |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.56450510025
  Full duration: 4.22321987152

  test scenario KeystoneBasic.create_tenant
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg  | success | count |
  +------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | keystone.create_tenant | 0.112 | 0.138  | 0.161  | 0.165  | 0.168 | 0.14 | 100.0%  | 10    |
  | total                  | 0.112 | 0.138  | 0.161  | 0.165  | 0.168 | 0.14 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  Load duration: 0.417885065079
  Full duration: 4.0450899601

  test scenario KeystoneBasic.create_user
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.126 | 0.177  | 0.186  | 0.189  | 0.191 | 0.164 | 100.0%  | 10    |
  | total                | 0.126 | 0.177  | 0.186  | 0.189  | 0.191 | 0.164 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.485447883606
  Full duration: 4.35393500328

  test scenario KeystoneBasic.create_and_list_tenants
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.117 | 0.13   | 0.139  | 0.139  | 0.14  | 0.129 | 100.0%  | 10    |
  | keystone.list_tenants  | 0.047 | 0.053  | 0.094  | 0.107  | 0.121 | 0.063 | 100.0%  | 10    |
  | total                  | 0.167 | 0.186  | 0.212  | 0.233  | 0.253 | 0.192 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.566509962082
  Full duration: 5.80973696709

  test scenario KeystoneBasic.create_and_delete_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.109 | 0.227  | 0.291  | 0.3    | 0.308 | 0.205 | 100.0%  | 10    |
  | keystone.delete_role | 0.106 | 0.114  | 0.238  | 0.25   | 0.263 | 0.14  | 100.0%  | 10    |
  | total                | 0.222 | 0.34   | 0.544  | 0.548  | 0.552 | 0.345 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.969199895859
  Full duration: 5.0005710125

  test scenario KeystoneBasic.get_entities
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.115 | 0.13   | 0.153  | 0.154  | 0.154 | 0.131 | 100.0%  | 10    |
  | keystone.create_user   | 0.059 | 0.063  | 0.068  | 0.075  | 0.083 | 0.065 | 100.0%  | 10    |
  | keystone.create_role   | 0.046 | 0.06   | 0.085  | 0.085  | 0.086 | 0.061 | 100.0%  | 10    |
  | keystone.get_tenant    | 0.044 | 0.051  | 0.058  | 0.06   | 0.062 | 0.051 | 100.0%  | 10    |
  | keystone.get_user      | 0.052 | 0.067  | 0.103  | 0.106  | 0.109 | 0.07  | 100.0%  | 10    |
  | keystone.get_role      | 0.042 | 0.049  | 0.066  | 0.067  | 0.068 | 0.052 | 100.0%  | 10    |
  | keystone.service_list  | 0.044 | 0.05   | 0.067  | 0.083  | 0.099 | 0.055 | 100.0%  | 10    |
  | keystone.get_service   | 0.041 | 0.044  | 0.051  | 0.052  | 0.054 | 0.046 | 100.0%  | 10    |
  | total                  | 0.489 | 0.533  | 0.57   | 0.572  | 0.574 | 0.532 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.58059597015
  Full duration: 9.58514809608

  test scenario KeystoneBasic.create_and_list_users
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.129 | 0.139  | 0.153  | 0.167  | 0.181 | 0.143 | 100.0%  | 10    |
  | keystone.list_users  | 0.046 | 0.054  | 0.073  | 0.079  | 0.084 | 0.06  | 100.0%  | 10    |
  | total                | 0.185 | 0.198  | 0.222  | 0.227  | 0.232 | 0.203 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.615728855133
  Full duration: 4.46038007736

  run_rally - INFO - Test scenario: "keystone" OK.

  run_rally - INFO - Starting test scenario "neutron" ...
  run_rally - INFO -
   Preparing input task
   Task  60b0f938-d4b3-4eae-9392-3ac4c8a6a4b7: started
  Task 60b0f938-d4b3-4eae-9392-3ac4c8a6a4b7: finished

  test scenario NeutronNetworks.create_and_delete_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.448 | 0.508  | 0.67   | 0.679  | 0.687 | 0.525 | 100.0%  | 10    |
  | neutron.delete_port | 0.152 | 0.299  | 0.373  | 0.376  | 0.378 | 0.301 | 100.0%  | 10    |
  | total               | 0.6   | 0.817  | 0.958  | 0.977  | 0.995 | 0.826 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.44042801857
  Full duration: 24.5799560547

  test scenario NeutronNetworks.create_and_list_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.392 | 0.512  | 0.61   | 0.629  | 0.649 | 0.519 | 100.0%  | 10    |
  | neutron.create_router        | 0.032 | 0.176  | 0.253  | 0.254  | 0.256 | 0.156 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.227 | 0.375  | 0.444  | 0.468  | 0.492 | 0.366 | 100.0%  | 10    |
  | neutron.list_routers         | 0.03  | 0.151  | 0.184  | 0.196  | 0.207 | 0.115 | 100.0%  | 10    |
  | total                        | 0.942 | 1.153  | 1.326  | 1.377  | 1.429 | 1.157 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.41682577133
  Full duration: 27.1603848934

  test scenario NeutronNetworks.create_and_delete_routers
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet           | 0.406 | 0.478  | 0.571  | 0.602  | 0.634 | 0.488 | 100.0%  | 10    |
  | neutron.create_router           | 0.032 | 0.189  | 0.275  | 0.28   | 0.284 | 0.183 | 100.0%  | 10    |
  | neutron.add_interface_router    | 0.232 | 0.326  | 0.474  | 0.479  | 0.484 | 0.337 | 100.0%  | 10    |
  | neutron.remove_interface_router | 0.163 | 0.25   | 0.492  | 0.5    | 0.508 | 0.288 | 100.0%  | 10    |
  | neutron.delete_router           | 0.126 | 0.229  | 0.301  | 0.356  | 0.41  | 0.224 | 100.0%  | 10    |
  | total                           | 1.294 | 1.49   | 1.698  | 1.753  | 1.807 | 1.52  | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.38407206535
  Full duration: 28.0664179325

  test scenario NeutronNetworks.create_and_list_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.433 | 0.663  | 0.718  | 0.718  | 0.719 | 0.601 | 100.0%  | 10    |
  | neutron.list_ports  | 0.089 | 0.231  | 0.345  | 0.385  | 0.425 | 0.243 | 100.0%  | 10    |
  | total               | 0.524 | 0.843  | 1.028  | 1.072  | 1.117 | 0.844 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.59062600136
  Full duration: 25.9457578659

  test scenario NeutronNetworks.create_and_delete_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.387 | 0.429  | 0.52   | 0.533  | 0.545 | 0.452 | 100.0%  | 10    |
  | neutron.delete_subnet | 0.144 | 0.296  | 0.356  | 0.367  | 0.378 | 0.275 | 100.0%  | 10    |
  | total                 | 0.573 | 0.733  | 0.811  | 0.829  | 0.846 | 0.727 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.22101807594
  Full duration: 24.9812419415

  test scenario NeutronNetworks.create_and_delete_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.293 | 0.395  | 0.476  | 0.482  | 0.488 | 0.397 | 100.0%  | 10    |
  | neutron.delete_network | 0.103 | 0.24   | 0.332  | 0.344  | 0.357 | 0.228 | 100.0%  | 10    |
  | total                  | 0.471 | 0.585  | 0.766  | 0.798  | 0.829 | 0.625 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.84316086769
  Full duration: 14.2107710838

  test scenario NeutronNetworks.create_and_list_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.31  | 0.347  | 0.452  | 0.454  | 0.455 | 0.362 | 100.0%  | 10    |
  | neutron.list_networks  | 0.042 | 0.111  | 0.199  | 0.24   | 0.281 | 0.124 | 100.0%  | 10    |
  | total                  | 0.358 | 0.493  | 0.603  | 0.624  | 0.644 | 0.486 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.45903801918
  Full duration: 15.4646441936

  test scenario NeutronNetworks.create_and_update_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.382 | 0.419  | 0.612  | 0.613  | 0.614 | 0.478 | 100.0%  | 10    |
  | neutron.create_router        | 0.033 | 0.176  | 0.22   | 0.239  | 0.258 | 0.149 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.229 | 0.272  | 0.394  | 0.458  | 0.522 | 0.307 | 100.0%  | 10    |
  | neutron.update_router        | 0.091 | 0.252  | 0.307  | 0.324  | 0.342 | 0.221 | 100.0%  | 10    |
  | total                        | 0.938 | 1.105  | 1.328  | 1.406  | 1.484 | 1.156 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.27084898949
  Full duration: 27.761991024

  test scenario NeutronNetworks.create_and_update_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.306 | 0.356  | 0.425  | 0.429  | 0.433 | 0.366 | 100.0%  | 10    |
  | neutron.update_network | 0.113 | 0.27   | 0.33   | 0.337  | 0.343 | 0.24  | 100.0%  | 10    |
  | total                  | 0.423 | 0.611  | 0.763  | 0.763  | 0.764 | 0.606 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.81449484825
  Full duration: 15.7938911915

  test scenario NeutronNetworks.create_and_update_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.431 | 0.488  | 0.702  | 0.707  | 0.711 | 0.521 | 100.0%  | 10    |
  | neutron.update_port | 0.11  | 0.256  | 0.37   | 0.39   | 0.409 | 0.23  | 100.0%  | 10    |
  | total               | 0.541 | 0.758  | 0.865  | 0.987  | 1.11  | 0.752 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.09433794022
  Full duration: 26.3668129444

  test scenario NeutronNetworks.create_and_list_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.391 | 0.421  | 0.542  | 0.558  | 0.574 | 0.449 | 100.0%  | 10    |
  | neutron.list_subnets  | 0.059 | 0.135  | 0.295  | 0.332  | 0.37  | 0.163 | 100.0%  | 10    |
  | total                 | 0.45  | 0.631  | 0.736  | 0.752  | 0.769 | 0.612 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.75437092781
  Full duration: 25.2292289734

  test scenario NeutronNetworks.create_and_update_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.4   | 0.45   | 0.535  | 0.536  | 0.537 | 0.462 | 100.0%  | 10    |
  | neutron.update_subnet | 0.158 | 0.306  | 0.397  | 0.412  | 0.427 | 0.3   | 100.0%  | 10    |
  | total                 | 0.564 | 0.773  | 0.88   | 0.904  | 0.929 | 0.763 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.266477108
  Full duration: 25.2276790142

  run_rally - INFO - Test scenario: "neutron" OK.

  run_rally - INFO - Starting test scenario "nova" ...
  run_rally - INFO -
   Preparing input task
   Task  51b9485f-50cd-43c0-89c7-901e4b55ffa4: started
  Task 51b9485f-50cd-43c0-89c7-901e4b55ffa4: finished

  test scenario NovaKeypair.create_and_delete_keypair
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.378 | 0.469  | 0.572  | 0.585  | 0.599 | 0.487 | 100.0%  | 10    |
  | nova.delete_keypair | 0.018 | 0.021  | 0.031  | 0.032  | 0.032 | 0.023 | 100.0%  | 10    |
  | total               | 0.41  | 0.487  | 0.592  | 0.607  | 0.621 | 0.51  | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.44199299812
  Full duration: 14.8640050888

  test scenario NovaServers.snapshot_server
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | action                 | min    | median | 90%ile  | 95%ile  | max     | avg    | success | count |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | nova.boot_server       | 3.252  | 5.309  | 6.304   | 6.39    | 6.476   | 5.049  | 100.0%  | 10    |
  | nova.create_image      | 27.858 | 48.811 | 65.726  | 65.73   | 65.734  | 47.725 | 100.0%  | 10    |
  | nova.delete_server     | 2.519  | 2.96   | 5.038   | 5.043   | 5.047   | 3.302  | 100.0%  | 10    |
  | nova.boot_server (2)   | 14.132 | 28.496 | 38.684  | 44.307  | 49.929  | 28.943 | 100.0%  | 10    |
  | nova.delete_server (2) | 2.39   | 4.627  | 7.042   | 7.135   | 7.229   | 4.368  | 100.0%  | 10    |
  | nova.delete_image      | 0.317  | 0.482  | 1.285   | 1.976   | 2.667   | 0.749  | 100.0%  | 10    |
  | total                  | 61.01  | 97.217 | 121.154 | 121.205 | 121.255 | 90.137 | 100.0%  | 10    |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  Load duration: 248.724915028
  Full duration: 271.744755983

  test scenario NovaKeypair.boot_and_delete_server_with_keypair
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | nova.create_keypair | 0.436 | 0.508  | 0.611  | 0.618  | 0.624  | 0.52  | 100.0%  | 10    |
  | nova.boot_server    | 3.084 | 4.238  | 6.002  | 6.114  | 6.226  | 4.436 | 100.0%  | 10    |
  | nova.delete_server  | 2.385 | 2.558  | 3.021  | 3.844  | 4.667  | 2.752 | 100.0%  | 10    |
  | nova.delete_keypair | 0.015 | 0.02   | 0.024  | 0.024  | 0.025  | 0.02  | 100.0%  | 10    |
  | total               | 5.997 | 7.197  | 9.438  | 10.178 | 10.917 | 7.728 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 22.9343290329
  Full duration: 44.7740108967

  test scenario NovaKeypair.create_and_list_keypairs
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.367 | 0.477  | 0.546  | 0.584  | 0.622 | 0.473 | 100.0%  | 10    |
  | nova.list_keypairs  | 0.014 | 0.019  | 0.025  | 0.028  | 0.03  | 0.021 | 100.0%  | 10    |
  | total               | 0.384 | 0.501  | 0.565  | 0.601  | 0.636 | 0.494 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.53178596497
  Full duration: 16.4732458591

  test scenario NovaServers.list_servers
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.list_servers | 0.588 | 0.656  | 0.754  | 0.774  | 0.795 | 0.663 | 100.0%  | 10    |
  | total             | 0.589 | 0.656  | 0.754  | 0.775  | 0.795 | 0.663 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.98694491386
  Full duration: 47.495290041

  test scenario NovaServers.resize_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.412  | 4.572  | 6.064  | 6.069  | 6.073  | 4.644  | 100.0%  | 10    |
  | nova.resize         | 21.205 | 34.251 | 42.136 | 42.238 | 42.34  | 31.684 | 100.0%  | 10    |
  | nova.resize_confirm | 2.364  | 2.437  | 2.588  | 2.638  | 2.688  | 2.479  | 100.0%  | 10    |
  | nova.delete_server  | 2.38   | 2.427  | 2.64   | 2.727  | 2.814  | 2.475  | 100.0%  | 10    |
  | total               | 29.399 | 43.496 | 53.296 | 53.299 | 53.302 | 41.282 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 112.265089989
  Full duration: 126.299309015

  test scenario NovaServers.boot_server_from_volume_and_delete
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.376  | 4.574  | 6.275  | 6.295  | 6.315  | 4.705  | 100.0%  | 10    |
  | nova.boot_server     | 8.443  | 9.25   | 11.22  | 11.494 | 11.768 | 9.658  | 100.0%  | 10    |
  | nova.delete_server   | 4.478  | 4.614  | 4.912  | 5.81   | 6.708  | 4.799  | 100.0%  | 10    |
  | total                | 16.358 | 19.136 | 21.665 | 22.113 | 22.56  | 19.163 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 56.0801298618
  Full duration: 85.6200530529

  test scenario NovaServers.boot_and_migrate_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.498  | 4.001  | 5.998  | 6.132  | 6.267  | 4.49   | 100.0%  | 10    |
  | nova.stop_server    | 4.649  | 13.73  | 15.606 | 15.699 | 15.791 | 11.515 | 100.0%  | 10    |
  | nova.migrate        | 15.233 | 21.214 | 29.778 | 29.939 | 30.099 | 22.004 | 100.0%  | 10    |
  | nova.resize_confirm | 2.366  | 2.398  | 2.559  | 2.699  | 2.838  | 2.451  | 100.0%  | 10    |
  | nova.delete_server  | 2.384  | 2.428  | 2.527  | 2.567  | 2.606  | 2.444  | 100.0%  | 10    |
  | total               | 35.813 | 43.101 | 49.38  | 49.998 | 50.616 | 42.904 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 121.644474983
  Full duration: 135.548355818

  test scenario NovaServers.boot_and_delete_server
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | nova.boot_server   | 3.484 | 6.119  | 7.588  | 7.617  | 7.647  | 5.778 | 100.0%  | 10    |
  | nova.delete_server | 2.393 | 2.758  | 4.763  | 4.817  | 4.872  | 3.438 | 100.0%  | 10    |
  | total              | 5.885 | 8.701  | 12.336 | 12.358 | 12.379 | 9.216 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 26.0077610016
  Full duration: 48.9747579098

  test scenario NovaServers.boot_and_rebuild_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.5    | 4.786  | 6.225  | 6.257  | 6.289  | 4.859  | 100.0%  | 10    |
  | nova.rebuild_server | 6.349  | 11.303 | 17.156 | 17.218 | 17.279 | 11.611 | 100.0%  | 10    |
  | nova.delete_server  | 2.381  | 2.441  | 2.549  | 2.55   | 2.552  | 2.464  | 100.0%  | 10    |
  | total               | 13.553 | 18.971 | 23.648 | 24.245 | 24.842 | 18.934 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 52.6579520702
  Full duration: 75.2351601124

  test scenario NovaSecGroup.create_and_list_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.386  | 2.017  | 2.077  | 2.091  | 2.106  | 1.84   | 100.0%  | 10    |
  | nova.create_100_rules          | 8.891  | 10.215 | 10.514 | 10.722 | 10.929 | 10.096 | 100.0%  | 10    |
  | nova.list_security_groups      | 0.107  | 0.152  | 0.269  | 0.288  | 0.307  | 0.171  | 100.0%  | 10    |
  | total                          | 10.858 | 12.348 | 12.575 | 12.61  | 12.645 | 12.108 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 35.6299619675
  Full duration: 63.5884320736

  test scenario NovaSecGroup.create_and_delete_secgroups
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +--------------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.387 | 1.712  | 2.11   | 2.114  | 2.118  | 1.782  | 100.0%  | 10    |
  | nova.create_100_rules          | 8.912 | 9.991  | 10.333 | 10.39  | 10.447 | 9.849  | 100.0%  | 10    |
  | nova.delete_10_security_groups | 0.735 | 0.953  | 1.042  | 1.101  | 1.161  | 0.955  | 100.0%  | 10    |
  | total                          | 11.2  | 12.869 | 13.019 | 13.049 | 13.079 | 12.586 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 37.0498371124
  Full duration: 51.703150034

  test scenario NovaServers.boot_and_bounce_server
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  | action                  | min    | median | 90%ile | 95%ile  | max     | avg    | success | count |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  | nova.boot_server        | 3.232  | 4.745  | 6.322  | 6.339   | 6.356   | 4.884  | 100.0%  | 10    |
  | nova.reboot_server      | 4.43   | 4.579  | 4.667  | 4.687   | 4.707   | 4.59   | 100.0%  | 10    |
  | nova.soft_reboot_server | 4.722  | 6.782  | 18.815 | 72.233  | 125.65  | 18.46  | 100.0%  | 10    |
  | nova.stop_server        | 4.631  | 4.711  | 6.14   | 10.834  | 15.527  | 5.852  | 100.0%  | 10    |
  | nova.start_server       | 2.625  | 2.712  | 3.141  | 3.595   | 4.048   | 2.891  | 100.0%  | 10    |
  | nova.rescue_server      | 6.624  | 11.131 | 17.578 | 17.69   | 17.803  | 11.544 | 100.0%  | 10    |
  | nova.unrescue_server    | 2.293  | 4.467  | 4.631  | 4.634   | 4.636   | 3.681  | 100.0%  | 10    |
  | nova.delete_server      | 2.346  | 2.407  | 2.563  | 2.572   | 2.581   | 2.442  | 100.0%  | 10    |
  | total                   | 35.909 | 44.054 | 60.343 | 108.964 | 157.584 | 54.354 | 100.0%  | 10    |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  Load duration: 157.603001118
  Full duration: 179.857326031

  test scenario NovaServers.boot_server
  +---------------------------------------------------------------------------------------+
  |                                 Response Times (sec)                                  |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server | 3.435 | 4.325  | 6.075  | 6.183  | 6.292 | 4.629 | 100.0%  | 10    |
  | total            | 3.435 | 4.325  | 6.075  | 6.183  | 6.292 | 4.629 | 100.0%  | 10    |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 13.5383079052
  Full duration: 36.4747169018

  test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
  +-----------------------------------------------------------------------------------------------------------+
  |                                           Response Times (sec)                                            |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups    | 1.622  | 1.87   | 1.968  | 2.066  | 2.163  | 1.846  | 100.0%  | 10    |
  | nova.create_100_rules             | 8.778  | 9.885  | 10.429 | 10.484 | 10.538 | 9.786  | 100.0%  | 10    |
  | nova.boot_server                  | 4.372  | 5.705  | 6.744  | 6.784  | 6.825  | 5.534  | 100.0%  | 10    |
  | nova.get_attached_security_groups | 0.145  | 0.15   | 0.163  | 0.171  | 0.179  | 0.154  | 100.0%  | 10    |
  | nova.delete_server                | 2.392  | 2.532  | 4.639  | 4.677  | 4.715  | 3.324  | 100.0%  | 10    |
  | nova.delete_10_security_groups    | 0.762  | 0.811  | 1.001  | 1.056  | 1.112  | 0.864  | 100.0%  | 10    |
  | total                             | 18.434 | 20.813 | 24.815 | 24.847 | 24.879 | 21.508 | 100.0%  | 10    |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 64.179831028
  Full duration: 87.2896039486

  test scenario NovaServers.pause_and_unpause_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 3.419  | 4.899  | 6.417  | 6.437  | 6.457  | 4.897  | 100.0%  | 10    |
  | nova.pause_server   | 2.319  | 2.452  | 2.541  | 2.574  | 2.607  | 2.443  | 100.0%  | 10    |
  | nova.unpause_server | 2.291  | 2.397  | 2.512  | 2.565  | 2.619  | 2.409  | 100.0%  | 10    |
  | nova.delete_server  | 2.36   | 2.542  | 3.024  | 3.769  | 4.514  | 2.719  | 100.0%  | 10    |
  | total               | 10.572 | 12.299 | 14.07  | 14.773 | 15.475 | 12.469 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 36.6686770916
  Full duration: 59.3664259911

  test scenario NovaServers.boot_server_from_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.258  | 3.501  | 5.924  | 5.949  | 5.974  | 4.155  | 100.0%  | 10    |
  | nova.boot_server     | 7.572  | 8.821  | 12.368 | 12.983 | 13.598 | 9.51   | 100.0%  | 10    |
  | total                | 11.135 | 12.15  | 18.14  | 18.856 | 19.572 | 13.665 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 38.717217207
  Full duration: 73.4654810429

  test scenario NovaServers.boot_and_list_server
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server  | 3.569 | 4.788  | 6.354  | 6.43   | 6.506 | 4.924 | 100.0%  | 10    |
  | nova.list_servers | 0.189 | 0.37   | 0.447  | 0.453  | 0.46  | 0.346 | 100.0%  | 10    |
  | total             | 3.757 | 5.231  | 6.727  | 6.745  | 6.763 | 5.27  | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.4698469639
  Full duration: 47.3727209568

  run_rally - INFO - Test scenario: "nova" OK.

  run_rally - INFO - Starting test scenario "quotas" ...
  run_rally - INFO -
   Preparing input task
   Task  9226e59f-9bfb-44aa-8641-99f492cd92a9: started
  Task 9226e59f-9bfb-44aa-8641-99f492cd92a9: finished

  test scenario Quotas.cinder_update
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +----------------------+-----+--------+--------+--------+-------+-------+---------+-------+
  | action               | min | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-----+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.6 | 0.64   | 0.688  | 0.721  | 0.754 | 0.649 | 100.0%  | 10    |
  | total                | 0.6 | 0.64   | 0.688  | 0.721  | 0.754 | 0.649 | 100.0%  | 10    |
  +----------------------+-----+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.92687010765
  Full duration: 7.31987595558

  test scenario Quotas.neutron_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.217 | 0.255  | 0.377  | 0.401  | 0.424 | 0.28  | 100.0%  | 10    |
  | total                | 0.28  | 0.325  | 0.445  | 0.469  | 0.492 | 0.346 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.03654098511
  Full duration: 6.59040594101

  test scenario Quotas.cinder_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.588 | 0.651  | 0.699  | 0.702  | 0.705 | 0.652 | 100.0%  | 10    |
  | quotas.delete_quotas | 0.389 | 0.434  | 0.5    | 0.527  | 0.554 | 0.449 | 100.0%  | 10    |
  | total                | 1.011 | 1.097  | 1.176  | 1.179  | 1.182 | 1.101 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.32944512367
  Full duration: 8.96466994286

  test scenario Quotas.nova_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.322 | 0.358  | 0.54   | 0.633  | 0.726 | 0.407 | 100.0%  | 10    |
  | quotas.delete_quotas | 0.016 | 0.022  | 0.028  | 0.029  | 0.03  | 0.022 | 100.0%  | 10    |
  | total                | 0.344 | 0.383  | 0.557  | 0.652  | 0.747 | 0.429 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.20111894608
  Full duration: 6.32782506943

  test scenario Quotas.nova_update
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +----------------------+------+--------+--------+--------+-------+------+---------+-------+
  | action               | min  | median | 90%ile | 95%ile | max   | avg  | success | count |
  +----------------------+------+--------+--------+--------+-------+------+---------+-------+
  | quotas.update_quotas | 0.32 | 0.373  | 0.485  | 0.499  | 0.513 | 0.39 | 100.0%  | 10    |
  | total                | 0.32 | 0.373  | 0.485  | 0.499  | 0.513 | 0.39 | 100.0%  | 10    |
  +----------------------+------+--------+--------+--------+-------+------+---------+-------+
  Load duration: 1.11949706078
  Full duration: 6.58456206322

  run_rally - INFO - Test scenario: "quotas" OK.

  run_rally - INFO - Starting test scenario "requests" ...
  run_rally - INFO -
   Preparing input task
   Task  2e77e5dd-e2ca-466a-9edb-4f5f741dd55b: started
  Task 2e77e5dd-e2ca-466a-9edb-4f5f741dd55b: finished

  test scenario HttpRequests.check_random_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 0.462 | 0.483  | 1.478  | 3.509  | 5.541 | 1.102 | 100.0%  | 10    |
  | total                  | 0.462 | 0.483  | 1.478  | 3.509  | 5.541 | 1.102 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 6.3974840641
  Full duration: 8.66475987434

  test scenario HttpRequests.check_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 0.453 | 0.458  | 0.477  | 0.494  | 0.511 | 0.465 | 100.0%  | 10    |
  | total                  | 0.453 | 0.458  | 0.477  | 0.494  | 0.512 | 0.465 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.39966082573
  Full duration: 3.74285912514

  run_rally - INFO - Test scenario: "requests" OK.

  run_rally - INFO -

                       Rally Summary Report
  +===================+============+===============+===========+
  | Module            | Duration   | nb. Test Run  | Success   |
  +===================+============+===============+===========+
  | authenticate      | 00:17      | 10            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | glance            | 01:24      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | cinder            | 16:34      | 50            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | heat              | 06:19      | 32            | 92.31%    |
  +-------------------+------------+---------------+-----------+
  | keystone          | 01:07      | 29            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | neutron           | 04:40      | 31            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | nova              | 24:26      | 61            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | quotas            | 00:35      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | requests          | 00:12      | 2             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  +===================+============+===============+===========+
  | TOTAL:            | 00:55:38   | 229           | 99.15%    |
  +===================+============+===============+===========+


SDN Controller
--------------

ONOS
^^^^
::

  FUNCTEST.info: Running ONOS test case...
  Cloning into '/home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest'...
  FUNCvirNetNB - INFO - Creating component Handle: ONOSrest

                                  +----------------+
  ------------------------------ { Script And Files }  ------------------------------
                                  +----------------+
  Script Log File : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNB_22_Feb_2016_16_47_23/FUNCvirNetNB_22_Feb_2016_16_47_23.log
  Report Log File : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNB_22_Feb_2016_16_47_23/FUNCvirNetNB_22_Feb_2016_16_47_23.rpt
  ONOSrest Session Log : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNB_22_Feb_2016_16_47_23/ONOSrest.session
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

  Network Post
   2.1: Generate Post Data
   2.2: Post Data via HTTP
   2.3: Get Data via HTTP
   2.4: Compare Send Id and Get Id

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase3
  ******************************

  Network Update
   3.1: Generate Post Data
   3.2: Post Data via HTTP
   3.3: Update Data via HTTP
   3.4: Get Data via HTTP
   3.5: Compare Update data.

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase4
  ******************************

  Network Delete
   4.1: Generate Post Data
   4.2: Post Data via HTTP
   4.3: Delete Data via HTTP
   4.4: Get Data is NULL

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase5
  ******************************

  Subnet Post
   5.1: Generate Post Data
   5.2: Post Network Data via HTTP(Post Subnet need post network)
   5.3: Post Subnet Data via HTTP
   5.4: Get Subnet Data via HTTP
   5.5: Compare Post Subnet Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase6
  ******************************

  Subnet Update
   6.1: Generate Post Data
   6.2: Post Network Data via HTTP(Post Subnet need post network)
   6.3: Post Subnet Data via HTTP
   6.4: Update Subnet Data via HTTP
   6.5: Get Subnet Data via HTTP
   6.6: Compare Subnet Data
   6.7: Delete Subnet via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase7
  ******************************

  Subnet Delete
   7.1: Generate Post Data
   7.2: Post Network Data via HTTP(Post Subnet need post network)
   7.3: Post Subnet Data via HTTP
   7.4: Delete Subnet Data via HTTP
   7.5: Get Subnet Data is NULL

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase8
  ******************************

  Port Post
   8.1: Generate Post Data
   8.2: Post Network Data via HTTP(Post port need post network)
   8.3: Post Subnet Data via HTTP(Post port need post subnet)
   8.4: Post Port Data via HTTP
   8.5: Get Port Data via HTTP
   8.6: Compare Post Port Data
   8.7: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase9
  ******************************

  Port Update
   9.1: Generate Post Data
   9.2: Post Network Data via HTTP(Post port need post network)
   9.3: Post Subnet Data via HTTP(Post port need post subnet)
   9.4: Post Port Data via HTTP
   9.5: Update Port Data via HTTP
   9.6: Get Port Data via HTTP
   9.7: Compare Update Port Data
   9.8: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase10
  ******************************

  Port Delete
   10.1: Generate Post Data
   10.2: Post Network Data via HTTP(Post port need post network)
   10.3: Post Subnet Data via HTTP(Post port need post subnet)
   10.4: Post Port Data via HTTP
   10.5: Delete Port Data via HTTP
   10.6: Get Port Data is NULL
   10.7: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  *************************************
  Test Execution Summary
  *************************************

   Test Start           : 22 Feb 2016 16:47:23
   Test End             : 22 Feb 2016 16:47:39
   Execution Time       : 0:00:15.597834
   Total tests planned  : 9
   Total tests RUN      : 9
   Total Pass           : 9
   Total Fail           : 0
   Total No Result      : 0
   Success Percentage   : 100%
   Execution Result     : 100%
  Disconnecting from ONOSrest: <drivers.common.api.controller.onosrestdriver.OnosRestDriver object at 0x7f848e052a50>
  FUNCvirNetNBL3 - INFO - Creating component Handle: ONOSrest

                                  +----------------+
  ------------------------------ { Script And Files }  ------------------------------
                                  +----------------+

  Script Log File : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNBL3_22_Feb_2016_16_47_39/FUNCvirNetNBL3_22_Feb_2016_16_47_39.log
  Report Log File : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNBL3_22_Feb_2016_16_47_39/FUNCvirNetNBL3_22_Feb_2016_16_47_39.rpt
  ONOSrest Session Log : /home/opnfv/repos/functest/testcases/Controllers/ONOS/Teston/CI/OnosSystemTest/TestON/logs/FUNCvirNetNBL3_22_Feb_2016_16_47_39/ONOSrest.session
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

  Router Post
   2.1: Post Network Data via HTTP(Post Router need post network)
   2.2: Post Router Data via HTTP
   2.3: Get Router Data via HTTP
   2.4: Compare Post Router Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase3
  ******************************

  Router Update
   3.1: Post Network Data via HTTP(Post Router need post network)
   3.2: Post Router Data via HTTP
   3.3: Update Router Data via HTTP
   3.4: Get Router Data via HTTP
   3.5: Compare Router Data
   3.6: Delete Router via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase4
  ******************************

  Router Delete
   4.1: Post Network Data via HTTP(Post Router need post network)
   4.2: Post Router Data via HTTP
   4.3: Delete Router Data via HTTP
   4.4: Get Router Data is NULL
  Verify the Router status

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase5
  ******************************

  RouterInterface Post
   5.1: Post Network Data via HTTP(Post port need post network)
   5.2: Post Subnet Data via HTTP(Post port need post subnet)
   5.3: Post Port Data via HTTP
   5.4: Post Router Data via HTTP
   5.5: Put RouterInterface Data via HTTP
   5.6: Get RouterInterface Data via HTTP
   5.7: Compare Post Port Data
   5.8: Del RouterInterface Data via HTTP
   5.9: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase6
  ******************************

  RouterInterface Delete
   6.1: Post Network Data via HTTP(Post port need post network)
   6.2: Post Subnet Data via HTTP(Post port need post subnet)
   6.3: Post Port Data via HTTP
   6.4: Post Router Data via HTTP
   6.5: Post RouterInterface Data via HTTP
   6.6: Del RouterInterface Data via HTTP
   6.7: Delete Port Data via HTTP
   6.8: Get Port Data is NULL
   6.9: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase7
  ******************************

  FloatingIp Post
   7.1: Post Network Data via HTTP(Post port need post network)
   7.2: Post Subnet Data via HTTP(Post port need post subnet)
   7.3: Post Port Data via HTTP
   7.4: Post Router Data via HTTP
   7.5: Get Port Data via HTTP
   7.6: Post FloatingIp Data via HTTP
   7.7: Get Port Data via HTTP
   7.8: Get FloatingIp Data via HTTP
   7.9: Get FloatingIp Data via HTTP
   7.10: Compare Post FloatingIp Data
   7.11: Post FloatingIp Clean Data via HTTP
   7.12: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase8
  ******************************

  FloatingIp Update
   8.1: Post Network Data via HTTP(Post port need post network)
   8.2: Post Subnet Data via HTTP(Post port need post subnet)
   8.3: Post Port Data via HTTP
   8.4: Post Router Data via HTTP
   8.5: Post FloatingIp Data via HTTP
   8.6: Post Delete Data via HTTP
   8.7: Post NewPort Data via HTTP
   8.8: Post NewFloatingIp Data via HTTP
   8.9: Get NewFloatingIp Data via HTTP
   8.10: Compare Post FloatingIp Data
   8.11: Post FloatingIp Clean Data via HTTP
   8.12: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase9
  ******************************

  FloatingIp Delete
   9.1: Post Network Data via HTTP(Post port need post network)
   9.2: Post Subnet Data via HTTP(Post port need post subnet)
   9.3: Post Port Data via HTTP
   9.4: Post Router Data via HTTP
   9.5: Post FloatingIp Data via HTTP
   9.6: Post FloatingIp Clean Data via HTTP
   9.7: Get FloatingIp Data is NULL
   9.8: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase10
  ******************************

  Gateway Post
   10.1: Post Network Data via HTTP(Post port need post network)
   10.2: Post Subnet Data via HTTP(Post port need post subnet)
   10.3: Post Port Data via HTTP
   10.4: Post Router Data via HTTP
   10.5: Get Gateway Data via HTTP
   10.6: Compare Post Gateway Data
   10.7: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase11
  ******************************

  Gateway Update
   11.1: Post Network Data via HTTP(Post port need post network)
   11.2: Post Subnet Data via HTTP(Post port need post subnet)
   11.3: Post Port Data via HTTP
   11.4: Post Router Data via HTTP
   11.5: Post New Router Data via HTTP
   11.6: Get Gateway Data via HTTP
   11.7: Compare Post Gateway Data
   11.8: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  ******************************
   Result summary for Testcase12
  ******************************

  Gateway Delete
   12.1: Post Network Data via HTTP(Post port need post network)
   12.2: Post Subnet Data via HTTP(Post port need post subnet)
   12.3: Post Port Data via HTTP
   12.4: Post Router Data via HTTP
   12.5: Post Del Gateway Data via HTTP
   12.6: Get Gateway Data via HTTP
   12.7: If Gateway Data is NULL
   12.8: Clean Data via HTTP

  *****************************
   Result: Pass
  *****************************

  *************************************
  Test Execution Summary
  *************************************

   Test Start           : 22 Feb 2016 16:47:39
   Test End             : 22 Feb 2016 16:47:59
   Execution Time       : 0:00:20.564415
   Total tests planned  : 11
   Total tests RUN      : 11
   Total Pass           : 11
   Total Fail           : 0
   Total No Result      : 0
   Success Percentage   : 100%
   Execution Result     : 100%
  Disconnecting from ONOSrest: <drivers.common.api.controller.onosrestdriver.OnosRestDriver object at 0x7fcc82fc7ad0>
