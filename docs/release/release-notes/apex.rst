apex
====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-19 22:54:11  lf-pod1     PASS
api_check             2018-04-19 23:07:11  lf-pod1     PASS
snaps_health_check    2018-04-19 23:07:58  lf-pod1     PASS
vping_ssh             2018-04-19 23:09:42  lf-pod1     PASS
vping_userdata        2018-04-19 23:10:49  lf-pod1     PASS
tempest_smoke_serial  2018-04-19 23:26:30  lf-pod1     PASS
rally_sanity          2018-04-19 23:52:33  lf-pod1     PASS      APEX-564
refstack_defcore      2018-04-19 23:55:32  lf-pod1     PASS
patrole               2018-04-19 23:58:42  lf-pod1     PASS
snaps_smoke           2018-04-20 00:55:10  lf-pod1     FAIL      SNAPS-283
neutron_trunk         2018-04-20 00:57:45  lf-pod1     PASS
cloudify_ims          2018-04-20 01:26:53  lf-pod1     PASS
vyos_vrouter          2018-04-20 01:49:40  lf-pod1     PASS
juju_epc              2018-04-20 02:38:36  lf-pod1     PASS      APEX-570
====================  ===================  ==========  ========  =========

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-19 03:13:41  lf-pod1     PASS
api_check             2018-04-19 03:25:58  lf-pod1     PASS
snaps_health_check    2018-04-19 03:26:41  lf-pod1     PASS
vping_ssh             2018-04-19 03:28:21  lf-pod1     PASS
vping_userdata        2018-04-19 03:29:18  lf-pod1     PASS
tempest_smoke_serial  2018-04-19 03:46:47  lf-pod1     PASS
rally_sanity          2018-04-19 04:07:39  lf-pod1     FAIL
refstack_defcore      2018-04-19 04:15:37  lf-pod1     FAIL
patrole               2018-04-19 04:19:09  lf-pod1     PASS
snaps_smoke           2018-04-19 05:01:46  lf-pod1     FAIL      SNAPS-283
odl                   2018-04-19 04:19:32  lf-pod1     PASS
neutron_trunk         2018-04-19 05:04:28  lf-pod1     FAIL
cloudify_ims          2018-04-19 05:06:30  lf-pod1     FAIL
vyos_vrouter          2018-04-19 05:08:38  lf-pod1     FAIL
juju_epc              2018-04-19 05:09:01  lf-pod1     FAIL
====================  ===================  ==========  ========  =========
