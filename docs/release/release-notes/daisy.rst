daisy
=====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-20 07:48:02  zte-pod2    PASS
api_check             2018-04-20 07:59:03  zte-pod2    PASS
snaps_health_check    2018-04-20 07:59:46  zte-pod2    PASS
vping_ssh             2018-04-20 08:02:00  zte-pod2    PASS
vping_userdata        2018-04-20 08:03:04  zte-pod2    PASS
tempest_smoke_serial  2018-04-20 08:18:54  zte-pod2    PASS
rally_sanity          2018-04-20 08:47:35  zte-pod2    PASS
refstack_defcore      2018-04-19 02:45:46  zte-pod2    PASS
patrole               2018-04-19 02:50:04  zte-pod2    PASS
snaps_smoke           2018-04-19 03:40:52  zte-pod2    FAIL      SNAPS-283
neutron_trunk                              zte-pod2
cloudify_ims          2018-04-19 10:21:55  zte-pod2    PASS
vyos_vrouter          2018-04-19 10:55:06  zte-pod2    PASS
juju_epc              2018-04-19 11:42:43  zte-pod2    PASS
====================  ===================  ==========  ========  =========

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-19 19:45:23  zte-pod2    PASS
api_check             2018-04-19 19:56:46  zte-pod2    PASS
snaps_health_check    2018-04-19 19:57:30  zte-pod2    PASS
vping_ssh             2018-04-19 19:58:32  zte-pod2    PASS
vping_userdata        2018-04-19 20:08:02  zte-pod2    FAIL
tempest_smoke_serial  2018-04-16 14:56:12  zte-pod2    PASS
rally_sanity          2018-04-16 15:24:30  zte-pod2    PASS
refstack_defcore      2018-04-16 15:28:25  zte-pod2    PASS
patrole               2018-04-16 15:34:12  zte-pod2    FAIL
snaps_smoke           2018-04-16 16:28:34  zte-pod2    PASS      SNAPS-283
odl                   2018-04-16 15:34:33  zte-pod2    PASS
neutron_trunk                              zte-pod2
cloudify_ims          2018-04-19 20:39:49  zte-pod2    FAIL
vyos_vrouter          2018-04-19 21:46:06  zte-pod2    PASS
juju_epc              2018-04-19 22:14:27  zte-pod2    FAIL
====================  ===================  ==========  ========  =========
