fuel(amd64)
===========

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ========
connection_check      2018-04-07 22:08:05  lf-pod2     PASS
api_check             2018-04-07 22:19:50  lf-pod2     PASS
snaps_health_check    2018-04-07 22:20:38  lf-pod2     PASS
vping_ssh             2018-04-07 22:21:45  lf-pod2     PASS
vping_userdata        2018-04-07 22:22:57  lf-pod2     PASS
tempest_smoke_serial  2018-04-07 22:42:15  lf-pod2     PASS
rally_sanity          2018-04-07 23:13:04  lf-pod2     PASS
refstack_defcore      2018-04-07 23:19:35  lf-pod2     PASS
patrole               2018-04-07 23:25:04  lf-pod2     PASS
snaps_smoke           2018-04-08 00:31:06  lf-pod2     FAIL      FUEL-356
neutron_trunk         2018-04-08 00:34:04  lf-pod2     PASS
cloudify_ims          2018-04-08 00:51:42  lf-pod2     FAIL
vyos_vrouter          2018-04-08 01:09:38  lf-pod2     FAIL
juju_epc              2018-04-08 01:18:36  lf-pod2     FAIL
====================  ===================  ==========  ========  ========

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-06 23:17:26  lf-pod2     PASS
api_check             2018-04-06 23:28:58  lf-pod2     PASS
snaps_health_check    2018-04-06 23:29:48  lf-pod2     PASS
vping_ssh             2018-04-06 23:31:06  lf-pod2     PASS
vping_userdata        2018-04-06 23:32:13  lf-pod2     PASS
tempest_smoke_serial  2018-04-06 23:51:25  lf-pod2     FAIL
rally_sanity          2018-04-07 00:24:03  lf-pod2     FAIL
refstack_defcore      2018-04-07 00:30:34  lf-pod2     PASS
patrole               2018-04-07 00:34:31  lf-pod2     PASS
snaps_smoke           2018-04-07 01:44:38  lf-pod2     FAIL      SNAPS-283
odl                   2018-04-07 00:34:42  lf-pod2     FAIL
neutron_trunk         2018-04-07 01:47:59  lf-pod2     FAIL
====================  ===================  ==========  ========  =========
