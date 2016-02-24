.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for fuel-os-nosdn-nofeature-ha
----------------------------------------------------

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

    +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    | name                                                                                                                                     | time      | status  |
    +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.29312   | success |
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.12976   | success |
    | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 23.95577  | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 32.53650  | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 22.68958  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.54691   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.30066   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.57103   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.97553   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.37256   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.33110   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.34175   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.35964   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.62128   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.88552   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.35258   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 1.14056   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.64330   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 1.59904   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 0.85262   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.89806   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 1.43298   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 2.74835   | success |
    | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 7.51973   | success |
    | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 17.31905  | success |
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
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.11526   | success |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 4.43153   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.49287   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.32071   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.24839   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.62886   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.45498   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.11221   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.07743   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.07866   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.08414   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.09610   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.87584   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00178   | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.18671   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.07254   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.02355   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.09336   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.08789   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.02832   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.01969   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.05608   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.09405   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.07124   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 1.09862   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.02806   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.10085   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.00074   | skip    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 7.05293   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 12.83974  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 75.96327  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.89960   | skip    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 86.10969  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 14.36274  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 25.20801  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 9.79668   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.10422   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.45171   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.71962   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.37393   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.39671   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.67878   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.96139   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.70247   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 5.01425   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 21.66147  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 29.15375  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 17.01011  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 15.12162  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 2.32047   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 2.43351   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 3.54755   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 3.49832   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 1.66971   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 2.67563   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 1.52468   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 2.11125   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 1.11519   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 1.59954   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 2.71532   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 0.67781   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 0.80861   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 1.12394   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.98070   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 1.95038   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.58962   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 1.76753   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 0.92874   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 1.98170   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 1.09696   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.23813   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.02568   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 0.73035   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.03287   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 0.61622   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.10251   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.32244   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.05310   | success |
    | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 46.35639  | success |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 1.19554   | success |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.13783   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.28038   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.02405   | success |
    | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.0       | fail    |
    | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 1.06799   | success |
    | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.70652   | success |
    | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.56777   | success |
    | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.34317   | success |
    | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.61946   | success |
    | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 2.55157   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.10777   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.09198   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.08536   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.12301   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.19557   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.11454   | success |
    | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.58158   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 1.96230   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 3.11881   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 31.78599  | success |
    | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 6.18197   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 0.36573   | fail    |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 4.19923   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 2.05001   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 2.85155   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 4.85758   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 2.47936   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 4.29082   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 4.14373   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 2.85702   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.63578   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.44139   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.31069   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.31575   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.34149   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 2.96967   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.61978   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.30406   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.29284   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.07605   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.28866   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 3.34364   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 2.65709   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 1.51327   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.34515   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.34468   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 3.78910   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 3.78827   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 2.58076   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.35346   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.38372   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 8.02302   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 5.55884   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 4.89503   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 3.13616   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 7.91220   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 4.35397   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 4.24212   | success |
    | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 3.20634   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 2.00386   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 3.26379   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.29497   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 2.34355   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 3.27875   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.05434   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.63001   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 7.10424   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.06177   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 3.98140   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.05857   | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 19.61269  | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 4.21790   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 2.96832   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 2.59962   | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 14.77900  | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 19.28760  | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 14.36310  | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 24.02107  | success |
    | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.05931   | success |
    | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.31742   | success |
    | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 54.55460  | success |
    | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 41.67013  | fail    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 109.37734 | success |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 61.05784  | fail    |
    +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    run_tempest - INFO - Results: {'timestart': '2016-02-1813:29:52.500975', 'duration': 416, 'tests': 210, 'failures': 25}


Rally
^^^^^
::

    FUNCTEST.info: Running Rally benchmark suite...
    run_rally - INFO - Starting test scenario "authenticate" ...
    run_rally - INFO -
     Preparing input task
     Task  2ff4981a-75d9-4de4-a111-3194115c4a00: started
    Task 2ff4981a-75d9-4de4-a111-3194115c4a00: finished

    test scenario Authenticate.validate_glance
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_glance     | 0.534 | 0.569  | 0.722  | 0.818  | 0.914 | 0.618 | 100.0%  | 10    |
    | authenticate.validate_glance (2) | 0.512 | 0.609  | 0.713  | 0.766  | 0.818 | 0.631 | 100.0%  | 10    |
    | total                            | 1.257 | 1.358  | 1.703  | 1.715  | 1.726 | 1.418 | 100.0%  | 10    |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.01803302765
    Full duration: 11.7534348965



    test scenario Authenticate.keystone
    +-----------------------------------------------------------------------------+
    |                            Response Times (sec)                             |
    +--------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------+-------+--------+--------+--------+-------+-------+---------+-------+
    | total  | 0.132 | 0.154  | 0.172  | 0.172  | 0.173 | 0.155 | 100.0%  | 10    |
    +--------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.491301059723
    Full duration: 8.25924301147



    test scenario Authenticate.validate_heat
    +-----------------------------------------------------------------------------------------------------+
    |                                        Response Times (sec)                                         |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_heat     | 0.297 | 0.32   | 0.355  | 0.359  | 0.363 | 0.324 | 100.0%  | 10    |
    | authenticate.validate_heat (2) | 0.043 | 0.056  | 0.302  | 0.304  | 0.307 | 0.127 | 100.0%  | 10    |
    | total                          | 0.499 | 0.607  | 0.769  | 0.82   | 0.87  | 0.629 | 100.0%  | 10    |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.91573691368
    Full duration: 10.0396120548



    test scenario Authenticate.validate_nova
    +-----------------------------------------------------------------------------------------------------+
    |                                        Response Times (sec)                                         |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_nova     | 0.306 | 0.35   | 0.534  | 0.554  | 0.574 | 0.407 | 100.0%  | 10    |
    | authenticate.validate_nova (2) | 0.037 | 0.059  | 0.07   | 0.081  | 0.092 | 0.059 | 100.0%  | 10    |
    | total                          | 0.526 | 0.596  | 0.771  | 0.782  | 0.792 | 0.639 | 100.0%  | 10    |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.9150788784
    Full duration: 9.77701401711



    test scenario Authenticate.validate_cinder
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_cinder     | 0.268 | 0.315  | 0.353  | 0.475  | 0.596 | 0.334 | 100.0%  | 10    |
    | authenticate.validate_cinder (2) | 0.025 | 0.282  | 0.314  | 0.323  | 0.331 | 0.264 | 100.0%  | 10    |
    | total                            | 0.721 | 0.78   | 0.827  | 0.837  | 0.847 | 0.779 | 100.0%  | 10    |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.34766292572
    Full duration: 10.0672118664



    test scenario Authenticate.validate_neutron
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_neutron     | 0.266 | 0.305  | 0.386  | 0.399  | 0.411 | 0.319 | 100.0%  | 10    |
    | authenticate.validate_neutron (2) | 0.043 | 0.291  | 0.375  | 0.403  | 0.432 | 0.241 | 100.0%  | 10    |
    | total                             | 0.483 | 0.76   | 0.908  | 0.914  | 0.92  | 0.729 | 100.0%  | 10    |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.25539779663
    Full duration: 9.62706780434



    run_rally - INFO - Test scenario: "authenticate" OK.

    run_rally - INFO - Starting test scenario "glance" ...
    run_rally - INFO -
     Preparing input task
     Task  9fb726cd-f20e-4f95-b32f-5928c72cf58d: started
    Task 9fb726cd-f20e-4f95-b32f-5928c72cf58d: finished

    test scenario GlanceImages.list_images
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | glance.list_images | 0.72  | 0.85   | 0.942  | 0.947  | 0.951 | 0.833 | 100.0%  | 10    |
    | total              | 0.721 | 0.85   | 0.943  | 0.947  | 0.951 | 0.834 | 100.0%  | 10    |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.45959687233
    Full duration: 12.9740490913



    test scenario GlanceImages.create_image_and_boot_instances
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | glance.create_image | 7.498  | 7.743  | 17.964 | 19.73  | 21.495 | 10.171 | 100.0%  | 10    |
    | nova.boot_servers   | 13.174 | 14.424 | 15.318 | 15.539 | 15.76  | 14.34  | 100.0%  | 10    |
    | total               | 20.863 | 22.368 | 32.383 | 33.741 | 35.099 | 24.511 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 68.7006659508
    Full duration: 127.436779022



    test scenario GlanceImages.create_and_list_image
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | glance.create_image | 7.303 | 7.684  | 7.837  | 7.911  | 7.984 | 7.63  | 100.0%  | 10    |
    | glance.list_images  | 0.328 | 0.583  | 0.697  | 0.698  | 0.699 | 0.574 | 100.0%  | 10    |
    | total               | 7.862 | 8.283  | 8.38   | 8.472  | 8.564 | 8.205 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 24.5710179806
    Full duration: 37.9533209801



    test scenario GlanceImages.create_and_delete_image
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | glance.create_image | 7.448 | 7.605  | 7.805  | 7.817  | 7.829  | 7.617 | 100.0%  | 10    |
    | glance.delete_image | 2.01  | 2.372  | 2.628  | 2.686  | 2.743  | 2.393 | 100.0%  | 10    |
    | total               | 9.506 | 9.976  | 10.387 | 10.466 | 10.545 | 10.01 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 30.0124220848
    Full duration: 40.2773120403



    run_rally - INFO - Test scenario: "glance" OK.

    run_rally - INFO - Starting test scenario "cinder" ...
    run_rally - INFO -
     Preparing input task
     Task  a724f287-e014-40ef-8e87-173e5eb2b0a2: started
    Task a724f287-e014-40ef-8e87-173e5eb2b0a2: finished

    test scenario CinderVolumes.create_and_attach_volume
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server     | 10.889 | 13.965 | 14.695 | 14.724 | 14.752 | 13.234 | 100.0%  | 10    |
    | cinder.create_volume | 3.218  | 3.812  | 4.128  | 4.214  | 4.3    | 3.776  | 100.0%  | 10    |
    | nova.attach_volume   | 3.737  | 4.69   | 4.963  | 5.092  | 5.222  | 4.612  | 100.0%  | 10    |
    | nova.detach_volume   | 3.18   | 3.917  | 4.273  | 4.325  | 4.377  | 3.867  | 100.0%  | 10    |
    | cinder.delete_volume | 0.489  | 2.54   | 2.801  | 2.886  | 2.972  | 2.261  | 100.0%  | 10    |
    | nova.delete_server   | 2.527  | 2.94   | 3.218  | 3.228  | 3.239  | 2.926  | 100.0%  | 10    |
    | total                | 26.351 | 30.9   | 32.731 | 33.273 | 33.815 | 30.677 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 91.1857719421
    Full duration: 133.454293013



    test scenario CinderVolumes.create_and_list_volume
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | cinder.create_volume | 7.415 | 9.652  | 10.383 | 10.548 | 10.713 | 9.48  | 100.0%  | 10    |
    | cinder.list_volumes  | 0.072 | 0.328  | 0.4    | 0.407  | 0.415  | 0.295 | 100.0%  | 10    |
    | total                | 7.76  | 10.022 | 10.706 | 10.88  | 11.054 | 9.775 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 28.0870580673
    Full duration: 51.2606179714



    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.521 | 4.03   | 4.785  | 4.869  | 4.953 | 4.19  | 100.0%  | 10    |
    | cinder.list_volumes  | 0.062 | 0.347  | 0.411  | 0.426  | 0.44  | 0.308 | 100.0%  | 10    |
    | total                | 3.852 | 4.421  | 5.139  | 5.227  | 5.315 | 4.499 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 13.1967639923
    Full duration: 35.2137930393



    test scenario CinderVolumes.create_and_list_snapshots
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_snapshot | 2.957 | 3.349  | 5.449  | 5.627  | 5.805 | 3.738 | 100.0%  | 10    |
    | cinder.list_snapshots  | 0.028 | 0.304  | 0.348  | 0.382  | 0.416 | 0.213 | 100.0%  | 10    |
    | total                  | 3.259 | 3.42   | 5.776  | 5.945  | 6.113 | 3.952 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 10.5537779331
    Full duration: 49.7043690681



    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.281 | 3.907  | 4.106  | 4.128  | 4.15  | 3.806 | 100.0%  | 10    |
    | cinder.delete_volume | 0.788 | 2.667  | 3.082  | 3.16   | 3.239 | 2.256 | 100.0%  | 10    |
    | total                | 4.617 | 6.29   | 6.997  | 7.066  | 7.135 | 6.063 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 18.3220980167
    Full duration: 36.1331720352



    test scenario CinderVolumes.create_and_delete_volume
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 8.901 | 9.932  | 10.338 | 10.395 | 10.452 | 9.781  | 100.0%  | 10    |
    | cinder.delete_volume | 0.579 | 1.672  | 2.856  | 2.952  | 3.049  | 1.773  | 100.0%  | 10    |
    | total                | 9.725 | 11.645 | 12.996 | 13.017 | 13.039 | 11.554 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 35.517152071
    Full duration: 54.0071978569



    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.596 | 3.887  | 4.71   | 4.712  | 4.715 | 4.08  | 100.0%  | 10    |
    | cinder.delete_volume | 0.512 | 0.923  | 1.297  | 2.319  | 3.341 | 1.114 | 100.0%  | 10    |
    | total                | 4.381 | 4.91   | 5.923  | 6.573  | 7.223 | 5.195 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 15.0102190971
    Full duration: 33.4934709072



    test scenario CinderVolumes.create_and_upload_volume_to_image
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume          | 3.512  | 3.838  | 4.155  | 4.202  | 4.249  | 3.861  | 100.0%  | 10    |
    | cinder.upload_volume_to_image | 16.283 | 24.737 | 33.632 | 38.034 | 42.436 | 26.102 | 100.0%  | 10    |
    | cinder.delete_volume          | 0.583  | 1.719  | 3.056  | 3.165  | 3.274  | 1.853  | 100.0%  | 10    |
    | nova.delete_image             | 2.514  | 2.856  | 13.194 | 14.749 | 16.305 | 5.182  | 100.0%  | 10    |
    | total                         | 23.887 | 34.293 | 49.972 | 51.48  | 52.988 | 36.998 | 100.0%  | 10    |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 107.503821135
    Full duration: 129.166619062



    test scenario CinderVolumes.create_and_delete_snapshot
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_snapshot | 3.064 | 3.257  | 3.408  | 3.415  | 3.422 | 3.261 | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.586 | 2.915  | 3.148  | 3.165  | 3.181 | 2.938 | 100.0%  | 10    |
    | total                  | 5.837 | 6.18   | 6.465  | 6.534  | 6.603 | 6.199 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 18.601981163
    Full duration: 53.3941659927



    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.424 | 3.854  | 4.025  | 4.05   | 4.075 | 3.808 | 100.0%  | 10    |
    | total                | 3.424 | 3.854  | 4.025  | 4.05   | 4.075 | 3.808 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 11.3824880123
    Full duration: 30.7913680077



    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.391 | 3.979  | 4.585  | 4.6    | 4.616 | 3.999 | 100.0%  | 10    |
    | total                | 3.391 | 3.979  | 4.585  | 4.601  | 4.616 | 3.999 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 12.107943058
    Full duration: 36.5596921444



    test scenario CinderVolumes.list_volumes
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.list_volumes | 0.478 | 0.562  | 0.711  | 0.746  | 0.781 | 0.587 | 100.0%  | 10    |
    | total               | 0.479 | 0.562  | 0.711  | 0.746  | 0.781 | 0.587 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.79518508911
    Full duration: 65.9313700199



    test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
    +-----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                      |
    +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.557 | 3.914  | 4.206  | 4.213  | 4.22   | 3.884  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.701 | 3.063  | 3.248  | 3.251  | 3.254  | 3.06   | 100.0%  | 10    |
    | nova.attach_volume     | 3.75  | 4.986  | 6.112  | 6.385  | 6.658  | 5.059  | 100.0%  | 10    |
    | nova.detach_volume     | 3.149 | 3.81   | 4.11   | 4.168  | 4.225  | 3.762  | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.241 | 2.766  | 3.077  | 3.102  | 3.128  | 2.725  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.748 | 2.428  | 2.712  | 2.772  | 2.831  | 1.912  | 100.0%  | 10    |
    | total                  | 19.22 | 21.354 | 24.347 | 24.725 | 25.102 | 21.684 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 64.028840065
    Full duration: 186.598311901



    test scenario CinderVolumes.create_from_volume_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.539 | 4.149  | 4.62   | 4.622  | 4.623 | 4.106 | 100.0%  | 10    |
    | cinder.delete_volume | 2.844 | 3.223  | 3.604  | 3.609  | 3.614 | 3.235 | 100.0%  | 10    |
    | total                | 6.383 | 7.559  | 7.85   | 7.868  | 7.886 | 7.341 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 21.6859838963
    Full duration: 55.5635709763



    test scenario CinderVolumes.create_and_extend_volume
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | cinder.create_volume | 3.434 | 3.852  | 3.99   | 4.004  | 4.018  | 3.842 | 100.0%  | 10    |
    | cinder.extend_volume | 0.955 | 2.236  | 3.552  | 3.564  | 3.576  | 2.281 | 100.0%  | 10    |
    | cinder.delete_volume | 0.868 | 3.015  | 3.332  | 3.398  | 3.465  | 2.861 | 100.0%  | 10    |
    | total                | 5.962 | 9.186  | 10.497 | 10.52  | 10.544 | 8.984 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 28.1479110718
    Full duration: 47.0005409718



    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.595  | 3.868  | 4.206  | 4.208  | 4.211  | 3.886  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.595  | 3.131  | 3.249  | 3.258  | 3.267  | 3.037  | 100.0%  | 10    |
    | nova.attach_volume     | 4.101  | 4.563  | 5.363  | 7.225  | 9.087  | 4.928  | 100.0%  | 10    |
    | nova.detach_volume     | 3.299  | 3.896  | 4.226  | 4.274  | 4.323  | 3.816  | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.27   | 2.573  | 2.884  | 3.105  | 3.325  | 2.635  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.611  | 2.479  | 2.742  | 2.863  | 2.983  | 2.239  | 100.0%  | 10    |
    | total                  | 19.728 | 21.533 | 22.719 | 24.643 | 26.568 | 21.737 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 62.6771988869
    Full duration: 187.817504883



    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.255  | 3.476  | 4.793  | 4.86   | 4.926  | 3.766  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.387  | 2.868  | 3.304  | 3.311  | 3.318  | 2.906  | 100.0%  | 10    |
    | nova.attach_volume     | 3.864  | 4.167  | 4.94   | 5.864  | 6.787  | 4.392  | 100.0%  | 10    |
    | nova.detach_volume     | 3.699  | 4.047  | 4.388  | 4.408  | 4.428  | 4.066  | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.492  | 2.621  | 2.825  | 2.828  | 2.831  | 2.651  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.65   | 2.735  | 3.048  | 3.123  | 3.198  | 2.567  | 100.0%  | 10    |
    | total                  | 18.915 | 21.629 | 24.215 | 25.025 | 25.835 | 22.025 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 64.388502121
    Full duration: 192.928286076



    run_rally - INFO - Test scenario: "cinder" OK.

    run_rally - INFO - Starting test scenario "heat" ...
    run_rally - INFO -
     Preparing input task
     Task  44fe34e1-bd7f-47f7-b4e9-ca32c892d8b5: started
    Task 44fe34e1-bd7f-47f7-b4e9-ca32c892d8b5: finished

    test scenario HeatStacks.create_suspend_resume_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action             | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack  | 4.131 | 4.448  | 4.579  | 4.616  | 4.652  | 4.417 | 100.0%  | 10    |
    | heat.suspend_stack | 1.521 | 1.721  | 1.772  | 1.792  | 1.812  | 1.701 | 100.0%  | 10    |
    | heat.resume_stack  | 1.454 | 1.625  | 1.703  | 1.708  | 1.713  | 1.63  | 100.0%  | 10    |
    | heat.delete_stack  | 1.387 | 1.57   | 2.717  | 2.724  | 2.731  | 1.88  | 100.0%  | 10    |
    | total              | 8.994 | 9.448  | 10.723 | 10.75  | 10.777 | 9.627 | 100.0%  | 10    |
    +--------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 28.125330925
    Full duration: 37.9011991024



    test scenario HeatStacks.create_and_delete_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 4.098 | 4.267  | 4.383  | 4.452  | 4.52  | 4.266 | 100.0%  | 10    |
    | heat.delete_stack | 1.423 | 1.468  | 1.536  | 1.679  | 1.822 | 1.505 | 100.0%  | 10    |
    | total             | 5.574 | 5.769  | 5.922  | 5.933  | 5.944 | 5.77  | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 17.2579169273
    Full duration: 27.4368560314



    test scenario HeatStacks.create_and_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 25.037 | 28.231 | 29.801 | 29.828 | 29.856 | 27.99  | 100.0%  | 10    |
    | heat.delete_stack | 10.707 | 11.831 | 13.046 | 13.573 | 14.099 | 12.249 | 100.0%  | 10    |
    | total             | 36.902 | 40.321 | 42.736 | 42.79  | 42.844 | 40.24  | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 119.344232082
    Full duration: 129.710185051



    test scenario HeatStacks.create_and_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 21.352 | 24.853 | 26.526 | 26.562 | 26.598 | 24.433 | 100.0%  | 10    |
    | heat.delete_stack | 9.51   | 10.67  | 10.95  | 11.42  | 11.889 | 10.684 | 100.0%  | 10    |
    | total             | 31.928 | 35.457 | 37.299 | 37.449 | 37.598 | 35.117 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 106.840685844
    Full duration: 117.40921998



    test scenario HeatStacks.list_stacks_and_resources
    +------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                         |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.list_stacks                | 0.488 | 0.522  | 0.539  | 0.54   | 0.54  | 0.522 | 100.0%  | 10    |
    | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0   | 0.0   | 100.0%  | 10    |
    | total                           | 0.488 | 0.522  | 0.539  | 0.54   | 0.541 | 0.522 | 100.0%  | 10    |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.59450078011
    Full duration: 9.86936807632



    test scenario HeatStacks.create_update_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 3.845 | 4.214  | 4.356  | 4.377  | 4.397  | 4.193  | 100.0%  | 10    |
    | heat.update_stack | 3.558 | 3.774  | 3.853  | 3.855  | 3.857  | 3.726  | 100.0%  | 10    |
    | heat.delete_stack | 1.56  | 2.57   | 2.756  | 2.776  | 2.797  | 2.512  | 100.0%  | 10    |
    | total             | 9.445 | 10.455 | 10.866 | 10.915 | 10.963 | 10.431 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 31.3620579243
    Full duration: 42.2799968719



    test scenario HeatStacks.create_update_delete_stack
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack | 4.133 | 4.157  | 4.354  | 4.413  | 4.472  | 4.209 | 100.0%  | 10    |
    | heat.update_stack | 3.534 | 3.713  | 3.821  | 3.958  | 4.096  | 3.717 | 100.0%  | 10    |
    | heat.delete_stack | 1.383 | 1.402  | 1.736  | 2.156  | 2.575  | 1.556 | 100.0%  | 10    |
    | total             | 9.126 | 9.41   | 9.772  | 10.018 | 10.263 | 9.482 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 29.0769648552
    Full duration: 39.4647920132



    test scenario HeatStacks.create_update_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack | 4.275  | 4.465  | 4.666  | 4.855  | 5.044  | 4.509 | 100.0%  | 10    |
    | heat.update_stack | 5.801  | 5.876  | 6.0    | 6.166  | 6.332  | 5.928 | 100.0%  | 10    |
    | heat.delete_stack | 2.525  | 2.564  | 3.649  | 3.683  | 3.717  | 2.793 | 100.0%  | 10    |
    | total             | 12.743 | 13.005 | 13.996 | 14.01  | 14.023 | 13.23 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 39.5067877769
    Full duration: 50.3663468361



    test scenario HeatStacks.create_update_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack | 4.517  | 5.462  | 5.602  | 5.608  | 5.614  | 5.389 | 100.0%  | 10    |
    | heat.update_stack | 8.345  | 9.324  | 9.403  | 9.411  | 9.42   | 9.245 | 100.0%  | 10    |
    | heat.delete_stack | 3.69   | 3.723  | 3.746  | 3.755  | 3.763  | 3.725 | 100.0%  | 10    |
    | total             | 17.515 | 18.525 | 18.645 | 18.683 | 18.722 | 18.36 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 54.7039349079
    Full duration: 65.6854679585



    test scenario HeatStacks.create_update_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 4.122  | 4.348  | 4.549  | 4.597  | 4.645  | 4.358  | 100.0%  | 10    |
    | heat.update_stack | 5.791  | 5.87   | 5.92   | 5.932  | 5.944  | 5.864  | 100.0%  | 10    |
    | heat.delete_stack | 2.506  | 2.55   | 3.704  | 3.778  | 3.853  | 2.791  | 100.0%  | 10    |
    | total             | 12.485 | 12.814 | 13.98  | 14.075 | 14.169 | 13.013 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 38.5906641483
    Full duration: 49.8386061192



    test scenario HeatStacks.create_update_delete_stack
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack | 4.062 | 4.33   | 4.493  | 4.501  | 4.508  | 4.317 | 100.0%  | 10    |
    | heat.update_stack | 3.553 | 3.585  | 3.783  | 3.936  | 4.088  | 3.648 | 100.0%  | 10    |
    | heat.delete_stack | 1.376 | 1.418  | 2.552  | 2.555  | 2.558  | 1.856 | 100.0%  | 10    |
    | total             | 9.179 | 9.535  | 10.607 | 10.678 | 10.749 | 9.822 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 29.5593960285
    Full duration: 40.873290062



    test scenario HeatStacks.create_and_list_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 4.105 | 4.264  | 4.394  | 4.43   | 4.466 | 4.276 | 100.0%  | 10    |
    | heat.list_stacks  | 0.062 | 0.103  | 0.113  | 0.116  | 0.119 | 0.096 | 100.0%  | 10    |
    | total             | 4.18  | 4.373  | 4.501  | 4.531  | 4.561 | 4.371 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 13.1703698635
    Full duration: 29.690456152



    test scenario HeatStacks.create_check_delete_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 4.194 | 4.357  | 4.595  | 4.64   | 4.684 | 4.393 | 100.0%  | 10    |
    | heat.check_stack  | 1.511 | 1.542  | 1.627  | 1.753  | 1.88  | 1.58  | 100.0%  | 10    |
    | heat.delete_stack | 1.402 | 2.55   | 2.707  | 2.749  | 2.791 | 2.257 | 100.0%  | 10    |
    | total             | 7.411 | 8.429  | 8.66   | 8.745  | 8.829 | 8.23  | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 24.4679090977
    Full duration: 35.6907479763



    run_rally - INFO - Test scenario: "heat" OK.

    run_rally - INFO - Starting test scenario "keystone" ...
    run_rally - INFO -
     Preparing input task
     Task  416065d0-3811-4bee-9b53-37743e1f179c: started
    Task 416065d0-3811-4bee-9b53-37743e1f179c: finished

    test scenario KeystoneBasic.create_tenant_with_users
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.285 | 0.297  | 0.328  | 0.336  | 0.343 | 0.305 | 100.0%  | 10    |
    | keystone.create_users  | 1.651 | 1.673  | 1.73   | 1.749  | 1.768 | 1.688 | 100.0%  | 10    |
    | total                  | 1.952 | 1.986  | 2.027  | 2.061  | 2.095 | 1.993 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 5.98874807358
    Full duration: 22.4405510426



    test scenario KeystoneBasic.create_add_and_list_user_roles
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.287 | 0.308  | 0.404  | 0.428  | 0.452 | 0.331 | 100.0%  | 10    |
    | keystone.add_role    | 0.276 | 0.31   | 0.371  | 0.379  | 0.388 | 0.319 | 100.0%  | 10    |
    | keystone.list_roles  | 0.137 | 0.151  | 0.175  | 0.207  | 0.239 | 0.16  | 100.0%  | 10    |
    | total                | 0.732 | 0.775  | 0.951  | 0.962  | 0.972 | 0.809 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.38230800629
    Full duration: 15.068157196



    test scenario KeystoneBasic.add_and_remove_user_role
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.263 | 0.3    | 0.41   | 0.455  | 0.499 | 0.336 | 100.0%  | 10    |
    | keystone.add_role    | 0.265 | 0.28   | 0.342  | 0.405  | 0.468 | 0.302 | 100.0%  | 10    |
    | keystone.remove_role | 0.151 | 0.182  | 0.347  | 0.35   | 0.354 | 0.226 | 100.0%  | 10    |
    | total                | 0.713 | 0.844  | 1.002  | 1.019  | 1.036 | 0.864 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.52822303772
    Full duration: 15.38514781



    test scenario KeystoneBasic.create_update_and_delete_tenant
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.267 | 0.354  | 0.411  | 0.421  | 0.432 | 0.346 | 100.0%  | 10    |
    | keystone.update_tenant | 0.139 | 0.15   | 0.185  | 0.223  | 0.262 | 0.164 | 100.0%  | 10    |
    | keystone.delete_tenant | 0.302 | 0.333  | 0.418  | 0.448  | 0.477 | 0.35  | 100.0%  | 10    |
    | total                  | 0.738 | 0.879  | 0.917  | 0.961  | 1.006 | 0.86  | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.55070900917
    Full duration: 14.2816069126



    test scenario KeystoneBasic.create_and_delete_service
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_service | 0.279 | 0.303  | 0.408  | 0.41   | 0.412 | 0.322 | 100.0%  | 10    |
    | keystone.delete_service | 0.15  | 0.168  | 0.188  | 0.192  | 0.196 | 0.169 | 100.0%  | 10    |
    | total                   | 0.443 | 0.471  | 0.584  | 0.594  | 0.604 | 0.491 | 100.0%  | 10    |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.47291088104
    Full duration: 12.6235470772



    test scenario KeystoneBasic.create_tenant
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.274 | 0.302  | 0.315  | 0.324  | 0.334 | 0.301 | 100.0%  | 10    |
    | total                  | 0.274 | 0.302  | 0.315  | 0.325  | 0.334 | 0.301 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.926929950714
    Full duration: 9.11541318893



    test scenario KeystoneBasic.create_user
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_user | 0.285 | 0.312  | 0.353  | 0.392  | 0.431 | 0.323 | 100.0%  | 10    |
    | total                | 0.285 | 0.313  | 0.353  | 0.392  | 0.431 | 0.323 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.09427213669
    Full duration: 9.44248485565



    test scenario KeystoneBasic.create_and_list_tenants
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.276 | 0.302  | 0.312  | 0.315  | 0.318 | 0.299 | 100.0%  | 10    |
    | keystone.list_tenants  | 0.133 | 0.141  | 0.147  | 0.149  | 0.15  | 0.141 | 100.0%  | 10    |
    | total                  | 0.416 | 0.441  | 0.462  | 0.463  | 0.463 | 0.44  | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.356580019
    Full duration: 14.5843369961



    test scenario KeystoneBasic.create_and_delete_role
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.271 | 0.306  | 0.517  | 0.532  | 0.547 | 0.37  | 100.0%  | 10    |
    | keystone.delete_role | 0.295 | 0.305  | 0.621  | 0.655  | 0.689 | 0.401 | 100.0%  | 10    |
    | total                | 0.572 | 0.743  | 0.991  | 1.076  | 1.16  | 0.771 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.24743795395
    Full duration: 14.336769104



    test scenario KeystoneBasic.get_entities
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.284 | 0.313  | 0.395  | 0.4    | 0.405 | 0.328 | 100.0%  | 10    |
    | keystone.create_user   | 0.141 | 0.155  | 0.176  | 0.176  | 0.177 | 0.159 | 100.0%  | 10    |
    | keystone.create_role   | 0.136 | 0.155  | 0.173  | 0.209  | 0.245 | 0.16  | 100.0%  | 10    |
    | keystone.get_tenant    | 0.124 | 0.132  | 0.143  | 0.144  | 0.144 | 0.133 | 100.0%  | 10    |
    | keystone.get_user      | 0.124 | 0.141  | 0.232  | 0.234  | 0.237 | 0.158 | 100.0%  | 10    |
    | keystone.get_role      | 0.122 | 0.125  | 0.142  | 0.144  | 0.147 | 0.129 | 100.0%  | 10    |
    | keystone.service_list  | 0.121 | 0.13   | 0.138  | 0.139  | 0.139 | 0.13  | 100.0%  | 10    |
    | keystone.get_service   | 0.118 | 0.132  | 0.158  | 0.16   | 0.161 | 0.136 | 100.0%  | 10    |
    | total                  | 1.253 | 1.315  | 1.403  | 1.449  | 1.495 | 1.334 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.18330001831
    Full duration: 21.2465929985



    test scenario KeystoneBasic.create_and_list_users
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_user | 0.27  | 0.324  | 0.381  | 0.409  | 0.436 | 0.33  | 100.0%  | 10    |
    | keystone.list_users  | 0.125 | 0.142  | 0.183  | 0.233  | 0.283 | 0.157 | 100.0%  | 10    |
    | total                | 0.409 | 0.47   | 0.53   | 0.625  | 0.719 | 0.487 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.41358304024
    Full duration: 9.46058607101



    run_rally - INFO - Test scenario: "keystone" OK.

    run_rally - INFO - Starting test scenario "neutron" ...
    run_rally - INFO -
     Preparing input task
     Task  66bee4c3-3b3f-4215-9910-63425b400d9a: started
    Task 66bee4c3-3b3f-4215-9910-63425b400d9a: finished

    test scenario NeutronNetworks.create_and_delete_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.762 | 0.83   | 0.953  | 0.983  | 1.014 | 0.858 | 100.0%  | 10    |
    | neutron.delete_port | 0.224 | 0.62   | 0.763  | 0.78   | 0.797 | 0.582 | 100.0%  | 10    |
    | total               | 1.011 | 1.549  | 1.599  | 1.603  | 1.607 | 1.441 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.14246201515
    Full duration: 53.9938690662



    test scenario NeutronNetworks.create_and_list_routers
    +---------------------------------------------------------------------------------------------------+
    |                                       Response Times (sec)                                        |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet        | 0.718 | 0.792  | 0.884  | 0.89   | 0.895 | 0.801 | 100.0%  | 10    |
    | neutron.create_router        | 0.435 | 0.451  | 0.555  | 0.56   | 0.565 | 0.474 | 100.0%  | 10    |
    | neutron.add_interface_router | 0.341 | 0.776  | 1.004  | 1.11   | 1.215 | 0.789 | 100.0%  | 10    |
    | neutron.list_routers         | 0.066 | 0.42   | 0.477  | 0.491  | 0.505 | 0.367 | 100.0%  | 10    |
    | total                        | 1.661 | 2.48   | 2.738  | 2.797  | 2.855 | 2.431 | 100.0%  | 10    |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 7.12932991982
    Full duration: 59.6318800449



    test scenario NeutronNetworks.create_and_delete_routers
    +------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                         |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet           | 0.739 | 0.812  | 0.936  | 0.949  | 0.963 | 0.833 | 100.0%  | 10    |
    | neutron.create_router           | 0.073 | 0.467  | 0.548  | 0.564  | 0.58  | 0.447 | 100.0%  | 10    |
    | neutron.add_interface_router    | 0.32  | 0.758  | 0.881  | 0.901  | 0.92  | 0.737 | 100.0%  | 10    |
    | neutron.remove_interface_router | 0.632 | 0.723  | 0.767  | 0.788  | 0.808 | 0.719 | 100.0%  | 10    |
    | neutron.delete_router           | 0.575 | 0.622  | 0.72   | 0.74   | 0.759 | 0.639 | 100.0%  | 10    |
    | total                           | 2.939 | 3.398  | 3.635  | 3.725  | 3.814 | 3.375 | 100.0%  | 10    |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 10.4781250954
    Full duration: 61.2645328045



    test scenario NeutronNetworks.create_and_list_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.728 | 0.859  | 0.909  | 0.944  | 0.978 | 0.857 | 100.0%  | 10    |
    | neutron.list_ports  | 0.52  | 0.599  | 0.71   | 0.735  | 0.76  | 0.618 | 100.0%  | 10    |
    | total               | 1.37  | 1.459  | 1.597  | 1.611  | 1.624 | 1.475 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.50073218346
    Full duration: 55.2021510601



    test scenario NeutronNetworks.create_and_delete_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.749 | 0.788  | 0.939  | 0.956  | 0.972 | 0.824 | 100.0%  | 10    |
    | neutron.delete_subnet | 0.556 | 0.673  | 0.778  | 0.819  | 0.859 | 0.687 | 100.0%  | 10    |
    | total                 | 1.361 | 1.521  | 1.693  | 1.697  | 1.702 | 1.511 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.66956591606
    Full duration: 54.1284301281



    test scenario NeutronNetworks.create_and_delete_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.62  | 0.643  | 0.756  | 0.784  | 0.812 | 0.672 | 100.0%  | 10    |
    | neutron.delete_network | 0.481 | 0.54   | 0.616  | 0.686  | 0.756 | 0.558 | 100.0%  | 10    |
    | total                  | 1.101 | 1.206  | 1.363  | 1.377  | 1.391 | 1.23  | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.73822879791
    Full duration: 33.2811751366



    test scenario NeutronNetworks.create_and_list_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.583 | 0.675  | 0.782  | 0.782  | 0.783 | 0.691 | 100.0%  | 10    |
    | neutron.list_networks  | 0.058 | 0.395  | 0.517  | 0.522  | 0.528 | 0.364 | 100.0%  | 10    |
    | total                  | 0.834 | 1.066  | 1.187  | 1.242  | 1.298 | 1.055 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.09279990196
    Full duration: 33.633177042



    test scenario NeutronNetworks.create_and_update_routers
    +---------------------------------------------------------------------------------------------------+
    |                                       Response Times (sec)                                        |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet        | 0.713 | 0.8    | 0.903  | 0.913  | 0.922 | 0.811 | 100.0%  | 10    |
    | neutron.create_router        | 0.434 | 0.449  | 0.476  | 0.497  | 0.519 | 0.458 | 100.0%  | 10    |
    | neutron.add_interface_router | 0.666 | 0.749  | 0.912  | 0.954  | 0.996 | 0.791 | 100.0%  | 10    |
    | neutron.update_router        | 0.222 | 0.579  | 0.659  | 0.678  | 0.697 | 0.556 | 100.0%  | 10    |
    | total                        | 2.156 | 2.643  | 2.768  | 2.799  | 2.83  | 2.617 | 100.0%  | 10    |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 7.76268601418
    Full duration: 57.6214001179



    test scenario NeutronNetworks.create_and_update_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.606 | 0.672  | 0.761  | 0.785  | 0.81  | 0.681 | 100.0%  | 10    |
    | neutron.update_network | 0.137 | 0.518  | 0.538  | 0.542  | 0.547 | 0.482 | 100.0%  | 10    |
    | total                  | 0.893 | 1.183  | 1.261  | 1.288  | 1.315 | 1.164 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.59189605713
    Full duration: 34.8437690735



    test scenario NeutronNetworks.create_and_update_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.738 | 0.792  | 0.889  | 0.921  | 0.952 | 0.815 | 100.0%  | 10    |
    | neutron.update_port | 0.161 | 0.551  | 0.596  | 0.6    | 0.605 | 0.516 | 100.0%  | 10    |
    | total               | 1.044 | 1.339  | 1.429  | 1.482  | 1.536 | 1.331 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.11195087433
    Full duration: 53.0145220757



    test scenario NeutronNetworks.create_and_list_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.703 | 0.748  | 0.832  | 0.861  | 0.89  | 0.764 | 100.0%  | 10    |
    | neutron.list_subnets  | 0.054 | 0.396  | 0.445  | 0.479  | 0.513 | 0.374 | 100.0%  | 10    |
    | total                 | 0.757 | 1.159  | 1.256  | 1.272  | 1.287 | 1.138 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.5137629509
    Full duration: 52.7622568607



    test scenario NeutronNetworks.create_and_update_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.742 | 0.813  | 0.947  | 0.948  | 0.949 | 0.838 | 100.0%  | 10    |
    | neutron.update_subnet | 0.234 | 0.583  | 0.695  | 0.696  | 0.696 | 0.58  | 100.0%  | 10    |
    | total                 | 1.043 | 1.427  | 1.587  | 1.596  | 1.604 | 1.418 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.36762094498
    Full duration: 54.1341950893



    run_rally - INFO - Test scenario: "neutron" OK.

    run_rally - INFO - Starting test scenario "nova" ...
    run_rally - INFO -
     Preparing input task
     Task  c631be68-64eb-462f-af72-0946f649719e: started
    Task c631be68-64eb-462f-af72-0946f649719e: finished

    test scenario NovaKeypair.create_and_delete_keypair
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | nova.create_keypair | 0.689 | 0.825  | 1.389  | 1.414  | 1.439 | 0.956 | 100.0%  | 10    |
    | nova.delete_keypair | 0.034 | 0.045  | 0.058  | 0.058  | 0.059 | 0.046 | 100.0%  | 10    |
    | total               | 0.734 | 0.868  | 1.43   | 1.458  | 1.487 | 1.002 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.95623397827
    Full duration: 43.0288610458



    test scenario NovaServers.snapshot_server
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server       | 13.069 | 14.075 | 14.775 | 15.063 | 15.35  | 14.118 | 100.0%  | 10    |
    | nova.create_image      | 10.992 | 11.363 | 11.948 | 12.03  | 12.112 | 11.402 | 100.0%  | 10    |
    | nova.delete_server     | 2.878  | 3.026  | 3.413  | 3.454  | 3.495  | 3.121  | 100.0%  | 10    |
    | nova.boot_server (2)   | 10.807 | 12.891 | 14.009 | 14.098 | 14.188 | 12.932 | 100.0%  | 10    |
    | nova.delete_server (2) | 2.914  | 3.356  | 4.738  | 4.974  | 5.21   | 3.557  | 100.0%  | 10    |
    | nova.delete_image      | 2.769  | 3.227  | 3.659  | 3.685  | 3.711  | 3.238  | 100.0%  | 10    |
    | total                  | 44.842 | 48.482 | 49.94  | 50.257 | 50.573 | 48.369 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 145.116047144
    Full duration: 218.130707026



    test scenario NovaKeypair.boot_and_delete_server_with_keypair
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_keypair | 0.67   | 0.815  | 1.452  | 1.483  | 1.515  | 0.945  | 100.0%  | 10    |
    | nova.boot_server    | 11.229 | 12.914 | 14.714 | 15.148 | 15.581 | 13.075 | 100.0%  | 10    |
    | nova.delete_server  | 2.87   | 3.313  | 3.4    | 3.451  | 3.502  | 3.214  | 100.0%  | 10    |
    | nova.delete_keypair | 0.034  | 0.048  | 0.056  | 0.056  | 0.057  | 0.046  | 100.0%  | 10    |
    | total               | 15.3   | 17.062 | 18.916 | 19.109 | 19.302 | 17.281 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 51.5624389648
    Full duration: 121.866284132



    test scenario NovaKeypair.create_and_list_keypairs
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | nova.create_keypair | 0.681 | 0.825  | 1.368  | 1.468  | 1.568 | 0.975 | 100.0%  | 10    |
    | nova.list_keypairs  | 0.021 | 0.027  | 0.038  | 0.038  | 0.039 | 0.03  | 100.0%  | 10    |
    | total               | 0.715 | 0.855  | 1.394  | 1.494  | 1.593 | 1.005 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.00225996971
    Full duration: 44.8396139145



    test scenario NovaServers.list_servers
    +---------------------------------------------------------------------------------------+
    |                                 Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg  | success | count |
    +-------------------+-------+--------+--------+--------+-------+------+---------+-------+
    | nova.list_servers | 1.385 | 1.648  | 1.794  | 1.8    | 1.806 | 1.64 | 100.0%  | 10    |
    | total             | 1.386 | 1.648  | 1.794  | 1.8    | 1.807 | 1.64 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+------+---------+-------+
    Load duration: 4.86725592613
    Full duration: 144.563478947



    test scenario NovaServers.resize_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 11.794 | 13.235 | 14.683 | 15.23  | 15.778 | 13.569 | 100.0%  | 10    |
    | nova.resize         | 40.775 | 43.909 | 47.803 | 47.888 | 47.973 | 44.294 | 100.0%  | 10    |
    | nova.resize_confirm | 2.664  | 3.406  | 5.701  | 5.894  | 6.087  | 3.777  | 100.0%  | 10    |
    | nova.delete_server  | 2.831  | 2.964  | 3.671  | 4.355  | 5.038  | 3.264  | 100.0%  | 10    |
    | total               | 59.51  | 64.72  | 68.963 | 69.477 | 69.991 | 64.905 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 193.15106678
    Full duration: 234.439800978



    test scenario NovaServers.boot_server_from_volume_and_delete
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 9.703  | 10.351 | 11.374 | 12.306 | 13.237 | 10.631 | 100.0%  | 10    |
    | nova.boot_server     | 13.02  | 14.474 | 15.965 | 16.121 | 16.276 | 14.667 | 100.0%  | 10    |
    | nova.delete_server   | 3.826  | 5.813  | 5.967  | 6.081  | 6.196  | 5.561  | 100.0%  | 10    |
    | total                | 27.612 | 30.787 | 32.582 | 32.736 | 32.891 | 30.859 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 92.1244728565
    Full duration: 176.439888954



    test scenario NovaServers.boot_and_migrate_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 12.068 | 13.808 | 14.866 | 14.966 | 15.067 | 13.788 | 100.0%  | 10    |
    | nova.stop_server    | 4.417  | 6.774  | 7.032  | 7.224  | 7.416  | 6.512  | 100.0%  | 10    |
    | nova.migrate        | 10.786 | 11.454 | 11.957 | 11.999 | 12.04  | 11.487 | 100.0%  | 10    |
    | nova.resize_confirm | 3.328  | 3.614  | 3.822  | 3.905  | 3.988  | 3.621  | 100.0%  | 10    |
    | nova.delete_server  | 2.862  | 3.057  | 3.364  | 3.454  | 3.544  | 3.116  | 100.0%  | 10    |
    | total               | 34.85  | 38.711 | 40.179 | 40.344 | 40.508 | 38.525 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 115.221567869
    Full duration: 156.790792227



    test scenario NovaServers.boot_and_delete_server
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action             | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server   | 12.492 | 13.618 | 14.995 | 15.0   | 15.004 | 13.701 | 100.0%  | 10    |
    | nova.delete_server | 2.88   | 3.033  | 3.371  | 3.49   | 3.61   | 3.125  | 100.0%  | 10    |
    | total              | 15.773 | 16.838 | 17.914 | 18.089 | 18.264 | 16.827 | 100.0%  | 10    |
    +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 50.1218390465
    Full duration: 119.306482077



    test scenario NovaServers.boot_and_rebuild_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 12.196 | 13.798 | 15.074 | 15.293 | 15.511 | 13.812 | 100.0%  | 10    |
    | nova.rebuild_server | 12.036 | 13.891 | 15.523 | 15.599 | 15.676 | 13.972 | 100.0%  | 10    |
    | nova.delete_server  | 2.645  | 3.268  | 3.55   | 3.589  | 3.628  | 3.208  | 100.0%  | 10    |
    | total               | 28.349 | 31.175 | 32.771 | 33.141 | 33.511 | 30.993 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 92.8703818321
    Full duration: 164.587569952



    test scenario NovaSecGroup.create_and_list_secgroups
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups | 4.388  | 5.032  | 5.224  | 5.25   | 5.277  | 4.975  | 100.0%  | 10    |
    | nova.create_100_rules          | 42.993 | 44.613 | 45.762 | 45.785 | 45.808 | 44.39  | 100.0%  | 10    |
    | nova.list_security_groups      | 0.153  | 0.195  | 0.36   | 0.486  | 0.613  | 0.251  | 100.0%  | 10    |
    | total                          | 48.225 | 50.01  | 50.441 | 50.635 | 50.83  | 49.616 | 100.0%  | 10    |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 149.417917013
    Full duration: 217.353839159



    test scenario NovaSecGroup.create_and_delete_secgroups
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups | 4.382  | 5.191  | 5.496  | 5.608  | 5.72   | 5.12   | 100.0%  | 10    |
    | nova.create_100_rules          | 43.059 | 44.368 | 45.778 | 46.029 | 46.28  | 44.458 | 100.0%  | 10    |
    | nova.delete_10_security_groups | 1.662  | 2.265  | 2.495  | 2.664  | 2.832  | 2.215  | 100.0%  | 10    |
    | total                          | 50.772 | 51.601 | 53.26  | 53.294 | 53.327 | 51.794 | 100.0%  | 10    |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 156.369856119
    Full duration: 199.137834787



    test scenario NovaServers.boot_and_bounce_server
    +-------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                       |
    +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                  | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server        | 12.013 | 14.52  | 15.332 | 15.8   | 16.267 | 14.249 | 100.0%  | 10    |
    | nova.reboot_server      | 5.223  | 6.071  | 6.385  | 6.462  | 6.539  | 5.987  | 100.0%  | 10    |
    | nova.soft_reboot_server | 5.766  | 8.423  | 8.806  | 9.002  | 9.198  | 8.214  | 100.0%  | 10    |
    | nova.stop_server        | 3.892  | 6.503  | 7.587  | 10.894 | 14.201 | 6.898  | 100.0%  | 10    |
    | nova.start_server       | 3.432  | 4.687  | 5.177  | 5.424  | 5.672  | 4.587  | 100.0%  | 10    |
    | nova.rescue_server      | 7.9    | 8.519  | 9.688  | 10.196 | 10.703 | 8.724  | 100.0%  | 10    |
    | nova.unrescue_server    | 5.091  | 5.518  | 5.836  | 6.131  | 6.426  | 5.577  | 100.0%  | 10    |
    | nova.delete_server      | 2.495  | 2.921  | 3.469  | 3.516  | 3.563  | 2.974  | 100.0%  | 10    |
    | total                   | 53.649 | 57.305 | 59.111 | 60.626 | 62.142 | 57.23  | 100.0%  | 10    |
    +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 174.621170044
    Full duration: 245.828352928



    test scenario NovaServers.boot_server
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action           | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server | 13.233 | 14.359 | 15.326 | 15.425 | 15.523 | 14.261 | 100.0%  | 10    |
    | total            | 13.234 | 14.359 | 15.326 | 15.425 | 15.523 | 14.261 | 100.0%  | 10    |
    +------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 42.6567699909
    Full duration: 99.771146059



    test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
    +-----------------------------------------------------------------------------------------------------------+
    |                                           Response Times (sec)                                            |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups    | 4.306  | 4.999  | 5.282  | 5.289  | 5.296  | 4.937  | 100.0%  | 10    |
    | nova.create_100_rules             | 41.795 | 43.955 | 45.983 | 46.201 | 46.418 | 44.135 | 100.0%  | 10    |
    | nova.boot_server                  | 10.075 | 11.651 | 12.302 | 13.061 | 13.82  | 11.534 | 100.0%  | 10    |
    | nova.get_attached_security_groups | 0.217  | 0.249  | 0.568  | 0.572  | 0.577  | 0.338  | 100.0%  | 10    |
    | nova.delete_server                | 2.469  | 2.619  | 2.937  | 3.034  | 3.131  | 2.712  | 100.0%  | 10    |
    | nova.delete_10_security_groups    | 1.574  | 1.878  | 2.55   | 2.704  | 2.858  | 2.053  | 100.0%  | 10    |
    | total                             | 63.097 | 65.905 | 66.858 | 67.329 | 67.8   | 65.71  | 100.0%  | 10    |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 195.037164927
    Full duration: 263.490648985



    test scenario NovaServers.pause_and_unpause_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 12.325 | 13.238 | 14.398 | 14.542 | 14.687 | 13.373 | 100.0%  | 10    |
    | nova.pause_server   | 2.412  | 2.986  | 3.177  | 3.205  | 3.233  | 2.946  | 100.0%  | 10    |
    | nova.unpause_server | 2.824  | 3.169  | 3.325  | 3.392  | 3.459  | 3.13   | 100.0%  | 10    |
    | nova.delete_server  | 2.501  | 3.244  | 3.557  | 3.634  | 3.71   | 3.233  | 100.0%  | 10    |
    | total               | 21.499 | 22.307 | 24.0   | 24.022 | 24.043 | 22.682 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 67.2968730927
    Full duration: 134.783083916



    test scenario NovaServers.boot_server_from_volume
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 9.885  | 10.866 | 11.617 | 11.636 | 11.655 | 10.841 | 100.0%  | 10    |
    | nova.boot_server     | 13.236 | 14.774 | 15.766 | 16.126 | 16.486 | 14.693 | 100.0%  | 10    |
    | total                | 23.437 | 25.64  | 27.197 | 27.213 | 27.23  | 25.534 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 78.3072631359
    Full duration: 145.979751825



    test scenario NovaServers.boot_and_list_server
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server  | 12.745 | 14.15  | 15.755 | 15.872 | 15.99  | 14.143 | 100.0%  | 10    |
    | nova.list_servers | 0.579  | 0.977  | 1.114  | 1.158  | 1.203  | 0.926  | 100.0%  | 10    |
    | total             | 13.49  | 14.979 | 16.933 | 16.94  | 16.947 | 15.07  | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 46.7471969128
    Full duration: 130.989289045



    run_rally - INFO - Test scenario: "nova" OK.

    run_rally - INFO - Starting test scenario "quotas" ...
    run_rally - INFO -
     Preparing input task
     Task  09c70711-40eb-4c85-8b87-c0c081222b0d: started
    Task 09c70711-40eb-4c85-8b87-c0c081222b0d: finished

    test scenario Quotas.cinder_update
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +----------------------+-------+--------+--------+--------+-------+------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg  | success | count |
    +----------------------+-------+--------+--------+--------+-------+------+---------+-------+
    | quotas.update_quotas | 1.123 | 1.192  | 1.297  | 1.331  | 1.365 | 1.21 | 100.0%  | 10    |
    | total                | 1.123 | 1.192  | 1.297  | 1.331  | 1.365 | 1.21 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+------+---------+-------+
    Load duration: 3.62791609764
    Full duration: 16.2237439156



    test scenario Quotas.neutron_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.396 | 0.426  | 0.572  | 0.581  | 0.591 | 0.464 | 100.0%  | 10    |
    | total                | 0.553 | 0.575  | 0.773  | 0.834  | 0.896 | 0.64  | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.80940699577
    Full duration: 13.0895729065



    test scenario Quotas.cinder_update_and_delete
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 1.145 | 1.182  | 1.365  | 1.407  | 1.449 | 1.234 | 100.0%  | 10    |
    | quotas.delete_quotas | 0.543 | 0.933  | 1.011  | 1.032  | 1.053 | 0.873 | 100.0%  | 10    |
    | total                | 1.723 | 2.095  | 2.413  | 2.435  | 2.456 | 2.107 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 6.34634900093
    Full duration: 18.2702391148



    test scenario Quotas.nova_update_and_delete
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.544 | 0.621  | 0.695  | 0.705  | 0.716 | 0.619 | 100.0%  | 10    |
    | quotas.delete_quotas | 0.017 | 0.023  | 0.028  | 0.028  | 0.029 | 0.024 | 100.0%  | 10    |
    | total                | 0.569 | 0.642  | 0.713  | 0.726  | 0.739 | 0.643 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.95026016235
    Full duration: 13.2278659344



    test scenario Quotas.nova_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.571 | 0.647  | 0.664  | 0.692  | 0.719 | 0.643 | 100.0%  | 10    |
    | total                | 0.571 | 0.647  | 0.664  | 0.692  | 0.719 | 0.644 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.94177007675
    Full duration: 13.6731410027



    run_rally - INFO - Test scenario: "quotas" OK.

    run_rally - INFO - Starting test scenario "requests" ...
    run_rally - INFO -
     Preparing input task
     Task  ee8c572e-1240-4996-a06f-801592da0277: started
    Task ee8c572e-1240-4996-a06f-801592da0277: finished

    test scenario HttpRequests.check_random_request
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | requests.check_request | 0.047 | 0.201  | 0.383  | 0.384  | 0.386 | 0.214 | 100.0%  | 10    |
    | total                  | 0.047 | 0.201  | 0.383  | 0.384  | 0.386 | 0.214 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.791751146317
    Full duration: 5.66926693916



    test scenario HttpRequests.check_request
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | requests.check_request | 0.044 | 0.046  | 0.052  | 0.052  | 0.053 | 0.048 | 100.0%  | 10    |
    | total                  | 0.044 | 0.046  | 0.052  | 0.052  | 0.053 | 0.048 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.181750059128
    Full duration: 5.16227507591



    run_rally - INFO - Test scenario: "requests" OK.

    run_rally - INFO -


                         Rally Summary Report
    +===================+============+===============+===========+
    | Module            | Duration   | nb. Test Run  | Success   |
    +===================+============+===============+===========+
    | authenticate      | 00:59      | 10            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | glance            | 03:38      | 7             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | cinder            | 22:59      | 50            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | heat              | 11:16      | 35            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | keystone          | 02:37      | 29            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | neutron           | 10:03      | 31            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | nova              | 47:41      | 61            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | quotas            | 01:14      | 7             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | requests          | 00:10      | 2             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    +===================+============+===============+===========+
    | TOTAL:            | 01:40:41   | 232           | 100.00%   |
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
        "start": "2016-02-18T13:37:06.661Z",
        "end": "2016-02-18T13:37:12.962Z",
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


