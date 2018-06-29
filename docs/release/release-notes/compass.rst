compass
=======

os-nosdn-nofeature-ha
---------------------

====================  ===================  ===========  ========  ===========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  ===========
connection_check      2018-06-29 11:56:27  huawei-pod2  PASS
api_check             2018-06-29 12:06:41  huawei-pod2  PASS
snaps_health_check    2018-06-29 12:08:13  huawei-pod2  PASS
vping_ssh             2018-06-29 12:10:13  huawei-pod2  PASS
vping_userdata        2018-06-29 12:11:59  huawei-pod2  PASS
tempest_smoke_serial  2018-06-29 12:28:07  huawei-pod2  FAIL
rally_sanity          2018-06-29 12:58:42  huawei-pod2  FAIL      COMPASS-597
refstack_defcore      2018-06-29 13:02:37  huawei-pod2  PASS
patrole               2018-06-29 13:05:45  huawei-pod2  PASS
snaps_smoke           2018-06-29 14:00:12  huawei-pod2  PASS
neutron_trunk         2018-06-29 14:03:35  huawei-pod2  PASS
cloudify_ims          2018-06-29 15:18:53  huawei-pod2  FAIL
vyos_vrouter          2018-06-27 19:06:55  huawei-pod2  PASS
juju_epc              2018-06-27 19:55:47  huawei-pod2  PASS
====================  ===================  ===========  ========  ===========

os-odl_l3-nofeature-ha
----------------------

====================  ===================  ===========  ========  ======
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  ======
connection_check      2018-06-29 01:17:01  huawei-pod2  PASS
api_check             2018-06-29 01:27:17  huawei-pod2  PASS
snaps_health_check    2018-06-29 01:28:19  huawei-pod2  FAIL
vping_ssh             2018-06-27 03:58:19  huawei-pod2  PASS
vping_userdata        2018-06-27 03:58:58  huawei-pod2  PASS
tempest_smoke_serial  2018-06-25 03:18:29  huawei-pod2  FAIL
rally_sanity          2018-06-25 03:19:34  huawei-pod2  FAIL
refstack_defcore      2018-06-25 03:23:02  huawei-pod2  PASS
patrole               2018-06-25 03:26:15  huawei-pod2  PASS
snaps_smoke           2018-06-25 04:13:18  huawei-pod2  FAIL
odl                   2018-05-15 05:26:20  huawei-pod2  PASS
neutron_trunk         2018-06-25 04:15:59  huawei-pod2  PASS
cloudify_ims          2018-06-27 05:08:03  huawei-pod2  FAIL
vyos_vrouter          2018-06-27 05:32:53  huawei-pod2  PASS
juju_epc              2018-06-27 06:18:50  huawei-pod2  PASS
====================  ===================  ===========  ========  ======

k8-nosdn-nofeature-ha
---------------------

===============  ======  ===========  ========  ======
testcase         date    pod_name     result    jira
===============  ======  ===========  ========  ======
k8s_smoke                huawei-pod2
k8s_conformance          huawei-pod2
===============  ======  ===========  ========  ======
