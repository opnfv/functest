apex
====

os-nosdn-nofeature-noha
-----------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-05-22 03:05:29  lf-pod1     PASS
api_check             2018-05-22 03:15:22  lf-pod1     PASS
snaps_health_check    2018-05-22 03:15:55  lf-pod1     PASS
vping_ssh             2018-05-22 03:17:02  lf-pod1     PASS
vping_userdata        2018-05-22 03:17:51  lf-pod1     PASS
tempest_smoke_serial  2018-05-22 03:29:22  lf-pod1     PASS
rally_sanity          2018-05-22 03:50:04  lf-pod1     PASS
refstack_defcore      2018-05-22 03:53:33  lf-pod1     PASS
patrole               2018-05-22 03:56:35  lf-pod1     PASS
snaps_smoke           2018-05-22 04:37:48  lf-pod1     PASS
neutron_trunk         2018-05-22 04:40:07  lf-pod1     PASS
cloudify_ims          2018-05-22 05:08:28  lf-pod1     PASS
vyos_vrouter          2018-05-22 05:30:49  lf-pod1     PASS
juju_epc              2018-05-22 06:13:06  lf-pod1     PASS
====================  ===================  ==========  ========  ======

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ========
connection_check      2018-05-15 20:50:04  lf-pod1     PASS
api_check             2018-05-15 21:03:24  lf-pod1     PASS
snaps_health_check    2018-05-15 21:04:17  lf-pod1     PASS
vping_ssh             2018-05-15 21:07:52  lf-pod1     PASS
vping_userdata        2018-05-15 21:08:59  lf-pod1     PASS
tempest_smoke_serial  2018-05-15 21:24:40  lf-pod1     PASS
rally_sanity          2018-05-15 21:50:37  lf-pod1     PASS
refstack_defcore      2018-05-15 21:54:21  lf-pod1     PASS
patrole               2018-05-15 21:57:33  lf-pod1     PASS
snaps_smoke           2018-05-15 22:52:27  lf-pod1     FAIL      APEX-598
neutron_trunk         2018-05-15 22:55:00  lf-pod1     PASS
cloudify_ims          2018-05-15 23:22:40  lf-pod1     PASS
vyos_vrouter          2018-05-15 23:44:44  lf-pod1     PASS
juju_epc              2018-05-16 00:34:04  lf-pod1     PASS
====================  ===================  ==========  ========  ========

os-odl-nofeature-noha
---------------------

====================  ===================  ==========  ========  ========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ========
connection_check      2018-05-19 16:29:01  lf-pod1     PASS
api_check             2018-05-19 16:39:03  lf-pod1     PASS
snaps_health_check    2018-05-19 16:39:38  lf-pod1     PASS
vping_ssh             2018-05-19 16:40:23  lf-pod1     PASS
vping_userdata        2018-05-19 16:41:10  lf-pod1     PASS
tempest_smoke_serial  2018-05-19 16:55:07  lf-pod1     FAIL
rally_sanity          2018-05-19 17:17:15  lf-pod1     PASS
refstack_defcore      2018-05-19 17:29:38  lf-pod1     FAIL
patrole               2018-05-19 17:32:51  lf-pod1     PASS
snaps_smoke           2018-05-19 18:16:08  lf-pod1     FAIL      APEX-598
odl                   2018-05-19 17:33:09  lf-pod1     PASS
neutron_trunk         2018-05-19 18:18:36  lf-pod1     PASS
cloudify_ims          2018-05-19 18:32:20  lf-pod1     FAIL
vyos_vrouter          2018-05-16 14:14:02  lf-pod1     FAIL
juju_epc              2018-05-16 14:14:27  lf-pod1     FAIL
====================  ===================  ==========  ========  ========

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  ========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ========
connection_check      2018-05-19 03:39:41  lf-pod1     PASS
api_check             2018-05-19 03:52:36  lf-pod1     PASS
snaps_health_check    2018-05-19 03:53:20  lf-pod1     PASS
vping_ssh             2018-05-19 03:55:28  lf-pod1     PASS
vping_userdata        2018-05-19 03:56:27  lf-pod1     PASS
tempest_smoke_serial  2018-05-19 04:14:34  lf-pod1     FAIL
rally_sanity          2018-05-19 04:14:59  lf-pod1     FAIL
refstack_defcore      2018-05-19 04:17:43  lf-pod1     FAIL
patrole               2018-05-19 04:21:05  lf-pod1     PASS
snaps_smoke           2018-05-19 05:00:26  lf-pod1     FAIL      APEX-598
odl                   2018-05-19 04:21:27  lf-pod1     PASS
neutron_trunk         2018-05-19 05:03:03  lf-pod1     FAIL
cloudify_ims          2018-05-19 05:05:04  lf-pod1     FAIL
vyos_vrouter          2018-05-19 05:06:59  lf-pod1     FAIL
juju_epc              2018-05-19 05:07:20  lf-pod1     FAIL
====================  ===================  ==========  ========  ========

os-ovn-nofeature-noha
---------------------

====================  ===================  ==========  ========  ========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ========
connection_check      2018-05-19 11:32:32  lf-pod1     PASS
api_check             2018-05-19 11:41:31  lf-pod1     PASS
snaps_health_check    2018-05-19 11:42:01  lf-pod1     PASS
vping_ssh             2018-05-19 11:42:49  lf-pod1     PASS
vping_userdata        2018-05-19 11:43:34  lf-pod1     PASS
tempest_smoke_serial  2018-05-19 11:56:24  lf-pod1     FAIL
rally_sanity          2018-05-19 12:17:54  lf-pod1     PASS
refstack_defcore      2018-05-19 12:20:53  lf-pod1     PASS
patrole               2018-05-19 12:23:56  lf-pod1     FAIL
snaps_smoke           2018-05-19 13:05:57  lf-pod1     FAIL      APEX-598
neutron_trunk         2018-05-19 13:07:47  lf-pod1     FAIL
cloudify_ims          2018-05-19 13:14:11  lf-pod1     FAIL
vyos_vrouter          2018-05-19 13:20:36  lf-pod1     FAIL
juju_epc              2018-05-19 13:23:47  lf-pod1     FAIL
====================  ===================  ==========  ========  ========
