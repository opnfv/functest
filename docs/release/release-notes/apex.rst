apex
====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-04-10 19:08:51  lf-pod1     PASS
api_check             2018-04-10 19:21:53  lf-pod1     PASS
snaps_health_check    2018-04-10 19:22:37  lf-pod1     PASS
vping_ssh             2018-04-10 19:24:52  lf-pod1     PASS
vping_userdata        2018-04-10 19:26:01  lf-pod1     PASS
tempest_smoke_serial  2018-04-10 19:41:43  lf-pod1     PASS
rally_sanity                               lf-pod1
refstack_defcore                           lf-pod1
patrole                                    lf-pod1
snaps_smoke                                lf-pod1
neutron_trunk                              lf-pod1
cloudify_ims                               lf-pod1
vyos_vrouter                               lf-pod1
juju_epc                                   lf-pod1
====================  ===================  ==========  ========  ======

os-odl-nofeature-ha
-------------------

====================  ======  ==========  ========  ======
testcase              date    pod_name    result    jira
====================  ======  ==========  ========  ======
connection_check              lf-pod1
api_check                     lf-pod1
snaps_health_check            lf-pod1
vping_ssh                     lf-pod1
vping_userdata                lf-pod1
tempest_smoke_serial          lf-pod1
rally_sanity                  lf-pod1
refstack_defcore              lf-pod1
patrole                       lf-pod1
snaps_smoke                   lf-pod1
odl                           lf-pod1
neutron_trunk                 lf-pod1
cloudify_ims                  lf-pod1
vyos_vrouter                  lf-pod1
juju_epc                      lf-pod1
====================  ======  ==========  ========  ======
