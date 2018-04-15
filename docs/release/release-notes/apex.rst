apex
====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-07 04:52:18  lf-pod1     PASS
api_check             2018-04-07 05:05:30  lf-pod1     PASS
snaps_health_check    2018-04-07 05:06:12  lf-pod1     PASS
vping_ssh             2018-04-07 05:07:49  lf-pod1     PASS
vping_userdata        2018-04-07 05:08:55  lf-pod1     PASS
tempest_smoke_serial  2018-04-07 05:24:59  lf-pod1     PASS
rally_sanity          2018-04-07 05:46:43  lf-pod1     FAIL      APEX-564
refstack_defcore      2018-04-07 05:49:54  lf-pod1     PASS
patrole               2018-04-07 05:53:10  lf-pod1     PASS
snaps_smoke           2018-04-07 06:50:35  lf-pod1     FAIL      SNAPS-283
neutron_trunk         2018-04-07 06:53:13  lf-pod1     PASS
cloudify_ims          2018-04-07 07:19:50  lf-pod1     PASS
vyos_vrouter          2018-04-07 07:40:53  lf-pod1     PASS
juju_epc              2018-04-07 08:06:00  lf-pod1     FAIL      APEX-570
====================  ===================  ==========  ========  =========

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-07 13:18:17  lf-pod1     PASS
api_check             2018-04-07 13:30:11  lf-pod1     PASS
snaps_health_check    2018-04-07 13:31:46  lf-pod1     PASS
vping_ssh             2018-04-07 13:32:46  lf-pod1     PASS
vping_userdata        2018-04-07 13:33:40  lf-pod1     PASS
tempest_smoke_serial  2018-04-07 13:53:58  lf-pod1     FAIL
rally_sanity          2018-04-07 14:12:42  lf-pod1     FAIL
refstack_defcore      2018-04-07 14:21:20  lf-pod1     FAIL
patrole               2018-04-07 14:24:48  lf-pod1     FAIL
snaps_smoke           2018-04-07 15:05:15  lf-pod1     FAIL      SNAPS-283
odl                   2018-04-07 14:25:10  lf-pod1     PASS
neutron_trunk         2018-04-07 15:07:53  lf-pod1     FAIL
cloudify_ims                               lf-pod1
vyos_vrouter                               lf-pod1
juju_epc                                   lf-pod1
====================  ===================  ==========  ========  =========
