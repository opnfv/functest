fuel(amd64)
===========

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-05-14 17:40:16  lf-pod2     PASS
api_check             2018-05-14 17:51:05  lf-pod2     PASS
snaps_health_check    2018-05-14 17:51:41  lf-pod2     PASS
vping_ssh             2018-05-14 17:53:57  lf-pod2     PASS
vping_userdata        2018-05-14 17:54:55  lf-pod2     PASS
tempest_smoke_serial  2018-05-14 18:11:38  lf-pod2     PASS
rally_sanity          2018-05-14 18:40:50  lf-pod2     PASS
refstack_defcore      2018-05-14 18:44:36  lf-pod2     PASS
patrole               2018-05-14 18:49:12  lf-pod2     PASS
snaps_smoke           2018-05-14 19:39:05  lf-pod2     PASS
neutron_trunk         2018-05-14 19:42:13  lf-pod2     PASS
cloudify_ims          2018-05-14 19:54:41  lf-pod2     FAIL
vyos_vrouter          2018-05-14 20:36:34  lf-pod2     PASS
juju_epc              2018-05-14 21:30:41  lf-pod2     PASS
====================  ===================  ==========  ========  ======

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-05-18 13:09:21  lf-pod2     PASS
api_check             2018-05-18 13:20:57  lf-pod2     PASS
snaps_health_check    2018-05-18 13:21:38  lf-pod2     PASS
vping_ssh             2018-05-18 13:23:28  lf-pod2     PASS
vping_userdata        2018-05-18 13:24:31  lf-pod2     PASS
tempest_smoke_serial  2018-05-18 13:43:53  lf-pod2     PASS
rally_sanity          2018-05-18 14:15:45  lf-pod2     PASS
refstack_defcore      2018-05-18 14:22:38  lf-pod2     PASS
patrole               2018-05-18 14:26:37  lf-pod2     PASS
snaps_smoke           2018-05-18 15:25:11  lf-pod2     PASS
odl                   2018-05-18 14:27:00  lf-pod2     PASS
neutron_trunk         2018-05-18 15:28:59  lf-pod2     FAIL
cloudify_ims          2018-05-18 15:38:36  lf-pod2     FAIL
vyos_vrouter          2018-05-18 15:45:18  lf-pod2     FAIL
juju_epc              2018-05-19 02:28:06  lf-pod2     FAIL
====================  ===================  ==========  ========  ======
