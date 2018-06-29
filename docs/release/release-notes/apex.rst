apex
====

os-nosdn-nofeature-noha
-----------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-06-24 21:40:33  lf-pod1     PASS
api_check             2018-06-24 21:50:59  lf-pod1     PASS
snaps_health_check    2018-06-24 21:51:38  lf-pod1     PASS
vping_ssh             2018-06-24 21:52:27  lf-pod1     PASS
vping_userdata        2018-06-24 21:53:10  lf-pod1     PASS
tempest_smoke_serial  2018-06-24 22:05:20  lf-pod1     PASS
rally_sanity          2018-06-24 22:26:24  lf-pod1     PASS
refstack_defcore      2018-06-24 22:33:44  lf-pod1     PASS
patrole               2018-06-24 22:36:47  lf-pod1     PASS
snaps_smoke           2018-06-24 23:18:09  lf-pod1     PASS
neutron_trunk         2018-06-24 23:20:29  lf-pod1     PASS
cloudify_ims          2018-06-24 23:50:53  lf-pod1     PASS
vyos_vrouter          2018-06-20 17:56:48  lf-pod1     PASS
juju_epc              2018-06-20 18:42:19  lf-pod1     PASS
====================  ===================  ==========  ========  ======

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-06-25 08:59:21  lf-pod1     PASS
api_check             2018-06-25 09:12:17  lf-pod1     PASS
snaps_health_check    2018-06-25 09:13:00  lf-pod1     PASS
vping_ssh             2018-06-25 09:13:52  lf-pod1     PASS
vping_userdata        2018-06-25 09:15:14  lf-pod1     PASS
tempest_smoke_serial  2018-06-25 09:30:42  lf-pod1     PASS
rally_sanity          2018-06-25 09:56:10  lf-pod1     PASS
refstack_defcore      2018-06-25 09:59:40  lf-pod1     PASS
patrole               2018-06-25 10:02:45  lf-pod1     PASS
snaps_smoke           2018-06-25 10:58:29  lf-pod1     PASS
neutron_trunk         2018-06-25 11:00:59  lf-pod1     PASS
cloudify_ims          2018-06-25 11:30:08  lf-pod1     PASS
vyos_vrouter          2018-06-25 11:48:52  lf-pod1     PASS
juju_epc              2018-06-25 12:31:10  lf-pod1     PASS
====================  ===================  ==========  ========  ======

os-odl-nofeature-noha
---------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-06-21 19:15:31  lf-pod1     PASS
api_check             2018-06-21 19:25:15  lf-pod1     PASS
snaps_health_check    2018-06-21 19:26:15  lf-pod1     PASS
vping_ssh             2018-06-21 19:33:49  lf-pod1     FAIL
vping_userdata        2018-06-21 19:34:31  lf-pod1     PASS
tempest_smoke_serial  2018-06-21 19:46:41  lf-pod1     PASS
rally_sanity          2018-06-21 20:08:17  lf-pod1     PASS
refstack_defcore      2018-06-21 20:17:08  lf-pod1     FAIL
patrole               2018-06-21 20:20:20  lf-pod1     PASS
snaps_smoke           2018-06-21 21:13:42  lf-pod1     FAIL
odl                   2018-06-21 20:20:38  lf-pod1     PASS
neutron_trunk         2018-06-21 21:16:06  lf-pod1     PASS
cloudify_ims          2018-06-21 21:29:28  lf-pod1     FAIL
vyos_vrouter          2018-06-21 23:36:49  lf-pod1     FAIL
juju_epc              2018-06-22 00:09:16  lf-pod1     FAIL
====================  ===================  ==========  ========  ======

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-06-25 20:35:00  lf-pod1     PASS
api_check             2018-06-25 20:47:16  lf-pod1     PASS
snaps_health_check    2018-06-25 20:48:52  lf-pod1     PASS
vping_ssh             2018-06-25 20:50:43  lf-pod1     PASS
vping_userdata        2018-06-25 20:52:33  lf-pod1     PASS
tempest_smoke_serial  2018-06-25 21:09:07  lf-pod1     FAIL
rally_sanity          2018-06-25 21:33:49  lf-pod1     PASS
refstack_defcore      2018-06-25 21:36:55  lf-pod1     FAIL
patrole               2018-06-25 21:40:21  lf-pod1     PASS
snaps_smoke           2018-06-25 22:20:20  lf-pod1     FAIL
odl                   2018-06-25 21:40:43  lf-pod1     PASS
neutron_trunk         2018-06-25 22:22:52  lf-pod1     FAIL
cloudify_ims          2018-06-25 22:24:55  lf-pod1     FAIL
vyos_vrouter          2018-06-25 22:26:54  lf-pod1     FAIL
juju_epc              2018-06-25 22:27:16  lf-pod1     FAIL
====================  ===================  ==========  ========  ======

os-ovn-nofeature-noha
---------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-06-22 03:36:05  lf-pod1     PASS
api_check             2018-06-22 03:45:17  lf-pod1     PASS
snaps_health_check    2018-06-22 03:45:50  lf-pod1     PASS
vping_ssh             2018-06-22 03:46:27  lf-pod1     PASS
vping_userdata        2018-06-22 03:47:08  lf-pod1     PASS
tempest_smoke_serial  2018-06-22 04:00:34  lf-pod1     FAIL
rally_sanity          2018-06-22 04:21:54  lf-pod1     PASS
refstack_defcore      2018-06-22 04:24:52  lf-pod1     PASS
patrole               2018-06-22 04:27:51  lf-pod1     FAIL
snaps_smoke           2018-06-22 05:10:38  lf-pod1     PASS
neutron_trunk         2018-06-22 05:12:23  lf-pod1     FAIL
cloudify_ims          2018-06-22 06:18:55  lf-pod1     FAIL
vyos_vrouter          2018-06-22 06:37:18  lf-pod1     PASS
juju_epc              2018-06-22 06:40:52  lf-pod1     FAIL
====================  ===================  ==========  ========  ======
