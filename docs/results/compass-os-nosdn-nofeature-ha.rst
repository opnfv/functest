.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for compass-os-nosdn-nofeature-ha
=======================================================

.. Add any text in here that could be useful for a reader.

The following section outlines the detailed functest results for the Brahmaputra scenario
deploying OpenStack in a Pharos environment by the Compass installer.

VIM
---

vPing_SSH
^^^^^^^^^

::
  FUNCTEST.info: Running vPing test...
  2016-01-23 03:18:20,153 - vPing- INFO - Creating neutron network vping-net...
  2016-01-23 03:18:35,476 - vPing- INFO - Flavor found 'm1.small'
  2016-01-23 03:18:36,350 - vPing- INFO - vPing Start Time:'2016-01-23 03:18:36'
  2016-01-23 03:18:38,571 - vPing- INFO - Creating instance 'opnfv-vping-1' with IP 192.168.130.30...
  2016-01-23 03:18:53,716 - vPing- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  2016-01-23 03:18:55,239 - vPing- INFO - Creating instance 'opnfv-vping-2' with IP 192.168.130.40...
  2016-01-23 03:19:15,593 - vPing- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  2016-01-23 03:19:15,593 - vPing- INFO - Creating floating IP for the second VM...
  2016-01-23 03:19:18,017 - vPing- INFO - Floating IP created: '10.2.65.6'
  2016-01-23 03:19:18,017 - vPing- INFO - Associating floating ip: '10.2.65.6' to VM2
  2016-01-23 03:19:37,839 - vPing- INFO - SCP ping script to VM2...
  2016-01-23 03:19:37,839 - vPing- INFO - Waiting for ping...
  2016-01-23 03:19:40,130 - vPing- INFO - vPing detected!
  2016-01-23 03:19:40,130 - vPing- INFO - vPing duration:'63.8'
  2016-01-23 03:19:40,130 - vPing- INFO - Cleaning up...
  2016-01-23 03:20:06,574 - vPing- INFO - Deleting network 'vping-net'...
  2016-01-23 03:20:13,587 - vPing- INFO - vPing OK
::



vPing_userdata
^^^^^^^^^^^^^^
::
    2016-01-06 16:06:20,550 - vPing- INFO - Creating neutron network vping-net...
    2016-01-06 16:06:23,867 - vPing- INFO - Flavor found 'm1.small'
    2016-01-06 16:06:24,457 - vPing- INFO - vPing Start Time:'2016-01-06 16:06:24'
    2016-01-06 16:06:24,626 - vPing- INFO - Creating instance 'opnfv-vping-1' with IP 192.168.130.30...
    2016-01-06 16:06:39,351 - vPing- INFO - Instance 'opnfv-vping-1' is ACTIVE.
    2016-01-06 16:06:39,650 - vPing- INFO - Creating instance 'opnfv-vping-2' with IP 192.168.130.40...
    2016-01-06 16:06:53,330 - vPing- INFO - Instance 'opnfv-vping-2' is ACTIVE.
    2016-01-06 16:06:53,330 - vPing- INFO - Waiting for ping...
    2016-01-06 16:06:58,669 - vPing- INFO - vPing detected!
    2016-01-06 16:06:58,669 - vPing- INFO - vPing duration:'34.2'
    2016-01-06 16:06:58,670 - vPing- INFO - Cleaning up...
    2016-01-06 16:07:12,661 - vPing- INFO - Deleting network 'vping-net'...
    2016-01-06 16:07:14,748 - vPing- INFO - vPing OK
::

Tempest
^^^^^^^
::

  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | name                                                                                                                                     | time      | status  |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.11781   | success |
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.05430   | success |
  | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 20.72631  | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 7.73912   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 7.47082   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.06171   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.05417   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.07193   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.12763   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.11964   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.08112   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.06481   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.08369   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.05765   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.12868   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.07230   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.16652   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.06731   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 0.24466   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 0.05089   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.09075   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 0.52102   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 0.58238   | success |
  | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 1.17341   | success |
  | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 16.90411  | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 3.14876   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.07525   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.17151   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 0.30083   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.00066   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 3.18218   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.06488   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.16982   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 0.30444   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.00067   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.08270   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 2.73820   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.19029   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.27854   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.16463   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.19733   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.16045   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.07527   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.05853   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.07255   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.05323   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.06890   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.18956   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00085   | skip    |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.12169   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.05169   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.01235   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.06910   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.06535   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.01176   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.01149   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.02745   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.05178   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.05124   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.20630   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.01319   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.06254   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.00070   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 4.72621   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 7.89477   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 12.23475  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.34511   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 18.65911  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 14.34968  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 23.18098  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 6.83678   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.05339   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.14447   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.43219   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.28758   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.31953   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.51589   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.52237   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.52855   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 2.37952   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 27.66900  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 26.43174  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 13.46497  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 11.34705  | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 0.59680   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 1.63905   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 0.63308   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 1.06122   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 0.57986   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 1.32645   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 0.56305   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 0.51822   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 0.43277   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.42442   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 1.37911   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 0.45828   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 0.37247   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 0.50085   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.32349   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 0.59661   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.41010   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 0.38688   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 0.34123   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 0.44430   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 0.57666   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.09876   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.01270   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 0.08179   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.01249   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 0.50856   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.06014   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.13249   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.05539   | success |
  | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 40.15264  | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.53502   | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.07374   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.12760   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.01065   | success |
  | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.16129   | success |
  | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.07225   | success |
  | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.13999   | success |
  | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.04030   | success |
  | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 0.26792   | success |
  | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.21608   | success |
  | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 0.89698   | success |
  | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.14521   | success |
  | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.08784   | success |
  | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.16453   | success |
  | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.15886   | success |
  | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 0.82495   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.03055   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.01697   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.01605   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.02072   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.01769   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.02375   | success |
  | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.07780   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 0.47641   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 0.41564   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 0.58103   | success |
  | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 0.61292   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 0.94290   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 1.26214   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 0.56268   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 1.03444   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 3.64415   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 0.61620   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 1.53122   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 1.16908   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 0.92732   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.11643   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.15497   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.07420   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.07296   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.07818   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 0.97980   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.12274   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.04495   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.06903   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.03206   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.03540   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 1.02047   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 1.08551   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 0.62181   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.07352   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.04485   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 1.07412   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 1.33841   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 0.74686   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.06553   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.05371   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 3.78970   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 1.74745   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 1.75165   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 1.13418   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 3.18918   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 1.30202   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 1.30648   | success |
  | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 0.84797   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 0.40040   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 0.61899   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.02067   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 0.58062   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 0.58547   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.02261   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.38658   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 4.95623   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.02169   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 0.92296   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.42568   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.33744   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.73197   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.35260   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.40455   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 2.42636   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.02149   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 0.68013   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 1.76115   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 2.40038   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 1.76992   | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 11.65383  | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 11.11969  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 12.30336  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 10.28020  | success |
  | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.16159   | success |
  | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.04956   | success |
  | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 36.69814  | success |
  | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 24.22887  | success |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 114.63134 | success |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 115.57809 | success |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  2016-02-11 10:25:15,246 - run_tempest - DEBUG - Executing command : rally verify list
  2016-02-11 10:25:15,807 - run_tempest - INFO - Results: {'timestart': '2016-02-1110:21:57.213292', 'duration': 197, 'tests': 210, 'failures': 0}
::


vIMS
^^^^

::
  FUNCTEST.info: Running vIMS test...
  2016-02-11 10:25:18,996 - vIMS - INFO - Prepare OpenStack plateform (create tenant and user)
  2016-02-11 10:25:19,218 - vIMS - INFO - Update OpenStack creds informations
  2016-02-11 10:25:19,218 - vIMS - INFO - Upload some OS images if it doesn't exist
  2016-02-11 10:25:19,344 - vIMS - INFO - centos_7 image doesn't exist on glance repository.
                              Try downloading this image and upload on glance !
  2016-02-11 10:28:59,907 - vIMS - INFO - ubuntu_14.04 image doesn't exist on glance repository.
                              Try downloading this image and upload on glance !
  2016-02-11 10:30:06,923 - vIMS - INFO - Update security group quota for this tenant
  2016-02-11 10:30:07,129 - vIMS - INFO - Update cinder quota for this tenant
  2016-02-11 10:30:07,570 - vIMS - INFO - Collect flavor id for cloudify manager server
  2016-02-11 10:30:08,036 - vIMS - INFO - Prepare virtualenv for cloudify-cli
  2016-02-11 10:30:41,255 - vIMS - INFO - Downloading the cloudify manager server blueprint
  2016-02-11 10:30:48,023 - vIMS - INFO - Cloudify deployment Start Time:'2016-02-11 10:30:48'
  2016-02-11 10:30:48,023 - vIMS - INFO - Writing the inputs file
  2016-02-11 10:30:48,027 - vIMS - INFO - Launching the cloudify-manager deployment
  2016-02-11 10:38:00,816 - vIMS - INFO - Cloudify-manager server is UP !
  2016-02-11 10:38:00,816 - vIMS - INFO - Cloudify deployment duration:'432.8'
  2016-02-11 10:38:00,816 - vIMS - INFO - Collect flavor id for all clearwater vm
  2016-02-11 10:38:01,343 - vIMS - INFO - vIMS VNF deployment Start Time:'2016-02-11 10:38:01'
  2016-02-11 10:38:01,343 - vIMS - INFO - Downloading the openstack-blueprint.yaml blueprint
  2016-02-11 10:38:05,941 - vIMS - INFO - Writing the inputs file
  2016-02-11 10:38:05,943 - vIMS - INFO - Launching the clearwater deployment
  2016-02-11 10:52:45,102 - vIMS - INFO - The deployment of clearwater-opnfv is ended
  2016-02-11 10:52:45,103 - vIMS - INFO - vIMS VNF deployment duration:'883.8'
  2016-02-11 10:55:52,908 - vIMS - INFO - vIMS functional test Start Time:'2016-02-11 10:55:52'
  2016-02-11 10:55:56,220 - vIMS - INFO - vIMS functional test duration:'3.3'
  2016-02-11 10:55:57,497 - vIMS - INFO - Launching the clearwater-opnfv undeployment
  2016-02-11 10:59:30,524 - vIMS - ERROR - Error when executing command /bin/bash -c 'source /home/opnfv/functest/data/vIMS/venv_cloudify/bin/activate; cd /home/opnfv/functest/data/vIMS/; cfy executions start -w uninstall -d clearwater-opnfv --timeout 1800 ; cfy deployments delete -d clearwater-opnfv; '
  2016-02-11 10:59:30,524 - vIMS - INFO - Launching the cloudify-manager undeployment
  2016-02-11 11:00:19,064 - vIMS - INFO - Cloudify-manager server has been successfully removed!
  2016-02-11 11:00:19,138 - vIMS - INFO - Removing vIMS tenant ..
  2016-02-11 11:00:19,977 - vIMS - INFO - Removing vIMS user ..
::

Rally
^^^^^

::
  2016-02-11 11:00:23,629 - run_rally - INFO - Starting test scenario "authenticate" ...
  2016-02-11 11:00:23,629 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-authenticate.yaml
  2016-02-11 11:00:23,889 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '48071712-5859-4fe7-a4fa-f723725ef015', 'service_list': ['authenticate'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-11 11:00:51,272 - run_rally - INFO - 
   Preparing input task
   Task  51e851b7-32dc-460a-ab4b-addf21394bd2: started
  Task 51e851b7-32dc-460a-ab4b-addf21394bd2: finished
  
  test scenario Authenticate.validate_glance
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_glance     | 0.118 | 0.151  | 0.203  | 0.242  | 0.282 | 0.165 | 100.0%  | 10    |
  | authenticate.validate_glance (2) | 0.036 | 0.039  | 0.105  | 0.105  | 0.106 | 0.052 | 100.0%  | 10    |
  | total                            | 0.224 | 0.275  | 0.392  | 0.401  | 0.41  | 0.298 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.870975017548
  Full duration: 3.27026605606
  
  
  
  test scenario Authenticate.keystone
  +-----------------------------------------------------------------------------+
  |                            Response Times (sec)                             |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | total  | 0.065 | 0.074  | 0.096  | 0.11   | 0.125 | 0.079 | 100.0%  | 10    |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.288023948669
  Full duration: 2.66391801834
  
  
  
  test scenario Authenticate.validate_heat
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_heat     | 0.103 | 0.205  | 0.24   | 0.287  | 0.334 | 0.189 | 100.0%  | 10    |
  | authenticate.validate_heat (2) | 0.025 | 0.071  | 0.075  | 0.083  | 0.092 | 0.056 | 100.0%  | 10    |
  | total                          | 0.194 | 0.327  | 0.402  | 0.437  | 0.471 | 0.325 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.899745941162
  Full duration: 3.1050620079
  
  
  
  test scenario Authenticate.validate_nova
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_nova     | 0.109 | 0.122  | 0.147  | 0.148  | 0.149 | 0.126 | 100.0%  | 10    |
  | authenticate.validate_nova (2) | 0.025 | 0.035  | 0.042  | 0.047  | 0.052 | 0.034 | 100.0%  | 10    |
  | total                          | 0.204 | 0.234  | 0.256  | 0.258  | 0.259 | 0.234 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.704580068588
  Full duration: 2.78002095222
  
  
  
  test scenario Authenticate.validate_cinder
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_cinder     | 0.096 | 0.114  | 0.162  | 0.276  | 0.389 | 0.142 | 100.0%  | 10    |
  | authenticate.validate_cinder (2) | 0.014 | 0.062  | 0.092  | 0.092  | 0.092 | 0.061 | 100.0%  | 10    |
  | total                            | 0.18  | 0.259  | 0.349  | 0.43   | 0.511 | 0.287 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.08016705513
  Full duration: 3.2588429451
  
  
  
  test scenario Authenticate.validate_neutron
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_neutron     | 0.107 | 0.139  | 0.187  | 0.195  | 0.203 | 0.145 | 100.0%  | 10    |
  | authenticate.validate_neutron (2) | 0.029 | 0.088  | 0.18   | 0.197  | 0.214 | 0.102 | 100.0%  | 10    |
  | total                             | 0.211 | 0.293  | 0.429  | 0.431  | 0.433 | 0.317 | 100.0%  | 10    |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.8887758255
  Full duration: 3.18487811089
  
  
  
  2016-02-11 11:00:51,273 - run_rally - DEBUG - task_id : 51e851b7-32dc-460a-ab4b-addf21394bd2
  2016-02-11 11:00:51,273 - run_rally - DEBUG - running command line : rally task report 51e851b7-32dc-460a-ab4b-addf21394bd2 --out /home/opnfv/functest/results/rally/opnfv-authenticate.html
  2016-02-11 11:00:51,924 - run_rally - DEBUG - running command line : rally task results 51e851b7-32dc-460a-ab4b-addf21394bd2
  2016-02-11 11:00:52,503 - run_rally - DEBUG - saving json file
  2016-02-11 11:00:52,505 - run_rally - DEBUG - Push result into DB
  2016-02-11 11:01:00,545 - run_rally - DEBUG - <Response [200]>
  2016-02-11 11:01:00,547 - run_rally - INFO - Test scenario: "authenticate" OK.
  
  2016-02-11 11:01:00,547 - run_rally - INFO - Starting test scenario "glance" ...
  2016-02-11 11:01:00,547 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-glance.yaml
  2016-02-11 11:01:00,715 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '48071712-5859-4fe7-a4fa-f723725ef015', 'service_list': ['glance'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-11 11:03:02,339 - run_rally - INFO - 
   Preparing input task
   Task  0514c645-e775-4ebf-ba6c-a85b35bcf330: started
  Task 0514c645-e775-4ebf-ba6c-a85b35bcf330: finished
  
  test scenario GlanceImages.list_images
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.list_images | 0.196 | 0.235  | 0.255  | 0.262  | 0.268 | 0.234 | 100.0%  | 10    |
  | total              | 0.196 | 0.235  | 0.255  | 0.262  | 0.268 | 0.235 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.73396396637
  Full duration: 3.6917579174
  
  
  
  test scenario GlanceImages.create_image_and_boot_instances
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | glance.create_image | 2.83   | 3.083  | 3.329  | 3.348  | 3.366  | 3.081  | 100.0%  | 10    |
  | nova.boot_servers   | 13.805 | 15.845 | 17.99  | 18.001 | 18.011 | 16.006 | 100.0%  | 10    |
  | total               | 16.635 | 18.928 | 20.956 | 21.082 | 21.207 | 19.086 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 56.1656239033
  Full duration: 83.2321109772
  
  
  
  test scenario GlanceImages.create_and_list_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 2.786 | 3.337  | 3.427  | 3.431  | 3.434 | 3.199 | 100.0%  | 10    |
  | glance.list_images  | 0.04  | 0.044  | 0.054  | 0.055  | 0.056 | 0.047 | 100.0%  | 10    |
  | total               | 2.829 | 3.381  | 3.475  | 3.483  | 3.49  | 3.245 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.66495990753
  Full duration: 14.2776150703
  
  
  
  test scenario GlanceImages.create_and_delete_image
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +---------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 2.92 | 3.441  | 3.706  | 3.729  | 3.752 | 3.383 | 100.0%  | 10    |
  | glance.delete_image | 0.13 | 0.146  | 0.164  | 0.166  | 0.169 | 0.148 | 100.0%  | 10    |
  | total               | 3.05 | 3.594  | 3.857  | 3.876  | 3.896 | 3.531 | 100.0%  | 10    |
  +---------------------+------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 10.3788890839
  Full duration: 13.5018799305
  
  
  
  2016-02-11 11:03:02,340 - run_rally - DEBUG - task_id : 0514c645-e775-4ebf-ba6c-a85b35bcf330
  2016-02-11 11:03:02,340 - run_rally - DEBUG - running command line : rally task report 0514c645-e775-4ebf-ba6c-a85b35bcf330 --out /home/opnfv/functest/results/rally/opnfv-glance.html
  2016-02-11 11:03:02,938 - run_rally - DEBUG - running command line : rally task results 0514c645-e775-4ebf-ba6c-a85b35bcf330
  2016-02-11 11:03:03,512 - run_rally - DEBUG - saving json file
  2016-02-11 11:03:03,514 - run_rally - DEBUG - Push result into DB
  2016-02-11 11:03:09,392 - run_rally - DEBUG - <Response [200]>
  2016-02-11 11:03:09,393 - run_rally - INFO - Test scenario: "glance" OK.
  
  2016-02-11 11:03:09,393 - run_rally - INFO - Starting test scenario "cinder" ...
  2016-02-11 11:03:09,393 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-cinder.yaml
  2016-02-11 11:03:09,567 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '48071712-5859-4fe7-a4fa-f723725ef015', 'service_list': ['cinder'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-11 11:21:00,829 - run_rally - INFO - 
   Preparing input task
   Task  900b8dcf-c285-4dd6-9d7f-d96dd70c867e: started
  Task 900b8dcf-c285-4dd6-9d7f-d96dd70c867e: finished
  
  test scenario CinderVolumes.create_and_attach_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server     | 7.877  | 10.22  | 13.83  | 13.833 | 13.836 | 10.894 | 100.0%  | 10    |
  | cinder.create_volume | 2.675  | 2.783  | 2.827  | 2.9    | 2.972  | 2.784  | 100.0%  | 10    |
  | nova.attach_volume   | 5.466  | 7.767  | 10.611 | 11.433 | 12.255 | 8.25   | 100.0%  | 10    |
  | nova.detach_volume   | 2.954  | 5.454  | 5.549  | 5.586  | 5.623  | 4.958  | 100.0%  | 10    |
  | cinder.delete_volume | 2.361  | 2.54   | 2.593  | 2.617  | 2.641  | 2.518  | 100.0%  | 10    |
  | nova.delete_server   | 2.371  | 2.492  | 2.754  | 3.676  | 4.598  | 2.677  | 100.0%  | 10    |
  | total                | 27.829 | 30.867 | 37.529 | 38.253 | 38.977 | 32.081 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 94.6691319942
  Full duration: 108.104104996
  
  
  
  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 5.195 | 5.367  | 5.487  | 5.504  | 5.521 | 5.344 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.046 | 0.119  | 0.125  | 0.125  | 0.125 | 0.104 | 100.0%  | 10    |
  | total                | 5.268 | 5.446  | 5.605  | 5.618  | 5.631 | 5.448 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.2577528954
  Full duration: 27.6948328018
  
  
  
  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.845 | 2.977  | 3.126  | 3.127  | 3.127 | 2.981 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.073 | 0.128  | 0.18   | 0.192  | 0.205 | 0.133 | 100.0%  | 10    |
  | total                | 2.918 | 3.113  | 3.254  | 3.255  | 3.256 | 3.115 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.32777905464
  Full duration: 20.7225239277
  
  
  
  test scenario CinderVolumes.create_and_list_snapshots
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.45  | 2.516  | 2.591  | 2.608  | 2.624 | 2.522 | 100.0%  | 10    |
  | cinder.list_snapshots  | 0.017 | 0.08   | 0.115  | 0.149  | 0.182 | 0.075 | 100.0%  | 10    |
  | total                  | 2.528 | 2.564  | 2.677  | 2.688  | 2.699 | 2.597 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 7.81214690208
  Full duration: 31.1933379173
  
  
  
  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.869 | 2.971  | 3.052  | 3.056  | 3.061 | 2.972 | 100.0%  | 10    |
  | cinder.delete_volume | 2.403 | 2.545  | 2.605  | 2.653  | 2.702 | 2.537 | 100.0%  | 10    |
  | total                | 5.272 | 5.51   | 5.62   | 5.691  | 5.763 | 5.509 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.4689249992
  Full duration: 22.9906311035
  
  
  
  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 3.071 | 5.365  | 5.482  | 5.5    | 5.518 | 4.949 | 100.0%  | 10    |
  | cinder.delete_volume | 2.387 | 2.528  | 2.639  | 2.701  | 2.762 | 2.546 | 100.0%  | 10    |
  | total                | 5.548 | 7.938  | 8.039  | 8.16   | 8.28  | 7.494 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 21.4687700272
  Full duration: 28.3897769451
  
  
  
  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.821 | 2.884  | 3.014  | 3.043  | 3.072 | 2.914 | 100.0%  | 10    |
  | cinder.delete_volume | 2.471 | 2.524  | 2.652  | 2.662  | 2.672 | 2.544 | 100.0%  | 10    |
  | total                | 5.329 | 5.417  | 5.63   | 5.655  | 5.68  | 5.458 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.3380551338
  Full duration: 22.9960508347
  
  
  
  test scenario CinderVolumes.create_and_upload_volume_to_image
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume          | 2.796  | 3.072  | 3.296  | 3.303  | 3.31   | 3.08   | 100.0%  | 10    |
  | cinder.upload_volume_to_image | 23.924 | 63.042 | 67.082 | 67.666 | 68.25  | 53.998 | 100.0%  | 10    |
  | cinder.delete_volume          | 2.36   | 2.557  | 2.856  | 2.869  | 2.883  | 2.604  | 100.0%  | 10    |
  | nova.delete_image             | 0.293  | 0.5    | 0.705  | 0.733  | 0.761  | 0.518  | 100.0%  | 10    |
  | total                         | 29.698 | 69.114 | 73.363 | 73.938 | 74.513 | 60.201 | 100.0%  | 10    |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 171.225147963
  Full duration: 178.588042974
  
  
  
  test scenario CinderVolumes.create_and_delete_snapshot
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.451 | 2.535  | 2.599  | 2.601  | 2.603 | 2.537 | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.314 | 2.372  | 2.428  | 2.44   | 2.451 | 2.377 | 100.0%  | 10    |
  | total                  | 4.841 | 4.918  | 4.955  | 4.965  | 4.975 | 4.914 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.7416520119
  Full duration: 33.7979490757
  
  
  
  test scenario CinderVolumes.create_volume
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.77 | 2.934  | 3.191  | 3.206  | 3.221 | 2.975 | 100.0%  | 10    |
  | total                | 2.77 | 2.934  | 3.191  | 3.206  | 3.221 | 2.975 | 100.0%  | 10    |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 8.76418590546
  Full duration: 18.1201279163
  
  
  
  test scenario CinderVolumes.create_volume
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.91 | 2.969  | 3.153  | 3.156  | 3.159 | 3.016 | 100.0%  | 10    |
  | total                | 2.91 | 2.969  | 3.153  | 3.156  | 3.159 | 3.016 | 100.0%  | 10    |
  +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.04045200348
  Full duration: 20.918489933
  
  
  
  test scenario CinderVolumes.list_volumes
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.list_volumes | 0.221 | 0.28   | 0.353  | 0.367  | 0.381 | 0.286 | 100.0%  | 10    |
  | total               | 0.221 | 0.281  | 0.353  | 0.367  | 0.381 | 0.286 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.899931907654
  Full duration: 47.394310236
  
  
  
  test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.849  | 2.979  | 3.13   | 3.135  | 3.139  | 2.983  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.246  | 2.347  | 2.423  | 2.441  | 2.458  | 2.347  | 100.0%  | 10    |
  | nova.attach_volume     | 7.593  | 7.735  | 10.768 | 11.83  | 12.893 | 8.754  | 100.0%  | 10    |
  | nova.detach_volume     | 3.049  | 5.246  | 5.363  | 5.401  | 5.438  | 4.664  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.236  | 2.337  | 2.436  | 2.462  | 2.488  | 2.338  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.416  | 2.472  | 2.668  | 2.703  | 2.738  | 2.516  | 100.0%  | 10    |
  | total                  | 21.452 | 23.5   | 26.208 | 26.342 | 26.477 | 23.913 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 70.1711850166
  Full duration: 127.766703844
  
  
  
  test scenario CinderVolumes.create_from_volume_and_delete_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 9.84   | 12.345 | 17.242 | 18.095 | 18.947 | 12.953 | 100.0%  | 10    |
  | cinder.delete_volume | 2.423  | 2.524  | 2.651  | 2.652  | 2.654  | 2.549  | 100.0%  | 10    |
  | total                | 12.325 | 14.802 | 19.864 | 20.732 | 21.601 | 15.502 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 44.2985730171
  Full duration: 63.4050178528
  
  
  
  test scenario CinderVolumes.create_and_extend_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.84  | 3.007  | 3.169  | 3.186  | 3.202 | 3.003 | 100.0%  | 10    |
  | cinder.extend_volume | 2.635 | 2.766  | 2.82   | 2.863  | 2.906 | 2.763 | 100.0%  | 10    |
  | cinder.delete_volume | 2.474 | 2.557  | 2.653  | 2.657  | 2.662 | 2.564 | 100.0%  | 10    |
  | total                | 8.102 | 8.255  | 8.582  | 8.618  | 8.653 | 8.331 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.934566021
  Full duration: 31.7552449703
  
  
  
  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.821  | 3.019  | 3.15   | 3.15   | 3.15   | 3.003  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.329  | 2.347  | 2.544  | 2.556  | 2.567  | 2.403  | 100.0%  | 10    |
  | nova.attach_volume     | 7.641  | 7.945  | 10.466 | 11.342 | 12.217 | 8.745  | 100.0%  | 10    |
  | nova.detach_volume     | 2.921  | 5.276  | 5.456  | 5.489  | 5.521  | 4.447  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.204  | 2.355  | 2.461  | 2.481  | 2.501  | 2.357  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.349  | 2.484  | 2.582  | 2.585  | 2.588  | 2.481  | 100.0%  | 10    |
  | total                  | 21.463 | 23.779 | 25.971 | 26.099 | 26.226 | 23.747 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 69.164083004
  Full duration: 130.257413864
  
  
  
  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.685  | 2.835  | 2.952  | 2.962  | 2.972  | 2.841  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.27   | 2.377  | 2.426  | 2.447  | 2.468  | 2.375  | 100.0%  | 10    |
  | nova.attach_volume     | 7.587  | 7.788  | 10.602 | 11.506 | 12.41  | 8.705  | 100.0%  | 10    |
  | nova.detach_volume     | 3.085  | 5.289  | 5.584  | 5.605  | 5.626  | 5.124  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.186  | 2.317  | 2.392  | 2.42   | 2.448  | 2.307  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.389  | 2.514  | 2.56   | 2.591  | 2.622  | 2.499  | 100.0%  | 10    |
  | total                  | 23.286 | 23.66  | 26.371 | 26.512 | 26.653 | 24.395 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 73.7153699398
  Full duration: 137.208030939
  
  
  
  2016-02-11 11:21:00,829 - run_rally - DEBUG - task_id : 900b8dcf-c285-4dd6-9d7f-d96dd70c867e
  2016-02-11 11:21:00,829 - run_rally - DEBUG - running command line : rally task report 900b8dcf-c285-4dd6-9d7f-d96dd70c867e --out /home/opnfv/functest/results/rally/opnfv-cinder.html
  2016-02-11 11:21:01,545 - run_rally - DEBUG - running command line : rally task results 900b8dcf-c285-4dd6-9d7f-d96dd70c867e
  2016-02-11 11:21:02,138 - run_rally - DEBUG - saving json file
  2016-02-11 11:21:02,143 - run_rally - DEBUG - Push result into DB
  2016-02-11 11:21:08,903 - run_rally - DEBUG - <Response [200]>
  2016-02-11 11:21:08,906 - run_rally - INFO - Test scenario: "cinder" OK.
  
  2016-02-11 11:21:08,906 - run_rally - INFO - Starting test scenario "heat" ...
  2016-02-11 11:21:08,906 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-heat.yaml
  2016-02-11 11:21:09,103 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '48071712-5859-4fe7-a4fa-f723725ef015', 'service_list': ['heat'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-11 11:28:20,183 - run_rally - INFO - 
   Preparing input task
   Task  387dedc1-62f1-4d72-8a34-bbf4940fd1ac: started
  Task 387dedc1-62f1-4d72-8a34-bbf4940fd1ac: finished
  
  test scenario HeatStacks.create_suspend_resume_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack  | 2.833 | 3.112  | 3.347  | 3.348  | 3.348 | 3.116 | 100.0%  | 10    |
  | heat.suspend_stack | 0.511 | 1.079  | 1.65   | 1.654  | 1.659 | 1.091 | 100.0%  | 10    |
  | heat.resume_stack  | 0.654 | 1.609  | 1.801  | 1.878  | 1.955 | 1.55  | 100.0%  | 10    |
  | heat.delete_stack  | 0.649 | 1.481  | 1.581  | 1.591  | 1.601 | 1.413 | 100.0%  | 10    |
  | total              | 6.075 | 6.967  | 8.284  | 8.335  | 8.386 | 7.171 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 21.5846898556
  Full duration: 24.9157381058
  
  
  
  test scenario HeatStacks.create_and_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.902 | 3.071  | 3.242  | 3.358  | 3.474 | 3.103 | 100.0%  | 10    |
  | heat.delete_stack | 0.403 | 0.514  | 1.517  | 1.597  | 1.677 | 0.885 | 100.0%  | 10    |
  | total             | 3.356 | 3.755  | 4.685  | 4.777  | 4.868 | 3.988 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 11.9179480076
  Full duration: 15.2915010452
  
  
  
  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 15.2   | 17.516 | 18.839 | 19.237 | 19.635 | 17.508 | 100.0%  | 10    |
  | heat.delete_stack | 8.058  | 8.27   | 8.864  | 8.902  | 8.94   | 8.364  | 100.0%  | 10    |
  | total             | 23.482 | 26.115 | 27.568 | 27.731 | 27.893 | 25.872 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 76.6700150967
  Full duration: 80.0998740196
  
  
  
  test scenario HeatStacks.create_and_delete_stack
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 18.63 | 19.909 | 21.859 | 22.311 | 22.764 | 20.261 | 100.0%  | 10    |
  | heat.delete_stack | 8.058 | 9.259  | 10.244 | 10.762 | 11.279 | 9.38   | 100.0%  | 10    |
  | total             | 28.08 | 29.419 | 31.27  | 31.715 | 32.16  | 29.641 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 87.3162331581
  Full duration: 90.7692539692
  
  
  
  test scenario HeatStacks.list_stacks_and_resources
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.list_stacks                | 0.224 | 0.28   | 0.316  | 0.37   | 0.424 | 0.286 | 100.0%  | 10    |
  | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0   | 0.0   | 100.0%  | 10    |
  | total                           | 0.225 | 0.28   | 0.316  | 0.37   | 0.424 | 0.286 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.828476190567
  Full duration: 3.95608401299
  
  
  
  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.833 | 3.13   | 3.304  | 3.312  | 3.32  | 3.114 | 100.0%  | 10    |
  | heat.update_stack | 2.494 | 3.64   | 3.805  | 3.878  | 3.951 | 3.416 | 100.0%  | 10    |
  | heat.delete_stack | 1.311 | 1.52   | 1.726  | 1.738  | 1.751 | 1.515 | 100.0%  | 10    |
  | total             | 7.252 | 8.141  | 8.657  | 8.676  | 8.695 | 8.044 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.2576129436
  Full duration: 27.9351220131
  
  
  
  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 3.013 | 3.158  | 3.272  | 3.273  | 3.273 | 3.149 | 100.0%  | 10    |
  | heat.update_stack | 2.434 | 2.585  | 2.841  | 3.284  | 3.728 | 2.701 | 100.0%  | 10    |
  | heat.delete_stack | 0.419 | 1.501  | 1.666  | 1.7    | 1.734 | 1.252 | 100.0%  | 10    |
  | total             | 6.07  | 7.268  | 7.688  | 8.031  | 8.374 | 7.102 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 21.1723821163
  Full duration: 24.7491641045
  
  
  
  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | heat.create_stack | 2.963 | 3.188  | 3.39   | 3.755  | 4.12   | 3.229 | 100.0%  | 10    |
  | heat.update_stack | 4.699 | 4.993  | 5.247  | 5.713  | 6.179  | 5.079 | 100.0%  | 10    |
  | heat.delete_stack | 1.586 | 2.029  | 2.587  | 2.612  | 2.636  | 2.062 | 100.0%  | 10    |
  | total             | 9.696 | 10.458 | 10.863 | 11.215 | 11.567 | 10.37 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 31.0684840679
  Full duration: 34.8022019863
  
  
  
  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 6     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 6.64154100418
  Full duration: 14.7267448902
  
  
  
  test scenario HeatStacks.create_update_delete_stack
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 2.937 | 3.274  | 3.45   | 3.488  | 3.525  | 3.27   | 100.0%  | 10    |
  | heat.update_stack | 4.832 | 4.978  | 5.254  | 5.624  | 5.994  | 5.084  | 100.0%  | 10    |
  | heat.delete_stack | 1.49  | 2.095  | 2.778  | 2.825  | 2.873  | 2.137  | 100.0%  | 10    |
  | total             | 9.553 | 10.809 | 11.06  | 11.083 | 11.105 | 10.491 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 31.7130131721
  Full duration: 35.5221500397
  
  
  
  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.842 | 3.14   | 3.315  | 3.317  | 3.32  | 3.127 | 100.0%  | 10    |
  | heat.update_stack | 3.528 | 3.713  | 3.874  | 3.98   | 4.086 | 3.746 | 100.0%  | 10    |
  | heat.delete_stack | 0.609 | 1.418  | 1.547  | 1.687  | 1.826 | 1.237 | 100.0%  | 10    |
  | total             | 7.439 | 8.161  | 8.587  | 8.686  | 8.786 | 8.111 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.0782799721
  Full duration: 28.0063171387
  
  
  
  test scenario HeatStacks.create_and_list_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.916 | 3.109  | 3.265  | 3.324  | 3.382 | 3.111 | 100.0%  | 10    |
  | heat.list_stacks  | 0.039 | 0.108  | 0.198  | 0.211  | 0.224 | 0.117 | 100.0%  | 10    |
  | total             | 3.036 | 3.211  | 3.427  | 3.452  | 3.477 | 3.228 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.50542497635
  Full duration: 16.6530652046
  
  
  
  test scenario HeatStacks.create_check_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.931 | 3.305  | 3.435  | 3.459  | 3.483 | 3.246 | 100.0%  | 10    |
  | heat.check_stack  | 0.298 | 0.595  | 1.379  | 1.522  | 1.665 | 0.709 | 100.0%  | 10    |
  | heat.delete_stack | 0.531 | 1.498  | 1.703  | 1.77   | 1.838 | 1.286 | 100.0%  | 10    |
  | total             | 4.012 | 5.271  | 6.372  | 6.396  | 6.42  | 5.24  | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.8742229939
  Full duration: 18.9062831402
  
  
  
  2016-02-11 11:28:20,183 - run_rally - DEBUG - task_id : 387dedc1-62f1-4d72-8a34-bbf4940fd1ac
  2016-02-11 11:28:20,183 - run_rally - DEBUG - running command line : rally task report 387dedc1-62f1-4d72-8a34-bbf4940fd1ac --out /home/opnfv/functest/results/rally/opnfv-heat.html
  2016-02-11 11:28:20,821 - run_rally - DEBUG - running command line : rally task results 387dedc1-62f1-4d72-8a34-bbf4940fd1ac
  2016-02-11 11:28:21,416 - run_rally - DEBUG - saving json file
  2016-02-11 11:28:21,420 - run_rally - DEBUG - Push result into DB
  2016-02-11 11:28:28,166 - run_rally - DEBUG - <Response [200]>
  2016-02-11 11:28:28,168 - run_rally - INFO - Test scenario: "heat" Failed.
  
  2016-02-11 11:28:28,169 - run_rally - INFO - Starting test scenario "keystone" ...
  2016-02-11 11:28:28,169 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-keystone.yaml
  2016-02-11 11:28:28,538 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '48071712-5859-4fe7-a4fa-f723725ef015', 'service_list': ['keystone'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-11 11:29:56,831 - run_rally - INFO - 
   Preparing input task
   Task  69a631a7-3909-4268-90ca-ce29363de184: started
  Task 69a631a7-3909-4268-90ca-ce29363de184: finished
  
  test scenario KeystoneBasic.create_tenant_with_users
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.122 | 0.132  | 0.143  | 0.146  | 0.148 | 0.133 | 100.0%  | 10    |
  | keystone.create_users  | 0.643 | 0.699  | 0.755  | 0.771  | 0.788 | 0.707 | 100.0%  | 10    |
  | total                  | 0.769 | 0.833  | 0.885  | 0.908  | 0.931 | 0.84  | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.4707968235
  Full duration: 12.8068091869
  
  
  
  test scenario KeystoneBasic.create_add_and_list_user_roles
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.11  | 0.125  | 0.144  | 0.145  | 0.146 | 0.129 | 100.0%  | 10    |
  | keystone.add_role    | 0.092 | 0.101  | 0.112  | 0.122  | 0.131 | 0.103 | 100.0%  | 10    |
  | keystone.list_roles  | 0.053 | 0.059  | 0.098  | 0.104  | 0.11  | 0.067 | 100.0%  | 10    |
  | total                | 0.261 | 0.301  | 0.319  | 0.329  | 0.339 | 0.299 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.910135984421
  Full duration: 6.13412499428
  
  
  
  test scenario KeystoneBasic.add_and_remove_user_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.12  | 0.21   | 0.264  | 0.266  | 0.269 | 0.197 | 100.0%  | 10    |
  | keystone.add_role    | 0.093 | 0.099  | 0.155  | 0.157  | 0.16  | 0.111 | 100.0%  | 10    |
  | keystone.remove_role | 0.066 | 0.084  | 0.107  | 0.107  | 0.107 | 0.085 | 100.0%  | 10    |
  | total                | 0.308 | 0.42   | 0.459  | 0.467  | 0.475 | 0.393 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.23530602455
  Full duration: 6.42563891411
  
  
  
  test scenario KeystoneBasic.create_update_and_delete_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.124 | 0.218  | 0.233  | 0.236  | 0.238 | 0.193 | 100.0%  | 10    |
  | keystone.update_tenant | 0.056 | 0.063  | 0.069  | 0.071  | 0.073 | 0.064 | 100.0%  | 10    |
  | keystone.delete_tenant | 0.125 | 0.14   | 0.159  | 0.177  | 0.195 | 0.144 | 100.0%  | 10    |
  | total                  | 0.322 | 0.415  | 0.447  | 0.462  | 0.476 | 0.4   | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.26893806458
  Full duration: 5.33236098289
  
  
  
  test scenario KeystoneBasic.create_and_delete_service
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_service | 0.114 | 0.136  | 0.162  | 0.165  | 0.167 | 0.136 | 100.0%  | 10    |
  | keystone.delete_service | 0.057 | 0.066  | 0.072  | 0.073  | 0.073 | 0.066 | 100.0%  | 10    |
  | total                   | 0.177 | 0.207  | 0.22   | 0.226  | 0.233 | 0.202 | 100.0%  | 10    |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.596924066544
  Full duration: 4.35803890228
  
  
  
  test scenario KeystoneBasic.create_tenant
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +------------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max  | avg   | success | count |
  +------------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | keystone.create_tenant | 0.115 | 0.136  | 0.161  | 0.166  | 0.17 | 0.136 | 100.0%  | 10    |
  | total                  | 0.115 | 0.136  | 0.161  | 0.166  | 0.17 | 0.136 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+------+-------+---------+-------+
  Load duration: 0.419772863388
  Full duration: 4.34560608864
  
  
  
  test scenario KeystoneBasic.create_user
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.127 | 0.143  | 0.185  | 0.19   | 0.195 | 0.149 | 100.0%  | 10    |
  | total                | 0.127 | 0.143  | 0.185  | 0.19   | 0.195 | 0.149 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.44237613678
  Full duration: 4.28579497337
  
  
  
  test scenario KeystoneBasic.create_and_list_tenants
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.112 | 0.127  | 0.154  | 0.155  | 0.157 | 0.131 | 100.0%  | 10    |
  | keystone.list_tenants  | 0.049 | 0.056  | 0.096  | 0.1    | 0.105 | 0.065 | 100.0%  | 10    |
  | total                  | 0.167 | 0.19   | 0.222  | 0.224  | 0.225 | 0.196 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.609141111374
  Full duration: 6.10883498192
  
  
  
  test scenario KeystoneBasic.create_and_delete_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.135 | 0.234  | 0.289  | 0.291  | 0.292 | 0.208 | 100.0%  | 10    |
  | keystone.delete_role | 0.099 | 0.12   | 0.14   | 0.182  | 0.224 | 0.127 | 100.0%  | 10    |
  | total                | 0.257 | 0.341  | 0.401  | 0.458  | 0.516 | 0.336 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.982420921326
  Full duration: 5.07269620895
  
  
  
  test scenario KeystoneBasic.get_entities
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.116 | 0.123  | 0.126  | 0.129  | 0.131 | 0.123 | 100.0%  | 10    |
  | keystone.create_user   | 0.06  | 0.067  | 0.072  | 0.073  | 0.074 | 0.067 | 100.0%  | 10    |
  | keystone.create_role   | 0.048 | 0.053  | 0.063  | 0.063  | 0.064 | 0.054 | 100.0%  | 10    |
  | keystone.get_tenant    | 0.043 | 0.054  | 0.078  | 0.092  | 0.106 | 0.06  | 100.0%  | 10    |
  | keystone.get_user      | 0.047 | 0.059  | 0.079  | 0.079  | 0.08  | 0.06  | 100.0%  | 10    |
  | keystone.get_role      | 0.043 | 0.051  | 0.06   | 0.074  | 0.089 | 0.054 | 100.0%  | 10    |
  | keystone.service_list  | 0.044 | 0.049  | 0.06   | 0.078  | 0.095 | 0.054 | 100.0%  | 10    |
  | keystone.get_service   | 0.042 | 0.052  | 0.056  | 0.058  | 0.059 | 0.052 | 100.0%  | 10    |
  | total                  | 0.471 | 0.525  | 0.559  | 0.573  | 0.586 | 0.525 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.58637881279
  Full duration: 9.88001894951
  
  
  
  test scenario KeystoneBasic.create_and_list_users
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.13  | 0.144  | 0.161  | 0.164  | 0.166 | 0.146 | 100.0%  | 10    |
  | keystone.list_users  | 0.055 | 0.064  | 0.072  | 0.073  | 0.073 | 0.064 | 100.0%  | 10    |
  | total                | 0.186 | 0.209  | 0.234  | 0.234  | 0.234 | 0.21  | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.629101037979
  Full duration: 4.65930700302
  
  
  
  2016-02-11 11:29:56,832 - run_rally - DEBUG - task_id : 69a631a7-3909-4268-90ca-ce29363de184
  2016-02-11 11:29:56,832 - run_rally - DEBUG - running command line : rally task report 69a631a7-3909-4268-90ca-ce29363de184 --out /home/opnfv/functest/results/rally/opnfv-keystone.html
  2016-02-11 11:29:57,448 - run_rally - DEBUG - running command line : rally task results 69a631a7-3909-4268-90ca-ce29363de184
  2016-02-11 11:29:58,033 - run_rally - DEBUG - saving json file
  2016-02-11 11:29:58,036 - run_rally - DEBUG - Push result into DB
  2016-02-11 11:30:04,403 - run_rally - DEBUG - <Response [200]>
  2016-02-11 11:30:04,405 - run_rally - INFO - Test scenario: "keystone" OK.
  
  2016-02-11 11:30:04,406 - run_rally - INFO - Starting test scenario "neutron" ...
  2016-02-11 11:30:04,406 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-neutron.yaml
  2016-02-11 11:30:04,724 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '48071712-5859-4fe7-a4fa-f723725ef015', 'service_list': ['neutron'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-11 11:35:06,092 - run_rally - INFO - 
   Preparing input task
   Task  1255bc34-bd71-4bcc-8a24-fe4560d922f6: started
  Task 1255bc34-bd71-4bcc-8a24-fe4560d922f6: finished
  
  test scenario NeutronNetworks.create_and_delete_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.433 | 0.45   | 0.589  | 0.61   | 0.631 | 0.494 | 100.0%  | 10    |
  | neutron.delete_port | 0.153 | 0.159  | 0.299  | 0.301  | 0.303 | 0.2   | 100.0%  | 10    |
  | total               | 0.593 | 0.718  | 0.793  | 0.814  | 0.834 | 0.695 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.11287713051
  Full duration: 25.6731390953
  
  
  
  test scenario NeutronNetworks.create_and_list_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.389 | 0.441  | 0.515  | 0.52   | 0.525 | 0.448 | 100.0%  | 10    |
  | neutron.create_router        | 0.04  | 0.177  | 0.33   | 0.343  | 0.356 | 0.165 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.279 | 0.432  | 0.557  | 0.559  | 0.56  | 0.423 | 100.0%  | 10    |
  | neutron.list_routers         | 0.033 | 0.046  | 0.195  | 0.195  | 0.196 | 0.085 | 100.0%  | 10    |
  | total                        | 0.805 | 1.103  | 1.357  | 1.41   | 1.462 | 1.121 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.03660392761
  Full duration: 27.9115738869
  
  
  
  test scenario NeutronNetworks.create_and_delete_routers
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet           | 0.397 | 0.428  | 0.485  | 0.539  | 0.593 | 0.443 | 100.0%  | 10    |
  | neutron.create_router           | 0.038 | 0.109  | 0.192  | 0.194  | 0.195 | 0.114 | 100.0%  | 10    |
  | neutron.add_interface_router    | 0.279 | 0.3    | 0.528  | 0.557  | 0.585 | 0.362 | 100.0%  | 10    |
  | neutron.remove_interface_router | 0.219 | 0.373  | 0.514  | 0.545  | 0.576 | 0.355 | 100.0%  | 10    |
  | neutron.delete_router           | 0.144 | 0.216  | 0.321  | 0.372  | 0.423 | 0.234 | 100.0%  | 10    |
  | total                           | 1.282 | 1.545  | 1.692  | 1.731  | 1.77  | 1.508 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.48996591568
  Full duration: 28.484484911
  
  
  
  test scenario NeutronNetworks.create_and_list_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.433 | 0.537  | 0.725  | 0.729  | 0.733 | 0.57  | 100.0%  | 10    |
  | neutron.list_ports  | 0.093 | 0.211  | 0.321  | 0.348  | 0.376 | 0.218 | 100.0%  | 10    |
  | total               | 0.566 | 0.723  | 1.016  | 1.032  | 1.047 | 0.788 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.25542998314
  Full duration: 25.8901529312
  
  
  
  test scenario NeutronNetworks.create_and_delete_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.403 | 0.436  | 0.522  | 0.524  | 0.527 | 0.447 | 100.0%  | 10    |
  | neutron.delete_subnet | 0.136 | 0.146  | 0.29   | 0.296  | 0.302 | 0.187 | 100.0%  | 10    |
  | total                 | 0.548 | 0.578  | 0.747  | 0.781  | 0.815 | 0.634 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.82214593887
  Full duration: 25.1257920265
  
  
  
  test scenario NeutronNetworks.create_and_delete_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.305 | 0.343  | 0.4    | 0.403  | 0.405 | 0.349 | 100.0%  | 10    |
  | neutron.delete_network | 0.098 | 0.113  | 0.28   | 0.311  | 0.341 | 0.175 | 100.0%  | 10    |
  | total                  | 0.411 | 0.488  | 0.615  | 0.681  | 0.746 | 0.525 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.58722496033
  Full duration: 14.0869660378
  
  
  
  test scenario NeutronNetworks.create_and_list_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.299 | 0.348  | 0.456  | 0.46   | 0.463 | 0.37  | 100.0%  | 10    |
  | neutron.list_networks  | 0.043 | 0.171  | 0.319  | 0.381  | 0.443 | 0.165 | 100.0%  | 10    |
  | total                  | 0.342 | 0.516  | 0.655  | 0.725  | 0.795 | 0.535 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.51354122162
  Full duration: 15.9000859261
  
  
  
  test scenario NeutronNetworks.create_and_update_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.418 | 0.509  | 0.572  | 0.586  | 0.6   | 0.508 | 100.0%  | 10    |
  | neutron.create_router        | 0.037 | 0.044  | 0.195  | 0.222  | 0.249 | 0.081 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.286 | 0.429  | 0.539  | 0.54   | 0.54  | 0.419 | 100.0%  | 10    |
  | neutron.update_router        | 0.123 | 0.143  | 0.323  | 0.365  | 0.407 | 0.195 | 100.0%  | 10    |
  | total                        | 1.053 | 1.224  | 1.325  | 1.341  | 1.356 | 1.203 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.53330993652
  Full duration: 28.5734660625
  
  
  
  test scenario NeutronNetworks.create_and_update_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.299 | 0.394  | 0.428  | 0.449  | 0.47  | 0.38  | 100.0%  | 10    |
  | neutron.update_network | 0.094 | 0.268  | 0.409  | 0.409  | 0.41  | 0.247 | 100.0%  | 10    |
  | total                  | 0.435 | 0.647  | 0.806  | 0.808  | 0.809 | 0.627 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.82976198196
  Full duration: 15.7649109364
  
  
  
  test scenario NeutronNetworks.create_and_update_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.435 | 0.52   | 0.67   | 0.672  | 0.674 | 0.54  | 100.0%  | 10    |
  | neutron.update_port | 0.106 | 0.187  | 0.268  | 0.27   | 0.272 | 0.187 | 100.0%  | 10    |
  | total               | 0.585 | 0.724  | 0.831  | 0.881  | 0.931 | 0.728 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.22469115257
  Full duration: 26.4524641037
  
  
  
  test scenario NeutronNetworks.create_and_list_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.406 | 0.545  | 0.646  | 0.646  | 0.647 | 0.549 | 100.0%  | 10    |
  | neutron.list_subnets  | 0.06  | 0.099  | 0.241  | 0.252  | 0.264 | 0.139 | 100.0%  | 10    |
  | total                 | 0.474 | 0.705  | 0.812  | 0.841  | 0.869 | 0.688 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.99994397163
  Full duration: 26.4032180309
  
  
  
  test scenario NeutronNetworks.create_and_update_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.398 | 0.438  | 0.465  | 0.465  | 0.466 | 0.439 | 100.0%  | 10    |
  | neutron.update_subnet | 0.151 | 0.331  | 0.544  | 0.589  | 0.634 | 0.358 | 100.0%  | 10    |
  | total                 | 0.616 | 0.763  | 0.976  | 1.027  | 1.078 | 0.796 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.42046093941
  Full duration: 26.611082077
  
  
  
  2016-02-11 11:35:06,092 - run_rally - DEBUG - task_id : 1255bc34-bd71-4bcc-8a24-fe4560d922f6
  2016-02-11 11:35:06,092 - run_rally - DEBUG - running command line : rally task report 1255bc34-bd71-4bcc-8a24-fe4560d922f6 --out /home/opnfv/functest/results/rally/opnfv-neutron.html
  2016-02-11 11:35:06,709 - run_rally - DEBUG - running command line : rally task results 1255bc34-bd71-4bcc-8a24-fe4560d922f6
  2016-02-11 11:35:07,303 - run_rally - DEBUG - saving json file
  2016-02-11 11:35:07,308 - run_rally - DEBUG - Push result into DB
  2016-02-11 11:35:13,942 - run_rally - DEBUG - <Response [200]>
  2016-02-11 11:35:13,945 - run_rally - INFO - Test scenario: "neutron" OK.
  
  2016-02-11 11:35:13,945 - run_rally - INFO - Starting test scenario "nova" ...
  2016-02-11 11:35:13,945 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-nova.yaml
  2016-02-11 11:35:14,543 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '48071712-5859-4fe7-a4fa-f723725ef015', 'service_list': ['nova'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-11 12:09:23,356 - run_rally - INFO - 
   Preparing input task
   Task  5d0308fc-048b-4829-b346-6500d3e21bd3: started
  Task 5d0308fc-048b-4829-b346-6500d3e21bd3: finished
  
  test scenario NovaKeypair.create_and_delete_keypair
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.35  | 0.482  | 0.564  | 0.569  | 0.573 | 0.477 | 100.0%  | 10    |
  | nova.delete_keypair | 0.013 | 0.018  | 0.02   | 0.02   | 0.02  | 0.018 | 100.0%  | 10    |
  | total               | 0.368 | 0.501  | 0.583  | 0.587  | 0.591 | 0.495 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.56911206245
  Full duration: 15.5810060501
  
  
  
  test scenario NovaServers.boot_and_live_migrate_server
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 24.0756909847
  Full duration: 45.605629921
  
  
  
  test scenario NovaServers.resize_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 8.5    | 10.265 | 13.462 | 13.48  | 13.497 | 11.031 | 100.0%  | 10    |
  | nova.resize         | 21.021 | 31.715 | 41.894 | 41.955 | 42.017 | 31.101 | 100.0%  | 10    |
  | nova.resize_confirm | 2.366  | 2.385  | 2.458  | 2.508  | 2.557  | 2.406  | 100.0%  | 10    |
  | nova.delete_server  | 2.374  | 2.561  | 4.673  | 4.716  | 4.759  | 3.309  | 100.0%  | 10    |
  | total               | 35.485 | 48.58  | 62.131 | 62.205 | 62.28  | 47.847 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 135.703742027
  Full duration: 149.641403913
  
  
  
  test scenario NovaServers.snapshot_server
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | action                 | min    | median | 90%ile  | 95%ile  | max     | avg    | success | count |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  | nova.boot_server       | 8.546  | 11.086 | 12.297  | 12.315  | 12.333  | 10.961 | 100.0%  | 10    |
  | nova.create_image      | 28.926 | 39.293 | 53.571  | 59.29   | 65.01   | 42.354 | 100.0%  | 10    |
  | nova.delete_server     | 2.376  | 2.832  | 4.729   | 4.74    | 4.751   | 3.158  | 100.0%  | 10    |
  | nova.boot_server (2)   | 20.905 | 25.466 | 34.935  | 35.116  | 35.297  | 27.05  | 100.0%  | 10    |
  | nova.delete_server (2) | 2.398  | 2.755  | 4.917   | 4.949   | 4.981   | 3.137  | 100.0%  | 10    |
  | nova.delete_image      | 0.186  | 0.447  | 0.633   | 0.894   | 1.154   | 0.471  | 100.0%  | 10    |
  | total                  | 69.69  | 81.986 | 108.409 | 113.975 | 119.542 | 87.131 | 100.0%  | 10    |
  +------------------------+--------+--------+---------+---------+---------+--------+---------+-------+
  Load duration: 245.940519094
  Full duration: 270.120299816
  
  
  
  test scenario NovaKeypair.boot_and_delete_server_with_keypair
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_keypair | 0.36   | 0.446  | 0.595  | 0.613  | 0.631  | 0.474  | 100.0%  | 10    |
  | nova.boot_server    | 8.197  | 9.375  | 10.819 | 11.368 | 11.918 | 9.711  | 100.0%  | 10    |
  | nova.delete_server  | 2.369  | 2.389  | 2.423  | 2.473  | 2.523  | 2.402  | 100.0%  | 10    |
  | nova.delete_keypair | 0.012  | 0.019  | 0.023  | 0.023  | 0.023  | 0.019  | 100.0%  | 10    |
  | total               | 11.116 | 12.177 | 13.793 | 14.36  | 14.927 | 12.607 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 36.5086538792
  Full duration: 59.5541279316
  
  
  
  test scenario NovaKeypair.create_and_list_keypairs
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.383 | 0.428  | 0.577  | 0.577  | 0.577 | 0.451 | 100.0%  | 10    |
  | nova.list_keypairs  | 0.012 | 0.018  | 0.02   | 0.02   | 0.021 | 0.017 | 100.0%  | 10    |
  | total               | 0.4   | 0.444  | 0.593  | 0.594  | 0.595 | 0.468 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.35172510147
  Full duration: 16.8010981083
  
  
  
  test scenario NovaServers.list_servers
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.list_servers | 0.578 | 0.66   | 0.698  | 0.727  | 0.757 | 0.653 | 100.0%  | 10    |
  | total             | 0.578 | 0.66   | 0.698  | 0.727  | 0.757 | 0.653 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.92253804207
  Full duration: 65.4294450283
  
  
  
  test scenario NovaServers.boot_server_attach_created_volume_and_live_migrate
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 46.8340380192
  Full duration: 79.3581779003
  
  
  
  test scenario NovaServers.boot_server_from_volume_and_delete
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.263  | 3.608  | 5.727  | 5.887  | 6.048  | 4.351  | 100.0%  | 10    |
  | nova.boot_server     | 13.167 | 14.489 | 16.099 | 17.146 | 18.192 | 14.652 | 100.0%  | 10    |
  | nova.delete_server   | 4.488  | 4.602  | 4.8    | 4.819  | 4.839  | 4.628  | 100.0%  | 10    |
  | total                | 21.025 | 22.693 | 26.393 | 27.28  | 28.166 | 23.631 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 69.0365488529
  Full duration: 98.4866499901
  
  
  
  test scenario NovaServers.boot_and_migrate_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 8.678  | 10.115 | 12.244 | 12.524 | 12.805 | 10.543 | 100.0%  | 10    |
  | nova.stop_server    | 5.126  | 15.546 | 15.762 | 15.837 | 15.912 | 14.377 | 100.0%  | 10    |
  | nova.migrate        | 16.303 | 21.071 | 25.467 | 25.57  | 25.674 | 20.932 | 100.0%  | 10    |
  | nova.resize_confirm | 2.368  | 2.387  | 2.574  | 2.585  | 2.596  | 2.44   | 100.0%  | 10    |
  | nova.delete_server  | 2.368  | 2.392  | 2.533  | 2.619  | 2.704  | 2.438  | 100.0%  | 10    |
  | total               | 39.82  | 51.63  | 57.576 | 57.814 | 58.051 | 50.731 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 141.781988859
  Full duration: 156.064862967
  
  
  
  test scenario NovaServers.boot_and_delete_server
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action             | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server   | 8.445  | 10.994 | 13.498 | 13.596 | 13.694 | 10.945 | 100.0%  | 10    |
  | nova.delete_server | 2.367  | 2.486  | 4.61   | 4.64   | 4.67   | 3.089  | 100.0%  | 10    |
  | total              | 10.812 | 14.816 | 16.064 | 16.088 | 16.113 | 14.034 | 100.0%  | 10    |
  +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 40.6690340042
  Full duration: 64.2563021183
  
  
  
  test scenario NovaServers.boot_and_rebuild_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 8.348  | 11.07  | 13.505 | 13.575 | 13.646 | 10.951 | 100.0%  | 10    |
  | nova.rebuild_server | 7.479  | 15.492 | 16.807 | 20.016 | 23.225 | 14.764 | 100.0%  | 10    |
  | nova.delete_server  | 2.392  | 4.47   | 4.54   | 4.596  | 4.652  | 3.692  | 100.0%  | 10    |
  | total               | 20.316 | 31.223 | 33.99  | 34.082 | 34.174 | 29.407 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 86.6938700676
  Full duration: 109.955939054
  
  
  
  test scenario NovaSecGroup.create_and_list_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.421  | 1.661  | 2.019  | 2.059  | 2.098  | 1.728  | 100.0%  | 10    |
  | nova.create_100_rules          | 8.863  | 10.358 | 10.566 | 10.637 | 10.709 | 10.081 | 100.0%  | 10    |
  | nova.list_security_groups      | 0.093  | 0.171  | 0.218  | 0.228  | 0.239  | 0.171  | 100.0%  | 10    |
  | total                          | 10.803 | 12.109 | 12.506 | 12.619 | 12.733 | 11.981 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 35.1620168686
  Full duration: 62.5070729256
  
  
  
  test scenario NovaSecGroup.create_and_delete_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 1.351  | 1.93   | 2.039  | 2.068  | 2.096  | 1.824  | 100.0%  | 10    |
  | nova.create_100_rules          | 8.92   | 9.841  | 10.419 | 10.488 | 10.557 | 9.801  | 100.0%  | 10    |
  | nova.delete_10_security_groups | 0.844  | 0.885  | 0.939  | 0.954  | 0.969  | 0.891  | 100.0%  | 10    |
  | total                          | 11.461 | 12.712 | 12.926 | 12.988 | 13.049 | 12.516 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 37.1039390564
  Full duration: 51.6090979576
  
  
  
  test scenario NovaServers.boot_and_bounce_server
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  | action                  | min    | median | 90%ile | 95%ile  | max     | avg    | success | count |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  | nova.boot_server        | 8.375  | 9.683  | 10.167 | 11.196  | 12.224  | 9.742  | 100.0%  | 10    |
  | nova.reboot_server      | 2.435  | 4.597  | 4.683  | 4.731   | 4.78    | 4.385  | 100.0%  | 10    |
  | nova.soft_reboot_server | 6.561  | 6.748  | 18.978 | 71.705  | 124.431 | 18.545 | 100.0%  | 10    |
  | nova.stop_server        | 4.627  | 4.663  | 4.844  | 4.846   | 4.847   | 4.705  | 100.0%  | 10    |
  | nova.start_server       | 2.639  | 2.745  | 3.798  | 3.892   | 3.986   | 2.978  | 100.0%  | 10    |
  | nova.rescue_server      | 6.603  | 11.178 | 17.543 | 17.565  | 17.587  | 11.682 | 100.0%  | 10    |
  | nova.unrescue_server    | 2.342  | 4.469  | 6.599  | 6.617   | 6.634   | 4.682  | 100.0%  | 10    |
  | nova.delete_server      | 2.363  | 2.393  | 4.494  | 4.499   | 4.504   | 2.825  | 100.0%  | 10    |
  | total                   | 41.094 | 48.675 | 64.097 | 115.103 | 166.11  | 59.555 | 100.0%  | 10    |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  Load duration: 264.457379103
  Full duration: 288.250715971
  
  
  
  test scenario NovaServers.boot_server
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action           | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server | 8.162 | 11.1   | 12.354 | 12.414 | 12.474 | 10.973 | 100.0%  | 10    |
  | total            | 8.162 | 11.1   | 12.354 | 12.414 | 12.474 | 10.973 | 100.0%  | 10    |
  +------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 31.763892889
  Full duration: 56.217361927
  
  
  
  test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
  +-----------------------------------------------------------------------------------------------------------+
  |                                           Response Times (sec)                                            |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups    | 1.475  | 1.787  | 2.114  | 2.126  | 2.139  | 1.802  | 100.0%  | 10    |
  | nova.create_100_rules             | 9.086  | 9.76   | 10.588 | 10.617 | 10.645 | 9.838  | 100.0%  | 10    |
  | nova.boot_server                  | 7.854  | 10.956 | 11.432 | 11.459 | 11.485 | 10.169 | 100.0%  | 10    |
  | nova.get_attached_security_groups | 0.13   | 0.15   | 0.18   | 0.238  | 0.296  | 0.163  | 100.0%  | 10    |
  | nova.delete_server                | 2.396  | 2.436  | 4.649  | 4.688  | 4.726  | 3.095  | 100.0%  | 10    |
  | nova.delete_10_security_groups    | 0.804  | 0.848  | 0.94   | 0.981  | 1.022  | 0.874  | 100.0%  | 10    |
  | total                             | 22.492 | 25.639 | 29.318 | 29.34  | 29.362 | 25.942 | 100.0%  | 10    |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 75.6021800041
  Full duration: 99.6540331841
  
  
  
  test scenario NovaServers.pause_and_unpause_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 9.732  | 10.884 | 11.218 | 11.745 | 12.272 | 10.741 | 100.0%  | 10    |
  | nova.pause_server   | 2.307  | 2.398  | 2.517  | 2.601  | 2.685  | 2.422  | 100.0%  | 10    |
  | nova.unpause_server | 2.308  | 2.398  | 2.511  | 2.584  | 2.656  | 2.416  | 100.0%  | 10    |
  | nova.delete_server  | 2.378  | 2.629  | 4.553  | 4.634  | 4.715  | 3.125  | 100.0%  | 10    |
  | total               | 17.279 | 18.34  | 20.126 | 20.405 | 20.683 | 18.704 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 55.6299200058
  Full duration: 79.6088850498
  
  
  
  test scenario NovaServers.boot_server_from_volume_and_live_migrate
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 58.3723990917
  Full duration: 88.5405950546
  
  
  
  test scenario NovaServers.boot_server_from_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 3.351  | 4.603  | 5.886  | 5.919  | 5.953  | 4.626  | 100.0%  | 10    |
  | nova.boot_server     | 12.326 | 15.273 | 18.357 | 18.452 | 18.546 | 15.585 | 100.0%  | 10    |
  | total                | 15.677 | 20.516 | 24.089 | 24.139 | 24.189 | 20.212 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 59.4558730125
  Full duration: 95.1560180187
  
  
  
  test scenario NovaServers.boot_and_list_server
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server  | 9.422 | 11.71  | 12.617 | 13.138 | 13.658 | 11.406 | 100.0%  | 10    |
  | nova.list_servers | 0.165 | 0.204  | 0.326  | 0.365  | 0.404  | 0.238  | 100.0%  | 10    |
  | total             | 9.714 | 11.913 | 12.801 | 13.33  | 13.858 | 11.644 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 34.6017370224
  Full duration: 69.1325480938
  
  
  
  2016-02-11 12:09:23,356 - run_rally - DEBUG - task_id : 5d0308fc-048b-4829-b346-6500d3e21bd3
  2016-02-11 12:09:23,357 - run_rally - DEBUG - running command line : rally task report 5d0308fc-048b-4829-b346-6500d3e21bd3 --out /home/opnfv/functest/results/rally/opnfv-nova.html
  2016-02-11 12:09:24,060 - run_rally - DEBUG - running command line : rally task results 5d0308fc-048b-4829-b346-6500d3e21bd3
  2016-02-11 12:09:24,668 - run_rally - DEBUG - saving json file
  2016-02-11 12:09:24,675 - run_rally - DEBUG - Push result into DB
  2016-02-11 12:09:32,025 - run_rally - DEBUG - <Response [200]>
  2016-02-11 12:09:32,029 - run_rally - INFO - Test scenario: "nova" Failed.
  
  2016-02-11 12:09:32,030 - run_rally - INFO - Starting test scenario "quotas" ...
  2016-02-11 12:09:32,030 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-quotas.yaml
  2016-02-11 12:09:32,619 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '48071712-5859-4fe7-a4fa-f723725ef015', 'service_list': ['quotas'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-11 12:10:18,739 - run_rally - INFO - 
   Preparing input task
   Task  618ee647-de15-4bb4-b5d8-7071f7a1cd3a: started
  Task 618ee647-de15-4bb4-b5d8-7071f7a1cd3a: finished
  
  test scenario Quotas.cinder_update
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max  | avg   | success | count |
  +----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | quotas.update_quotas | 0.613 | 0.711  | 0.827  | 0.859  | 0.89 | 0.729 | 100.0%  | 10    |
  | total                | 0.613 | 0.711  | 0.828  | 0.859  | 0.89 | 0.729 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  Load duration: 2.19303894043
  Full duration: 7.96247792244
  
  
  
  test scenario Quotas.neutron_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.233 | 0.257  | 0.293  | 0.294  | 0.296 | 0.263 | 100.0%  | 10    |
  | total                | 0.296 | 0.323  | 0.36   | 0.361  | 0.361 | 0.329 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.00596499443
  Full duration: 6.2725110054
  
  
  
  test scenario Quotas.cinder_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.588 | 0.654  | 0.75   | 0.751  | 0.753 | 0.668 | 100.0%  | 10    |
  | quotas.delete_quotas | 0.305 | 0.442  | 0.469  | 0.476  | 0.483 | 0.432 | 100.0%  | 10    |
  | total                | 0.925 | 1.09   | 1.204  | 1.22   | 1.236 | 1.101 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.31535387039
  Full duration: 8.83757400513
  
  
  
  test scenario Quotas.nova_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.311 | 0.352  | 0.372  | 0.381  | 0.39  | 0.35  | 100.0%  | 10    |
  | quotas.delete_quotas | 0.019 | 0.023  | 0.028  | 0.03   | 0.033 | 0.023 | 80.0%   | 10    |
  | total                | 0.334 | 0.371  | 0.39   | 0.403  | 0.416 | 0.37  | 80.0%   | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.12344503403
  Full duration: 6.14012598991
  
  
  
  test scenario Quotas.nova_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.343 | 0.364  | 0.388  | 0.397  | 0.406 | 0.366 | 100.0%  | 10    |
  | total                | 0.343 | 0.364  | 0.388  | 0.397  | 0.407 | 0.366 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.11645007133
  Full duration: 6.30511116982
  
  
  
  2016-02-11 12:10:18,739 - run_rally - DEBUG - task_id : 618ee647-de15-4bb4-b5d8-7071f7a1cd3a
  2016-02-11 12:10:18,739 - run_rally - DEBUG - running command line : rally task report 618ee647-de15-4bb4-b5d8-7071f7a1cd3a --out /home/opnfv/functest/results/rally/opnfv-quotas.html
  2016-02-11 12:10:19,340 - run_rally - DEBUG - running command line : rally task results 618ee647-de15-4bb4-b5d8-7071f7a1cd3a
  2016-02-11 12:10:19,916 - run_rally - DEBUG - saving json file
  2016-02-11 12:10:19,917 - run_rally - DEBUG - Push result into DB
  2016-02-11 12:10:26,201 - run_rally - DEBUG - <Response [200]>
  2016-02-11 12:10:26,202 - run_rally - INFO - Test scenario: "quotas" Failed.
  
  2016-02-11 12:10:26,202 - run_rally - INFO - Starting test scenario "requests" ...
  2016-02-11 12:10:26,202 - run_rally - DEBUG - Scenario fetched from : /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/opnfv-requests.yaml
  2016-02-11 12:10:26,596 - run_rally - DEBUG - running command line : rally task start --abort-on-sla-failure --task /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/task.yaml --task-args "{'floating_network': 'ext-net', 'iterations': 10, 'tmpl_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/templates', 'netid': '48071712-5859-4fe7-a4fa-f723725ef015', 'service_list': ['requests'], 'concurrency': 4, 'tenants_amount': 3, 'image_name': 'functest-img', 'glance_image_location': '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img', 'flavor_name': 'm1.tiny', 'smoke': False, 'users_amount': 2, 'sup_dir': '/home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/rally_cert/scenario/support'}" 
  2016-02-11 12:11:10,557 - run_rally - INFO - 
   Preparing input task
   Task  b0726659-cf16-4374-927e-0e279418212f: started
  Task b0726659-cf16-4374-927e-0e279418212f: finished
  
  test scenario HttpRequests.check_random_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 5.449 | 5.479  | 6.067  | 6.096  | 6.125 | 5.599 | 100.0%  | 10    |
  | total                  | 5.449 | 5.479  | 6.067  | 6.096  | 6.125 | 5.599 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.4673690796
  Full duration: 18.8692798615
  
  
  
  test scenario HttpRequests.check_request
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg  | success | count |
  +------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  | requests.check_request | 5.452 | 5.467  | 5.51   | 5.526  | 5.542 | 5.48 | 100.0%  | 10    |
  | total                  | 5.452 | 5.467  | 5.51   | 5.526  | 5.542 | 5.48 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+------+---------+-------+
  Load duration: 16.4834599495
  Full duration: 18.9142780304
  
  
  
  2016-02-11 12:11:10,557 - run_rally - DEBUG - task_id : b0726659-cf16-4374-927e-0e279418212f
  2016-02-11 12:11:10,557 - run_rally - DEBUG - running command line : rally task report b0726659-cf16-4374-927e-0e279418212f --out /home/opnfv/functest/results/rally/opnfv-requests.html
  2016-02-11 12:11:11,152 - run_rally - DEBUG - running command line : rally task results b0726659-cf16-4374-927e-0e279418212f
  2016-02-11 12:11:11,725 - run_rally - DEBUG - saving json file
  2016-02-11 12:11:11,726 - run_rally - DEBUG - Push result into DB
  2016-02-11 12:11:18,337 - run_rally - DEBUG - <Response [200]>
  2016-02-11 12:11:18,338 - run_rally - INFO - Test scenario: "requests" OK.
  
  2016-02-11 12:11:18,338 - run_rally - INFO - 
  
                                                                
                       Rally Summary Report
  +===================+============+===============+===========+
  | Module            | Duration   | nb. Test Run  | Success   |
  +===================+============+===============+===========+
  | authenticate      | 00:18      | 10            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | glance            | 01:54      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | cinder            | 17:31      | 50            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | heat              | 06:56      | 32            | 92.31%    |
  +-------------------+------------+---------------+-----------+
  | keystone          | 01:09      | 29            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | neutron           | 04:46      | 31            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | nova              | 33:41      | 61            | 85.71%    |
  +-------------------+------------+---------------+-----------+
  | quotas            | 00:35      | 7             | 96.00%    |
  +-------------------+------------+---------------+-----------+
  | requests          | 00:37      | 2             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  +===================+============+===============+===========+
  | TOTAL:            | 01:07:31   | 229           | 97.11%    |
  +===================+============+===============+===========+
 
 ::
  
