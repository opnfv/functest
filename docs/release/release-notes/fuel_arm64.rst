fuel(arm64)
===========

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-05 19:46:24  arm-pod6    PASS
api_check             2018-04-05 20:23:40  arm-pod6    PASS
snaps_health_check    2018-04-05 20:25:54  arm-pod6    PASS
vping_ssh             2018-04-05 20:31:11  arm-pod6    PASS
vping_userdata        2018-04-05 20:35:28  arm-pod6    PASS
tempest_smoke_serial  2018-04-05 21:47:34  arm-pod6    PASS
rally_sanity          2018-04-05 23:07:52  arm-pod6    PASS
refstack_defcore      2018-04-05 23:32:04  arm-pod6    FAIL
patrole               2018-04-05 23:47:59  arm-pod6    PASS
snaps_smoke           2018-04-06 02:56:45  arm-pod6    FAIL      SNAPS-283
neutron_trunk         2018-04-06 03:10:36  arm-pod6    PASS
====================  ===================  ==========  ========  =========
