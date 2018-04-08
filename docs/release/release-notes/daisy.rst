daisy
=====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-03 13:41:18  zte-pod2    PASS
api_check             2018-04-03 13:52:18  zte-pod2    PASS
snaps_health_check    2018-04-03 13:53:02  zte-pod2    PASS
vping_ssh             2018-04-03 13:55:21  zte-pod2    PASS
vping_userdata        2018-04-03 13:56:22  zte-pod2    PASS
tempest_smoke_serial  2018-04-03 14:12:18  zte-pod2    PASS
rally_sanity          2018-04-03 14:39:43  zte-pod2    PASS
refstack_defcore      2018-04-03 14:44:51  zte-pod2    PASS
patrole               2018-04-03 14:49:10  zte-pod2    PASS
snaps_smoke           2018-04-03 15:34:51  zte-pod2    FAIL      SNAPS-283
neutron_trunk                              zte-pod2
cloudify_ims          2018-04-03 15:47:44  zte-pod2    FAIL
vyos_vrouter          2018-04-03 15:58:55  zte-pod2    FAIL
juju_epc              2018-04-03 16:49:31  zte-pod2    PASS
====================  ===================  ==========  ========  =========

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-05 19:46:11  zte-pod2    PASS
api_check             2018-04-05 19:57:00  zte-pod2    PASS
snaps_health_check    2018-04-05 19:57:39  zte-pod2    PASS
vping_ssh             2018-04-05 20:00:05  zte-pod2    PASS
vping_userdata        2018-04-05 20:01:04  zte-pod2    PASS
tempest_smoke_serial  2018-04-05 20:17:48  zte-pod2    PASS
rally_sanity          2018-04-05 20:46:11  zte-pod2    PASS
refstack_defcore      2018-04-05 20:51:36  zte-pod2    PASS
patrole               2018-04-05 20:57:27  zte-pod2    PASS
snaps_smoke           2018-04-05 21:51:34  zte-pod2    PASS      SNAPS-283
odl                   2018-04-05 20:57:48  zte-pod2    PASS
neutron_trunk                              zte-pod2
====================  ===================  ==========  ========  =========
