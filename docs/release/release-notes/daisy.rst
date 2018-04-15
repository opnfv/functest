daisy
=====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-12 13:45:13  zte-pod2    PASS
api_check             2018-04-12 13:55:54  zte-pod2    PASS
snaps_health_check    2018-04-12 13:56:33  zte-pod2    PASS
vping_ssh             2018-04-12 13:58:58  zte-pod2    PASS
vping_userdata        2018-04-12 13:59:54  zte-pod2    PASS
tempest_smoke_serial  2018-04-12 14:15:24  zte-pod2    PASS
rally_sanity          2018-04-12 14:43:18  zte-pod2    PASS
refstack_defcore      2018-04-12 14:49:02  zte-pod2    PASS
patrole               2018-04-12 14:53:20  zte-pod2    PASS
snaps_smoke           2018-04-12 15:42:14  zte-pod2    PASS      SNAPS-283
neutron_trunk                              zte-pod2
cloudify_ims          2018-04-12 16:14:40  zte-pod2    PASS
vyos_vrouter          2018-04-12 16:37:09  zte-pod2    PASS
juju_epc              2018-04-12 17:29:07  zte-pod2    PASS
====================  ===================  ==========  ========  =========

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-12 20:58:36  zte-pod2    PASS
api_check             2018-04-12 21:09:58  zte-pod2    PASS
snaps_health_check    2018-04-12 21:10:36  zte-pod2    PASS
vping_ssh             2018-04-12 21:12:56  zte-pod2    PASS
vping_userdata        2018-04-12 21:14:03  zte-pod2    PASS
tempest_smoke_serial  2018-04-12 21:37:11  zte-pod2    FAIL
rally_sanity          2018-04-12 22:06:49  zte-pod2    PASS
refstack_defcore      2018-04-12 22:11:48  zte-pod2    PASS
patrole               2018-04-12 22:39:08  zte-pod2    FAIL
snaps_smoke           2018-04-12 00:34:53  zte-pod2    FAIL      SNAPS-283
odl                   2018-04-12 22:40:09  zte-pod2    FAIL
neutron_trunk                              zte-pod2
cloudify_ims          2018-04-12 22:48:35  zte-pod2    FAIL
vyos_vrouter          2018-04-12 22:49:39  zte-pod2    FAIL
juju_epc              2018-04-12 22:50:43  zte-pod2    FAIL
====================  ===================  ==========  ========  =========
