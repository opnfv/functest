compass
=======

os-nosdn-nofeature-ha
---------------------

====================  ===================  ===========  ========  ===========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  ===========
connection_check      2018-04-20 08:11:02  huawei-pod1  PASS
api_check             2018-04-18 05:41:29  huawei-pod1  PASS
snaps_health_check    2018-04-18 05:43:03  huawei-pod1  PASS
vping_ssh             2018-04-18 05:45:33  huawei-pod1  PASS
vping_userdata        2018-04-18 05:47:28  huawei-pod1  PASS
tempest_smoke_serial  2018-04-18 06:03:52  huawei-pod1  FAIL      COMPASS-588
rally_sanity          2018-04-18 06:33:29  huawei-pod1  PASS
refstack_defcore      2018-04-13 22:02:34  huawei-pod1  FAIL
patrole               2018-04-18 06:36:42  huawei-pod1  PASS
snaps_smoke           2018-04-18 07:30:19  huawei-pod1  FAIL      SNAPS-283
neutron_trunk         2018-04-18 07:33:57  huawei-pod1  FAIL
cloudify_ims          2018-04-18 08:19:27  huawei-pod1  PASS
vyos_vrouter          2018-04-18 08:45:36  huawei-pod1  PASS
juju_epc              2018-04-18 11:15:12  huawei-pod1  FAIL
====================  ===================  ===========  ========  ===========

os-odl_l3-nofeature-ha
----------------------

====================  ===================  ===========  ========  =========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  =========
connection_check      2018-04-17 03:03:00  huawei-pod1  PASS
api_check             2018-04-17 03:13:00  huawei-pod1  PASS
snaps_health_check    2018-04-17 03:13:37  huawei-pod1  PASS
vping_ssh             2018-04-17 03:14:32  huawei-pod1  PASS
vping_userdata        2018-04-17 03:15:24  huawei-pod1  PASS
tempest_smoke_serial  2018-04-17 03:31:19  huawei-pod1  FAIL
rally_sanity          2018-04-17 04:00:16  huawei-pod1  PASS
refstack_defcore      2018-04-12 20:39:54  huawei-pod1  PASS
patrole               2018-04-17 04:02:52  huawei-pod1  PASS
snaps_smoke           2018-04-17 04:52:31  huawei-pod1  FAIL      SNAPS-283
odl                   2018-04-17 04:03:13  huawei-pod1  PASS
neutron_trunk         2018-04-17 04:55:37  huawei-pod1  FAIL
cloudify_ims          2018-04-17 05:25:17  huawei-pod1  PASS
vyos_vrouter          2018-04-17 05:51:12  huawei-pod1  PASS
juju_epc              2018-04-17 06:53:35  huawei-pod1  PASS
====================  ===================  ===========  ========  =========

k8-nosdn-nofeature-ha
---------------------

===============  ===================  ===========  ========  ======
testcase         date                 pod_name     result    jira
===============  ===================  ===========  ========  ======
k8s_smoke        2018-04-17 19:28:56  huawei-pod1  FAIL
k8s_conformance  2018-04-17 19:44:09  huawei-pod1  FAIL
===============  ===================  ===========  ========  ======
