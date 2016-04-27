.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for fuel-os-nosdn-kvm-ha
----------------------------------------------

VIM
---

Tempest
^^^^^^^
::

    +---------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    | name                                                                                                                      | time      | status  |
    +---------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                | 0.37487   | success |
    | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                              | 0.09209   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create | 0.94115   | success |
    | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list   | 1.59631   | success |
    | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete   | 3.03178   | success |
    | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                      | 11.13795  | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                          | 0.07863   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                 | 0.00116   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                    | 0.08504   | success |
    | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                           | 0.00099   | success |
    | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                             | 7.63607   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                      | 0.06693   | success |
    | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network           | 0.13367   | success |
    | tempest.api.data_processing.test_cluster_templates.ClusterTemplateTest.test_cluster_template_create                       | 0.0       | skip    |
    | tempest.api.data_processing.test_cluster_templates.ClusterTemplateTest.test_cluster_template_delete                       | 0.0       | skip    |
    | tempest.api.data_processing.test_cluster_templates.ClusterTemplateTest.test_cluster_template_get                          | 0.0       | skip    |
    | tempest.api.data_processing.test_cluster_templates.ClusterTemplateTest.test_cluster_template_list                         | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_external_hdfs_data_source_create                        | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_external_hdfs_data_source_delete                        | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_external_hdfs_data_source_get                           | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_external_hdfs_data_source_list                          | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_local_hdfs_data_source_create                           | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_local_hdfs_data_source_delete                           | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_local_hdfs_data_source_get                              | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_local_hdfs_data_source_list                             | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_swift_data_source_create                                | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_swift_data_source_delete                                | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_swift_data_source_get                                   | 0.0       | skip    |
    | tempest.api.data_processing.test_data_sources.DataSourceTest.test_swift_data_source_list                                  | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binaries.JobBinaryTest.test_internal_db_job_binary_create                            | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binaries.JobBinaryTest.test_internal_db_job_binary_delete                            | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binaries.JobBinaryTest.test_internal_db_job_binary_get                               | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binaries.JobBinaryTest.test_internal_db_job_binary_list                              | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binaries.JobBinaryTest.test_job_binary_get_data                                      | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binaries.JobBinaryTest.test_swift_job_binary_create                                  | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binaries.JobBinaryTest.test_swift_job_binary_delete                                  | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binaries.JobBinaryTest.test_swift_job_binary_get                                     | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binaries.JobBinaryTest.test_swift_job_binary_list                                    | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binary_internals.JobBinaryInternalTest.test_job_binary_internal_create               | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binary_internals.JobBinaryInternalTest.test_job_binary_internal_delete               | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binary_internals.JobBinaryInternalTest.test_job_binary_internal_get                  | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binary_internals.JobBinaryInternalTest.test_job_binary_internal_get_data             | 0.0       | skip    |
    | tempest.api.data_processing.test_job_binary_internals.JobBinaryInternalTest.test_job_binary_internal_list                 | 0.0       | skip    |
    | tempest.api.data_processing.test_jobs.JobTest.test_job_create                                                             | 0.0       | skip    |
    | tempest.api.data_processing.test_jobs.JobTest.test_job_delete                                                             | 0.0       | skip    |
    | tempest.api.data_processing.test_jobs.JobTest.test_job_get                                                                | 0.0       | skip    |
    | tempest.api.data_processing.test_jobs.JobTest.test_job_list                                                               | 0.0       | skip    |
    | tempest.api.data_processing.test_node_group_templates.NodeGroupTemplateTest.test_node_group_template_create               | 0.0       | skip    |
    | tempest.api.data_processing.test_node_group_templates.NodeGroupTemplateTest.test_node_group_template_delete               | 0.0       | skip    |
    | tempest.api.data_processing.test_node_group_templates.NodeGroupTemplateTest.test_node_group_template_get                  | 0.0       | skip    |
    | tempest.api.data_processing.test_node_group_templates.NodeGroupTemplateTest.test_node_group_template_list                 | 0.0       | skip    |
    | tempest.api.data_processing.test_plugins.PluginsTest.test_plugin_get                                                      | 0.0       | skip    |
    | tempest.api.data_processing.test_plugins.PluginsTest.test_plugin_list                                                     | 0.0       | skip    |
    | tempest.api.database.flavors.test_flavors.DatabaseFlavorsTest.test_compare_db_flavors_with_os                             | 0.0       | skip    |
    | tempest.api.database.flavors.test_flavors.DatabaseFlavorsTest.test_get_db_flavor                                          | 0.0       | skip    |
    | tempest.api.database.flavors.test_flavors.DatabaseFlavorsTest.test_list_db_flavors                                        | 0.0       | skip    |
    | tempest.api.database.limits.test_limits.DatabaseLimitsTest.test_absolute_limits                                           | 0.0       | skip    |
    | tempest.api.database.versions.test_versions.DatabaseVersionsTest.test_list_db_versions                                    | 0.0       | skip    |
    | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                           | 0.57347   | success |
    | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                   | 0.17627   | success |
    | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete              | 0.33315   | success |
    | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                               | 0.08263   | success |
    | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                               | 0.82181   | success |
    | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                       | 0.42812   | success |
    | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                               | 1.89984   | success |
    | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                             | 0.33804   | success |
    | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                            | 0.26122   | success |
    | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_show_list                                | 0.43116   | success |
    | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                               | 0.40022   | success |
    | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                            | 1.70626   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                          | 0.07075   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                    | 0.06209   | success |
    | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                     | 0.06225   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                          | 0.08494   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                    | 0.04772   | success |
    | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                     | 0.05578   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                              | 1.27065   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                            | 2.38206   | success |
    | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                              | 2.46710   | success |
    | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                          | 2.88813   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address            | 0.91435   | success |
    | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                  | 1.63719   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_network                                  | 1.30351   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_port                                     | 1.98554   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsIpV6Test.test_bulk_create_delete_subnet                                   | 3.09141   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTest.test_bulk_create_delete_network                                      | 1.40844   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTest.test_bulk_create_delete_port                                         | 1.67281   | success |
    | tempest.api.network.test_networks.BulkNetworkOpsTest.test_bulk_create_delete_subnet                                       | 2.34230   | success |
    | tempest.api.network.test_networks.NetworksIpV6Test.test_create_update_delete_network_subnet                               | 1.77383   | success |
    | tempest.api.network.test_networks.NetworksIpV6Test.test_external_network_visibility                                       | 0.27369   | success |
    | tempest.api.network.test_networks.NetworksIpV6Test.test_list_networks                                                     | 0.21206   | success |
    | tempest.api.network.test_networks.NetworksIpV6Test.test_list_subnets                                                      | 0.05304   | success |
    | tempest.api.network.test_networks.NetworksIpV6Test.test_show_network                                                      | 0.03923   | success |
    | tempest.api.network.test_networks.NetworksIpV6Test.test_show_subnet                                                       | 0.21345   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                          | 1.96905   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                  | 0.41775   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                | 0.04545   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                 | 0.03878   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                 | 0.03483   | success |
    | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                  | 0.19582   | success |
    | tempest.api.network.test_networks.NetworksTest.test_create_update_delete_network_subnet                                   | 1.74789   | success |
    | tempest.api.network.test_networks.NetworksTest.test_external_network_visibility                                           | 0.23307   | success |
    | tempest.api.network.test_networks.NetworksTest.test_list_networks                                                         | 0.05593   | success |
    | tempest.api.network.test_networks.NetworksTest.test_list_subnets                                                          | 0.03420   | success |
    | tempest.api.network.test_networks.NetworksTest.test_show_network                                                          | 0.22495   | success |
    | tempest.api.network.test_networks.NetworksTest.test_show_subnet                                                           | 0.04874   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                             | 1.87449   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                  | 1.73660   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                           | 1.47535   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                          | 0.07632   | success |
    | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                           | 0.22105   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                 | 1.88100   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                      | 2.43974   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                               | 0.73850   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                              | 0.23058   | success |
    | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                               | 0.22952   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                      | 4.10475   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                            | 2.05694   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                          | 1.35753   | success |
    | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                               | 1.43959   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                          | 3.83507   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                | 2.17349   | success |
    | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                              | 1.93067   | success |
    | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                   | 1.12709   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group              | 1.29264   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                     | 1.59275   | success |
    | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                       | 0.03756   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                  | 1.57130   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                         | 1.52547   | success |
    | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                           | 0.05488   | success |
    | tempest.api.network.test_subnetpools_extensions.SubnetPoolsTestJSON.test_create_list_show_update_delete_subnetpools       | 1.47037   | success |
    | tempest.api.object_storage.test_account_quotas.AccountQuotasTest.test_admin_modify_quota                                  | 0.0       | fail    |
    | tempest.api.object_storage.test_account_quotas.AccountQuotasTest.test_upload_valid_object                                 | 0.0       | fail    |
    | tempest.api.object_storage.test_account_services.AccountTest.test_list_account_metadata                                   | 0.0       | fail    |
    | tempest.api.object_storage.test_account_services.AccountTest.test_list_containers                                         | 0.0       | fail    |
    | tempest.api.object_storage.test_container_quotas.ContainerQuotasTest.test_upload_large_object                             | 0.32095   | fail    |
    | tempest.api.object_storage.test_container_quotas.ContainerQuotasTest.test_upload_too_many_objects                         | 0.02198   | fail    |
    | tempest.api.object_storage.test_container_quotas.ContainerQuotasTest.test_upload_valid_object                             | 0.01216   | fail    |
    | tempest.api.object_storage.test_container_services.ContainerTest.test_create_container                                    | 0.36258   | fail    |
    | tempest.api.object_storage.test_container_services.ContainerTest.test_list_container_contents                             | 0.01330   | fail    |
    | tempest.api.object_storage.test_container_services.ContainerTest.test_list_container_metadata                             | 0.01521   | fail    |
    | tempest.api.object_storage.test_object_services.ObjectTest.test_create_object                                             | 0.0       | fail    |
    | tempest.api.object_storage.test_object_services.ObjectTest.test_get_object                                                | 0.0       | fail    |
    | tempest.api.object_storage.test_object_services.ObjectTest.test_list_object_metadata                                      | 0.0       | fail    |
    | tempest.api.object_storage.test_object_services.ObjectTest.test_update_object_metadata                                    | 0.0       | fail    |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                            | 0.40358   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                            | 4.40282   | success |
    | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                        | 0.04414   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                               | 1.05533   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                           | 0.48932   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                               | 0.49844   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate               | 0.49092   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change     | 0.60408   | success |
    | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change   | 0.63262   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                  | 2.74910   | success |
    | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                      | 0.04588   | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications | 5.96533   | success |
    | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications | 2.93564   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                        | 2.06137   | success |
    | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                        | 2.08282   | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                 | 7.85484   | success |
    | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                      | 13.98156  | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                 | 7.31661   | success |
    | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                      | 14.01416  | success |
    | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                               | 0.06604   | success |
    | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                               | 0.25951   | success |
    | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                        | 49.36369  | success |
    | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basic_ops                                           | 25.33085  | success |
    | tempest.scenario.test_server_multinode.TestServerMultinode.test_schedule_to_all_nodes                                     | 0.0       | skip    |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                  | 103.45858 | success |
    | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                | 76.91454  | success |
    +---------------------------------------------------------------------------------------------------------------------------+-----------+---------+
    2016-04-26 01:22:55,788 - run_tempest - INFO - Results: {'timestart': '2016-04-2601:09:10.555191', 'duration': 824, 'tests': 171, 'failures': 14}

Rally
^^^^^
::

    FUNCTEST.info: Running Rally benchmark suite...
    2016-04-26 01:24:50,982 - run_rally - INFO - Starting test scenario "authenticate" ...
    2016-04-26 01:25:56,731 - run_rally - INFO -
     Preparing input task
     Task  8204ef26-e392-473b-b607-fe79c30f3c6c: started
    Task 8204ef26-e392-473b-b607-fe79c30f3c6c: finished

    test scenario Authenticate.validate_glance
    +-----------------------------------------------------------------------------------------------------------------------------------------+
    |                                                          Response Times (sec)                                                           |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_glance_2_times | 0.823     | 0.883        | 0.951        | 0.954        | 0.957     | 0.885     | 100.0%  | 10    |
    | total                                | 1.01      | 1.089        | 1.144        | 1.158        | 1.172     | 1.085     | 100.0%  | 10    |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 3.33679389954
    Full duration: 10.0142049789

    test scenario Authenticate.keystone
    +--------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                   |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.keystone | 0.173     | 0.191        | 0.195        | 0.201        | 0.206     | 0.189     | 100.0%  | 10    |
    | total                 | 0.173     | 0.191        | 0.195        | 0.201        | 0.206     | 0.189     | 100.0%  | 10    |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.59915304184
    Full duration: 6.89671802521

    test scenario Authenticate.validate_heat
    +---------------------------------------------------------------------------------------------------------------------------------------+
    |                                                         Response Times (sec)                                                          |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_heat_2_times | 0.436     | 0.468        | 0.496        | 0.499        | 0.502     | 0.47      | 100.0%  | 10    |
    | total                              | 0.637     | 0.668        | 0.704        | 0.705        | 0.707     | 0.671     | 100.0%  | 10    |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.02648496628
    Full duration: 8.63242101669

    test scenario Authenticate.validate_nova
    +---------------------------------------------------------------------------------------------------------------------------------------+
    |                                                         Response Times (sec)                                                          |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_nova_2_times | 0.245     | 0.281        | 0.405        | 0.41         | 0.416     | 0.301     | 100.0%  | 10    |
    | total                              | 0.423     | 0.459        | 0.585        | 0.607        | 0.628     | 0.488     | 100.0%  | 10    |
    +------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.44381713867
    Full duration: 8.15497398376

    test scenario Authenticate.validate_cinder
    +-----------------------------------------------------------------------------------------------------------------------------------------+
    |                                                          Response Times (sec)                                                           |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_cinder_2_times | 0.245     | 0.435        | 0.501        | 0.598        | 0.695     | 0.446     | 100.0%  | 10    |
    | total                                | 0.416     | 0.662        | 0.692        | 0.777        | 0.862     | 0.642     | 100.0%  | 10    |
    +--------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.90059304237
    Full duration: 8.63323712349

    test scenario Authenticate.validate_neutron
    +------------------------------------------------------------------------------------------------------------------------------------------+
    |                                                           Response Times (sec)                                                           |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | authenticate.validate_neutron_2_times | 0.312     | 0.491        | 0.599        | 0.608        | 0.617     | 0.493     | 100.0%  | 10    |
    | total                                 | 0.512     | 0.69         | 0.788        | 0.798        | 0.808     | 0.69      | 100.0%  | 10    |
    +---------------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.07425689697
    Full duration: 8.5414249897

    2016-04-26 01:25:58,048 - run_rally - INFO - Test scenario: "authenticate" OK.

    2016-04-26 01:25:58,314 - run_rally - INFO - Starting test scenario "glance" ...
    2016-04-26 01:29:06,596 - run_rally - INFO -
     Preparing input task
     Task  4929df57-a129-42f5-bf1e-e1acf761f7dd: started
    Task 4929df57-a129-42f5-bf1e-e1acf761f7dd: finished

    test scenario GlanceImages.list_images
    +-----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                  |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.list_images | 0.629     | 0.677        | 0.844        | 0.862        | 0.879     | 0.706     | 100.0%  | 10    |
    | total              | 0.629     | 0.677        | 0.844        | 0.862        | 0.879     | 0.706     | 100.0%  | 10    |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.06210279465
    Full duration: 11.1119971275

    test scenario GlanceImages.create_image_and_boot_instances
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 6.132     | 6.43         | 6.695        | 6.801        | 6.907     | 6.444     | 100.0%  | 10    |
    | nova.boot_servers   | 12.665    | 13.469       | 14.176       | 14.374       | 14.573    | 13.486    | 100.0%  | 10    |
    | total               | 19.057    | 19.947       | 20.84        | 20.94        | 21.039    | 19.931    | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 58.8742520809
    Full duration: 95.2440040112

    test scenario GlanceImages.create_and_list_image
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 6.278     | 6.53         | 7.761        | 11.222       | 14.683    | 7.394     | 100.0%  | 10    |
    | glance.list_images  | 0.299     | 0.472        | 0.515        | 0.522        | 0.529     | 0.462     | 100.0%  | 10    |
    | total               | 6.752     | 7.034        | 8.227        | 11.691       | 15.154    | 7.856     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 22.2857620716
    Full duration: 34.3181619644

    test scenario GlanceImages.create_and_delete_image
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | glance.create_image | 6.137     | 6.554        | 6.898        | 6.924        | 6.95      | 6.58      | 100.0%  | 10    |
    | glance.delete_image | 1.285     | 1.713        | 1.917        | 1.962        | 2.006     | 1.713     | 100.0%  | 10    |
    | total               | 7.602     | 8.362        | 8.696        | 8.748        | 8.799     | 8.292     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 25.0005450249
    Full duration: 34.4151468277

    2016-04-26 01:29:07,930 - run_rally - INFO - Test scenario: "glance" OK.

    2016-04-26 01:29:08,087 - run_rally - INFO - Starting test scenario "cinder" ...
    2016-04-26 02:24:09,641 - run_rally - INFO - Percentage error: n/a, | total                | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |

    2016-04-26 02:24:09,661 - run_rally - INFO - Percentage error: n/a, | total                  | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |

    2016-04-26 02:24:09,663 - run_rally - INFO - Percentage error: n/a, | total                  | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |

    2016-04-26 02:24:09,666 - run_rally - INFO - Percentage error: n/a, | total                  | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |

    2016-04-26 02:24:09,780 - run_rally - INFO -
     Preparing input task
     Task  3d8fb27f-5dfb-4a07-ad7d-cec99384404f: started
    Task 3d8fb27f-5dfb-4a07-ad7d-cec99384404f: finished

    test scenario CinderVolumes.create_and_attach_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server     | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | cinder.create_volume | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | nova.attach_volume   | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | nova.detach_volume   | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | total                | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 438.78555584
    Full duration: 476.062150002

    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 7.312     | 9.44         | 9.821        | 9.964        | 10.107    | 9.128     | 100.0%  | 10    |
    | cinder.list_volumes  | 0.058     | 0.27         | 0.297        | 0.324        | 0.35      | 0.215     | 100.0%  | 10    |
    | total                | 7.37      | 9.626        | 10.164       | 10.275       | 10.386    | 9.343     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 28.7357289791
    Full duration: 47.5475459099

    test scenario CinderVolumes.create_and_list_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.202     | 3.516        | 3.662        | 3.711        | 3.761     | 3.5       | 100.0%  | 10    |
    | cinder.list_volumes  | 0.05      | 0.224        | 0.315        | 0.344        | 0.372     | 0.193     | 100.0%  | 10    |
    | total                | 3.298     | 3.743        | 3.868        | 3.888        | 3.907     | 3.693     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 11.2217340469
    Full duration: 27.984375

    test scenario CinderVolumes.create_and_list_snapshots
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_snapshot | 2.92      | 3.143        | 4.9          | 4.966        | 5.032     | 3.472     | 100.0%  | 10    |
    | cinder.list_snapshots  | 0.023     | 0.029        | 0.218        | 0.233        | 0.248     | 0.072     | 100.0%  | 10    |
    | total                  | 2.955     | 3.197        | 4.927        | 4.993        | 5.06      | 3.545     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 9.69527101517
    Full duration: 42.2511930466

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.018     | 3.457        | 3.685        | 3.737        | 3.788     | 3.413     | 100.0%  | 10    |
    | cinder.delete_volume | 0.914     | 2.612        | 3.053        | 3.069        | 3.085     | 2.563     | 100.0%  | 10    |
    | total                | 3.932     | 6.16         | 6.58         | 6.669        | 6.759     | 5.977     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 17.8796432018
    Full duration: 31.8870809078

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 8.958     | 9.585        | 9.884        | 10.249       | 10.614    | 9.589     | 100.0%  | 10    |
    | cinder.delete_volume | 0.775     | 2.647        | 3.059        | 3.255        | 3.451     | 2.387     | 100.0%  | 10    |
    | total                | 10.49     | 12.128       | 12.864       | 13.066       | 13.269    | 11.977    | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 35.2168581486
    Full duration: 50.825067997

    test scenario CinderVolumes.create_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.192     | 3.607        | 4.26         | 4.265        | 4.27      | 3.682     | 100.0%  | 10    |
    | cinder.delete_volume | 2.551     | 2.625        | 3.0          | 3.039        | 3.079     | 2.731     | 100.0%  | 10    |
    | total                | 5.766     | 6.169        | 7.217        | 7.239        | 7.262     | 6.413     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 19.1643960476
    Full duration: 32.8357338905

    test scenario CinderVolumes.create_and_upload_volume_to_image
    +----------------------------------------------------------------------------------------------------------------------------------+
    |                                                       Response Times (sec)                                                       |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                        | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume          | 3.223     | 3.533        | 3.679        | 3.775        | 3.87      | 3.545     | 100.0%  | 10    |
    | cinder.upload_volume_to_image | 24.815    | 36.631       | 39.206       | 39.953       | 40.701    | 34.888    | 100.0%  | 10    |
    | cinder.delete_volume          | 2.335     | 2.578        | 2.734        | 2.742        | 2.75      | 2.535     | 100.0%  | 10    |
    | nova.delete_image             | 1.988     | 2.228        | 2.551        | 2.734        | 2.917     | 2.296     | 100.0%  | 10    |
    | total                         | 32.77     | 45.39        | 47.552       | 48.244       | 48.935    | 43.265    | 100.0%  | 10    |
    +-------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 124.777842999
    Full duration: 139.828857899

    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.281     | 3.509        | 3.788        | 3.8          | 3.812     | 3.517     | 100.0%  | 10    |
    | total                | 3.281     | 3.509        | 3.788        | 3.8          | 3.813     | 3.517     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 10.4726939201
    Full duration: 25.0890491009

    test scenario CinderVolumes.create_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.219     | 3.547        | 3.845        | 3.858        | 3.872     | 3.556     | 100.0%  | 10    |
    | total                | 3.22      | 3.548        | 3.845        | 3.858        | 3.872     | 3.556     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 10.6221859455
    Full duration: 28.0074269772

    test scenario CinderVolumes.list_volumes
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.list_volumes | 0.459     | 0.521        | 0.574        | 0.58         | 0.585     | 0.523     | 100.0%  | 10    |
    | total               | 0.459     | 0.521        | 0.574        | 0.58         | 0.586     | 0.523     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.56029701233
    Full duration: 54.4247999191

    test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | cinder.create_snapshot | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | nova.attach_volume     | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | nova.detach_volume     | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | total                  | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 428.079464197
    Full duration: 524.52899909

    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | cinder.create_snapshot | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | nova.attach_volume     | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | nova.detach_volume     | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | total                  | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 423.273214102
    Full duration: 1129.47603798

    test scenario CinderVolumes.create_snapshot_and_attach_volume
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume   | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | cinder.create_snapshot | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | nova.attach_volume     | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | nova.detach_volume     | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    | total                  | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 5     |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 426.579771996
    Full duration: 529.032740116

    test scenario CinderVolumes.create_and_delete_snapshot
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_snapshot | 2.8       | 2.961        | 3.287        | 4.217        | 5.148     | 3.157     | 100.0%  | 10    |
    | cinder.delete_snapshot | 2.364     | 2.643        | 2.86         | 2.881        | 2.902     | 2.611     | 100.0%  | 10    |
    | total                  | 5.173     | 5.494        | 6.148        | 7.099        | 8.05      | 5.769     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 16.4653530121
    Full duration: 44.3639709949

    test scenario CinderVolumes.create_and_extend_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.119     | 3.685        | 4.169        | 4.22         | 4.27      | 3.741     | 100.0%  | 10    |
    | cinder.extend_volume | 2.536     | 3.106        | 3.175        | 3.189        | 3.203     | 3.023     | 100.0%  | 10    |
    | cinder.delete_volume | 2.42      | 2.895        | 3.05         | 3.068        | 3.087     | 2.822     | 100.0%  | 10    |
    | total                | 8.68      | 9.571        | 10.355       | 10.358       | 10.362    | 9.586     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 28.6492631435
    Full duration: 42.1216299534

    test scenario CinderVolumes.create_from_volume_and_delete_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 3.108     | 3.632        | 3.846        | 3.968        | 4.089     | 3.621     | 100.0%  | 10    |
    | cinder.delete_volume | 2.54      | 2.847        | 3.276        | 3.29         | 3.304     | 2.881     | 100.0%  | 10    |
    | total                | 6.172     | 6.512        | 6.734        | 6.756        | 6.778     | 6.502     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 19.1909890175
    Full duration: 46.976804018

    2016-04-26 02:24:11,068 - run_rally - INFO - Test scenario: "cinder" Failed.

    2016-04-26 02:24:12,074 - run_rally - INFO - Starting test scenario "heat" ...
    2016-04-26 04:42:36,239 - run_rally - INFO - Percentage error: n/a, | total             | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 6     |

    2016-04-26 04:42:36,363 - run_rally - INFO -
     Preparing input task
     Task  e9e698b5-79f5-41a7-be5f-04761a3c0034: started
    Task e9e698b5-79f5-41a7-be5f-04761a3c0034: finished

    test scenario HeatStacks.create_suspend_resume_delete_stack
    +-----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                  |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack  | 3.62      | 3.722        | 4.104        | 4.115        | 4.126     | 3.846     | 100.0%  | 10    |
    | heat.suspend_stack | 1.392     | 1.475        | 1.609        | 1.616        | 1.623     | 1.493     | 100.0%  | 10    |
    | heat.resume_stack  | 1.339     | 1.369        | 1.514        | 1.533        | 1.553     | 1.406     | 100.0%  | 10    |
    | heat.delete_stack  | 1.283     | 1.429        | 1.447        | 1.461        | 1.474     | 1.382     | 100.0%  | 10    |
    | total              | 7.77      | 8.014        | 8.597        | 8.614        | 8.631     | 8.127     | 100.0%  | 10    |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 24.2256169319
    Full duration: 33.6042699814

    test scenario HeatStacks.create_and_delete_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | 3.528     | 3.756        | 3.905        | 3.933        | 3.961     | 3.764     | 100.0%  | 10    |
    | heat.delete_stack | 1.311     | 1.341        | 1.386        | 1.503        | 1.62      | 1.366     | 100.0%  | 10    |
    | total             | 5.037     | 5.102        | 5.246        | 5.271        | 5.296     | 5.13      | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 15.2723751068
    Full duration: 24.6334218979

    test scenario HeatStacks.create_and_delete_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | 20.555    | 22.623       | 23.694       | 23.77        | 23.845    | 22.663    | 100.0%  | 10    |
    | heat.delete_stack | 9.082     | 10.25        | 10.461       | 10.929       | 11.397    | 9.938     | 100.0%  | 10    |
    | total             | 29.655    | 32.918       | 33.982       | 33.989       | 33.997    | 32.602    | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 97.7232019901
    Full duration: 107.206387043

    test scenario HeatStacks.create_and_delete_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 6     |
    | heat.delete_stack | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 6     |
    | total             | n/a       | n/a          | n/a          | n/a          | n/a       | n/a       | n/a     | 6     |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 7201.48637915
    Full duration: 7812.01388121

    test scenario HeatStacks.list_stacks_and_resources
    +------------------------------------------------------------------------------------------------------------------------------------+
    |                                                        Response Times (sec)                                                        |
    +---------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                          | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.list_stacks                | 0.371     | 0.401        | 0.42         | 0.421        | 0.423     | 0.4       | 100.0%  | 10    |
    | heat.list_resources_of_0_stacks | 0.0       | 0.0          | 0.0          | 0.0          | 0.0       | 0.0       | 100.0%  | 10    |
    | total                           | 0.371     | 0.401        | 0.42         | 0.422        | 0.423     | 0.4       | 100.0%  | 10    |
    +---------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.24707102776
    Full duration: 7.24165606499

    test scenario HeatStacks.create_update_delete_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | 3.41      | 3.442        | 3.472        | 3.481        | 3.49      | 3.444     | 100.0%  | 10    |
    | heat.update_stack | 3.427     | 3.453        | 3.509        | 3.599        | 3.69      | 3.475     | 100.0%  | 10    |
    | heat.delete_stack | 1.295     | 1.311        | 1.326        | 1.329        | 1.332     | 1.312     | 100.0%  | 10    |
    | total             | 8.162     | 8.205        | 8.277        | 8.357        | 8.436     | 8.231     | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 24.6856651306
    Full duration: 32.1383240223

    test scenario HeatStacks.create_update_delete_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | 3.326     | 3.417        | 3.624        | 3.676        | 3.728     | 3.459     | 100.0%  | 10    |
    | heat.update_stack | 3.408     | 3.52         | 3.811        | 3.819        | 3.828     | 3.573     | 100.0%  | 10    |
    | heat.delete_stack | 1.276     | 1.302        | 1.335        | 1.398        | 1.46      | 1.317     | 100.0%  | 10    |
    | total             | 8.14      | 8.309        | 8.56         | 8.596        | 8.632     | 8.349     | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 25.028924942
    Full duration: 32.9079070091

    test scenario HeatStacks.create_update_delete_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | 3.527     | 4.137        | 4.746        | 4.747        | 4.748     | 4.133     | 100.0%  | 10    |
    | heat.update_stack | 5.668     | 5.712        | 5.744        | 5.767        | 5.789     | 5.712     | 100.0%  | 10    |
    | heat.delete_stack | 2.413     | 2.431        | 2.441        | 2.446        | 2.451     | 2.431     | 100.0%  | 10    |
    | total             | 11.652    | 12.305       | 12.891       | 12.9         | 12.909    | 12.276    | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 37.3458311558
    Full duration: 45.2056248188

    test scenario HeatStacks.create_update_delete_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | 4.501     | 4.64         | 4.77         | 4.782        | 4.793     | 4.64      | 100.0%  | 10    |
    | heat.update_stack | 7.947     | 9.065        | 9.146        | 9.207        | 9.269     | 8.97      | 100.0%  | 10    |
    | heat.delete_stack | 2.4       | 2.442        | 2.645        | 3.133        | 3.62      | 2.563     | 100.0%  | 10    |
    | total             | 14.999    | 16.132       | 16.488       | 16.984       | 17.479    | 16.174    | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 49.7609598637
    Full duration: 58.2143821716

    test scenario HeatStacks.create_update_delete_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | 3.481     | 3.63         | 4.77         | 4.771        | 4.772     | 4.024     | 100.0%  | 10    |
    | heat.update_stack | 5.615     | 5.681        | 5.721        | 5.745        | 5.77      | 5.683     | 100.0%  | 10    |
    | heat.delete_stack | 2.4       | 2.433        | 2.467        | 2.492        | 2.516     | 2.438     | 100.0%  | 10    |
    | total             | 11.536    | 11.803       | 12.864       | 12.933       | 13.001    | 12.145    | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 36.3764190674
    Full duration: 44.1169888973

    test scenario HeatStacks.create_update_delete_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | 3.513     | 3.601        | 3.641        | 3.658        | 3.674     | 3.59      | 100.0%  | 10    |
    | heat.update_stack | 3.405     | 3.427        | 3.437        | 3.457        | 3.477     | 3.427     | 100.0%  | 10    |
    | heat.delete_stack | 1.298     | 1.326        | 1.353        | 1.356        | 1.358     | 1.328     | 100.0%  | 10    |
    | total             | 8.251     | 8.353        | 8.412        | 8.416        | 8.42      | 8.345     | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 25.0552000999
    Full duration: 33.6825659275

    test scenario HeatStacks.create_and_list_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | 3.53      | 3.568        | 3.594        | 3.61         | 3.626     | 3.57      | 100.0%  | 10    |
    | heat.list_stacks  | 0.047     | 0.073        | 0.102        | 0.107        | 0.111     | 0.075     | 100.0%  | 10    |
    | total             | 3.6       | 3.639        | 3.69         | 3.696        | 3.702     | 3.646     | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 11.0165708065
    Full duration: 22.4389858246

    test scenario HeatStacks.create_check_delete_stack
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | heat.create_stack | 3.561     | 3.575        | 3.625        | 3.627        | 3.63      | 3.585     | 100.0%  | 10    |
    | heat.check_stack  | 1.396     | 1.41         | 1.433        | 1.439        | 1.445     | 1.413     | 100.0%  | 10    |
    | heat.delete_stack | 1.266     | 1.309        | 1.32         | 1.323        | 1.327     | 1.302     | 100.0%  | 10    |
    | total             | 6.234     | 6.289        | 6.339        | 6.347        | 6.355     | 6.3       | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 18.943114996
    Full duration: 27.5446438789

    2016-04-26 04:42:37,867 - run_rally - INFO - Test scenario: "heat" Failed.

    2016-04-26 04:42:38,263 - run_rally - INFO - Starting test scenario "keystone" ...
    2016-04-26 04:44:49,615 - run_rally - INFO -
     Preparing input task
     Task  20bc8dfd-1a51-488b-97df-c30ea71319be: started
    Task 20bc8dfd-1a51-488b-97df-c30ea71319be: finished

    test scenario KeystoneBasic.create_tenant_with_users
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_tenant | 0.27      | 0.29         | 0.299        | 0.303        | 0.308     | 0.289     | 100.0%  | 10    |
    | keystone.create_users  | 1.059     | 1.132        | 1.206        | 1.212        | 1.218     | 1.138     | 100.0%  | 10    |
    | total                  | 1.348     | 1.431        | 1.504        | 1.507        | 1.51      | 1.427     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 4.29734396935
    Full duration: 16.6833910942

    test scenario KeystoneBasic.create_add_and_list_user_roles
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_role | 0.241     | 0.277        | 0.302        | 0.303        | 0.303     | 0.275     | 100.0%  | 10    |
    | keystone.add_role    | 0.16      | 0.176        | 0.19         | 0.193        | 0.196     | 0.177     | 100.0%  | 10    |
    | keystone.list_roles  | 0.085     | 0.095        | 0.1          | 0.104        | 0.108     | 0.095     | 100.0%  | 10    |
    | total                | 0.501     | 0.55         | 0.583        | 0.589        | 0.595     | 0.547     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.68035697937
    Full duration: 10.5181751251

    test scenario KeystoneBasic.add_and_remove_user_role
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_role | 0.267     | 0.289        | 0.32         | 0.322        | 0.324     | 0.294     | 100.0%  | 10    |
    | keystone.add_role    | 0.148     | 0.172        | 0.194        | 0.195        | 0.196     | 0.172     | 100.0%  | 10    |
    | keystone.remove_role | 0.093     | 0.132        | 0.166        | 0.168        | 0.169     | 0.133     | 100.0%  | 10    |
    | total                | 0.527     | 0.616        | 0.63         | 0.638        | 0.646     | 0.599     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.79448008537
    Full duration: 10.6772811413

    test scenario KeystoneBasic.create_update_and_delete_tenant
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_tenant | 0.277     | 0.31         | 0.398        | 0.421        | 0.443     | 0.33      | 100.0%  | 10    |
    | keystone.update_tenant | 0.083     | 0.097        | 0.116        | 0.117        | 0.118     | 0.1       | 100.0%  | 10    |
    | keystone.delete_tenant | 0.198     | 0.236        | 0.247        | 0.249        | 0.251     | 0.232     | 100.0%  | 10    |
    | total                  | 0.598     | 0.643        | 0.731        | 0.761        | 0.791     | 0.662     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.00753998756
    Full duration: 9.88667607307

    test scenario KeystoneBasic.create_and_delete_service
    +----------------------------------------------------------------------------------------------------------------------------+
    |                                                    Response Times (sec)                                                    |
    +-------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                  | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_service | 0.276     | 0.302        | 0.313        | 0.344        | 0.374     | 0.305     | 100.0%  | 10    |
    | keystone.delete_service | 0.092     | 0.105        | 0.118        | 0.118        | 0.119     | 0.106     | 100.0%  | 10    |
    | total                   | 0.369     | 0.41         | 0.421        | 0.444        | 0.467     | 0.411     | 100.0%  | 10    |
    +-------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.31590604782
    Full duration: 9.7633960247

    test scenario KeystoneBasic.create_tenant
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_tenant | 0.283     | 0.314        | 0.348        | 0.359        | 0.371     | 0.32      | 100.0%  | 10    |
    | total                  | 0.283     | 0.315        | 0.348        | 0.36         | 0.371     | 0.32      | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 0.971438169479
    Full duration: 6.68577694893

    test scenario KeystoneBasic.create_user
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_user | 0.308     | 0.325        | 0.341        | 0.345        | 0.349     | 0.326     | 100.0%  | 10    |
    | total                | 0.308     | 0.326        | 0.341        | 0.345        | 0.349     | 0.326     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.01120591164
    Full duration: 6.84676504135

    test scenario KeystoneBasic.create_and_list_tenants
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_tenant | 0.26      | 0.276        | 0.295        | 0.297        | 0.3       | 0.277     | 100.0%  | 10    |
    | keystone.list_tenants  | 0.071     | 0.082        | 0.09         | 0.094        | 0.098     | 0.083     | 100.0%  | 10    |
    | total                  | 0.333     | 0.361        | 0.378        | 0.38         | 0.383     | 0.36      | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.12287592888
    Full duration: 9.86326503754

    test scenario KeystoneBasic.create_and_delete_role
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_role | 0.285     | 0.323        | 0.381        | 0.382        | 0.382     | 0.33      | 100.0%  | 10    |
    | keystone.delete_role | 0.167     | 0.191        | 0.225        | 0.226        | 0.228     | 0.194     | 100.0%  | 10    |
    | total                | 0.47      | 0.513        | 0.582        | 0.595        | 0.609     | 0.524     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.57796812057
    Full duration: 9.51138591766

    test scenario KeystoneBasic.get_entities
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_tenant | 0.282     | 0.31         | 0.334        | 0.364        | 0.395     | 0.315     | 100.0%  | 10    |
    | keystone.create_user   | 0.1       | 0.104        | 0.122        | 0.122        | 0.123     | 0.108     | 100.0%  | 10    |
    | keystone.create_role   | 0.079     | 0.092        | 0.102        | 0.107        | 0.112     | 0.094     | 100.0%  | 10    |
    | keystone.get_tenant    | 0.072     | 0.08         | 0.087        | 0.089        | 0.092     | 0.081     | 100.0%  | 10    |
    | keystone.get_user      | 0.087     | 0.091        | 0.114        | 0.139        | 0.163     | 0.099     | 100.0%  | 10    |
    | keystone.get_role      | 0.07      | 0.078        | 0.085        | 0.086        | 0.088     | 0.078     | 100.0%  | 10    |
    | keystone.service_list  | 0.079     | 0.086        | 0.103        | 0.124        | 0.145     | 0.093     | 100.0%  | 10    |
    | keystone.get_service   | 0.069     | 0.086        | 0.093        | 0.096        | 0.098     | 0.084     | 100.0%  | 10    |
    | total                  | 0.889     | 0.939        | 1.023        | 1.035        | 1.048     | 0.952     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.919891119
    Full duration: 15.3317778111

    test scenario KeystoneBasic.create_and_list_users
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | keystone.create_user | 0.287     | 0.314        | 0.336        | 0.345        | 0.354     | 0.316     | 100.0%  | 10    |
    | keystone.list_users  | 0.072     | 0.081        | 0.096        | 0.097        | 0.097     | 0.083     | 100.0%  | 10    |
    | total                | 0.365     | 0.393        | 0.424        | 0.431        | 0.437     | 0.399     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.23520803452
    Full duration: 7.35707998276

    2016-04-26 04:44:50,952 - run_rally - INFO - Test scenario: "keystone" OK.

    2016-04-26 04:44:51,319 - run_rally - INFO - Starting test scenario "neutron" ...
    2016-04-26 04:51:16,265 - run_rally - INFO -
     Preparing input task
     Task  256bf66d-8312-4077-869b-394a1574c2e3: started
    Task 256bf66d-8312-4077-869b-394a1574c2e3: finished

    test scenario NeutronNetworks.create_and_delete_ports
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_port | 0.607     | 0.653        | 0.721        | 0.75         | 0.78      | 0.666     | 100.0%  | 10    |
    | neutron.delete_port | 0.175     | 0.407        | 0.455        | 0.462        | 0.469     | 0.37      | 100.0%  | 10    |
    | total               | 0.814     | 1.09         | 1.137        | 1.137        | 1.137     | 1.036     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 3.12694001198
    Full duration: 32.3510808945

    test scenario NeutronNetworks.create_and_list_routers
    +---------------------------------------------------------------------------------------------------------------------------------+
    |                                                      Response Times (sec)                                                       |
    +------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                       | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_subnet        | 0.578     | 0.606        | 0.635        | 0.643        | 0.65      | 0.609     | 100.0%  | 10    |
    | neutron.create_router        | 0.06      | 0.256        | 0.307        | 0.341        | 0.376     | 0.237     | 100.0%  | 10    |
    | neutron.add_interface_router | 0.244     | 0.508        | 0.566        | 0.589        | 0.612     | 0.476     | 100.0%  | 10    |
    | neutron.list_routers         | 0.04      | 0.238        | 0.271        | 0.275        | 0.278     | 0.194     | 100.0%  | 10    |
    | total                        | 1.169     | 1.517        | 1.722        | 1.742        | 1.762     | 1.517     | 100.0%  | 10    |
    +------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 4.54089903831
    Full duration: 35.4128360748

    test scenario NeutronNetworks.create_and_update_networks
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_network | 0.523     | 0.561        | 0.635        | 0.642        | 0.648     | 0.573     | 100.0%  | 10    |
    | neutron.update_network | 0.106     | 0.337        | 0.376        | 0.391        | 0.406     | 0.303     | 100.0%  | 10    |
    | total                  | 0.691     | 0.877        | 1.006        | 1.007        | 1.008     | 0.876     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.54131317139
    Full duration: 19.3984429836

    test scenario NeutronNetworks.create_and_list_ports
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_port | 0.581     | 0.643        | 0.971        | 1.006        | 1.042     | 0.712     | 100.0%  | 10    |
    | neutron.list_ports  | 0.102     | 0.365        | 0.455        | 0.469        | 0.483     | 0.307     | 100.0%  | 10    |
    | total               | 0.725     | 1.086        | 1.149        | 1.292        | 1.435     | 1.019     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.83818507195
    Full duration: 32.8225178719

    test scenario NeutronNetworks.create_and_delete_subnets
    +--------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                   |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_subnet | 0.571     | 0.62         | 0.673        | 0.682        | 0.69      | 0.626     | 100.0%  | 10    |
    | neutron.delete_subnet | 0.136     | 0.358        | 0.5          | 0.571        | 0.642     | 0.333     | 100.0%  | 10    |
    | total                 | 0.724     | 0.978        | 1.14         | 1.183        | 1.227     | 0.959     | 100.0%  | 10    |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 3.04690408707
    Full duration: 31.1584250927

    test scenario NeutronNetworks.create_and_update_subnets
    +--------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                   |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_subnet | 0.579     | 0.74         | 0.789        | 0.831        | 0.873     | 0.728     | 100.0%  | 10    |
    | neutron.update_subnet | 0.166     | 0.4          | 0.491        | 0.516        | 0.541     | 0.378     | 100.0%  | 10    |
    | total                 | 0.789     | 1.155        | 1.275        | 1.279        | 1.283     | 1.106     | 100.0%  | 10    |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 3.20878195763
    Full duration: 31.9853599072

    test scenario NeutronNetworks.create_and_list_networks
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_network | 0.524     | 0.589        | 0.694        | 0.736        | 0.779     | 0.613     | 100.0%  | 10    |
    | neutron.list_networks  | 0.046     | 0.171        | 0.409        | 0.461        | 0.513     | 0.211     | 100.0%  | 10    |
    | total                  | 0.58      | 0.747        | 1.083        | 1.09         | 1.096     | 0.824     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.37781405449
    Full duration: 19.9551098347

    test scenario NeutronNetworks.create_and_update_routers
    +---------------------------------------------------------------------------------------------------------------------------------+
    |                                                      Response Times (sec)                                                       |
    +------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                       | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_subnet        | 0.592     | 0.623        | 0.664        | 0.665        | 0.667     | 0.628     | 100.0%  | 10    |
    | neutron.create_router        | 0.269     | 0.279        | 0.31         | 0.32         | 0.329     | 0.287     | 100.0%  | 10    |
    | neutron.add_interface_router | 0.28      | 0.484        | 0.653        | 0.671        | 0.688     | 0.477     | 100.0%  | 10    |
    | neutron.update_router        | 0.156     | 0.389        | 0.45         | 0.456        | 0.462     | 0.361     | 100.0%  | 10    |
    | total                        | 1.388     | 1.739        | 1.953        | 1.981        | 2.009     | 1.754     | 100.0%  | 10    |
    +------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 5.26099705696
    Full duration: 37.1857252121

    test scenario NeutronNetworks.create_and_delete_routers
    +------------------------------------------------------------------------------------------------------------------------------------+
    |                                                        Response Times (sec)                                                        |
    +---------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                          | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_subnet           | 0.558     | 0.624        | 0.707        | 0.736        | 0.765     | 0.637     | 100.0%  | 10    |
    | neutron.create_router           | 0.044     | 0.288        | 0.341        | 0.362        | 0.383     | 0.253     | 100.0%  | 10    |
    | neutron.add_interface_router    | 0.299     | 0.527        | 0.563        | 0.573        | 0.583     | 0.502     | 100.0%  | 10    |
    | neutron.remove_interface_router | 0.241     | 0.46         | 0.559        | 0.56         | 0.561     | 0.444     | 100.0%  | 10    |
    | neutron.delete_router           | 0.15      | 0.392        | 0.469        | 0.487        | 0.505     | 0.343     | 100.0%  | 10    |
    | total                           | 1.845     | 2.118        | 2.453        | 2.507        | 2.56      | 2.179     | 100.0%  | 10    |
    +---------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 6.46906304359
    Full duration: 37.6224770546

    test scenario NeutronNetworks.create_and_update_ports
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_port | 0.605     | 0.665        | 0.825        | 0.85         | 0.876     | 0.691     | 100.0%  | 10    |
    | neutron.update_port | 0.126     | 0.359        | 0.409        | 0.423        | 0.437     | 0.325     | 100.0%  | 10    |
    | total               | 0.731     | 1.054        | 1.179        | 1.192        | 1.205     | 1.017     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 3.16282176971
    Full duration: 34.5440177917

    test scenario NeutronNetworks.create_and_list_subnets
    +--------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                   |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_subnet | 0.578     | 0.613        | 0.667        | 0.678        | 0.689     | 0.622     | 100.0%  | 10    |
    | neutron.list_subnets  | 0.23      | 0.266        | 0.336        | 0.34         | 0.344     | 0.276     | 100.0%  | 10    |
    | total                 | 0.835     | 0.9          | 0.963        | 0.966        | 0.969     | 0.898     | 100.0%  | 10    |
    +-----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.74195313454
    Full duration: 32.8288888931

    test scenario NeutronNetworks.create_and_delete_networks
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | neutron.create_network | 0.525     | 0.612        | 0.729        | 0.735        | 0.74      | 0.626     | 100.0%  | 10    |
    | neutron.delete_network | 0.133     | 0.375        | 0.446        | 0.474        | 0.501     | 0.35      | 100.0%  | 10    |
    | total                  | 0.739     | 1.004        | 1.113        | 1.177        | 1.242     | 0.976     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.94529485703
    Full duration: 19.0619311333

    2016-04-26 04:51:17,592 - run_rally - INFO - Test scenario: "neutron" OK.

    2016-04-26 04:51:18,073 - run_rally - INFO - Starting test scenario "nova" ...
    2016-04-26 07:03:18,875 - run_rally - INFO -
     Preparing input task
     Task  a238f5f4-fd3d-4015-95c9-2b0ba5d314b6: started
    Task a238f5f4-fd3d-4015-95c9-2b0ba5d314b6: finished

    test scenario NovaKeypair.create_and_delete_keypair
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.create_keypair | 0.579     | 0.646        | 0.774        | 0.918        | 1.062     | 0.695     | 100.0%  | 10    |
    | nova.delete_keypair | 0.023     | 0.027        | 0.048        | 0.051        | 0.054     | 0.033     | 100.0%  | 10    |
    | total               | 0.627     | 0.687        | 0.8          | 0.943        | 1.085     | 0.728     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.11327505112
    Full duration: 24.7004601955

    test scenario NovaServers.snapshot_server
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server       | 9.939     | 11.728       | 13.031       | 13.319       | 13.606    | 11.722    | 100.0%  | 10    |
    | nova.create_image      | 9.473     | 9.734        | 10.003       | 10.052       | 10.1      | 9.728     | 100.0%  | 10    |
    | nova.delete_server     | 2.63      | 2.927        | 3.279        | 3.899        | 4.52      | 3.033     | 100.0%  | 10    |
    | nova.boot_server (2)   | 9.986     | 10.959       | 11.567       | 11.737       | 11.907    | 10.921    | 100.0%  | 10    |
    | nova.delete_server (2) | 2.41      | 2.772        | 2.958        | 2.963        | 2.968     | 2.712     | 100.0%  | 10    |
    | nova.delete_image      | 1.467     | 2.001        | 2.188        | 2.332        | 2.477     | 1.95      | 100.0%  | 10    |
    | total                  | 37.87     | 39.802       | 41.419       | 42.304       | 43.189    | 40.067    | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 120.693696976
    Full duration: 164.095020056

    test scenario NovaKeypair.boot_and_delete_server_with_keypair
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.create_keypair | 0.515     | 0.637        | 0.702        | 0.714        | 0.726     | 0.631     | 100.0%  | 10    |
    | nova.boot_server    | 10.03     | 11.695       | 12.539       | 12.808       | 13.076    | 11.597    | 100.0%  | 10    |
    | nova.delete_server  | 2.581     | 2.755        | 2.899        | 3.003        | 3.108     | 2.769     | 100.0%  | 10    |
    | nova.delete_keypair | 0.026     | 0.036        | 0.044        | 0.044        | 0.045     | 0.036     | 100.0%  | 10    |
    | total               | 13.194    | 15.135       | 15.888       | 16.111       | 16.334    | 15.033    | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 43.7031610012
    Full duration: 84.4934301376

    test scenario NovaKeypair.create_and_list_keypairs
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.create_keypair | 0.613     | 0.68         | 0.8          | 0.83         | 0.859     | 0.701     | 100.0%  | 10    |
    | nova.list_keypairs  | 0.017     | 0.029        | 0.055        | 0.132        | 0.209     | 0.045     | 100.0%  | 10    |
    | total               | 0.631     | 0.715        | 0.893        | 0.919        | 0.945     | 0.746     | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.10457396507
    Full duration: 25.5227000713

    test scenario NovaServers.list_servers
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.list_servers | 0.963     | 1.205        | 1.239        | 1.272        | 1.304     | 1.187     | 100.0%  | 10    |
    | total             | 0.963     | 1.205        | 1.239        | 1.272        | 1.305     | 1.187     | 100.0%  | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 3.61515402794
    Full duration: 89.3156220913

    test scenario NovaServers.resize_server
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server    | 11.077    | 11.648       | 13.586       | 13.788       | 13.99     | 12.144    | 100.0%  | 10    |
    | nova.resize         | 97.438    | 98.364       | 99.784       | 101.736      | 103.687   | 98.895    | 100.0%  | 10    |
    | nova.resize_confirm | 2.462     | 2.85         | 3.013        | 3.032        | 3.052     | 2.81      | 100.0%  | 10    |
    | nova.delete_server  | 2.362     | 2.635        | 2.717        | 2.759        | 2.802     | 2.576     | 100.0%  | 10    |
    | total               | 114.396   | 116.205      | 117.751      | 119.281      | 120.811   | 116.425   | 100.0%  | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 352.596132994
    Full duration: 373.961167812

    test scenario NovaServers.boot_server_from_volume_and_delete
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 9.652     | 10.151       | 10.573       | 10.621       | 10.669    | 10.165    | 100.0%  | 10    |
    | nova.boot_server     | 10.713    | 13.21        | 14.394       | 14.695       | 14.996    | 13.013    | 100.0%  | 10    |
    | nova.delete_server   | 4.701     | 4.969        | 5.039        | 5.159        | 5.279     | 4.942     | 100.0%  | 10    |
    | total                | 25.26     | 27.982       | 30.104       | 30.137       | 30.17     | 28.121    | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 83.7665529251
    Full duration: 133.76401782

    test scenario NovaServers.boot_and_migrate_server
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server    | 9.342     | 11.196       | 12.987       | 13.225       | 13.463    | 11.305    | 80.0%   | 10    |
    | nova.stop_server    | 61.257    | 62.345       | 63.163       | 63.249       | 63.336    | 62.301    | 80.0%   | 10    |
    | nova.migrate        | 8.224     | 9.522        | 11.336       | 11.478       | 11.62     | 9.663     | 80.0%   | 10    |
    | nova.resize_confirm | 2.413     | 2.724        | 3.003        | 3.108        | 3.213     | 2.704     | 100.0%  | 8     |
    | nova.delete_server  | 2.397     | 2.418        | 2.638        | 2.652        | 2.666     | 2.495     | 100.0%  | 8     |
    | total               | 85.3      | 88.008       | 91.856       | 92.68        | 93.504    | 88.469    | 80.0%   | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 282.145553112
    Full duration: 310.275305033

    test scenario NovaServers.boot_and_delete_server
    +-----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                  |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action             | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server   | 10.164    | 10.763       | 21.145       | 31.824       | 42.503    | 14.815    | 80.0%   | 10    |
    | nova.delete_server | 2.439     | 2.701        | 2.959        | 2.97         | 2.982     | 2.728     | 88.9%   | 9     |
    | total              | 12.997    | 13.446       | 23.964       | 34.453       | 44.942    | 17.544    | 80.0%   | 10    |
    +--------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 352.537348986
    Full duration: 997.781033993

    test scenario NovaServers.boot_and_rebuild_server
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server    | 10.618    | 11.665       | 12.726       | 12.764       | 12.802    | 11.718    | 70.0%   | 10    |
    | nova.rebuild_server | 69.264    | 71.18        | 72.314       | 72.575       | 72.836    | 71.097    | 100.0%  | 7     |
    | nova.delete_server  | 2.391     | 2.632        | 2.88         | 2.883        | 2.886     | 2.639     | 100.0%  | 7     |
    | total               | 83.337    | 85.019       | 87.645       | 87.923       | 88.201    | 85.454    | 70.0%   | 10    |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 477.006741047
    Full duration: 1121.04293394

    test scenario NovaSecGroup.create_and_list_secgroups
    +-----------------------------------------------------------------------------------------------------------------------------------+
    |                                                       Response Times (sec)                                                        |
    +--------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                         | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.create_10_security_groups | 3.03      | 3.488        | 3.933        | 3.989        | 4.044     | 3.487     | 100.0%  | 10    |
    | nova.create_100_rules          | 22.925    | 23.261       | 23.92        | 24.188       | 24.456    | 23.425    | 100.0%  | 10    |
    | nova.list_security_groups      | 0.126     | 0.16         | 0.213        | 0.294        | 0.376     | 0.18      | 100.0%  | 10    |
    | total                          | 26.54     | 26.984       | 27.591       | 27.704       | 27.817    | 27.092    | 100.0%  | 10    |
    +--------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 81.6362090111
    Full duration: 118.557869911

    test scenario NovaSecGroup.create_and_delete_secgroups
    +-----------------------------------------------------------------------------------------------------------------------------------+
    |                                                       Response Times (sec)                                                        |
    +--------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                         | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +--------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.create_10_security_groups | 2.934     | 3.533        | 3.804        | 3.912        | 4.021     | 3.522     | 100.0%  | 10    |
    | nova.create_100_rules          | 22.89     | 23.403       | 23.74        | 23.847       | 23.953    | 23.394    | 100.0%  | 10    |
    | nova.delete_10_security_groups | 1.219     | 1.282        | 1.629        | 1.634        | 1.64      | 1.372     | 100.0%  | 10    |
    | total                          | 27.6      | 28.387       | 28.547       | 28.634       | 28.722    | 28.288    | 100.0%  | 10    |
    +--------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 85.2456521988
    Full duration: 109.930608988

    test scenario NovaServers.boot_and_bounce_server
    +----------------------------------------------------------------------------------------------------------------------------+
    |                                                    Response Times (sec)                                                    |
    +-------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                  | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server        | 10.584    | 11.76        | 12.966       | 13.02        | 13.073    | 11.794    | 57.1%   | 7     |
    | nova.reboot_server      | 4.802     | 5.11         | 5.257        | 5.278        | 5.299     | 5.08      | 100.0%  | 4     |
    | nova.soft_reboot_server | 123.97    | 124.161      | 125.321      | 125.531      | 125.741   | 124.508   | 100.0%  | 4     |
    | nova.stop_server        | 61.413    | 62.307       | 63.351       | 63.532       | 63.713    | 62.435    | 100.0%  | 4     |
    | nova.start_server       | 2.747     | 2.775        | 2.996        | 3.039        | 3.082     | 2.845     | 100.0%  | 4     |
    | nova.rescue_server      | 64.447    | 66.021       | 66.521       | 66.564       | 66.607    | 65.774    | 100.0%  | 4     |
    | nova.unrescue_server    | 2.368     | 4.579        | 4.599        | 4.6          | 4.601     | 4.032     | 100.0%  | 4     |
    | nova.delete_server      | 2.398     | 2.511        | 2.663        | 2.679        | 2.694     | 2.528     | 100.0%  | 4     |
    | total                   | 274.414   | 278.786      | 282.788      | 283.426      | 284.064   | 279.013   | 57.1%   | 7     |
    +-------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 584.260617018
    Full duration: 1223.11469412

    test scenario NovaServers.boot_server
    +---------------------------------------------------------------------------------------------------------------------+
    |                                                Response Times (sec)                                                 |
    +------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action           | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server | 11.343    | 11.648       | 12.248       | 12.342       | 12.435    | 11.804    | 55.6%   | 9     |
    | total            | 11.344    | 11.648       | 12.249       | 12.342       | 12.435    | 11.804    | 55.6%   | 9     |
    +------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 339.613210917
    Full duration: 959.207664013

    test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
    +--------------------------------------------------------------------------------------------------------------------------------------+
    |                                                         Response Times (sec)                                                         |
    +-----------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-----------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.create_10_security_groups    | 2.471     | 2.641        | 2.886        | 2.916        | 2.947     | 2.686     | 37.5%   | 8     |
    | nova.create_100_rules             | 20.403    | 20.759       | 21.005       | 21.036       | 21.067    | 20.743    | 37.5%   | 8     |
    | nova.boot_server                  | 8.329     | 10.397       | 10.543       | 10.561       | 10.58     | 9.768     | 37.5%   | 8     |
    | nova.get_attached_security_groups | 0.177     | 0.18         | 0.189        | 0.19         | 0.191     | 0.183     | 100.0%  | 3     |
    | nova.delete_server                | 2.417     | 2.424        | 2.563        | 2.58         | 2.597     | 2.48      | 100.0%  | 3     |
    | nova.delete_10_security_groups    | 1.146     | 1.185        | 1.295        | 1.309        | 1.323     | 1.218     | 100.0%  | 3     |
    | total                             | 35.785    | 37.72        | 37.728       | 37.729       | 37.73     | 37.079    | 37.5%   | 8     |
    +-----------------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 653.787332058
    Full duration: 698.373892784

    test scenario NovaServers.pause_and_unpause_server
    +------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                  |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action              | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server    | 9.228     | 10.626       | 10.698       | 10.707       | 10.715    | 10.19     | 37.5%   | 8     |
    | nova.pause_server   | 2.325     | 2.628        | 2.631        | 2.631        | 2.631     | 2.528     | 100.0%  | 3     |
    | nova.unpause_server | 2.624     | 2.647        | 2.691        | 2.697        | 2.702     | 2.658     | 100.0%  | 3     |
    | nova.delete_server  | 2.596     | 2.732        | 2.747        | 2.749        | 2.751     | 2.693     | 100.0%  | 3     |
    | total               | 16.772    | 18.711       | 18.72        | 18.722       | 18.723    | 18.069    | 37.5%   | 8     |
    +---------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 607.316802025
    Full duration: 645.979089022

    test scenario NovaServers.boot_server_from_volume
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | cinder.create_volume | 8.57      | 9.398        | 10.796       | 10.932       | 11.068    | 9.692     | 60.0%   | 10    |
    | nova.boot_server     | 11.064    | 12.084       | 12.627       | 12.859       | 13.092    | 12.061    | 60.0%   | 10    |
    | total                | 20.261    | 21.884       | 22.881       | 22.979       | 23.078    | 21.754    | 60.0%   | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 377.391654015
    Full duration: 411.411114931

    test scenario NovaServers.boot_and_list_server
    +----------------------------------------------------------------------------------------------------------------------+
    |                                                 Response Times (sec)                                                 |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action            | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | nova.boot_server  | 9.689     | 10.784       | 12.049       | 12.245       | 12.44     | 10.872    | 60.0%   | 10    |
    | nova.list_servers | 0.2       | 0.431        | 0.5          | 0.513        | 0.526     | 0.414     | 100.0%  | 6     |
    | total             | 10.11     | 11.216       | 12.386       | 12.649       | 12.913    | 11.286    | 60.0%   | 10    |
    +-------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 339.637984037
    Full duration: 382.637588978

    2016-04-26 07:03:20,320 - run_rally - INFO - Test scenario: "nova" Failed.
    2016-04-26 07:03:20,864 - run_rally - INFO - Starting test scenario "quotas" ...
    2016-04-26 07:04:24,690 - run_rally - INFO -
     Preparing input task
     Task  31d451cc-0c33-44e6-8ce1-a226ec4d3747: started
    Task 31d451cc-0c33-44e6-8ce1-a226ec4d3747: finished

    test scenario Quotas.cinder_update
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | quotas.update_quotas | 0.676     | 0.77         | 1.004        | 1.007        | 1.01      | 0.823     | 100.0%  | 10    |
    | total                | 0.676     | 0.77         | 1.005        | 1.007        | 1.01      | 0.823     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 2.49713397026
    Full duration: 10.5032558441

    test scenario Quotas.neutron_update
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | quotas.update_quotas | 0.214     | 0.235        | 0.26         | 0.262        | 0.263     | 0.238     | 100.0%  | 10    |
    | total                | 0.372     | 0.415        | 0.426        | 0.427        | 0.428     | 0.408     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.27715206146
    Full duration: 8.95948386192

    test scenario Quotas.cinder_update_and_delete
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | quotas.update_quotas | 0.77      | 0.834        | 0.965        | 0.99         | 1.015     | 0.857     | 100.0%  | 10    |
    | quotas.delete_quotas | 0.345     | 0.54         | 0.562        | 0.581        | 0.6       | 0.505     | 100.0%  | 10    |
    | total                | 1.127     | 1.365        | 1.437        | 1.498        | 1.56      | 1.362     | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 4.07208108902
    Full duration: 12.2027239799

    test scenario Quotas.nova_update_and_delete
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | quotas.update_quotas | 0.448     | 0.48         | 0.54         | 0.679        | 0.819     | 0.511     | 100.0%  | 10    |
    | quotas.delete_quotas | 0.012     | 0.019        | 0.024        | 0.025        | 0.027     | 0.019     | 100.0%  | 10    |
    | total                | 0.463     | 0.499        | 0.563        | 0.699        | 0.836     | 0.53      | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.53432106972
    Full duration: 9.25113201141

    test scenario Quotas.nova_update
    +-------------------------------------------------------------------------------------------------------------------------+
    |                                                  Response Times (sec)                                                   |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action               | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | quotas.update_quotas | 0.395     | 0.469        | 0.541        | 0.549        | 0.557     | 0.47      | 100.0%  | 10    |
    | total                | 0.395     | 0.469        | 0.541        | 0.549        | 0.557     | 0.47      | 100.0%  | 10    |
    +----------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 1.49797797203
    Full duration: 8.86192798615

    2016-04-26 07:04:26,066 - run_rally - INFO - Test scenario: "quotas" OK.
    2016-04-26 07:04:26,381 - run_rally - INFO - Starting test scenario "requests" ...
    2016-04-26 07:04:56,876 - run_rally - INFO -
     Preparing input task
     Task  1c6ea3eb-b807-414a-b07a-d9ecf1aa2344: started
    Task 1c6ea3eb-b807-414a-b07a-d9ecf1aa2344: finished

    test scenario HttpRequests.check_random_request
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | requests.check_request | 0.018     | 0.542        | 5.956        | 8.184        | 10.411    | 2.811     | 100.0%  | 10    |
    | total                  | 0.018     | 0.542        | 5.956        | 8.184        | 10.411    | 2.812     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 10.5026738644
    Full duration: 13.9263000488

    test scenario HttpRequests.check_request
    +---------------------------------------------------------------------------------------------------------------------------+
    |                                                   Response Times (sec)                                                    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | Action                 | Min (sec) | Median (sec) | 90%ile (sec) | 95%ile (sec) | Max (sec) | Avg (sec) | Success | Count |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    | requests.check_request | 0.016     | 0.059        | 5.062        | 5.063        | 5.065     | 2.047     | 100.0%  | 10    |
    | total                  | 0.016     | 0.059        | 5.062        | 5.063        | 5.065     | 2.047     | 100.0%  | 10    |
    +------------------------+-----------+--------------+--------------+--------------+-----------+-----------+---------+-------+
    Load duration: 5.16210699081
    Full duration: 8.87197899818

    2016-04-26 07:04:58,210 - run_rally - INFO - Test scenario: "requests" OK.
    2016-04-26 07:04:58,402 - run_rally - INFO -

                         Rally Summary Report

    +===================+============+===============+===========+
    | Module            | Duration   | nb. Test Run  | Success   |
    +===================+============+===============+===========+
    | authenticate      | 00:50      | 12            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | glance            | 02:55      | 11            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | cinder            | 54:33      | 59            | 76.47%    |
    +-------------------+------------+---------------+-----------+
    | heat              | 18:00      | 48            | 92.31%    |
    +-------------------+------------+---------------+-----------+
    | keystone          | 01:53      | 40            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | neutron           | 06:04      | 43            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | nova              | 11:14      | 79            | 79.87%    |
    +-------------------+------------+---------------+-----------+
    | quotas            | 00:49      | 12            | 100.00%   |
    +-------------------+------------+---------------+-----------+
    | requests          | 00:22      | 4             | 100.00%   |
    +-------------------+------------+---------------+-----------+
    +===================+============+===============+===========+
    | TOTAL:            | 05:36:44   | 308           | 94.29%    |
    +===================+============+===============+===========+

Feature tests
-------------

Promise
^^^^^^^
::

    FUNCTEST.info: Running PROMISE test case...
    2016-04-26 01:23:01,296 - Promise- INFO - Creating tenant 'promise'...
    2016-04-26 01:23:01,461 - Promise- INFO - Adding role 'a6da18e9c7e94ee9975e85b6f26c974a' to tenant 'promise'...
    2016-04-26 01:23:01,553 - Promise- INFO - Creating user 'promiser'...
    2016-04-26 01:23:01,666 - Promise- INFO - Updating OpenStack credentials...
    2016-04-26 01:23:01,687 - Promise- INFO - Creating image 'promise-img' from '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img'...
    2016-04-26 01:23:05,215 - Promise- INFO - Creating flavor 'promise-flavor'...
    2016-04-26 01:23:05,871 - Promise- INFO - Exporting environment variables...
    2016-04-26 01:23:05,871 - Promise- INFO - Running command: npm run -s test -- --reporter json
    2016-04-26 01:23:12,658 - Promise- INFO - The test succeeded.
    2016-04-26 01:23:12,660 - Promise- INFO -
    ****************************************
              Promise test report

    ****************************************
     Suites:  	23
     Tests:   	33
     Passes:  	33
     Pending: 	0
     Failures:	0
     Start:   	2016-04-26T01:23:08.348Z
     End:     	2016-04-26T01:23:12.610Z
     Duration:	4.262
