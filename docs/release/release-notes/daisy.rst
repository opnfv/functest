daisy
=====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  =========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  =========
connection_check      2018-04-15 07:44:54  zte-pod2    PASS
api_check             2018-04-15 07:55:55  zte-pod2    PASS
snaps_health_check    2018-04-15 07:56:37  zte-pod2    PASS
vping_ssh             2018-04-15 07:59:05  zte-pod2    PASS
vping_userdata        2018-04-15 08:00:09  zte-pod2    PASS
tempest_smoke_serial  2018-04-15 08:16:22  zte-pod2    PASS
rally_sanity          2018-04-15 08:45:03  zte-pod2    PASS
refstack_defcore      2018-04-15 08:46:43  zte-pod2    PASS
patrole               2018-04-15 08:51:00  zte-pod2    PASS
snaps_smoke           2018-04-15 09:42:07  zte-pod2    PASS      SNAPS-283
neutron_trunk                              zte-pod2
cloudify_ims          2018-04-15 10:12:47  zte-pod2    PASS
vyos_vrouter          2018-04-14 10:35:53  zte-pod2    PASS
juju_epc              2018-04-14 11:22:46  zte-pod2    PASS
====================  ===================  ==========  ========  =========

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-04-14 16:45:45  zte-pod2    PASS
api_check             2018-04-14 16:56:56  zte-pod2    PASS
snaps_health_check    2018-04-14 16:57:38  zte-pod2    PASS
vping_ssh             2018-04-14 17:00:49  zte-pod2    FAIL
vping_userdata        2018-04-10 04:32:48  zte-pod2    FAIL
tempest_smoke_serial                       zte-pod2
rally_sanity                               zte-pod2
refstack_defcore                           zte-pod2
patrole                                    zte-pod2
snaps_smoke                                zte-pod2
odl                                        zte-pod2
neutron_trunk                              zte-pod2
cloudify_ims          2018-04-14 17:31:53  zte-pod2    PASS
vyos_vrouter          2018-04-14 17:54:41  zte-pod2    PASS
juju_epc              2018-04-14 18:47:30  zte-pod2    PASS
====================  ===================  ==========  ========  ======
