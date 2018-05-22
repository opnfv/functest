fuel(arm64)
===========

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-05-15 14:36:48  arm-pod6    PASS
api_check             2018-05-15 15:05:32  arm-pod6    PASS
snaps_health_check    2018-05-15 15:07:37  arm-pod6    PASS
vping_ssh             2018-05-15 15:11:41  arm-pod6    PASS
vping_userdata        2018-05-15 15:14:47  arm-pod6    PASS
tempest_smoke_serial  2018-05-15 16:07:59  arm-pod6    PASS
rally_sanity          2018-05-15 17:14:19  arm-pod6    PASS
refstack_defcore      2018-05-15 17:32:52  arm-pod6    PASS
patrole               2018-05-15 17:47:50  arm-pod6    PASS
snaps_smoke           2018-05-15 20:34:24  arm-pod6    PASS
neutron_trunk         2018-05-15 20:47:58  arm-pod6    PASS
====================  ===================  ==========  ========  ======

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-05-18 06:19:39  arm-pod6    PASS
api_check             2018-05-18 06:47:08  arm-pod6    PASS
snaps_health_check    2018-05-18 06:49:04  arm-pod6    PASS
vping_ssh             2018-05-18 06:55:04  arm-pod6    FAIL
vping_userdata        2018-05-08 06:03:00  arm-pod6    PASS
tempest_smoke_serial  2018-05-08 06:55:43  arm-pod6    PASS
rally_sanity          2018-05-08 07:58:58  arm-pod6    PASS
refstack_defcore      2018-05-08 08:17:00  arm-pod6    FAIL
patrole               2018-05-08 08:31:40  arm-pod6    PASS
snaps_smoke           2018-05-08 11:11:52  arm-pod6    PASS
neutron_trunk         2018-05-08 11:25:26  arm-pod6    FAIL
====================  ===================  ==========  ========  ======
