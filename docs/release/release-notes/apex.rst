apex
====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-10 19:08:51  lf-pod1     PASS
api_check             2018-04-10 19:21:53  lf-pod1     PASS
snaps_health_check    2018-04-10 19:22:37  lf-pod1     PASS
vping_ssh             2018-04-10 19:24:52  lf-pod1     PASS
vping_userdata        2018-04-10 19:26:01  lf-pod1     PASS
tempest_smoke_serial  2018-04-10 19:41:43  lf-pod1     PASS
rally_sanity          2018-04-10 20:03:27  lf-pod1     FAIL      APEX-564
refstack_defcore      2018-04-10 20:06:01  lf-pod1     PASS
patrole               2018-04-10 20:09:20  lf-pod1     PASS
snaps_smoke           2018-04-10 21:06:47  lf-pod1     FAIL      SNAPS-283
neutron_trunk         2018-04-10 21:09:21  lf-pod1     PASS
cloudify_ims          2018-04-10 21:39:18  lf-pod1     PASS
vyos_vrouter          2018-04-10 22:01:34  lf-pod1     PASS
juju_epc              2018-04-10 22:24:23  lf-pod1     FAIL      APEX-570
====================  ===================  ==========  ========  =========

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-11 03:54:43  lf-pod1     PASS
api_check             2018-04-11 04:06:49  lf-pod1     PASS
snaps_health_check    2018-04-11 04:08:27  lf-pod1     PASS
vping_ssh             2018-04-11 04:10:36  lf-pod1     PASS
vping_userdata        2018-04-11 04:12:36  lf-pod1     PASS
tempest_smoke_serial  2018-04-11 04:30:14  lf-pod1     FAIL
rally_sanity          2018-04-11 04:50:51  lf-pod1     FAIL
refstack_defcore      2018-04-11 04:56:07  lf-pod1     PASS
patrole               2018-04-11 04:59:31  lf-pod1     PASS
snaps_smoke           2018-04-11 06:06:04  lf-pod1     FAIL      SNAPS-283
odl                   2018-04-11 04:59:52  lf-pod1     PASS
neutron_trunk         2018-04-11 06:08:45  lf-pod1     FAIL
cloudify_ims          2018-04-11 06:10:47  lf-pod1     FAIL
vyos_vrouter          2018-04-11 06:12:47  lf-pod1     FAIL
juju_epc              2018-04-11 06:13:08  lf-pod1     FAIL
====================  ===================  ==========  ========  =========
