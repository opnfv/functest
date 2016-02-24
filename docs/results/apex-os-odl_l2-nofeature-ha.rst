.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for apex-os-odl_l2-nofeature-ha
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
  vPing_ssh- INFO - vPing Start Time:'2016-02-23 07:43:00'
  vPing_ssh- INFO - Creating instance 'opnfv-vping-1'...
     name=opnfv-vping-1
     flavor=<Flavor: m1.small>
     image=a0698b8a-e881-4b84-b540-a0324d671c5a
     network=df3509f4-ef3d-4264-9293-9e0688a5c38e
  vPing_ssh- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  vPing_ssh- INFO - Adding 'opnfv-vping-1' to security group 'vPing-sg'...
  vPing_ssh- INFO - Creating instance 'opnfv-vping-2'...
     name=opnfv-vping-2
     flavor=<Flavor: m1.small>
     image=a0698b8a-e881-4b84-b540-a0324d671c5a
     network=df3509f4-ef3d-4264-9293-9e0688a5c38e
  vPing_ssh- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  vPing_ssh- INFO - Adding 'opnfv-vping-2' to security group 'vPing-sg'...
  vPing_ssh- INFO - Creating floating IP for VM 'opnfv-vping-2'...
  vPing_ssh- INFO - Floating IP created: '172.30.9.201'
  vPing_ssh- INFO - Associating floating ip: '172.30.9.201' to VM 'opnfv-vping-2'
  vPing_ssh- INFO - Trying to establish SSH connection to 172.30.9.201...
  vPing_ssh- INFO - Waiting for ping...
  vPing_ssh- INFO - vPing detected!
  vPing_ssh- INFO - vPing duration:'82.0' s.
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
  vPing_userdata- INFO - vPing Start Time:'2016-02-23 07:44:41'
  vPing_userdata- INFO - Creating instance 'opnfv-vping-1'...
     name=opnfv-vping-1
     flavor=<Flavor: m1.small>
     image=78cd8dbf-54fb-43ce-9f19-7801130b5a99
     network=a030c4ca-00ea-4913-bbec-505eaca9f5ff
  vPing_userdata- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  vPing_userdata- INFO - Creating instance 'opnfv-vping-2'...
     name=opnfv-vping-2
     flavor=<Flavor: m1.small>
     image=78cd8dbf-54fb-43ce-9f19-7801130b5a99
     network=a030c4ca-00ea-4913-bbec-505eaca9f5ff
     userdata=
    #!/bin/sh

    while true; do
     ping -c 1 192.168.130.6 2>&1 >/dev/null
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
  vPing_userdata- INFO - vPing duration:'72.7'
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
  | b470a125-b6d9-400e-872e-abe779ff1ab5 | 784b68a9-2eab-4e1e-abc7-a4f68d4d02fe |          | 70    | 8        | 2016-02-23 07:46:13.668289 | finished |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+

  Tests:

  +----------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | name                                                                                                                             | time      | status  |
  +----------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since             | 0.10275   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                      | 0.14924   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                 | 0.05661   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                | 0.32593   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                    | 0.38913   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                      | 0.05691   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                       | 0.09185   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since | 0.04789   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name          | 0.04881   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref    | 0.27540   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status        | 0.10541   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type          | 0.13467   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results           | 0.33891   | success |
  | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete          | 2.13276   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                       | 331.74491 | fail    |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                           | 0.41803   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                               | 0.17025   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                            | 316.35661 | fail    |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                  | 0.00272   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                  | 1.84308   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                             | 10.10318  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                   | 17.23894  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                       | 7.82065   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                 | 7.02428   | success |
  | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                  | 0.0       | fail    |
  | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                          | 0.09527   | success |
  | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                     | 0.16436   | success |
  | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                      | 0.02123   | success |
  | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                      | 0.32681   | success |
  | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                        | 0.74903   | success |
  | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                   | 1.33567   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                 | 0.01368   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                           | 0.01283   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                            | 0.01451   | success |
  | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                             | 0.17814   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                     | 0.69374   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                   | 1.40285   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                     | 2.95154   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                   | 0.85749   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                         | 1.12230   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                         | 1.29858   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                            | 3.11215   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                          | 3.42505   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                 | 3.05471   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                         | 0.15865   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                       | 0.08296   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                        | 0.08528   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                        | 0.02219   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                         | 0.09302   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                     | 0.71309   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                            | 3.81771   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                              | 0.01890   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                         | 1.06254   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                | 2.54527   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                  | 0.26689   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                      | 1.09816   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                  | 0.67413   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                      | 0.56914   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                      | 0.37443   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change            | 0.74292   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change          | 0.43472   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                         | 0.0       | fail    |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                             | 0.0       | fail    |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications        | 303.15352 | fail    |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications        | 301.75020 | fail    |
  | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                               | 2.79412   | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                        | 9.60493   | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                             | 11.53698  | success |
  | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                      | 0.40696   | success |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                         | 383.53375 | fail    |
  +----------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  run_tempest - INFO - Results: {'timestart': '2016-02-2307:46:13.668289', 'duration': 695, 'tests': 70, 'failures': 8}
  run_tempest - INFO - Pushing results to DB: 'http://testresults.opnfv.org/testapi/results'.
  run_tempest - INFO - Deleting tenant and user for Tempest suite)


Rally
^^^^^
::

  FUNCTEST.info: Running Rally benchmark suite...
  run_rally - INFO - Starting test scenario "authenticate" ...

  Preparing input task
  Task  7ac7e940-ea41-4f7d-9cca-facd241c0d42: started
  Task 7ac7e940-ea41-4f7d-9cca-facd241c0d42: finished

  test scenario Authenticate.validate_glance
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_glance     | 0.14  | 0.147  | 0.19   | 0.23   | 0.27  | 0.164 | 100.0%  | 10    |
  | authenticate.validate_glance (2) | 0.027 | 0.085  | 0.091  | 0.097  | 0.103 | 0.081 | 100.0%  | 10    |
  | total                            | 0.24  | 0.324  | 0.449  | 0.497  | 0.544 | 0.354 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.991291999817
  Full duration: 3.52114295959

  test scenario Authenticate.keystone
  +-----------------------------------------------------------------------------+
  |                            Response Times (sec)                             |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | total  | 0.062 | 0.071  | 0.092  | 0.093  | 0.093 | 0.075 | 100.0%  | 10    |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.256750106812
  Full duration: 3.22034788132

  test scenario Authenticate.validate_heat
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_heat     | 0.079 | 0.083  | 0.086  | 0.089  | 0.091 | 0.083 | 100.0%  | 10    |
  | authenticate.validate_heat (2) | 0.073 | 0.083  | 0.088  | 0.088  | 0.088 | 0.082 | 100.0%  | 10    |
  | total                          | 0.219 | 0.235  | 0.273  | 0.281  | 0.289 | 0.247 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.758399963379
  Full duration: 3.36240792274

  test scenario Authenticate.validate_nova
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_nova     | 0.08  | 0.095  | 0.164  | 0.194  | 0.225 | 0.116 | 100.0%  | 10    |
  | authenticate.validate_nova (2) | 0.018 | 0.024  | 0.032  | 0.035  | 0.037 | 0.025 | 100.0%  | 10    |
  | total                          | 0.172 | 0.198  | 0.261  | 0.297  | 0.333 | 0.221 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.659279108047
  Full duration: 3.35535907745

  test scenario Authenticate.validate_cinder
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_cinder     | 0.073 | 0.079  | 0.092  | 0.094  | 0.097 | 0.082 | 100.0%  | 10    |
  | authenticate.validate_cinder (2) | 0.013 | 0.082  | 0.149  | 0.265  | 0.381 | 0.106 | 100.0%  | 10    |
  | total                            | 0.152 | 0.241  | 0.344  | 0.464  | 0.585 | 0.272 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.793002128601
  Full duration: 3.46288895607

  test scenario Authenticate.validate_neutron
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_neutron     | 0.082 | 0.095  | 0.115  | 0.137  | 0.159 | 0.1   | 100.0%  | 10    |
  | authenticate.validate_neutron (2) | 0.018 | 0.089  | 0.103  | 0.104  | 0.105 | 0.072 | 100.0%  | 10    |
  | total                             | 0.177 | 0.243  | 0.29   | 0.321  | 0.353 | 0.247 | 100.0%  | 10    |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.788791894913
  Full duration: 3.39974403381

  run_rally - INFO - Test scenario: "authenticate" OK.
  run_rally - INFO - Starting test scenario "glance" ...

  Preparing input task
  Task  56b5e198-2c90-4440-a9bf-b098659c5783: started
  Task 56b5e198-2c90-4440-a9bf-b098659c5783: finished

  test scenario GlanceImages.list_images
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.list_images | 0.226 | 0.256  | 0.328  | 0.335  | 0.343 | 0.268 | 100.0%  | 10    |
  | total              | 0.226 | 0.256  | 0.328  | 0.336  | 0.343 | 0.268 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.82669711113
  Full duration: 4.65047502518

  test scenario GlanceImages.create_image_and_boot_instances
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | glance.create_image | 3.917 | 4.559  | 4.731  | 4.819  | 4.906  | 4.469  | 100.0%  | 10    |
  | nova.boot_servers   | 5.082 | 8.269  | 10.835 | 11.119 | 11.402 | 8.596  | 100.0%  | 10    |
  | total               | 9.684 | 12.929 | 15.683 | 15.704 | 15.725 | 13.065 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 38.0555651188
  Full duration: 65.7321281433

  test scenario GlanceImages.create_and_list_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 3.631 | 4.223  | 4.681  | 4.717  | 4.753 | 4.26  | 100.0%  | 10    |
  | glance.list_images  | 0.03  | 0.1    | 0.11   | 0.132  | 0.153 | 0.085 | 100.0%  | 10    |
  | total               | 3.731 | 4.287  | 4.781  | 4.817  | 4.854 | 4.345 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 13.4343621731
  Full duration: 20.5471830368

  test scenario GlanceImages.create_and_delete_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 3.679 | 4.522  | 4.775  | 4.781  | 4.786 | 4.475 | 100.0%  | 10    |
  | glance.delete_image | 0.68  | 1.416  | 1.924  | 1.945  | 1.966 | 1.355 | 100.0%  | 10    |
  | total               | 4.359 | 5.895  | 6.659  | 6.682  | 6.706 | 5.83  | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 17.0444431305
  Full duration: 21.4709100723

  run_rally - INFO - Test scenario: "glance" OK.
  run_rally - INFO - Starting test scenario "cinder" ...

  Preparing input task
  Task  30bb498c-6dda-4d30-bf2d-cf3979a83615: started
  Task 30bb498c-6dda-4d30-bf2d-cf3979a83615: finished

  test scenario CinderVolumes.create_and_attach_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server     | 3.361  | 5.067  | 5.688  | 5.748  | 5.808  | 4.948  | 100.0%  | 10    |
  | cinder.create_volume | 2.56   | 2.856  | 3.04   | 3.098  | 3.156  | 2.872  | 100.0%  | 10    |
  | nova.attach_volume   | 3.018  | 3.376  | 4.145  | 5.024  | 5.903  | 3.65   | 100.0%  | 10    |
  | nova.detach_volume   | 2.643  | 2.895  | 3.093  | 3.156  | 3.219  | 2.912  | 100.0%  | 10    |
  | cinder.delete_volume | 0.517  | 2.429  | 2.538  | 2.676  | 2.814  | 2.268  | 100.0%  | 10    |
  | nova.delete_server   | 2.329  | 2.456  | 2.645  | 2.656  | 2.667  | 2.468  | 100.0%  | 10    |
  | total                | 17.686 | 19.384 | 20.284 | 20.286 | 20.288 | 19.117 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 56.4022140503
  Full duration: 68.9135789871

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 5.146 | 5.432  | 5.632  | 5.652  | 5.673 | 5.415 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.034 | 0.115  | 0.135  | 0.135  | 0.135 | 0.096 | 100.0%  | 10    |
  | total                | 5.18  | 5.507  | 5.747  | 5.772  | 5.797 | 5.511 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.3556389809
  Full duration: 27.6093170643

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.773 | 2.959  | 3.11   | 3.137  | 3.165 | 2.955 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.028 | 0.127  | 0.202  | 0.219  | 0.237 | 0.111 | 100.0%  | 10    |
  | total                | 2.812 | 3.033  | 3.293  | 3.298  | 3.302 | 3.066 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.06200098991
  Full duration: 19.9587731361

  test scenario CinderVolumes.create_and_list_snapshots
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.482 | 4.642  | 4.889  | 4.91   | 4.931 | 4.296 | 100.0%  | 10    |
  | cinder.list_snapshots  | 0.013 | 0.096  | 0.107  | 0.134  | 0.162 | 0.079 | 100.0%  | 10    |
  | total                  | 2.583 | 4.772  | 4.95   | 4.967  | 4.984 | 4.375 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 12.2352650166
  Full duration: 44.3921279907

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.707 | 2.813  | 2.903  | 2.956  | 3.009 | 2.825 | 100.0%  | 10    |
  | cinder.delete_volume | 2.407 | 2.548  | 2.613  | 2.626  | 2.638 | 2.55  | 100.0%  | 10    |
  | total                | 5.191 | 5.377  | 5.507  | 5.532  | 5.558 | 5.375 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.1588079929
  Full duration: 22.6795511246

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 5.089 | 5.255  | 5.753  | 6.601  | 7.449 | 5.494 | 100.0%  | 10    |
  | cinder.delete_volume | 2.343 | 2.456  | 2.615  | 2.688  | 2.761 | 2.496 | 100.0%  | 10    |
  | total                | 7.471 | 7.795  | 8.253  | 9.073  | 9.893 | 7.991 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 23.303401947
  Full duration: 30.3196620941

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.724 | 2.844  | 2.939  | 2.963  | 2.986 | 2.856 | 100.0%  | 10    |
  | cinder.delete_volume | 2.353 | 2.519  | 2.659  | 2.718  | 2.778 | 2.525 | 100.0%  | 10    |
  | total                | 5.147 | 5.393  | 5.45   | 5.541  | 5.633 | 5.381 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.1724491119
  Full duration: 22.9236290455

  test scenario CinderVolumes.create_and_upload_volume_to_image
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume          | 2.726  | 2.886  | 3.014  | 3.047  | 3.08   | 2.888  | 100.0%  | 10    |
  | cinder.upload_volume_to_image | 28.041 | 44.016 | 44.644 | 44.698 | 44.751 | 40.726 | 100.0%  | 10    |
  | cinder.delete_volume          | 2.34   | 2.458  | 2.551  | 2.622  | 2.692  | 2.452  | 100.0%  | 10    |
  | nova.delete_image             | 0.846  | 1.837  | 2.379  | 2.418  | 2.456  | 1.73   | 100.0%  | 10    |
  | total                         | 34.983 | 51.394 | 51.872 | 51.877 | 51.881 | 47.796 | 100.0%  | 10    |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 136.222712994
  Full duration: 144.124747038

  test scenario CinderVolumes.create_and_delete_snapshot
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.51  | 4.611  | 4.709  | 4.787  | 4.865 | 4.288 | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.233 | 4.443  | 4.619  | 4.627  | 4.634 | 3.882 | 100.0%  | 10    |
  | total                  | 4.981 | 9.079  | 9.333  | 9.362  | 9.39  | 8.17  | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 23.2197830677
  Full duration: 42.1724328995

  test scenario CinderVolumes.create_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.725 | 2.887  | 3.064  | 3.106  | 3.149 | 2.895 | 100.0%  | 10    |
  | total                | 2.725 | 2.887  | 3.064  | 3.106  | 3.149 | 2.895 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 8.62664198875
  Full duration: 18.587531805

  test scenario CinderVolumes.create_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.696 | 2.857  | 2.932  | 2.943  | 2.954 | 2.838 | 100.0%  | 10    |
  | total                | 2.696 | 2.857  | 2.932  | 2.943  | 2.954 | 2.838 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 8.48678183556
  Full duration: 20.6692960262

  test scenario CinderVolumes.list_volumes
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.list_volumes | 0.202 | 0.275  | 0.381  | 0.408  | 0.435 | 0.283 | 100.0%  | 10    |
  | total               | 0.202 | 0.275  | 0.381  | 0.408  | 0.435 | 0.284 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.910716056824
  Full duration: 47.5472760201

  test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
  +-----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                      |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.74  | 2.894  | 3.015  | 3.036  | 3.056  | 2.893  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.407 | 2.549  | 4.689  | 4.745  | 4.802  | 3.163  | 100.0%  | 10    |
  | nova.attach_volume     | 2.856 | 3.305  | 5.42   | 5.647  | 5.874  | 3.866  | 100.0%  | 10    |
  | nova.detach_volume     | 2.746 | 3.092  | 3.492  | 4.368  | 5.245  | 3.261  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.347 | 2.508  | 4.471  | 4.534  | 4.596  | 2.868  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.418 | 2.546  | 2.956  | 3.852  | 4.748  | 2.758  | 100.0%  | 10    |
  | total                  | 16.42 | 18.913 | 21.766 | 22.976 | 24.185 | 19.181 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 55.4410011768
  Full duration: 103.909024954

  test scenario CinderVolumes.create_from_volume_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.821 | 4.176  | 7.514  | 7.588  | 7.662 | 4.605 | 100.0%  | 10    |
  | cinder.delete_volume | 2.451 | 4.688  | 4.929  | 4.955  | 4.981 | 4.087 | 100.0%  | 10    |
  | total                | 5.373 | 8.93   | 12.095 | 12.233 | 12.37 | 8.692 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.4642841816
  Full duration: 44.0787379742

  test scenario CinderVolumes.create_and_extend_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 2.58  | 2.854  | 3.055  | 3.19   | 3.325 | 2.89  | 100.0%  | 10    |
  | cinder.extend_volume | 2.55  | 2.699  | 2.795  | 2.849  | 2.903 | 2.705 | 100.0%  | 10    |
  | cinder.delete_volume | 2.458 | 2.516  | 2.674  | 2.786  | 2.898 | 2.573 | 100.0%  | 10    |
  | total                | 7.82  | 8.198  | 8.396  | 8.442  | 8.488 | 8.169 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.4196460247
  Full duration: 31.8590240479

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.748  | 2.952  | 3.137  | 3.199  | 3.261  | 2.978  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.472  | 2.569  | 4.675  | 4.696  | 4.717  | 3.178  | 100.0%  | 10    |
  | nova.attach_volume     | 3.051  | 3.462  | 5.38   | 5.41   | 5.439  | 3.956  | 100.0%  | 10    |
  | nova.detach_volume     | 2.802  | 3.058  | 3.281  | 3.413  | 3.546  | 3.096  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.255  | 2.431  | 4.385  | 4.44   | 4.496  | 2.984  | 100.0%  | 10    |
  | cinder.delete_volume   | 2.341  | 2.485  | 2.773  | 3.721  | 4.67   | 2.693  | 100.0%  | 10    |
  | total                  | 16.553 | 19.163 | 21.677 | 21.681 | 21.686 | 19.224 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 55.8534150124
  Full duration: 107.20220089

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +-----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
  +------------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | cinder.create_volume   | 2.655  | 2.924  | 3.771  | 3.779  | 3.786  | 3.159 | 100.0%  | 10    |
  | cinder.create_snapshot | 2.411  | 2.565  | 4.602  | 4.659  | 4.716  | 3.157 | 100.0%  | 10    |
  | nova.attach_volume     | 3.053  | 3.236  | 5.158  | 5.352  | 5.546  | 3.726 | 100.0%  | 10    |
  | nova.detach_volume     | 2.752  | 2.964  | 3.54   | 4.371  | 5.201  | 3.196 | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.147  | 2.424  | 4.491  | 4.497  | 4.503  | 2.802 | 100.0%  | 10    |
  | cinder.delete_volume   | 2.484  | 2.574  | 2.677  | 2.726  | 2.775  | 2.582 | 100.0%  | 10    |
  | total                  | 17.334 | 19.301 | 20.332 | 21.118 | 21.904 | 19.2  | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 56.6079628468
  Full duration: 108.998883963

  run_rally - INFO - Test scenario: "cinder" OK.
  run_rally - INFO - Starting test scenario "heat" ...

  Preparing input task
  Task  aae5a92c-66ff-4c8c-b4a3-0957baac4610: started
  Task aae5a92c-66ff-4c8c-b4a3-0957baac4610: finished

  test scenario HeatStacks.create_suspend_resume_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack  | 2.922 | 3.271  | 3.354  | 3.38   | 3.406 | 3.229 | 100.0%  | 10    |
  | heat.suspend_stack | 1.21  | 1.305  | 1.397  | 1.4    | 1.403 | 1.31  | 100.0%  | 10    |
  | heat.resume_stack  | 1.183 | 1.318  | 1.348  | 1.352  | 1.356 | 1.301 | 100.0%  | 10    |
  | heat.delete_stack  | 1.161 | 1.306  | 2.368  | 2.383  | 2.398 | 1.68  | 100.0%  | 10    |
  | total              | 6.612 | 7.196  | 8.411  | 8.476  | 8.541 | 7.519 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 21.979665041
  Full duration: 25.784487009

  test scenario HeatStacks.create_and_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.8   | 2.896  | 3.053  | 3.136  | 3.219 | 2.929 | 100.0%  | 10    |
  | heat.delete_stack | 1.167 | 1.185  | 1.272  | 1.284  | 1.296 | 1.202 | 100.0%  | 10    |
  | total             | 3.967 | 4.11   | 4.26   | 4.334  | 4.409 | 4.13  | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 12.3352811337
  Full duration: 16.1414811611

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 13.463 | 15.842 | 17.472 | 17.519 | 17.565 | 15.768 | 100.0%  | 10    |
  | heat.delete_stack | 8.575  | 9.635  | 10.691 | 10.703 | 10.714 | 9.537  | 100.0%  | 10    |
  | total             | 22.054 | 25.534 | 27.126 | 27.181 | 27.236 | 25.305 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 74.6174178123
  Full duration: 78.7209010124

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 9.848  | 12.353 | 14.548 | 14.574 | 14.6   | 12.757 | 100.0%  | 10    |
  | heat.delete_stack | 6.448  | 7.541  | 8.549  | 8.581  | 8.612  | 7.65   | 100.0%  | 10    |
  | total             | 17.369 | 19.894 | 23.098 | 23.155 | 23.212 | 20.407 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 61.6486670971
  Full duration: 65.8705642223

  test scenario HeatStacks.list_stacks_and_resources
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.list_stacks                | 0.198 | 0.23   | 0.268  | 0.302  | 0.337 | 0.238 | 100.0%  | 10    |
  | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0   | 0.0   | 100.0%  | 10    |
  | total                           | 0.198 | 0.231  | 0.268  | 0.302  | 0.337 | 0.238 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.700455904007
  Full duration: 4.55407810211

  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | heat.create_stack | 3.01  | 3.109  | 3.377  | 3.561  | 3.744  | 3.173 | 100.0%  | 10    |
  | heat.update_stack | 3.232 | 3.408  | 4.335  | 4.354  | 4.374  | 3.612 | 100.0%  | 10    |
  | heat.delete_stack | 1.146 | 1.207  | 2.478  | 2.887  | 3.296  | 1.721 | 100.0%  | 10    |
  | total             | 7.423 | 7.67   | 9.921  | 10.311 | 10.702 | 8.505 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 24.7915220261
  Full duration: 29.4085850716

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.881 | 3.066  | 3.233  | 3.377  | 3.52  | 3.09  | 100.0%  | 10    |
  | heat.update_stack | 3.212 | 3.254  | 3.48   | 3.507  | 3.535 | 3.303 | 100.0%  | 10    |
  | heat.delete_stack | 1.154 | 1.167  | 1.188  | 1.194  | 1.201 | 1.17  | 100.0%  | 10    |
  | total             | 7.263 | 7.498  | 7.904  | 7.912  | 7.921 | 7.563 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 22.4006979465
  Full duration: 26.8767819405

  test scenario HeatStacks.create_update_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 3.972  | 4.032  | 6.634  | 6.716  | 6.798  | 4.942  | 100.0%  | 10    |
  | heat.update_stack | 5.327  | 5.354  | 5.482  | 5.548  | 5.614  | 5.388  | 100.0%  | 10    |
  | heat.delete_stack | 2.19   | 2.207  | 2.213  | 2.214  | 2.215  | 2.203  | 100.0%  | 10    |
  | total             | 11.521 | 11.583 | 14.284 | 14.325 | 14.367 | 12.534 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 37.184043169
  Full duration: 41.6411378384

  test scenario HeatStacks.create_update_delete_stack
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 8     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 8.45521402359
  Full duration: 17.6498777866

  test scenario HeatStacks.create_update_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 3.971  | 5.16   | 5.356  | 5.407  | 5.459  | 4.973  | 100.0%  | 10    |
  | heat.update_stack | 5.318  | 5.359  | 5.382  | 5.394  | 5.405  | 5.358  | 100.0%  | 10    |
  | heat.delete_stack | 2.188  | 2.198  | 2.266  | 2.267  | 2.267  | 2.211  | 100.0%  | 10    |
  | total             | 11.488 | 12.723 | 12.979 | 13.011 | 13.043 | 12.543 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 37.0396420956
  Full duration: 41.5464501381

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.829 | 3.044  | 3.212  | 3.247  | 3.283 | 3.029 | 100.0%  | 10    |
  | heat.update_stack | 3.215 | 3.228  | 3.295  | 3.317  | 3.339 | 3.248 | 100.0%  | 10    |
  | heat.delete_stack | 1.144 | 1.154  | 1.183  | 1.191  | 1.198 | 1.161 | 100.0%  | 10    |
  | total             | 7.202 | 7.41   | 7.611  | 7.692  | 7.774 | 7.438 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 22.2332119942
  Full duration: 26.9551222324

  test scenario HeatStacks.create_and_list_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.901 | 3.019  | 3.106  | 3.131  | 3.157 | 3.024 | 100.0%  | 10    |
  | heat.list_stacks  | 0.026 | 0.033  | 0.038  | 0.039  | 0.039 | 0.032 | 100.0%  | 10    |
  | total             | 2.94  | 3.049  | 3.139  | 3.163  | 3.188 | 3.056 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 9.14466500282
  Full duration: 16.6371269226

  test scenario HeatStacks.create_check_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 2.988 | 3.093  | 3.17   | 3.178  | 3.187 | 3.087 | 100.0%  | 10    |
  | heat.check_stack  | 1.182 | 1.191  | 1.218  | 1.227  | 1.235 | 1.197 | 100.0%  | 10    |
  | heat.delete_stack | 1.135 | 1.146  | 1.159  | 1.163  | 1.167 | 1.148 | 100.0%  | 10    |
  | total             | 5.315 | 5.451  | 5.54   | 5.549  | 5.558 | 5.432 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.1800320148
  Full duration: 20.4218199253

  run_rally - INFO - Test scenario: "heat" Failed.
  run_rally - INFO - Starting test scenario "keystone" ...

  Preparing input task
  Task  a2566777-434b-4a10-8720-118485a7d427: started
  Task a2566777-434b-4a10-8720-118485a7d427: finished

  test scenario KeystoneBasic.create_tenant_with_users
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.129 | 0.152  | 0.179  | 0.185  | 0.19  | 0.153 | 100.0%  | 10    |
  | keystone.create_users  | 1.041 | 1.142  | 1.45   | 1.48   | 1.509 | 1.211 | 100.0%  | 10    |
  | total                  | 1.177 | 1.295  | 1.637  | 1.653  | 1.668 | 1.363 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.19324994087
  Full duration: 15.3481221199

  test scenario KeystoneBasic.create_add_and_list_user_roles
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.126 | 0.137  | 0.15   | 0.155  | 0.16  | 0.138 | 100.0%  | 10    |
  | keystone.add_role    | 0.116 | 0.123  | 0.145  | 0.158  | 0.171 | 0.128 | 100.0%  | 10    |
  | keystone.list_roles  | 0.055 | 0.064  | 0.076  | 0.093  | 0.11  | 0.068 | 100.0%  | 10    |
  | total                | 0.308 | 0.334  | 0.36   | 0.362  | 0.364 | 0.335 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.02259397507
  Full duration: 7.21977186203

  test scenario KeystoneBasic.add_and_remove_user_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.127 | 0.155  | 0.187  | 0.19   | 0.192 | 0.159 | 100.0%  | 10    |
  | keystone.add_role    | 0.117 | 0.131  | 0.161  | 0.175  | 0.188 | 0.137 | 100.0%  | 10    |
  | keystone.remove_role | 0.089 | 0.104  | 0.137  | 0.161  | 0.184 | 0.113 | 100.0%  | 10    |
  | total                | 0.352 | 0.4    | 0.454  | 0.471  | 0.487 | 0.408 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.2577559948
  Full duration: 7.18419408798

  test scenario KeystoneBasic.create_update_and_delete_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.131 | 0.147  | 0.168  | 0.175  | 0.181 | 0.15  | 100.0%  | 10    |
  | keystone.update_tenant | 0.073 | 0.081  | 0.138  | 0.138  | 0.138 | 0.094 | 100.0%  | 10    |
  | keystone.delete_tenant | 0.146 | 0.181  | 0.212  | 0.215  | 0.218 | 0.182 | 100.0%  | 10    |
  | total                  | 0.356 | 0.436  | 0.488  | 0.501  | 0.514 | 0.426 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.28746080399
  Full duration: 5.78163409233

  test scenario KeystoneBasic.create_and_delete_service
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_service | 0.136 | 0.149  | 0.185  | 0.201  | 0.217 | 0.158 | 100.0%  | 10    |
  | keystone.delete_service | 0.079 | 0.081  | 0.094  | 0.105  | 0.116 | 0.086 | 100.0%  | 10    |
  | total                   | 0.22  | 0.233  | 0.267  | 0.288  | 0.309 | 0.244 | 100.0%  | 10    |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.732470035553
  Full duration: 5.50471711159

  test scenario KeystoneBasic.create_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.135 | 0.141  | 0.177  | 0.184  | 0.19  | 0.151 | 100.0%  | 10    |
  | total                  | 0.135 | 0.141  | 0.177  | 0.184  | 0.191 | 0.152 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.47666311264
  Full duration: 4.65166783333

  test scenario KeystoneBasic.create_user
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.145 | 0.17   | 0.2    | 0.206  | 0.211 | 0.174 | 100.0%  | 10    |
  | total                | 0.145 | 0.171  | 0.2    | 0.206  | 0.212 | 0.174 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.544457912445
  Full duration: 4.52855014801

  test scenario KeystoneBasic.create_and_list_tenants
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.139 | 0.151  | 0.184  | 0.204  | 0.224 | 0.161 | 100.0%  | 10    |
  | keystone.list_tenants  | 0.054 | 0.062  | 0.076  | 0.095  | 0.115 | 0.067 | 100.0%  | 10    |
  | total                  | 0.201 | 0.213  | 0.277  | 0.286  | 0.295 | 0.227 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.684409141541
  Full duration: 7.2159280777

  test scenario KeystoneBasic.create_and_delete_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.131 | 0.156  | 0.212  | 0.213  | 0.215 | 0.167 | 100.0%  | 10    |
  | keystone.delete_role | 0.132 | 0.159  | 0.222  | 0.244  | 0.266 | 0.174 | 100.0%  | 10    |
  | total                | 0.276 | 0.349  | 0.375  | 0.409  | 0.444 | 0.341 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.00079798698
  Full duration: 5.79344797134

  test scenario KeystoneBasic.get_entities
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.14  | 0.148  | 0.211  | 0.214  | 0.216 | 0.161 | 100.0%  | 10    |
  | keystone.create_user   | 0.083 | 0.09   | 0.105  | 0.122  | 0.138 | 0.094 | 100.0%  | 10    |
  | keystone.create_role   | 0.065 | 0.081  | 0.12   | 0.126  | 0.131 | 0.087 | 100.0%  | 10    |
  | keystone.get_tenant    | 0.054 | 0.064  | 0.115  | 0.117  | 0.119 | 0.078 | 100.0%  | 10    |
  | keystone.get_user      | 0.055 | 0.062  | 0.081  | 0.104  | 0.127 | 0.069 | 100.0%  | 10    |
  | keystone.get_role      | 0.055 | 0.062  | 0.096  | 0.109  | 0.121 | 0.071 | 100.0%  | 10    |
  | keystone.service_list  | 0.053 | 0.06   | 0.069  | 0.072  | 0.074 | 0.061 | 100.0%  | 10    |
  | keystone.get_service   | 0.054 | 0.059  | 0.068  | 0.087  | 0.105 | 0.063 | 100.0%  | 10    |
  | total                  | 0.577 | 0.674  | 0.806  | 0.815  | 0.825 | 0.685 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.99226713181
  Full duration: 11.5220220089

  test scenario KeystoneBasic.create_and_list_users
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.148 | 0.173  | 0.197  | 0.206  | 0.215 | 0.175 | 100.0%  | 10    |
  | keystone.list_users  | 0.059 | 0.062  | 0.068  | 0.068  | 0.069 | 0.063 | 100.0%  | 10    |
  | total                | 0.207 | 0.238  | 0.259  | 0.267  | 0.275 | 0.238 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.724813938141
  Full duration: 4.96498990059

  run_rally - INFO - Test scenario: "keystone" OK.
  run_rally - INFO - Starting test scenario "neutron" ...

  Preparing input task
  Task  54896a60-668a-4109-89ce-b6be1526b03c: started
  Task 54896a60-668a-4109-89ce-b6be1526b03c: finished

  test scenario NeutronNetworks.create_and_delete_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.495 | 0.647  | 0.86   | 0.862  | 0.864 | 0.662 | 100.0%  | 10    |
  | neutron.delete_port | 0.138 | 0.389  | 0.568  | 0.757  | 0.946 | 0.413 | 100.0%  | 10    |
  | total               | 0.633 | 0.994  | 1.292  | 1.551  | 1.809 | 1.075 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.11711192131
  Full duration: 33.0977571011

  test scenario NeutronNetworks.create_and_list_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.499 | 0.61   | 0.652  | 0.678  | 0.704 | 0.602 | 100.0%  | 10    |
  | neutron.create_router        | 0.146 | 0.344  | 0.458  | 0.463  | 0.467 | 0.349 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.258 | 0.522  | 0.604  | 0.672  | 0.739 | 0.519 | 100.0%  | 10    |
  | neutron.list_routers         | 0.026 | 0.282  | 0.457  | 0.501  | 0.545 | 0.272 | 100.0%  | 10    |
  | total                        | 1.316 | 1.657  | 1.975  | 2.111  | 2.247 | 1.742 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 5.24421405792
  Full duration: 37.3269040585

  test scenario NeutronNetworks.create_and_delete_routers
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet           | 0.563 | 0.666  | 0.868  | 1.002  | 1.136 | 0.721 | 100.0%  | 10    |
  | neutron.create_router           | 0.13  | 0.373  | 0.573  | 0.595  | 0.616 | 0.384 | 100.0%  | 10    |
  | neutron.add_interface_router    | 0.274 | 0.505  | 0.574  | 0.605  | 0.637 | 0.471 | 100.0%  | 10    |
  | neutron.remove_interface_router | 0.234 | 0.492  | 0.66   | 0.676  | 0.692 | 0.512 | 100.0%  | 10    |
  | neutron.delete_router           | 0.117 | 0.329  | 0.731  | 0.744  | 0.756 | 0.341 | 100.0%  | 10    |
  | total                           | 1.572 | 2.372  | 2.966  | 3.156  | 3.347 | 2.43  | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 7.02413988113
  Full duration: 37.7696969509

  test scenario NeutronNetworks.create_and_list_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.507 | 0.678  | 0.859  | 0.871  | 0.883 | 0.7   | 100.0%  | 10    |
  | neutron.list_ports  | 0.131 | 0.305  | 0.497  | 0.512  | 0.526 | 0.325 | 100.0%  | 10    |
  | total               | 0.792 | 1.051  | 1.18   | 1.187  | 1.193 | 1.025 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.00920605659
  Full duration: 34.7632040977

  test scenario NeutronNetworks.create_and_delete_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.505 | 0.561  | 0.698  | 0.722  | 0.747 | 0.592 | 100.0%  | 10    |
  | neutron.delete_subnet | 0.141 | 0.477  | 0.75   | 0.785  | 0.82  | 0.516 | 100.0%  | 10    |
  | total                 | 0.759 | 1.066  | 1.367  | 1.429  | 1.491 | 1.108 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.30927801132
  Full duration: 34.2646439075

  test scenario NeutronNetworks.create_and_delete_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.368 | 0.511  | 0.727  | 0.746  | 0.765 | 0.541 | 100.0%  | 10    |
  | neutron.delete_network | 0.115 | 0.331  | 0.399  | 0.421  | 0.443 | 0.328 | 100.0%  | 10    |
  | total                  | 0.519 | 0.876  | 1.09   | 1.149  | 1.209 | 0.87  | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.45112395287
  Full duration: 17.3522310257

  test scenario NeutronNetworks.create_and_list_networks
  +-----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                      |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | neutron.create_network | 0.376 | 0.514  | 51.874 | 51.881 | 51.887 | 21.012 | 100.0%  | 10    |
  | neutron.list_networks  | 0.048 | 0.264  | 0.303  | 0.312  | 0.32   | 0.246  | 100.0%  | 10    |
  | total                  | 0.644 | 0.78   | 52.142 | 52.175 | 52.208 | 21.258 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 53.5037658215
  Full duration: 70.7888660431

  test scenario NeutronNetworks.create_and_update_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.457 | 0.651  | 0.738  | 0.757  | 0.777 | 0.631 | 100.0%  | 10    |
  | neutron.create_router        | 0.144 | 0.334  | 0.45   | 0.477  | 0.504 | 0.349 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.286 | 0.546  | 0.676  | 0.685  | 0.695 | 0.555 | 100.0%  | 10    |
  | neutron.update_router        | 0.099 | 0.36   | 0.43   | 0.438  | 0.446 | 0.312 | 100.0%  | 10    |
  | total                        | 1.176 | 1.895  | 2.106  | 2.13   | 2.155 | 1.848 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 5.49681401253
  Full duration: 37.4188079834

  test scenario NeutronNetworks.create_and_update_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.36  | 0.471  | 0.71   | 0.73   | 0.75  | 0.528 | 100.0%  | 10    |
  | neutron.update_network | 0.123 | 0.355  | 0.42   | 0.426  | 0.431 | 0.336 | 100.0%  | 10    |
  | total                  | 0.651 | 0.826  | 1.115  | 1.126  | 1.137 | 0.863 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.45435285568
  Full duration: 19.8497779369

  test scenario NeutronNetworks.create_and_update_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.522 | 0.606  | 0.691  | 0.706  | 0.721 | 0.612 | 100.0%  | 10    |
  | neutron.update_port | 0.187 | 0.343  | 0.388  | 0.389  | 0.39  | 0.336 | 100.0%  | 10    |
  | total               | 0.756 | 0.965  | 1.027  | 1.044  | 1.061 | 0.948 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.89304494858
  Full duration: 35.0843141079

  test scenario NeutronNetworks.create_and_list_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.435 | 0.561  | 0.697  | 0.716  | 0.735 | 0.584 | 100.0%  | 10    |
  | neutron.list_subnets  | 0.259 | 0.312  | 0.4    | 0.427  | 0.455 | 0.331 | 100.0%  | 10    |
  | total                 | 0.785 | 0.877  | 1.111  | 1.12   | 1.129 | 0.915 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.61414718628
  Full duration: 34.7340919971

  test scenario NeutronNetworks.create_and_update_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.496 | 0.57   | 0.724  | 0.732  | 0.741 | 0.598 | 100.0%  | 10    |
  | neutron.update_subnet | 0.356 | 0.433  | 0.584  | 0.599  | 0.615 | 0.47  | 100.0%  | 10    |
  | total                 | 0.889 | 1.045  | 1.22   | 1.231  | 1.242 | 1.068 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.22795987129
  Full duration: 33.4197108746

  run_rally - INFO - Test scenario: "neutron" OK.
  run_rally - INFO - Starting test scenario "nova" ...

  Preparing input task
  Task  d97765c7-bb1a-461c-8a74-ade03e3cc05a: started
  Task d97765c7-bb1a-461c-8a74-ade03e3cc05a: finished

  test scenario NovaKeypair.create_and_delete_keypair
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.404 | 0.52   | 1.075  | 1.084  | 1.093 | 0.647 | 100.0%  | 10    |
  | nova.delete_keypair | 0.021 | 0.023  | 0.03   | 0.036  | 0.041 | 0.026 | 100.0%  | 10    |
  | total               | 0.432 | 0.546  | 1.099  | 1.11   | 1.122 | 0.673 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.18305206299
  Full duration: 18.7849049568

  test scenario NovaServers.snapshot_server
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server       | 4.34   | 6.072  | 6.37   | 6.458  | 6.546  | 5.696  | 100.0%  | 10    |
  | nova.create_image      | 26.042 | 43.405 | 45.329 | 45.435 | 45.541 | 40.593 | 100.0%  | 10    |
  | nova.delete_server     | 2.313  | 2.59   | 2.699  | 2.859  | 3.019  | 2.586  | 100.0%  | 10    |
  | nova.boot_server (2)   | 8.297  | 11.985 | 12.916 | 13.279 | 13.642 | 11.495 | 100.0%  | 10    |
  | nova.delete_server (2) | 2.4    | 2.622  | 2.761  | 2.777  | 2.792  | 2.638  | 100.0%  | 10    |
  | nova.delete_image      | 1.443  | 2.236  | 2.891  | 3.258  | 3.626  | 2.279  | 100.0%  | 10    |
  | total                  | 45.514 | 69.068 | 71.631 | 72.478 | 73.326 | 65.288 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 189.056165934
  Full duration: 227.369397879

  test scenario NovaKeypair.boot_and_delete_server_with_keypair
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | nova.create_keypair | 0.393 | 0.542  | 0.682  | 0.906  | 1.129  | 0.575 | 100.0%  | 10    |
  | nova.boot_server    | 5.333 | 6.169  | 7.894  | 7.9    | 7.907  | 6.354 | 100.0%  | 10    |
  | nova.delete_server  | 2.343 | 2.689  | 2.83   | 2.847  | 2.864  | 2.658 | 100.0%  | 10    |
  | nova.delete_keypair | 0.02  | 0.025  | 0.032  | 0.034  | 0.035  | 0.026 | 100.0%  | 10    |
  | total               | 8.385 | 9.359  | 11.149 | 11.258 | 11.367 | 9.613 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 29.3410420418
  Full duration: 66.8611400127

  test scenario NovaKeypair.create_and_list_keypairs
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +---------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.4  | 0.494  | 0.589  | 0.867  | 1.146 | 0.544 | 100.0%  | 10    |
  | nova.list_keypairs  | 0.01 | 0.014  | 0.017  | 0.018  | 0.019 | 0.013 | 100.0%  | 10    |
  | total               | 0.41 | 0.508  | 0.603  | 0.884  | 1.165 | 0.558 | 100.0%  | 10    |
  +---------------------+------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.71813702583
  Full duration: 20.3168940544

  test scenario NovaServers.list_servers
  +---------------------------------------------------------------------------------------+
  |                                 Response Times (sec)                                  |
  +-------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min  | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+------+--------+--------+--------+-------+-------+---------+-------+
  | nova.list_servers | 0.64 | 0.917  | 1.069  | 1.117  | 1.165 | 0.895 | 100.0%  | 10    |
  | total             | 0.64 | 0.917  | 1.07   | 1.117  | 1.165 | 0.895 | 100.0%  | 10    |
  +-------------------+------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.65287709236
  Full duration: 66.0498650074

  test scenario NovaServers.resize_server
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 6     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 815.834815979
  Full duration: 839.469985008

  test scenario NovaServers.boot_server_from_volume_and_delete
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+-------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max   | avg    | success | count |
  +----------------------+--------+--------+--------+--------+-------+--------+---------+-------+
  | cinder.create_volume | 5.574  | 6.234  | 8.567  | 8.613  | 8.66  | 6.605  | 100.0%  | 10    |
  | nova.boot_server     | 4.812  | 6.08   | 6.59   | 6.789  | 6.988 | 6.029  | 100.0%  | 10    |
  | nova.delete_server   | 2.339  | 2.631  | 2.668  | 2.687  | 2.707 | 2.602  | 100.0%  | 10    |
  | total                | 13.379 | 15.107 | 16.804 | 16.977 | 17.15 | 15.236 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+-------+--------+---------+-------+
  Load duration: 45.449835062
  Full duration: 88.6502871513

  test scenario NovaServers.boot_and_migrate_server
  +-----------------------------------------------------------------------+
  |                         Response Times (sec)                          |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | action | min | median | 90%ile | 95%ile | max | avg | success | count |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  | total  | n/a | n/a    | n/a    | n/a    | n/a | n/a | 0.0%    | 5     |
  +--------+-----+--------+--------+--------+-----+-----+---------+-------+
  Load duration: 824.306979895
  Full duration: 846.910109043

  test scenario NovaServers.boot_and_delete_server
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server   | 4.471 | 5.91   | 6.147  | 6.182  | 6.217 | 5.681 | 100.0%  | 10    |
  | nova.delete_server | 2.378 | 2.586  | 2.707  | 2.746  | 2.785 | 2.579 | 100.0%  | 10    |
  | total              | 7.061 | 8.47   | 8.67   | 8.754  | 8.839 | 8.26  | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 24.1857261658
  Full duration: 60.5944719315

  test scenario NovaServers.boot_and_rebuild_server
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +---------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg   | success | count |
  +---------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  | nova.boot_server    | 4.333  | 5.804  | 6.335  | 6.417  | 6.498  | 5.565 | 100.0%  | 10    |
  | nova.rebuild_server | 7.496  | 8.885  | 9.786  | 9.911  | 10.036 | 8.862 | 100.0%  | 10    |
  | nova.delete_server  | 2.289  | 2.614  | 2.738  | 2.741  | 2.744  | 2.563 | 100.0%  | 10    |
  | total               | 14.866 | 17.495 | 18.471 | 18.474 | 18.476 | 16.99 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 49.6322209835
  Full duration: 85.0604588985

  test scenario NovaSecGroup.create_and_list_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 3.185  | 3.686  | 3.987  | 4.312  | 4.638  | 3.699  | 100.0%  | 10    |
  | nova.create_100_rules          | 18.567 | 26.267 | 26.534 | 26.699 | 26.865 | 24.773 | 100.0%  | 10    |
  | nova.list_security_groups      | 0.078  | 0.128  | 0.182  | 0.185  | 0.187  | 0.13   | 100.0%  | 10    |
  | total                          | 22.414 | 29.93  | 30.82  | 30.98  | 31.14  | 28.603 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 82.9733760357
  Full duration: 116.589685917

  test scenario NovaSecGroup.create_and_delete_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 2.944  | 3.432  | 3.733  | 3.782  | 3.831  | 3.421  | 100.0%  | 10    |
  | nova.create_100_rules          | 16.376 | 21.41  | 22.17  | 22.462 | 22.754 | 20.611 | 100.0%  | 10    |
  | nova.delete_10_security_groups | 0.917  | 1.088  | 1.275  | 1.303  | 1.332  | 1.093  | 100.0%  | 10    |
  | total                          | 20.695 | 25.965 | 26.896 | 26.95  | 27.004 | 25.125 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 72.9624798298
  Full duration: 89.82077384

  test scenario NovaServers.boot_and_bounce_server
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  | action                  | min    | median | 90%ile | 95%ile  | max     | avg    | success | count |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  | nova.boot_server        | 4.125  | 4.583  | 6.312  | 6.519   | 6.725   | 5.156  | 100.0%  | 10    |
  | nova.reboot_server      | 2.419  | 2.493  | 2.871  | 3.889   | 4.906   | 2.736  | 100.0%  | 10    |
  | nova.soft_reboot_server | 4.365  | 4.758  | 16.946 | 70.03   | 123.114 | 16.564 | 100.0%  | 10    |
  | nova.stop_server        | 5.106  | 14.074 | 15.736 | 15.772  | 15.808  | 13.538 | 100.0%  | 10    |
  | nova.start_server       | 1.398  | 1.653  | 1.789  | 2.027   | 2.264   | 1.691  | 100.0%  | 10    |
  | nova.rescue_server      | 6.466  | 6.855  | 15.712 | 16.593  | 17.474  | 8.701  | 100.0%  | 10    |
  | nova.unrescue_server    | 2.236  | 2.258  | 2.473  | 2.501   | 2.529   | 2.318  | 100.0%  | 10    |
  | nova.delete_server      | 2.302  | 2.339  | 2.497  | 2.533   | 2.568   | 2.392  | 100.0%  | 10    |
  | total                   | 30.075 | 40.221 | 65.737 | 113.006 | 160.274 | 53.112 | 100.0%  | 10    |
  +-------------------------+--------+--------+--------+---------+---------+--------+---------+-------+
  Load duration: 160.307124138
  Full duration: 195.760754108

  test scenario NovaServers.boot_server
  +---------------------------------------------------------------------------------------+
  |                                 Response Times (sec)                                  |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server | 4.346 | 5.987  | 7.641  | 7.662  | 7.683 | 6.099 | 100.0%  | 10    |
  | total            | 4.346 | 5.987  | 7.641  | 7.662  | 7.684 | 6.099 | 100.0%  | 10    |
  +------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 17.5887329578
  Full duration: 42.9464931488

  test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
  +-----------------------------------------------------------------------------------------------------------+
  |                                           Response Times (sec)                                            |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups    | 2.723  | 3.726  | 4.171  | 4.216  | 4.261  | 3.683  | 100.0%  | 10    |
  | nova.create_100_rules             | 18.505 | 26.114 | 26.91  | 26.926 | 26.943 | 24.62  | 100.0%  | 10    |
  | nova.boot_server                  | 3.627  | 4.946  | 5.965  | 6.019  | 6.073  | 4.932  | 100.0%  | 10    |
  | nova.get_attached_security_groups | 0.108  | 0.131  | 0.253  | 0.324  | 0.396  | 0.166  | 100.0%  | 10    |
  | nova.delete_server                | 2.334  | 2.379  | 2.491  | 2.512  | 2.533  | 2.396  | 100.0%  | 10    |
  | nova.delete_10_security_groups    | 0.973  | 1.409  | 1.639  | 1.832  | 2.026  | 1.399  | 100.0%  | 10    |
  | total                             | 28.564 | 39.133 | 39.77  | 39.952 | 40.134 | 37.197 | 100.0%  | 10    |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 107.169257164
  Full duration: 144.236375093

  test scenario NovaServers.pause_and_unpause_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 4.178  | 6.265  | 6.892  | 7.037  | 7.182  | 6.066  | 100.0%  | 10    |
  | nova.pause_server   | 2.287  | 2.526  | 2.683  | 2.743  | 2.804  | 2.548  | 100.0%  | 10    |
  | nova.unpause_server | 2.436  | 2.503  | 2.571  | 2.571  | 2.572  | 2.507  | 100.0%  | 10    |
  | nova.delete_server  | 2.294  | 2.606  | 2.995  | 3.945  | 4.895  | 2.755  | 100.0%  | 10    |
  | total               | 11.529 | 13.896 | 14.859 | 15.712 | 16.564 | 13.876 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 40.5261249542
  Full duration: 76.823114872

  test scenario NovaServers.boot_server_from_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 5.836  | 6.478  | 9.07   | 9.177  | 9.283  | 7.115  | 100.0%  | 10    |
  | nova.boot_server     | 5.52   | 6.079  | 6.596  | 7.362  | 8.128  | 6.22   | 100.0%  | 10    |
  | total                | 11.526 | 12.516 | 15.434 | 15.438 | 15.442 | 13.335 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 39.5622808933
  Full duration: 73.6733939648

  test scenario NovaServers.boot_and_list_server
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.boot_server  | 4.694 | 6.002  | 6.133  | 6.249  | 6.365 | 5.738 | 100.0%  | 10    |
  | nova.list_servers | 0.141 | 0.377  | 0.551  | 0.599  | 0.646 | 0.376 | 100.0%  | 10    |
  | total             | 5.074 | 6.186  | 6.707  | 6.807  | 6.906 | 6.114 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 17.6599957943
  Full duration: 64.1471071243

  run_rally - INFO - Test scenario: "nova" Failed.
  run_rally - INFO - Starting test scenario "quotas" ...

  Preparing input task
  Task  5eda6ea1-f001-4a0e-b6cd-7685d1803fd5: started
  Task 5eda6ea1-f001-4a0e-b6cd-7685d1803fd5: finished

  test scenario Quotas.cinder_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.692 | 0.867  | 1.007  | 1.025  | 1.043 | 0.869 | 100.0%  | 10    |
  | total                | 0.692 | 0.867  | 1.007  | 1.025  | 1.043 | 0.869 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.54990196228
  Full duration: 9.24233794212

  test scenario Quotas.neutron_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.318 | 0.578  | 0.742  | 0.759  | 0.776 | 0.558 | 100.0%  | 10    |
  | total                | 0.384 | 0.669  | 0.825  | 0.837  | 0.848 | 0.646 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.74635910988
  Full duration: 8.15396595001

  test scenario Quotas.cinder_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.686 | 0.867  | 1.072  | 1.087  | 1.102 | 0.87  | 100.0%  | 10    |
  | quotas.delete_quotas | 0.563 | 0.613  | 0.737  | 0.75   | 0.763 | 0.631 | 100.0%  | 10    |
  | total                | 1.274 | 1.453  | 1.698  | 1.782  | 1.865 | 1.501 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.41035509109
  Full duration: 11.0862941742

  test scenario Quotas.nova_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.48  | 0.753  | 1.082  | 1.107  | 1.133 | 0.811 | 100.0%  | 10    |
  | quotas.delete_quotas | 0.025 | 0.066  | 0.091  | 0.114  | 0.138 | 0.066 | 100.0%  | 10    |
  | total                | 0.505 | 0.812  | 1.14   | 1.173  | 1.206 | 0.878 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.45851612091
  Full duration: 8.88383197784

  test scenario Quotas.nova_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.516 | 0.798  | 1.182  | 1.19   | 1.198 | 0.829 | 100.0%  | 10    |
  | total                | 0.516 | 0.798  | 1.182  | 1.19   | 1.198 | 0.829 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.38111186028
  Full duration: 8.62598204613

  run_rally - INFO - Test scenario: "quotas" OK.
  run_rally - INFO - Starting test scenario "requests" ...

  Preparing input task
  Task  6afaa02c-ce64-423c-8af7-1f3436c08dbd: started
  Task 6afaa02c-ce64-423c-8af7-1f3436c08dbd: finished

  test scenario HttpRequests.check_random_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 5.022 | 5.033  | 5.491  | 5.493  | 5.495 | 5.191 | 100.0%  | 10    |
  | total                  | 5.022 | 5.034  | 5.491  | 5.493  | 5.495 | 5.191 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 15.5716190338
  Full duration: 18.0286371708

  test scenario HttpRequests.check_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 5.021 | 5.026  | 5.03   | 5.032  | 5.033 | 5.026 | 100.0%  | 10    |
  | total                  | 5.021 | 5.026  | 5.03   | 5.032  | 5.033 | 5.026 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 15.1103169918
  Full duration: 17.6116039753

  run_rally - INFO - Test scenario: "requests" OK.

                       Rally Summary Report
  +===================+============+===============+===========+
  | Module            | Duration   | nb. Test Run  | Success   |
  +===================+============+===============+===========+
  | authenticate      | 00:20      | 10            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | glance            | 01:52      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | cinder            | 15:05      | 50            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | heat              | 06:52      | 32            | 92.31%    |
  +-------------------+------------+---------------+-----------+
  | keystone          | 01:19      | 29            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | neutron           | 07:05      | 31            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | nova              | 52:04      | 52            | 88.89%    |
  +-------------------+------------+---------------+-----------+
  | quotas            | 00:45      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | requests          | 00:35      | 2             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  +===================+============+===============+===========+
  | TOTAL:            | 01:26:02   | 220           | 97.91%    |
  +===================+============+===============+===========+



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
    | checksum         | 11834a548b5f6fa25d331353b139cb1a     |
    | container_format | bare                                 |
    | created_at       | 2016-02-24T07:59:46Z                 |
    | disk_format      | qcow2                                |
    | id               | 0074bf80-807e-4cb7-b904-bf4347c2a668 |
    | min_disk         | 0                                    |
    | min_ram          | 0                                    |
    | name             | cirros                               |
    | owner            | 3d15a63c2519439f839df6785236b0e1     |
    | protected        | False                                |
    | size             | 15482                                |
    | status           | active                               |
    | tags             | []                                   |
    | updated_at       | 2016-02-24T07:59:47Z                 |
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
    | created                              | 2016-02-24T07:59:49Z                          |
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
