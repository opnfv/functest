.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for fuel-os-odl_l2-nofeature-ha
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
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.49156   | success |
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.10940   | success |
    | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 15.01623  | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 29.41033  | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 13.86580  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.60879   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.34531   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.33518   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.96138   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.90751   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.62183   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.62195   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.33497   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.64235   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 1.23145   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.83801   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 1.18842   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.35784   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 1.09813   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 0.88696   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.84049   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 1.52238   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 3.63444   | success |
    | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 6.75102   | success |
    | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 14.44295  | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 316.24706 | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.34052   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.75888   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 316.38576 | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.00196   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 0.0       | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.0       | fail    |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.10067   | success |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 4.93829   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.78542   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.64749   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.89411   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.32315   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.91146   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.13496   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.11222   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.11119   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.09119   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.10776   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.57188   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00131   | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.20660   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.08830   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.02378   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.33571   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.10769   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.02694   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.02251   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.04963   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.07987   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.08196   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.92759   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.03606   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.09925   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 0.0       | fail    |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.10704   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.20889   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.78463   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.44852   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.37770   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.72001   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.74485   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.67380   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 4.65947   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 19.27912  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 22.83188  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 13.05190  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 10.22705  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 3.02970   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 4.04190   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 2.67671   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 3.10372   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 3.80641   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 2.05689   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 1.62404   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 1.47470   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 1.21997   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 2.20741   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 3.12907   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 1.56617   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 1.38405   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 1.74547   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.94955   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 1.62631   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 1.24089   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 1.28176   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 1.39299   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 0.59369   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 1.00537   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.35547   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.02691   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 0.77671   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.03595   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 0.67764   | success |
    | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.12390   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.35252   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.05395   | success |
    | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 343.72467 | fail    |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.95003   | success |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.99399   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.31689   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.02590   | success |
    | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.0       | fail    |
    | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.09974   | success |
    | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 1.21063   | success |
    | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.77355   | success |
    | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.0       | fail    |
    | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 2.63115   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.10751   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.08180   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.11419   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.09997   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.15346   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.10901   | success |
    | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.26936   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 1.78244   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 2.75904   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 3.58070   | success |
    | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 6.97865   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 0.0       | fail    |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 0.0       | fail    |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 2.19846   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 3.01338   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 5.65439   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 5.23138   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 4.63026   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 4.20924   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 3.23093   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.72657   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.45440   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.37147   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.35779   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.30639   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 3.21748   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.64248   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.30977   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.03731   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.49862   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.26355   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 3.12061   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 3.35577   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 1.94748   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.39794   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.33413   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 3.39562   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 5.89837   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 2.99973   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.58956   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.48395   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 10.99445  | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 6.94692   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 4.69234   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 0.56033   | fail    |
    | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 8.28629   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 4.94750   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 4.97154   | success |
    | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 3.42252   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 2.06578   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 3.53065   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.29313   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 2.98492   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 3.10014   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.39465   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.76994   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 7.29710   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.05370   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.0       | fail    |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 20.70674  | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 12.57512  | success |
    | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 2.94613   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 3.13954   | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 15.28613  | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 17.92871  | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 15.55119  | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 19.10263  | success |
    | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.07108   | success |
    | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.37294   | success |
    | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 25.63959  | fail    |
    | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 16.24070  | fail    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 343.58312 | fail    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 356.71394 | fail    |
    +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    run_tempest - INFO - Results: {'timestart': '2016-02-1905:28:37.031139', 'duration': 730, 'tests': 210, 'failures': 40}

Rally
^^^^^
::

    FUNCTEST.info: Running Rally benchmark suite...
    run_rally - INFO - Starting test scenario "authenticate" ...
    run_rally - INFO -
     Preparing input task
     Task  c7f4e0fd-a882-4e14-ba02-553118d0cb77: started
    Task c7f4e0fd-a882-4e14-ba02-553118d0cb77: finished

    test scenario Authenticate.validate_glance
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_glance     | 0.535 | 0.78   | 0.847  | 0.86   | 0.874 | 0.74  | 100.0%  | 10    |
    | authenticate.validate_glance (2) | 0.667 | 0.689  | 0.793  | 0.807  | 0.821 | 0.717 | 100.0%  | 10    |
    | total                            | 1.381 | 1.677  | 1.718  | 1.735  | 1.752 | 1.625 | 100.0%  | 10    |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.80417394638
    Full duration: 12.8028140068



    test scenario Authenticate.keystone
    +-----------------------------------------------------------------------------+
    |                            Response Times (sec)                             |
    +--------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------+-------+--------+--------+--------+-------+-------+---------+-------+
    | total  | 0.121 | 0.149  | 0.163  | 0.164  | 0.166 | 0.149 | 100.0%  | 10    |
    +--------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.489310979843
    Full duration: 7.96697187424



    test scenario Authenticate.validate_heat
    +-----------------------------------------------------------------------------------------------------+
    |                                        Response Times (sec)                                         |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_heat     | 0.259 | 0.318  | 0.482  | 0.511  | 0.539 | 0.371 | 100.0%  | 10    |
    | authenticate.validate_heat (2) | 0.051 | 0.287  | 0.385  | 0.386  | 0.387 | 0.24  | 100.0%  | 10    |
    | total                          | 0.512 | 0.771  | 0.957  | 0.996  | 1.035 | 0.776 | 100.0%  | 10    |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.53649091721
    Full duration: 10.2540290356



    test scenario Authenticate.validate_nova
    +-----------------------------------------------------------------------------------------------------+
    |                                        Response Times (sec)                                         |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_nova     | 0.3   | 0.332  | 0.474  | 0.482  | 0.489 | 0.368 | 100.0%  | 10    |
    | authenticate.validate_nova (2) | 0.034 | 0.049  | 0.059  | 0.065  | 0.07  | 0.05  | 100.0%  | 10    |
    | total                          | 0.499 | 0.564  | 0.716  | 0.722  | 0.727 | 0.586 | 100.0%  | 10    |
    +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.84303689003
    Full duration: 9.65319395065



    test scenario Authenticate.validate_cinder
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_cinder     | 0.274 | 0.428  | 0.475  | 0.509  | 0.543 | 0.405 | 100.0%  | 10    |
    | authenticate.validate_cinder (2) | 0.025 | 0.424  | 0.455  | 0.456  | 0.458 | 0.376 | 100.0%  | 10    |
    | total                            | 0.469 | 1.071  | 1.131  | 1.141  | 1.151 | 0.964 | 100.0%  | 10    |
    +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.72650790215
    Full duration: 10.753674984



    test scenario Authenticate.validate_neutron
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | authenticate.validate_neutron     | 0.28  | 0.302  | 0.32   | 0.326  | 0.333 | 0.303 | 100.0%  | 10    |
    | authenticate.validate_neutron (2) | 0.046 | 0.31   | 0.334  | 0.34   | 0.346 | 0.262 | 100.0%  | 10    |
    | total                             | 0.467 | 0.764  | 0.81   | 0.838  | 0.866 | 0.728 | 100.0%  | 10    |
    +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.37260484695
    Full duration: 9.99744796753



    run_rally - INFO - Test scenario: "authenticate" OK.

    run_rally - INFO - Starting test scenario "glance" ...
    run_rally - INFO -
     Preparing input task
     Task  d54fa25b-b992-4b4e-bef2-14425b86329c: started
    Task d54fa25b-b992-4b4e-bef2-14425b86329c: finished

    test scenario GlanceImages.list_images
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | glance.list_images | 0.877 | 0.902  | 0.997  | 0.998  | 0.999 | 0.932 | 100.0%  | 10    |
    | total              | 0.877 | 0.902  | 0.997  | 0.998  | 0.999 | 0.932 | 100.0%  | 10    |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.92263484001
    Full duration: 13.4585630894



    test scenario GlanceImages.create_image_and_boot_instances
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +---------------------+--------+--------+--------+--------+-------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max   | avg    | success | count |
    +---------------------+--------+--------+--------+--------+-------+--------+---------+-------+
    | glance.create_image | 7.386  | 7.929  | 8.381  | 8.481  | 8.581 | 7.97   | 100.0%  | 10    |
    | nova.boot_servers   | 8.641  | 10.384 | 10.714 | 11.007 | 11.3  | 10.241 | 100.0%  | 10    |
    | total               | 16.702 | 18.427 | 18.943 | 19.047 | 19.15 | 18.211 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+-------+--------+---------+-------+
    Load duration: 54.6946680546
    Full duration: 110.071588039



    test scenario GlanceImages.create_and_list_image
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | glance.create_image | 7.081 | 7.618  | 8.085  | 8.19   | 8.296 | 7.689 | 100.0%  | 10    |
    | glance.list_images  | 0.324 | 0.573  | 0.642  | 0.714  | 0.786 | 0.573 | 100.0%  | 10    |
    | total               | 7.612 | 8.241  | 8.722  | 8.902  | 9.082 | 8.262 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 24.6801600456
    Full duration: 39.2870121002



    test scenario GlanceImages.create_and_delete_image
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | glance.create_image | 7.449 | 7.593  | 7.856  | 8.073  | 8.289  | 7.673 | 100.0%  | 10    |
    | glance.delete_image | 2.001 | 2.442  | 12.75  | 13.42  | 14.089 | 5.507 | 100.0%  | 10    |
    | total               | 9.487 | 10.064 | 20.503 | 21.441 | 22.378 | 13.18 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 40.0675120354
    Full duration: 50.2370131016



    run_rally - INFO - Test scenario: "glance" OK.

    run_rally - INFO - Starting test scenario "cinder" ...
    run_rally - INFO -
     Preparing input task
     Task  6b2be534-fd42-4a5f-be0e-9a789027d4b3: started
    Task 6b2be534-fd42-4a5f-be0e-9a789027d4b3: finished

    test scenario CinderVolumes.create_and_attach_volume
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server     | 7.135  | 7.936  | 8.663  | 8.672  | 8.68   | 7.941  | 100.0%  | 10    |
    | cinder.create_volume | 3.274  | 3.507  | 4.072  | 4.096  | 4.12   | 3.616  | 100.0%  | 10    |
    | nova.attach_volume   | 4.012  | 4.845  | 6.553  | 6.624  | 6.694  | 5.31   | 100.0%  | 10    |
    | nova.detach_volume   | 3.256  | 3.739  | 3.938  | 4.096  | 4.253  | 3.716  | 100.0%  | 10    |
    | cinder.delete_volume | 0.464  | 2.707  | 2.98   | 3.154  | 3.328  | 1.98   | 100.0%  | 10    |
    | nova.delete_server   | 2.784  | 3.059  | 3.15   | 3.19   | 3.23   | 3.04   | 100.0%  | 10    |
    | total                | 22.316 | 26.079 | 27.631 | 28.362 | 29.094 | 25.604 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 73.9451169968
    Full duration: 116.516190052



    test scenario CinderVolumes.create_and_list_volume
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | cinder.create_volume | 9.065 | 9.591  | 9.94   | 9.943  | 9.945  | 9.554 | 100.0%  | 10    |
    | cinder.list_volumes  | 0.048 | 0.346  | 0.386  | 0.394  | 0.402  | 0.301 | 100.0%  | 10    |
    | total                | 9.138 | 9.94   | 10.313 | 10.324 | 10.335 | 9.855 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 28.8989629745
    Full duration: 51.7012848854



    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.251 | 3.883  | 4.897  | 4.899  | 4.901 | 4.006 | 100.0%  | 10    |
    | cinder.list_volumes  | 0.055 | 0.072  | 0.333  | 0.334  | 0.334 | 0.145 | 100.0%  | 10    |
    | total                | 3.313 | 3.952  | 5.212  | 5.223  | 5.234 | 4.151 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 11.7280011177
    Full duration: 34.1200621128



    test scenario CinderVolumes.create_and_list_snapshots
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_snapshot | 2.973 | 3.289  | 5.554  | 5.57   | 5.585 | 3.702 | 100.0%  | 10    |
    | cinder.list_snapshots  | 0.027 | 0.162  | 0.313  | 0.32   | 0.326 | 0.168 | 100.0%  | 10    |
    | total                  | 3.001 | 3.593  | 5.586  | 5.601  | 5.616 | 3.871 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 10.6676809788
    Full duration: 51.8370318413



    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.324 | 3.69   | 4.382  | 4.392  | 4.403 | 3.828 | 100.0%  | 10    |
    | cinder.delete_volume | 0.625 | 2.781  | 3.053  | 3.199  | 3.345 | 2.086 | 100.0%  | 10    |
    | total                | 4.288 | 6.438  | 7.073  | 7.173  | 7.273 | 5.914 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 18.0577061176
    Full duration: 35.664162159



    test scenario CinderVolumes.create_and_delete_volume
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +----------------------+------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min  | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 7.41 | 9.74   | 10.091 | 10.094 | 10.097 | 9.522  | 100.0%  | 10    |
    | cinder.delete_volume | 0.54 | 0.965  | 3.092  | 3.097  | 3.103  | 1.691  | 100.0%  | 10    |
    | total                | 7.95 | 10.903 | 12.9   | 12.964 | 13.029 | 11.214 | 100.0%  | 10    |
    +----------------------+------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 33.3823940754
    Full duration: 52.0277431011



    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.681 | 3.946  | 4.01   | 4.051  | 4.092 | 3.903 | 100.0%  | 10    |
    | cinder.delete_volume | 0.506 | 2.848  | 3.217  | 3.222  | 3.228 | 2.122 | 100.0%  | 10    |
    | total                | 4.188 | 6.787  | 7.161  | 7.175  | 7.189 | 6.026 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 18.0166649818
    Full duration: 35.4839038849



    test scenario CinderVolumes.create_and_upload_volume_to_image
    +-------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                          |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume          | 3.672  | 4.074  | 4.522  | 4.546  | 4.57   | 4.114  | 100.0%  | 10    |
    | cinder.upload_volume_to_image | 21.673 | 31.257 | 31.931 | 31.979 | 32.027 | 29.253 | 100.0%  | 10    |
    | cinder.delete_volume          | 0.56   | 2.568  | 3.011  | 3.067  | 3.123  | 2.293  | 100.0%  | 10    |
    | nova.delete_image             | 2.137  | 2.51   | 2.606  | 2.681  | 2.756  | 2.451  | 100.0%  | 10    |
    | total                         | 28.587 | 39.952 | 40.849 | 41.35  | 41.852 | 38.112 | 100.0%  | 10    |
    +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 110.444069147
    Full duration: 131.52224803



    test scenario CinderVolumes.create_and_delete_snapshot
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_snapshot | 3.208 | 3.343  | 5.587  | 5.628  | 5.669 | 3.788 | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.503 | 2.86   | 3.196  | 3.217  | 3.239 | 2.893 | 100.0%  | 10    |
    | total                  | 5.787 | 6.422  | 8.296  | 8.392  | 8.488 | 6.681 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 18.7773430347
    Full duration: 53.0582361221



    test scenario CinderVolumes.create_volume
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.52 | 3.822  | 4.222  | 4.228  | 4.233 | 3.852 | 100.0%  | 10    |
    | total                | 3.52 | 3.822  | 4.223  | 4.228  | 4.233 | 3.852 | 100.0%  | 10    |
    +----------------------+------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 11.2881109715
    Full duration: 29.6710369587



    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.248 | 3.651  | 3.891  | 3.988  | 4.084 | 3.645 | 100.0%  | 10    |
    | total                | 3.249 | 3.652  | 3.891  | 3.988  | 4.084 | 3.645 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 10.7785470486
    Full duration: 32.9540159702



    test scenario CinderVolumes.list_volumes
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.list_volumes | 0.499 | 0.52   | 0.539  | 0.55   | 0.561 | 0.522 | 100.0%  | 10    |
    | total               | 0.499 | 0.52   | 0.539  | 0.55   | 0.561 | 0.523 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.60948395729
    Full duration: 65.5444660187



    test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.547  | 3.82   | 3.891  | 3.927  | 3.962  | 3.787  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.552  | 2.875  | 3.173  | 3.215  | 3.257  | 2.931  | 100.0%  | 10    |
    | nova.attach_volume     | 3.633  | 5.774  | 8.279  | 8.853  | 9.427  | 6.038  | 100.0%  | 10    |
    | nova.detach_volume     | 3.599  | 3.826  | 4.233  | 4.444  | 4.655  | 3.905  | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.22   | 2.537  | 2.852  | 2.971  | 3.09   | 2.577  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.648  | 2.735  | 2.845  | 2.892  | 2.939  | 2.321  | 100.0%  | 10    |
    | total                  | 18.538 | 22.642 | 25.806 | 26.204 | 26.601 | 22.745 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 66.8299760818
    Full duration: 173.895985842



    test scenario CinderVolumes.create_from_volume_and_delete_volume
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | cinder.create_volume | 3.481 | 3.953  | 4.613  | 5.302  | 5.991 | 4.167 | 100.0%  | 10    |
    | cinder.delete_volume | 1.163 | 3.065  | 3.469  | 3.474  | 3.479 | 2.919 | 100.0%  | 10    |
    | total                | 5.012 | 7.114  | 7.89   | 8.462  | 9.034 | 7.087 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 20.8082921505
    Full duration: 55.4062600136



    test scenario CinderVolumes.create_and_extend_volume
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | cinder.create_volume | 3.417 | 3.839  | 3.908  | 3.925  | 3.941  | 3.742 | 100.0%  | 10    |
    | cinder.extend_volume | 0.938 | 2.978  | 3.574  | 3.713  | 3.853  | 2.396 | 100.0%  | 10    |
    | cinder.delete_volume | 0.577 | 1.808  | 3.066  | 3.146  | 3.225  | 1.858 | 100.0%  | 10    |
    | total                | 5.44  | 8.275  | 9.921  | 10.095 | 10.269 | 7.997 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 23.5873560905
    Full duration: 41.9279878139



    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +-----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                      |
    +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.668 | 3.89   | 4.255  | 4.266  | 4.277  | 3.937  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.268 | 2.949  | 3.306  | 3.36   | 3.414  | 2.903  | 100.0%  | 10    |
    | nova.attach_volume     | 3.471 | 4.393  | 7.358  | 8.251  | 9.145  | 5.113  | 100.0%  | 10    |
    | nova.detach_volume     | 3.277 | 3.925  | 4.509  | 4.566  | 4.622  | 3.926  | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.286 | 2.607  | 2.849  | 2.862  | 2.875  | 2.614  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.591 | 2.677  | 2.96   | 3.019  | 3.078  | 2.352  | 100.0%  | 10    |
    | total                  | 18.8  | 21.654 | 23.365 | 25.201 | 27.038 | 21.974 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 65.2181398869
    Full duration: 179.069041967



    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume   | 3.22   | 3.682  | 4.259  | 4.27   | 4.281  | 3.723  | 100.0%  | 10    |
    | cinder.create_snapshot | 2.292  | 3.051  | 3.199  | 3.232  | 3.265  | 2.991  | 100.0%  | 10    |
    | nova.attach_volume     | 3.891  | 4.365  | 6.53   | 6.577  | 6.625  | 4.971  | 100.0%  | 10    |
    | nova.detach_volume     | 3.248  | 3.565  | 3.767  | 4.044  | 4.321  | 3.568  | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.258  | 2.551  | 2.836  | 2.87   | 2.904  | 2.609  | 100.0%  | 10    |
    | cinder.delete_volume   | 0.883  | 2.687  | 3.02   | 3.224  | 3.427  | 2.286  | 100.0%  | 10    |
    | total                  | 19.132 | 21.712 | 23.229 | 23.566 | 23.904 | 21.677 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 64.7866289616
    Full duration: 180.275881052



    run_rally - INFO - Test scenario: "cinder" OK.

    run_rally - INFO - Starting test scenario "heat" ...
    run_rally - INFO -
     Preparing input task
     Task  51925ef8-a527-44d2-8df3-6164af0ec62a: started
    Task 51925ef8-a527-44d2-8df3-6164af0ec62a: finished

    test scenario HeatStacks.create_suspend_resume_delete_stack
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack  | 4.245 | 4.317  | 4.434  | 4.474  | 4.514 | 4.348 | 100.0%  | 10    |
    | heat.suspend_stack | 1.497 | 1.713  | 1.747  | 1.75   | 1.753 | 1.7   | 100.0%  | 10    |
    | heat.resume_stack  | 1.42  | 1.621  | 1.668  | 1.67   | 1.671 | 1.562 | 100.0%  | 10    |
    | heat.delete_stack  | 1.377 | 1.573  | 1.716  | 2.249  | 2.782 | 1.675 | 100.0%  | 10    |
    | total              | 8.851 | 9.198  | 9.402  | 9.981  | 10.56 | 9.285 | 100.0%  | 10    |
    +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 27.3572640419
    Full duration: 37.0984110832



    test scenario HeatStacks.create_and_delete_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 3.911 | 4.181  | 4.323  | 4.325  | 4.327 | 4.149 | 100.0%  | 10    |
    | heat.delete_stack | 1.392 | 1.426  | 1.744  | 1.776  | 1.808 | 1.491 | 100.0%  | 10    |
    | total             | 5.311 | 5.631  | 5.774  | 5.775  | 5.776 | 5.64  | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 16.9275529385
    Full duration: 26.8473479748



    test scenario HeatStacks.create_and_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 20.192 | 23.206 | 23.805 | 23.826 | 23.847 | 22.465 | 100.0%  | 10    |
    | heat.delete_stack | 11.755 | 11.868 | 12.963 | 13.0   | 13.036 | 12.282 | 100.0%  | 10    |
    | total             | 32.02  | 35.613 | 36.714 | 36.721 | 36.729 | 34.747 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 102.752908945
    Full duration: 112.369065046



    test scenario HeatStacks.create_and_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 16.808 | 18.33  | 20.748 | 20.751 | 20.755 | 18.654 | 100.0%  | 10    |
    | heat.delete_stack | 9.404  | 10.582 | 10.788 | 10.803 | 10.818 | 10.313 | 100.0%  | 10    |
    | total             | 26.212 | 28.318 | 31.532 | 31.553 | 31.574 | 28.967 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 85.8598790169
    Full duration: 95.2520959377



    test scenario HeatStacks.list_stacks_and_resources
    +-----------------------------------------------------------------------------------------------------+
    |                                        Response Times (sec)                                         |
    +---------------------------------+------+--------+--------+--------+-------+-------+---------+-------+
    | action                          | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------------------+------+--------+--------+--------+-------+-------+---------+-------+
    | heat.list_stacks                | 0.45 | 0.485  | 0.512  | 0.512  | 0.512 | 0.487 | 100.0%  | 10    |
    | heat.list_resources_of_0_stacks | 0.0  | 0.0    | 0.0    | 0.0    | 0.0   | 0.0   | 100.0%  | 10    |
    | total                           | 0.45 | 0.485  | 0.512  | 0.512  | 0.512 | 0.487 | 100.0%  | 10    |
    +---------------------------------+------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.48300600052
    Full duration: 9.57427692413



    test scenario HeatStacks.create_update_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 3.727 | 4.075  | 4.288  | 4.337  | 4.386  | 4.085  | 100.0%  | 10    |
    | heat.update_stack | 3.549 | 3.676  | 3.903  | 3.972  | 4.042  | 3.704  | 100.0%  | 10    |
    | heat.delete_stack | 1.405 | 2.619  | 2.76   | 2.774  | 2.789  | 2.212  | 100.0%  | 10    |
    | total             | 9.105 | 10.287 | 10.719 | 10.741 | 10.763 | 10.001 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 29.4346759319
    Full duration: 39.5471699238



    test scenario HeatStacks.create_update_delete_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 3.915 | 4.067  | 4.171  | 4.199  | 4.227 | 4.052 | 100.0%  | 10    |
    | heat.update_stack | 3.521 | 3.661  | 3.773  | 3.791  | 3.81  | 3.658 | 100.0%  | 10    |
    | heat.delete_stack | 1.38  | 1.477  | 1.612  | 1.618  | 1.624 | 1.492 | 100.0%  | 10    |
    | total             | 8.916 | 9.128  | 9.484  | 9.493  | 9.503 | 9.203 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 27.5511319637
    Full duration: 37.5252559185



    test scenario HeatStacks.create_update_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 4.023  | 4.301  | 4.59   | 5.029  | 5.468  | 4.38   | 100.0%  | 10    |
    | heat.update_stack | 5.783  | 5.888  | 6.061  | 6.08   | 6.1    | 5.912  | 100.0%  | 10    |
    | heat.delete_stack | 2.475  | 2.546  | 2.705  | 3.2    | 3.694  | 2.65   | 100.0%  | 10    |
    | total             | 12.613 | 12.74  | 13.76  | 13.912 | 14.064 | 12.942 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 38.1860618591
    Full duration: 48.4381308556



    test scenario HeatStacks.create_update_delete_stack
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 4.094  | 5.24   | 5.479  | 5.528  | 5.577  | 5.17   | 100.0%  | 10    |
    | heat.update_stack | 8.178  | 9.243  | 9.316  | 9.324  | 9.332  | 8.862  | 100.0%  | 10    |
    | heat.delete_stack | 3.63   | 3.68   | 3.714  | 3.714  | 3.715  | 3.68   | 100.0%  | 10    |
    | total             | 16.974 | 17.76  | 18.444 | 18.466 | 18.488 | 17.713 | 100.0%  | 10    |
    +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 52.4500279427
    Full duration: 63.0265882015



    test scenario HeatStacks.create_update_delete_stack
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | heat.create_stack | 4.113 | 4.273  | 4.647  | 4.934  | 5.22   | 4.362  | 100.0%  | 10    |
    | heat.update_stack | 5.809 | 5.888  | 5.941  | 6.056  | 6.17   | 5.907  | 100.0%  | 10    |
    | heat.delete_stack | 2.513 | 2.561  | 3.694  | 3.7    | 3.706  | 2.891  | 100.0%  | 10    |
    | total             | 12.55 | 12.759 | 14.013 | 14.546 | 15.079 | 13.161 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 39.0816349983
    Full duration: 49.7756490707



    test scenario HeatStacks.create_update_delete_stack
    +-----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | heat.create_stack | 3.762 | 4.115  | 4.19   | 4.27   | 4.35   | 4.062 | 100.0%  | 10    |
    | heat.update_stack | 3.543 | 3.63   | 3.844  | 3.977  | 4.11   | 3.69  | 100.0%  | 10    |
    | heat.delete_stack | 1.383 | 1.499  | 2.506  | 2.528  | 2.549  | 1.677 | 100.0%  | 10    |
    | total             | 8.868 | 9.275  | 10.208 | 10.225 | 10.242 | 9.429 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 27.9543409348
    Full duration: 38.8234701157



    test scenario HeatStacks.create_and_list_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 4.005 | 4.128  | 4.199  | 4.234  | 4.27  | 4.127 | 100.0%  | 10    |
    | heat.list_stacks  | 0.075 | 0.094  | 0.108  | 0.112  | 0.117 | 0.094 | 100.0%  | 10    |
    | total             | 4.112 | 4.226  | 4.281  | 4.313  | 4.345 | 4.221 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 12.6059498787
    Full duration: 27.8848700523



    test scenario HeatStacks.create_check_delete_stack
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | heat.create_stack | 4.084 | 4.153  | 4.178  | 4.217  | 4.256 | 4.153 | 100.0%  | 10    |
    | heat.check_stack  | 0.706 | 1.53   | 1.571  | 1.586  | 1.6   | 1.459 | 100.0%  | 10    |
    | heat.delete_stack | 1.375 | 1.432  | 2.542  | 2.546  | 2.55  | 1.763 | 100.0%  | 10    |
    | total             | 7.01  | 7.159  | 8.25   | 8.279  | 8.309 | 7.375 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 22.5798799992
    Full duration: 33.7318949699



    run_rally - INFO - Test scenario: "heat" OK.

    run_rally - INFO - Starting test scenario "keystone" ...
    run_rally - INFO -
     Preparing input task
     Task  98c40f01-0adc-48ce-91ca-105f22e60ec9: started
    Task 98c40f01-0adc-48ce-91ca-105f22e60ec9: finished

    test scenario KeystoneBasic.create_tenant_with_users
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.263 | 0.291  | 0.401  | 0.408  | 0.415 | 0.322 | 100.0%  | 10    |
    | keystone.create_users  | 1.508 | 1.599  | 1.672  | 1.733  | 1.793 | 1.601 | 100.0%  | 10    |
    | total                  | 1.782 | 1.949  | 2.051  | 2.066  | 2.081 | 1.923 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 5.82497000694
    Full duration: 20.636977911



    test scenario KeystoneBasic.create_add_and_list_user_roles
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.256 | 0.273  | 0.292  | 0.296  | 0.3   | 0.274 | 100.0%  | 10    |
    | keystone.add_role    | 0.24  | 0.262  | 0.297  | 0.319  | 0.341 | 0.267 | 100.0%  | 10    |
    | keystone.list_roles  | 0.131 | 0.146  | 0.226  | 0.237  | 0.248 | 0.16  | 100.0%  | 10    |
    | total                | 0.636 | 0.682  | 0.774  | 0.78   | 0.786 | 0.702 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.11375284195
    Full duration: 14.9668319225



    test scenario KeystoneBasic.add_and_remove_user_role
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.267 | 0.326  | 0.368  | 0.376  | 0.383 | 0.322 | 100.0%  | 10    |
    | keystone.add_role    | 0.244 | 0.255  | 0.278  | 0.302  | 0.326 | 0.263 | 100.0%  | 10    |
    | keystone.remove_role | 0.149 | 0.163  | 0.191  | 0.244  | 0.296 | 0.177 | 100.0%  | 10    |
    | total                | 0.681 | 0.765  | 0.834  | 0.84   | 0.846 | 0.762 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.33364892006
    Full duration: 14.8711419106



    test scenario KeystoneBasic.create_update_and_delete_tenant
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.272 | 0.316  | 0.391  | 0.394  | 0.396 | 0.327 | 100.0%  | 10    |
    | keystone.update_tenant | 0.125 | 0.141  | 0.169  | 0.215  | 0.261 | 0.152 | 100.0%  | 10    |
    | keystone.delete_tenant | 0.299 | 0.321  | 0.379  | 0.394  | 0.408 | 0.333 | 100.0%  | 10    |
    | total                  | 0.745 | 0.81   | 0.859  | 0.915  | 0.971 | 0.812 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.46658396721
    Full duration: 13.4442551136



    test scenario KeystoneBasic.create_and_delete_service
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_service | 0.258 | 0.271  | 0.303  | 0.308  | 0.314 | 0.278 | 100.0%  | 10    |
    | keystone.delete_service | 0.146 | 0.158  | 0.181  | 0.203  | 0.226 | 0.164 | 100.0%  | 10    |
    | total                   | 0.408 | 0.442  | 0.464  | 0.475  | 0.487 | 0.442 | 100.0%  | 10    |
    +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.34449720383
    Full duration: 12.1886069775



    test scenario KeystoneBasic.create_tenant
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.253 | 0.302  | 0.319  | 0.324  | 0.328 | 0.297 | 100.0%  | 10    |
    | total                  | 0.253 | 0.302  | 0.319  | 0.324  | 0.329 | 0.298 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.912425994873
    Full duration: 8.74173903465



    test scenario KeystoneBasic.create_user
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_user | 0.262 | 0.303  | 0.319  | 0.319  | 0.319 | 0.296 | 100.0%  | 10    |
    | total                | 0.262 | 0.303  | 0.319  | 0.319  | 0.32  | 0.296 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 0.953788042068
    Full duration: 8.72430300713



    test scenario KeystoneBasic.create_and_list_tenants
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.247 | 0.28   | 0.302  | 0.304  | 0.307 | 0.281 | 100.0%  | 10    |
    | keystone.list_tenants  | 0.121 | 0.129  | 0.224  | 0.225  | 0.225 | 0.147 | 100.0%  | 10    |
    | total                  | 0.392 | 0.42   | 0.476  | 0.493  | 0.511 | 0.428 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.32897400856
    Full duration: 13.584346056



    test scenario KeystoneBasic.create_and_delete_role
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_role | 0.286 | 0.324  | 0.395  | 0.47   | 0.545 | 0.347 | 100.0%  | 10    |
    | keystone.delete_role | 0.25  | 0.32   | 0.487  | 0.522  | 0.557 | 0.344 | 100.0%  | 10    |
    | total                | 0.546 | 0.62   | 0.889  | 0.913  | 0.936 | 0.691 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.18193697929
    Full duration: 12.766493082



    test scenario KeystoneBasic.get_entities
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_tenant | 0.271 | 0.283  | 0.299  | 0.311  | 0.322 | 0.287 | 100.0%  | 10    |
    | keystone.create_user   | 0.145 | 0.156  | 0.162  | 0.165  | 0.167 | 0.155 | 100.0%  | 10    |
    | keystone.create_role   | 0.122 | 0.133  | 0.155  | 0.183  | 0.211 | 0.141 | 100.0%  | 10    |
    | keystone.get_tenant    | 0.109 | 0.126  | 0.145  | 0.178  | 0.211 | 0.133 | 100.0%  | 10    |
    | keystone.get_user      | 0.12  | 0.133  | 0.2    | 0.205  | 0.21  | 0.148 | 100.0%  | 10    |
    | keystone.get_role      | 0.106 | 0.12   | 0.137  | 0.155  | 0.172 | 0.126 | 100.0%  | 10    |
    | keystone.service_list  | 0.112 | 0.126  | 0.144  | 0.178  | 0.212 | 0.134 | 100.0%  | 10    |
    | keystone.get_service   | 0.104 | 0.125  | 0.131  | 0.134  | 0.136 | 0.123 | 100.0%  | 10    |
    | total                  | 1.177 | 1.23   | 1.321  | 1.328  | 1.334 | 1.248 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.83582210541
    Full duration: 20.6130208969



    test scenario KeystoneBasic.create_and_list_users
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | keystone.create_user | 0.295 | 0.312  | 0.374  | 0.386  | 0.399 | 0.326 | 100.0%  | 10    |
    | keystone.list_users  | 0.114 | 0.129  | 0.148  | 0.148  | 0.149 | 0.133 | 100.0%  | 10    |
    | total                | 0.419 | 0.442  | 0.521  | 0.535  | 0.549 | 0.458 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.37977695465
    Full duration: 9.29229903221



    run_rally - INFO - Test scenario: "keystone" OK.

    run_rally - INFO - Starting test scenario "neutron" ...
    run_rally - INFO -
     Preparing input task
     Task  0a18c72f-b575-481a-8997-6d3d52130ede: started
    Task 0a18c72f-b575-481a-8997-6d3d52130ede: finished

    test scenario NeutronNetworks.create_and_delete_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.758 | 0.851  | 1.15   | 1.23   | 1.309 | 0.925 | 100.0%  | 10    |
    | neutron.delete_port | 0.241 | 0.578  | 0.611  | 0.618  | 0.625 | 0.488 | 100.0%  | 10    |
    | total               | 0.998 | 1.415  | 1.73   | 1.808  | 1.886 | 1.414 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.22447299957
    Full duration: 51.8464670181



    test scenario NeutronNetworks.create_and_list_routers
    +---------------------------------------------------------------------------------------------------+
    |                                       Response Times (sec)                                        |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet        | 0.768 | 0.804  | 0.942  | 1.007  | 1.073 | 0.852 | 100.0%  | 10    |
    | neutron.create_router        | 0.08  | 0.425  | 0.456  | 0.469  | 0.482 | 0.394 | 100.0%  | 10    |
    | neutron.add_interface_router | 0.371 | 0.741  | 1.213  | 1.526  | 1.84  | 0.855 | 100.0%  | 10    |
    | neutron.list_routers         | 0.048 | 0.405  | 0.478  | 0.502  | 0.527 | 0.286 | 100.0%  | 10    |
    | total                        | 1.684 | 2.22   | 3.085  | 3.308  | 3.53  | 2.388 | 100.0%  | 10    |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 7.42530488968
    Full duration: 57.8292651176



    test scenario NeutronNetworks.create_and_delete_routers
    +------------------------------------------------------------------------------------------------------+
    |                                         Response Times (sec)                                         |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet           | 0.689 | 0.768  | 0.931  | 0.941  | 0.95  | 0.811 | 100.0%  | 10    |
    | neutron.create_router           | 0.408 | 0.421  | 0.457  | 0.547  | 0.636 | 0.441 | 100.0%  | 10    |
    | neutron.add_interface_router    | 0.363 | 0.702  | 0.802  | 0.807  | 0.813 | 0.653 | 100.0%  | 10    |
    | neutron.remove_interface_router | 0.273 | 0.662  | 0.823  | 0.847  | 0.872 | 0.65  | 100.0%  | 10    |
    | neutron.delete_router           | 0.178 | 0.557  | 0.661  | 0.665  | 0.669 | 0.541 | 100.0%  | 10    |
    | total                           | 2.291 | 3.046  | 3.598  | 3.647  | 3.695 | 3.096 | 100.0%  | 10    |
    +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 9.11136102676
    Full duration: 56.6760940552



    test scenario NeutronNetworks.create_and_list_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.746 | 0.824  | 0.923  | 0.946  | 0.968 | 0.846 | 100.0%  | 10    |
    | neutron.list_ports  | 0.157 | 0.57   | 0.629  | 0.663  | 0.697 | 0.481 | 100.0%  | 10    |
    | total               | 1.065 | 1.343  | 1.476  | 1.493  | 1.51  | 1.327 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.94901585579
    Full duration: 52.597589016



    test scenario NeutronNetworks.create_and_delete_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.701 | 0.757  | 1.049  | 1.144  | 1.238 | 0.835 | 100.0%  | 10    |
    | neutron.delete_subnet | 0.196 | 0.565  | 0.691  | 0.725  | 0.759 | 0.531 | 100.0%  | 10    |
    | total                 | 0.939 | 1.384  | 1.496  | 1.595  | 1.694 | 1.366 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.35806703568
    Full duration: 51.0885548592



    test scenario NeutronNetworks.create_and_delete_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.614 | 0.675  | 0.811  | 0.817  | 0.823 | 0.692 | 100.0%  | 10    |
    | neutron.delete_network | 0.491 | 0.545  | 0.62   | 0.624  | 0.628 | 0.554 | 100.0%  | 10    |
    | total                  | 1.133 | 1.231  | 1.388  | 1.415  | 1.443 | 1.246 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.68652009964
    Full duration: 30.7036879063



    test scenario NeutronNetworks.create_and_list_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.556 | 0.652  | 0.754  | 0.757  | 0.759 | 0.665 | 100.0%  | 10    |
    | neutron.list_networks  | 0.361 | 0.383  | 0.478  | 0.503  | 0.528 | 0.403 | 100.0%  | 10    |
    | total                  | 0.917 | 1.027  | 1.231  | 1.252  | 1.273 | 1.068 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.11869502068
    Full duration: 33.6655409336



    test scenario NeutronNetworks.create_and_update_routers
    +---------------------------------------------------------------------------------------------------+
    |                                       Response Times (sec)                                        |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet        | 0.718 | 0.757  | 0.921  | 0.922  | 0.923 | 0.795 | 100.0%  | 10    |
    | neutron.create_router        | 0.073 | 0.405  | 0.44   | 0.448  | 0.455 | 0.38  | 100.0%  | 10    |
    | neutron.add_interface_router | 0.65  | 0.699  | 0.805  | 0.827  | 0.849 | 0.717 | 100.0%  | 10    |
    | neutron.update_router        | 0.228 | 0.537  | 0.661  | 0.677  | 0.693 | 0.53  | 100.0%  | 10    |
    | total                        | 2.134 | 2.511  | 2.583  | 2.583  | 2.583 | 2.422 | 100.0%  | 10    |
    +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 7.21204185486
    Full duration: 58.3329060078



    test scenario NeutronNetworks.create_and_update_networks
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_network | 0.59  | 0.678  | 0.77   | 0.785  | 0.8   | 0.684 | 100.0%  | 10    |
    | neutron.update_network | 0.452 | 0.51   | 0.55   | 0.569  | 0.587 | 0.514 | 100.0%  | 10    |
    | total                  | 1.054 | 1.188  | 1.314  | 1.319  | 1.323 | 1.198 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.48062801361
    Full duration: 33.7373108864



    test scenario NeutronNetworks.create_and_update_ports
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_port | 0.724 | 0.911  | 1.036  | 1.046  | 1.055 | 0.915 | 100.0%  | 10    |
    | neutron.update_port | 0.332 | 0.55   | 0.569  | 0.573  | 0.578 | 0.53  | 100.0%  | 10    |
    | total               | 1.173 | 1.466  | 1.591  | 1.607  | 1.623 | 1.445 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.40219402313
    Full duration: 52.9743890762



    test scenario NeutronNetworks.create_and_list_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.768 | 0.823  | 0.981  | 1.001  | 1.02  | 0.857 | 100.0%  | 10    |
    | neutron.list_subnets  | 0.053 | 0.403  | 0.472  | 0.483  | 0.495 | 0.316 | 100.0%  | 10    |
    | total                 | 0.821 | 1.249  | 1.342  | 1.384  | 1.426 | 1.173 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.63253998756
    Full duration: 52.0335438251



    test scenario NeutronNetworks.create_and_update_subnets
    +--------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | neutron.create_subnet | 0.721 | 0.797  | 0.952  | 0.953  | 0.954 | 0.82  | 100.0%  | 10    |
    | neutron.update_subnet | 0.233 | 0.605  | 0.745  | 0.753  | 0.761 | 0.589 | 100.0%  | 10    |
    | total                 | 1.002 | 1.432  | 1.561  | 1.638  | 1.715 | 1.409 | 100.0%  | 10    |
    +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.58866596222
    Full duration: 52.8035202026



    run_rally - INFO - Test scenario: "neutron" OK.

    run_rally - INFO - Starting test scenario "nova" ...
    run_rally - INFO -
     Preparing input task
     Task  7bc9f24e-75ad-4e01-afd5-3647398a073e: started
    Task 7bc9f24e-75ad-4e01-afd5-3647398a073e: finished

    test scenario NovaKeypair.create_and_delete_keypair
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | nova.create_keypair | 0.705 | 0.755  | 0.85   | 1.155  | 1.459 | 0.818 | 100.0%  | 10    |
    | nova.delete_keypair | 0.032 | 0.046  | 0.063  | 0.064  | 0.064 | 0.046 | 100.0%  | 10    |
    | total               | 0.744 | 0.804  | 0.895  | 1.21   | 1.524 | 0.864 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.08747410774
    Full duration: 41.9948050976



    test scenario NovaServers.snapshot_server
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server       | 8.021  | 10.195 | 10.572 | 10.642 | 10.713 | 9.936  | 100.0%  | 10    |
    | nova.create_image      | 10.782 | 11.261 | 11.548 | 11.631 | 11.715 | 11.242 | 100.0%  | 10    |
    | nova.delete_server     | 2.821  | 3.28   | 3.4    | 3.426  | 3.452  | 3.222  | 100.0%  | 10    |
    | nova.boot_server (2)   | 6.39   | 8.069  | 9.073  | 9.382  | 9.691  | 7.984  | 100.0%  | 10    |
    | nova.delete_server (2) | 2.855  | 2.91   | 3.425  | 3.429  | 3.434  | 3.04   | 100.0%  | 10    |
    | nova.delete_image      | 2.558  | 2.911  | 3.161  | 3.22   | 3.279  | 2.887  | 100.0%  | 10    |
    | total                  | 35.039 | 38.279 | 39.897 | 40.21  | 40.523 | 38.314 | 100.0%  | 10    |
    +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 115.44729495
    Full duration: 188.161262035



    test scenario NovaKeypair.boot_and_delete_server_with_keypair
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_keypair | 0.64   | 0.869  | 1.365  | 1.399  | 1.433  | 0.948  | 100.0%  | 10    |
    | nova.boot_server    | 7.047  | 8.139  | 10.062 | 10.11  | 10.159 | 8.606  | 100.0%  | 10    |
    | nova.delete_server  | 2.522  | 3.1    | 3.242  | 3.267  | 3.292  | 3.041  | 100.0%  | 10    |
    | nova.delete_keypair | 0.042  | 0.051  | 0.061  | 0.068  | 0.075  | 0.052  | 100.0%  | 10    |
    | total               | 11.115 | 12.323 | 14.176 | 14.258 | 14.341 | 12.648 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 39.1623878479
    Full duration: 108.56980896



    test scenario NovaKeypair.create_and_list_keypairs
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | nova.create_keypair | 0.734 | 0.87   | 0.947  | 0.982  | 1.018 | 0.859 | 100.0%  | 10    |
    | nova.list_keypairs  | 0.022 | 0.034  | 0.042  | 0.044  | 0.046 | 0.033 | 100.0%  | 10    |
    | total               | 0.769 | 0.903  | 0.981  | 1.02   | 1.059 | 0.892 | 100.0%  | 10    |
    +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 2.59114599228
    Full duration: 44.6869869232



    test scenario NovaServers.list_servers
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | nova.list_servers | 1.436 | 1.556  | 1.653  | 1.689  | 1.725 | 1.565 | 100.0%  | 10    |
    | total             | 1.436 | 1.557  | 1.653  | 1.689  | 1.726 | 1.565 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 4.71795606613
    Full duration: 123.497851133



    test scenario NovaServers.resize_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 8.388  | 9.39   | 10.016 | 10.105 | 10.194 | 9.406  | 100.0%  | 10    |
    | nova.resize         | 40.666 | 42.089 | 46.186 | 46.669 | 47.151 | 42.721 | 100.0%  | 10    |
    | nova.resize_confirm | 3.322  | 3.648  | 4.206  | 5.097  | 5.989  | 3.842  | 100.0%  | 10    |
    | nova.delete_server  | 2.499  | 2.977  | 3.32   | 3.383  | 3.446  | 3.012  | 100.0%  | 10    |
    | total               | 56.246 | 58.698 | 61.838 | 62.514 | 63.19  | 58.982 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 180.054177999
    Full duration: 221.624077082



    test scenario NovaServers.boot_server_from_volume_and_delete
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 9.965  | 10.647 | 11.15  | 11.275 | 11.4   | 10.648 | 100.0%  | 10    |
    | nova.boot_server     | 8.986  | 10.62  | 12.102 | 12.345 | 12.587 | 10.685 | 100.0%  | 10    |
    | nova.delete_server   | 3.355  | 5.419  | 5.857  | 5.908  | 5.96   | 5.311  | 100.0%  | 10    |
    | total                | 23.598 | 26.481 | 28.991 | 29.016 | 29.041 | 26.644 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 79.5105199814
    Full duration: 161.905633926



    test scenario NovaServers.boot_and_migrate_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 8.833  | 10.242 | 11.298 | 11.673 | 12.049 | 10.106 | 100.0%  | 10    |
    | nova.stop_server    | 3.821  | 6.772  | 7.286  | 7.317  | 7.349  | 6.484  | 100.0%  | 10    |
    | nova.migrate        | 8.569  | 12.084 | 12.564 | 12.67  | 12.776 | 11.309 | 100.0%  | 10    |
    | nova.resize_confirm | 2.922  | 3.398  | 4.001  | 4.054  | 4.107  | 3.49   | 100.0%  | 10    |
    | nova.delete_server  | 2.522  | 2.922  | 3.396  | 3.406  | 3.416  | 2.976  | 100.0%  | 10    |
    | total               | 29.694 | 34.582 | 36.24  | 36.517 | 36.795 | 34.367 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 100.483532906
    Full duration: 141.506958961



    test scenario NovaServers.boot_and_delete_server
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +--------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action             | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server   | 8.586 | 9.397  | 10.198 | 10.288 | 10.378 | 9.508  | 100.0%  | 10    |
    | nova.delete_server | 2.497 | 3.108  | 3.472  | 3.478  | 3.485  | 3.09   | 100.0%  | 10    |
    | total              | 11.39 | 12.555 | 13.374 | 13.612 | 13.849 | 12.598 | 100.0%  | 10    |
    +--------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 38.4852130413
    Full duration: 106.844094992



    test scenario NovaServers.boot_and_rebuild_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 8.193  | 9.878  | 10.329 | 10.703 | 11.078 | 9.597  | 100.0%  | 10    |
    | nova.rebuild_server | 8.434  | 9.946  | 10.942 | 11.066 | 11.191 | 9.967  | 100.0%  | 10    |
    | nova.delete_server  | 2.887  | 3.097  | 3.934  | 4.794  | 5.654  | 3.399  | 100.0%  | 10    |
    | total               | 20.573 | 22.393 | 25.427 | 25.892 | 26.357 | 22.963 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 68.7611658573
    Full duration: 138.198104143



    test scenario NovaSecGroup.create_and_list_secgroups
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups | 4.914  | 5.073  | 5.815  | 5.965  | 6.116  | 5.288  | 100.0%  | 10    |
    | nova.create_100_rules          | 41.66  | 44.384 | 45.431 | 45.816 | 46.201 | 44.305 | 100.0%  | 10    |
    | nova.list_security_groups      | 0.152  | 0.533  | 0.902  | 0.96   | 1.018  | 0.5    | 100.0%  | 10    |
    | total                          | 47.592 | 50.13  | 51.2   | 51.527 | 51.854 | 50.094 | 100.0%  | 10    |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 149.717460871
    Full duration: 216.41701889



    test scenario NovaSecGroup.create_and_delete_secgroups
    +--------------------------------------------------------------------------------------------------------+
    |                                          Response Times (sec)                                          |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups | 4.565  | 5.19   | 5.563  | 5.615  | 5.668  | 5.131  | 100.0%  | 10    |
    | nova.create_100_rules          | 41.981 | 43.448 | 44.817 | 44.926 | 45.034 | 43.666 | 100.0%  | 10    |
    | nova.delete_10_security_groups | 2.07   | 2.522  | 2.976  | 3.171  | 3.366  | 2.551  | 100.0%  | 10    |
    | total                          | 49.35  | 51.576 | 51.781 | 52.087 | 52.394 | 51.349 | 100.0%  | 10    |
    +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 154.714606047
    Full duration: 196.745972872



    test scenario NovaServers.boot_and_bounce_server
    +------------------------------------------------------------------------------------------------+
    |                                      Response Times (sec)                                      |
    +-------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action                  | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server        | 8.097 | 9.924  | 11.182 | 11.428 | 11.673 | 10.029 | 100.0%  | 10    |
    | nova.reboot_server      | 5.363 | 6.246  | 8.84   | 8.907  | 8.973  | 7.049  | 100.0%  | 10    |
    | nova.soft_reboot_server | 8.452 | 8.823  | 9.184  | 9.291  | 9.398  | 8.83   | 100.0%  | 10    |
    | nova.stop_server        | 3.808 | 6.394  | 7.284  | 7.3    | 7.316  | 6.358  | 100.0%  | 10    |
    | nova.start_server       | 3.677 | 5.011  | 5.706  | 5.852  | 5.997  | 4.954  | 100.0%  | 10    |
    | nova.rescue_server      | 7.752 | 8.674  | 11.07  | 11.07  | 11.071 | 9.269  | 100.0%  | 10    |
    | nova.unrescue_server    | 5.065 | 5.536  | 5.762  | 5.781  | 5.8    | 5.532  | 100.0%  | 10    |
    | nova.delete_server      | 2.485 | 2.546  | 3.501  | 4.347  | 5.194  | 2.952  | 100.0%  | 10    |
    | total                   | 50.79 | 54.629 | 59.2   | 59.748 | 60.297 | 54.995 | 100.0%  | 10    |
    +-------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 166.248807907
    Full duration: 235.770923853



    test scenario NovaServers.boot_server
    +----------------------------------------------------------------------------------------+
    |                                  Response Times (sec)                                  |
    +------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | action           | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
    +------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    | nova.boot_server | 6.916 | 9.539  | 12.275 | 12.369 | 12.464 | 9.975 | 100.0%  | 10    |
    | total            | 6.916 | 9.54   | 12.275 | 12.37  | 12.464 | 9.976 | 100.0%  | 10    |
    +------------------+-------+--------+--------+--------+--------+-------+---------+-------+
    Load duration: 29.8727550507
    Full duration: 87.0325229168



    test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
    +-----------------------------------------------------------------------------------------------------------+
    |                                           Response Times (sec)                                            |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.create_10_security_groups    | 5.065  | 5.392  | 5.642  | 5.731  | 5.819  | 5.4    | 100.0%  | 10    |
    | nova.create_100_rules             | 42.116 | 43.904 | 45.452 | 45.794 | 46.137 | 44.057 | 100.0%  | 10    |
    | nova.boot_server                  | 6.906  | 7.809  | 8.73   | 8.911  | 9.092  | 7.954  | 100.0%  | 10    |
    | nova.get_attached_security_groups | 0.209  | 0.264  | 0.361  | 0.463  | 0.565  | 0.289  | 100.0%  | 10    |
    | nova.delete_server                | 2.508  | 2.562  | 2.7    | 2.829  | 2.959  | 2.607  | 100.0%  | 10    |
    | nova.delete_10_security_groups    | 1.784  | 2.564  | 3.087  | 3.153  | 3.218  | 2.561  | 100.0%  | 10    |
    | total                             | 60.06  | 63.125 | 63.757 | 63.889 | 64.021 | 62.869 | 100.0%  | 10    |
    +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 188.221204996
    Full duration: 257.303071976



    test scenario NovaServers.pause_and_unpause_server
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server    | 7.896  | 9.252  | 10.006 | 10.25  | 10.494 | 9.303  | 100.0%  | 10    |
    | nova.pause_server   | 2.784  | 3.19   | 3.465  | 3.487  | 3.509  | 3.226  | 100.0%  | 10    |
    | nova.unpause_server | 2.782  | 3.172  | 3.226  | 3.258  | 3.29   | 3.105  | 100.0%  | 10    |
    | nova.delete_server  | 2.553  | 3.301  | 3.545  | 3.619  | 3.693  | 3.248  | 100.0%  | 10    |
    | total               | 17.692 | 19.035 | 19.794 | 19.85  | 19.905 | 18.883 | 100.0%  | 10    |
    +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 56.6791820526
    Full duration: 126.811426163



    test scenario NovaServers.boot_server_from_volume
    +----------------------------------------------------------------------------------------------+
    |                                     Response Times (sec)                                     |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    | cinder.create_volume | 9.412  | 10.207 | 10.376 | 10.441 | 10.505 | 10.131 | 100.0%  | 10    |
    | nova.boot_server     | 8.849  | 10.342 | 11.591 | 11.741 | 11.892 | 10.423 | 100.0%  | 10    |
    | total                | 18.922 | 20.498 | 21.854 | 21.976 | 22.099 | 20.555 | 100.0%  | 10    |
    +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 60.9860489368
    Full duration: 126.851632118



    test scenario NovaServers.boot_and_list_server
    +------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                   |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    | nova.boot_server  | 8.227 | 8.931  | 10.864 | 10.959 | 11.054 | 9.41   | 100.0%  | 10    |
    | nova.list_servers | 0.624 | 1.017  | 1.144  | 1.153  | 1.163  | 0.949  | 100.0%  | 10    |
    | total             | 8.969 | 9.945  | 11.851 | 11.89  | 11.928 | 10.359 | 100.0%  | 10    |
    +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
    Load duration: 30.9555499554
    Full duration: 111.845392942



    run_rally - INFO - Test scenario: "nova" OK.

    run_rally - INFO - Starting test scenario "quotas" ...
    run_rally - INFO -
     Preparing input task
     Task  1b950d54-5c1a-4680-9d86-cbebdb0d1b72: started
    Task 1b950d54-5c1a-4680-9d86-cbebdb0d1b72: finished

    test scenario Quotas.cinder_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 1.138 | 1.278  | 1.336  | 1.347  | 1.357 | 1.267 | 100.0%  | 10    |
    | total                | 1.138 | 1.278  | 1.336  | 1.347  | 1.357 | 1.267 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 3.75106191635
    Full duration: 16.480301857



    test scenario Quotas.neutron_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.406 | 0.441  | 0.5    | 0.501  | 0.502 | 0.454 | 100.0%  | 10    |
    | total                | 0.546 | 0.618  | 0.666  | 0.67   | 0.674 | 0.616 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.8795170784
    Full duration: 13.8104491234



    test scenario Quotas.cinder_update_and_delete
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 1.178 | 1.264  | 1.311  | 1.344  | 1.378 | 1.26  | 100.0%  | 10    |
    | quotas.delete_quotas | 0.89  | 0.996  | 1.091  | 1.115  | 1.138 | 1.003 | 100.0%  | 10    |
    | total                | 2.155 | 2.273  | 2.366  | 2.404  | 2.442 | 2.264 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 6.68874502182
    Full duration: 18.7547061443



    test scenario Quotas.nova_update_and_delete
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.559 | 0.615  | 0.666  | 0.669  | 0.671 | 0.616 | 100.0%  | 10    |
    | quotas.delete_quotas | 0.013 | 0.022  | 0.026  | 0.028  | 0.029 | 0.022 | 100.0%  | 10    |
    | total                | 0.585 | 0.641  | 0.68   | 0.687  | 0.693 | 0.638 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.9670290947
    Full duration: 13.6480379105



    test scenario Quotas.nova_update
    +-------------------------------------------------------------------------------------------+
    |                                   Response Times (sec)                                    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | quotas.update_quotas | 0.587 | 0.621  | 0.738  | 0.758  | 0.777 | 0.646 | 100.0%  | 10    |
    | total                | 0.587 | 0.621  | 0.738  | 0.758  | 0.777 | 0.647 | 100.0%  | 10    |
    +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 1.87492918968
    Full duration: 13.4147770405



    run_rally - INFO - Test scenario: "quotas" OK.

    run_rally - INFO - Starting test scenario "requests" ...
    run_rally - INFO -
     Preparing input task
     Task  21739b85-984f-45b9-ae85-066dbd1adce3: started
    Task 21739b85-984f-45b9-ae85-066dbd1adce3: finished

    test scenario HttpRequests.check_random_request
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | requests.check_request | 5.047 | 5.181  | 5.389  | 5.395  | 5.401 | 5.204 | 100.0%  | 10    |
    | total                  | 5.047 | 5.181  | 5.39   | 5.395  | 5.401 | 5.205 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 15.7369980812
    Full duration: 20.6335179806



    test scenario HttpRequests.check_request
    +---------------------------------------------------------------------------------------------+
    |                                    Response Times (sec)                                     |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    | requests.check_request | 5.048 | 5.052  | 5.058  | 5.058  | 5.058 | 5.053 | 100.0%  | 10    |
    | total                  | 5.049 | 5.052  | 5.058  | 5.058  | 5.058 | 5.053 | 100.0%  | 10    |
    +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
    Load duration: 15.2042939663
    Full duration: 20.2779421806



    run_rally - INFO - Test scenario: "requests" OK.

    run_rally - INFO -


                         Rally Summary Report
    +===================+============+===============+===========+
    | Module            | Duration   | nb. Test Run  | Success   |
    +===================+============+===============+===========+
    | authenticate      | 01:01      | 10            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | glance            | 03:33      | 7             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | cinder            | 22:00      | 50            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | heat              | 10:19      | 35            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | keystone          | 02:29      | 29            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | neutron           | 09:44      | 31            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | nova              | 43:55      | 61            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | quotas            | 01:16      | 7             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | requests          | 00:40      | 2             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    +===================+============+===============+===========+
    | TOTAL:            | 01:35:01   | 232           | 100.00%   |
    +===================+============+===============+===========+



SDN Controller
--------------

ODL
^^^^
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
    Output:  /home/opnfv/repos/functest/output.xml
    Log:     /home/opnfv/repos/functest/log.html
    Report:  /home/opnfv/repos/functest/report.html
    [1;32mStarting test: test/csit/suites/openstack/neutron/ [0m
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
    [0;32mFinal report is located:[0m
    Log:     /home/opnfv/repos/functest/log.html
    Report:  /home/opnfv/repos/functest/report.html



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
        "start": "2016-02-19T05:41:25.739Z",
        "end": "2016-02-19T05:41:31.140Z",
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
     Start:     2016-02-19T05:41:25.739Z
     End:       2016-02-19T05:41:31.140Z
     Duration:  6.301
    ****************************************


