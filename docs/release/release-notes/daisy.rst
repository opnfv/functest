daisy
=====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-04-25 06:59:37  zte-pod2    PASS
api_check             2018-04-25 07:10:47  zte-pod2    PASS
snaps_health_check    2018-04-25 07:11:29  zte-pod2    PASS
vping_ssh             2018-04-25 07:12:35  zte-pod2    PASS
vping_userdata        2018-04-25 07:13:35  zte-pod2    PASS
tempest_smoke_serial  2018-04-25 07:29:32  zte-pod2    PASS
rally_sanity          2018-04-25 07:57:31  zte-pod2    PASS
refstack_defcore      2018-04-25 08:02:24  zte-pod2    PASS
patrole               2018-04-25 08:06:40  zte-pod2    PASS
snaps_smoke           2018-04-25 09:00:28  zte-pod2    PASS
neutron_trunk                              zte-pod2
cloudify_ims          2018-04-25 09:22:50  zte-pod2    FAIL
vyos_vrouter          2018-04-25 09:50:01  zte-pod2    PASS
juju_epc              2018-04-25 10:37:44  zte-pod2    PASS
====================  ===================  ==========  ========  ======

os-odl-nofeature-ha
-------------------

====================  ===================  ==========  ========  ======
testcase              date                 pod_name    result    jira
====================  ===================  ==========  ========  ======
connection_check      2018-04-24 21:22:19  zte-pod2    PASS
api_check             2018-04-24 21:33:28  zte-pod2    PASS
snaps_health_check    2018-04-24 21:34:09  zte-pod2    PASS
vping_ssh             2018-04-24 21:37:52  zte-pod2    PASS
vping_userdata        2018-04-24 21:38:54  zte-pod2    PASS
tempest_smoke_serial  2018-04-24 21:54:24  zte-pod2    PASS
rally_sanity          2018-04-24 22:22:44  zte-pod2    PASS
refstack_defcore      2018-04-24 22:28:32  zte-pod2    PASS
patrole               2018-04-24 22:34:25  zte-pod2    PASS
snaps_smoke           2018-04-24 23:24:54  zte-pod2    FAIL
odl                   2018-04-24 22:34:46  zte-pod2    PASS
neutron_trunk                              zte-pod2
cloudify_ims          2018-04-25 00:00:01  zte-pod2    FAIL
vyos_vrouter          2018-04-25 01:34:52  zte-pod2    PASS
juju_epc              2018-04-25 02:03:48  zte-pod2    FAIL
====================  ===================  ==========  ========  ======
