fuel(amd64)
===========

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ========
connection_check      2018-04-11 22:10:32  lf-pod2     PASS
api_check             2018-04-11 22:22:36  lf-pod2     PASS
snaps_health_check    2018-04-11 22:23:24  lf-pod2     PASS
vping_ssh             2018-04-11 22:24:53  lf-pod2     PASS
vping_userdata        2018-04-11 22:26:12  lf-pod2     PASS
tempest_smoke_serial  2018-04-11 22:45:34  lf-pod2     PASS
rally_sanity          2018-04-11 23:16:23  lf-pod2     PASS
refstack_defcore      2018-04-11 23:20:58  lf-pod2     PASS
patrole               2018-04-11 23:25:53  lf-pod2     PASS
snaps_smoke           2018-04-12 00:34:00  lf-pod2     FAIL      FUEL-356
neutron_trunk         2018-04-12 00:36:57  lf-pod2     PASS
cloudify_ims          2018-04-12 00:56:01  lf-pod2     FAIL
vyos_vrouter          2018-04-12 01:13:43  lf-pod2     FAIL
juju_epc              2018-04-12 01:22:37  lf-pod2     FAIL
====================  ===================  ==========  ========  ========

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-13 04:43:03  lf-pod2     PASS
api_check             2018-04-13 05:01:11  lf-pod2     FAIL
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
cloudify_ims                               lf-pod2
vyos_vrouter                               lf-pod2
juju_epc                                   lf-pod2
====================  ===================  ==========  ========  =========
