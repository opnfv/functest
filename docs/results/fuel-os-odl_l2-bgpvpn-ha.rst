.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for fuel-os-odl_l2-bgpvpn-ha
-----------------------------------------------------

VIM
---

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
    vPing_userdata- INFO - vPing duration:'79.7'
    vPing_userdata- INFO - vPing OK
    vPing_userdata- INFO - Cleaning up...
    vPing_userdata- INFO - Deleting network 'vping-net'...

Tempest
^^^^^^^
::

    +------------------------------------------------------------------------------------------------------------------------------------------+---------+---------+
    | name                                                                                                                                     | time    | status  |
    +------------------------------------------------------------------------------------------------------------------------------------------+---------+---------+
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.281   | success |
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.114   | success |
    | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 12.926  | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 24.849  | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 36.056  | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.547   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.768   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.486   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 1.049   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.347   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.299   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.952   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.529   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.260   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.786   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.487   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.624   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.792   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 0.859   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 0.417   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.461   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 1.160   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 2.692   | success |
    | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 4.500   | success |
    | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 9.766   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 300.727 | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.330   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.687   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 302.209 | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.002   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 300.741 | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.455   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.680   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 302.095 | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.002   | success |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.084   | success |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 3.891   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.470   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.001   | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.220   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.530   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.437   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.143   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.001   | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.103   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.079   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.096   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.721   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.001   | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.181   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.091   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.018   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.095   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.088   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.030   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.035   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.054   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.069   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.084   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.699   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.022   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.075   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.002   | skip    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 5.318   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 10.683  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 306.252 | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.838   | skip    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 311.592 | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 15.370  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 25.343  | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 9.258   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.091   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.152   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.491   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.366   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.286   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.567   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.727   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.596   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 4.330   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 14.127  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 18.635  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 12.265  | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 12.122  | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 1.506   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 2.128   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 1.933   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 2.111   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 2.560   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 2.578   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 1.508   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 0.998   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.998   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 2.359   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 1.243   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 1.306   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 1.421   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.998   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 1.635   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.974   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 1.015   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 1.512   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 0.886   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.250   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.052   | success |
    | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 336.810 | fail    |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.740   | success |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.093   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.535   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.028   | success |
    | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.750   | success |
    | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.245   | success |
    | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.398   | success |
    | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.097   | success |
    | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 0.904   | success |
    | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.520   | success |
    | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 2.415   | success |
    | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.403   | success |
    | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.292   | success |
    | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.521   | success |
    | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 2.183   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.109   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.086   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.080   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.089   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.089   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.077   | success |
    | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.269   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 1.917   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 15.399  | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 20.214  | success |
    | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 5.865   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 1.207   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 2.604   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 2.662   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.556   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.059   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.041   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.278   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.271   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 2.640   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 2.800   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 2.208   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.293   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.300   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 2.291   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 2.745   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 1.368   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.318   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.065   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 5.069   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 3.298   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 2.237   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 2.321   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 5.779   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 2.980   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 2.462   | success |
    | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 2.617   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 1.811   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 3.256   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.033   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 1.774   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 2.789   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.077   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.565   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 6.751   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.047   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 1.299   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.592   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.613   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.569   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.805   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.762   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 3.270   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.048   | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 6.732   | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 3.526   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 3.356   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 2.875   | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 9.723   | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 17.070  | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 9.744   | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 18.252  | success |
    | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.284   | success |
    | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.048   | success |
    | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 322.942 | fail    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 335.472 | fail    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 332.744 | fail    |
    +------------------------------------------------------------------------------------------------------------------------------------------+---------+---------+
    2016-04-26 21:34:37,839 - run_tempest - INFO - Results: {'timestart': '2016-04-2620:21:12.306509', 'duration': 803, 'tests': 188, 'failures': 10}

Rally
^^^^^
::

    FUNCTEST.info: Running Rally benchmark suite...
    2016-04-26 21:36:15,676 - run_rally - INFO - Starting test scenario "authenticate" ...
    2016-04-26 21:37:35,906 - run_rally - INFO -
     Preparing input task
     Task  a8cb2031-5232-47f0-bc43-9316bd7ceefa: started
    Task a8cb2031-5232-47f0-bc43-9316bd7ceefa: finished

    test scenario Authenticate.validate_glance
    +-----------------------------------------------------------------------------------------------------------------------------------------+
    |                                                          Response Times (sec)                                                           |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_glance_2_times | 1.015     | 1.244        | 1.415        | 1.476        | 1.536     | 1.249     | 100.0%  | 10    |
    | total                                | 1.281     | 1.505        | 1.685        | 1.744        | 1.804     | 1.516     | 100.0%  | 10    |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 4.44646310806
    Full duration: 12.853926897

    test scenario Authenticate.keystone
    +--------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                   |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.keystone | 0.214     | 0.249        | 0.267        | 0.269        | 0.272     | 0.248     | 100.0%  | 10    |
    | total                 | 0.214     | 0.249        | 0.267        | 0.269        | 0.272     | 0.248     | 100.0%  | 10    |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.754605054855
    Full duration: 9.11485695839

    test scenario Authenticate.validate_heat
    +---------------------------------------------------------------------------------------------------------------------------------------+
    |                                                         Response Times (sec)                                                          |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_heat_2_times | 0.343     | 0.61         | 0.662        | 0.733        | 0.805     | 0.606     | 100.0%  | 10    |
    | total                              | 0.589     | 0.871        | 0.971        | 1.045        | 1.12      | 0.878     | 100.0%  | 10    |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.61781597137
    Full duration: 11.0082919598

    test scenario Authenticate.validate_nova
    +---------------------------------------------------------------------------------------------------------------------------------------+
    |                                                         Response Times (sec)                                                          |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_nova_2_times | 0.328     | 0.371        | 0.479        | 0.495        | 0.51      | 0.391     | 100.0%  | 10    |
    | total                              | 0.555     | 0.619        | 0.743        | 0.756        | 0.769     | 0.643     | 100.0%  | 10    |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.93781709671
    Full duration: 10.4554929733

    test scenario Authenticate.validate_cinder
    +-----------------------------------------------------------------------------------------------------------------------------------------+
    |                                                          Response Times (sec)                                                           |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_cinder_2_times | 0.31      | 0.64         | 0.927        | 0.962        | 0.998     | 0.67      | 100.0%  | 10    |
    | total                                | 0.549     | 0.921        | 1.219        | 1.236        | 1.253     | 0.939     | 100.0%  | 10    |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.9773349762
    Full duration: 11.6194210052

    test scenario Authenticate.validate_neutron
    +------------------------------------------------------------------------------------------------------------------------------------------+
    |                                                           Response Times (sec)                                                           |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_neutron_2_times | 0.304     | 0.558        | 0.576        | 0.611        | 0.646     | 0.539     | 100.0%  | 10    |
    | total                                 | 0.569     | 0.804        | 0.819        | 0.851        | 0.882     | 0.785     | 100.0%  | 10    |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.409938097
    Full duration: 11.0552449226

    2016-04-26 21:37:37,881 - run_rally - INFO - Test scenario: "authenticate" OK.

    2016-04-26 21:37:37,882 - run_rally - INFO - Starting test scenario "glance" ...
    2016-04-26 21:41:19,902 - run_rally - INFO -
     Preparing input task
     Task  5a858da8-1039-4f20-960f-2d44354c4c60: started
    Task 5a858da8-1039-4f20-960f-2d44354c4c60: finished

    test scenario GlanceImages.list_images
    +-----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                  |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.list_images | 0.803     | 0.914        | 1.107        | 1.148        | 1.189     | 0.949     | 100.0%  | 10    |
    | total              | 0.803     | 0.914        | 1.107        | 1.148        | 1.189     | 0.949     | 100.0%  | 10    |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.9055929184
    Full duration: 14.7421119213

    test scenario GlanceImages.create_image_and_boot_instances
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 7.493     | 7.807        | 9.069        | 12.596       | 16.122    | 8.653     | 100.0%  | 10    |
    | nova.boot_servers   | 9.309     | 10.032       | 11.628       | 11.726       | 11.824    | 10.411    | 100.0%  | 10    |
    | total               | 17.19     | 18.474       | 20.176       | 22.804       | 25.432    | 19.064    | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 54.8601989746
    Full duration: 113.092097998

    test scenario GlanceImages.create_and_list_image
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 7.313     | 7.52         | 8.653        | 12.221       | 15.788    | 8.359     | 100.0%  | 10    |
    | glance.list_images  | 0.356     | 0.537        | 0.57         | 0.599        | 0.627     | 0.519     | 100.0%  | 10    |
    | total               | 7.817     | 8.058        | 9.194        | 12.748       | 16.302    | 8.878     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 24.3566281796
    Full duration: 40.1059360504

    test scenario GlanceImages.create_and_delete_image
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 7.08      | 7.515        | 7.968        | 8.084        | 8.201     | 7.585     | 100.0%  | 10    |
    | glance.delete_image | 1.893     | 2.224        | 2.429        | 2.431        | 2.434     | 2.198     | 100.0%  | 10    |
    | total               | 9.374     | 9.68         | 10.313       | 10.449       | 10.585    | 9.783     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 29.927503109
    Full duration: 40.712335825

    2016-04-26 21:41:21,905 - run_rally - INFO - Test scenario: "glance" OK.

    2016-04-26 21:41:21,905 - run_rally - INFO - Starting test scenario "cinder" ...
    2016-04-26 22:02:57,566 - run_rally - INFO -
     Preparing input task
     Task  8714ce27-ec07-493c-894b-0378b012f768: started
    Task 8714ce27-ec07-493c-894b-0378b012f768: finished

    test scenario CinderVolumes.create_and_attach_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server     | 7.315     | 7.849        | 8.808        | 9.275        | 9.743     | 8.131     | 100.0%  | 10    |
    | cinder.create_volume | 3.204     | 3.91         | 4.165        | 4.209        | 4.253     | 3.777     | 100.0%  | 10    |
    | nova.attach_volume   | 4.193     | 5.576        | 6.847        | 6.918        | 6.989     | 5.577     | 100.0%  | 10    |
    | nova.detach_volume   | 3.591     | 4.036        | 4.652        | 4.887        | 5.122     | 4.155     | 100.0%  | 10    |
    | cinder.delete_volume | 0.805     | 2.91         | 3.015        | 3.158        | 3.301     | 2.362     | 100.0%  | 10    |
    | nova.delete_server   | 2.813     | 3.044        | 3.223        | 3.232        | 3.24      | 3.033     | 100.0%  | 10    |
    | total                | 24.205    | 26.801       | 29.041       | 29.115       | 29.188    | 27.034    | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 81.0580990314
    Full duration: 112.19692111

    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 10.993    | 11.11        | 11.434       | 11.435       | 11.436    | 11.186    | 100.0%  | 10    |
    | cinder.list_volumes  | 0.069     | 0.33         | 0.436        | 0.474        | 0.512     | 0.268     | 100.0%  | 10    |
    | total                | 11.084    | 11.476       | 11.601       | 11.714       | 11.828    | 11.454    | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 34.1340601444
    Full duration: 55.759376049

    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.45      | 3.958        | 4.546        | 4.569        | 4.591     | 4.003     | 100.0%  | 10    |
    | cinder.list_volumes  | 0.062     | 0.325        | 0.344        | 0.345        | 0.345     | 0.275     | 100.0%  | 10    |
    | total                | 3.513     | 4.292        | 4.865        | 4.9          | 4.935     | 4.279     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 12.6924929619
    Full duration: 34.0712091923

    test scenario CinderVolumes.create_and_list_snapshots
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_snapshot | 3.235     | 3.344        | 3.856        | 4.736        | 5.617     | 3.629     | 100.0%  | 10    |
    | cinder.list_snapshots  | 0.039     | 0.285        | 0.337        | 0.376        | 0.416     | 0.254     | 100.0%  | 10    |
    | total                  | 3.333     | 3.676        | 4.127        | 4.892        | 5.657     | 3.884     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 10.8523409367
    Full duration: 47.7997851372

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.471     | 3.85         | 4.197        | 4.341        | 4.485     | 3.858     | 100.0%  | 10    |
    | cinder.delete_volume | 0.532     | 2.741        | 3.118        | 3.184        | 3.251     | 2.077     | 100.0%  | 10    |
    | total                | 4.328     | 6.376        | 7.081        | 7.248        | 7.416     | 5.935     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 17.2594389915
    Full duration: 34.9955868721

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 8.676     | 10.604       | 11.06        | 11.115       | 11.17     | 10.243    | 100.0%  | 10    |
    | cinder.delete_volume | 0.894     | 2.767        | 3.153        | 3.195        | 3.237     | 2.369     | 100.0%  | 10    |
    | total                | 9.774     | 12.84        | 13.865       | 14.089       | 14.313    | 12.612    | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 37.8307890892
    Full duration: 56.2227160931

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.45      | 3.88         | 4.434        | 4.439        | 4.445     | 3.935     | 100.0%  | 10    |
    | cinder.delete_volume | 0.8       | 0.932        | 3.003        | 3.159        | 3.316     | 1.539     | 100.0%  | 10    |
    | total                | 4.496     | 4.916        | 6.901        | 7.325        | 7.749     | 5.474     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 16.0426750183
    Full duration: 32.9341490269

    test scenario CinderVolumes.create_and_upload_volume_to_image
    +----------------------------------------------------------------------------------------------------------------------------------+
    |                                                       Response Times (sec)                                                       |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                        | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume          | 3.49      | 3.782        | 4.253        | 4.255        | 4.256     | 3.847     | 100.0%  | 10    |
    | cinder.upload_volume_to_image | 16.394    | 27.4         | 31.961       | 32.07        | 32.18     | 25.735    | 100.0%  | 10    |
    | cinder.delete_volume          | 0.68      | 2.971        | 3.15         | 3.173        | 3.195     | 2.523     | 100.0%  | 10    |
    | nova.delete_image             | 2.479     | 2.591        | 14.325       | 14.525       | 14.725    | 4.969     | 100.0%  | 10    |
    | total                         | 24.827    | 37.87        | 49.56        | 51.384       | 53.208    | 37.075    | 100.0%  | 10    |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 101.809072971
    Full duration: 121.969902992

    test scenario CinderVolumes.create_and_delete_snapshot
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_snapshot | 3.076     | 3.402        | 3.707        | 4.558        | 5.409     | 3.552     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.541     | 2.81         | 3.096        | 3.171        | 3.246     | 2.854     | 100.0%  | 10    |
    | total                  | 5.963     | 6.195        | 6.881        | 7.543        | 8.206     | 6.406     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 18.6676621437
    Full duration: 51.159060955

    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.592     | 3.816        | 3.986        | 4.022        | 4.058     | 3.828     | 100.0%  | 10    |
    | total                | 3.592     | 3.816        | 3.986        | 4.022        | 4.058     | 3.828     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 11.4555690289
    Full duration: 28.3837711811

    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.49      | 3.885        | 4.203        | 4.22         | 4.238     | 3.914     | 100.0%  | 10    |
    | total                | 3.49      | 3.885        | 4.203        | 4.22         | 4.238     | 3.914     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 11.7762680054
    Full duration: 32.9480211735

    test scenario CinderVolumes.list_volumes
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.list_volumes | 0.556     | 0.603        | 0.646        | 0.687        | 0.728     | 0.61      | 100.0%  | 10    |
    | total               | 0.556     | 0.603        | 0.646        | 0.687        | 0.728     | 0.611     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.8286819458
    Full duration: 63.6903710365

    test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | 3.584     | 3.868        | 4.043        | 4.092        | 4.141     | 3.882     | 100.0%  | 10    |
    | cinder.create_snapshot | 2.795     | 3.099        | 3.183        | 3.279        | 3.376     | 3.058     | 100.0%  | 10    |
    | nova.attach_volume     | 3.804     | 4.321        | 9.448        | 9.664        | 9.88      | 5.664     | 100.0%  | 10    |
    | nova.detach_volume     | 3.584     | 4.108        | 4.341        | 4.345        | 4.349     | 4.073     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.527     | 2.796        | 3.137        | 3.155        | 3.172     | 2.849     | 100.0%  | 10    |
    | cinder.delete_volume   | 0.516     | 2.694        | 3.048        | 3.146        | 3.244     | 2.193     | 100.0%  | 10    |
    | total                  | 19.584    | 21.934       | 25.955       | 26.608       | 27.261    | 22.822    | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 65.3636519909
    Full duration: 157.771946192

    test scenario CinderVolumes.create_from_volume_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.799     | 4.234        | 6.551        | 6.658        | 6.765     | 4.608     | 100.0%  | 10    |
    | cinder.delete_volume | 2.709     | 3.319        | 3.584        | 3.584        | 3.585     | 3.276     | 100.0%  | 10    |
    | total                | 7.064     | 7.351        | 9.902        | 9.97         | 10.037    | 7.885     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 24.1967608929
    Full duration: 56.604929924

    test scenario CinderVolumes.create_and_extend_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.542     | 3.816        | 3.903        | 3.913        | 3.923     | 3.81      | 100.0%  | 10    |
    | cinder.extend_volume | 1.122     | 3.325        | 3.477        | 3.479        | 3.482     | 2.916     | 100.0%  | 10    |
    | cinder.delete_volume | 0.537     | 2.74         | 3.216        | 3.222        | 3.227     | 2.259     | 100.0%  | 10    |
    | total                | 5.854     | 9.459        | 10.487       | 10.503       | 10.52     | 8.985     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 28.2484090328
    Full duration: 46.2826929092

    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | 3.569     | 3.853        | 3.95         | 4.015        | 4.08      | 3.829     | 100.0%  | 10    |
    | cinder.create_snapshot | 2.31      | 2.832        | 3.33         | 3.355        | 3.38      | 2.897     | 100.0%  | 10    |
    | nova.attach_volume     | 4.043     | 4.744        | 7.838        | 8.729        | 9.621     | 5.643     | 100.0%  | 10    |
    | nova.detach_volume     | 3.471     | 4.246        | 4.498        | 4.498        | 4.498     | 4.184     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.532     | 2.852        | 2.92         | 2.971        | 3.022     | 2.789     | 100.0%  | 10    |
    | cinder.delete_volume   | 0.549     | 2.606        | 2.992        | 3.023        | 3.053     | 2.117     | 100.0%  | 10    |
    | total                  | 18.473    | 22.08        | 25.688       | 26.47        | 27.253    | 22.541    | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 66.4576151371
    Full duration: 166.03899312

    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | 3.15      | 3.42         | 3.637        | 3.78         | 3.923     | 3.45      | 100.0%  | 10    |
    | cinder.create_snapshot | 2.546     | 2.911        | 3.114        | 3.207        | 3.301     | 2.929     | 100.0%  | 10    |
    | nova.attach_volume     | 4.077     | 5.64         | 7.857        | 8.865        | 9.874     | 5.963     | 100.0%  | 10    |
    | nova.detach_volume     | 3.76      | 4.056        | 4.468        | 4.626        | 4.784     | 4.137     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.242     | 2.665        | 2.932        | 2.947        | 2.961     | 2.633     | 100.0%  | 10    |
    | cinder.delete_volume   | 0.539     | 2.723        | 3.0          | 3.115        | 3.23      | 2.577     | 100.0%  | 10    |
    | total                  | 19.142    | 22.899       | 26.465       | 27.264       | 28.063    | 23.373    | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 68.2796330452
    Full duration: 167.136126041

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
     Start:   	2016-04-26T21:35:23.780Z
     End:     	2016-04-26T21:35:29.337Z
     Duration:	5.557
    ****************************************

bgpvpn
^^^^^^
::

    ${PYTHON:-python} -m subunit.run discover -t ${OS_TOP_LEVEL:-./} ${OS_TEST_PATH:-./tempest/test_discover}  --load-list /tmp/tmpB17uh4
    {0} networking_bgpvpn_tempest.tests.api.test_bgpvpn.BgpvpnTest.test_create_bgpvpn [0.640872s] ... ok
    {0} networking_bgpvpn_tempest.tests.api.test_bgpvpn.BgpvpnTest.test_create_bgpvpn_as_non_admin_fail [0.293540s] ... ok

    ======
    Totals
    ======
    Ran: 2 tests in 13.0000 sec.
     - Passed: 2
     - Skipped: 0
     - Expected Fail: 0
     - Unexpected Success: 0
     - Failed: 0
    Sum of execute time for each test: 0.9344 sec.
