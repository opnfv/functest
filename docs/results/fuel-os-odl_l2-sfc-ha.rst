.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for fuel-os-odl_l2-sfc-ha
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
    vPing_ssh- INFO - vPing duration:'34.7' s.
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
    vPing_userdata- INFO - vPing duration:'20.2'
    vPing_userdata- INFO - vPing OK
    vPing_userdata- INFO - Cleaning up...
    vPing_userdata- INFO - Deleting network 'vping-net'...

Tempest
^^^^^^^
::
    +------------------------------------------------------------------------------------------------------------------------------------------+---------+---------+
    | name                                                                                                                                     | time    | status  |
    +------------------------------------------------------------------------------------------------------------------------------------------+---------+---------+
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.254   | success |
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.125   | success |
    | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 12.388  | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 24.859  | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 11.610  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.780   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.301   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.308   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 1.031   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.525   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.310   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.327   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.451   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.657   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.624   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.325   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.614   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.537   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 0.637   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 0.480   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.480   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 1.447   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 2.524   | success |
    | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 5.127   | success |
    | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 9.604   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 3.288   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.114   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.489   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 0.209   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.001   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 15.311  | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.090   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.467   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 0.207   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.001   | success |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.085   | success |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 3.900   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.712   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.001   | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.713   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.622   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.433   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.110   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.001   | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.094   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.076   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.093   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.528   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.001   | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.173   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.093   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.025   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.093   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.080   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.020   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.025   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.043   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.581   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.066   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.288   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.030   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.096   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.001   | skip    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 5.780   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 10.302  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 11.027  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 1.138   | skip    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 11.793  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 14.743  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 24.954  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 8.319   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.102   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.170   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.536   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.507   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.449   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.688   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.515   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.556   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 3.590   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 12.764  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 21.680  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 9.787   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 11.049  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 2.045   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 2.190   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 2.549   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 2.194   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 2.236   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 2.806   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 1.026   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 1.050   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.552   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 1.557   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 1.266   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 0.803   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 0.824   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.778   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 1.357   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 1.212   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 1.691   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 0.931   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 1.165   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.248   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.078   | success |
    | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 47.118  | success |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.111   | success |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.097   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.262   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.016   | success |
    | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.809   | success |
    | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.233   | success |
    | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.397   | success |
    | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.077   | success |
    | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 0.966   | success |
    | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.513   | success |
    | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 2.311   | success |
    | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.401   | success |
    | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.332   | success |
    | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.555   | success |
    | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 2.059   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.086   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.091   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.078   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.087   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.083   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.076   | success |
    | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.579   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 2.026   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 2.947   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 15.745  | success |
    | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 4.489   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 1.373   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 3.080   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 2.565   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.671   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.317   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.042   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.282   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.045   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 2.800   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 2.487   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 1.722   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.272   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.282   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 2.391   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 2.499   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 1.658   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.062   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.087   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 5.549   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 3.796   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 3.120   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 2.261   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 6.149   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 3.659   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 2.738   | success |
    | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 2.213   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 1.612   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 2.371   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.043   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 1.383   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 3.275   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.237   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.531   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 5.699   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.045   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 1.426   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.579   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.680   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.622   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.799   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.770   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 3.216   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.051   | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 18.428  | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 3.313   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 2.580   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 3.176   | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 10.232  | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 17.327  | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 11.862  | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 17.953  | success |
    | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.304   | success |
    | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.680   | success |
    | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 45.140  | success |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 115.284 | success |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 88.143  | success |
    +------------------------------------------------------------------------------------------------------------------------------------------+---------+---------+
    run_tempest - INFO - Results: {'timestart': '2016-04-2701:33:43.774958', 'duration': 1541, 'tests': 188, 'failures': 0}

Rally
^^^^^
::

    FUNCTEST.info: Running Rally benchmark suite...
    2016-04-27 02:14:20,172 - run_rally - INFO - Starting test scenario "authenticate" ...
    2016-04-27 02:15:40,641 - run_rally - INFO -
     Preparing input task
     Task  1491f5fb-1f66-45d3-b04b-31a8cf53eb71: started
    Task 1491f5fb-1f66-45d3-b04b-31a8cf53eb71: finished

    test scenario Authenticate.validate_glance
    +-----------------------------------------------------------------------------------------------------------------------------------------+
    |                                                          Response Times (sec)                                                           |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_glance_2_times | 0.966     | 1.042        | 1.146        | 1.191        | 1.236     | 1.063     | 100.0%  | 10    |
    | total                                | 1.21      | 1.272        | 1.393        | 1.45         | 1.507     | 1.307     | 100.0%  | 10    |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 3.89922785759
    Full duration: 12.1358039379

    test scenario Authenticate.keystone
    +--------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                   |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.keystone | 0.216     | 0.247        | 0.379        | 0.382        | 0.385     | 0.267     | 100.0%  | 10    |
    | total                 | 0.216     | 0.247        | 0.379        | 0.382        | 0.386     | 0.268     | 100.0%  | 10    |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.732311964035
    Full duration: 8.95613193512

    test scenario Authenticate.validate_heat
    +---------------------------------------------------------------------------------------------------------------------------------------+
    |                                                         Response Times (sec)                                                          |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_heat_2_times | 0.346     | 0.575        | 0.619        | 0.625        | 0.63      | 0.505     | 100.0%  | 10    |
    | total                              | 0.575     | 0.807        | 0.866        | 0.899        | 0.932     | 0.77      | 100.0%  | 10    |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.38545608521
    Full duration: 11.1800699234

    test scenario Authenticate.validate_nova
    +---------------------------------------------------------------------------------------------------------------------------------------+
    |                                                         Response Times (sec)                                                          |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_nova_2_times | 0.31      | 0.388        | 0.536        | 0.54         | 0.543     | 0.409     | 100.0%  | 10    |
    | total                              | 0.553     | 0.635        | 0.773        | 0.794        | 0.814     | 0.663     | 100.0%  | 10    |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.93493509293
    Full duration: 10.6224660873

    test scenario Authenticate.validate_cinder
    +-----------------------------------------------------------------------------------------------------------------------------------------+
    |                                                          Response Times (sec)                                                           |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_cinder_2_times | 0.296     | 0.55         | 0.598        | 0.713        | 0.828     | 0.553     | 100.0%  | 10    |
    | total                                | 0.525     | 0.815        | 0.942        | 1.052        | 1.162     | 0.829     | 100.0%  | 10    |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.46085309982
    Full duration: 10.4235949516

    test scenario Authenticate.validate_neutron
    +------------------------------------------------------------------------------------------------------------------------------------------+
    |                                                           Response Times (sec)                                                           |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_neutron_2_times | 0.526     | 0.601        | 0.73         | 0.74         | 0.749     | 0.615     | 100.0%  | 10    |
    | total                                 | 0.797     | 0.826        | 0.973        | 0.981        | 0.989     | 0.86      | 100.0%  | 10    |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.49738502502
    Full duration: 11.2271738052

    2016-04-27 02:15:42,749 - run_rally - INFO - Test scenario: "authenticate" OK.
    2016-04-27 02:15:42,749 - run_rally - INFO - Starting test scenario "glance" ...
    2016-04-27 02:19:48,692 - run_rally - INFO -
     Preparing input task
     Task  661ec9b2-9c4d-4fcd-b522-0cf3f1dbc4ec: started
    Task 661ec9b2-9c4d-4fcd-b522-0cf3f1dbc4ec: finished

    test scenario GlanceImages.list_images
    +-----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                  |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.list_images | 0.763     | 0.847        | 0.96         | 0.961        | 0.962     | 0.858     | 100.0%  | 10    |
    | total              | 0.763     | 0.847        | 0.96         | 0.961        | 0.962     | 0.859     | 100.0%  | 10    |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.59311103821
    Full duration: 13.8837060928

    test scenario GlanceImages.create_image_and_boot_instances
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 7.004     | 7.656        | 20.755       | 26.239       | 31.723    | 11.873    | 100.0%  | 10    |
    | nova.boot_servers   | 8.947     | 10.367       | 10.531       | 10.637       | 10.744    | 10.109    | 100.0%  | 10    |
    | total               | 15.951    | 18.072       | 31.179       | 36.629       | 42.078    | 21.982    | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 66.442127943
    Full duration: 112.407797098

    test scenario GlanceImages.create_and_list_image
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 7.244     | 7.582        | 7.891        | 7.95         | 8.009     | 7.634     | 100.0%  | 10    |
    | glance.list_images  | 0.306     | 0.566        | 0.613        | 0.638        | 0.663     | 0.546     | 100.0%  | 10    |
    | total               | 7.774     | 8.159        | 8.369        | 8.413        | 8.457     | 8.181     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 24.4534111023
    Full duration: 55.2102069855

    test scenario GlanceImages.create_and_delete_image
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 7.177     | 7.831        | 16.251       | 17.887       | 19.523    | 9.669     | 100.0%  | 10    |
    | glance.delete_image | 1.407     | 2.22         | 2.375        | 2.45         | 2.525     | 2.125     | 100.0%  | 10    |
    | total               | 9.332     | 9.768        | 18.192       | 20.001       | 21.809    | 11.794    | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 40.9665431976
    Full duration: 52.3726029396

    22016-04-27 02:19:50,772 - run_rally - INFO - Test scenario: "glance" OK.
    2016-04-27 02:19:50,773 - run_rally - INFO - Starting test scenario "cinder" ...
    2016-04-27 02:41:55,538 - run_rally - INFO -
     Preparing input task
     Task  a74fb68a-1212-4fff-afdd-a8ad044039fd: started
    Task a74fb68a-1212-4fff-afdd-a8ad044039fd: finished

    test scenario CinderVolumes.create_and_attach_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server     | 7.389     | 8.334        | 9.206        | 9.56         | 9.914     | 8.417     | 100.0%  | 10    |
    | cinder.create_volume | 3.216     | 3.747        | 4.031        | 4.195        | 4.359     | 3.726     | 100.0%  | 10    |
    | nova.attach_volume   | 3.856     | 4.202        | 7.174        | 7.341        | 7.508     | 4.8       | 100.0%  | 10    |
    | nova.detach_volume   | 4.017     | 4.272        | 4.467        | 4.641        | 4.815     | 4.302     | 100.0%  | 10    |
    | cinder.delete_volume | 0.631     | 2.93         | 3.151        | 3.193        | 3.235     | 2.346     | 100.0%  | 10    |
    | nova.delete_server   | 2.937     | 3.051        | 3.119        | 3.273        | 3.426     | 3.078     | 100.0%  | 10    |
    | total                | 23.718    | 25.911       | 29.125       | 29.723       | 30.322    | 26.67     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 78.0439009666
    Full duration: 110.455639839

    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 9.979     | 10.793       | 11.421       | 11.46        | 11.499    | 10.766    | 100.0%  | 10    |
    | cinder.list_volumes  | 0.074     | 0.299        | 0.372        | 0.384        | 0.397     | 0.235     | 100.0%  | 10    |
    | total                | 10.062    | 11.109       | 11.668       | 11.734       | 11.8      | 11.002    | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 32.7168459892
    Full duration: 54.91467309

    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.417     | 3.882        | 4.164        | 4.19         | 4.217     | 3.871     | 100.0%  | 10    |
    | cinder.list_volumes  | 0.077     | 0.338        | 0.473        | 0.485        | 0.497     | 0.335     | 100.0%  | 10    |
    | total                | 3.881     | 4.176        | 4.51         | 4.539        | 4.568     | 4.206     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 12.7357430458
    Full duration: 32.5659849644

    test scenario CinderVolumes.create_and_list_snapshots
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_snapshot | 3.051     | 3.454        | 5.626        | 5.696        | 5.765     | 3.827     | 100.0%  | 10    |
    | cinder.list_snapshots  | 0.035     | 0.296        | 0.325        | 0.325        | 0.325     | 0.227     | 100.0%  | 10    |
    | total                  | 3.355     | 3.657        | 5.947        | 6.0          | 6.052     | 4.054     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 13.0978519917
    Full duration: 50.9691619873

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.632     | 3.83         | 4.025        | 4.124        | 4.223     | 3.857     | 100.0%  | 10    |
    | cinder.delete_volume | 0.55      | 0.83         | 2.782        | 2.965        | 3.147     | 1.365     | 100.0%  | 10    |
    | total                | 4.281     | 4.87         | 6.615        | 6.841        | 7.066     | 5.222     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 15.9277088642
    Full duration: 34.237901926

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 10.252    | 10.977       | 11.943       | 11.948       | 11.953    | 11.097    | 100.0%  | 10    |
    | cinder.delete_volume | 0.82      | 1.996        | 2.99         | 3.013        | 3.036     | 1.938     | 100.0%  | 10    |
    | total                | 11.877    | 12.968       | 14.015       | 14.471       | 14.927    | 13.036    | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 37.8433139324
    Full duration: 56.9522650242

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.852     | 4.061        | 4.498        | 4.604        | 4.711     | 4.133     | 100.0%  | 10    |
    | cinder.delete_volume | 0.835     | 0.977        | 2.77         | 2.939        | 3.108     | 1.5       | 100.0%  | 10    |
    | total                | 4.799     | 5.266        | 6.888        | 6.964        | 7.039     | 5.634     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 17.0594739914
    Full duration: 34.639097929

    test scenario CinderVolumes.create_and_upload_volume_to_image
    +----------------------------------------------------------------------------------------------------------------------------------+
    |                                                       Response Times (sec)                                                       |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                        | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume          | 3.582     | 3.801        | 4.194        | 4.213        | 4.231     | 3.878     | 100.0%  | 10    |
    | cinder.upload_volume_to_image | 19.387    | 31.495       | 32.341       | 32.354       | 32.367    | 29.335    | 100.0%  | 10    |
    | cinder.delete_volume          | 0.844     | 2.45         | 2.784        | 2.825        | 2.866     | 1.905     | 100.0%  | 10    |
    | nova.delete_image             | 2.332     | 2.682        | 2.872        | 2.969        | 3.065     | 2.677     | 100.0%  | 10    |
    | total                         | 26.258    | 39.786       | 40.849       | 41.006       | 41.163    | 37.796    | 100.0%  | 10    |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 111.222266197
    Full duration: 129.783249855

    test scenario CinderVolumes.create_and_delete_snapshot
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_snapshot | 3.34      | 3.423        | 5.731        | 5.746        | 5.76      | 3.87      | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.556     | 3.104        | 3.272        | 3.285        | 3.299     | 3.068     | 100.0%  | 10    |
    | total                  | 6.365     | 6.599        | 8.332        | 8.543        | 8.755     | 6.938     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 19.7357230186
    Full duration: 50.7531559467

    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.497     | 3.901        | 4.226        | 4.246        | 4.266     | 3.883     | 100.0%  | 10    |
    | total                | 3.497     | 3.901        | 4.226        | 4.246        | 4.266     | 3.883     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 11.6317541599
    Full duration: 29.422949791

    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.649     | 3.933        | 4.176        | 4.178        | 4.179     | 3.939     | 100.0%  | 10    |
    | total                | 3.649     | 3.933        | 4.176        | 4.178        | 4.179     | 3.939     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 11.7954070568
    Full duration: 33.4074928761

    test scenario CinderVolumes.list_volumes
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.list_volumes | 0.559     | 0.596        | 0.645        | 0.658        | 0.671     | 0.603     | 100.0%  | 10    |
    | total               | 0.559     | 0.596        | 0.645        | 0.658        | 0.671     | 0.603     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.80386185646
    Full duration: 65.103438139

    test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | 3.223     | 4.031        | 4.142        | 4.196        | 4.25      | 3.949     | 100.0%  | 10    |
    | cinder.create_snapshot | 2.821     | 3.096        | 3.318        | 3.349        | 3.38      | 3.082     | 100.0%  | 10    |
    | nova.attach_volume     | 4.011     | 4.73         | 9.508        | 10.629       | 11.75     | 5.874     | 100.0%  | 10    |
    | nova.detach_volume     | 3.603     | 4.136        | 4.42         | 4.481        | 4.542     | 4.112     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.532     | 2.593        | 2.862        | 2.973        | 3.084     | 2.691     | 100.0%  | 10    |
    | cinder.delete_volume   | 0.626     | 2.709        | 3.035        | 3.087        | 3.139     | 2.413     | 100.0%  | 10    |
    | total                  | 20.294    | 22.503       | 27.052       | 28.211       | 29.37     | 23.272    | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 67.9758191109
    Full duration: 167.151215076

    test scenario CinderVolumes.create_from_volume_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.396     | 4.269        | 4.654        | 5.616        | 6.578     | 4.385     | 100.0%  | 10    |
    | cinder.delete_volume | 2.712     | 3.275        | 3.476        | 3.485        | 3.493     | 3.193     | 100.0%  | 10    |
    | total                | 6.117     | 7.6          | 8.118        | 8.975        | 9.831     | 7.578     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 24.3931138515
    Full duration: 56.1436901093

    test scenario CinderVolumes.create_and_extend_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.562     | 4.002        | 4.303        | 4.334        | 4.364     | 4.012     | 100.0%  | 10    |
    | cinder.extend_volume | 0.691     | 1.1          | 3.236        | 3.411        | 3.587     | 1.713     | 100.0%  | 10    |
    | cinder.delete_volume | 0.583     | 0.974        | 3.176        | 3.253        | 3.33      | 1.51      | 100.0%  | 10    |
    | total                | 5.58      | 6.337        | 10.123       | 10.341       | 10.559    | 7.236     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 20.3285830021
    Full duration: 37.9043469429

    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | 3.524     | 4.049        | 4.167        | 4.196        | 4.225     | 3.94      | 100.0%  | 10    |
    | cinder.create_snapshot | 2.743     | 3.026        | 3.356        | 3.408        | 3.46      | 3.053     | 100.0%  | 10    |
    | nova.attach_volume     | 4.113     | 4.635        | 6.974        | 7.136        | 7.298     | 5.464     | 100.0%  | 10    |
    | nova.detach_volume     | 3.695     | 4.078        | 4.306        | 4.692        | 5.078     | 4.146     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.489     | 2.864        | 3.117        | 3.127        | 3.136     | 2.861     | 100.0%  | 10    |
    | cinder.delete_volume   | 0.577     | 2.556        | 2.985        | 3.013        | 3.041     | 2.272     | 100.0%  | 10    |
    | total                  | 19.553    | 22.646       | 25.102       | 25.135       | 25.168    | 22.862    | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 67.4835031033
    Full duration: 178.220266819

    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | 3.143     | 3.843        | 3.997        | 4.099        | 4.2       | 3.793     | 100.0%  | 10    |
    | cinder.create_snapshot | 2.558     | 2.892        | 3.176        | 3.328        | 3.48      | 2.92      | 100.0%  | 10    |
    | nova.attach_volume     | 4.209     | 5.877        | 7.368        | 8.681        | 9.994     | 6.076     | 100.0%  | 10    |
    | nova.detach_volume     | 3.533     | 3.91         | 4.349        | 4.363        | 4.378     | 3.99      | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.531     | 2.847        | 3.044        | 3.101        | 3.158     | 2.802     | 100.0%  | 10    |
    | cinder.delete_volume   | 0.626     | 2.561        | 2.989        | 3.03         | 3.071     | 2.206     | 100.0%  | 10    |
    | total                  | 20.143    | 23.986       | 25.362       | 26.711       | 28.06     | 23.469    | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 67.7886071205
    Full duration: 169.118987083

    2016-04-27 02:41:57,893 - run_rally - INFO - Test scenario: "cinder" OK.

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
        "start": "2016-04-27T02:00:03.021Z",
        "end": "2016-04-27T02:00:08.968Z",
        "duration": 5947
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
     Start:   	2016-04-27T02:00:03.021Z
     End:     	2016-04-27T02:00:08.968Z
     Duration:	5.947
    ****************************************

vIMS
^^^^^^^
::

    FUNCTEST.info: Running vIMS test...
    2016-04-27 02:00:26,953 - vIMS - INFO - Prepare OpenStack plateform (create tenant and user)
    2016-04-27 02:00:27,734 - vIMS - INFO - Update OpenStack creds informations
    2016-04-27 02:00:27,734 - vIMS - INFO - Upload some OS images if it doesn't exist
    2016-04-27 02:00:28,202 - vIMS - INFO - centos_7 image doesn't exist on glance repository.
                                Try downloading this image and upload on glance !
    2016-04-27 02:01:55,022 - vIMS - INFO - ubuntu_14.04 image doesn't exist on glance repository.
                                Try downloading this image and upload on glance !
    2016-04-27 02:03:39,709 - vIMS - INFO - Update security group quota for this tenant
    2016-04-27 02:03:40,572 - vIMS - INFO - Update cinder quota for this tenant
    2016-04-27 02:03:41,548 - vIMS - INFO - Collect flavor id for cloudify manager server
    2016-04-27 02:03:43,403 - vIMS - INFO - Prepare virtualenv for cloudify-cli
    2016-04-27 02:04:20,255 - vIMS - INFO - Downloading the cloudify manager server blueprint
    2016-04-27 02:04:21,701 - vIMS - INFO - Cloudify deployment Start Time:'2016-04-27 02:04:21'
    2016-04-27 02:04:21,701 - vIMS - INFO - Writing the inputs file
    2016-04-27 02:04:21,706 - vIMS - INFO - Launching the cloudify-manager deployment
    2016-04-27 02:11:57,797 - vIMS - INFO - Cloudify-manager server is UP !
    2016-04-27 02:11:57,797 - vIMS - INFO - Cloudify deployment duration:'456.1'
    2016-04-27 02:11:57,798 - vIMS - INFO - Collect flavor id for all clearwater vm
    2016-04-27 02:12:00,174 - vIMS - INFO - vIMS VNF deployment Start Time:'2016-04-27 02:12:00'
    2016-04-27 02:12:00,174 - vIMS - INFO - Downloading the openstack-blueprint.yaml blueprint
    2016-04-27 02:12:01,517 - vIMS - INFO - Writing the inputs file
    2016-04-27 02:12:01,520 - vIMS - INFO - Launching the clearwater deployment
    2016-04-27 02:13:46,397 - vIMS - ERROR - Error when executing command /bin/bash -c 'source /home/opnfv/functest/data/vIMS/venv_cloudify/bin/activate; cd /home/opnfv/functest/data/vIMS/opnfv-cloudify-clearwater; cfy blueprints upload -b clearwater -p openstack-blueprint.yaml; cfy deployments create -b clearwater -d clearwater-opnfv --inputs inputs.yaml; cfy executions start -w install -d clearwater-opnfv --timeout 1800; '
    2016-04-27 02:13:46,398 - vIMS - ERROR - RuntimeError: Workflow failed: Task failed 'nova_plugin.server.start' -> NonRecoverableError('Unexpected server state ERROR:None',)
