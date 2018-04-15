compass
=======

os-nosdn-nofeature-ha
---------------------

====================  ===================  ===========  ========  ===========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  ===========
connection_check      2018-04-13 20:46:32  huawei-pod1  PASS
api_check             2018-04-13 20:56:59  huawei-pod1  PASS
snaps_health_check    2018-04-13 20:58:35  huawei-pod1  PASS
vping_ssh             2018-04-13 21:11:39  huawei-pod1  PASS
vping_userdata        2018-04-13 21:13:38  huawei-pod1  PASS
tempest_smoke_serial  2018-04-13 21:31:50  huawei-pod1  FAIL      COMPASS-588
rally_sanity          2018-04-13 22:01:42  huawei-pod1  PASS
refstack_defcore      2018-04-13 22:02:34  huawei-pod1  FAIL
patrole               2018-04-13 22:05:52  huawei-pod1  FAIL
snaps_smoke           2018-04-13 22:59:22  huawei-pod1  FAIL      SNAPS-283
neutron_trunk         2018-04-13 23:25:34  huawei-pod1  FAIL
cloudify_ims          2018-04-13 23:57:49  huawei-pod1  PASS
vyos_vrouter          2018-04-14 00:21:46  huawei-pod1  PASS
juju_epc              2018-04-14 01:12:41  huawei-pod1  PASS
====================  ===================  ===========  ========  ===========

os-odl_l3-nofeature-ha
----------------------

====================  ===================  ===========  ========  =========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  =========
connection_check      2018-04-14 22:45:33  huawei-pod1  PASS
api_check             2018-04-14 22:55:50  huawei-pod1  PASS
snaps_health_check    2018-04-14 22:56:28  huawei-pod1  PASS
vping_ssh             2016-07-23 20:21:55  huawei-pod1  PASS
vping_userdata        2018-04-14 22:57:12  huawei-pod1  PASS
tempest_smoke_serial  2018-04-14 23:12:14  huawei-pod1  FAIL
rally_sanity          2018-04-14 23:40:56  huawei-pod1  PASS
refstack_defcore      2018-04-12 20:39:54  huawei-pod1  PASS
patrole               2018-04-14 23:43:29  huawei-pod1  PASS
snaps_smoke           2018-04-15 00:30:14  huawei-pod1  FAIL      SNAPS-283
odl                   2018-04-14 23:43:50  huawei-pod1  PASS
neutron_trunk         2018-04-15 00:33:17  huawei-pod1  FAIL
cloudify_ims          2018-04-15 00:40:27  huawei-pod1  FAIL
vyos_vrouter          2018-04-15 01:00:06  huawei-pod1  PASS
juju_epc              2018-04-15 01:49:55  huawei-pod1  PASS
====================  ===================  ===========  ========  =========

k8-nosdn-nofeature-ha
---------------------

===============  ===================  ===========  ========  ======
testcase         date                 pod_name     result    jira
===============  ===================  ===========  ========  ======
k8s_smoke        2018-04-13 10:27:28  huawei-pod1  PASS
k8s_conformance  2018-04-13 11:20:38  huawei-pod1  PASS
===============  ===================  ===========  ========  ======
