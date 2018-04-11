daisy
=====

os-nosdn-nofeature-ha
---------------------

====================  ======  ==========  ========  ======
testcase              date    pod_name    result    jira
====================  ======  ==========  ========  ======
connection_check              zte-pod2
api_check                     zte-pod2
snaps_health_check            zte-pod2
vping_ssh                     zte-pod2
vping_userdata                zte-pod2
tempest_smoke_serial          zte-pod2
rally_sanity                  zte-pod2
refstack_defcore              zte-pod2
patrole                       zte-pod2
snaps_smoke                   zte-pod2
neutron_trunk                 zte-pod2
cloudify_ims                  zte-pod2
vyos_vrouter                  zte-pod2
juju_epc                      zte-pod2
====================  ======  ==========  ========  ======

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-04-10 04:13:38  zte-pod2    PASS
api_check             2018-04-10 04:24:54  zte-pod2    PASS
snaps_health_check    2018-04-10 04:25:36  zte-pod2    PASS
vping_ssh             2018-04-10 04:28:12  zte-pod2    PASS
vping_userdata        2018-04-10 04:32:48  zte-pod2    FAIL
tempest_smoke_serial                       zte-pod2
rally_sanity                               zte-pod2
refstack_defcore                           zte-pod2
patrole                                    zte-pod2
snaps_smoke                                zte-pod2
odl                                        zte-pod2
neutron_trunk                              zte-pod2
cloudify_ims          2018-04-10 05:10:27  zte-pod2    PASS
vyos_vrouter          2018-04-10 05:34:30  zte-pod2    PASS
juju_epc              2018-04-10 06:26:16  zte-pod2    PASS
====================  ===================  ==========  ========  ======
