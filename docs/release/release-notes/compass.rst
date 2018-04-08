compass
=======

os-nosdn-nofeature-ha
---------------------

====================  ===================  ===========  ========  ===========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  ===========
connection_check      2018-04-07 11:59:03  huawei-pod1  PASS
api_check             2018-04-07 12:09:28  huawei-pod1  PASS
snaps_health_check    2018-04-07 12:11:01  huawei-pod1  PASS
vping_ssh             2018-04-07 12:12:45  huawei-pod1  PASS
vping_userdata        2018-04-07 12:14:32  huawei-pod1  PASS
tempest_smoke_serial  2018-04-07 12:31:35  huawei-pod1  FAIL      COMPASS-588
rally_sanity          2018-04-07 13:00:49  huawei-pod1  PASS
refstack_defcore      2018-04-07 13:06:36  huawei-pod1  PASS
patrole               2018-04-07 13:10:05  huawei-pod1  PASS
snaps_smoke           2018-04-07 14:02:28  huawei-pod1  FAIL      SNAPS-283
neutron_trunk         2018-04-07 14:04:43  huawei-pod1  FAIL
cloudify_ims          2018-04-07 14:32:36  huawei-pod1  PASS
vyos_vrouter          2018-04-07 14:56:46  huawei-pod1  PASS
juju_epc              2018-04-07 15:52:35  huawei-pod1  PASS
====================  ===================  ===========  ========  ===========

os-odl_l3-nofeature-ha
----------------------

====================  ===================  ===========  ========  =========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  =========
connection_check      2018-04-04 08:53:18  huawei-pod1  PASS
api_check             2018-04-04 09:03:23  huawei-pod1  PASS
snaps_health_check    2018-04-04 09:03:59  huawei-pod1  PASS
vping_ssh             2016-07-23 20:21:55  huawei-pod1  PASS
vping_userdata        2018-04-04 09:04:43  huawei-pod1  PASS
tempest_smoke_serial  2018-04-04 09:21:20  huawei-pod1  FAIL
rally_sanity          2018-04-04 09:50:09  huawei-pod1  PASS
refstack_defcore      2018-04-04 09:52:32  huawei-pod1  PASS
patrole               2018-04-04 09:56:08  huawei-pod1  PASS
snaps_smoke           2018-04-04 10:48:07  huawei-pod1  FAIL      SNAPS-283
odl                   2018-04-04 09:56:30  huawei-pod1  PASS
neutron_trunk         2018-04-04 10:51:10  huawei-pod1  FAIL
====================  ===================  ===========  ========  =========

k8-nosdn-nofeature-ha
---------------------

===============  ===================  ===========  ========  ======
testcase         date                 pod_name     result    jira
===============  ===================  ===========  ========  ======
k8s_smoke        2018-04-07 05:46:58  huawei-pod1  PASS
k8s_conformance  2018-04-07 06:38:26  huawei-pod1  PASS
===============  ===================  ===========  ========  ======
