.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for fuel-os-onos-nofeature-ha
---------------------------------------------------

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
    vPing_ssh- INFO - vPing Start Time:'2016-02-21 09:42:15'
    vPing_ssh- INFO - Creating instance 'opnfv-vping-1'...
     name=opnfv-vping-1
     flavor=<Flavor: m1.small>
     image=c921bde1-b564-4670-9801-7607bb7dd5f9
     network=ddbf909c-8936-4d5a-b499-ae5bc6e4981f

    vPing_ssh- INFO - Instance 'opnfv-vping-1' is ACTIVE.
    vPing_ssh- INFO - Adding 'opnfv-vping-1' to security group 'vPing-sg'...
    vPing_ssh- INFO - Creating instance 'opnfv-vping-2'...
     name=opnfv-vping-2
     flavor=<Flavor: m1.small>
     image=c921bde1-b564-4670-9801-7607bb7dd5f9
     network=ddbf909c-8936-4d5a-b499-ae5bc6e4981f

    vPing_ssh- INFO - Instance 'opnfv-vping-2' is ACTIVE.
    vPing_ssh- INFO - Adding 'opnfv-vping-2' to security group 'vPing-sg'...
    vPing_ssh- INFO - Creating floating IP for VM 'opnfv-vping-2'...
    vPing_ssh- INFO - Floating IP created: '10.118.101.200'
    vPing_ssh- INFO - Associating floating ip: '10.118.101.200' to VM 'opnfv-vping-2'
    vPing_ssh- INFO - Trying to establish SSH connection to 10.118.101.200...
    vPing_ssh- INFO - Waiting for ping...
    vPing_ssh- INFO - vPing detected!
    vPing_ssh- INFO - vPing duration:'267.2' s.
    vPing_ssh- INFO - Cleaning up...
    vPing_ssh- INFO - vPing OK




Tempest
^^^^^^^
::

    +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    | name                                                                                                                                     | time      | status  |
    +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.33888   | success |
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.10971   | success |
    | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 15.11040  | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 30.42278  | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 13.85713  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.32690   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.34397   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.37412   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 1.53125   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.34050   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.55659   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.33680   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.57251   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.33960   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.69068   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.33768   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.67793   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.33491   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 1.60438   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 1.39355   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 1.24188   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 1.85431   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 2.83096   | success |
    | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 6.66403   | success |
    | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 13.11276  | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.0       | fail    |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.11312   | success |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 4.98764   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.62118   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 1.01188   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.73001   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 1.04071   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.53598   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.12633   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.13548   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.08098   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.08810   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.10130   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.63997   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00129   | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.20987   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.10442   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.02285   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.10168   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.08641   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.03051   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.02042   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.08087   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.06620   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.07583   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 1.02614   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.03649   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.10806   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.09498   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.15150   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.76964   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.40090   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.38359   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.65971   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.66699   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.63491   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 5.25088   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 16.25121  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 22.90196  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 11.28175  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 12.26759  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 2.49600   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 2.57009   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 3.21321   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 3.04861   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 3.93770   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 2.76115   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 1.71809   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 1.21977   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 0.91452   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.95440   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 3.16889   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 1.57679   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 1.42447   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 1.46180   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 1.15287   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 1.87581   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.99209   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 0.58096   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 1.07971   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 1.73518   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 1.51942   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.32883   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.01961   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 1.56142   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.03891   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 0.62077   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.07524   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.29801   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.07714   | success |
    | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 0.0       | fail    |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 1.06122   | success |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 1.10604   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.41781   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.03176   | success |
    | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.0       | fail    |
    | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.34417   | success |
    | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 1.00125   | success |
    | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.64367   | success |
    | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.38885   | success |
    | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 2.52793   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.11210   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.08846   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.10244   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.10511   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.10566   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.14063   | success |
    | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.57457   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 1.72677   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 15.66304  | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 3.84418   | success |
    | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 5.53626   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 2.54078   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 4.09094   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 1.98866   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 2.87451   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 5.20792   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 2.28358   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 4.49162   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 3.79765   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 2.99403   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.66099   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.29854   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.32442   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.04955   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.33630   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 2.80651   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.65929   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.36943   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.38991   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.31486   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.30617   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 2.96002   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 3.15725   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 1.88622   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.32563   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.37153   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 3.19676   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 2.65017   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 2.26448   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.38004   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.32783   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 8.61053   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 5.36523   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 3.30263   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 2.90758   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 7.98249   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 4.15672   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 4.09748   | success |
    | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 3.08662   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 1.74965   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 3.81896   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.31019   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 2.07790   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 3.59873   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.33280   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.62361   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 6.93849   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.07141   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 1.31814   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.61532   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.61600   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.59934   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.81253   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.84469   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 3.72972   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.06791   | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 19.60479  | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 3.74694   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 3.11182   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 3.04832   | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 10.66890  | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 18.01898  | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 16.52370  | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 17.05563  | success |
    | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.08365   | success |
    | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.05607   | success |
    | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 374.04656 | fail    |
    | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 340.58084 | fail    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 349.05347 | fail    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 338.91569 | fail    |
    +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    run_tempest - INFO - Results: {'timestart': '2016-02-2109:47:08.529077', 'duration': 512, 'tests': 210, 'failures': 31}

Rally
^^^^^
::

    FUNCTEST.info: Running Rally benchmark suite...
    run_rally - INFO - Starting test scenario "authenticate" ...
    run_rally - INFO -
     Preparing input task
     Task  938ee7f4-76f5-42f3-a908-9eb3557dac60: started
    Task 938ee7f4-76f5-42f3-a908-9eb3557dac60: finished

    test scenario Authenticate.validate_glance
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_glance     | 0.528 | 0.563  | 0.576  | 0.577  | 0.578 | 0.558 | 100.0%  | 10    |
    | authenticate.validate_glance (2) | 0.524 | 0.536  | 0.584  | 0.646  | 0.707 | 0.556 | 100.0%  | 10    |
    | total                            | 1.209 | 1.274  | 1.348  | 1.391  | 1.434 | 1.285 | 100.0%  | 10    |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.82395505905
    Full duration: 11.5060088634



    test scenario Authenticate.keystone
    +----------------------------------------------------------------------------+
    |                            Response Times (sec)                            |
    +--------+-------+--------+--------+--------+------+-------+---------+-------+
    | action | min   | median | 90%ile | 95%ile | max  | avg   | success | count |
    +--------+-------+--------+--------+--------+------+-------+---------+-------+
    | total  | 0.145 | 0.166  | 0.262  | 0.271  | 0.28 | 0.193 | 100.0%  | 10    |
    +--------+-------+--------+--------+--------+------+-------+---------+-------+
    Load duration: 0.597311973572
    Full duration: 8.39117598534



    test scenario Authenticate.validate_heat
    +-----------------------------------------------------------------------------------------------------+
    |                                        Response Times (sec)                                         |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_heat     | 0.289 | 0.308  | 0.338  | 0.34   | 0.342 | 0.312 | 100.0%  | 10    |
    | authenticate.validate_heat (2) | 0.054 | 0.289  | 0.31   | 0.318  | 0.327 | 0.27  | 100.0%  | 10    |
    | total                          | 0.575 | 0.782  | 0.858  | 0.862  | 0.865 | 0.773 | 100.0%  | 10    |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.38020992279
    Full duration: 10.2995789051



    test scenario Authenticate.validate_nova
    +-----------------------------------------------------------------------------------------------------+
    |                                        Response Times (sec)                                         |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_nova     | 0.279 | 0.311  | 0.459  | 0.464  | 0.468 | 0.352 | 100.0%  | 10    |
    | authenticate.validate_nova (2) | 0.033 | 0.056  | 0.061  | 0.063  | 0.065 | 0.053 | 100.0%  | 10    |
    | total                          | 0.477 | 0.53   | 0.699  | 0.711  | 0.723 | 0.569 | 100.0%  | 10    |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.69243693352
    Full duration: 9.33592200279



    test scenario Authenticate.validate_cinder
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_cinder     | 0.276 | 0.29   | 0.335  | 0.335  | 0.335 | 0.302 | 100.0%  | 10    |
    | authenticate.validate_cinder (2) | 0.257 | 0.29   | 0.318  | 0.346  | 0.374 | 0.297 | 100.0%  | 10    |
    | total                            | 0.719 | 0.773  | 0.853  | 0.863  | 0.873 | 0.781 | 100.0%  | 10    |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.3241250515
    Full duration: 9.87282705307



    test scenario Authenticate.validate_neutron
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_neutron     | 0.289 | 0.309  | 0.329  | 0.334  | 0.34  | 0.31  | 100.0%  | 10    |
    | authenticate.validate_neutron (2) | 0.044 | 0.294  | 0.324  | 0.365  | 0.406 | 0.265 | 100.0%  | 10    |
    | total                             | 0.533 | 0.752  | 0.809  | 0.831  | 0.854 | 0.734 | 100.0%  | 10    |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.165102005
    Full duration: 9.4830288887



    run_rally - INFO - Test scenario: "authenticate" OK.

    run_rally - INFO - Starting test scenario "glance" ...
    run_rally - INFO -
     Preparing input task
     Task  158cf9e7-5336-4cfc-be40-3e75d061e99a: started
    Task 158cf9e7-5336-4cfc-be40-3e75d061e99a: finished

    test scenario GlanceImages.list_images
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | glance.list_images | 0.726 | 0.781  | 0.882  | 0.891  | 0.899 | 0.807 | 100.0%  | 10    |
    | total              | 0.726 | 0.783  | 0.882  | 0.891  | 0.899 | 0.807 | 100.0%  | 10    |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.53244495392
    Full duration: 12.5428349972



    test scenario GlanceImages.create_image_and_boot_instances
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | glance.create_image | 6.979  | 7.618  | 7.794  | 7.829  | 7.863  | 7.563  | 100.0%  | 10    |
    | nova.boot_servers   | 8.651  | 10.765 | 11.756 | 11.781 | 11.807 | 10.556 | 100.0%  | 10    |
    | total               | 15.879 | 18.421 | 19.261 | 19.311 | 19.36  | 18.119 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 53.8314111233
    Full duration: 120.073235035



    test scenario GlanceImages.create_and_list_image
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | glance.create_image | 7.329 | 7.6    | 7.99   | 8.113  | 8.236 | 7.653 | 100.0%  | 10    |
    | glance.list_images  | 0.333 | 0.582  | 0.613  | 0.646  | 0.679 | 0.566 | 100.0%  | 10    |
    | total               | 7.902 | 8.164  | 8.547  | 8.674  | 8.802 | 8.219 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 24.6576690674
    Full duration: 38.7420179844



    test scenario GlanceImages.create_and_delete_image
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | glance.create_image | 7.217 | 7.695  | 7.985  | 8.039  | 8.092  | 7.694 | 100.0%  | 10    |
    | glance.delete_image | 1.995 | 2.137  | 2.493  | 2.608  | 2.722  | 2.22  | 100.0%  | 10    |
    | total               | 9.374 | 10.024 | 10.211 | 10.289 | 10.367 | 9.914 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 29.6123759747
    Full duration: 39.9493000507



    run_rally - INFO - Test scenario: "glance" OK.

    run_rally - INFO - Starting test scenario "cinder" ...
    run_rally - INFO -
     Preparing input task
     Task  b1aa2d13-0f7a-4bff-8331-81336fed8893: started
    Task b1aa2d13-0f7a-4bff-8331-81336fed8893: finished

    test scenario CinderVolumes.create_and_attach_volume
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server     | 6.503  | 8.078  | 8.609  | 8.703  | 8.796  | 7.961  | 100.0%  | 10    |
    | cinder.create_volume | 3.188  | 3.68   | 3.956  | 3.978  | 4.0    | 3.679  | 100.0%  | 10    |
    | nova.attach_volume   | 3.64   | 4.357  | 6.302  | 6.474  | 6.646  | 4.857  | 100.0%  | 10    |
    | nova.detach_volume   | 3.578  | 3.916  | 4.783  | 4.818  | 4.854  | 4.034  | 100.0%  | 10    |
    | cinder.delete_volume | 0.561  | 1.816  | 3.1    | 3.132  | 3.165  | 1.823  | 100.0%  | 10    |
    | nova.delete_server   | 2.774  | 2.91   | 3.153  | 3.263  | 3.373  | 2.961  | 100.0%  | 10    |
    | total                | 22.849 | 25.428 | 26.942 | 27.99  | 29.037 | 25.315 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 75.149212122
    Full duration: 118.157259941



    test scenario CinderVolumes.create_and_list_volume
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 7.83  | 9.929  | 10.531 | 10.536 | 10.541 | 9.772  | 100.0%  | 10    |
    | cinder.list_volumes  | 0.08  | 0.374  | 0.44   | 0.453  | 0.465  | 0.361  | 100.0%  | 10    |
    | total                | 8.172 | 10.346 | 10.952 | 10.96  | 10.967 | 10.134 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 29.4478600025
    Full duration: 52.5886940956



    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.301 | 3.843  | 4.226  | 4.357  | 4.488 | 3.882 | 100.0%  | 10    |
    | cinder.list_volumes  | 0.053 | 0.331  | 0.398  | 0.398  | 0.398 | 0.273 | 100.0%  | 10    |
    | total                | 3.637 | 4.144  | 4.619  | 4.733  | 4.847 | 4.156 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 12.4273290634
    Full duration: 34.9144048691



    test scenario CinderVolumes.create_and_list_snapshots
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_snapshot | 2.946 | 3.307  | 3.538  | 3.549  | 3.56  | 3.273 | 100.0%  | 10    |
    | cinder.list_snapshots  | 0.028 | 0.295  | 0.328  | 0.338  | 0.348 | 0.201 | 100.0%  | 10    |
    | total                  | 3.176 | 3.555  | 3.638  | 3.662  | 3.686 | 3.474 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 10.5382380486
    Full duration: 51.362334013



    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.624 | 3.895  | 4.231  | 4.281  | 4.331 | 3.947 | 100.0%  | 10    |
    | cinder.delete_volume | 0.812 | 1.949  | 3.114  | 3.122  | 3.131 | 1.972 | 100.0%  | 10    |
    | total                | 4.618 | 5.84   | 7.204  | 7.278  | 7.351 | 5.92  | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 16.7822580338
    Full duration: 34.5782420635



    test scenario CinderVolumes.create_and_delete_volume
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 9.294  | 9.687  | 9.755  | 9.776  | 9.798  | 9.602  | 100.0%  | 10    |
    | cinder.delete_volume | 0.832  | 2.037  | 2.912  | 3.099  | 3.287  | 1.974  | 100.0%  | 10    |
    | total                | 10.153 | 11.549 | 12.579 | 12.706 | 12.832 | 11.576 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 33.8279159069
    Full duration: 52.5032699108



    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.531 | 3.917  | 4.114  | 4.116  | 4.119 | 3.89  | 100.0%  | 10    |
    | cinder.delete_volume | 0.795 | 0.992  | 3.094  | 3.232  | 3.371 | 1.405 | 100.0%  | 10    |
    | total                | 4.55  | 4.893  | 6.895  | 7.065  | 7.235 | 5.295 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 14.6577680111
    Full duration: 32.7706868649



    test scenario CinderVolumes.create_and_upload_volume_to_image
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume          | 3.529  | 3.821  | 4.216  | 4.22   | 4.223  | 3.861  | 100.0%  | 10    |
    | cinder.upload_volume_to_image | 19.02  | 29.858 | 31.714 | 31.91  | 32.105 | 28.579 | 100.0%  | 10    |
    | cinder.delete_volume          | 0.778  | 2.823  | 3.199  | 3.243  | 3.288  | 2.495  | 100.0%  | 10    |
    | nova.delete_image             | 2.394  | 2.794  | 4.071  | 9.486  | 14.9   | 3.949  | 100.0%  | 10    |
    | total                         | 28.359 | 39.027 | 42.376 | 45.938 | 49.5   | 38.885 | 100.0%  | 10    |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 119.134256124
    Full duration: 139.814013958



    test scenario CinderVolumes.create_and_delete_snapshot
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_snapshot | 3.047 | 3.312  | 3.751  | 4.588  | 5.426 | 3.504 | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.515 | 2.959  | 3.129  | 3.134  | 3.139 | 2.904 | 100.0%  | 10    |
    | total                  | 5.93  | 6.273  | 6.77   | 7.355  | 7.941 | 6.408 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 18.6710958481
    Full duration: 52.810079813



    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.645 | 3.983  | 4.278  | 4.284  | 4.291 | 4.015 | 100.0%  | 10    |
    | total                | 3.645 | 3.983  | 4.278  | 4.284  | 4.291 | 4.015 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 11.9593629837
    Full duration: 30.0458798409



    test scenario CinderVolumes.create_volume
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +----------------------+-----+--------+--------+--------+-------+-------+---------+-------+
    | action               | min | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-----+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.5 | 4.11   | 4.423  | 4.479  | 4.535 | 4.045 | 100.0%  | 10    |
    | total                | 3.5 | 4.11   | 4.423  | 4.479  | 4.535 | 4.045 | 100.0%  | 10    |
    +----------------------+-----+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 11.9883899689
    Full duration: 34.5793349743



    test scenario CinderVolumes.list_volumes
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.list_volumes | 0.527 | 0.566  | 0.622  | 0.634  | 0.647 | 0.579 | 100.0%  | 10    |
    | total               | 0.527 | 0.566  | 0.622  | 0.635  | 0.647 | 0.579 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.71377515793
    Full duration: 66.8403449059



    test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.423  | 3.79   | 4.204  | 4.228  | 4.253  | 3.832  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.595  | 2.914  | 3.105  | 3.107  | 3.109  | 2.93   | 100.0%  | 10    |
    | nova.attach_volume     | 3.943  | 6.629  | 7.921  | 8.552  | 9.183  | 6.368  | 100.0%  | 10    |
    | nova.detach_volume     | 3.275  | 3.933  | 4.098  | 4.151  | 4.204  | 3.813  | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.26   | 2.576  | 3.109  | 3.173  | 3.237  | 2.627  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.572  | 2.766  | 2.935  | 3.011  | 3.086  | 2.543  | 100.0%  | 10    |
    | total                  | 20.778 | 22.953 | 25.368 | 26.28  | 27.193 | 23.194 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 69.8529119492
    Full duration: 173.89911294



    test scenario CinderVolumes.create_from_volume_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.664 | 3.994  | 4.4    | 4.405  | 4.411 | 4.043 | 100.0%  | 10    |
    | cinder.delete_volume | 2.706 | 3.262  | 3.503  | 3.525  | 3.547 | 3.211 | 100.0%  | 10    |
    | total                | 6.956 | 7.239  | 7.437  | 7.513  | 7.589 | 7.254 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 21.7929730415
    Full duration: 56.4282138348



    test scenario CinderVolumes.create_and_extend_volume
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 3.519 | 3.91   | 4.25   | 4.293  | 4.336  | 3.898  | 100.0%  | 10    |
    | cinder.extend_volume | 0.954 | 3.479  | 3.822  | 3.974  | 4.126  | 3.266  | 100.0%  | 10    |
    | cinder.delete_volume | 2.743 | 3.002  | 3.324  | 3.34   | 3.356  | 3.018  | 100.0%  | 10    |
    | total                | 8.353 | 10.523 | 10.792 | 10.838 | 10.885 | 10.182 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 30.6360728741
    Full duration: 49.9283909798



    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.39   | 3.97   | 4.263  | 4.45   | 4.638  | 3.957  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.608  | 3.069  | 3.308  | 3.31   | 3.312  | 3.012  | 100.0%  | 10    |
    | nova.attach_volume     | 4.043  | 5.478  | 7.465  | 8.181  | 8.896  | 5.734  | 100.0%  | 10    |
    | nova.detach_volume     | 3.111  | 3.712  | 4.231  | 4.297  | 4.362  | 3.748  | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.272  | 2.63   | 2.889  | 3.032  | 3.174  | 2.679  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.594  | 2.64   | 3.158  | 3.173  | 3.187  | 2.251  | 100.0%  | 10    |
    | total                  | 18.408 | 23.294 | 24.568 | 24.632 | 24.697 | 22.576 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 68.1245191097
    Full duration: 178.916586161



    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.136  | 3.923  | 4.27   | 4.334  | 4.398  | 3.903  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.708  | 2.894  | 3.269  | 3.309  | 3.348  | 2.997  | 100.0%  | 10    |
    | nova.attach_volume     | 3.853  | 5.659  | 9.176  | 9.424  | 9.673  | 6.046  | 100.0%  | 10    |
    | nova.detach_volume     | 3.349  | 3.857  | 4.334  | 4.582  | 4.829  | 3.88   | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.261  | 2.578  | 3.148  | 3.183  | 3.219  | 2.687  | 100.0%  | 10    |
    | cinder.delete_volume   | 2.584  | 2.856  | 3.08   | 3.208  | 3.335  | 2.877  | 100.0%  | 10    |
    | total                  | 21.769 | 23.113 | 27.189 | 27.9   | 28.611 | 24.037 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 69.8956279755
    Full duration: 185.589872122



    run_rally - INFO - Test scenario: "cinder" OK.

    run_rally - INFO - Starting test scenario "heat" ...
    run_rally - INFO -
     Preparing input task
     Task  6323c0be-a020-4b31-99f0-846288593cf5: started
    Task 6323c0be-a020-4b31-99f0-846288593cf5: finished

    test scenario HeatStacks.create_suspend_resume_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action             | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack  | 3.897 | 4.064  | 4.38   | 4.573  | 4.766  | 4.148 | 100.0%  | 10    |
    | heat.suspend_stack | 0.856 | 1.754  | 2.035  | 2.047  | 2.058  | 1.584 | 100.0%  | 10    |
    | heat.resume_stack  | 1.455 | 1.659  | 1.714  | 1.716  | 1.718  | 1.62  | 100.0%  | 10    |
    | heat.delete_stack  | 1.394 | 1.581  | 2.739  | 2.752  | 2.765  | 1.784 | 100.0%  | 10    |
    | total              | 8.071 | 9.183  | 10.285 | 10.314 | 10.344 | 9.135 | 100.0%  | 10    |
    +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 27.614921093
    Full duration: 38.014703989



    test scenario HeatStacks.create_and_delete_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 4.032 | 4.108  | 4.322  | 4.37   | 4.419 | 4.169 | 100.0%  | 10    |
    | heat.delete_stack | 1.408 | 1.463  | 1.821  | 2.204  | 2.588 | 1.599 | 100.0%  | 10    |
    | total             | 5.497 | 5.706  | 5.963  | 6.33   | 6.698 | 5.768 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 17.1844079494
    Full duration: 27.193780899



    test scenario HeatStacks.create_and_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 22.283 | 23.81  | 24.26  | 24.642 | 25.023 | 23.576 | 100.0%  | 10    |
    | heat.delete_stack | 10.675 | 11.83  | 13.071 | 13.072 | 13.073 | 12.167 | 100.0%  | 10    |
    | total             | 33.542 | 35.738 | 36.805 | 36.843 | 36.881 | 35.743 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 107.773921967
    Full duration: 118.200341225



    test scenario HeatStacks.create_and_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack | 18.184 | 20.407 | 21.635 | 21.85  | 22.065 | 20.2  | 100.0%  | 10    |
    | heat.delete_stack | 10.601 | 10.722 | 11.882 | 11.945 | 12.008 | 11.03 | 100.0%  | 10    |
    | total             | 28.903 | 31.02  | 33.025 | 33.24  | 33.455 | 31.23 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 92.4247808456
    Full duration: 102.624263048



    test scenario HeatStacks.list_stacks_and_resources
    +------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                         |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.list_stacks                | 0.493 | 0.534  | 0.591  | 0.604  | 0.617 | 0.542 | 100.0%  | 10    |
    | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0   | 0.0   | 100.0%  | 10    |
    | total                           | 0.493 | 0.534  | 0.592  | 0.604  | 0.617 | 0.542 | 100.0%  | 10    |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.70831894875
    Full duration: 10.6722428799



    test scenario HeatStacks.create_update_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 4.142 | 4.331  | 4.481  | 4.527  | 4.573  | 4.327  | 100.0%  | 10    |
    | heat.update_stack | 3.575 | 3.673  | 3.746  | 3.752  | 3.758  | 3.674  | 100.0%  | 10    |
    | heat.delete_stack | 1.9   | 2.609  | 2.795  | 2.836  | 2.877  | 2.6    | 100.0%  | 10    |
    | total             | 9.714 | 10.635 | 10.858 | 10.879 | 10.899 | 10.601 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 32.1056320667
    Full duration: 42.6386361122



    test scenario HeatStacks.create_update_delete_stack
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack | 4.12  | 4.273  | 4.323  | 4.33   | 4.336  | 4.247 | 100.0%  | 10    |
    | heat.update_stack | 3.504 | 3.594  | 3.722  | 3.741  | 3.76   | 3.615 | 100.0%  | 10    |
    | heat.delete_stack | 1.391 | 1.433  | 1.71   | 2.139  | 2.568  | 1.584 | 100.0%  | 10    |
    | total             | 9.04  | 9.38   | 9.599  | 10.09  | 10.581 | 9.447 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 29.2272830009
    Full duration: 40.1677620411



    test scenario HeatStacks.create_update_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 3.97   | 4.292  | 4.415  | 4.448  | 4.481  | 4.271  | 100.0%  | 10    |
    | heat.update_stack | 5.842  | 5.898  | 5.997  | 6.123  | 6.248  | 5.932  | 100.0%  | 10    |
    | heat.delete_stack | 2.495  | 2.556  | 3.706  | 3.713  | 3.721  | 2.769  | 100.0%  | 10    |
    | total             | 12.606 | 12.776 | 13.842 | 13.936 | 14.029 | 12.972 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 39.4572560787
    Full duration: 50.1925730705



    test scenario HeatStacks.create_update_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+--------+--------+--------+--------+-------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max   | avg    | success | count |
    +-------------------+--------+--------+--------+--------+-------+--------+---------+-------+
    | heat.create_stack | 4.629  | 5.407  | 5.516  | 5.7    | 5.884 | 5.364  | 100.0%  | 10    |
    | heat.update_stack | 8.444  | 9.309  | 9.353  | 9.359  | 9.365 | 9.16   | 100.0%  | 10    |
    | heat.delete_stack | 3.645  | 3.715  | 3.749  | 3.76   | 3.771 | 3.715  | 100.0%  | 10    |
    | total             | 17.585 | 18.448 | 18.542 | 18.731 | 18.92 | 18.239 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+-------+--------+---------+-------+
    Load duration: 54.5839819908
    Full duration: 66.1476221085



    test scenario HeatStacks.create_update_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 4.153  | 4.42   | 4.537  | 4.626  | 4.716  | 4.414  | 100.0%  | 10    |
    | heat.update_stack | 5.756  | 5.867  | 5.968  | 5.986  | 6.003  | 5.879  | 100.0%  | 10    |
    | heat.delete_stack | 2.537  | 2.569  | 3.682  | 3.771  | 3.859  | 2.812  | 100.0%  | 10    |
    | total             | 12.735 | 12.934 | 13.781 | 13.841 | 13.901 | 13.105 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 39.6327600479
    Full duration: 51.5351819992



    test scenario HeatStacks.create_update_delete_stack
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack | 4.216 | 4.41   | 4.524  | 4.563  | 4.602  | 4.398 | 100.0%  | 10    |
    | heat.update_stack | 3.532 | 3.608  | 3.773  | 3.784  | 3.795  | 3.634 | 100.0%  | 10    |
    | heat.delete_stack | 1.377 | 1.48   | 2.549  | 2.553  | 2.557  | 1.868 | 100.0%  | 10    |
    | total             | 9.266 | 9.676  | 10.603 | 10.665 | 10.728 | 9.9   | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 29.3563029766
    Full duration: 41.178768158



    test scenario HeatStacks.create_and_list_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 4.154 | 4.25   | 4.32   | 4.358  | 4.396 | 4.255 | 100.0%  | 10    |
    | heat.list_stacks  | 0.074 | 0.097  | 0.126  | 0.128  | 0.13  | 0.104 | 100.0%  | 10    |
    | total             | 4.279 | 4.357  | 4.412  | 4.448  | 4.484 | 4.359 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 13.1276688576
    Full duration: 29.3930869102



    test scenario HeatStacks.create_check_delete_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 4.092 | 4.317  | 4.556  | 4.566  | 4.577 | 4.328 | 100.0%  | 10    |
    | heat.check_stack  | 1.476 | 1.524  | 1.598  | 1.722  | 1.845 | 1.56  | 100.0%  | 10    |
    | heat.delete_stack | 1.38  | 2.515  | 2.587  | 2.689  | 2.791 | 2.103 | 100.0%  | 10    |
    | total             | 7.059 | 8.243  | 8.619  | 8.666  | 8.713 | 7.99  | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 24.3825399876
    Full duration: 35.8954949379



    run_rally - INFO - Test scenario: "heat" OK.

    run_rally - INFO - Starting test scenario "keystone" ...
    run_rally - INFO -
     Preparing input task
     Task  01416586-e6ad-4e3a-a1a2-6fc6305bbaea: started
    Task 01416586-e6ad-4e3a-a1a2-6fc6305bbaea: finished

    test scenario KeystoneBasic.create_tenant_with_users
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.27  | 0.298  | 0.409  | 0.435  | 0.46  | 0.321 | 100.0%  | 10    |
    | keystone.create_users  | 1.62  | 1.702  | 1.784  | 1.8    | 1.816 | 1.71  | 100.0%  | 10    |
    | total                  | 1.925 | 2.027  | 2.126  | 2.152  | 2.178 | 2.031 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 6.16570997238
    Full duration: 22.7167549133



    test scenario KeystoneBasic.create_add_and_list_user_roles
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.266 | 0.303  | 0.411  | 0.414  | 0.418 | 0.326 | 100.0%  | 10    |
    | keystone.add_role    | 0.268 | 0.295  | 0.314  | 0.344  | 0.373 | 0.3   | 100.0%  | 10    |
    | keystone.list_roles  | 0.148 | 0.159  | 0.168  | 0.169  | 0.17  | 0.158 | 100.0%  | 10    |
    | total                | 0.695 | 0.767  | 0.865  | 0.868  | 0.872 | 0.784 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.35486006737
    Full duration: 15.306978941



    test scenario KeystoneBasic.add_and_remove_user_role
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.29  | 0.387  | 0.421  | 0.453  | 0.485 | 0.366 | 100.0%  | 10    |
    | keystone.add_role    | 0.258 | 0.281  | 0.337  | 0.355  | 0.373 | 0.294 | 100.0%  | 10    |
    | keystone.remove_role | 0.164 | 0.171  | 0.231  | 0.302  | 0.373 | 0.197 | 100.0%  | 10    |
    | total                | 0.747 | 0.827  | 0.964  | 1.078  | 1.191 | 0.857 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.82508516312
    Full duration: 16.1954729557



    test scenario KeystoneBasic.create_update_and_delete_tenant
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.258 | 0.319  | 0.527  | 0.533  | 0.538 | 0.37  | 100.0%  | 10    |
    | keystone.update_tenant | 0.138 | 0.159  | 0.258  | 0.263  | 0.269 | 0.18  | 100.0%  | 10    |
    | keystone.delete_tenant | 0.319 | 0.34   | 0.454  | 0.455  | 0.455 | 0.371 | 100.0%  | 10    |
    | total                  | 0.776 | 0.89   | 1.119  | 1.121  | 1.124 | 0.922 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.63998699188
    Full duration: 14.1927289963



    test scenario KeystoneBasic.create_and_delete_service
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_service | 0.278 | 0.299  | 0.315  | 0.315  | 0.316 | 0.3   | 100.0%  | 10    |
    | keystone.delete_service | 0.15  | 0.17   | 0.241  | 0.247  | 0.253 | 0.182 | 100.0%  | 10    |
    | total                   | 0.434 | 0.481  | 0.533  | 0.538  | 0.544 | 0.482 | 100.0%  | 10    |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.47481298447
    Full duration: 13.4397730827



    test scenario KeystoneBasic.create_tenant
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.301 | 0.315  | 0.339  | 0.384  | 0.429 | 0.325 | 100.0%  | 10    |
    | total                  | 0.301 | 0.316  | 0.339  | 0.384  | 0.429 | 0.325 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.985784053802
    Full duration: 9.20213198662



    test scenario KeystoneBasic.create_user
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +----------------------+------+--------+--------+--------+-------+------+---------+-------+
    | action               | min  | median | 90%ile | 95%ile | max   | avg  | success | count |
    +----------------------+------+--------+--------+--------+-------+------+---------+-------+
    | keystone.create_user | 0.31 | 0.315  | 0.333  | 0.333  | 0.333 | 0.32 | 100.0%  | 10    |
    | total                | 0.31 | 0.315  | 0.333  | 0.333  | 0.333 | 0.32 | 100.0%  | 10    |
    +----------------------+------+--------+--------+--------+-------+------+---------+-------+
    Load duration: 1.00818705559
    Full duration: 9.22635006905



    test scenario KeystoneBasic.create_and_list_tenants
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.287 | 0.304  | 0.325  | 0.327  | 0.329 | 0.306 | 100.0%  | 10    |
    | keystone.list_tenants  | 0.127 | 0.136  | 0.153  | 0.157  | 0.16  | 0.139 | 100.0%  | 10    |
    | total                  | 0.42  | 0.445  | 0.462  | 0.466  | 0.469 | 0.445 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.36337804794
    Full duration: 14.8872029781



    test scenario KeystoneBasic.create_and_delete_role
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.282 | 0.386  | 0.408  | 0.422  | 0.436 | 0.365 | 100.0%  | 10    |
    | keystone.delete_role | 0.268 | 0.3    | 0.401  | 0.491  | 0.581 | 0.334 | 100.0%  | 10    |
    | total                | 0.575 | 0.677  | 0.804  | 0.911  | 1.018 | 0.699 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.04137206078
    Full duration: 14.1024041176



    test scenario KeystoneBasic.get_entities
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.286 | 0.308  | 0.319  | 0.328  | 0.336 | 0.307 | 100.0%  | 10    |
    | keystone.create_user   | 0.143 | 0.156  | 0.164  | 0.167  | 0.17  | 0.157 | 100.0%  | 10    |
    | keystone.create_role   | 0.135 | 0.143  | 0.175  | 0.19   | 0.204 | 0.151 | 100.0%  | 10    |
    | keystone.get_tenant    | 0.117 | 0.13   | 0.135  | 0.136  | 0.138 | 0.129 | 100.0%  | 10    |
    | keystone.get_user      | 0.127 | 0.15   | 0.222  | 0.227  | 0.232 | 0.162 | 100.0%  | 10    |
    | keystone.get_role      | 0.12  | 0.132  | 0.144  | 0.154  | 0.164 | 0.134 | 100.0%  | 10    |
    | keystone.service_list  | 0.125 | 0.138  | 0.243  | 0.244  | 0.245 | 0.164 | 100.0%  | 10    |
    | keystone.get_service   | 0.124 | 0.133  | 0.153  | 0.194  | 0.235 | 0.143 | 100.0%  | 10    |
    | total                  | 1.279 | 1.333  | 1.411  | 1.47   | 1.528 | 1.345 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.00930905342
    Full duration: 20.4269800186



    test scenario KeystoneBasic.create_and_list_users
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_user | 0.295 | 0.304  | 0.332  | 0.342  | 0.351 | 0.311 | 100.0%  | 10    |
    | keystone.list_users  | 0.127 | 0.146  | 0.162  | 0.201  | 0.24  | 0.151 | 100.0%  | 10    |
    | total                | 0.422 | 0.458  | 0.506  | 0.523  | 0.539 | 0.462 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.42111587524
    Full duration: 9.87036585808



    run_rally - INFO - Test scenario: "keystone" OK.

    run_rally - INFO - Starting test scenario "neutron" ...
    run_rally - INFO -
     Preparing input task
     Task  31a75089-836c-4dd2-bea5-146049608ff3: started
    Task 31a75089-836c-4dd2-bea5-146049608ff3: finished

    test scenario NeutronNetworks.create_and_delete_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.763 | 0.911  | 1.019  | 1.048  | 1.078 | 0.909 | 100.0%  | 10    |
    | neutron.delete_port | 0.237 | 0.633  | 0.682  | 0.717  | 0.752 | 0.534 | 100.0%  | 10    |
    | total               | 1.07  | 1.489  | 1.683  | 1.704  | 1.726 | 1.443 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.20432686806
    Full duration: 54.8132340908



    test scenario NeutronNetworks.create_and_list_routers
    +---------------------------------------------------------------------------------------------------+
    |                                       Response Times (sec)                                        |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet        | 0.762 | 0.836  | 0.949  | 0.98   | 1.011 | 0.863 | 100.0%  | 10    |
    | neutron.create_router        | 0.066 | 0.493  | 0.686  | 0.691  | 0.695 | 0.459 | 100.0%  | 10    |
    | neutron.add_interface_router | 0.262 | 0.695  | 0.795  | 0.844  | 0.892 | 0.637 | 100.0%  | 10    |
    | neutron.list_routers         | 0.039 | 0.407  | 0.441  | 0.452  | 0.462 | 0.308 | 100.0%  | 10    |
    | total                        | 1.54  | 2.352  | 2.744  | 2.824  | 2.904 | 2.268 | 100.0%  | 10    |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 7.36094808578
    Full duration: 61.3011310101



    test scenario NeutronNetworks.create_and_delete_routers
    +------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                         |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet           | 0.79  | 0.836  | 0.945  | 1.009  | 1.072 | 0.868 | 100.0%  | 10    |
    | neutron.create_router           | 0.074 | 0.436  | 0.479  | 0.499  | 0.518 | 0.377 | 100.0%  | 10    |
    | neutron.add_interface_router    | 0.284 | 0.545  | 0.739  | 0.812  | 0.886 | 0.527 | 100.0%  | 10    |
    | neutron.remove_interface_router | 0.221 | 0.615  | 0.709  | 0.724  | 0.739 | 0.518 | 100.0%  | 10    |
    | neutron.delete_router           | 0.187 | 0.566  | 0.709  | 0.751  | 0.793 | 0.508 | 100.0%  | 10    |
    | total                           | 2.124 | 2.811  | 3.347  | 3.379  | 3.412 | 2.799 | 100.0%  | 10    |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 8.68784189224
    Full duration: 59.8806409836



    test scenario NeutronNetworks.create_and_list_ports
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg  | success | count |
    +---------------------+-------+--------+--------+--------+-------+------+---------+-------+
    | neutron.create_port | 0.777 | 0.895  | 0.981  | 1.01   | 1.039 | 0.89 | 100.0%  | 10    |
    | neutron.list_ports  | 0.525 | 0.678  | 0.726  | 0.735  | 0.743 | 0.65 | 100.0%  | 10    |
    | total               | 1.351 | 1.564  | 1.694  | 1.729  | 1.764 | 1.54 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+------+---------+-------+
    Load duration: 4.66481399536
    Full duration: 56.677120924



    test scenario NeutronNetworks.create_and_delete_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.785 | 0.926  | 1.065  | 1.065  | 1.065 | 0.914 | 100.0%  | 10    |
    | neutron.delete_subnet | 0.193 | 0.762  | 0.952  | 1.035  | 1.117 | 0.745 | 100.0%  | 10    |
    | total                 | 1.258 | 1.702  | 1.876  | 1.903  | 1.929 | 1.659 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 5.09031915665
    Full duration: 56.7336909771



    test scenario NeutronNetworks.create_and_delete_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.614 | 0.708  | 0.774  | 0.81   | 0.847 | 0.712 | 100.0%  | 10    |
    | neutron.delete_network | 0.144 | 0.554  | 0.592  | 0.645  | 0.698 | 0.489 | 100.0%  | 10    |
    | total                  | 0.809 | 1.248  | 1.41   | 1.418  | 1.427 | 1.202 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.66986989975
    Full duration: 34.80159688



    test scenario NeutronNetworks.create_and_list_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.627 | 0.707  | 0.85   | 0.851  | 0.853 | 0.719 | 100.0%  | 10    |
    | neutron.list_networks  | 0.059 | 0.439  | 0.513  | 0.515  | 0.518 | 0.413 | 100.0%  | 10    |
    | total                  | 0.909 | 1.126  | 1.242  | 1.306  | 1.371 | 1.132 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.38921308517
    Full duration: 36.8345379829



    test scenario NeutronNetworks.create_and_update_routers
    +---------------------------------------------------------------------------------------------------+
    |                                       Response Times (sec)                                        |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet        | 0.751 | 0.824  | 0.876  | 0.921  | 0.967 | 0.832 | 100.0%  | 10    |
    | neutron.create_router        | 0.431 | 0.473  | 0.541  | 0.577  | 0.613 | 0.489 | 100.0%  | 10    |
    | neutron.add_interface_router | 0.301 | 0.711  | 0.928  | 1.08   | 1.231 | 0.684 | 100.0%  | 10    |
    | neutron.update_router        | 0.48  | 0.514  | 0.703  | 0.74   | 0.778 | 0.579 | 100.0%  | 10    |
    | total                        | 2.062 | 2.629  | 2.871  | 3.084  | 3.298 | 2.584 | 100.0%  | 10    |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 7.65487504005
    Full duration: 63.1229610443



    test scenario NeutronNetworks.create_and_update_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.656 | 0.719  | 1.152  | 1.152  | 1.153 | 0.796 | 100.0%  | 10    |
    | neutron.update_network | 0.136 | 0.33   | 0.656  | 0.684  | 0.711 | 0.37  | 100.0%  | 10    |
    | total                  | 0.793 | 1.067  | 1.71   | 1.757  | 1.803 | 1.166 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.25723409653
    Full duration: 35.7245519161



    test scenario NeutronNetworks.create_and_update_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.757 | 0.871  | 0.937  | 0.949  | 0.961 | 0.872 | 100.0%  | 10    |
    | neutron.update_port | 0.152 | 0.553  | 0.69   | 0.695  | 0.7   | 0.449 | 100.0%  | 10    |
    | total               | 1.013 | 1.374  | 1.562  | 1.591  | 1.621 | 1.322 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.26963686943
    Full duration: 56.3142960072



    test scenario NeutronNetworks.create_and_list_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.759 | 0.838  | 0.884  | 0.921  | 0.959 | 0.833 | 100.0%  | 10    |
    | neutron.list_subnets  | 0.419 | 0.437  | 0.474  | 0.504  | 0.535 | 0.447 | 100.0%  | 10    |
    | total                 | 1.205 | 1.29   | 1.325  | 1.352  | 1.379 | 1.281 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.90167307854
    Full duration: 56.5125339031



    test scenario NeutronNetworks.create_and_update_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.739 | 0.86   | 0.894  | 0.899  | 0.904 | 0.847 | 100.0%  | 10    |
    | neutron.update_subnet | 0.215 | 0.626  | 0.747  | 0.751  | 0.754 | 0.619 | 100.0%  | 10    |
    | total                 | 0.992 | 1.503  | 1.597  | 1.604  | 1.611 | 1.466 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.40182685852
    Full duration: 57.6830070019



    run_rally - INFO - Test scenario: "neutron" OK.

    run_rally - INFO - Starting test scenario "nova" ...
    run_rally - INFO -
     Preparing input task
     Task  584052d3-7a9b-44cb-b72b-0fa69c80ff0f: started
    Task 584052d3-7a9b-44cb-b72b-0fa69c80ff0f: finished

    test scenario NovaKeypair.create_and_delete_keypair
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | nova.create_keypair | 0.784 | 0.836  | 1.474  | 1.484  | 1.495 | 0.974 | 100.0%  | 10    |
    | nova.delete_keypair | 0.034 | 0.05   | 0.055  | 0.057  | 0.058 | 0.047 | 100.0%  | 10    |
    | total               | 0.832 | 0.883  | 1.529  | 1.541  | 1.553 | 1.022 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.34695100784
    Full duration: 45.7756779194



    test scenario NovaServers.snapshot_server
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server       | 7.554  | 10.346 | 11.835 | 11.965 | 12.095 | 10.244 | 100.0%  | 10    |
    | nova.create_image      | 11.631 | 12.185 | 12.844 | 13.707 | 14.57  | 12.355 | 100.0%  | 10    |
    | nova.delete_server     | 2.863  | 3.258  | 3.364  | 3.387  | 3.409  | 3.184  | 100.0%  | 10    |
    | nova.boot_server (2)   | 7.672  | 8.531  | 9.58   | 9.806  | 10.032 | 8.647  | 100.0%  | 10    |
    | nova.delete_server (2) | 2.536  | 2.983  | 3.338  | 3.367  | 3.396  | 3.003  | 100.0%  | 10    |
    | nova.delete_image      | 2.294  | 3.138  | 3.917  | 3.949  | 3.981  | 3.199  | 100.0%  | 10    |
    | total                  | 37.226 | 39.77  | 43.868 | 44.502 | 45.136 | 40.632 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 120.862003088
    Full duration: 196.742653131



    test scenario NovaKeypair.boot_and_delete_server_with_keypair
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_keypair | 0.722  | 0.911  | 1.196  | 1.303  | 1.41   | 0.932  | 100.0%  | 10    |
    | nova.boot_server    | 8.584  | 9.058  | 10.234 | 10.397 | 10.559 | 9.363  | 100.0%  | 10    |
    | nova.delete_server  | 2.535  | 3.3    | 3.362  | 3.407  | 3.453  | 3.174  | 100.0%  | 10    |
    | nova.delete_keypair | 0.037  | 0.048  | 0.055  | 0.057  | 0.059  | 0.049  | 100.0%  | 10    |
    | total               | 12.316 | 13.426 | 14.867 | 14.936 | 15.006 | 13.518 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 39.9865550995
    Full duration: 111.508669853



    test scenario NovaKeypair.create_and_list_keypairs
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | nova.create_keypair | 0.648 | 0.815  | 1.082  | 1.098  | 1.113 | 0.837 | 100.0%  | 10    |
    | nova.list_keypairs  | 0.019 | 0.028  | 0.042  | 0.042  | 0.042 | 0.03  | 100.0%  | 10    |
    | total               | 0.674 | 0.84   | 1.113  | 1.126  | 1.139 | 0.868 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.55701994896
    Full duration: 46.8838369846



    test scenario NovaServers.list_servers
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | nova.list_servers | 1.225 | 1.717  | 2.028  | 2.148  | 2.269 | 1.703 | 100.0%  | 10    |
    | total             | 1.225 | 1.717  | 2.028  | 2.149  | 2.269 | 1.703 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 5.18592405319
    Full duration: 131.096873999



    test scenario NovaServers.resize_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 7.681  | 9.106  | 9.667  | 9.855  | 10.043 | 8.967  | 100.0%  | 10    |
    | nova.resize         | 41.039 | 42.444 | 47.666 | 47.89  | 48.113 | 43.647 | 100.0%  | 10    |
    | nova.resize_confirm | 3.05   | 3.839  | 5.756  | 5.796  | 5.836  | 4.129  | 100.0%  | 10    |
    | nova.delete_server  | 2.538  | 2.977  | 3.37   | 3.436  | 3.502  | 2.99   | 100.0%  | 10    |
    | total               | 56.14  | 58.909 | 63.601 | 64.059 | 64.517 | 59.734 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 175.1216681
    Full duration: 218.552350998



    test scenario NovaServers.boot_server_from_volume_and_delete
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 10.051 | 10.651 | 11.762 | 11.824 | 11.885 | 10.8   | 100.0%  | 10    |
    | nova.boot_server     | 9.377  | 9.86   | 11.429 | 11.996 | 12.563 | 10.33  | 100.0%  | 10    |
    | nova.delete_server   | 3.706  | 5.644  | 6.192  | 6.201  | 6.209  | 5.374  | 100.0%  | 10    |
    | total                | 23.576 | 26.289 | 28.117 | 28.514 | 28.911 | 26.505 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 78.3103020191
    Full duration: 163.452836037



    test scenario NovaServers.boot_and_migrate_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 8.257  | 9.346  | 10.61  | 10.662 | 10.713 | 9.544  | 100.0%  | 10    |
    | nova.stop_server    | 4.295  | 6.497  | 7.089  | 7.118  | 7.147  | 6.056  | 100.0%  | 10    |
    | nova.migrate        | 9.675  | 12.304 | 13.12  | 13.229 | 13.338 | 12.161 | 100.0%  | 10    |
    | nova.resize_confirm | 3.122  | 3.507  | 4.272  | 4.364  | 4.457  | 3.653  | 100.0%  | 10    |
    | nova.delete_server  | 2.554  | 3.188  | 3.429  | 3.496  | 3.562  | 3.139  | 100.0%  | 10    |
    | total               | 32.033 | 35.063 | 36.096 | 36.58  | 37.064 | 34.553 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 105.193811893
    Full duration: 148.141517878



    test scenario NovaServers.boot_and_delete_server
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action             | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server   | 8.014  | 9.185  | 9.831  | 10.523 | 11.215 | 9.243  | 100.0%  | 10    |
    | nova.delete_server | 2.908  | 3.295  | 3.466  | 3.472  | 3.478  | 3.254  | 100.0%  | 10    |
    | total              | 11.295 | 12.557 | 13.028 | 13.839 | 14.649 | 12.498 | 100.0%  | 10    |
    +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 36.6073288918
    Full duration: 109.97128582



    test scenario NovaServers.boot_and_rebuild_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 7.698  | 9.483  | 10.427 | 10.794 | 11.162 | 9.37   | 100.0%  | 10    |
    | nova.rebuild_server | 8.598  | 9.448  | 10.319 | 10.378 | 10.438 | 9.551  | 100.0%  | 10    |
    | nova.delete_server  | 2.858  | 3.099  | 3.428  | 3.623  | 3.817  | 3.161  | 100.0%  | 10    |
    | total               | 20.044 | 22.42  | 23.365 | 23.559 | 23.752 | 22.083 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 64.9432969093
    Full duration: 139.465661049



    test scenario NovaSecGroup.create_and_list_secgroups
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups | 4.683  | 5.344  | 5.852  | 5.859  | 5.866  | 5.356  | 100.0%  | 10    |
    | nova.create_100_rules          | 42.414 | 45.678 | 47.163 | 47.368 | 47.574 | 45.254 | 100.0%  | 10    |
    | nova.list_security_groups      | 0.175  | 0.212  | 0.354  | 0.608  | 0.863  | 0.283  | 100.0%  | 10    |
    | total                          | 47.348 | 51.421 | 52.56  | 52.638 | 52.716 | 50.893 | 100.0%  | 10    |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 151.312942028
    Full duration: 221.151799202



    test scenario NovaSecGroup.create_and_delete_secgroups
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups | 4.207  | 5.153  | 5.865  | 6.016  | 6.167  | 5.223  | 100.0%  | 10    |
    | nova.create_100_rules          | 44.426 | 45.496 | 46.391 | 46.57  | 46.749 | 45.514 | 100.0%  | 10    |
    | nova.delete_10_security_groups | 1.719  | 2.314  | 3.033  | 3.409  | 3.786  | 2.461  | 100.0%  | 10    |
    | total                          | 51.911 | 53.27  | 54.098 | 54.11  | 54.121 | 53.199 | 100.0%  | 10    |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 158.767210007
    Full duration: 204.404190063



    test scenario NovaServers.boot_and_bounce_server
    +-------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                       |
    +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                  | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server        | 8.232  | 10.238 | 11.257 | 11.387 | 11.516 | 9.989  | 100.0%  | 10    |
    | nova.reboot_server      | 5.292  | 6.196  | 8.351  | 8.675  | 8.999  | 6.856  | 100.0%  | 10    |
    | nova.soft_reboot_server | 7.958  | 8.738  | 8.914  | 8.918  | 8.923  | 8.624  | 100.0%  | 10    |
    | nova.stop_server        | 3.374  | 6.332  | 7.13   | 7.453  | 7.776  | 5.867  | 100.0%  | 10    |
    | nova.start_server       | 2.904  | 4.376  | 4.992  | 5.042  | 5.093  | 4.338  | 100.0%  | 10    |
    | nova.rescue_server      | 7.695  | 9.49   | 10.886 | 11.148 | 11.409 | 9.448  | 100.0%  | 10    |
    | nova.unrescue_server    | 5.081  | 5.557  | 7.819  | 8.065  | 8.31   | 5.985  | 100.0%  | 10    |
    | nova.delete_server      | 2.544  | 3.077  | 3.429  | 3.523  | 3.617  | 3.093  | 100.0%  | 10    |
    | total                   | 49.625 | 55.207 | 55.707 | 56.454 | 57.202 | 54.222 | 100.0%  | 10    |
    +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 163.818984032
    Full duration: 233.215523958



    test scenario NovaServers.boot_server
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action           | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | nova.boot_server | 8.48  | 8.958  | 10.243 | 10.531 | 10.819 | 9.243 | 100.0%  | 10    |
    | total            | 8.481 | 8.958  | 10.244 | 10.531 | 10.819 | 9.244 | 100.0%  | 10    |
    +------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 27.3609120846
    Full duration: 84.3593919277



    test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
    +-----------------------------------------------------------------------------------------------------------+
    |                                           Response Times (sec)                                            |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups    | 4.247  | 5.184  | 5.369  | 5.396  | 5.424  | 5.095  | 100.0%  | 10    |
    | nova.create_100_rules             | 40.661 | 43.059 | 43.938 | 44.458 | 44.978 | 42.794 | 100.0%  | 10    |
    | nova.boot_server                  | 6.947  | 8.26   | 9.169  | 9.358  | 9.548  | 8.098  | 100.0%  | 10    |
    | nova.get_attached_security_groups | 0.225  | 0.263  | 0.273  | 0.293  | 0.313  | 0.26   | 100.0%  | 10    |
    | nova.delete_server                | 2.528  | 2.586  | 2.843  | 2.904  | 2.965  | 2.638  | 100.0%  | 10    |
    | nova.delete_10_security_groups    | 1.791  | 2.426  | 2.99   | 3.057  | 3.123  | 2.475  | 100.0%  | 10    |
    | total                             | 59.505 | 61.408 | 62.425 | 63.244 | 64.063 | 61.363 | 100.0%  | 10    |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 184.570534945
    Full duration: 253.34465313



    test scenario NovaServers.pause_and_unpause_server
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +---------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
    +---------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    | nova.boot_server    | 7.448  | 9.26   | 10.374 | 10.502 | 10.629 | 9.397 | 100.0%  | 10    |
    | nova.pause_server   | 2.424  | 3.161  | 3.286  | 3.379  | 3.472  | 3.026 | 100.0%  | 10    |
    | nova.unpause_server | 2.773  | 3.096  | 3.242  | 3.272  | 3.303  | 3.035 | 100.0%  | 10    |
    | nova.delete_server  | 2.878  | 3.224  | 3.526  | 3.553  | 3.58   | 3.191 | 100.0%  | 10    |
    | total               | 15.943 | 18.76  | 19.747 | 19.77  | 19.793 | 18.65 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 56.3870060444
    Full duration: 124.540560007



    test scenario NovaServers.boot_server_from_volume
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 9.453  | 10.083 | 10.563 | 10.801 | 11.039 | 10.104 | 100.0%  | 10    |
    | nova.boot_server     | 9.213  | 10.415 | 10.885 | 11.116 | 11.346 | 10.301 | 100.0%  | 10    |
    | total                | 18.667 | 20.779 | 21.44  | 21.628 | 21.816 | 20.405 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 60.3854188919
    Full duration: 124.319462061



    test scenario NovaServers.boot_and_list_server
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server  | 8.037 | 9.396  | 10.043 | 10.516 | 10.989 | 9.351  | 100.0%  | 10    |
    | nova.list_servers | 0.654 | 1.026  | 1.113  | 1.156  | 1.198  | 0.988  | 100.0%  | 10    |
    | total             | 8.984 | 10.311 | 11.119 | 11.575 | 12.032 | 10.339 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 31.5458390713
    Full duration: 114.252287149



    run_rally - INFO - Test scenario: "nova" OK.

    run_rally - INFO - Starting test scenario "quotas" ...
    run_rally - INFO -
     Preparing input task
     Task  5d3885f2-1759-48e8-9284-c14f3492c4f3: started
    Task 5d3885f2-1759-48e8-9284-c14f3492c4f3: finished

    test scenario Quotas.cinder_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 1.126 | 1.235  | 1.607  | 1.612  | 1.618 | 1.297 | 100.0%  | 10    |
    | total                | 1.126 | 1.235  | 1.607  | 1.613  | 1.618 | 1.297 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.74135613441
    Full duration: 16.1623110771



    test scenario Quotas.neutron_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.407 | 0.429  | 0.526  | 0.528  | 0.531 | 0.447 | 100.0%  | 10    |
    | total                | 0.552 | 0.586  | 0.666  | 0.671  | 0.676 | 0.599 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.82448792458
    Full duration: 13.357311964



    test scenario Quotas.cinder_update_and_delete
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 1.093 | 1.146  | 1.27   | 1.276  | 1.282 | 1.177 | 100.0%  | 10    |
    | quotas.delete_quotas | 0.536 | 0.907  | 0.975  | 1.01   | 1.046 | 0.862 | 100.0%  | 10    |
    | total                | 1.67  | 2.089  | 2.177  | 2.184  | 2.192 | 2.039 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 6.09977889061
    Full duration: 18.3411080837



    test scenario Quotas.nova_update_and_delete
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.58  | 0.636  | 0.718  | 0.764  | 0.81  | 0.652 | 100.0%  | 10    |
    | quotas.delete_quotas | 0.018 | 0.026  | 0.035  | 0.039  | 0.043 | 0.028 | 100.0%  | 10    |
    | total                | 0.616 | 0.657  | 0.741  | 0.793  | 0.844 | 0.68  | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.00378704071
    Full duration: 13.8784749508



    test scenario Quotas.nova_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.583 | 0.637  | 0.914  | 1.049  | 1.185 | 0.713 | 100.0%  | 10    |
    | total                | 0.583 | 0.637  | 0.914  | 1.05   | 1.186 | 0.713 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.00103402138
    Full duration: 13.8432979584



    run_rally - INFO - Test scenario: "quotas" OK.

    run_rally - INFO - Starting test scenario "requests" ...
    run_rally - INFO -
     Preparing input task
     Task  6e9ed029-0497-4707-a4d4-c83a848e12e4: started
    Task 6e9ed029-0497-4707-a4d4-c83a848e12e4: finished

    test scenario HttpRequests.check_random_request
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | requests.check_request | 0.044 | 0.183  | 0.349  | 0.376  | 0.402 | 0.201 | 100.0%  | 10    |
    | total                  | 0.045 | 0.183  | 0.349  | 0.376  | 0.403 | 0.201 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.716305971146
    Full duration: 5.89718389511



    test scenario HttpRequests.check_request
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | requests.check_request | 0.044 | 0.046  | 0.052  | 0.053  | 0.054 | 0.048 | 100.0%  | 10    |
    | total                  | 0.044 | 0.046  | 0.052  | 0.053  | 0.054 | 0.048 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.182355165482
    Full duration: 5.23191189766



    run_rally - INFO - Test scenario: "requests" OK.

    run_rally - INFO -


                         Rally Summary Report
    +===================+============+===============+===========+
    | Module            | Duration   | nb. Test Run  | Success   |
    +===================+============+===============+===========+
    | authenticate      | 00:58      | 10            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | glance            | 03:31      | 7             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | cinder            | 22:25      | 50            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | heat              | 10:53      | 35            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | keystone          | 02:39      | 29            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | neutron           | 10:30      | 31            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | nova              | 44:31      | 61            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | quotas            | 01:15      | 7             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | requests          | 00:11      | 2             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    +===================+============+===============+===========+
    | TOTAL:            | 01:36:57   | 232           | 100.00%   |
    +===================+============+===============+===========+



SDN Controller
--------------

ONOS
^^^^
::

    FUNCTEST.info: Running ONOS test case...
    FUNCvirNetNB - INFO - Creating component Handle: ONOSrest
    ******************************
     CASE INIT
    ******************************

    ['ONOSrest']

    ******************************
     Result summary for Testcase2
    ******************************

    [2016-02-21 09:55:56.965174] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Network Post
    [2016-02-21 09:55:56.965727] [FUNCvirNetNB] [STEP]  2.1: Generate Post Data
    [2016-02-21 09:55:56.966454] [FUNCvirNetNB] [STEP]  2.2: Post Data via HTTP
    [2016-02-21 09:55:57.006264] [FUNCvirNetNB] [STEP]  2.3: Get Data via HTTP
    [2016-02-21 09:55:57.037745] [FUNCvirNetNB] [STEP]  2.4: Compare Send Id and Get Id

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase3
    ******************************

    [2016-02-21 09:55:57.048240] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Network Update
    [2016-02-21 09:55:57.048783] [FUNCvirNetNB] [STEP]  3.1: Generate Post Data
    [2016-02-21 09:55:57.049571] [FUNCvirNetNB] [STEP]  3.2: Post Data via HTTP
    [2016-02-21 09:55:57.056744] [FUNCvirNetNB] [STEP]  3.3: Update Data via HTTP
    [2016-02-21 09:55:57.064248] [FUNCvirNetNB] [STEP]  3.4: Get Data via HTTP
    [2016-02-21 09:55:57.072845] [FUNCvirNetNB] [STEP]  3.5: Compare Update data.

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase4
    ******************************

    [2016-02-21 09:55:57.084363] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Network Delete
    [2016-02-21 09:55:57.084882] [FUNCvirNetNB] [STEP]  4.1: Generate Post Data
    [2016-02-21 09:55:57.085617] [FUNCvirNetNB] [STEP]  4.2: Post Data via HTTP
    [2016-02-21 09:55:57.093018] [FUNCvirNetNB] [STEP]  4.3: Delete Data via HTTP
    [2016-02-21 09:55:57.099770] [FUNCvirNetNB] [STEP]  4.4: Get Data is NULL

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase5
    ******************************

    [2016-02-21 09:56:02.115745] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Subnet Post
    [2016-02-21 09:56:02.116339] [FUNCvirNetNB] [STEP]  5.1: Generate Post Data
    [2016-02-21 09:56:02.117459] [FUNCvirNetNB] [STEP]  5.2: Post Network Data via HTTP(Post Subnet need post network)
    [2016-02-21 09:56:02.126052] [FUNCvirNetNB] [STEP]  5.3: Post Subnet Data via HTTP
    [2016-02-21 09:56:02.159577] [FUNCvirNetNB] [STEP]  5.4: Get Subnet Data via HTTP
    [2016-02-21 09:56:02.172655] [FUNCvirNetNB] [STEP]  5.5: Compare Post Subnet Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase6
    ******************************

    [2016-02-21 09:56:02.183187] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Subnet Update
    [2016-02-21 09:56:02.183876] [FUNCvirNetNB] [STEP]  6.1: Generate Post Data
    [2016-02-21 09:56:02.184887] [FUNCvirNetNB] [STEP]  6.2: Post Network Data via HTTP(Post Subnet need post network)
    [2016-02-21 09:56:02.192777] [FUNCvirNetNB] [STEP]  6.3: Post Subnet Data via HTTP
    [2016-02-21 09:56:02.201349] [FUNCvirNetNB] [STEP]  6.4: Update Subnet Data via HTTP
    [2016-02-21 09:56:02.209629] [FUNCvirNetNB] [STEP]  6.5: Get Subnet Data via HTTP
    [2016-02-21 09:56:02.216700] [FUNCvirNetNB] [STEP]  6.6: Compare Subnet Data
    [2016-02-21 09:56:02.217492] [FUNCvirNetNB] [STEP]  6.7: Delete Subnet via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase7
    ******************************

    [2016-02-21 09:56:02.227738] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Subnet Delete
    [2016-02-21 09:56:02.228309] [FUNCvirNetNB] [STEP]  7.1: Generate Post Data
    [2016-02-21 09:56:02.229188] [FUNCvirNetNB] [STEP]  7.2: Post Network Data via HTTP(Post Subnet need post network)
    [2016-02-21 09:56:02.237036] [FUNCvirNetNB] [STEP]  7.3: Post Subnet Data via HTTP
    [2016-02-21 09:56:02.245482] [FUNCvirNetNB] [STEP]  7.4: Delete Subnet Data via HTTP
    [2016-02-21 09:56:02.253076] [FUNCvirNetNB] [STEP]  7.5: Get Subnet Data is NULL

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase8
    ******************************

    [2016-02-21 09:56:07.269037] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Port Post
    [2016-02-21 09:56:07.269689] [FUNCvirNetNB] [STEP]  8.1: Generate Post Data
    [2016-02-21 09:56:07.270772] [FUNCvirNetNB] [STEP]  8.2: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:07.279440] [FUNCvirNetNB] [STEP]  8.3: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:07.287800] [FUNCvirNetNB] [STEP]  8.4: Post Port Data via HTTP
    [2016-02-21 09:56:07.296863] [FUNCvirNetNB] [STEP]  8.5: Get Port Data via HTTP
    [2016-02-21 09:56:07.306388] [FUNCvirNetNB] [STEP]  8.6: Compare Post Port Data
    [2016-02-21 09:56:07.307677] [FUNCvirNetNB] [STEP]  8.7: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase9
    ******************************

    [2016-02-21 09:56:07.318023] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Port Update
    [2016-02-21 09:56:07.318708] [FUNCvirNetNB] [STEP]  9.1: Generate Post Data
    [2016-02-21 09:56:07.320149] [FUNCvirNetNB] [STEP]  9.2: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:07.327326] [FUNCvirNetNB] [STEP]  9.3: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:07.336517] [FUNCvirNetNB] [STEP]  9.4: Post Port Data via HTTP
    [2016-02-21 09:56:07.345702] [FUNCvirNetNB] [STEP]  9.5: Update Port Data via HTTP
    [2016-02-21 09:56:07.354021] [FUNCvirNetNB] [STEP]  9.6: Get Port Data via HTTP
    [2016-02-21 09:56:07.360429] [FUNCvirNetNB] [STEP]  9.7: Compare Update Port Data
    [2016-02-21 09:56:07.361666] [FUNCvirNetNB] [STEP]  9.8: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase10
    ******************************

    [2016-02-21 09:56:07.372086] [FUNCvirNetNB] [CASE]  Virtual Network NBI Test - Port Delete
    [2016-02-21 09:56:07.372739] [FUNCvirNetNB] [STEP]  10.1: Generate Post Data
    [2016-02-21 09:56:07.373778] [FUNCvirNetNB] [STEP]  10.2: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:07.380739] [FUNCvirNetNB] [STEP]  10.3: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:07.388862] [FUNCvirNetNB] [STEP]  10.4: Post Port Data via HTTP
    [2016-02-21 09:56:07.396014] [FUNCvirNetNB] [STEP]  10.5: Delete Port Data via HTTP
    [2016-02-21 09:56:07.417621] [FUNCvirNetNB] [STEP]  10.6: Get Port Data is NULL
    [2016-02-21 09:56:12.430407] [FUNCvirNetNB] [STEP]  10.7: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************



    *************************************
        Test Execution Summary

    *************************************

     Test Start           : 21 Feb 2016 09:55:56
     Test End             : 21 Feb 2016 09:56:12
     Execution Time       : 0:00:15.628718
     Total tests planned  : 9
     Total tests RUN      : 9
     Total Pass           : 9
     Total Fail           : 0
     Total No Result      : 0
     Success Percentage   : 100%
     Execution Result     : 100%



    ******************************
     CASE INIT
    ******************************

    ['ONOSrest']

    ******************************
     Result summary for Testcase2
    ******************************

    [2016-02-21 09:56:12.836955] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Router Post
    [2016-02-21 09:56:12.838221] [FUNCvirNetNBL3] [STEP]  2.1: Post Network Data via HTTP(Post Router need post network)
    [2016-02-21 09:56:12.873649] [FUNCvirNetNBL3] [STEP]  2.2: Post Router Data via HTTP
    [2016-02-21 09:56:12.881751] [FUNCvirNetNBL3] [STEP]  2.3: Get Router Data via HTTP
    [2016-02-21 09:56:12.914578] [FUNCvirNetNBL3] [STEP]  2.4: Compare Post Router Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase3
    ******************************

    [2016-02-21 09:56:12.930658] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Router Update
    [2016-02-21 09:56:12.931841] [FUNCvirNetNBL3] [STEP]  3.1: Post Network Data via HTTP(Post Router need post network)
    [2016-02-21 09:56:12.939584] [FUNCvirNetNBL3] [STEP]  3.2: Post Router Data via HTTP
    [2016-02-21 09:56:12.946895] [FUNCvirNetNBL3] [STEP]  3.3: Update Router Data via HTTP
    [2016-02-21 09:56:12.953601] [FUNCvirNetNBL3] [STEP]  3.4: Get Router Data via HTTP
    [2016-02-21 09:56:12.959887] [FUNCvirNetNBL3] [STEP]  3.5: Compare Router Data
    [2016-02-21 09:56:12.961048] [FUNCvirNetNBL3] [STEP]  3.6: Delete Router via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase4
    ******************************

    [2016-02-21 09:56:12.970433] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Router Delete
    [2016-02-21 09:56:12.971622] [FUNCvirNetNBL3] [STEP]  4.1: Post Network Data via HTTP(Post Router need post network)
    [2016-02-21 09:56:12.979473] [FUNCvirNetNBL3] [STEP]  4.2: Post Router Data via HTTP
    [2016-02-21 09:56:12.986263] [FUNCvirNetNBL3] [STEP]  4.3: Delete Router Data via HTTP
    [2016-02-21 09:56:12.992190] [FUNCvirNetNBL3] [STEP]  4.4: Get Router Data is NULL
    Verify the Router status

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase5
    ******************************

    [2016-02-21 09:56:18.008957] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - RouterInterface Post
    [2016-02-21 09:56:18.010175] [FUNCvirNetNBL3] [STEP]  5.1: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:18.018296] [FUNCvirNetNBL3] [STEP]  5.2: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:18.026382] [FUNCvirNetNBL3] [STEP]  5.3: Post Port Data via HTTP
    [2016-02-21 09:56:18.034099] [FUNCvirNetNBL3] [STEP]  5.4: Post Router Data via HTTP
    [2016-02-21 09:56:18.040193] [FUNCvirNetNBL3] [STEP]  5.5: Put RouterInterface Data via HTTP
    [2016-02-21 09:56:18.047317] [FUNCvirNetNBL3] [STEP]  5.6: Get RouterInterface Data via HTTP
    [2016-02-21 09:56:18.053592] [FUNCvirNetNBL3] [STEP]  5.7: Compare Post Port Data
    [2016-02-21 09:56:18.055253] [FUNCvirNetNBL3] [STEP]  5.8: Del RouterInterface Data via HTTP
    [2016-02-21 09:56:18.062038] [FUNCvirNetNBL3] [STEP]  5.9: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase6
    ******************************

    [2016-02-21 09:56:18.078391] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - RouterInterface Delete
    [2016-02-21 09:56:18.079883] [FUNCvirNetNBL3] [STEP]  6.1: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:18.087420] [FUNCvirNetNBL3] [STEP]  6.2: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:18.095337] [FUNCvirNetNBL3] [STEP]  6.3: Post Port Data via HTTP
    [2016-02-21 09:56:18.103345] [FUNCvirNetNBL3] [STEP]  6.4: Post Router Data via HTTP
    [2016-02-21 09:56:18.109767] [FUNCvirNetNBL3] [STEP]  6.5: Post RouterInterface Data via HTTP
    [2016-02-21 09:56:18.116024] [FUNCvirNetNBL3] [STEP]  6.6: Del RouterInterface Data via HTTP
    [2016-02-21 09:56:18.122686] [FUNCvirNetNBL3] [STEP]  6.7: Delete Port Data via HTTP
    [2016-02-21 09:56:18.129655] [FUNCvirNetNBL3] [STEP]  6.8: Get Port Data is NULL
    [2016-02-21 09:56:23.145559] [FUNCvirNetNBL3] [STEP]  6.9: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase7
    ******************************

    [2016-02-21 09:56:23.164294] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - FloatingIp Post
    [2016-02-21 09:56:23.165631] [FUNCvirNetNBL3] [STEP]  7.1: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:23.173909] [FUNCvirNetNBL3] [STEP]  7.2: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:23.182105] [FUNCvirNetNBL3] [STEP]  7.3: Post Port Data via HTTP
    [2016-02-21 09:56:23.189623] [FUNCvirNetNBL3] [STEP]  7.4: Post Router Data via HTTP
    [2016-02-21 09:56:23.196108] [FUNCvirNetNBL3] [STEP]  7.5: Get Port Data via HTTP
    [2016-02-21 09:56:23.204332] [FUNCvirNetNBL3] [STEP]  7.6: Post FloatingIp Data via HTTP
    [2016-02-21 09:56:23.211580] [FUNCvirNetNBL3] [STEP]  7.7: Get Port Data via HTTP
    [2016-02-21 09:56:23.218993] [FUNCvirNetNBL3] [STEP]  7.8: Get FloatingIp Data via HTTP
    [2016-02-21 09:56:23.251318] [FUNCvirNetNBL3] [STEP]  7.9: Get FloatingIp Data via HTTP
    [2016-02-21 09:56:23.259068] [FUNCvirNetNBL3] [STEP]  7.10: Compare Post FloatingIp Data
    [2016-02-21 09:56:23.260001] [FUNCvirNetNBL3] [STEP]  7.11: Post FloatingIp Clean Data via HTTP
    [2016-02-21 09:56:23.266784] [FUNCvirNetNBL3] [STEP]  7.12: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase8
    ******************************

    [2016-02-21 09:56:23.289110] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - FloatingIp Update
    [2016-02-21 09:56:23.291300] [FUNCvirNetNBL3] [STEP]  8.1: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:23.299318] [FUNCvirNetNBL3] [STEP]  8.2: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:23.307738] [FUNCvirNetNBL3] [STEP]  8.3: Post Port Data via HTTP
    [2016-02-21 09:56:23.315822] [FUNCvirNetNBL3] [STEP]  8.4: Post Router Data via HTTP
    [2016-02-21 09:56:23.322853] [FUNCvirNetNBL3] [STEP]  8.5: Post FloatingIp Data via HTTP
    [2016-02-21 09:56:23.329316] [FUNCvirNetNBL3] [STEP]  8.6: Post Delete Data via HTTP
    [2016-02-21 09:56:23.337183] [FUNCvirNetNBL3] [STEP]  8.7: Post NewPort Data via HTTP
    [2016-02-21 09:56:23.345756] [FUNCvirNetNBL3] [STEP]  8.8: Post NewFloatingIp Data via HTTP
    [2016-02-21 09:56:23.353311] [FUNCvirNetNBL3] [STEP]  8.9: Get NewFloatingIp Data via HTTP
    [2016-02-21 09:56:23.384949] [FUNCvirNetNBL3] [STEP]  8.10: Compare Post FloatingIp Data
    [2016-02-21 09:56:23.385934] [FUNCvirNetNBL3] [STEP]  8.11: Post FloatingIp Clean Data via HTTP
    [2016-02-21 09:56:23.392515] [FUNCvirNetNBL3] [STEP]  8.12: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase9
    ******************************

    [2016-02-21 09:56:23.416898] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - FloatingIp Delete
    [2016-02-21 09:56:23.418399] [FUNCvirNetNBL3] [STEP]  9.1: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:23.425551] [FUNCvirNetNBL3] [STEP]  9.2: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:23.433217] [FUNCvirNetNBL3] [STEP]  9.3: Post Port Data via HTTP
    [2016-02-21 09:56:23.440717] [FUNCvirNetNBL3] [STEP]  9.4: Post Router Data via HTTP
    [2016-02-21 09:56:23.447116] [FUNCvirNetNBL3] [STEP]  9.5: Post FloatingIp Data via HTTP
    [2016-02-21 09:56:23.454356] [FUNCvirNetNBL3] [STEP]  9.6: Post FloatingIp Clean Data via HTTP
    [2016-02-21 09:56:23.465800] [FUNCvirNetNBL3] [STEP]  9.7: Get FloatingIp Data is NULL
    [2016-02-21 09:56:28.479269] [FUNCvirNetNBL3] [STEP]  9.8: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase10
    ******************************

    [2016-02-21 09:56:28.496538] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Gateway Post
    [2016-02-21 09:56:28.498465] [FUNCvirNetNBL3] [STEP]  10.1: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:28.507466] [FUNCvirNetNBL3] [STEP]  10.2: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:28.515564] [FUNCvirNetNBL3] [STEP]  10.3: Post Port Data via HTTP
    [2016-02-21 09:56:28.522598] [FUNCvirNetNBL3] [STEP]  10.4: Post Router Data via HTTP
    [2016-02-21 09:56:28.528755] [FUNCvirNetNBL3] [STEP]  10.5: Get Gateway Data via HTTP
    [2016-02-21 09:56:28.536142] [FUNCvirNetNBL3] [STEP]  10.6: Compare Post Gateway Data
    [2016-02-21 09:56:28.537198] [FUNCvirNetNBL3] [STEP]  10.7: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase11
    ******************************

    [2016-02-21 09:56:28.553805] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Gateway Update
    [2016-02-21 09:56:28.555461] [FUNCvirNetNBL3] [STEP]  11.1: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:28.562664] [FUNCvirNetNBL3] [STEP]  11.2: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:28.570094] [FUNCvirNetNBL3] [STEP]  11.3: Post Port Data via HTTP
    [2016-02-21 09:56:28.577203] [FUNCvirNetNBL3] [STEP]  11.4: Post Router Data via HTTP
    [2016-02-21 09:56:28.583265] [FUNCvirNetNBL3] [STEP]  11.5: Post New Router Data via HTTP
    [2016-02-21 09:56:28.589203] [FUNCvirNetNBL3] [STEP]  11.6: Get Gateway Data via HTTP
    [2016-02-21 09:56:28.594700] [FUNCvirNetNBL3] [STEP]  11.7: Compare Post Gateway Data
    [2016-02-21 09:56:28.595799] [FUNCvirNetNBL3] [STEP]  11.8: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************


    ******************************
     Result summary for Testcase12
    ******************************

    [2016-02-21 09:56:28.611322] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Gateway Delete
    [2016-02-21 09:56:28.612734] [FUNCvirNetNBL3] [STEP]  12.1: Post Network Data via HTTP(Post port need post network)
    [2016-02-21 09:56:28.620160] [FUNCvirNetNBL3] [STEP]  12.2: Post Subnet Data via HTTP(Post port need post subnet)
    [2016-02-21 09:56:28.628079] [FUNCvirNetNBL3] [STEP]  12.3: Post Port Data via HTTP
    [2016-02-21 09:56:28.635761] [FUNCvirNetNBL3] [STEP]  12.4: Post Router Data via HTTP
    [2016-02-21 09:56:28.642664] [FUNCvirNetNBL3] [STEP]  12.5: Post Del Gateway Data via HTTP
    [2016-02-21 09:56:28.648775] [FUNCvirNetNBL3] [STEP]  12.6: Get Gateway Data via HTTP
    [2016-02-21 09:56:28.654590] [FUNCvirNetNBL3] [STEP]  12.7: If Gateway Data is NULL
    [2016-02-21 09:56:33.660980] [FUNCvirNetNBL3] [STEP]  12.8: Clean Data via HTTP

    *****************************
     Result: Pass
    *****************************



    *************************************
        Test Execution Summary

    *************************************

     Test Start           : 21 Feb 2016 09:56:12
     Test End             : 21 Feb 2016 09:56:33
     Execution Time       : 0:00:20.999784
     Total tests planned  : 11
     Total tests RUN      : 11
     Total Pass           : 11
     Total Fail           : 0
     Total No Result      : 0
     Success Percentage   : 100%
     Execution Result     : 100%


Feature tests
-------------

Promise
^^^^^^^
::

    FUNCTEST.info: Running PROMISE test case...
    Promise- INFO - Creating tenant 'promise'...
    Promise- INFO - Adding role '9d0a0a36d3d54cdcb4cd3c29c5f79a28' to tenant 'promise'...
    Promise- INFO - Creating user 'promiser'...
    Promise- INFO - Updating OpenStack credentials...
    Promise- INFO - Creating image 'promise-img' from '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img'...
    Promise- INFO - Creating flavor 'promise-flavor'...
    Promise- INFO - Exporting environment variables...
    Promise- INFO - Running command: npm run -s test -- --reporter json
    Promise- INFO - The test succeeded.
    Promise- DEBUG -
    {
      "stats": {
        "suites": 23,
        "tests": 33,
        "passes": 33,
        "pending": 0,
        "failures": 0,
        "start": "2016-02-21T09:56:46.846Z",
        "end": "2016-02-21T09:56:51.847Z",
        "duration": 5524
      },
      "tests": [
        {
          "title": "should add a new OpenStack provider without error",
          "fullTitle": "promise register OpenStack into resource pool add-provider should add a new OpenStack provider without error",
          "duration": 1217,
          "err": {}
        },
        {
          "title": "should update promise.providers with a new entry",
          "fullTitle": "promise register OpenStack into resource pool add-provider should update promise.providers with a new entry",
          "duration": 10,
          "err": {}
        },
        {
          "title": "should contain a new ResourceProvider record in the store",
          "fullTitle": "promise register OpenStack into resource pool add-provider should contain a new ResourceProvider record in the store",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should add more capacity to the reservation service without error",
          "fullTitle": "promise register OpenStack into resource pool increase-capacity should add more capacity to the reservation service without error",
          "duration": 25,
          "err": {}
        },
        {
          "title": "should update promise.pools with a new entry",
          "fullTitle": "promise register OpenStack into resource pool increase-capacity should update promise.pools with a new entry",
          "duration": 1,
          "err": {}
        },
        {
          "title": "should contain a ResourcePool record in the store",
          "fullTitle": "promise register OpenStack into resource pool increase-capacity should contain a ResourcePool record in the store",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should report total collections and utilizations",
          "fullTitle": "promise register OpenStack into resource pool query-capacity should report total collections and utilizations",
          "duration": 18,
          "err": {}
        },
        {
          "title": "should contain newly added capacity pool",
          "fullTitle": "promise register OpenStack into resource pool query-capacity should contain newly added capacity pool",
          "duration": 8,
          "err": {}
        },
        {
          "title": "should create a new server in target provider without error",
          "fullTitle": "promise allocation without reservation create-instance should create a new server in target provider without error",
          "duration": 1768,
          "err": {}
        },
        {
          "title": "should update promise.allocations with a new entry",
          "fullTitle": "promise allocation without reservation create-instance should update promise.allocations with a new entry",
          "duration": 2,
          "err": {}
        },
        {
          "title": "should contain a new ResourceAllocation record in the store",
          "fullTitle": "promise allocation without reservation create-instance should contain a new ResourceAllocation record in the store",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should reference the created server ID from the provider",
          "fullTitle": "promise allocation without reservation create-instance should reference the created server ID from the provider",
          "duration": 1,
          "err": {}
        },
        {
          "title": "should have low priority state",
          "fullTitle": "promise allocation without reservation create-instance should have low priority state",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should create reservation record (no start/end) without error",
          "fullTitle": "promise allocation using reservation for immediate use create-reservation should create reservation record (no start/end) without error",
          "duration": 41,
          "err": {}
        },
        {
          "title": "should update promise.reservations with a new entry",
          "fullTitle": "promise allocation using reservation for immediate use create-reservation should update promise.reservations with a new entry",
          "duration": 7,
          "err": {}
        },
        {
          "title": "should contain a new ResourceReservation record in the store",
          "fullTitle": "promise allocation using reservation for immediate use create-reservation should contain a new ResourceReservation record in the store",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should create a new server in target provider (with reservation) without error",
          "fullTitle": "promise allocation using reservation for immediate use create-instance should create a new server in target provider (with reservation) without error",
          "duration": 1617,
          "err": {}
        },
        {
          "title": "should contain a new ResourceAllocation record in the store",
          "fullTitle": "promise allocation using reservation for immediate use create-instance should contain a new ResourceAllocation record in the store",
          "duration": 1,
          "err": {}
        },
        {
          "title": "should be referenced in the reservation record",
          "fullTitle": "promise allocation using reservation for immediate use create-instance should be referenced in the reservation record",
          "duration": 7,
          "err": {}
        },
        {
          "title": "should have high priority state",
          "fullTitle": "promise allocation using reservation for immediate use create-instance should have high priority state",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should create reservation record (for future) without error",
          "fullTitle": "promise reservation for future use create-reservation should create reservation record (for future) without error",
          "duration": 75,
          "err": {}
        },
        {
          "title": "should update promise.reservations with a new entry",
          "fullTitle": "promise reservation for future use create-reservation should update promise.reservations with a new entry",
          "duration": 17,
          "err": {}
        },
        {
          "title": "should contain a new ResourceReservation record in the store",
          "fullTitle": "promise reservation for future use create-reservation should contain a new ResourceReservation record in the store",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should contain newly created future reservation",
          "fullTitle": "promise reservation for future use query-reservation should contain newly created future reservation",
          "duration": 61,
          "err": {}
        },
        {
          "title": "should modify existing reservation without error",
          "fullTitle": "promise reservation for future use update-reservation should modify existing reservation without error",
          "duration": 65,
          "err": {}
        },
        {
          "title": "should modify existing reservation without error",
          "fullTitle": "promise reservation for future use cancel-reservation should modify existing reservation without error",
          "duration": 17,
          "err": {}
        },
        {
          "title": "should no longer contain record of the deleted reservation",
          "fullTitle": "promise reservation for future use cancel-reservation should no longer contain record of the deleted reservation",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should decrease available capacity from a provider in the future",
          "fullTitle": "promise capacity planning decrease-capacity should decrease available capacity from a provider in the future",
          "duration": 15,
          "err": {}
        },
        {
          "title": "should increase available capacity from a provider in the future",
          "fullTitle": "promise capacity planning increase-capacity should increase available capacity from a provider in the future",
          "duration": 11,
          "err": {}
        },
        {
          "title": "should report available collections and utilizations",
          "fullTitle": "promise capacity planning query-capacity should report available collections and utilizations",
          "duration": 56,
          "err": {}
        },
        {
          "title": "should fail to create immediate reservation record with proper error",
          "fullTitle": "promise reservation with conflict create-reservation should fail to create immediate reservation record with proper error",
          "duration": 60,
          "err": {}
        },
        {
          "title": "should fail to create future reservation record with proper error",
          "fullTitle": "promise reservation with conflict create-reservation should fail to create future reservation record with proper error",
          "duration": 38,
          "err": {}
        },
        {
          "title": "should successfully destroy all allocations",
          "fullTitle": "promise cleanup test allocations destroy-instance should successfully destroy all allocations",
          "duration": 361,
          "err": {}
        }
      ],
      "pending": [],
      "failures": [],
      "passes": [
        {
          "title": "should add a new OpenStack provider without error",
          "fullTitle": "promise register OpenStack into resource pool add-provider should add a new OpenStack provider without error",
          "duration": 1217,
          "err": {}
        },
        {
          "title": "should update promise.providers with a new entry",
          "fullTitle": "promise register OpenStack into resource pool add-provider should update promise.providers with a new entry",
          "duration": 10,
          "err": {}
        },
        {
          "title": "should contain a new ResourceProvider record in the store",
          "fullTitle": "promise register OpenStack into resource pool add-provider should contain a new ResourceProvider record in the store",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should add more capacity to the reservation service without error",
          "fullTitle": "promise register OpenStack into resource pool increase-capacity should add more capacity to the reservation service without error",
          "duration": 25,
          "err": {}
        },
        {
          "title": "should update promise.pools with a new entry",
          "fullTitle": "promise register OpenStack into resource pool increase-capacity should update promise.pools with a new entry",
          "duration": 1,
          "err": {}
        },
        {
          "title": "should contain a ResourcePool record in the store",
          "fullTitle": "promise register OpenStack into resource pool increase-capacity should contain a ResourcePool record in the store",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should report total collections and utilizations",
          "fullTitle": "promise register OpenStack into resource pool query-capacity should report total collections and utilizations",
          "duration": 18,
          "err": {}
        },
        {
          "title": "should contain newly added capacity pool",
          "fullTitle": "promise register OpenStack into resource pool query-capacity should contain newly added capacity pool",
          "duration": 8,
          "err": {}
        },
        {
          "title": "should create a new server in target provider without error",
          "fullTitle": "promise allocation without reservation create-instance should create a new server in target provider without error",
          "duration": 1768,
          "err": {}
        },
        {
          "title": "should update promise.allocations with a new entry",
          "fullTitle": "promise allocation without reservation create-instance should update promise.allocations with a new entry",
          "duration": 2,
          "err": {}
        },
        {
          "title": "should contain a new ResourceAllocation record in the store",
          "fullTitle": "promise allocation without reservation create-instance should contain a new ResourceAllocation record in the store",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should reference the created server ID from the provider",
          "fullTitle": "promise allocation without reservation create-instance should reference the created server ID from the provider",
          "duration": 1,
          "err": {}
        },
        {
          "title": "should have low priority state",
          "fullTitle": "promise allocation without reservation create-instance should have low priority state",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should create reservation record (no start/end) without error",
          "fullTitle": "promise allocation using reservation for immediate use create-reservation should create reservation record (no start/end) without error",
          "duration": 41,
          "err": {}
        },
        {
          "title": "should update promise.reservations with a new entry",
          "fullTitle": "promise allocation using reservation for immediate use create-reservation should update promise.reservations with a new entry",
          "duration": 7,
          "err": {}
        },
        {
          "title": "should contain a new ResourceReservation record in the store",
          "fullTitle": "promise allocation using reservation for immediate use create-reservation should contain a new ResourceReservation record in the store",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should create a new server in target provider (with reservation) without error",
          "fullTitle": "promise allocation using reservation for immediate use create-instance should create a new server in target provider (with reservation) without error",
          "duration": 1617,
          "err": {}
        },
        {
          "title": "should contain a new ResourceAllocation record in the store",
          "fullTitle": "promise allocation using reservation for immediate use create-instance should contain a new ResourceAllocation record in the store",
          "duration": 1,
          "err": {}
        },
        {
          "title": "should be referenced in the reservation record",
          "fullTitle": "promise allocation using reservation for immediate use create-instance should be referenced in the reservation record",
          "duration": 7,
          "err": {}
        },
        {
          "title": "should have high priority state",
          "fullTitle": "promise allocation using reservation for immediate use create-instance should have high priority state",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should create reservation record (for future) without error",
          "fullTitle": "promise reservation for future use create-reservation should create reservation record (for future) without error",
          "duration": 75,
          "err": {}
        },
        {
          "title": "should update promise.reservations with a new entry",
          "fullTitle": "promise reservation for future use create-reservation should update promise.reservations with a new entry",
          "duration": 17,
          "err": {}
        },
        {
          "title": "should contain a new ResourceReservation record in the store",
          "fullTitle": "promise reservation for future use create-reservation should contain a new ResourceReservation record in the store",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should contain newly created future reservation",
          "fullTitle": "promise reservation for future use query-reservation should contain newly created future reservation",
          "duration": 61,
          "err": {}
        },
        {
          "title": "should modify existing reservation without error",
          "fullTitle": "promise reservation for future use update-reservation should modify existing reservation without error",
          "duration": 65,
          "err": {}
        },
        {
          "title": "should modify existing reservation without error",
          "fullTitle": "promise reservation for future use cancel-reservation should modify existing reservation without error",
          "duration": 17,
          "err": {}
        },
        {
          "title": "should no longer contain record of the deleted reservation",
          "fullTitle": "promise reservation for future use cancel-reservation should no longer contain record of the deleted reservation",
          "duration": 0,
          "err": {}
        },
        {
          "title": "should decrease available capacity from a provider in the future",
          "fullTitle": "promise capacity planning decrease-capacity should decrease available capacity from a provider in the future",
          "duration": 15,
          "err": {}
        },
        {
          "title": "should increase available capacity from a provider in the future",
          "fullTitle": "promise capacity planning increase-capacity should increase available capacity from a provider in the future",
          "duration": 11,
          "err": {}
        },
        {
          "title": "should report available collections and utilizations",
          "fullTitle": "promise capacity planning query-capacity should report available collections and utilizations",
          "duration": 56,
          "err": {}
        },
        {
          "title": "should fail to create immediate reservation record with proper error",
          "fullTitle": "promise reservation with conflict create-reservation should fail to create immediate reservation record with proper error",
          "duration": 60,
          "err": {}
        },
        {
          "title": "should fail to create future reservation record with proper error",
          "fullTitle": "promise reservation with conflict create-reservation should fail to create future reservation record with proper error",
          "duration": 38,
          "err": {}
        },
        {
          "title": "should successfully destroy all allocations",
          "fullTitle": "promise cleanup test allocations destroy-instance should successfully destroy all allocations",
          "duration": 361,
          "err": {}
        }
      ]
    }
    Promise- INFO -
    ****************************************
              Promise test report

    ****************************************
     Suites:    23
     Tests:     33
     Passes:    33
     Pending:   0
     Failures:  0
     Start:     2016-02-21T09:56:46.846Z
     End:       2016-02-21T09:56:51.847Z
     Duration:  6.301
    ****************************************


