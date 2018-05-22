compass
=======

os-nosdn-nofeature-ha
---------------------

====================  ===================  ===========  ========  ===========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  ===========
connection_check      2018-05-12 02:32:04  huawei-pod2  PASS
api_check             2018-05-12 02:42:02  huawei-pod2  PASS
snaps_health_check    2018-05-12 02:43:35  huawei-pod2  PASS
vping_ssh             2018-05-12 02:48:02  huawei-pod2  PASS
vping_userdata        2018-05-12 02:49:57  huawei-pod2  PASS
tempest_smoke_serial  2018-05-12 03:06:53  huawei-pod2  PASS
rally_sanity          2018-05-12 03:37:35  huawei-pod2  FAIL      COMPASS-597
refstack_defcore      2018-05-12 03:41:38  huawei-pod2  PASS
patrole               2018-05-12 03:44:51  huawei-pod2  PASS
snaps_smoke           2018-05-12 04:38:44  huawei-pod2  PASS
neutron_trunk         2018-05-12 04:41:22  huawei-pod2  PASS
cloudify_ims          2018-05-12 05:27:20  huawei-pod2  PASS
vyos_vrouter          2018-05-12 05:56:23  huawei-pod2  PASS
juju_epc              2018-05-12 06:52:00  huawei-pod2  PASS
====================  ===================  ===========  ========  ===========

os-odl_l3-nofeature-ha
----------------------

====================  ===================  ===========  ========  ======
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  ======
connection_check      2018-05-15 04:50:53  huawei-pod2  PASS
api_check             2018-05-15 05:00:21  huawei-pod2  PASS
snaps_health_check    2018-05-15 05:00:58  huawei-pod2  PASS
vping_ssh             2018-05-15 05:01:54  huawei-pod2  PASS
vping_userdata        2018-05-15 05:02:44  huawei-pod2  PASS
tempest_smoke_serial  2018-05-15 05:17:21  huawei-pod2  FAIL
rally_sanity          2018-05-15 05:18:36  huawei-pod2  FAIL
refstack_defcore      2018-05-15 05:22:04  huawei-pod2  FAIL
patrole               2018-05-15 05:25:59  huawei-pod2  PASS
snaps_smoke           2018-05-15 06:14:17  huawei-pod2  FAIL
odl                   2018-05-15 05:26:20  huawei-pod2  PASS
neutron_trunk         2018-05-15 06:17:16  huawei-pod2  PASS
cloudify_ims          2018-05-15 06:46:27  huawei-pod2  FAIL
vyos_vrouter          2018-05-15 07:26:23  huawei-pod2  PASS
juju_epc              2018-05-15 08:23:53  huawei-pod2  PASS
====================  ===================  ===========  ========  ======

k8-nosdn-nofeature-ha
---------------------

===============  ======  ===========  ========  ======
testcase         date    pod_name     result    jira
===============  ======  ===========  ========  ======
k8s_smoke                huawei-pod2
k8s_conformance          huawei-pod2
===============  ======  ===========  ========  ======
