fuel(arm64)
===========

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-06-05 11:01:32  arm-pod6    PASS
api_check             2018-06-05 11:32:38  arm-pod6    PASS
snaps_health_check    2018-06-05 11:34:49  arm-pod6    PASS
vping_ssh             2018-06-05 11:38:25  arm-pod6    PASS
vping_userdata        2018-06-05 11:41:28  arm-pod6    PASS
tempest_smoke_serial  2018-06-05 12:38:36  arm-pod6    PASS
rally_sanity          2018-06-05 13:49:14  arm-pod6    PASS
refstack_defcore      2018-06-05 14:08:21  arm-pod6    PASS
patrole               2018-06-05 14:23:56  arm-pod6    FAIL
snaps_smoke           2018-06-05 17:19:43  arm-pod6    PASS
neutron_trunk         2018-06-05 17:34:35  arm-pod6    PASS
====================  ===================  ==========  ========  ======

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-06-01 06:01:27  arm-pod6    PASS
api_check             2018-06-01 06:31:53  arm-pod6    PASS
snaps_health_check    2018-06-01 06:33:52  arm-pod6    PASS
vping_ssh             2018-06-01 06:37:25  arm-pod6    PASS
vping_userdata        2018-06-01 06:40:26  arm-pod6    PASS
tempest_smoke_serial  2018-06-01 07:34:32  arm-pod6    PASS
rally_sanity          2018-06-01 08:41:07  arm-pod6    PASS
refstack_defcore      2018-06-01 09:00:13  arm-pod6    PASS
patrole               2018-06-01 09:15:33  arm-pod6    PASS
snaps_smoke           2018-06-01 12:04:59  arm-pod6    PASS
neutron_trunk         2018-06-01 12:19:52  arm-pod6    FAIL
====================  ===================  ==========  ========  ======
