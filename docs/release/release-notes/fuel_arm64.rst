fuel(arm64)
===========

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-19 03:31:53  arm-pod6    PASS
api_check             2018-04-19 04:03:23  arm-pod6    PASS
snaps_health_check    2018-04-19 04:05:20  arm-pod6    PASS
vping_ssh             2018-04-19 04:09:38  arm-pod6    PASS
vping_userdata        2018-04-19 04:13:08  arm-pod6    PASS
tempest_smoke_serial  2018-04-19 05:14:31  arm-pod6    PASS
rally_sanity          2018-04-19 06:28:45  arm-pod6    PASS
refstack_defcore      2018-04-19 06:52:04  arm-pod6    FAIL
patrole               2018-04-19 07:07:00  arm-pod6    PASS
snaps_smoke           2018-04-19 10:14:10  arm-pod6    FAIL      SNAPS-283
neutron_trunk         2018-04-19 10:27:50  arm-pod6    PASS
====================  ===================  ==========  ========  =========
