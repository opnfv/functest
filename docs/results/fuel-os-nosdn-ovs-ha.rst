.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for fuel-os-nosdn-ovs-ha
----------------------------------------------

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
    vPing_ssh- INFO - vPing Start Time:'2016-02-18 13:27:35'
    vPing_ssh- INFO - Creating instance 'opnfv-vping-1'...
     name=opnfv-vping-1
     flavor=<Flavor: m1.small>
     image=fff41d5d-579a-4c26-844d-4e86700c44f6
     network=a5137d46-dea8-4f85-8872-08c4a5927182

    vPing_ssh- INFO - Instance 'opnfv-vping-1' is ACTIVE.
    vPing_ssh- INFO - Adding 'opnfv-vping-1' to security group 'vPing-sg'...
    vPing_ssh- INFO - Creating instance 'opnfv-vping-2'...
     name=opnfv-vping-2
     flavor=<Flavor: m1.small>
     image=fff41d5d-579a-4c26-844d-4e86700c44f6
     network=a5137d46-dea8-4f85-8872-08c4a5927182

    vPing_ssh- INFO - Instance 'opnfv-vping-2' is ACTIVE.
    vPing_ssh- INFO - Adding 'opnfv-vping-2' to security group 'vPing-sg'...
    vPing_ssh- INFO - Creating floating IP for VM 'opnfv-vping-2'...
    vPing_ssh- INFO - Floating IP created: '10.118.101.200'
    vPing_ssh- INFO - Associating floating ip: '10.118.101.200' to VM 'opnfv-vping-2'
    vPing_ssh- INFO - Trying to establish SSH connection to 10.118.101.200...
    vPing_ssh- INFO - Waiting for ping...
    vPing_ssh- INFO - vPing detected!
    vPing_ssh- INFO - vPing duration:'42.1' s.
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
    vPing_userdata- INFO - vPing Start Time:'2016-02-18 13:29:00'
    vPing_userdata- INFO - Creating instance 'opnfv-vping-1'...
     name=opnfv-vping-1
     flavor=<Flavor: m1.small>
     image=5e34c73d-91d0-4852-a407-5a4b4c1932c6
     network=a1efb318-1338-436f-8f26-3a1bacab0538

    vPing_userdata- INFO - Instance 'opnfv-vping-1' is ACTIVE.
    vPing_userdata- INFO - Creating instance 'opnfv-vping-2'...
     name=opnfv-vping-2
     flavor=<Flavor: m1.small>
     image=5e34c73d-91d0-4852-a407-5a4b4c1932c6
     network=a1efb318-1338-436f-8f26-3a1bacab0538
     userdata=
    #!/bin/sh

    while true; do
     ping -c 1 192.168.130.4 2>&1 >/dev/null
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
    vPing_userdata- INFO - vPing duration:'28.6'
    vPing_userdata- INFO - vPing OK
    vPing_userdata- INFO - Cleaning up...
    vPing_userdata- INFO - Deleting network 'vping-net'...


Tempest
^^^^^^^
::

    +------------------------------------------------------------------------------------------------------------------------------------------+----------+---------+
    | name                                                                                                                                     | time     | status  |
    +------------------------------------------------------------------------------------------------------------------------------------------+----------+---------+
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.42319  | success |
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.10399  | success |
    | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 21.61136 | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 24.17689 | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 44.97306 | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.61967  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.61148  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.36880  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.97375  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.39432  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.62328  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.37363  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.61586  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.35380  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.67239  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.38634  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 1.05724  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.53191  | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 1.18318  | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 1.22600  | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 1.02248  | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 2.15108  | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 3.32340  | success |
    | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 5.71240  | success |
    | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 16.19396 | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 0.0      | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.0      | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.0      | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 0.0      | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.0      | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 0.0      | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.0      | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.0      | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 0.0      | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.0      | fail    |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.08151  | success |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 5.38225  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.30658  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 1.03364  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.55185  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.60722  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.61518  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.10976  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.10289  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.10607  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.09006  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.39571  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.55219  | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00134  | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.20517  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.08353  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.01952  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.07490  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.11856  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.03290  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.04317  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.04307  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.08060  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.09867  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.31911  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.03124  | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.10668  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.0      | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 0.0      | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 0.0      | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 0.0      | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.0      | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 0.0      | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 0.0      | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 0.0      | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 0.0      | fail    |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.11260  | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.20834  | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.75046  | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.37893  | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.36982  | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.68314  | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.57271  | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.64458  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 4.92495  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 22.44224 | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 30.13484 | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 15.86074 | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 12.98275 | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 2.59054  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 3.72221  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 2.78814  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 1.60414  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 3.08274  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 2.16235  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 2.57737  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 1.46117  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 1.22501  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 1.11043  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 2.71277  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 1.10491  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 1.50933  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 0.94894  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 1.36216  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 1.57821  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.85906  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 1.81229  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 1.26423  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 1.39718  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 1.00093  | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.29322  | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.02099  | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 0.64378  | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.06226  | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 0.83135  | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.08382  | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.30164  | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.04541  | success |
    | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 0.0      | fail    |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.97480  | success |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 1.05415  | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.26485  | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.02006  | success |
    | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.84845  | success |
    | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.0      | fail    |
    | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.0      | fail    |
    | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.10464  | success |
    | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 1.02679  | success |
    | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.64732  | success |
    | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 2.79302  | success |
    | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.0      | fail    |
    | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.38635  | success |
    | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.0      | fail    |
    | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.67061  | success |
    | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 2.34593  | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.09899  | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.08376  | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.07817  | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.10831  | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.09626  | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.09352  | success |
    | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.57765  | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 1.66822  | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 3.06984  | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 3.62527  | success |
    | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 6.08457  | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 2.35650  | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 2.99120  | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 1.72175  | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 3.61046  | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 4.54154  | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 2.24168  | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 3.49353  | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 3.50686  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 3.20151  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.69691  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.39375  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.38459  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.29588  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.51586  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 2.70137  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.60901  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.31436  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.32710  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.05551  | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.45609  | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 3.05677  | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 2.98082  | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 1.63311  | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.09653  | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.35475  | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 2.90406  | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 3.62630  | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 2.17609  | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.37848  | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.09860  | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 7.70778  | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 4.78033  | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 4.62080  | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 3.61729  | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 7.56892  | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 4.67551  | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 3.90091  | success |
    | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 2.96428  | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 1.98439  | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 3.83806  | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.29228  | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 2.05162  | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 3.96419  | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.36613  | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.64793  | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 6.64806  | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.04923  | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 1.42249  | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.61494  | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.64431  | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.61515  | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.79836  | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.84027  | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 3.71970  | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.06703  | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 15.64501 | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 3.81335  | success |
    | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 3.28514  | success |
    | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 3.08361  | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 13.04419 | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 17.72121 | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 15.46298 | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 19.52032 | success |
    | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.06039  | success |
    | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.07579  | success |
    | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 56.52179 | success |
    | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 42.52437 | success |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 81.46846 | fail    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 72.34328 | fail    |
    +------------------------------------------------------------------------------------------------------------------------------------------+----------+---------+
    run_tempest - INFO - Results: {'timestart': '2016-02-1602:24:40.738841', 'duration': 234, 'tests': 210, 'failures': 26}



Rally
^^^^^
::

    FUNCTEST.info: Running Rally benchmark suite...
    run_rally - INFO - Starting test scenario "authenticate" ...
    run_rally - INFO -
     Preparing input task
     Task  3074958f-9ce1-47bc-9d9d-e78bc2233a68: started
    Task 3074958f-9ce1-47bc-9d9d-e78bc2233a68: finished

    test scenario Authenticate.validate_glance
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_glance     | 0.519 | 0.582  | 0.614  | 0.616  | 0.619 | 0.577 | 100.0%  | 10    |
    | authenticate.validate_glance (2) | 0.318 | 0.548  | 0.621  | 0.699  | 0.777 | 0.557 | 100.0%  | 10    |
    | total                            | 1.086 | 1.305  | 1.37   | 1.467  | 1.563 | 1.307 | 100.0%  | 10    |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.99583816528
    Full duration: 11.4604001045



    test scenario Authenticate.keystone
    +-----------------------------------------------------------------------------+
    |                            Response Times (sec)                             |
    +--------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------+-------+--------+--------+--------+-------+-------+---------+-------+
    | total  | 0.139 | 0.157  | 0.174  | 0.175  | 0.175 | 0.158 | 100.0%  | 10    |
    +--------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.509595870972
    Full duration: 8.08681082726



    test scenario Authenticate.validate_heat
    +-----------------------------------------------------------------------------------------------------+
    |                                        Response Times (sec)                                         |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_heat     | 0.281 | 0.3    | 0.407  | 0.408  | 0.409 | 0.322 | 100.0%  | 10    |
    | authenticate.validate_heat (2) | 0.049 | 0.288  | 0.309  | 0.343  | 0.377 | 0.254 | 100.0%  | 10    |
    | total                          | 0.474 | 0.756  | 0.876  | 0.883  | 0.89  | 0.748 | 100.0%  | 10    |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.13345599174
    Full duration: 9.90360093117



    test scenario Authenticate.validate_nova
    +-----------------------------------------------------------------------------------------------------+
    |                                        Response Times (sec)                                         |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_nova     | 0.263 | 0.305  | 0.334  | 0.394  | 0.454 | 0.313 | 100.0%  | 10    |
    | authenticate.validate_nova (2) | 0.031 | 0.045  | 0.061  | 0.07   | 0.079 | 0.048 | 100.0%  | 10    |
    | total                          | 0.456 | 0.517  | 0.555  | 0.62   | 0.686 | 0.525 | 100.0%  | 10    |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.58427906036
    Full duration: 9.08766698837



    test scenario Authenticate.validate_cinder
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_cinder     | 0.279 | 0.31   | 0.336  | 0.384  | 0.433 | 0.316 | 100.0%  | 10    |
    | authenticate.validate_cinder (2) | 0.023 | 0.284  | 0.356  | 0.475  | 0.594 | 0.244 | 100.0%  | 10    |
    | total                            | 0.44  | 0.784  | 0.989  | 1.066  | 1.142 | 0.75  | 100.0%  | 10    |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.06888413429
    Full duration: 9.67203593254



    test scenario Authenticate.validate_neutron
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_neutron     | 0.279 | 0.333  | 0.347  | 0.348  | 0.348 | 0.328 | 100.0%  | 10    |
    | authenticate.validate_neutron (2) | 0.042 | 0.302  | 0.341  | 0.374  | 0.407 | 0.263 | 100.0%  | 10    |
    | total                             | 0.467 | 0.804  | 0.848  | 0.869  | 0.89  | 0.757 | 100.0%  | 10    |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.20722603798
    Full duration: 10.0450489521



    run_rally - INFO - Test scenario: "authenticate" OK.

    run_rally - INFO - Starting test scenario "glance" ...
    run_rally - INFO -
     Preparing input task
     Task  2d256e70-85ea-4394-a6ef-c1bb7f56a349: started
    Task 2d256e70-85ea-4394-a6ef-c1bb7f56a349: finished

    test scenario GlanceImages.list_images
    +---------------------------------------------------------------------------------------+
    |                                 Response Times (sec)                                  |
    +--------------------+------+--------+--------+--------+------+-------+---------+-------+
    | action             | min  | median | 90%ile | 95%ile | max  | avg   | success | count |
    +--------------------+------+--------+--------+--------+------+-------+---------+-------+
    | glance.list_images | 0.69 | 0.754  | 0.845  | 0.853  | 0.86 | 0.771 | 100.0%  | 10    |
    | total              | 0.69 | 0.754  | 0.845  | 0.853  | 0.86 | 0.771 | 100.0%  | 10    |
    +--------------------+------+--------+--------+--------+------+-------+---------+-------+
    Load duration: 2.37443709373
    Full duration: 12.192773819



    test scenario GlanceImages.create_image_and_boot_instances
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | glance.create_image | 7.016  | 7.626  | 8.071  | 8.175  | 8.28   | 7.656  | 100.0%  | 10    |
    | nova.boot_servers   | 14.247 | 15.398 | 16.507 | 16.622 | 16.737 | 15.457 | 100.0%  | 10    |
    | total               | 21.583 | 22.978 | 23.909 | 24.335 | 24.761 | 23.114 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 68.0709619522
    Full duration: 125.822338104



    test scenario GlanceImages.create_and_list_image
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | glance.create_image | 7.021 | 7.699  | 9.045  | 14.322 | 19.599 | 8.763 | 100.0%  | 10    |
    | glance.list_images  | 0.334 | 0.602  | 0.657  | 0.684  | 0.71   | 0.593 | 100.0%  | 10    |
    | total               | 7.61  | 8.326  | 9.638  | 14.906 | 20.173 | 9.356 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 28.350317955
    Full duration: 54.6049070358



    test scenario GlanceImages.create_and_delete_image
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | glance.create_image | 7.113 | 7.689  | 7.945  | 7.946  | 7.948  | 7.622  | 100.0%  | 10    |
    | glance.delete_image | 1.846 | 2.236  | 3.676  | 9.026  | 14.377 | 3.407  | 100.0%  | 10    |
    | total               | 9.452 | 9.823  | 11.494 | 16.81  | 22.126 | 11.029 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 31.6257281303
    Full duration: 42.0794751644



    run_rally - INFO - Test scenario: "glance" OK.

    run_rally - INFO - Starting test scenario "cinder" ...
    run_rally - INFO -
     Preparing input task
     Task  9f092186-5955-4467-948a-16d0404a8c2f: started
    Task 9f092186-5955-4467-948a-16d0404a8c2f: finished

    test scenario CinderVolumes.create_and_attach_volume
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server     | 10.268 | 12.476 | 13.344 | 13.444 | 13.544 | 12.273 | 100.0%  | 10    |
    | cinder.create_volume | 3.181  | 3.689  | 3.924  | 4.051  | 4.178  | 3.675  | 100.0%  | 10    |
    | nova.attach_volume   | 3.763  | 4.185  | 6.83   | 6.904  | 6.978  | 4.705  | 100.0%  | 10    |
    | nova.detach_volume   | 3.274  | 3.884  | 4.469  | 4.48   | 4.491  | 3.865  | 100.0%  | 10    |
    | cinder.delete_volume | 0.598  | 2.89   | 3.108  | 3.229  | 3.351  | 2.513  | 100.0%  | 10    |
    | nova.delete_server   | 2.824  | 3.112  | 3.135  | 3.142  | 3.15   | 3.06   | 100.0%  | 10    |
    | total                | 28.505 | 29.774 | 31.521 | 31.648 | 31.774 | 30.091 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 89.9433991909
    Full duration: 132.382716179



    test scenario CinderVolumes.create_and_list_volume
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | cinder.create_volume | 9.263 | 9.593  | 10.234 | 10.313 | 10.391 | 9.735 | 100.0%  | 10    |
    | cinder.list_volumes  | 0.073 | 0.334  | 0.502  | 0.51   | 0.517  | 0.325 | 100.0%  | 10    |
    | total                | 9.347 | 9.982  | 10.562 | 10.633 | 10.704 | 10.06 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 30.0611338615
    Full duration: 53.2253141403



    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.693 | 3.995  | 4.393  | 4.446  | 4.498 | 4.011 | 100.0%  | 10    |
    | cinder.list_volumes  | 0.073 | 0.365  | 0.473  | 0.503  | 0.532 | 0.334 | 100.0%  | 10    |
    | total                | 3.792 | 4.367  | 4.739  | 4.852  | 4.964 | 4.345 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 13.0783438683
    Full duration: 34.8268380165



    test scenario CinderVolumes.create_and_list_snapshots
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_snapshot | 3.034 | 3.324  | 3.749  | 4.714  | 5.679 | 3.488 | 100.0%  | 10    |
    | cinder.list_snapshots  | 0.027 | 0.306  | 0.324  | 0.326  | 0.329 | 0.227 | 100.0%  | 10    |
    | total                  | 3.132 | 3.417  | 4.072  | 5.033  | 5.994 | 3.715 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 10.4324269295
    Full duration: 51.1932430267



    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.495 | 3.952  | 4.201  | 4.213  | 4.224 | 3.929 | 100.0%  | 10    |
    | cinder.delete_volume | 0.559 | 2.729  | 3.265  | 3.327  | 3.389 | 2.111 | 100.0%  | 10    |
    | total                | 4.352 | 6.379  | 7.367  | 7.421  | 7.476 | 6.04  | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 18.7915260792
    Full duration: 37.4740400314



    test scenario CinderVolumes.create_and_delete_volume
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 9.153 | 9.894  | 10.152 | 10.17  | 10.189 | 9.798  | 100.0%  | 10    |
    | cinder.delete_volume | 0.563 | 0.972  | 3.341  | 3.425  | 3.51   | 1.572  | 100.0%  | 10    |
    | total                | 9.717 | 10.853 | 13.493 | 13.596 | 13.699 | 11.371 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 31.9503250122
    Full duration: 51.7525529861



    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.461 | 3.688  | 4.442  | 4.444  | 4.447 | 3.838 | 100.0%  | 10    |
    | cinder.delete_volume | 0.493 | 0.917  | 3.039  | 3.183  | 3.328 | 1.504 | 100.0%  | 10    |
    | total                | 4.048 | 4.704  | 7.416  | 7.425  | 7.434 | 5.343 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 16.7748939991
    Full duration: 35.0109767914



    test scenario CinderVolumes.create_and_upload_volume_to_image
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume          | 3.474  | 3.728  | 4.034  | 4.158  | 4.283  | 3.802  | 100.0%  | 10    |
    | cinder.upload_volume_to_image | 16.739 | 27.612 | 32.627 | 32.648 | 32.669 | 26.268 | 100.0%  | 10    |
    | cinder.delete_volume          | 0.914  | 2.817  | 3.041  | 3.073  | 3.105  | 2.347  | 100.0%  | 10    |
    | nova.delete_image             | 2.403  | 2.717  | 2.8    | 2.899  | 2.999  | 2.685  | 100.0%  | 10    |
    | total                         | 26.184 | 36.276 | 42.076 | 42.091 | 42.105 | 35.103 | 100.0%  | 10    |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 100.882842064
    Full duration: 122.017296791



    test scenario CinderVolumes.create_and_delete_snapshot
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_snapshot | 2.994 | 3.448  | 3.79   | 4.429  | 5.067 | 3.513 | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.529 | 2.878  | 3.135  | 3.14   | 3.144 | 2.867 | 100.0%  | 10    |
    | total                  | 5.551 | 6.333  | 6.766  | 7.484  | 8.202 | 6.38  | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 20.3024630547
    Full duration: 53.5971570015



    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.445 | 3.759  | 3.809  | 3.811  | 3.814 | 3.703 | 100.0%  | 10    |
    | total                | 3.445 | 3.759  | 3.809  | 3.812  | 3.814 | 3.703 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 11.0321419239
    Full duration: 28.9824199677



    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.698 | 3.935  | 4.094  | 4.163  | 4.233 | 3.919 | 100.0%  | 10    |
    | total                | 3.699 | 3.935  | 4.094  | 4.163  | 4.233 | 3.919 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 11.7128379345
    Full duration: 34.5113909245



    test scenario CinderVolumes.list_volumes
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.list_volumes | 0.491 | 0.525  | 0.554  | 0.555  | 0.556 | 0.529 | 100.0%  | 10    |
    | total               | 0.491 | 0.525  | 0.554  | 0.555  | 0.556 | 0.529 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.63166594505
    Full duration: 66.0012481213



    test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.397  | 3.887  | 4.192  | 4.206  | 4.22   | 3.861  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.867  | 3.153  | 3.188  | 3.25   | 3.311  | 3.111  | 100.0%  | 10    |
    | nova.attach_volume     | 3.869  | 5.36   | 10.321 | 11.444 | 12.567 | 6.387  | 100.0%  | 10    |
    | nova.detach_volume     | 3.309  | 3.955  | 4.207  | 4.268  | 4.33   | 3.843  | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.26   | 2.629  | 2.904  | 3.051  | 3.199  | 2.668  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.553  | 2.446  | 2.844  | 2.938  | 3.033  | 1.903  | 100.0%  | 10    |
    | total                  | 18.664 | 22.016 | 27.546 | 29.149 | 30.752 | 22.899 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 67.0612659454
    Full duration: 183.666878939



    test scenario CinderVolumes.create_from_volume_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.553 | 3.919  | 4.193  | 4.206  | 4.219 | 3.896 | 100.0%  | 10    |
    | cinder.delete_volume | 2.698 | 3.101  | 3.447  | 3.564  | 3.682 | 3.136 | 100.0%  | 10    |
    | total                | 6.251 | 7.071  | 7.484  | 7.564  | 7.645 | 7.032 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 21.0021979809
    Full duration: 55.9390618801



    test scenario CinderVolumes.create_and_extend_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.435 | 4.074  | 4.424  | 4.424  | 4.425 | 4.026 | 100.0%  | 10    |
    | cinder.extend_volume | 0.707 | 1.246  | 3.299  | 3.344  | 3.389 | 1.877 | 100.0%  | 10    |
    | cinder.delete_volume | 0.692 | 1.948  | 3.07   | 3.114  | 3.157 | 1.937 | 100.0%  | 10    |
    | total                | 5.944 | 8.052  | 8.803  | 9.273  | 9.743 | 7.84  | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 23.8975720406
    Full duration: 43.0286390781



    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.311  | 3.828  | 3.963  | 3.983  | 4.004  | 3.796  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.536  | 2.956  | 3.228  | 3.282  | 3.336  | 2.967  | 100.0%  | 10    |
    | nova.attach_volume     | 3.854  | 4.422  | 6.403  | 6.702  | 7.002  | 4.856  | 100.0%  | 10    |
    | nova.detach_volume     | 3.28   | 3.968  | 4.168  | 4.23   | 4.291  | 3.861  | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.409  | 2.566  | 2.92   | 2.931  | 2.943  | 2.652  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.616  | 2.517  | 2.894  | 3.087  | 3.279  | 2.098  | 100.0%  | 10    |
    | total                  | 19.096 | 21.622 | 23.818 | 24.006 | 24.195 | 21.486 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 61.8816320896
    Full duration: 192.880079985



    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +-----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                      |
    +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.008 | 3.875  | 4.246  | 4.262  | 4.278  | 3.77   | 100.0%  | 10    |
    | cinder.create_snapshot | 2.518 | 3.123  | 3.599  | 3.708  | 3.818  | 3.136  | 100.0%  | 10    |
    | nova.attach_volume     | 3.945 | 5.453  | 7.683  | 8.854  | 10.024 | 5.87   | 100.0%  | 10    |
    | nova.detach_volume     | 3.292 | 3.879  | 4.458  | 4.792  | 5.127  | 3.95   | 100.0%  | 10    |
    | cinder.delete_snapshot | 0.527 | 2.572  | 2.804  | 2.854  | 2.904  | 2.393  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.894 | 2.839  | 3.023  | 3.037  | 3.052  | 2.513  | 100.0%  | 10    |
    | total                  | 20.01 | 23.245 | 26.325 | 27.177 | 28.028 | 23.414 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 71.9912419319
    Full duration: 203.27274704



    run_rally - INFO - Test scenario: "cinder" OK.

    run_rally - INFO - Starting test scenario "heat" ...
    run_rally - INFO -
     Preparing input task
     Task  f964ffc4-416b-4d44-b65d-29baeaea8bec: started
    Task f964ffc4-416b-4d44-b65d-29baeaea8bec: finished

    test scenario HeatStacks.create_suspend_resume_delete_stack
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack  | 3.969 | 4.357  | 4.55   | 4.551  | 4.551 | 4.324 | 100.0%  | 10    |
    | heat.suspend_stack | 1.657 | 1.711  | 1.822  | 1.868  | 1.915 | 1.731 | 100.0%  | 10    |
    | heat.resume_stack  | 1.437 | 1.616  | 1.637  | 1.648  | 1.658 | 1.574 | 100.0%  | 10    |
    | heat.delete_stack  | 1.403 | 1.555  | 1.702  | 2.211  | 2.721 | 1.658 | 100.0%  | 10    |
    | total              | 8.875 | 9.374  | 9.503  | 9.735  | 9.967 | 9.288 | 100.0%  | 10    |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 27.5499420166
    Full duration: 37.6667420864



    test scenario HeatStacks.create_and_delete_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 3.985 | 4.305  | 4.343  | 4.374  | 4.405 | 4.237 | 100.0%  | 10    |
    | heat.delete_stack | 1.379 | 1.455  | 1.484  | 1.487  | 1.489 | 1.447 | 100.0%  | 10    |
    | total             | 5.451 | 5.729  | 5.798  | 5.812  | 5.826 | 5.683 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 17.0478360653
    Full duration: 27.8095588684



    test scenario HeatStacks.create_and_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 26.314 | 28.232 | 29.851 | 29.855 | 29.859 | 28.255 | 100.0%  | 10    |
    | heat.delete_stack | 10.7   | 11.864 | 12.929 | 12.939 | 12.949 | 12.051 | 100.0%  | 10    |
    | total             | 38.29  | 40.481 | 41.719 | 41.722 | 41.725 | 40.306 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 120.330497026
    Full duration: 130.361554861



    test scenario HeatStacks.create_and_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 22.65  | 24.176 | 25.608 | 26.138 | 26.667 | 24.433 | 100.0%  | 10    |
    | heat.delete_stack | 10.59  | 11.212 | 11.949 | 12.486 | 13.022 | 11.332 | 100.0%  | 10    |
    | total             | 33.338 | 36.173 | 37.277 | 37.282 | 37.287 | 35.765 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 105.698035955
    Full duration: 115.92205596



    test scenario HeatStacks.list_stacks_and_resources
    +------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                         |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.list_stacks                | 0.513 | 0.529  | 0.55   | 0.555  | 0.559 | 0.532 | 100.0%  | 10    |
    | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0   | 0.0   | 100.0%  | 10    |
    | total                           | 0.513 | 0.529  | 0.55   | 0.555  | 0.56  | 0.532 | 100.0%  | 10    |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.66571998596
    Full duration: 10.2634401321



    test scenario HeatStacks.create_update_delete_stack
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg    | success | count |
    +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
    | heat.create_stack | 3.891 | 4.318  | 4.491  | 4.525  | 4.559 | 4.283  | 100.0%  | 10    |
    | heat.update_stack | 3.532 | 3.653  | 3.805  | 3.849  | 3.893 | 3.669  | 100.0%  | 10    |
    | heat.delete_stack | 1.517 | 2.659  | 2.766  | 2.767  | 2.768 | 2.555  | 100.0%  | 10    |
    | total             | 9.434 | 10.591 | 10.815 | 10.957 | 11.1  | 10.507 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+--------+---------+-------+
    Load duration: 31.6606299877
    Full duration: 41.6391699314



    test scenario HeatStacks.create_update_delete_stack
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack | 3.815 | 4.241  | 4.394  | 4.403  | 4.411  | 4.206 | 100.0%  | 10    |
    | heat.update_stack | 3.536 | 3.637  | 3.758  | 3.809  | 3.86   | 3.655 | 100.0%  | 10    |
    | heat.delete_stack | 1.359 | 1.407  | 1.693  | 2.128  | 2.563  | 1.55  | 100.0%  | 10    |
    | total             | 9.067 | 9.301  | 9.655  | 10.15  | 10.645 | 9.412 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 27.7025399208
    Full duration: 38.6538958549



    test scenario HeatStacks.create_update_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 3.845  | 4.648  | 5.545  | 5.549  | 5.552  | 4.702  | 100.0%  | 10    |
    | heat.update_stack | 5.818  | 5.896  | 6.239  | 6.242  | 6.246  | 5.982  | 100.0%  | 10    |
    | heat.delete_stack | 2.479  | 2.526  | 2.59   | 2.606  | 2.623  | 2.537  | 100.0%  | 10    |
    | total             | 12.651 | 13.069 | 13.902 | 13.942 | 13.981 | 13.221 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 39.0307080746
    Full duration: 49.9186120033



    test scenario HeatStacks.create_update_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack | 5.244  | 5.361  | 5.485  | 5.498  | 5.511  | 5.375 | 100.0%  | 10    |
    | heat.update_stack | 9.239  | 9.295  | 9.34   | 9.346  | 9.353  | 9.298 | 100.0%  | 10    |
    | heat.delete_stack | 3.643  | 3.694  | 3.736  | 3.74   | 3.745  | 3.697 | 100.0%  | 10    |
    | total             | 18.262 | 18.349 | 18.503 | 18.508 | 18.514 | 18.37 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 55.1248130798
    Full duration: 66.4681949615



    test scenario HeatStacks.create_update_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 4.185  | 4.4    | 4.476  | 4.481  | 4.486  | 4.371  | 100.0%  | 10    |
    | heat.update_stack | 5.806  | 5.891  | 5.921  | 5.933  | 5.946  | 5.879  | 100.0%  | 10    |
    | heat.delete_stack | 2.512  | 2.569  | 2.622  | 2.626  | 2.629  | 2.572  | 100.0%  | 10    |
    | total             | 12.536 | 12.853 | 12.946 | 12.953 | 12.959 | 12.821 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 38.3984200954
    Full duration: 49.409635067



    test scenario HeatStacks.create_update_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 3.99  | 4.405  | 4.621  | 4.622  | 4.623  | 4.393  | 100.0%  | 10    |
    | heat.update_stack | 3.536 | 3.563  | 3.779  | 3.832  | 3.885  | 3.624  | 100.0%  | 10    |
    | heat.delete_stack | 1.335 | 2.488  | 2.546  | 2.555  | 2.564  | 2.09   | 100.0%  | 10    |
    | total             | 9.272 | 10.325 | 10.734 | 10.81  | 10.886 | 10.107 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 30.7103030682
    Full duration: 41.7412381172



    test scenario HeatStacks.create_and_list_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 4.146 | 4.271  | 4.393  | 4.448  | 4.504 | 4.284 | 100.0%  | 10    |
    | heat.list_stacks  | 0.072 | 0.1    | 0.111  | 0.115  | 0.119 | 0.097 | 100.0%  | 10    |
    | total             | 4.254 | 4.376  | 4.494  | 4.541  | 4.588 | 4.382 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 13.1074800491
    Full duration: 29.5266339779



    test scenario HeatStacks.create_check_delete_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 3.907 | 4.192  | 4.293  | 4.364  | 4.435 | 4.155 | 100.0%  | 10    |
    | heat.check_stack  | 0.745 | 1.525  | 1.901  | 1.922  | 1.944 | 1.529 | 100.0%  | 10    |
    | heat.delete_stack | 1.391 | 2.514  | 2.598  | 2.642  | 2.685 | 2.316 | 100.0%  | 10    |
    | total             | 7.026 | 8.237  | 8.42   | 8.494  | 8.569 | 8.0   | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 23.9746980667
    Full duration: 35.3819260597



    run_rally - INFO - Test scenario: "heat" OK.

    run_rally - INFO - Starting test scenario "keystone" ...
    run_rally - INFO -
     Preparing input task
     Task  66a8f673-a0ba-4559-8d8e-34457024edd9: started
    Task 66a8f673-a0ba-4559-8d8e-34457024edd9: finished

    test scenario KeystoneBasic.create_tenant_with_users
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.269 | 0.303  | 0.372  | 0.379  | 0.386 | 0.315 | 100.0%  | 10    |
    | keystone.create_users  | 1.601 | 1.647  | 1.771  | 1.776  | 1.78  | 1.67  | 100.0%  | 10    |
    | total                  | 1.871 | 1.96   | 2.095  | 2.101  | 2.107 | 1.985 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 5.90541005135
    Full duration: 21.2136161327



    test scenario KeystoneBasic.create_add_and_list_user_roles
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.274 | 0.295  | 0.314  | 0.347  | 0.379 | 0.299 | 100.0%  | 10    |
    | keystone.add_role    | 0.254 | 0.271  | 0.354  | 0.378  | 0.401 | 0.289 | 100.0%  | 10    |
    | keystone.list_roles  | 0.133 | 0.141  | 0.154  | 0.155  | 0.155 | 0.142 | 100.0%  | 10    |
    | total                | 0.673 | 0.705  | 0.811  | 0.828  | 0.844 | 0.73  | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.21612095833
    Full duration: 15.3072237968



    test scenario KeystoneBasic.add_and_remove_user_role
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.278 | 0.365  | 0.443  | 0.457  | 0.472 | 0.359 | 100.0%  | 10    |
    | keystone.add_role    | 0.262 | 0.275  | 0.348  | 0.352  | 0.356 | 0.291 | 100.0%  | 10    |
    | keystone.remove_role | 0.153 | 0.168  | 0.178  | 0.18   | 0.182 | 0.167 | 100.0%  | 10    |
    | total                | 0.723 | 0.83   | 0.906  | 0.91   | 0.915 | 0.817 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.51204109192
    Full duration: 15.9939908981



    test scenario KeystoneBasic.create_update_and_delete_tenant
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.283 | 0.313  | 0.4    | 0.402  | 0.403 | 0.333 | 100.0%  | 10    |
    | keystone.update_tenant | 0.128 | 0.156  | 0.251  | 0.251  | 0.251 | 0.178 | 100.0%  | 10    |
    | keystone.delete_tenant | 0.307 | 0.356  | 0.433  | 0.451  | 0.469 | 0.365 | 100.0%  | 10    |
    | total                  | 0.775 | 0.886  | 0.937  | 0.975  | 1.013 | 0.876 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.67470407486
    Full duration: 14.5480179787



    test scenario KeystoneBasic.create_and_delete_service
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_service | 0.262 | 0.301  | 0.324  | 0.35   | 0.375 | 0.301 | 100.0%  | 10    |
    | keystone.delete_service | 0.136 | 0.163  | 0.181  | 0.209  | 0.236 | 0.165 | 100.0%  | 10    |
    | total                   | 0.413 | 0.47   | 0.521  | 0.522  | 0.524 | 0.467 | 100.0%  | 10    |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.38856720924
    Full duration: 12.6957240105



    test scenario KeystoneBasic.create_tenant
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.275 | 0.301  | 0.313  | 0.324  | 0.335 | 0.299 | 100.0%  | 10    |
    | total                  | 0.276 | 0.301  | 0.313  | 0.324  | 0.335 | 0.299 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.917107105255
    Full duration: 8.57450699806



    test scenario KeystoneBasic.create_user
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_user | 0.287 | 0.309  | 0.394  | 0.408  | 0.422 | 0.331 | 100.0%  | 10    |
    | total                | 0.287 | 0.31   | 0.394  | 0.408  | 0.422 | 0.331 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.01195383072
    Full duration: 9.76411700249



    test scenario KeystoneBasic.create_and_list_tenants
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.29  | 0.31   | 0.33   | 0.331  | 0.332 | 0.311 | 100.0%  | 10    |
    | keystone.list_tenants  | 0.122 | 0.138  | 0.16   | 0.194  | 0.229 | 0.146 | 100.0%  | 10    |
    | total                  | 0.422 | 0.451  | 0.492  | 0.525  | 0.558 | 0.457 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.38993692398
    Full duration: 15.0407979488



    test scenario KeystoneBasic.create_and_delete_role
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.29  | 0.367  | 0.474  | 0.501  | 0.528 | 0.374 | 100.0%  | 10    |
    | keystone.delete_role | 0.276 | 0.317  | 0.52   | 0.54   | 0.561 | 0.362 | 100.0%  | 10    |
    | total                | 0.572 | 0.704  | 0.994  | 1.042  | 1.089 | 0.737 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.35643291473
    Full duration: 13.3514738083



    test scenario KeystoneBasic.get_entities
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.266 | 0.31   | 0.344  | 0.369  | 0.393 | 0.313 | 100.0%  | 10    |
    | keystone.create_user   | 0.137 | 0.157  | 0.169  | 0.174  | 0.179 | 0.158 | 100.0%  | 10    |
    | keystone.create_role   | 0.124 | 0.142  | 0.164  | 0.199  | 0.234 | 0.151 | 100.0%  | 10    |
    | keystone.get_tenant    | 0.112 | 0.129  | 0.147  | 0.149  | 0.15  | 0.13  | 100.0%  | 10    |
    | keystone.get_user      | 0.126 | 0.135  | 0.148  | 0.15   | 0.153 | 0.137 | 100.0%  | 10    |
    | keystone.get_role      | 0.116 | 0.127  | 0.143  | 0.156  | 0.169 | 0.131 | 100.0%  | 10    |
    | keystone.service_list  | 0.117 | 0.135  | 0.218  | 0.224  | 0.23  | 0.152 | 100.0%  | 10    |
    | keystone.get_service   | 0.12  | 0.13   | 0.172  | 0.197  | 0.221 | 0.141 | 100.0%  | 10    |
    | total                  | 1.204 | 1.319  | 1.391  | 1.394  | 1.398 | 1.315 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.94662213326
    Full duration: 21.1036419868



    test scenario KeystoneBasic.create_and_list_users
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_user | 0.28  | 0.313  | 0.343  | 0.364  | 0.385 | 0.32  | 100.0%  | 10    |
    | keystone.list_users  | 0.123 | 0.141  | 0.158  | 0.197  | 0.235 | 0.148 | 100.0%  | 10    |
    | total                | 0.43  | 0.461  | 0.516  | 0.53   | 0.545 | 0.468 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.41474604607
    Full duration: 9.85008382797



    run_rally - INFO - Test scenario: "keystone" OK.

    run_rally - INFO - Starting test scenario "neutron" ...
    run_rally - INFO -
     Preparing input task
     Task  2ead843e-f4d1-4ee2-a635-0d37175e3c39: started
    Task 2ead843e-f4d1-4ee2-a635-0d37175e3c39: finished

    test scenario NeutronNetworks.create_and_delete_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.788 | 0.834  | 0.941  | 0.962  | 0.984 | 0.854 | 100.0%  | 10    |
    | neutron.delete_port | 0.229 | 0.625  | 0.757  | 0.814  | 0.871 | 0.637 | 100.0%  | 10    |
    | total               | 1.057 | 1.507  | 1.702  | 1.707  | 1.712 | 1.492 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.537129879
    Full duration: 55.4609839916



    test scenario NeutronNetworks.create_and_list_routers
    +---------------------------------------------------------------------------------------------------+
    |                                       Response Times (sec)                                        |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet        | 0.706 | 0.789  | 0.991  | 0.992  | 0.992 | 0.825 | 100.0%  | 10    |
    | neutron.create_router        | 0.068 | 0.482  | 0.587  | 0.666  | 0.746 | 0.47  | 100.0%  | 10    |
    | neutron.add_interface_router | 0.711 | 0.784  | 0.907  | 1.031  | 1.155 | 0.817 | 100.0%  | 10    |
    | neutron.list_routers         | 0.417 | 0.467  | 0.513  | 0.54   | 0.567 | 0.474 | 100.0%  | 10    |
    | total                        | 2.404 | 2.525  | 2.859  | 2.897  | 2.934 | 2.587 | 100.0%  | 10    |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 7.67870306969
    Full duration: 58.1500780582



    test scenario NeutronNetworks.create_and_delete_routers
    +------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                         |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet           | 0.749 | 0.813  | 0.872  | 0.875  | 0.878 | 0.816 | 100.0%  | 10    |
    | neutron.create_router           | 0.06  | 0.463  | 0.517  | 0.53   | 0.544 | 0.435 | 100.0%  | 10    |
    | neutron.add_interface_router    | 0.335 | 0.772  | 0.867  | 0.868  | 0.869 | 0.707 | 100.0%  | 10    |
    | neutron.remove_interface_router | 0.341 | 0.691  | 0.901  | 0.916  | 0.93  | 0.69  | 100.0%  | 10    |
    | neutron.delete_router           | 0.553 | 0.682  | 0.838  | 0.854  | 0.87  | 0.686 | 100.0%  | 10    |
    | total                           | 2.946 | 3.271  | 3.758  | 3.795  | 3.832 | 3.335 | 100.0%  | 10    |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 9.81285190582
    Full duration: 60.2574419975



    test scenario NeutronNetworks.create_and_list_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.81  | 0.883  | 0.976  | 0.981  | 0.987 | 0.89  | 100.0%  | 10    |
    | neutron.list_ports  | 0.563 | 0.626  | 0.776  | 0.827  | 0.877 | 0.652 | 100.0%  | 10    |
    | total               | 1.398 | 1.535  | 1.661  | 1.723  | 1.785 | 1.542 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.79494190216
    Full duration: 57.4564638138



    test scenario NeutronNetworks.create_and_delete_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.782 | 0.868  | 0.944  | 0.944  | 0.945 | 0.867 | 100.0%  | 10    |
    | neutron.delete_subnet | 0.579 | 0.66   | 0.806  | 0.813  | 0.82  | 0.679 | 100.0%  | 10    |
    | total                 | 1.374 | 1.515  | 1.721  | 1.735  | 1.75  | 1.546 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.67370796204
    Full duration: 54.8155629635



    test scenario NeutronNetworks.create_and_delete_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.617 | 0.701  | 0.786  | 0.79   | 0.794 | 0.702 | 100.0%  | 10    |
    | neutron.delete_network | 0.516 | 0.595  | 0.635  | 0.66   | 0.685 | 0.592 | 100.0%  | 10    |
    | total                  | 1.156 | 1.302  | 1.382  | 1.392  | 1.401 | 1.294 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.91053414345
    Full duration: 34.4190309048



    test scenario NeutronNetworks.create_and_list_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.605 | 0.698  | 0.893  | 0.897  | 0.901 | 0.723 | 100.0%  | 10    |
    | neutron.list_networks  | 0.403 | 0.422  | 0.518  | 0.522  | 0.526 | 0.44  | 100.0%  | 10    |
    | total                  | 1.013 | 1.156  | 1.315  | 1.315  | 1.315 | 1.163 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.48294115067
    Full duration: 36.022400856



    test scenario NeutronNetworks.create_and_update_routers
    +---------------------------------------------------------------------------------------------------+
    |                                       Response Times (sec)                                        |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet        | 0.749 | 0.82   | 0.85   | 0.884  | 0.919 | 0.816 | 100.0%  | 10    |
    | neutron.create_router        | 0.077 | 0.47   | 0.6    | 0.73   | 0.861 | 0.482 | 100.0%  | 10    |
    | neutron.add_interface_router | 0.362 | 0.752  | 0.811  | 0.858  | 0.904 | 0.692 | 100.0%  | 10    |
    | neutron.update_router        | 0.206 | 0.635  | 0.668  | 0.68   | 0.691 | 0.554 | 100.0%  | 10    |
    | total                        | 1.848 | 2.659  | 2.876  | 3.008  | 3.14  | 2.544 | 100.0%  | 10    |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 7.22650980949
    Full duration: 60.5388588905



    test scenario NeutronNetworks.create_and_update_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.654 | 0.724  | 0.888  | 0.911  | 0.934 | 0.756 | 100.0%  | 10    |
    | neutron.update_network | 0.145 | 0.545  | 0.569  | 0.59   | 0.611 | 0.502 | 100.0%  | 10    |
    | total                  | 1.018 | 1.265  | 1.427  | 1.431  | 1.436 | 1.258 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.75120806694
    Full duration: 35.950884819



    test scenario NeutronNetworks.create_and_update_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.814 | 0.896  | 0.995  | 1.01   | 1.024 | 0.896 | 100.0%  | 10    |
    | neutron.update_port | 0.181 | 0.562  | 0.612  | 0.65   | 0.689 | 0.537 | 100.0%  | 10    |
    | total               | 0.995 | 1.461  | 1.585  | 1.597  | 1.608 | 1.433 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.42992901802
    Full duration: 55.774241209



    test scenario NeutronNetworks.create_and_list_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.726 | 0.805  | 1.041  | 1.045  | 1.049 | 0.845 | 100.0%  | 10    |
    | neutron.list_subnets  | 0.053 | 0.422  | 0.446  | 0.446  | 0.446 | 0.353 | 100.0%  | 10    |
    | total                 | 0.861 | 1.221  | 1.458  | 1.458  | 1.458 | 1.199 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.38276219368
    Full duration: 55.0756671429



    test scenario NeutronNetworks.create_and_update_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.731 | 0.802  | 0.891  | 0.923  | 0.954 | 0.814 | 100.0%  | 10    |
    | neutron.update_subnet | 0.186 | 0.573  | 0.629  | 0.662  | 0.694 | 0.455 | 100.0%  | 10    |
    | total                 | 0.962 | 1.374  | 1.524  | 1.533  | 1.543 | 1.27  | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.90665698051
    Full duration: 56.0127599239



    run_rally - INFO - Test scenario: "neutron" OK.

    run_rally - INFO - Starting test scenario "nova" ...
    run_rally - INFO -
     Preparing input task
     Task  63203b68-fb0f-4190-b881-339d49343b7e: started
    Task 63203b68-fb0f-4190-b881-339d49343b7e: finished

    test scenario NovaKeypair.create_and_delete_keypair
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | nova.create_keypair | 0.701 | 0.818  | 0.937  | 1.171  | 1.406 | 0.867 | 100.0%  | 10    |
    | nova.delete_keypair | 0.032 | 0.044  | 0.06   | 0.062  | 0.065 | 0.046 | 100.0%  | 10    |
    | total               | 0.733 | 0.862  | 0.986  | 1.228  | 1.471 | 0.913 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.58676719666
    Full duration: 44.6176929474



    test scenario NovaServers.snapshot_server
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server       | 13.231 | 15.082 | 16.288 | 16.485 | 16.681 | 15.005 | 100.0%  | 10    |
    | nova.create_image      | 11.557 | 12.205 | 14.231 | 14.559 | 14.887 | 12.815 | 100.0%  | 10    |
    | nova.delete_server     | 2.824  | 3.432  | 3.623  | 3.636  | 3.649  | 3.306  | 100.0%  | 10    |
    | nova.boot_server (2)   | 11.125 | 13.278 | 14.799 | 15.311 | 15.823 | 13.287 | 100.0%  | 10    |
    | nova.delete_server (2) | 2.504  | 2.94   | 3.422  | 3.44   | 3.457  | 3.055  | 100.0%  | 10    |
    | nova.delete_image      | 2.668  | 3.276  | 3.598  | 3.634  | 3.669  | 3.259  | 100.0%  | 10    |
    | total                  | 47.925 | 50.051 | 54.553 | 54.844 | 55.135 | 50.728 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 149.159065008
    Full duration: 223.027470827



    test scenario NovaKeypair.boot_and_delete_server_with_keypair
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_keypair | 0.681  | 0.807  | 0.953  | 1.005  | 1.056  | 0.813  | 100.0%  | 10    |
    | nova.boot_server    | 12.625 | 13.795 | 14.626 | 14.992 | 15.358 | 13.92  | 100.0%  | 10    |
    | nova.delete_server  | 2.895  | 3.252  | 3.838  | 4.433  | 5.028  | 3.378  | 100.0%  | 10    |
    | nova.delete_keypair | 0.041  | 0.049  | 0.084  | 0.2    | 0.316  | 0.076  | 100.0%  | 10    |
    | total               | 16.437 | 18.013 | 19.364 | 19.978 | 20.591 | 18.187 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 54.020512104
    Full duration: 122.761439085



    test scenario NovaKeypair.create_and_list_keypairs
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | nova.create_keypair | 0.633 | 0.811  | 0.88   | 0.945  | 1.01  | 0.797 | 100.0%  | 10    |
    | nova.list_keypairs  | 0.019 | 0.032  | 0.048  | 0.057  | 0.065 | 0.034 | 100.0%  | 10    |
    | total               | 0.663 | 0.833  | 0.925  | 0.988  | 1.051 | 0.831 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.51079297066
    Full duration: 45.2959558964



    test scenario NovaServers.list_servers
    +---------------------------------------------------------------------------------------+
    |                                 Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max  | avg   | success | count |
    +-------------------+-------+--------+--------+--------+------+-------+---------+-------+
    | nova.list_servers | 1.153 | 1.561  | 1.667  | 1.699  | 1.73 | 1.534 | 100.0%  | 10    |
    | total             | 1.153 | 1.562  | 1.667  | 1.699  | 1.73 | 1.534 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+------+-------+---------+-------+
    Load duration: 4.51852703094
    Full duration: 136.974627972



    test scenario NovaServers.resize_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 12.504 | 13.59  | 14.825 | 15.228 | 15.63  | 13.671 | 100.0%  | 10    |
    | nova.resize         | 41.099 | 42.204 | 47.49  | 47.556 | 47.621 | 44.023 | 100.0%  | 10    |
    | nova.resize_confirm | 2.651  | 3.698  | 3.805  | 4.059  | 4.314  | 3.556  | 100.0%  | 10    |
    | nova.delete_server  | 2.631  | 3.022  | 3.411  | 4.443  | 5.475  | 3.21   | 100.0%  | 10    |
    | total               | 60.59  | 62.713 | 69.597 | 69.873 | 70.149 | 64.46  | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 192.511741161
    Full duration: 232.632377863



    test scenario NovaServers.boot_server_from_volume_and_delete
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 9.605  | 10.39  | 10.671 | 10.678 | 10.685 | 10.283 | 100.0%  | 10    |
    | nova.boot_server     | 13.194 | 15.101 | 15.844 | 16.008 | 16.171 | 15.084 | 100.0%  | 10    |
    | nova.delete_server   | 5.067  | 5.835  | 6.025  | 6.147  | 6.269  | 5.704  | 100.0%  | 10    |
    | total                | 29.712 | 31.089 | 31.863 | 32.17  | 32.477 | 31.072 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 93.8591198921
    Full duration: 176.781407833



    test scenario NovaServers.boot_and_migrate_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 12.007 | 12.628 | 15.251 | 15.726 | 16.2   | 13.337 | 100.0%  | 10    |
    | nova.stop_server    | 5.734  | 6.679  | 7.157  | 7.198  | 7.239  | 6.643  | 100.0%  | 10    |
    | nova.migrate        | 11.005 | 12.115 | 12.764 | 12.898 | 13.031 | 12.041 | 100.0%  | 10    |
    | nova.resize_confirm | 2.991  | 3.639  | 4.391  | 5.442  | 6.493  | 3.866  | 100.0%  | 10    |
    | nova.delete_server  | 2.512  | 2.889  | 3.089  | 3.162  | 3.235  | 2.846  | 100.0%  | 10    |
    | total               | 36.009 | 38.096 | 41.114 | 42.08  | 43.046 | 38.733 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 117.547358036
    Full duration: 158.547077894



    test scenario NovaServers.boot_and_delete_server
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action             | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server   | 12.11  | 12.864 | 14.437 | 14.962 | 15.486 | 13.148 | 100.0%  | 10    |
    | nova.delete_server | 2.855  | 3.146  | 3.605  | 3.624  | 3.644  | 3.198  | 100.0%  | 10    |
    | total              | 15.189 | 15.944 | 18.012 | 18.222 | 18.433 | 16.346 | 100.0%  | 10    |
    +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 47.4842679501
    Full duration: 115.855407953



    test scenario NovaServers.boot_and_rebuild_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 11.096 | 13.966 | 14.767 | 14.775 | 14.783 | 13.664 | 100.0%  | 10    |
    | nova.rebuild_server | 12.012 | 14.475 | 15.049 | 15.15  | 15.252 | 14.233 | 100.0%  | 10    |
    | nova.delete_server  | 2.573  | 2.99   | 3.499  | 4.34   | 5.181  | 3.213  | 100.0%  | 10    |
    | total               | 28.419 | 30.951 | 32.946 | 34.081 | 35.216 | 31.111 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 91.1762368679
    Full duration: 160.48626709



    test scenario NovaSecGroup.create_and_list_secgroups
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups | 4.384  | 5.131  | 5.534  | 5.638  | 5.741  | 5.066  | 100.0%  | 10    |
    | nova.create_100_rules          | 42.262 | 43.319 | 44.707 | 45.482 | 46.258 | 43.582 | 100.0%  | 10    |
    | nova.list_security_groups      | 0.18   | 0.248  | 0.52   | 0.602  | 0.685  | 0.299  | 100.0%  | 10    |
    | total                          | 47.342 | 48.922 | 49.657 | 50.789 | 51.921 | 48.948 | 100.0%  | 10    |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 145.205770016
    Full duration: 212.670469999



    test scenario NovaSecGroup.create_and_delete_secgroups
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups | 3.797  | 4.842  | 5.428  | 5.548  | 5.668  | 4.805  | 100.0%  | 10    |
    | nova.create_100_rules          | 42.897 | 43.258 | 45.74  | 45.781 | 45.822 | 43.845 | 100.0%  | 10    |
    | nova.delete_10_security_groups | 1.712  | 2.272  | 2.576  | 2.63   | 2.685  | 2.249  | 100.0%  | 10    |
    | total                          | 49.862 | 50.866 | 51.896 | 52.159 | 52.422 | 50.9   | 100.0%  | 10    |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 153.145931959
    Full duration: 195.681600094



    test scenario NovaServers.boot_and_bounce_server
    +-------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                       |
    +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                  | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server        | 12.233 | 14.014 | 14.779 | 15.28  | 15.781 | 13.878 | 100.0%  | 10    |
    | nova.reboot_server      | 5.429  | 5.857  | 6.286  | 6.298  | 6.31   | 5.906  | 100.0%  | 10    |
    | nova.soft_reboot_server | 7.965  | 8.388  | 8.771  | 8.786  | 8.801  | 8.365  | 100.0%  | 10    |
    | nova.stop_server        | 4.492  | 6.237  | 6.84   | 6.896  | 6.952  | 6.14   | 100.0%  | 10    |
    | nova.start_server       | 3.528  | 4.271  | 5.459  | 5.844  | 6.229  | 4.465  | 100.0%  | 10    |
    | nova.rescue_server      | 7.297  | 8.174  | 10.803 | 11.337 | 11.872 | 8.852  | 100.0%  | 10    |
    | nova.unrescue_server    | 5.397  | 5.465  | 5.755  | 5.956  | 6.158  | 5.563  | 100.0%  | 10    |
    | nova.delete_server      | 2.694  | 2.967  | 3.17   | 3.266  | 3.362  | 2.999  | 100.0%  | 10    |
    | total                   | 53.124 | 55.752 | 58.931 | 59.472 | 60.013 | 56.189 | 100.0%  | 10    |
    +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 166.732338905
    Full duration: 235.669921875



    test scenario NovaServers.boot_server
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +------------------+--------+--------+--------+--------+------+--------+---------+-------+
    | action           | min    | median | 90%ile | 95%ile | max  | avg    | success | count |
    +------------------+--------+--------+--------+--------+------+--------+---------+-------+
    | nova.boot_server | 12.435 | 13.902 | 14.341 | 14.37  | 14.4 | 13.679 | 100.0%  | 10    |
    | total            | 12.435 | 13.903 | 14.341 | 14.37  | 14.4 | 13.679 | 100.0%  | 10    |
    +------------------+--------+--------+--------+--------+------+--------+---------+-------+
    Load duration: 40.4824538231
    Full duration: 98.6827569008



    test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
    +-----------------------------------------------------------------------------------------------------------+
    |                                           Response Times (sec)                                            |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups    | 4.34   | 5.246  | 5.496  | 5.585  | 5.675  | 5.171  | 100.0%  | 10    |
    | nova.create_100_rules             | 41.95  | 43.077 | 44.37  | 44.812 | 45.253 | 43.236 | 100.0%  | 10    |
    | nova.boot_server                  | 10.869 | 11.908 | 13.524 | 13.633 | 13.742 | 12.265 | 100.0%  | 10    |
    | nova.get_attached_security_groups | 0.224  | 0.267  | 0.504  | 0.555  | 0.607  | 0.332  | 100.0%  | 10    |
    | nova.delete_server                | 2.533  | 2.618  | 3.078  | 3.091  | 3.103  | 2.742  | 100.0%  | 10    |
    | nova.delete_10_security_groups    | 1.637  | 1.754  | 2.383  | 2.591  | 2.798  | 1.972  | 100.0%  | 10    |
    | total                             | 64.243 | 65.856 | 66.932 | 67.145 | 67.358 | 65.721 | 100.0%  | 10    |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 197.864094019
    Full duration: 266.162395



    test scenario NovaServers.pause_and_unpause_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 12.223 | 14.903 | 15.571 | 15.708 | 15.844 | 14.546 | 100.0%  | 10    |
    | nova.pause_server   | 2.791  | 3.173  | 3.334  | 3.379  | 3.424  | 3.141  | 100.0%  | 10    |
    | nova.unpause_server | 2.459  | 2.849  | 3.186  | 3.266  | 3.346  | 2.907  | 100.0%  | 10    |
    | nova.delete_server  | 2.863  | 3.13   | 3.335  | 3.403  | 3.47   | 3.121  | 100.0%  | 10    |
    | total               | 20.391 | 24.232 | 24.74  | 24.758 | 24.775 | 23.717 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 72.4143497944
    Full duration: 139.801489115



    test scenario NovaServers.boot_server_from_volume
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 9.672  | 10.675 | 10.972 | 11.222 | 11.472 | 10.543 | 100.0%  | 10    |
    | nova.boot_server     | 14.233 | 16.466 | 17.095 | 17.399 | 17.704 | 16.109 | 100.0%  | 10    |
    | total                | 23.906 | 27.176 | 27.879 | 28.21  | 28.54  | 26.653 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 79.5798490047
    Full duration: 145.711636782



    test scenario NovaServers.boot_and_list_server
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server  | 12.064 | 14.109 | 15.049 | 15.436 | 15.823 | 13.885 | 100.0%  | 10    |
    | nova.list_servers | 0.612  | 0.992  | 1.197  | 1.199  | 1.201  | 0.948  | 100.0%  | 10    |
    | total             | 13.261 | 15.082 | 15.982 | 16.209 | 16.435 | 14.833 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 43.442057848
    Full duration: 128.433704138



    run_rally - INFO - Test scenario: "nova" OK.

    run_rally - INFO - Starting test scenario "quotas" ...
    run_rally - INFO -
     Preparing input task
     Task  f60014e7-4880-41c6-afbc-ea7d18ef56e0: started
    Task f60014e7-4880-41c6-afbc-ea7d18ef56e0: finished

    test scenario Quotas.cinder_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 1.111 | 1.203  | 1.671  | 1.682  | 1.692 | 1.279 | 100.0%  | 10    |
    | total                | 1.111 | 1.203  | 1.671  | 1.682  | 1.692 | 1.279 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.63238286972
    Full duration: 15.5500700474



    test scenario Quotas.neutron_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.392 | 0.43   | 0.632  | 0.65   | 0.667 | 0.482 | 100.0%  | 10    |
    | total                | 0.555 | 0.597  | 0.799  | 0.808  | 0.816 | 0.64  | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.90143704414
    Full duration: 12.9954409599



    test scenario Quotas.cinder_update_and_delete
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 1.086 | 1.207  | 1.358  | 1.436  | 1.513 | 1.228 | 100.0%  | 10    |
    | quotas.delete_quotas | 0.549 | 0.88   | 0.94   | 0.951  | 0.963 | 0.839 | 100.0%  | 10    |
    | total                | 1.654 | 2.078  | 2.316  | 2.37   | 2.424 | 2.067 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 6.08279585838
    Full duration: 18.0140779018



    test scenario Quotas.nova_update_and_delete
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.573 | 0.62   | 0.652  | 0.658  | 0.664 | 0.619 | 100.0%  | 10    |
    | quotas.delete_quotas | 0.016 | 0.025  | 0.028  | 0.032  | 0.036 | 0.024 | 100.0%  | 10    |
    | total                | 0.599 | 0.642  | 0.678  | 0.68   | 0.681 | 0.643 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.95340800285
    Full duration: 13.6638329029



    test scenario Quotas.nova_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.575 | 0.616  | 0.669  | 0.681  | 0.692 | 0.622 | 100.0%  | 10    |
    | total                | 0.575 | 0.616  | 0.669  | 0.681  | 0.692 | 0.622 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.90668487549
    Full duration: 13.5694701672



    run_rally - INFO - Test scenario: "quotas" OK.

    run_rally - INFO - Starting test scenario "requests" ...
    run_rally - INFO -
     Preparing input task
     Task  3835bbc7-faf5-4671-9261-aa07c1d6a1e2: started
    Task 3835bbc7-faf5-4671-9261-aa07c1d6a1e2: finished

    test scenario HttpRequests.check_random_request
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | requests.check_request | 5.049 | 5.088  | 5.34   | 5.361  | 5.381 | 5.151 | 100.0%  | 10    |
    | total                  | 5.049 | 5.088  | 5.34   | 5.361  | 5.381 | 5.151 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 15.4988431931
    Full duration: 20.5546550751



    test scenario HttpRequests.check_request
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | requests.check_request | 5.048 | 5.052  | 5.057  | 5.058  | 5.058 | 5.053 | 100.0%  | 10    |
    | total                  | 5.048 | 5.052  | 5.057  | 5.058  | 5.058 | 5.053 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 15.2044279575
    Full duration: 20.1352801323



    run_rally - INFO - Test scenario: "requests" OK.

    run_rally - INFO -


                         Rally Summary Report
    +===================+============+===============+===========+
    | Module            | Duration   | nb. Test Run  | Success   |
    +===================+============+===============+===========+
    | authenticate      | 00:58      | 10            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | glance            | 03:54      | 7             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | cinder            | 22:59      | 50            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | heat              | 11:14      | 35            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | keystone          | 02:37      | 29            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | neutron           | 10:19      | 31            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | nova              | 47:19      | 61            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | quotas            | 01:13      | 7             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | requests          | 00:40      | 2             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    +===================+============+===============+===========+
    | TOTAL:            | 01:41:19   | 232           | 100.00%   |
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
    vIMS - INFO - Cloudify deployment Start Time:'2016-02-19 05:44:47'
    vIMS - INFO - Writing the inputs file
    vIMS - INFO - Launching the cloudify-manager deployment
    vIMS - INFO - Cloudify-manager server is UP !
    vIMS - INFO - Cloudify deployment duration:'1149.9'
    vIMS - INFO - Collect flavor id for all clearwater vm
    vIMS - INFO - vIMS VNF deployment Start Time:'2016-02-19 06:04:00'
    vIMS - INFO - Downloading the openstack-blueprint.yaml blueprint
    vIMS - INFO - Writing the inputs file
    vIMS - INFO - Launching the clearwater deployment
    vIMS - INFO - The deployment of clearwater-opnfv is ended
    vIMS - INFO - vIMS VNF deployment duration:'1133.8'
    vIMS - INFO - vIMS functional test Start Time:'2016-02-19 06:25:59'
    vIMS - INFO - vIMS functional test duration:'2.9'
    vIMS - INFO - Launching the clearwater-opnfv undeployment
    vIMS - ERROR - Error when executing command /bin/bash -c 'source /home/opnfv/functest/data/vIMS/venv_cloudify/bin/activate; cd /home/opnfv/functest/data/vIMS/; cfy executions start -w uninstall -d clearwater-opnfv --timeout 1800 ; cfy deployments delete -d clearwater-opnfv; '
    vIMS - INFO - Launching the cloudify-manager undeployment
    vIMS - INFO - Cloudify-manager server has been successfully removed!
    vIMS - INFO - Removing vIMS tenant ..
    vIMS - INFO - Removing vIMS user ..


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
        "start": "2016-02-23T02:24:39.314Z",
        "end": "2016-02-23T02:24:44.838Z",
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
     Start:     2016-02-18T13:37:06.661Z
     End:       2016-02-18T13:37:12.962Z
     Duration:  6.301
    ****************************************


