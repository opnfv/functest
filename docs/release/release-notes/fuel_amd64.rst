fuel(amd64)
===========

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ========
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ========
connection_check      2018-04-10 15:10:37  lf-pod2     PASS
api_check             2018-04-10 15:19:08  lf-pod2     PASS
snaps_health_check    2018-04-10 15:19:45  lf-pod2     PASS
vping_ssh             2018-04-10 15:21:03  lf-pod2     PASS
vping_userdata        2018-04-10 15:22:02  lf-pod2     PASS
tempest_smoke_serial  2018-04-10 15:35:32  lf-pod2     PASS
rally_sanity          2018-04-10 15:58:23  lf-pod2     PASS
refstack_defcore      2018-04-10 16:04:52  lf-pod2     PASS
patrole               2018-04-10 16:09:07  lf-pod2     PASS
snaps_smoke           2018-04-10 16:59:13  lf-pod2     FAIL      FUEL-356
neutron_trunk         2018-04-10 17:01:18  lf-pod2     PASS
cloudify_ims          2018-04-10 17:20:27  lf-pod2     FAIL
vyos_vrouter          2018-04-10 17:37:46  lf-pod2     FAIL
juju_epc              2018-04-10 17:46:10  lf-pod2     FAIL
====================  ===================  ==========  ========  ========

os-odl-nofeature-ha
-------------------

====================  ======  ==========  ========  ======
testcase              date    pod_name    result    jira
====================  ======  ==========  ========  ======
connection_check              lf-pod2
api_check                     lf-pod2
snaps_health_check            lf-pod2
vping_ssh                     lf-pod2
vping_userdata                lf-pod2
tempest_smoke_serial          lf-pod2
rally_sanity                  lf-pod2
refstack_defcore              lf-pod2
patrole                       lf-pod2
snaps_smoke                   lf-pod2
odl                           lf-pod2
neutron_trunk                 lf-pod2
cloudify_ims                  lf-pod2
vyos_vrouter                  lf-pod2
juju_epc                      lf-pod2
====================  ======  ==========  ========  ======
