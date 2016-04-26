.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for apex-os-odl_l2-bgpvpn-ha
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
  vPing_userdata- INFO - vPing Start Time:'2016-04-26 15:40:43'
  vPing_userdata- INFO - Creating instance 'opnfv-vping-1'...
  vPing_userdata- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  vPing_userdata- INFO - Creating instance 'opnfv-vping-2'...
  vPing_userdata- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  vPing_userdata- INFO - Waiting for ping...
  vPing_userdata- INFO - vPing detected!
  vPing_userdata- INFO - vPing duration:'87.1'
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
    | 97cda33b-5d92-46c5-8425-861d087d0d57 | 938a64f1-d650-497c-897d-8964906711fb |          | 188   | 27       | 2016-04-26 15:42:30.384572 | finished |
    +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+

    Tests:

    +----------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    | name                                                                                                                             | time      | status  |
    +----------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.643   | success |
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.048   | success |
    | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 6.046   | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 6.507   | success |
    | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 5.748   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.049   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 0.325   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.053   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.251   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.048   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.044   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.085   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.102   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.131   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.137   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.323   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.081   | success |
    | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.430   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 0.350   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 0.198   | success |
    | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.132   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 0.367   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 0.577   | success |
    | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 1.641   | success |
    | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 4.390   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 303.566 | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.154   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.173   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 300.550 | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.001   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 303.713 | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.094   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.674   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 300.091 | fail    |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.001   | success |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.043   | success |
    | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 1.587   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.262   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.121   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.178   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.135   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.113   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.047   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.040   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.040   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.038   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.259   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.391   | success |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.001   | skip    |
    | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.090   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.053   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.009   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.041   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.041   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.014   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.009   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.023   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.036   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.045   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.649   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.012   | success |
    | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.042   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.000   | skip    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 2.819   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 6.846   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 303.888 | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 0.347   | skip    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 317.471 | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 301.431 | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 301.068 | fail    |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 5.488   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.041   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 0.080   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.308   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 0.170   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.174   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.306   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.331   | success |
    | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.307   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 1.770   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 6.074   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 8.126   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 5.697   | success |
    | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 5.928   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 0.458   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 1.032   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 0.597   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 1.087   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 0.463   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 0.398   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 0.439   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 0.445   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.312   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 1.065   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 0.301   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 0.304   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 0.432   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.221   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 0.459   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.313   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 0.249   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 0.275   | success |
    | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 0.284   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.125   | success |
    | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.043   | success |
    | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 323.768 | fail    |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.055   | success |
    | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.289   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.052   | success |
    | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.009   | success |
    | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.238   | success |
    | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.107   | success |
    | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.214   | success |
    | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.102   | success |
    | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 0.382   | success |
    | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.000   | fail    |
    | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 0.894   | success |
    | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.129   | success |
    | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.168   | success |
    | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.172   | success |
    | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 0.000   | fail    |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.018   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.018   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.027   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.019   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.082   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.019   | success |
    | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.091   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 0.630   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 1.296   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 2.890   | success |
    | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 1.435   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 0.663   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 0.946   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 0.000   | fail    |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.000   | fail    |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.000   | fail    |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.000   | fail    |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.000   | fail    |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.000   | fail    |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 0.000   | fail    |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 0.000   | fail    |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 0.000   | fail    |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.000   | fail    |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.000   | fail    |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 1.425   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 2.459   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 0.711   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.099   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.094   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 3.077   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 1.372   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 1.769   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 0.889   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 3.092   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 1.691   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 1.689   | success |
    | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 1.001   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 0.748   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 1.306   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.142   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 0.748   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 1.189   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.074   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.278   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 2.527   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.015   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 0.629   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.355   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.333   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.335   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.353   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.339   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 2.951   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.022   | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 303.959 | fail    |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 302.043 | fail    |
    | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 1.600   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 1.606   | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 8.446   | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 8.743   | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 8.966   | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 10.497  | success |
    | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.105   | success |
    | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.038   | success |
    | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 134.544 | fail    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 333.942 | fail    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 336.063 | fail    |
    +------------------------------------------------------------------------------------------------------------------------------------------+---------+---------+
    run_tempest - INFO - Results: {'timestart': '2016-04-2615:42:30.384572', 'duration': 1497, 'tests': 188, 'failures': 27}
    run_tempest - INFO - Pushing results to DB: 'http://testresults.opnfv.org/testapi/results'.
    run_tempest - INFO - Deleting tenant and user for Tempest suite)

Rally
^^^^^
::

    FUNCTEST.info: Running Rally benchmark suite...
    run_rally - INFO - Starting test scenario "authenticate" ...

    Preparing input task
    Task  ad742546-c147-4903-a31f-841de938dd68: started
    Task ad742546-c147-4903-a31f-841de938dd68: finished

    test scenario Authenticate.validate_glance
    +-----------------------------------------------------------------------------------------------------------------------------------------+
    |                                                          Response Times (sec)                                                           |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_glance_2_times | 0.196     | 0.321        | 0.365        | 0.372        | 0.38      | 0.302     | 100.0%  | 10    |
    | total                                | 0.278     | 0.405        | 0.481        | 0.487        | 0.492     | 0.398     | 100.0%  | 10    |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.25959300995
    Full duration: 4.72824001312

    test scenario Authenticate.keystone
    +--------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                   |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.keystone | 0.076     | 0.084        | 0.111        | 0.116        | 0.121     | 0.09      | 100.0%  | 10    |
    | total                 | 0.076     | 0.084        | 0.111        | 0.116        | 0.121     | 0.09      | 100.0%  | 10    |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.271264076233
    Full duration: 3.62738013268

    test scenario Authenticate.validate_heat
    +---------------------------------------------------------------------------------------------------------------------------------------+
    |                                                         Response Times (sec)                                                          |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_heat_2_times | 0.175     | 0.197        | 0.249        | 0.254        | 0.258     | 0.207     | 100.0%  | 10    |
    | total                              | 0.254     | 0.297        | 0.383        | 0.398        | 0.413     | 0.316     | 100.0%  | 10    |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.942983865738
    Full duration: 4.24797916412

    test scenario Authenticate.validate_nova
    +---------------------------------------------------------------------------------------------------------------------------------------+
    |                                                         Response Times (sec)                                                          |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_nova_2_times | 0.119     | 0.158        | 0.214        | 0.226        | 0.237     | 0.164     | 100.0%  | 10    |
    | total                              | 0.206     | 0.255        | 0.317        | 0.323        | 0.329     | 0.261     | 100.0%  | 10    |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.78842997551
    Full duration: 4.25593304634

    test scenario Authenticate.validate_cinder
    +-----------------------------------------------------------------------------------------------------------------------------------------+
    |                                                          Response Times (sec)                                                           |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_cinder_2_times | 0.119     | 0.189        | 0.375        | 0.376        | 0.378     | 0.229     | 100.0%  | 10    |
    | total                                | 0.2       | 0.333        | 0.46         | 0.479        | 0.499     | 0.336     | 100.0%  | 10    |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.973871946335
    Full duration: 4.23989796638

    test scenario Authenticate.validate_neutron
    +------------------------------------------------------------------------------------------------------------------------------------------+
    |                                                           Response Times (sec)                                                           |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_neutron_2_times | 0.195     | 0.211        | 0.231        | 0.247        | 0.263     | 0.215     | 100.0%  | 10    |
    | total                                 | 0.277     | 0.305        | 0.331        | 0.345        | 0.359     | 0.309     | 100.0%  | 10    |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.916023015976
    Full duration: 4.58919405937

    2016-04-26 17:13:30,899 - run_rally - INFO - Test scenario: "authenticate" OK.
    2016-04-26 17:13:30,899 - run_rally - INFO - Starting test scenario "glance" ...
    2016-04-26 17:15:24,362 - run_rally - INFO -
     Preparing input task
     Task  9f0a1a59-63ee-4c5c-83b4-fda6ca64d4d3: started
    Task 9f0a1a59-63ee-4c5c-83b4-fda6ca64d4d3: finished

    test scenario GlanceImages.list_images
    +-----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                  |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.list_images | 0.265     | 0.322        | 0.356        | 0.383        | 0.411     | 0.319     | 100.0%  | 10    |
    | total              | 0.265     | 0.322        | 0.356        | 0.383        | 0.411     | 0.319     | 100.0%  | 10    |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.958132982254
    Full duration: 5.75791287422

    test scenario GlanceImages.create_image_and_boot_instances
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 3.814     | 4.56         | 5.238        | 5.417        | 5.597     | 4.572     | 100.0%  | 10    |
    | nova.boot_servers   | 6.063     | 7.369        | 7.972        | 8.963        | 9.955     | 7.357     | 100.0%  | 10    |
    | total               | 10.969    | 11.692       | 12.712       | 13.839       | 14.965    | 11.929    | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 34.7748630047
    Full duration: 56.4055418968

    test scenario GlanceImages.create_and_list_image
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 3.733     | 4.173        | 4.872        | 4.909        | 4.946     | 4.299     | 100.0%  | 10    |
    | glance.list_images  | 0.034     | 0.108        | 0.128        | 0.141        | 0.153     | 0.1       | 100.0%  | 10    |
    | total               | 3.841     | 4.25         | 4.982        | 5.018        | 5.055     | 4.399     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 13.4400930405
    Full duration: 21.2837600708

    test scenario GlanceImages.create_and_delete_image
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 3.579     | 4.549        | 4.615        | 4.621        | 4.627     | 4.302     | 100.0%  | 10    |
    | glance.delete_image | 0.561     | 0.882        | 1.06         | 1.077        | 1.093     | 0.878     | 100.0%  | 10    |
    | total               | 4.529     | 5.366        | 5.55         | 5.629        | 5.707     | 5.18      | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 15.3838078976
    Full duration: 20.4000329971

    2016-04-26 17:15:25,993 - run_rally - INFO - Test scenario: "glance" OK.
    2016-04-26 17:15:25,993 - run_rally - INFO - Starting test scenario "cinder" ...
    2016-04-26 17:30:47,609 - run_rally - INFO -
     Preparing input task
     Task  814c7265-77f0-4627-b851-4d6307469184: started
    Task 814c7265-77f0-4627-b851-4d6307469184: finished

    test scenario CinderVolumes.create_and_attach_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server     | 3.253     | 3.8          | 5.748        | 5.876        | 6.003     | 4.299     | 100.0%  | 10    |
    | cinder.create_volume | 2.647     | 2.849        | 3.122        | 3.314        | 3.506     | 2.905     | 100.0%  | 10    |
    | nova.attach_volume   | 2.828     | 2.941        | 3.024        | 3.139        | 3.253     | 2.956     | 100.0%  | 10    |
    | nova.detach_volume   | 2.694     | 2.805        | 3.047        | 3.066        | 3.085     | 2.854     | 100.0%  | 10    |
    | cinder.delete_volume | 0.465     | 2.501        | 2.589        | 2.62         | 2.652     | 2.292     | 100.0%  | 10    |
    | nova.delete_server   | 2.31      | 2.432        | 2.572        | 2.61         | 2.647     | 2.445     | 100.0%  | 10    |
    | total                | 17.005    | 17.344       | 19.667       | 19.684       | 19.702    | 17.752    | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 52.3380470276
    Full duration: 62.1368570328

    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 5.365     | 5.628        | 6.335        | 7.213        | 8.09      | 5.894     | 100.0%  | 10    |
    | cinder.list_volumes  | 0.12      | 0.13         | 0.179        | 0.324        | 0.47      | 0.165     | 100.0%  | 10    |
    | total                | 5.492     | 5.753        | 6.503        | 7.531        | 8.56      | 6.059     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 17.5699410439
    Full duration: 32.550137043

    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 2.66      | 2.948        | 3.145        | 3.171        | 3.197     | 2.939     | 100.0%  | 10    |
    | cinder.list_volumes  | 0.039     | 0.124        | 0.137        | 0.145        | 0.153     | 0.12      | 100.0%  | 10    |
    | total                | 2.765     | 3.073        | 3.28         | 3.3          | 3.32      | 3.059     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 8.95114684105
    Full duration: 20.4319190979

    test scenario CinderVolumes.create_and_list_snapshots
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_snapshot | 2.53      | 4.717        | 6.846        | 6.861        | 6.875     | 4.502     | 100.0%  | 10    |
    | cinder.list_snapshots  | 0.017     | 0.106        | 0.12         | 0.135        | 0.15      | 0.094     | 100.0%  | 10    |
    | total                  | 2.68      | 4.789        | 6.9          | 6.926        | 6.953     | 4.596     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 12.3801140785
    Full duration: 44.4814119339

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 2.72      | 2.87         | 2.984        | 3.001        | 3.018     | 2.88      | 100.0%  | 10    |
    | cinder.delete_volume | 2.327     | 2.533        | 2.641        | 2.663        | 2.685     | 2.526     | 100.0%  | 10    |
    | total                | 5.148     | 5.386        | 5.625        | 5.664        | 5.703     | 5.406     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 16.1617929935
    Full duration: 23.7529392242

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 5.261     | 5.487        | 5.686        | 5.742        | 5.797     | 5.493     | 100.0%  | 10    |
    | cinder.delete_volume | 2.393     | 2.591        | 2.671        | 2.776        | 2.881     | 2.572     | 100.0%  | 10    |
    | total                | 7.72      | 8.0          | 8.304        | 8.491        | 8.679     | 8.065     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 23.9920217991
    Full duration: 31.16101408

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 2.683     | 2.83         | 2.958        | 3.031        | 3.105     | 2.838     | 100.0%  | 10    |
    | cinder.delete_volume | 2.446     | 2.601        | 2.755        | 2.757        | 2.759     | 2.621     | 100.0%  | 10    |
    | total                | 5.209     | 5.463        | 5.632        | 5.673        | 5.715     | 5.459     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 16.2941839695
    Full duration: 23.1591808796

    test scenario CinderVolumes.create_and_upload_volume_to_image
    +----------------------------------------------------------------------------------------------------------------------------------+
    |                                                       Response Times (sec)                                                       |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                        | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume          | 2.705     | 3.234        | 5.839        | 6.009        | 6.178     | 4.101     | 100.0%  | 10    |
    | cinder.upload_volume_to_image | 25.866    | 34.579       | 36.121       | 36.966       | 37.811    | 33.004    | 100.0%  | 10    |
    | cinder.delete_volume          | 2.425     | 2.516        | 2.859        | 3.79         | 4.722     | 2.741     | 100.0%  | 10    |
    | nova.delete_image             | 1.063     | 1.781        | 2.315        | 2.368        | 2.421     | 1.768     | 100.0%  | 10    |
    | total                         | 33.42     | 42.477       | 46.051       | 46.561       | 47.071    | 41.614    | 100.0%  | 10    |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 122.33260107
    Full duration: 130.417927027

    test scenario CinderVolumes.create_and_delete_snapshot
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_snapshot | 2.619     | 4.753        | 5.128        | 5.998        | 6.868     | 4.741     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.341     | 4.464        | 4.614        | 4.628        | 4.642     | 3.881     | 100.0%  | 10    |
    | total                  | 5.069     | 9.108        | 9.651        | 10.58        | 11.51     | 8.622     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 23.5147559643
    Full duration: 42.4243760109

    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 2.687     | 2.862        | 5.341        | 5.342        | 5.342     | 3.334     | 100.0%  | 10    |
    | total                | 2.687     | 2.862        | 5.341        | 5.342        | 5.343     | 3.335     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 8.59894013405
    Full duration: 18.9968831539

    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 2.891     | 3.117        | 5.147        | 5.186        | 5.225     | 3.853     | 100.0%  | 10    |
    | total                | 2.892     | 3.118        | 5.147        | 5.186        | 5.225     | 3.853     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 11.1855640411
    Full duration: 23.8357381821

    test scenario CinderVolumes.list_volumes
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.list_volumes | 0.23      | 0.276        | 0.313        | 0.333        | 0.353     | 0.281     | 100.0%  | 10    |
    | total               | 0.23      | 0.276        | 0.313        | 0.333        | 0.354     | 0.281     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.832192182541
    Full duration: 49.1499869823

    test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | 2.745     | 3.988        | 5.311        | 5.419        | 5.527     | 4.036     | 100.0%  | 10    |
    | cinder.create_snapshot | 2.448     | 3.519        | 4.951        | 5.828        | 6.704     | 3.762     | 100.0%  | 10    |
    | nova.attach_volume     | 2.902     | 4.661        | 5.677        | 6.517        | 7.356     | 4.515     | 100.0%  | 10    |
    | nova.detach_volume     | 2.665     | 3.03         | 5.013        | 5.036        | 5.058     | 3.398     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.347     | 2.526        | 4.474        | 4.544        | 4.615     | 3.094     | 100.0%  | 10    |
    | cinder.delete_volume   | 2.357     | 2.512        | 2.616        | 2.622        | 2.629     | 2.497     | 100.0%  | 10    |
    | total                  | 16.23     | 22.038       | 24.243       | 25.404       | 26.565    | 21.659    | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 61.302448988
    Full duration: 101.445744038

    test scenario CinderVolumes.create_from_volume_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.012     | 5.284        | 7.846        | 8.73         | 9.613     | 5.488     | 100.0%  | 10    |
    | cinder.delete_volume | 2.465     | 4.731        | 6.986        | 7.116        | 7.247     | 4.39      | 100.0%  | 10    |
    | total                | 5.537     | 10.039       | 14.516       | 14.707       | 14.898    | 9.877     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 25.7450320721
    Full duration: 44.7656638622

    test scenario CinderVolumes.create_and_extend_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 2.809     | 2.87         | 3.171        | 3.173        | 3.174     | 2.925     | 100.0%  | 10    |
    | cinder.extend_volume | 2.68      | 2.828        | 5.155        | 5.156        | 5.157     | 3.67      | 100.0%  | 10    |
    | cinder.delete_volume | 2.351     | 2.533        | 2.633        | 2.64         | 2.648     | 2.537     | 100.0%  | 10    |
    | total                | 8.073     | 8.443        | 10.604       | 10.657       | 10.711    | 9.133     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 26.884996891
    Full duration: 34.1721270084

    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | 2.775     | 2.863        | 2.974        | 3.062        | 3.151     | 2.888     | 100.0%  | 10    |
    | cinder.create_snapshot | 2.383     | 3.589        | 6.958        | 7.815        | 8.672     | 4.208     | 100.0%  | 10    |
    | nova.attach_volume     | 2.875     | 3.242        | 5.488        | 6.395        | 7.302     | 4.124     | 100.0%  | 10    |
    | nova.detach_volume     | 2.665     | 2.896        | 3.035        | 3.047        | 3.059     | 2.879     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.154     | 2.468        | 2.771        | 3.49         | 4.209     | 2.6       | 100.0%  | 10    |
    | cinder.delete_volume   | 0.443     | 2.52         | 2.652        | 2.664        | 2.677     | 2.341     | 100.0%  | 10    |
    | total                  | 16.386    | 19.141       | 21.529       | 23.357       | 25.184    | 19.466    | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 56.0006937981
    Full duration: 103.148792982

    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | 2.734     | 2.837        | 2.972        | 2.98         | 2.987     | 2.853     | 100.0%  | 10    |
    | cinder.create_snapshot | 2.361     | 4.585        | 7.125        | 7.96         | 8.794     | 4.799     | 100.0%  | 10    |
    | nova.attach_volume     | 2.861     | 3.062        | 5.2          | 5.255        | 5.311     | 3.579     | 100.0%  | 10    |
    | nova.detach_volume     | 2.776     | 2.919        | 3.111        | 3.147        | 3.183     | 2.942     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.381     | 3.48         | 6.541        | 6.595        | 6.649     | 3.908     | 100.0%  | 10    |
    | cinder.delete_volume   | 2.273     | 2.579        | 4.795        | 5.881        | 6.967     | 3.176     | 100.0%  | 10    |
    | total                  | 16.565    | 23.291       | 23.896       | 24.12        | 24.344    | 21.919    | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 62.6618189812
    Full duration: 108.85529089

SDN Controller
--------------

ODL
^^^
::

    FUNCTEST.info: Running ODL test...
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
    Check Network :: Check Network created in OpenDaylight                | FAIL |
    404 != 200
    ------------------------------------------------------------------------------
    Neutron.Networks :: Checking Network created in OpenStack are push... | FAIL |
    4 critical tests, 3 passed, 1 failed
    4 tests total, 3 passed, 1 failed
    ==============================================================================
    Neutron.Subnets :: Checking Subnets created in OpenStack are pushed to Open...
    ==============================================================================
    Check OpenStack Subnets :: Checking OpenStack Neutron for known Su... | PASS |
    ------------------------------------------------------------------------------
    Check OpenDaylight subnets :: Checking OpenDaylight Neutron API fo... | PASS |
    ------------------------------------------------------------------------------
    Create New subnet :: Create new subnet in OpenStack                   | PASS |
    ------------------------------------------------------------------------------
    Check New subnet :: Check new subnet created in OpenDaylight          | FAIL |
    404 != 200
    ------------------------------------------------------------------------------
    Neutron.Subnets :: Checking Subnets created in OpenStack are pushe... | FAIL |
    4 critical tests, 3 passed, 1 failed
    4 tests total, 3 passed, 1 failed
    ==============================================================================
    Neutron.Ports :: Checking Port created in OpenStack are pushed to OpenDaylight
    ==============================================================================
    Check OpenStack ports :: Checking OpenStack Neutron for known ports   | PASS |
    ------------------------------------------------------------------------------
    Check OpenDaylight ports :: Checking OpenDaylight Neutron API for ... | PASS |
    ------------------------------------------------------------------------------
    Create New Port :: Create new port in OpenStack                       | PASS |
    ------------------------------------------------------------------------------
    Check New Port :: Check new subnet created in OpenDaylight            | FAIL |
    404 != 200
    ------------------------------------------------------------------------------
    Neutron.Ports :: Checking Port created in OpenStack are pushed to ... | FAIL |
    4 critical tests, 3 passed, 1 failed
    4 tests total, 3 passed, 1 failed
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
    Neutron :: Test suite for Neutron Plugin                              | FAIL |
    18 critical tests, 15 passed, 3 failed
    18 tests total, 15 passed, 3 failed
    ==============================================================================
    Output:  /home/opnfv/output.xml
    Log:     /home/opnfv/log.html
    Report:  /home/opnfv/report.html
    Log:     /home/opnfv/log.html
    Report:  /home/opnfv/report.html

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
    vIMS - INFO - Cloudify deployment Start Time:'2016-02-23 08:04:17'
    vIMS - INFO - Writing the inputs file
    vIMS - INFO - Launching the cloudify-manager deployment
    vIMS - INFO - Cloudify-manager server is UP !
    vIMS - INFO - Cloudify deployment duration:'495.7'
    vIMS - INFO - Collect flavor id for all clearwater vm
    vIMS - INFO - vIMS VNF deployment Start Time:'2016-02-23 08:12:33'
    vIMS - INFO - Downloading the openstack-blueprint.yaml blueprint
    vIMS - INFO - Writing the inputs file
    vIMS - INFO - Launching the clearwater deployment
    vIMS - INFO - The deployment of clearwater-opnfv is ended
    vIMS - INFO - vIMS VNF deployment duration:'759.1'
    vIMS - INFO - vIMS functional test Start Time:'2016-02-23 08:28:17'
    vIMS - INFO - vIMS functional test duration:'109.1'
    vIMS - INFO - Launching the clearwater-opnfv undeployment
    vIMS - ERROR - Error when executing command /bin/bash -c 'source /home/opnfv/functest/data/vIMS/venv_cloudify/bin/activate; cd /home/opnfv/functest/data/vIMS/; cfy executions start -w uninstall -d clearwater-opnfv --timeout 1800 ; cfy deployments delete -d clearwater-opnfv; '
    vIMS - INFO - Launching the cloudify-manager undeployment
    vIMS - INFO - Cloudify-manager server has been successfully removed!
    vIMS - INFO - Removing vIMS tenant ..
    vIMS - INFO - Removing vIMS user ..

Doctor
^^^^^^

::

    FUNCTEST.info: Running Doctor test...
    doctor - DEBUG - Executing command : cd /home/opnfv/repos/doctor/tests && ./run.sh
    doctor - DEBUG - + IMAGE_URL=https://launchpad.net/cirros/trunk/0.3.0/+download/cirros-0.3.0-x86_64-disk.img
    Note: doctor/tests/run.sh has been executed.
    PING 192.30.9.7 (192.30.9.7) 56(84) bytes of data.
    64 bytes from 192.30.9.7: icmp_seq=1 ttl=63 time=0.753 ms

    --- 192.30.9.7 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 0.753/0.753/0.753/0.000 ms
    preparing VM image...
    +------------------+--------------------------------------+
    | Property         | Value                                |
    +------------------+--------------------------------------+
    | checksum         | 7ca2842a166c276d49880998e4b397d5     |
    | container_format | bare                                 |
    | created_at       | 2016-04-26T17:07:58Z                 |
    | disk_format      | qcow2                                |
    | id               | ccc11584-d901-4c83-9bbe-1e35b12f03ee |
    | min_disk         | 0                                    |
    | min_ram          | 0                                    |
    | name             | cirros                               |
    | owner            | 8f39920048ea444d9dedb35e601c1292     |
    | protected        | False                                |
    | size             | 15446                                |
    | status           | active                               |
    | tags             | []                                   |
    | updated_at       | 2016-04-26T17:07:59Z                 |
    | virtual_size     | None                                 |
    | visibility       | public                               |
    +------------------+--------------------------------------+
    starting doctor sample components...
    creating VM and alarm...
    +--------------------------------------+-----------------------------------------------+
    | Property                             | Value                                         |
    +--------------------------------------+-----------------------------------------------+
    | OS-DCF:diskConfig                    | MANUAL                                        |
    | OS-EXT-AZ:availability_zone          |                                               |
    | OS-EXT-SRV-ATTR:host                 | -                                             |
    | OS-EXT-SRV-ATTR:hypervisor_hostname  | -                                             |
    | OS-EXT-SRV-ATTR:instance_name        | instance-00000048                             |
    | OS-EXT-STS:power_state               | 0                                             |
    | OS-EXT-STS:task_state                | scheduling                                    |
    | OS-EXT-STS:vm_state                  | building                                      |
    | OS-SRV-USG:launched_at               | -                                             |
    | OS-SRV-USG:terminated_at             | -                                             |
    | accessIPv4                           |                                               |
    | accessIPv6                           |                                               |
    | adminPass                            | AaUNZaoqw74Q                                  |
    | config_drive                         |                                               |
    | created                              | 2016-04-26T17:08:01Z                          |
    | flavor                               | m1.tiny (1)                                   |
    | hostId                               |                                               |
    | id                                   | 1ab94214-1d8c-46b5-8467-3d3e3b602f04          |
    | image                                | cirros (0074bf80-807e-4cb7-b904-bf4347c2a668) |
    | key_name                             | -                                             |
    | metadata                             | {}                                            |
    | name                                 | doctor_vm1                                    |
    | os-extended-volumes:volumes_attached | []                                            |
    | progress                             | 0                                             |
    | security_groups                      | default                                       |
    | status                               | BUILD                                         |
    | tenant_id                            | 3d15a63c2519439f839df6785236b0e1              |
    | updated                              | 2016-02-24T07:59:49Z                          |
    | user_id                              | 0cfa3d72e33b490880278ff6676aa961              |
    +--------------------------------------+-----------------------------------------------+

    +---------------------------+----------------------------------------------------------------------+
    | Property                  | Value                                                                |
    +---------------------------+----------------------------------------------------------------------+
    | alarm_actions             | ["http://localhost:12346/failure"]                                   |
    | alarm_id                  | 739ca887-1a9d-4fb4-ad77-17793de1db16                                 |
    | description               | VM failure                                                           |
    | enabled                   | True                                                                 |
    | event_type                | compute.instance.update                                              |
    | insufficient_data_actions | []                                                                   |
    | name                      | doctor_alarm1                                                        |
    | ok_actions                | []                                                                   |
    | project_id                | 3d15a63c2519439f839df6785236b0e1                                     |
    | query                     | [{"field": "traits.state", "type": "string", "value": "error", "op": |
    |                           | "eq"}, {"field": "traits.instance_id", "type": "string", "value":    |
    |                           | "1ab94214-1d8c-46b5-8467-3d3e3b602f04", "op": "eq"}]                 |
    | repeat_actions            | False                                                                |
    | severity                  | moderate                                                             |
    | state                     | insufficient data                                                    |
    | type                      | event                                                                |
    | user_id                   | 0cfa3d72e33b490880278ff6676aa961                                     |
    +---------------------------+----------------------------------------------------------------------+
    waiting for vm launch...
    injecting host failure...
    disabling network of comupte host [overcloud-novacompute-0] for 3 mins...
    Warning: Permanently added '192.30.9.7' (ECDSA) to the list of known hosts.
    Warning: Permanently added '192.30.9.7' (ECDSA) to the list of known hosts.
    0 OK
    done
    cleanup...
    24120
    24124
    24122
    24144
    Your request was processed by a Nova API which does not support microversions (X-OpenStack-Nova-API-Version header is missing from response). Warning: Response may be incorrect.
    Your request was processed by a Nova API which does not support microversions (X-OpenStack-Nova-API-Version header is missing from response). Warning: Response may be incorrect.
    Your request was processed by a Nova API which does not support microversions (X-OpenStack-Nova-API-Version header is missing from response). Warning: Response may be incorrect.
    Your request was processed by a Nova API which does not support microversions (X-OpenStack-Nova-API-Version header is missing from response). Warning: Response may be incorrect.
    24125
    24136
    + ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i instack_key heat-admin@192.30.9.7 '[ -e disable_network.log ] && cat disable_network.log'
    Warning: Permanently added '192.30.9.7' (ECDSA) to the list of known hosts.
    sudo ip link set enp8s0 down
    <Response [200]>
    Request to delete server doctor_vm1 has been accepted.
    waiting disabled compute host back to be enabled...

    doctor - INFO - doctor OK

bgpvpn
^^^^^^

::

    ${PYTHON:-python} -m subunit.run discover -t ${OS_TOP_LEVEL:-./} ${OS_TEST_PATH:-./tempest/test_discover}  --load-list /tmp/tmpvjQxKe
    {0} networking_bgpvpn_tempest.tests.api.test_bgpvpn.BgpvpnTest.test_create_bgpvpn [0.191925s] ... ok
    {0} networking_bgpvpn_tempest.tests.api.test_bgpvpn.BgpvpnTest.test_create_bgpvpn_as_non_admin_fail [0.078978s] ... ok

    ======
    Totals
    ======
    Ran: 2 tests in 7.0000 sec.
     - Passed: 2
     - Skipped: 0
     - Expected Fail: 0
     - Unexpected Success: 0
     - Failed: 0
    Sum of execute time for each test: 0.2709 sec.
