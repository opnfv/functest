fuel(arm64)
===========

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-13 16:27:05  arm-pod6    PASS
api_check             2018-04-13 16:58:41  arm-pod6    PASS
snaps_health_check    2018-04-13 17:00:42  arm-pod6    PASS
vping_ssh             2018-04-13 17:05:01  arm-pod6    PASS
vping_userdata        2018-04-13 17:08:41  arm-pod6    PASS
tempest_smoke_serial  2018-04-13 18:10:08  arm-pod6    PASS
rally_sanity          2018-04-13 19:24:17  arm-pod6    PASS
refstack_defcore      2018-04-13 19:48:28  arm-pod6    FAIL
patrole               2018-04-13 20:03:13  arm-pod6    PASS
snaps_smoke           2018-04-13 23:07:53  arm-pod6    FAIL      SNAPS-283
neutron_trunk         2018-04-13 23:21:44  arm-pod6    PASS
====================  ===================  ==========  ========  =========
