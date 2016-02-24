.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

Detailed test results for joid-os-odl_l2-nofeature-ha
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
  vPing_ssh- INFO - vPing Start Time:'2016-02-23 10:26:42'
  vPing_ssh- INFO - Creating instance 'opnfv-vping-1'...
   name=opnfv-vping-1
   flavor=<Flavor: m1.small>
   image=13cc508d-303d-46a8-bd03-3edae4434dfb
   network=b183c17a-bac5-4e45-afba-f5bc61edcf9e

  vPing_ssh- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  vPing_ssh- INFO - Adding 'opnfv-vping-1' to security group 'vPing-sg'...
  vPing_ssh- INFO - Creating instance 'opnfv-vping-2'...
   name=opnfv-vping-2
   flavor=<Flavor: m1.small>
   image=13cc508d-303d-46a8-bd03-3edae4434dfb
   network=b183c17a-bac5-4e45-afba-f5bc61edcf9e

  vPing_ssh- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  vPing_ssh- INFO - Adding 'opnfv-vping-2' to security group 'vPing-sg'...
  vPing_ssh- INFO - Creating floating IP for VM 'opnfv-vping-2'...
  vPing_ssh- INFO - Floating IP created: '161.105.231.3'
  vPing_ssh- INFO - Associating floating ip: '161.105.231.3' to VM 'opnfv-vping-2'
  vPing_ssh- INFO - Trying to establish SSH connection to 161.105.231.3...
  vPing_ssh- INFO - Waiting for ping...
  vPing_ssh- INFO - vPing detected!
  vPing_ssh- INFO - vPing duration:'33.5' s.
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
  vPing_userdata- INFO - vPing Start Time:'2016-02-23 10:27:41'
  vPing_userdata- INFO - Creating instance 'opnfv-vping-1'...
   name=opnfv-vping-1
   flavor=<Flavor: m1.small>
   image=a9b0741e-0d2d-4503-b267-af151870739e
   network=9d9b24f9-7bea-48b1-a4eb-771bf3784900

  vPing_userdata- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  vPing_userdata- INFO - Creating instance 'opnfv-vping-2'...
   name=opnfv-vping-2
   flavor=<Flavor: m1.small>
   image=a9b0741e-0d2d-4503-b267-af151870739e
   network=9d9b24f9-7bea-48b1-a4eb-771bf3784900
   userdata=
  #!/bin/sh

  while true; do
   ping -c 1 192.168.130.3 2>&1 >/dev/null
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
  vPing_userdata- INFO - vPing duration:'17.9'
  vPing_userdata- INFO - vPing OK
  vPing_userdata- INFO - Cleaning up...
  vPing_userdata- INFO - Deleting network 'vping-net'...


Tempest
^^^^^^^
::

  FUNCTEST.info: Running Tempest tests...
  run_tempest - INFO - Creating tenant and user for Tempest suite
  2016-02-23 10:28:17.615 23826 INFO rally.verification.tempest.tempest [-] Starting: Creating configuration file for Tempest.
  2016-02-23 10:28:23.990 23826 INFO rally.verification.tempest.tempest [-] Completed: Creating configuration file for Tempest.

  run_tempest - INFO - Starting Tempest test suite: '--tests-file /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/custom_tests/test_list.txt'.
  Total results of verification:

  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | UUID                                 | Deployment UUID                      | Set name | Tests | Failures | Created at                 | Status   |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | 473116be-ef51-45b4-a46d-dcc17b02d920 | 7fa447a8-f40c-475e-bae8-d4f62027b80b |          | 210   | 5        | 2016-02-23 10:28:27.307831 | finished |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+

  Tests:

  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | name                                                                                                                                     | time      | status  |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.88396   | success |
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.17728   | success |
  | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 9.72530   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 9.15814   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 7.24988   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.23094   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_name                              | 1.23775   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_id                         | 0.92287   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_server_ref                        | 0.79109   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_status                            | 0.20110   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_type                              | 0.48230   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_limit_results                               | 0.46126   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_changes_since         | 0.50215   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_name                  | 0.21126   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_server_ref            | 0.24888   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_status                | 0.19557   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_filter_by_type                  | 0.53114   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_with_detail_limit_results                   | 0.88118   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image                                                            | 0.52117   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images                                                          | 1.01633   | success |
  | tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail                                              | 0.40909   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_create                | 0.80631   | success |
  | tempest.api.compute.security_groups.test_security_group_rules.SecurityGroupRulesTestJSON.test_security_group_rules_list                  | 1.57659   | success |
  | tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete                  | 2.75110   | success |
  | tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_add_remove_fixed_ip                                     | 9.21019   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_host_name_is_same_as_server_name                                     | 62.75436  | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers                                                         | 0.17342   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_list_servers_with_detail                                             | 0.30973   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_created_server_vcpus                                          | 0.33235   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestJSON.test_verify_server_details                                                | 0.00133   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_host_name_is_same_as_server_name                               | 62.74257  | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers                                                   | 0.19542   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_list_servers_with_detail                                       | 0.35564   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_created_server_vcpus                                    | 0.36918   | success |
  | tempest.api.compute.servers.test_create_server.ServersTestManualDisk.test_verify_server_details                                          | 0.00129   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_get_instance_action                                       | 0.18644   | success |
  | tempest.api.compute.servers.test_instance_actions.InstanceActionsTestJSON.test_list_instance_actions                                     | 3.81844   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_flavor               | 0.52933   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_image                | 0.50494   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_name          | 0.33257   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_filter_by_server_status        | 0.38382   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_detailed_limit_results                  | 0.47799   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_flavor                        | 0.24448   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_image                         | 0.22883   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_limit                         | 0.21227   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_name                   | 0.27651   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filter_by_server_status                 | 0.06020   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip                          | 0.40370   | success |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_ip_regex                    | 0.00142   | skip    |
  | tempest.api.compute.servers.test_list_server_filters.ListServerFiltersTestJSON.test_list_servers_filtered_by_name_wildcard               | 0.30281   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_future_date        | 0.25500   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_changes_since_invalid_date       | 0.21292   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits                           | 0.19699   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_greater_than_actual_count | 0.07649   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_negative_value       | 0.14378   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_limits_pass_string               | 0.01122   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_flavor              | 0.03176   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_image               | 0.06131   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_by_non_existing_server_name         | 0.04448   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_detail_server_is_deleted            | 0.21242   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_status_non_existing                 | 0.18448   | success |
  | tempest.api.compute.servers.test_list_servers_negative.ListServersNegativeTestJSON.test_list_servers_with_a_deleted_server               | 0.06615   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_change_server_password                                        | 0.00170   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_get_console_output                                            | 5.05891   | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_lock_unlock_server                                            | 12.21875  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_hard                                            | 10.99696  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_reboot_server_soft                                            | 1.04170   | skip    |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server                                                | 24.60148  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm                                         | 15.56771  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert                                          | 21.94185  | success |
  | tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server                                             | 7.25441   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses                                     | 0.17943   | success |
  | tempest.api.compute.servers.test_server_addresses.ServerAddressesTestJSON.test_list_server_addresses_by_network                          | 1.00217   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_delete_server_metadata_item                                 | 0.76858   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_get_server_metadata_item                                    | 1.16728   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_list_server_metadata                                        | 0.46748   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata                                         | 0.60523   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_set_server_metadata_item                                    | 0.70657   | success |
  | tempest.api.compute.servers.test_server_metadata.ServerMetadataTestJSON.test_update_server_metadata                                      | 0.91519   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password                                          | 2.30147   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_specify_keypair                                                     | 7.86437   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_with_existing_server_name                                           | 15.09430  | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_access_server_address                                               | 9.89837   | success |
  | tempest.api.compute.servers.test_servers.ServersTestJSON.test_update_server_name                                                         | 10.11169  | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_numeric_server_name                                | 1.55906   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_metadata_exceeds_length_limit               | 1.98352   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_server_name_length_exceeds_256                     | 1.47851   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_flavor                                | 1.88043   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_image                                 | 1.53679   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_create_with_invalid_network_uuid                          | 1.27055   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_a_server_of_another_tenant                         | 1.08039   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_id_exceeding_length_limit              | 0.73357   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_delete_server_pass_negative_id                            | 0.86542   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_get_non_existent_server                                   | 0.99209   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_invalid_ip_v6_address                                     | 1.08220   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_reboot_non_existent_server                                | 0.83730   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_rebuild_non_existent_server                               | 0.99153   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_non_existent_flavor                    | 0.54860   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_server_with_null_flavor                            | 0.37611   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_server_name_blank                                         | 1.44613   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_stop_non_existent_server                                  | 0.55699   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_name_of_non_existent_server                        | 0.56507   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_name_length_exceeds_256                     | 0.48514   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_of_another_tenant                           | 0.86713   | success |
  | tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_update_server_set_empty_name                              | 0.61486   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_keypair_in_analt_user_tenant                                    | 0.12864   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_fails_when_tenant_incorrect                              | 0.67877   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_create_server_with_unauthorized_image                                  | 0.61740   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_keypair_of_alt_account_fails                                       | 0.13677   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_get_metadata_of_alt_account_server_fails                               | 1.40358   | success |
  | tempest.api.compute.test_authorization.AuthorizationTestJSON.test_set_metadata_of_alt_account_server_fails                               | 0.16372   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_default_quotas                                                                   | 0.18319   | success |
  | tempest.api.compute.test_quotas.QuotasTestJSON.test_get_quotas                                                                           | 0.33858   | success |
  | tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume                                            | 45.56777  | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list                                                           | 0.72770   | success |
  | tempest.api.compute.volumes.test_volumes_list.VolumesTestJSON.test_volume_list_with_details                                              | 0.30390   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_invalid_volume_id                                         | 0.20202   | success |
  | tempest.api.compute.volumes.test_volumes_negative.VolumesNegativeTest.test_get_volume_without_passing_volume_id                          | 0.17999   | success |
  | tempest.api.identity.admin.v2.test_services.ServicesTestJSON.test_list_services                                                          | 0.34894   | success |
  | tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user                                                                  | 0.13656   | success |
  | tempest.api.identity.admin.v3.test_credentials.CredentialsTestJSON.test_credentials_create_get_update_delete                             | 0.0       | fail    |
  | tempest.api.identity.admin.v3.test_domains.DefaultDomainTestJSON.test_default_domain_exists                                              | 0.05100   | success |
  | tempest.api.identity.admin.v3.test_domains.DomainsTestJSON.test_create_update_delete_domain                                              | 0.50255   | success |
  | tempest.api.identity.admin.v3.test_endpoints.EndPointsTestJSON.test_update_endpoint                                                      | 0.27108   | success |
  | tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON.test_group_users_add_list_delete                                              | 1.16016   | success |
  | tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy                                            | 0.21180   | success |
  | tempest.api.identity.admin.v3.test_regions.RegionsTestJSON.test_create_region_with_specific_id                                           | 0.14141   | success |
  | tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_role_create_update_get_list                                                | 0.25298   | success |
  | tempest.api.identity.admin.v3.test_services.ServicesTestJSON.test_create_update_get_service                                              | 0.20613   | success |
  | tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_get_trusts_all                                                           | 1.42131   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.04287   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.05581   | success |
  | tempest.api.identity.v2.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.05518   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_media_types                                                         | 0.04135   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_resources                                                   | 0.03642   | success |
  | tempest.api.identity.v3.test_api_discovery.TestApiDiscovery.test_api_version_statuses                                                    | 0.04205   | success |
  | tempest.api.image.v1.test_images.ListImagesTest.test_index_no_params                                                                     | 0.32191   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_delete_image                                                             | 1.18189   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_register_upload_get_image_file                                           | 1.74422   | success |
  | tempest.api.image.v2.test_images.BasicOperationsImagesTest.test_update_image                                                             | 2.30171   | success |
  | tempest.api.network.test_extensions.ExtensionsTestJSON.test_list_show_extensions                                                         | 3.45772   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_floating_ip_specifying_a_fixed_ip_address                           | 1.03994   | success |
  | tempest.api.network.test_floating_ips.FloatingIPTestJSON.test_create_list_show_update_delete_floating_ip                                 | 1.42863   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network                                             | 1.14505   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port                                                | 1.60767   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet                                              | 7.84206   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_network                                                 | 1.21731   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_port                                                    | 2.11434   | success |
  | tempest.api.network.test_networks.BulkNetworkOpsTestJSON.test_bulk_create_delete_subnet                                                  | 2.79624   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_create_update_delete_network_subnet                                         | 1.61530   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_external_network_visibility                                                 | 0.38291   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_networks                                                               | 0.20594   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_list_subnets                                                                | 0.19821   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_network                                                                | 0.20089   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestAttrs.test_show_subnet                                                                 | 0.19206   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_create_update_delete_network_subnet                                          | 1.49044   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_external_network_visibility                                                  | 0.23415   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_networks                                                                | 0.21291   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_list_subnets                                                                 | 0.07398   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_network                                                                 | 0.17873   | success |
  | tempest.api.network.test_networks.NetworksIpV6TestJSON.test_show_subnet                                                                  | 0.20287   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools                                            | 1.38012   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_with_no_securitygroups                                                 | 1.87547   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_update_delete_port                                                          | 1.20872   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_list_ports                                                                         | 0.05621   | success |
  | tempest.api.network.test_ports.PortsIpV6TestJSON.test_show_port                                                                          | 0.20890   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_in_allowed_allocation_pools                                                | 1.70139   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_port_with_no_securitygroups                                                     | 1.75502   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_create_update_delete_port                                                              | 1.16521   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_list_ports                                                                             | 0.22620   | success |
  | tempest.api.network.test_ports.PortsTestJSON.test_show_port                                                                              | 0.28640   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_multiple_router_interfaces                                                     | 4.12301   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_port_id                                           | 2.49067   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_add_remove_router_interface_with_subnet_id                                         | 2.25252   | success |
  | tempest.api.network.test_routers.RoutersIpV6Test.test_create_show_list_update_delete_router                                              | 1.48564   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_multiple_router_interfaces                                                         | 4.58651   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_port_id                                               | 2.38901   | success |
  | tempest.api.network.test_routers.RoutersTest.test_add_remove_router_interface_with_subnet_id                                             | 2.54963   | success |
  | tempest.api.network.test_routers.RoutersTest.test_create_show_list_update_delete_router                                                  | 1.37000   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_list_update_show_delete_security_group                             | 1.31226   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_create_show_delete_security_group_rule                                    | 2.04438   | success |
  | tempest.api.network.test_security_groups.SecGroupIPv6Test.test_list_security_groups                                                      | 0.19052   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_list_update_show_delete_security_group                                 | 1.32708   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_create_show_delete_security_group_rule                                        | 2.12672   | success |
  | tempest.api.network.test_security_groups.SecGroupTest.test_list_security_groups                                                          | 0.20945   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_list                                           | 0.55381   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_show                                           | 7.80051   | success |
  | tempest.api.orchestration.stacks.test_resource_types.ResourceTypesTest.test_resource_type_template                                       | 0.03030   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_list                                              | 1.61156   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_deployment_metadata                                          | 0.86944   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_get_software_config                                              | 0.57507   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_create_validate                              | 0.36337   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_no_metadata_change                    | 0.66632   | success |
  | tempest.api.orchestration.stacks.test_soft_conf.TestSoftwareConfig.test_software_deployment_update_with_metadata_change                  | 0.47493   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_crud_no_resources                                                 | 3.52216   | success |
  | tempest.api.orchestration.stacks.test_stacks.StacksTestJSON.test_stack_list_responds                                                     | 0.18647   | success |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v1_notifications                | 303.03506 | fail    |
  | tempest.api.telemetry.test_telemetry_notification_api.TelemetryNotificationAPITestJSON.test_check_glance_v2_notifications                | 301.96207 | fail    |
  | tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance                                       | 3.14842   | success |
  | tempest.api.volume.test_volumes_actions.VolumesV2ActionsTest.test_attach_detach_volume_to_instance                                       | 2.66111   | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete                                                | 9.31807   | success |
  | tempest.api.volume.test_volumes_get.VolumesV1GetTest.test_volume_create_get_update_delete_from_image                                     | 15.30017  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete                                                | 10.64441  | success |
  | tempest.api.volume.test_volumes_get.VolumesV2GetTest.test_volume_create_get_update_delete_from_image                                     | 13.02957  | success |
  | tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list                                                              | 0.56814   | success |
  | tempest.api.volume.test_volumes_list.VolumesV2ListTestJSON.test_volume_list                                                              | 0.23431   | success |
  | tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops                                                       | 42.47353  | success |
  | tempest.scenario.test_server_basic_ops.TestServerBasicOps.test_server_basicops                                                           | 82.90131  | success |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern                                                 | 499.21662 | fail    |
  | tempest.scenario.test_volume_boot_pattern.TestVolumeBootPatternV2.test_volume_boot_pattern                                               | 501.43822 | fail    |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  run_tempest - INFO - Results: {'timestart': '2016-02-2310:28:27.307831', 'duration': 931, 'tests': 210, 'failures': 5}
  run_tempest - INFO - Pushing results to DB: 'http://testresults.opnfv.org/testapi/results'.
  run_tempest - INFO - Deleting tenant and user for Tempest suite)


Rally
^^^^^
::

  FUNCTEST.info: Running Rally benchmark suite...
  run_rally - INFO - Starting test scenario "authenticate" ...
  run_rally - INFO -
   Preparing input task
   Task  1e91fffe-1834-4d97-b18c-95b1c3a11763: started
  Task 1e91fffe-1834-4d97-b18c-95b1c3a11763: finished

  test scenario Authenticate.validate_glance
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_glance     | 0.393 | 0.462  | 0.625  | 0.642  | 0.659 | 0.499 | 100.0%  | 10    |
  | authenticate.validate_glance (2) | 0.042 | 0.05   | 0.222  | 0.235  | 0.247 | 0.101 | 100.0%  | 10    |
  | total                            | 0.56  | 0.722  | 0.84   | 0.907  | 0.975 | 0.716 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.11308193207
  Full duration: 6.43925094604

  test scenario Authenticate.keystone
  +-----------------------------------------------------------------------------+
  |                            Response Times (sec)                             |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  | total  | 0.096 | 0.108  | 0.117  | 0.118  | 0.118 | 0.108 | 100.0%  | 10    |
  +--------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.360912799835
  Full duration: 4.84613108635

  test scenario Authenticate.validate_heat
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_heat     | 0.198 | 0.223  | 0.243  | 0.246  | 0.25  | 0.222 | 100.0%  | 10    |
  | authenticate.validate_heat (2) | 0.035 | 0.229  | 0.268  | 0.272  | 0.275 | 0.195 | 100.0%  | 10    |
  | total                          | 0.349 | 0.56   | 0.636  | 0.648  | 0.66  | 0.537 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.73545908928
  Full duration: 5.89906620979

  test scenario Authenticate.validate_nova
  +-----------------------------------------------------------------------------------------------------+
  |                                        Response Times (sec)                                         |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                         | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_nova     | 0.191 | 0.225  | 0.273  | 0.326  | 0.379 | 0.239 | 100.0%  | 10    |
  | authenticate.validate_nova (2) | 0.193 | 0.215  | 0.268  | 0.324  | 0.379 | 0.233 | 100.0%  | 10    |
  | total                          | 0.512 | 0.561  | 0.696  | 0.708  | 0.719 | 0.589 | 100.0%  | 10    |
  +--------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.73631811142
  Full duration: 6.18624401093

  test scenario Authenticate.validate_cinder
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                           | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_cinder     | 0.187 | 0.219  | 0.269  | 0.451  | 0.632 | 0.256 | 100.0%  | 10    |
  | authenticate.validate_cinder (2) | 0.019 | 0.202  | 0.228  | 0.232  | 0.235 | 0.19  | 100.0%  | 10    |
  | total                            | 0.318 | 0.572  | 0.652  | 0.81   | 0.967 | 0.582 | 100.0%  | 10    |
  +----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.90990018845
  Full duration: 6.19068098068

  test scenario Authenticate.validate_neutron
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | authenticate.validate_neutron     | 0.22  | 0.241  | 0.324  | 0.326  | 0.328 | 0.255 | 100.0%  | 10    |
  | authenticate.validate_neutron (2) | 0.21  | 0.234  | 0.327  | 0.349  | 0.37  | 0.254 | 100.0%  | 10    |
  | total                             | 0.529 | 0.595  | 0.67   | 0.689  | 0.708 | 0.613 | 100.0%  | 10    |
  +-----------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.81688117981
  Full duration: 5.97459483147

  run_rally - INFO - Test scenario: "authenticate" OK.

  run_rally - INFO - Starting test scenario "glance" ...
  run_rally - INFO -
   Preparing input task
   Task  c991643e-676b-49d8-af8c-cf9655ae236b: started
  Task c991643e-676b-49d8-af8c-cf9655ae236b: finished

  test scenario GlanceImages.list_images
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.list_images | 0.47  | 0.551  | 0.604  | 0.621  | 0.638 | 0.559 | 100.0%  | 10    |
  | total              | 0.471 | 0.551  | 0.604  | 0.621  | 0.638 | 0.559 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.7134771347
  Full duration: 7.86669206619

  test scenario GlanceImages.create_image_and_boot_instances
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | glance.create_image | 3.881  | 4.628  | 5.228  | 5.273  | 5.317  | 4.643  | 100.0%  | 10    |
  | nova.boot_servers   | 7.198  | 8.691  | 9.617  | 9.773  | 9.929  | 8.609  | 100.0%  | 10    |
  | total               | 11.395 | 13.062 | 14.63  | 14.674 | 14.718 | 13.252 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 40.5051100254
  Full duration: 80.9348599911

  test scenario GlanceImages.create_and_list_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 4.473 | 4.791  | 5.258  | 5.513  | 5.767 | 4.935 | 100.0%  | 10    |
  | glance.list_images  | 0.046 | 0.143  | 0.285  | 0.293  | 0.302 | 0.159 | 100.0%  | 10    |
  | total               | 4.67  | 5.043  | 5.524  | 5.679  | 5.834 | 5.095 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 15.4974470139
  Full duration: 26.4936869144

  test scenario GlanceImages.create_and_delete_image
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | glance.create_image | 4.297 | 4.864  | 5.167  | 5.345  | 5.523 | 4.859 | 100.0%  | 10    |
  | glance.delete_image | 0.842 | 1.496  | 1.603  | 1.702  | 1.801 | 1.371 | 100.0%  | 10    |
  | total               | 5.14  | 6.405  | 6.623  | 6.626  | 6.63  | 6.23  | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 18.5310051441
  Full duration: 24.86997509

  run_rally - INFO - Test scenario: "glance" OK.

  run_rally - INFO - Starting test scenario "cinder" ...
  run_rally - INFO -
   Preparing input task
   Task  388cb584-9c00-4d54-8f76-53ed3182a475: started
  Task 388cb584-9c00-4d54-8f76-53ed3182a475: finished

  test scenario CinderVolumes.create_and_attach_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server     | 4.792  | 5.804  | 8.436  | 8.476  | 8.516  | 6.313  | 100.0%  | 10    |
  | cinder.create_volume | 3.049  | 3.381  | 3.469  | 3.471  | 3.473  | 3.317  | 100.0%  | 10    |
  | nova.attach_volume   | 3.722  | 3.987  | 4.207  | 4.245  | 4.283  | 4.012  | 100.0%  | 10    |
  | nova.detach_volume   | 3.492  | 3.685  | 3.892  | 3.925  | 3.958  | 3.702  | 100.0%  | 10    |
  | cinder.delete_volume | 0.502  | 0.765  | 2.927  | 2.998  | 3.068  | 1.357  | 100.0%  | 10    |
  | nova.delete_server   | 2.66   | 3.128  | 3.235  | 3.243  | 3.251  | 3.056  | 100.0%  | 10    |
  | total                | 19.466 | 20.925 | 25.056 | 25.456 | 25.856 | 21.758 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 64.0748999119
  Full duration: 88.3469510078

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 6.151 | 6.548  | 8.972  | 9.007  | 9.043 | 7.201 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.044 | 0.249  | 0.299  | 0.32   | 0.34  | 0.227 | 100.0%  | 10    |
  | total                | 6.424 | 6.801  | 9.229  | 9.255  | 9.28  | 7.429 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 22.3146419525
  Full duration: 39.1755928993

  test scenario CinderVolumes.create_and_list_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 3.269 | 3.372  | 3.545  | 3.556  | 3.566 | 3.406 | 100.0%  | 10    |
  | cinder.list_volumes  | 0.051 | 0.27   | 0.296  | 0.304  | 0.313 | 0.249 | 100.0%  | 10    |
  | total                | 3.321 | 3.662  | 3.786  | 3.819  | 3.852 | 3.656 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 11.0692770481
  Full duration: 26.8993549347

  test scenario CinderVolumes.create_and_list_snapshots
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.807 | 3.0    | 3.236  | 4.094  | 4.951 | 3.175 | 100.0%  | 10    |
  | cinder.list_snapshots  | 0.023 | 0.263  | 0.29   | 0.295  | 0.299 | 0.238 | 100.0%  | 10    |
  | total                  | 3.039 | 3.247  | 3.493  | 4.372  | 5.251 | 3.413 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 11.5568339825
  Full duration: 45.8590891361

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 3.35  | 3.413  | 3.511  | 3.567  | 3.622 | 3.434 | 100.0%  | 10    |
  | cinder.delete_volume | 0.666 | 2.775  | 3.101  | 3.101  | 3.101 | 2.07  | 100.0%  | 10    |
  | total                | 4.016 | 6.163  | 6.511  | 6.555  | 6.6   | 5.505 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 16.3949551582
  Full duration: 29.3589651585

  test scenario CinderVolumes.create_and_delete_volume
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | cinder.create_volume | 6.12  | 6.499  | 8.727  | 8.888  | 9.049  | 6.934 | 100.0%  | 10    |
  | cinder.delete_volume | 0.689 | 2.95   | 3.117  | 3.132  | 3.147  | 2.519 | 100.0%  | 10    |
  | total                | 6.97  | 9.45   | 11.391 | 11.777 | 12.163 | 9.454 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 27.9512338638
  Full duration: 42.110273838

  test scenario CinderVolumes.create_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 3.153 | 3.382  | 3.523  | 3.546  | 3.569 | 3.401 | 100.0%  | 10    |
  | cinder.delete_volume | 0.459 | 1.756  | 3.107  | 3.143  | 3.179 | 1.823 | 100.0%  | 10    |
  | total                | 3.976 | 5.273  | 6.386  | 6.427  | 6.468 | 5.225 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.3155708313
  Full duration: 27.9943380356

  test scenario CinderVolumes.create_and_upload_volume_to_image
  +-------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                          |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                        | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume          | 3.216  | 3.504  | 3.612  | 3.614  | 3.616  | 3.473  | 100.0%  | 10    |
  | cinder.upload_volume_to_image | 48.706 | 66.291 | 69.416 | 69.518 | 69.621 | 64.031 | 100.0%  | 10    |
  | cinder.delete_volume          | 0.681  | 1.721  | 3.226  | 3.286  | 3.347  | 1.88   | 100.0%  | 10    |
  | nova.delete_image             | 1.064  | 1.392  | 1.76   | 1.884  | 2.007  | 1.407  | 100.0%  | 10    |
  | total                         | 57.671 | 73.06  | 75.032 | 75.707 | 76.382 | 70.791 | 100.0%  | 10    |
  +-------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 206.246454954
  Full duration: 221.344403028

  test scenario CinderVolumes.create_and_delete_snapshot
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_snapshot | 2.886 | 3.18   | 5.409  | 5.479  | 5.548 | 3.789 | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.442 | 2.892  | 3.051  | 3.111  | 3.172 | 2.875 | 100.0%  | 10    |
  | total                  | 5.432 | 6.063  | 8.28   | 8.355  | 8.429 | 6.664 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 20.3915560246
  Full duration: 49.2419481277

  test scenario CinderVolumes.create_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 3.151 | 3.492  | 3.579  | 3.641  | 3.703 | 3.459 | 100.0%  | 10    |
  | total                | 3.151 | 3.492  | 3.579  | 3.641  | 3.703 | 3.459 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 10.2652549744
  Full duration: 23.4044110775

  test scenario CinderVolumes.create_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 3.221 | 3.489  | 3.632  | 3.639  | 3.647 | 3.448 | 100.0%  | 10    |
  | total                | 3.222 | 3.489  | 3.632  | 3.64   | 3.647 | 3.448 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 10.2576260567
  Full duration: 27.1289498806

  test scenario CinderVolumes.list_volumes
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.list_volumes | 0.347 | 0.409  | 0.467  | 0.49   | 0.514 | 0.416 | 100.0%  | 10    |
  | total               | 0.347 | 0.409  | 0.467  | 0.49   | 0.514 | 0.416 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.25233316422
  Full duration: 60.8991248608

  test scenario CinderVolumes.create_nested_snapshots_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 3.37   | 3.431  | 3.543  | 3.585  | 3.627  | 3.454  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.744  | 2.922  | 2.98   | 2.993  | 3.006  | 2.901  | 100.0%  | 10    |
  | nova.attach_volume     | 4.052  | 4.214  | 6.878  | 6.969  | 7.06   | 4.803  | 100.0%  | 10    |
  | nova.detach_volume     | 3.392  | 3.988  | 4.066  | 4.11   | 4.154  | 3.906  | 100.0%  | 10    |
  | cinder.delete_snapshot | 0.753  | 2.605  | 2.986  | 3.013  | 3.04   | 2.343  | 100.0%  | 10    |
  | cinder.delete_volume   | 0.492  | 2.767  | 2.955  | 3.011  | 3.067  | 1.989  | 100.0%  | 10    |
  | total                  | 16.494 | 20.022 | 23.368 | 23.417 | 23.465 | 20.126 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 59.1712889671
  Full duration: 133.726794958

  test scenario CinderVolumes.create_from_volume_and_delete_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 3.434 | 3.618  | 4.006  | 4.825  | 5.645 | 3.835 | 100.0%  | 10    |
  | cinder.delete_volume | 2.853 | 2.996  | 3.194  | 3.231  | 3.269 | 3.035 | 100.0%  | 10    |
  | total                | 6.323 | 6.672  | 7.143  | 7.89   | 8.637 | 6.87  | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 20.0482749939
  Full duration: 48.4943790436

  test scenario CinderVolumes.create_and_extend_volume
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | cinder.create_volume | 3.242 | 3.547  | 3.574  | 3.574  | 3.575 | 3.477 | 100.0%  | 10    |
  | cinder.extend_volume | 0.67  | 0.904  | 3.113  | 3.227  | 3.341 | 1.343 | 100.0%  | 10    |
  | cinder.delete_volume | 0.756 | 2.645  | 3.074  | 3.111  | 3.147 | 2.224 | 100.0%  | 10    |
  | total                | 5.261 | 7.245  | 7.684  | 8.512  | 9.341 | 7.045 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 21.6863160133
  Full duration: 35.5403769016

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +-----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                      |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 3.427 | 3.543  | 3.82   | 3.829  | 3.838  | 3.59   | 100.0%  | 10    |
  | cinder.create_snapshot | 2.673 | 2.992  | 3.109  | 3.111  | 3.112  | 2.928  | 100.0%  | 10    |
  | nova.attach_volume     | 3.759 | 4.112  | 4.508  | 5.345  | 6.182  | 4.292  | 100.0%  | 10    |
  | nova.detach_volume     | 3.458 | 4.067  | 4.174  | 4.261  | 4.348  | 4.006  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.665 | 2.794  | 2.946  | 2.986  | 3.026  | 2.823  | 100.0%  | 10    |
  | cinder.delete_volume   | 0.707 | 2.907  | 3.246  | 3.257  | 3.268  | 2.558  | 100.0%  | 10    |
  | total                  | 18.87 | 21.068 | 21.909 | 22.497 | 23.086 | 20.904 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 61.3498468399
  Full duration: 141.86026597

  test scenario CinderVolumes.create_snapshot_and_attach_volume
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume   | 2.885  | 3.335  | 3.519  | 3.55   | 3.581  | 3.305  | 100.0%  | 10    |
  | cinder.create_snapshot | 2.609  | 2.889  | 3.002  | 3.021  | 3.041  | 2.853  | 100.0%  | 10    |
  | nova.attach_volume     | 3.794  | 4.368  | 6.443  | 6.495  | 6.548  | 4.951  | 100.0%  | 10    |
  | nova.detach_volume     | 3.341  | 3.93   | 4.07   | 4.11   | 4.15   | 3.862  | 100.0%  | 10    |
  | cinder.delete_snapshot | 2.73   | 2.943  | 3.009  | 3.029  | 3.049  | 2.912  | 100.0%  | 10    |
  | cinder.delete_volume   | 0.667  | 2.901  | 3.015  | 3.027  | 3.039  | 2.437  | 100.0%  | 10    |
  | total                  | 18.717 | 21.217 | 22.919 | 23.013 | 23.108 | 21.377 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 62.8349030018
  Full duration: 143.571810007

  run_rally - INFO - Test scenario: "cinder" OK.

  run_rally - INFO - Starting test scenario "heat" ...
  run_rally - INFO -
   Preparing input task
   Task  1055c160-be9e-4209-9219-2eda388f64ca: started
  Task 1055c160-be9e-4209-9219-2eda388f64ca: finished

  test scenario HeatStacks.create_suspend_resume_delete_stack
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action             | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack  | 3.658 | 4.153  | 4.633  | 4.957  | 5.28  | 4.179 | 100.0%  | 10    |
  | heat.suspend_stack | 0.603 | 0.984  | 1.772  | 1.876  | 1.98  | 1.163 | 100.0%  | 10    |
  | heat.resume_stack  | 0.553 | 1.347  | 2.26   | 2.264  | 2.268 | 1.425 | 100.0%  | 10    |
  | heat.delete_stack  | 1.527 | 1.61   | 1.95   | 1.96   | 1.97  | 1.701 | 100.0%  | 10    |
  | total              | 7.456 | 8.457  | 9.273  | 9.324  | 9.376 | 8.469 | 100.0%  | 10    |
  +--------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 25.1924760342
  Full duration: 31.4871768951

  test scenario HeatStacks.create_and_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 3.724 | 4.253  | 4.355  | 4.361  | 4.366 | 4.141 | 100.0%  | 10    |
  | heat.delete_stack | 1.538 | 1.86   | 2.427  | 2.427  | 2.428 | 1.933 | 100.0%  | 10    |
  | total             | 5.609 | 6.117  | 6.381  | 6.402  | 6.422 | 6.073 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 18.3157711029
  Full duration: 24.7532258034

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 19.874 | 21.385 | 22.341 | 22.535 | 22.729 | 21.343 | 100.0%  | 10    |
  | heat.delete_stack | 10.707 | 11.672 | 12.205 | 12.275 | 12.345 | 11.562 | 100.0%  | 10    |
  | total             | 30.923 | 33.359 | 33.959 | 34.235 | 34.512 | 32.905 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 99.1549890041
  Full duration: 105.660290003

  test scenario HeatStacks.create_and_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 15.572 | 18.262 | 19.048 | 19.088 | 19.127 | 18.071 | 100.0%  | 10    |
  | heat.delete_stack | 10.145 | 10.711 | 11.519 | 11.545 | 11.571 | 10.78  | 100.0%  | 10    |
  | total             | 25.725 | 29.14  | 29.903 | 30.143 | 30.382 | 28.851 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 85.5803580284
  Full duration: 92.0883340836

  test scenario HeatStacks.list_stacks_and_resources
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.list_stacks                | 0.391 | 0.425  | 0.461  | 0.477  | 0.492 | 0.432 | 100.0%  | 10    |
  | heat.list_resources_of_0_stacks | 0.0   | 0.0    | 0.0    | 0.0    | 0.0   | 0.0   | 100.0%  | 10    |
  | total                           | 0.391 | 0.425  | 0.461  | 0.477  | 0.492 | 0.432 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.32646512985
  Full duration: 6.55452680588

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 3.818 | 4.127  | 4.55   | 4.634  | 4.719 | 4.191 | 100.0%  | 10    |
  | heat.update_stack | 2.555 | 3.026  | 3.487  | 3.49   | 3.493 | 2.994 | 100.0%  | 10    |
  | heat.delete_stack | 1.278 | 1.905  | 2.468  | 2.484  | 2.501 | 1.938 | 100.0%  | 10    |
  | total             | 8.59  | 8.987  | 9.575  | 9.58   | 9.585 | 9.123 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 27.2428030968
  Full duration: 34.0842261314

  test scenario HeatStacks.create_update_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 3.817 | 4.322  | 4.498  | 4.571  | 4.643 | 4.268 | 100.0%  | 10    |
  | heat.update_stack | 2.571 | 3.085  | 3.495  | 3.651  | 3.807 | 3.093 | 100.0%  | 10    |
  | heat.delete_stack | 1.261 | 1.933  | 2.188  | 2.23   | 2.271 | 1.85  | 100.0%  | 10    |
  | total             | 8.823 | 9.193  | 9.529  | 9.645  | 9.76  | 9.211 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 27.712323904
  Full duration: 34.6925389767

  test scenario HeatStacks.create_update_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 3.534  | 4.559  | 4.878  | 4.986  | 5.094  | 4.397  | 100.0%  | 10    |
  | heat.update_stack | 4.274  | 4.722  | 5.38   | 5.427  | 5.474  | 4.782  | 100.0%  | 10    |
  | heat.delete_stack | 2.324  | 2.687  | 3.01   | 3.031  | 3.051  | 2.761  | 100.0%  | 10    |
  | total             | 10.398 | 11.879 | 12.749 | 13.064 | 13.379 | 11.941 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 36.5785570145
  Full duration: 43.5735290051

  test scenario HeatStacks.create_update_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 4.244  | 4.341  | 4.695  | 4.992  | 5.29   | 4.489  | 100.0%  | 10    |
  | heat.update_stack | 7.174  | 8.094  | 8.59   | 8.598  | 8.605  | 8.081  | 100.0%  | 10    |
  | heat.delete_stack | 2.663  | 2.892  | 3.804  | 3.808  | 3.813  | 3.088  | 100.0%  | 10    |
  | total             | 15.231 | 15.561 | 16.269 | 16.292 | 16.315 | 15.659 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 46.8214969635
  Full duration: 54.2644329071

  test scenario HeatStacks.create_update_delete_stack
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 4.041  | 4.381  | 4.699  | 4.835  | 4.971  | 4.435  | 100.0%  | 10    |
  | heat.update_stack | 4.032  | 4.694  | 5.611  | 5.758  | 5.906  | 4.82   | 100.0%  | 10    |
  | heat.delete_stack | 2.715  | 3.034  | 3.306  | 3.315  | 3.324  | 3.036  | 100.0%  | 10    |
  | total             | 11.427 | 12.204 | 13.196 | 13.241 | 13.286 | 12.292 | 100.0%  | 10    |
  +-------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 37.1505100727
  Full duration: 44.6821551323

  test scenario HeatStacks.create_update_delete_stack
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  | heat.create_stack | 3.692 | 4.397  | 4.751  | 4.908  | 5.065  | 4.428  | 100.0%  | 10    |
  | heat.update_stack | 3.631 | 4.037  | 4.866  | 4.875  | 4.885  | 4.167  | 100.0%  | 10    |
  | heat.delete_stack | 1.267 | 1.966  | 2.279  | 2.33   | 2.382  | 1.871  | 100.0%  | 10    |
  | total             | 9.823 | 10.45  | 11.136 | 11.248 | 11.361 | 10.466 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 31.3539619446
  Full duration: 39.0203011036

  test scenario HeatStacks.create_and_list_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 4.039 | 4.653  | 4.788  | 4.792  | 4.796 | 4.563 | 100.0%  | 10    |
  | heat.list_stacks  | 0.052 | 0.39   | 0.447  | 0.461  | 0.474 | 0.339 | 100.0%  | 10    |
  | total             | 4.106 | 4.992  | 5.218  | 5.244  | 5.27  | 4.902 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.8402919769
  Full duration: 27.3945071697

  test scenario HeatStacks.create_check_delete_stack
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | heat.create_stack | 3.744 | 4.489  | 4.836  | 4.864  | 4.891 | 4.475 | 100.0%  | 10    |
  | heat.check_stack  | 0.612 | 1.265  | 1.684  | 1.853  | 2.022 | 1.261 | 100.0%  | 10    |
  | heat.delete_stack | 1.272 | 1.804  | 2.077  | 2.209  | 2.342 | 1.813 | 100.0%  | 10    |
  | total             | 6.355 | 7.754  | 8.128  | 8.148  | 8.168 | 7.55  | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 23.1206851006
  Full duration: 31.1694560051

  run_rally - INFO - Test scenario: "heat" OK.

  run_rally - INFO - Starting test scenario "keystone" ...
  run_rally - INFO -
   Preparing input task
   Task  897d895f-d779-44a7-bb9b-0e66854f43da: started
  Task 897d895f-d779-44a7-bb9b-0e66854f43da: finished

  test scenario KeystoneBasic.create_tenant_with_users
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.199 | 0.225  | 0.245  | 0.26   | 0.274 | 0.227 | 100.0%  | 10    |
  | keystone.create_users  | 1.448 | 1.551  | 1.618  | 1.62   | 1.621 | 1.544 | 100.0%  | 10    |
  | total                  | 1.702 | 1.78   | 1.819  | 1.83   | 1.842 | 1.772 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 5.34110379219
  Full duration: 17.6792171001

  test scenario KeystoneBasic.create_add_and_list_user_roles
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.206 | 0.231  | 0.279  | 0.28   | 0.281 | 0.238 | 100.0%  | 10    |
  | keystone.add_role    | 0.248 | 0.256  | 0.3    | 0.314  | 0.328 | 0.269 | 100.0%  | 10    |
  | keystone.list_roles  | 0.133 | 0.143  | 0.175  | 0.182  | 0.189 | 0.149 | 100.0%  | 10    |
  | total                | 0.596 | 0.655  | 0.689  | 0.719  | 0.75  | 0.657 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.96121311188
  Full duration: 11.1928119659

  test scenario KeystoneBasic.add_and_remove_user_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.201 | 0.224  | 0.231  | 0.232  | 0.233 | 0.22  | 100.0%  | 10    |
  | keystone.add_role    | 0.245 | 0.259  | 0.287  | 0.295  | 0.304 | 0.265 | 100.0%  | 10    |
  | keystone.remove_role | 0.137 | 0.148  | 0.164  | 0.172  | 0.18  | 0.15  | 100.0%  | 10    |
  | total                | 0.605 | 0.631  | 0.668  | 0.673  | 0.679 | 0.635 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.9179649353
  Full duration: 11.3398149014

  test scenario KeystoneBasic.create_update_and_delete_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.204 | 0.23   | 0.249  | 0.262  | 0.276 | 0.234 | 100.0%  | 10    |
  | keystone.update_tenant | 0.134 | 0.136  | 0.178  | 0.179  | 0.18  | 0.148 | 100.0%  | 10    |
  | keystone.delete_tenant | 0.288 | 0.308  | 0.353  | 0.36   | 0.367 | 0.316 | 100.0%  | 10    |
  | total                  | 0.653 | 0.684  | 0.749  | 0.761  | 0.774 | 0.698 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.11506795883
  Full duration: 10.1015338898

  test scenario KeystoneBasic.create_and_delete_service
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                  | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_service | 0.223 | 0.237  | 0.288  | 0.289  | 0.29  | 0.245 | 100.0%  | 10    |
  | keystone.delete_service | 0.14  | 0.152  | 0.165  | 0.175  | 0.185 | 0.154 | 100.0%  | 10    |
  | total                   | 0.373 | 0.389  | 0.43   | 0.442  | 0.453 | 0.399 | 100.0%  | 10    |
  +-------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.24712610245
  Full duration: 9.40017700195

  test scenario KeystoneBasic.create_tenant
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.219 | 0.235  | 0.25   | 0.263  | 0.277 | 0.238 | 100.0%  | 10    |
  | total                  | 0.219 | 0.236  | 0.25   | 0.263  | 0.277 | 0.238 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.738801002502
  Full duration: 6.97619819641

  test scenario KeystoneBasic.create_user
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.242 | 0.253  | 0.272  | 0.28   | 0.288 | 0.257 | 100.0%  | 10    |
  | total                | 0.242 | 0.253  | 0.272  | 0.28   | 0.288 | 0.258 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.813333034515
  Full duration: 7.2009499073

  test scenario KeystoneBasic.create_and_list_tenants
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.215 | 0.241  | 0.264  | 0.277  | 0.289 | 0.245 | 100.0%  | 10    |
  | keystone.list_tenants  | 0.128 | 0.136  | 0.183  | 0.202  | 0.22  | 0.151 | 100.0%  | 10    |
  | total                  | 0.366 | 0.388  | 0.425  | 0.44   | 0.455 | 0.396 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.19499707222
  Full duration: 10.8357591629

  test scenario KeystoneBasic.create_and_delete_role
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.231 | 0.252  | 0.281  | 0.294  | 0.307 | 0.258 | 100.0%  | 10    |
  | keystone.delete_role | 0.28  | 0.293  | 0.399  | 0.418  | 0.437 | 0.329 | 100.0%  | 10    |
  | total                | 0.511 | 0.579  | 0.676  | 0.69   | 0.704 | 0.587 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.80924010277
  Full duration: 10.1753411293

  test scenario KeystoneBasic.get_entities
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_tenant | 0.24  | 0.257  | 0.281  | 0.283  | 0.284 | 0.258 | 100.0%  | 10    |
  | keystone.create_user   | 0.15  | 0.164  | 0.206  | 0.206  | 0.206 | 0.171 | 100.0%  | 10    |
  | keystone.create_role   | 0.13  | 0.136  | 0.143  | 0.159  | 0.176 | 0.139 | 100.0%  | 10    |
  | keystone.get_tenant    | 0.13  | 0.138  | 0.141  | 0.143  | 0.146 | 0.137 | 100.0%  | 10    |
  | keystone.get_user      | 0.112 | 0.132  | 0.137  | 0.137  | 0.137 | 0.131 | 100.0%  | 10    |
  | keystone.get_role      | 0.129 | 0.133  | 0.139  | 0.156  | 0.174 | 0.137 | 100.0%  | 10    |
  | keystone.service_list  | 0.129 | 0.132  | 0.135  | 0.137  | 0.138 | 0.133 | 100.0%  | 10    |
  | keystone.get_service   | 0.132 | 0.135  | 0.178  | 0.178  | 0.178 | 0.147 | 100.0%  | 10    |
  | total                  | 1.204 | 1.22   | 1.323  | 1.328  | 1.332 | 1.252 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.79558706284
  Full duration: 16.6252310276

  test scenario KeystoneBasic.create_and_list_users
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_user | 0.239 | 0.266  | 0.295  | 0.298  | 0.301 | 0.27  | 100.0%  | 10    |
  | keystone.list_users  | 0.137 | 0.143  | 0.186  | 0.211  | 0.235 | 0.157 | 100.0%  | 10    |
  | total                | 0.397 | 0.419  | 0.448  | 0.474  | 0.5   | 0.427 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.30778193474
  Full duration: 8.03108906746

  run_rally - INFO - Test scenario: "keystone" OK.

  run_rally - INFO - Starting test scenario "neutron" ...
  run_rally - INFO -
   Preparing input task
   Task  6e4f3aaf-b5ee-4eeb-8ac3-057f7b4d6309: started
  Task 6e4f3aaf-b5ee-4eeb-8ac3-057f7b4d6309: finished

  test scenario NeutronNetworks.create_and_delete_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.806 | 0.859  | 0.937  | 0.938  | 0.939 | 0.873 | 100.0%  | 10    |
  | neutron.delete_port | 0.202 | 0.689  | 0.761  | 0.777  | 0.794 | 0.529 | 100.0%  | 10    |
  | total               | 1.023 | 1.572  | 1.686  | 1.703  | 1.72  | 1.401 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.3307390213
  Full duration: 57.6386358738

  test scenario NeutronNetworks.create_and_list_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.739 | 0.817  | 0.85   | 0.861  | 0.871 | 0.812 | 100.0%  | 10    |
  | neutron.create_router        | 0.079 | 0.545  | 0.57   | 0.584  | 0.598 | 0.499 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.348 | 0.89   | 0.978  | 0.986  | 0.994 | 0.793 | 100.0%  | 10    |
  | neutron.list_routers         | 0.047 | 0.566  | 0.607  | 0.612  | 0.617 | 0.515 | 100.0%  | 10    |
  | total                        | 2.172 | 2.707  | 2.868  | 2.88   | 2.891 | 2.618 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 7.91338610649
  Full duration: 64.1935119629

  test scenario NeutronNetworks.create_and_delete_routers
  +------------------------------------------------------------------------------------------------------+
  |                                         Response Times (sec)                                         |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                          | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet           | 0.769 | 0.8    | 0.846  | 0.881  | 0.915 | 0.809 | 100.0%  | 10    |
  | neutron.create_router           | 0.488 | 0.528  | 0.576  | 0.615  | 0.653 | 0.539 | 100.0%  | 10    |
  | neutron.add_interface_router    | 0.839 | 0.882  | 0.983  | 0.985  | 0.987 | 0.901 | 100.0%  | 10    |
  | neutron.remove_interface_router | 0.343 | 0.809  | 0.898  | 0.906  | 0.913 | 0.763 | 100.0%  | 10    |
  | neutron.delete_router           | 0.614 | 0.686  | 0.787  | 0.849  | 0.912 | 0.708 | 100.0%  | 10    |
  | total                           | 3.419 | 3.666  | 3.994  | 3.997  | 3.999 | 3.719 | 100.0%  | 10    |
  +---------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 11.0299580097
  Full duration: 65.4096131325

  test scenario NeutronNetworks.create_and_list_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.83  | 0.888  | 0.995  | 1.184  | 1.372 | 0.935 | 100.0%  | 10    |
  | neutron.list_ports  | 0.554 | 0.625  | 0.697  | 0.704  | 0.712 | 0.626 | 100.0%  | 10    |
  | total               | 1.405 | 1.487  | 1.692  | 1.888  | 2.084 | 1.562 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 5.07633280754
  Full duration: 59.1840729713

  test scenario NeutronNetworks.create_and_delete_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.731 | 0.806  | 0.857  | 0.933  | 1.01  | 0.812 | 100.0%  | 10    |
  | neutron.delete_subnet | 0.183 | 0.688  | 0.872  | 0.918  | 0.965 | 0.691 | 100.0%  | 10    |
  | total                 | 0.948 | 1.544  | 1.665  | 1.681  | 1.696 | 1.503 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.69728302956
  Full duration: 58.486093998

  test scenario NeutronNetworks.create_and_delete_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.641 | 0.686  | 0.757  | 0.82   | 0.883 | 0.707 | 100.0%  | 10    |
  | neutron.delete_network | 0.158 | 0.632  | 0.656  | 0.665  | 0.674 | 0.585 | 100.0%  | 10    |
  | total                  | 0.901 | 1.305  | 1.424  | 1.469  | 1.514 | 1.292 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.96865105629
  Full duration: 36.4033529758

  test scenario NeutronNetworks.create_and_list_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.634 | 0.679  | 0.751  | 0.797  | 0.844 | 0.695 | 100.0%  | 10    |
  | neutron.list_networks  | 0.472 | 0.522  | 0.552  | 0.555  | 0.557 | 0.521 | 100.0%  | 10    |
  | total                  | 1.154 | 1.192  | 1.284  | 1.327  | 1.369 | 1.216 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.68979907036
  Full duration: 38.8585669994

  test scenario NeutronNetworks.create_and_update_routers
  +---------------------------------------------------------------------------------------------------+
  |                                       Response Times (sec)                                        |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                       | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet        | 0.759 | 0.82   | 0.863  | 0.871  | 0.879 | 0.819 | 100.0%  | 10    |
  | neutron.create_router        | 0.518 | 0.558  | 0.62   | 0.627  | 0.634 | 0.566 | 100.0%  | 10    |
  | neutron.add_interface_router | 0.465 | 0.878  | 1.032  | 1.081  | 1.13  | 0.879 | 100.0%  | 10    |
  | neutron.update_router        | 0.158 | 0.636  | 0.722  | 0.73   | 0.737 | 0.564 | 100.0%  | 10    |
  | total                        | 2.298 | 2.877  | 3.13   | 3.178  | 3.226 | 2.827 | 100.0%  | 10    |
  +------------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 8.47763490677
  Full duration: 62.3842899799

  test scenario NeutronNetworks.create_and_update_networks
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_network | 0.627 | 0.673  | 0.974  | 1.044  | 1.114 | 0.744 | 100.0%  | 10    |
  | neutron.update_network | 0.153 | 0.605  | 0.623  | 0.626  | 0.629 | 0.564 | 100.0%  | 10    |
  | total                  | 0.809 | 1.285  | 1.576  | 1.65   | 1.723 | 1.308 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.00336408615
  Full duration: 38.2563900948

  test scenario NeutronNetworks.create_and_update_ports
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_port | 0.796 | 0.874  | 1.084  | 1.1    | 1.116 | 0.908 | 100.0%  | 10    |
  | neutron.update_port | 0.595 | 0.622  | 0.697  | 0.76   | 0.823 | 0.646 | 100.0%  | 10    |
  | total               | 1.44  | 1.497  | 1.737  | 1.82   | 1.904 | 1.554 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.89373588562
  Full duration: 57.0287640095

  test scenario NeutronNetworks.create_and_list_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.706 | 0.775  | 0.866  | 0.893  | 0.92  | 0.789 | 100.0%  | 10    |
  | neutron.list_subnets  | 0.487 | 0.519  | 0.53   | 0.54   | 0.55  | 0.517 | 100.0%  | 10    |
  | total                 | 1.233 | 1.291  | 1.393  | 1.414  | 1.435 | 1.307 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.97321105003
  Full duration: 55.8097410202

  test scenario NeutronNetworks.create_and_update_subnets
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | neutron.create_subnet | 0.72  | 0.834  | 0.873  | 0.905  | 0.936 | 0.819 | 100.0%  | 10    |
  | neutron.update_subnet | 0.24  | 0.66   | 0.83   | 0.838  | 0.847 | 0.61  | 100.0%  | 10    |
  | total                 | 1.098 | 1.433  | 1.66   | 1.686  | 1.713 | 1.429 | 100.0%  | 10    |
  +-----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.11318302155
  Full duration: 55.0307190418

  run_rally - INFO - Test scenario: "neutron" OK.

  run_rally - INFO - Starting test scenario "nova" ...
  run_rally - INFO -
   Preparing input task
   Task  52be10f0-6365-4abd-8a9b-5f626b8c2e7a: started
  Task 52be10f0-6365-4abd-8a9b-5f626b8c2e7a: finished

  test scenario NovaKeypair.create_and_delete_keypair
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.695 | 0.769  | 0.948  | 0.991  | 1.035 | 0.816 | 100.0%  | 10    |
  | nova.delete_keypair | 0.017 | 0.453  | 0.499  | 0.551  | 0.604 | 0.423 | 100.0%  | 10    |
  | total               | 0.944 | 1.187  | 1.524  | 1.533  | 1.542 | 1.239 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.69359993935
  Full duration: 34.1216721535

  test scenario NovaServers.snapshot_server
  +------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                      |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                 | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server       | 6.466  | 7.619  | 9.603  | 9.617  | 9.63   | 7.898  | 100.0%  | 10    |
  | nova.create_image      | 7.251  | 8.663  | 10.95  | 11.033 | 11.116 | 8.905  | 100.0%  | 10    |
  | nova.delete_server     | 2.865  | 4.177  | 4.352  | 4.362  | 4.373  | 3.878  | 100.0%  | 10    |
  | nova.boot_server (2)   | 7.263  | 7.636  | 9.053  | 9.177  | 9.301  | 7.965  | 100.0%  | 10    |
  | nova.delete_server (2) | 2.41   | 3.487  | 3.939  | 4.129  | 4.318  | 3.406  | 100.0%  | 10    |
  | nova.delete_image      | 2.217  | 3.339  | 3.856  | 3.864  | 3.873  | 3.205  | 100.0%  | 10    |
  | total                  | 32.246 | 34.577 | 37.931 | 38.819 | 39.707 | 35.259 | 100.0%  | 10    |
  +------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 104.138304949
  Full duration: 162.17621994

  test scenario NovaKeypair.boot_and_delete_server_with_keypair
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_keypair | 0.717  | 0.776  | 0.905  | 0.916  | 0.927  | 0.799  | 100.0%  | 10    |
  | nova.boot_server    | 5.96   | 7.356  | 9.573  | 9.701  | 9.829  | 7.641  | 100.0%  | 10    |
  | nova.delete_server  | 3.226  | 3.979  | 4.24   | 4.272  | 4.305  | 3.929  | 100.0%  | 10    |
  | nova.delete_keypair | 0.018  | 0.446  | 0.498  | 0.498  | 0.498  | 0.375  | 100.0%  | 10    |
  | total               | 11.513 | 12.362 | 14.5   | 14.767 | 15.033 | 12.746 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 37.7138030529
  Full duration: 95.0321340561

  test scenario NovaKeypair.create_and_list_keypairs
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 0.706 | 0.754  | 0.859  | 0.881  | 0.904 | 0.766 | 100.0%  | 10    |
  | nova.list_keypairs  | 0.021 | 0.458  | 0.489  | 0.492  | 0.495 | 0.412 | 100.0%  | 10    |
  | total               | 0.767 | 1.195  | 1.282  | 1.326  | 1.371 | 1.178 | 100.0%  | 10    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.66450190544
  Full duration: 35.3121151924

  test scenario NovaServers.list_servers
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.list_servers | 1.158 | 1.197  | 1.257  | 1.26   | 1.263 | 1.207 | 100.0%  | 10    |
  | total             | 1.158 | 1.197  | 1.257  | 1.26   | 1.263 | 1.207 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.67958188057
  Full duration: 102.272238016

  test scenario NovaServers.resize_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 6.482  | 7.414  | 8.638  | 9.129  | 9.619  | 7.594  | 100.0%  | 10    |
  | nova.resize         | 12.87  | 13.632 | 13.841 | 14.061 | 14.281 | 13.519 | 100.0%  | 10    |
  | nova.resize_confirm | 3.854  | 4.236  | 4.429  | 4.579  | 4.729  | 4.184  | 100.0%  | 10    |
  | nova.delete_server  | 2.853  | 3.971  | 4.187  | 4.209  | 4.231  | 3.798  | 100.0%  | 10    |
  | total               | 27.866 | 29.013 | 29.93  | 30.646 | 31.361 | 29.095 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 86.1472420692
  Full duration: 116.147330999

  test scenario NovaServers.boot_server_from_volume_and_delete
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 7.809  | 9.646  | 10.21  | 10.4   | 10.59  | 9.268  | 100.0%  | 10    |
  | nova.boot_server     | 7.938  | 9.663  | 10.373 | 10.451 | 10.528 | 9.379  | 100.0%  | 10    |
  | nova.delete_server   | 3.263  | 4.164  | 4.323  | 4.341  | 4.359  | 3.965  | 100.0%  | 10    |
  | total                | 21.009 | 22.166 | 24.464 | 24.608 | 24.752 | 22.612 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 65.8047540188
  Full duration: 133.871994019

  test scenario NovaServers.boot_and_migrate_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 6.526  | 7.611  | 9.253  | 9.328  | 9.404  | 7.939  | 100.0%  | 10    |
  | nova.stop_server    | 3.956  | 4.801  | 7.753  | 7.839  | 7.924  | 5.676  | 100.0%  | 10    |
  | nova.migrate        | 9.278  | 9.686  | 10.387 | 10.401 | 10.415 | 9.75   | 100.0%  | 10    |
  | nova.resize_confirm | 3.763  | 4.624  | 4.769  | 4.775  | 4.781  | 4.457  | 100.0%  | 10    |
  | nova.delete_server  | 3.333  | 3.772  | 4.263  | 4.388  | 4.514  | 3.895  | 100.0%  | 10    |
  | total               | 28.369 | 30.746 | 35.217 | 35.664 | 36.111 | 31.718 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 95.1431679726
  Full duration: 124.915132999

  test scenario NovaServers.boot_and_delete_server
  +--------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                    |
  +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action             | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server   | 7.051  | 7.863  | 9.774  | 9.886  | 9.999  | 8.295  | 100.0%  | 10    |
  | nova.delete_server | 2.506  | 4.173  | 4.427  | 5.12   | 5.813  | 4.06   | 100.0%  | 10    |
  | total              | 10.355 | 11.708 | 14.201 | 15.006 | 15.812 | 12.355 | 100.0%  | 10    |
  +--------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 36.3530268669
  Full duration: 92.853083849

  test scenario NovaServers.boot_and_rebuild_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 6.552  | 7.699  | 10.036 | 10.113 | 10.19  | 8.371  | 100.0%  | 10    |
  | nova.rebuild_server | 9.522  | 11.78  | 13.651 | 13.906 | 14.162 | 11.746 | 100.0%  | 10    |
  | nova.delete_server  | 3.327  | 4.064  | 4.61   | 4.82   | 5.03   | 4.065  | 100.0%  | 10    |
  | total               | 19.511 | 25.224 | 26.458 | 26.522 | 26.586 | 24.182 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 73.8343379498
  Full duration: 129.419740915

  test scenario NovaSecGroup.create_and_list_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 6.563  | 9.397  | 10.161 | 10.173 | 10.185 | 8.839  | 100.0%  | 10    |
  | nova.create_100_rules          | 45.018 | 49.294 | 56.133 | 56.18  | 56.227 | 50.472 | 100.0%  | 10    |
  | nova.list_security_groups      | 0.111  | 0.217  | 0.579  | 0.601  | 0.623  | 0.264  | 100.0%  | 10    |
  | total                          | 52.204 | 58.754 | 65.138 | 65.785 | 66.433 | 59.576 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 179.173851967
  Full duration: 240.213445902

  test scenario NovaSecGroup.create_and_delete_secgroups
  +--------------------------------------------------------------------------------------------------------+
  |                                          Response Times (sec)                                          |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                         | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups | 7.358  | 9.711  | 10.153 | 10.476 | 10.798 | 9.428  | 100.0%  | 10    |
  | nova.create_100_rules          | 47.694 | 51.106 | 54.599 | 55.137 | 55.674 | 51.004 | 100.0%  | 10    |
  | nova.delete_10_security_groups | 1.777  | 3.576  | 4.456  | 4.736  | 5.016  | 3.515  | 100.0%  | 10    |
  | total                          | 59.615 | 63.877 | 66.262 | 66.848 | 67.435 | 63.947 | 100.0%  | 10    |
  +--------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 191.541640997
  Full duration: 222.269508839

  test scenario NovaServers.boot_and_bounce_server
  +-------------------------------------------------------------------------------------------------+
  |                                      Response Times (sec)                                       |
  +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                  | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server        | 7.313  | 7.988  | 8.758  | 9.045  | 9.331  | 8.15   | 100.0%  | 10    |
  | nova.reboot_server      | 5.889  | 6.906  | 7.056  | 7.078  | 7.101  | 6.624  | 100.0%  | 10    |
  | nova.soft_reboot_server | 6.349  | 6.773  | 8.096  | 8.126  | 8.156  | 6.947  | 100.0%  | 10    |
  | nova.stop_server        | 4.4    | 5.425  | 6.714  | 7.318  | 7.922  | 5.67   | 100.0%  | 10    |
  | nova.start_server       | 2.424  | 4.059  | 5.269  | 5.417  | 5.564  | 4.057  | 100.0%  | 10    |
  | nova.rescue_server      | 8.473  | 9.131  | 9.695  | 9.957  | 10.219 | 9.177  | 100.0%  | 10    |
  | nova.unrescue_server    | 2.688  | 5.82   | 6.893  | 6.92   | 6.948  | 5.504  | 100.0%  | 10    |
  | nova.delete_server      | 3.393  | 3.812  | 4.417  | 4.473  | 4.53   | 3.858  | 100.0%  | 10    |
  | total                   | 47.129 | 50.214 | 51.652 | 52.087 | 52.523 | 50.006 | 100.0%  | 10    |
  +-------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 150.170030117
  Full duration: 206.320158958

  test scenario NovaServers.boot_server
  +----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                  |
  +------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action           | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | nova.boot_server | 7.775 | 8.214  | 9.964  | 10.061 | 10.157 | 8.648 | 100.0%  | 10    |
  | total            | 7.775 | 8.214  | 9.965  | 10.061 | 10.157 | 8.649 | 100.0%  | 10    |
  +------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 25.5615310669
  Full duration: 72.0356788635

  test scenario NovaSecGroup.boot_and_delete_server_with_secgroups
  +-----------------------------------------------------------------------------------------------------------+
  |                                           Response Times (sec)                                            |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action                            | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.create_10_security_groups    | 7.852  | 9.225  | 10.298 | 10.398 | 10.498 | 9.327  | 100.0%  | 10    |
  | nova.create_100_rules             | 45.734 | 50.042 | 52.231 | 53.454 | 54.678 | 49.891 | 100.0%  | 10    |
  | nova.boot_server                  | 5.843  | 6.686  | 7.412  | 7.548  | 7.683  | 6.632  | 100.0%  | 10    |
  | nova.get_attached_security_groups | 0.173  | 0.215  | 0.678  | 0.757  | 0.836  | 0.311  | 100.0%  | 10    |
  | nova.delete_server                | 2.437  | 2.94   | 3.313  | 3.412  | 3.512  | 2.92   | 100.0%  | 10    |
  | nova.delete_10_security_groups    | 2.172  | 3.217  | 4.733  | 5.576  | 6.419  | 3.474  | 100.0%  | 10    |
  | total                             | 67.914 | 73.688 | 75.248 | 75.466 | 75.684 | 72.556 | 100.0%  | 10    |
  +-----------------------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 217.134851933
  Full duration: 273.106995821

  test scenario NovaServers.pause_and_unpause_server
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action              | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | nova.boot_server    | 7.355  | 8.061  | 9.184  | 9.727  | 10.271 | 8.306  | 100.0%  | 10    |
  | nova.pause_server   | 2.766  | 3.437  | 3.779  | 3.807  | 3.836  | 3.361  | 100.0%  | 10    |
  | nova.unpause_server | 2.762  | 3.685  | 3.988  | 4.013  | 4.037  | 3.492  | 100.0%  | 10    |
  | nova.delete_server  | 2.835  | 3.909  | 4.299  | 4.343  | 4.387  | 3.776  | 100.0%  | 10    |
  | total               | 16.602 | 18.903 | 20.184 | 20.456 | 20.729 | 18.936 | 100.0%  | 10    |
  +---------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 57.0698840618
  Full duration: 114.94224596

  test scenario NovaServers.boot_server_from_volume
  +----------------------------------------------------------------------------------------------+
  |                                     Response Times (sec)                                     |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | action               | min    | median | 90%ile | 95%ile | max    | avg    | success | count |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  | cinder.create_volume | 7.772  | 10.48  | 10.909 | 11.031 | 11.154 | 9.647  | 100.0%  | 10    |
  | nova.boot_server     | 8.129  | 9.825  | 11.137 | 11.167 | 11.196 | 9.722  | 100.0%  | 10    |
  | total                | 16.389 | 19.221 | 21.482 | 21.884 | 22.285 | 19.369 | 100.0%  | 10    |
  +----------------------+--------+--------+--------+--------+--------+--------+---------+-------+
  Load duration: 57.2666420937
  Full duration: 114.729999065

  test scenario NovaServers.boot_and_list_server
  +-----------------------------------------------------------------------------------------+
  |                                  Response Times (sec)                                   |
  +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | action            | min   | median | 90%ile | 95%ile | max    | avg   | success | count |
  +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  | nova.boot_server  | 7.43  | 8.747  | 9.88   | 10.022 | 10.163 | 8.832 | 100.0%  | 10    |
  | nova.list_servers | 0.267 | 1.207  | 1.259  | 1.275  | 1.29   | 1.04  | 100.0%  | 10    |
  | total             | 8.602 | 9.378  | 11.07  | 11.227 | 11.384 | 9.873 | 100.0%  | 10    |
  +-------------------+-------+--------+--------+--------+--------+-------+---------+-------+
  Load duration: 29.5450980663
  Full duration: 106.656322002

  run_rally - INFO - Test scenario: "nova" OK.

  run_rally - INFO - Starting test scenario "quotas" ...
  run_rally - INFO -
   Preparing input task
   Task  dcebd6f2-6fd1-4d5d-8d66-445030082b6c: started
  Task dcebd6f2-6fd1-4d5d-8d66-445030082b6c: finished

  test scenario Quotas.cinder_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 1.163 | 1.265  | 1.531  | 1.556  | 1.581 | 1.345 | 100.0%  | 10    |
  | total                | 1.163 | 1.265  | 1.531  | 1.556  | 1.581 | 1.345 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 4.06574201584
  Full duration: 14.4119129181

  test scenario Quotas.neutron_update
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.498 | 0.56   | 0.589  | 0.591  | 0.593 | 0.558 | 100.0%  | 10    |
  | total                | 0.62  | 0.66   | 0.701  | 0.702  | 0.703 | 0.667 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 2.05467915535
  Full duration: 11.7390589714

  test scenario Quotas.cinder_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 1.19  | 1.288  | 1.399  | 1.415  | 1.432 | 1.303 | 100.0%  | 10    |
  | quotas.delete_quotas | 0.531 | 1.107  | 1.208  | 1.235  | 1.262 | 1.062 | 100.0%  | 10    |
  | total                | 1.779 | 2.435  | 2.535  | 2.549  | 2.562 | 2.365 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 7.07872509956
  Full duration: 17.2571020126

  test scenario Quotas.nova_update_and_delete
  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | quotas.update_quotas | 0.669 | 0.708  | 0.732  | 0.745  | 0.757 | 0.703 | 100.0%  | 10    |
  | quotas.delete_quotas | 0.02  | 0.508  | 0.557  | 0.558  | 0.559 | 0.466 | 100.0%  | 10    |
  | total                | 0.727 | 1.212  | 1.275  | 1.28   | 1.285 | 1.169 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 3.64670991898
  Full duration: 13.1532580853

  test scenario Quotas.nova_update
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max  | avg   | success | count |
  +----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  | quotas.update_quotas | 0.652 | 0.726  | 0.761  | 0.766  | 0.77 | 0.722 | 100.0%  | 10    |
  | total                | 0.652 | 0.727  | 0.762  | 0.766  | 0.77 | 0.722 | 100.0%  | 10    |
  +----------------------+-------+--------+--------+--------+------+-------+---------+-------+
  Load duration: 2.22018194199
  Full duration: 11.9367260933

  run_rally - INFO - Test scenario: "quotas" OK.

  run_rally - INFO - Starting test scenario "requests" ...
  run_rally - INFO -
   Preparing input task
   Task  89de006e-a4fd-4526-9211-477075f8e5fc: started
  Task 89de006e-a4fd-4526-9211-477075f8e5fc: finished

  test scenario HttpRequests.check_random_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 0.184 | 0.456  | 1.019  | 1.022  | 1.026 | 0.555 | 100.0%  | 10    |
  | total                  | 0.184 | 0.456  | 1.02   | 1.023  | 1.026 | 0.555 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 1.69973492622
  Full duration: 5.72609114647

  test scenario HttpRequests.check_request
  +---------------------------------------------------------------------------------------------+
  |                                    Response Times (sec)                                     |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action                 | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | requests.check_request | 0.185 | 0.189  | 0.191  | 0.194  | 0.197 | 0.189 | 100.0%  | 10    |
  | total                  | 0.185 | 0.189  | 0.191  | 0.194  | 0.197 | 0.189 | 100.0%  | 10    |
  +------------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 0.616016864777
  Full duration: 4.89253997803

  run_rally - INFO - Test scenario: "requests" OK.

  run_rally - INFO -

                       Rally Summary Report
  +===================+============+===============+===========+
  | Module            | Duration   | nb. Test Run  | Success   |
  +===================+============+===============+===========+
  | authenticate      | 00:35      | 10            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | glance            | 02:20      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | cinder            | 19:44      | 50            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | heat              | 09:29      | 35            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | keystone          | 01:59      | 29            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | neutron           | 10:48      | 31            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | nova              | 39:36      | 61            | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | quotas            | 01:08      | 7             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  | requests          | 00:10      | 2             | 100.00%   |
  +-------------------+------------+---------------+-----------+
  +===================+============+===============+===========+
  | TOTAL:            | 01:25:53   | 232           | 100.00%   |
  +===================+============+===============+===========+


SDN Controller
--------------

ODL
^^^
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


Feature tests
-------------

Promise
^^^^^^^
::

  FUNCTEST.info: Running PROMISE test case...
  Promise- INFO - Creating tenant 'promise'...
  Promise- INFO - Adding role 'eed9b04b536646c994679496e7b653cc' to tenant 'promise'...
  Promise- INFO - Creating user 'promiser'...
  Promise- INFO - Updating OpenStack credentials...
  Promise- INFO - Creating image 'promise-img' from '/home/opnfv/functest/data/cirros-0.3.4-x86_64-disk.img'...
  Promise- INFO - Creating flavor 'promise-flavor'...
  Promise- INFO - Exporting environment variables...
  Promise- INFO - Running command: npm run -s test -- --reporter json
  Promise- INFO - The test succeeded.
  {
    "stats": {
      "suites": 23,
      "tests": 33,
      "passes": 33,
      "pending": 0,
      "failures": 0,
      "start": "2016-02-23T10:44:37.402Z",
      "end": "2016-02-23T10:44:42.006Z",
      "duration": 4604
    },
    "tests": [
      {
        "title": "should add a new OpenStack provider without error",
        "fullTitle": "promise register OpenStack into resource pool add-provider should add a new OpenStack provider without error",
        "duration": 1171,
        "err": {}
      },
      {
        "title": "should update promise.providers with a new entry",
        "fullTitle": "promise register OpenStack into resource pool add-provider should update promise.providers with a new entry",
        "duration": 7,
        "err": {}
      },
      {
        "title": "should contain a new ResourceProvider record in the store",
        "fullTitle": "promise register OpenStack into resource pool add-provider should contain a new ResourceProvider record in the store",
        "duration": 1,
        "err": {}
      },
      {
        "title": "should add more capacity to the reservation service without error",
        "fullTitle": "promise register OpenStack into resource pool increase-capacity should add more capacity to the reservation service without error",
        "duration": 29,
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
        "duration": 23,
        "err": {}
      },
      {
        "title": "should contain newly added capacity pool",
        "fullTitle": "promise register OpenStack into resource pool query-capacity should contain newly added capacity pool",
        "duration": 13,
        "err": {}
      },
      {
        "title": "should create a new server in target provider without error",
        "fullTitle": "promise allocation without reservation create-instance should create a new server in target provider without error",
        "duration": 1144,
        "err": {}
      },
      {
        "title": "should update promise.allocations with a new entry",
        "fullTitle": "promise allocation without reservation create-instance should update promise.allocations with a new entry",
        "duration": 3,
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
        "duration": 0,
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
        "duration": 71,
        "err": {}
      },
      {
        "title": "should update promise.reservations with a new entry",
        "fullTitle": "promise allocation using reservation for immediate use create-reservation should update promise.reservations with a new entry",
        "duration": 9,
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
        "duration": 1025,
        "err": {}
      },
      {
        "title": "should contain a new ResourceAllocation record in the store",
        "fullTitle": "promise allocation using reservation for immediate use create-instance should contain a new ResourceAllocation record in the store",
        "duration": 0,
        "err": {}
      },
      {
        "title": "should be referenced in the reservation record",
        "fullTitle": "promise allocation using reservation for immediate use create-instance should be referenced in the reservation record",
        "duration": 5,
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
        "duration": 125,
        "err": {}
      },
      {
        "title": "should update promise.reservations with a new entry",
        "fullTitle": "promise reservation for future use create-reservation should update promise.reservations with a new entry",
        "duration": 18,
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
        "duration": 74,
        "err": {}
      },
      {
        "title": "should modify existing reservation without error",
        "fullTitle": "promise reservation for future use update-reservation should modify existing reservation without error",
        "duration": 88,
        "err": {}
      },
      {
        "title": "should modify existing reservation without error",
        "fullTitle": "promise reservation for future use cancel-reservation should modify existing reservation without error",
        "duration": 19,
        "err": {}
      },
      {
        "title": "should no longer contain record of the deleted reservation",
        "fullTitle": "promise reservation for future use cancel-reservation should no longer contain record of the deleted reservation",
        "duration": 1,
        "err": {}
      },
      {
        "title": "should decrease available capacity from a provider in the future",
        "fullTitle": "promise capacity planning decrease-capacity should decrease available capacity from a provider in the future",
        "duration": 18,
        "err": {}
      },
      {
        "title": "should increase available capacity from a provider in the future",
        "fullTitle": "promise capacity planning increase-capacity should increase available capacity from a provider in the future",
        "duration": 13,
        "err": {}
      },
      {
        "title": "should report available collections and utilizations",
        "fullTitle": "promise capacity planning query-capacity should report available collections and utilizations",
        "duration": 66,
        "err": {}
      },
      {
        "title": "should fail to create immediate reservation record with proper error",
        "fullTitle": "promise reservation with conflict create-reservation should fail to create immediate reservation record with proper error",
        "duration": 74,
        "err": {}
      },
      {
        "title": "should fail to create future reservation record with proper error",
        "fullTitle": "promise reservation with conflict create-reservation should fail to create future reservation record with proper error",
        "duration": 69,
        "err": {}
      },
      {
        "title": "should successfully destroy all allocations",
        "fullTitle": "promise cleanup test allocations destroy-instance should successfully destroy all allocations",
        "duration": 507,
        "err": {}
      }
    ],
    "pending": [],
    "failures": [],
    "passes": [
      {
        "title": "should add a new OpenStack provider without error",
        "fullTitle": "promise register OpenStack into resource pool add-provider should add a new OpenStack provider without error",
        "duration": 1171,
        "err": {}
      },
      {
        "title": "should update promise.providers with a new entry",
        "fullTitle": "promise register OpenStack into resource pool add-provider should update promise.providers with a new entry",
        "duration": 7,
        "err": {}
      },
      {
        "title": "should contain a new ResourceProvider record in the store",
        "fullTitle": "promise register OpenStack into resource pool add-provider should contain a new ResourceProvider record in the store",
        "duration": 1,
        "err": {}
      },
      {
        "title": "should add more capacity to the reservation service without error",
        "fullTitle": "promise register OpenStack into resource pool increase-capacity should add more capacity to the reservation service without error",
        "duration": 29,
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
        "duration": 23,
        "err": {}
      },
      {
        "title": "should contain newly added capacity pool",
        "fullTitle": "promise register OpenStack into resource pool query-capacity should contain newly added capacity pool",
        "duration": 13,
        "err": {}
      },
      {
        "title": "should create a new server in target provider without error",
        "fullTitle": "promise allocation without reservation create-instance should create a new server in target provider without error",
        "duration": 1144,
        "err": {}
      },
      {
        "title": "should update promise.allocations with a new entry",
        "fullTitle": "promise allocation without reservation create-instance should update promise.allocations with a new entry",
        "duration": 3,
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
        "duration": 0,
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
        "duration": 71,
        "err": {}
      },
      {
        "title": "should update promise.reservations with a new entry",
        "fullTitle": "promise allocation using reservation for immediate use create-reservation should update promise.reservations with a new entry",
        "duration": 9,
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
        "duration": 1025,
        "err": {}
      },
      {
        "title": "should contain a new ResourceAllocation record in the store",
        "fullTitle": "promise allocation using reservation for immediate use create-instance should contain a new ResourceAllocation record in the store",
        "duration": 0,
        "err": {}
      },
      {
        "title": "should be referenced in the reservation record",
        "fullTitle": "promise allocation using reservation for immediate use create-instance should be referenced in the reservation record",
        "duration": 5,
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
        "duration": 125,
        "err": {}
      },
      {
        "title": "should update promise.reservations with a new entry",
        "fullTitle": "promise reservation for future use create-reservation should update promise.reservations with a new entry",
        "duration": 18,
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
        "duration": 74,
        "err": {}
      },
      {
        "title": "should modify existing reservation without error",
        "fullTitle": "promise reservation for future use update-reservation should modify existing reservation without error",
        "duration": 88,
        "err": {}
      },
      {
        "title": "should modify existing reservation without error",
        "fullTitle": "promise reservation for future use cancel-reservation should modify existing reservation without error",
        "duration": 19,
        "err": {}
      },
      {
        "title": "should no longer contain record of the deleted reservation",
        "fullTitle": "promise reservation for future use cancel-reservation should no longer contain record of the deleted reservation",
        "duration": 1,
        "err": {}
      },
      {
        "title": "should decrease available capacity from a provider in the future",
        "fullTitle": "promise capacity planning decrease-capacity should decrease available capacity from a provider in the future",
        "duration": 18,
        "err": {}
      },
      {
        "title": "should increase available capacity from a provider in the future",
        "fullTitle": "promise capacity planning increase-capacity should increase available capacity from a provider in the future",
        "duration": 13,
        "err": {}
      },
      {
        "title": "should report available collections and utilizations",
        "fullTitle": "promise capacity planning query-capacity should report available collections and utilizations",
        "duration": 66,
        "err": {}
      },
      {
        "title": "should fail to create immediate reservation record with proper error",
        "fullTitle": "promise reservation with conflict create-reservation should fail to create immediate reservation record with proper error",
        "duration": 74,
        "err": {}
      },
      {
        "title": "should fail to create future reservation record with proper error",
        "fullTitle": "promise reservation with conflict create-reservation should fail to create future reservation record with proper error",
        "duration": 69,
        "err": {}
      },
      {
        "title": "should successfully destroy all allocations",
        "fullTitle": "promise cleanup test allocations destroy-instance should successfully destroy all allocations",
        "duration": 507,
        "err": {}
      }
    ]
  }
  Promise- INFO -
  ****************************************
            Promise test report

  ****************************************
   Suites:  	23
   Tests:   	33
   Passes:  	33
   Pending: 	0
   Failures:	0
   Start:   	2016-02-23T10:44:37.402Z
   End:     	2016-02-23T10:44:42.006Z
   Duration:	4.604
  ****************************************

  Promise- INFO - Pushing results to DB...
