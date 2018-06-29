fuel(amd64)
===========

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-05-28 13:19:03  lf-pod2     PASS
api_check             2018-05-28 13:34:24  lf-pod2     PASS
snaps_health_check    2018-05-28 13:35:24  lf-pod2     PASS
vping_ssh             2018-05-28 13:37:05  lf-pod2     PASS
vping_userdata        2018-05-28 13:38:25  lf-pod2     PASS
tempest_smoke_serial  2018-05-28 14:02:24  lf-pod2     PASS
rally_sanity          2018-05-28 14:40:14  lf-pod2     PASS
refstack_defcore      2018-05-28 14:44:43  lf-pod2     PASS
patrole               2018-05-28 14:49:51  lf-pod2     PASS
snaps_smoke           2018-05-28 16:02:47  lf-pod2     PASS
neutron_trunk         2018-05-28 16:07:20  lf-pod2     PASS
cloudify_ims          2018-05-28 16:21:53  lf-pod2     FAIL
vyos_vrouter          2018-05-28 17:14:28  lf-pod2     FAIL
juju_epc              2018-05-28 18:08:07  lf-pod2     PASS
====================  ===================  ==========  ========  ======

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-05-29 18:56:33  lf-pod2     PASS
api_check             2018-05-29 19:07:45  lf-pod2     PASS
snaps_health_check    2018-05-29 19:08:23  lf-pod2     PASS
vping_ssh             2018-05-29 19:09:25  lf-pod2     PASS
vping_userdata        2018-05-29 19:10:14  lf-pod2     PASS
tempest_smoke_serial  2018-05-29 19:29:16  lf-pod2     FAIL
rally_sanity          2018-05-29 19:59:06  lf-pod2     PASS
refstack_defcore      2018-05-29 20:04:48  lf-pod2     FAIL
patrole               2018-05-29 20:09:08  lf-pod2     PASS
snaps_smoke           2018-05-29 21:03:10  lf-pod2     PASS
odl                   2018-05-29 20:09:31  lf-pod2     PASS
neutron_trunk         2018-05-29 21:06:24  lf-pod2     FAIL
cloudify_ims          2018-05-29 21:12:00  lf-pod2     FAIL
vyos_vrouter          2018-05-29 21:17:35  lf-pod2     FAIL
juju_epc              2018-05-30 01:44:01  lf-pod2     FAIL
====================  ===================  ==========  ========  ======
