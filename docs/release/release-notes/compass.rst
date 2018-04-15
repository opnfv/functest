compass
=======

os-nosdn-nofeature-ha
---------------------

====================  ===================  ===========  ========  ===========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  ===========
connection_check      2018-04-14 05:35:25  huawei-pod2  PASS
api_check             2018-04-14 05:45:24  huawei-pod2  PASS
snaps_health_check    2018-04-14 05:46:56  huawei-pod2  PASS
vping_ssh             2018-04-14 05:49:30  huawei-pod2  PASS
vping_userdata        2018-04-14 05:51:26  huawei-pod2  PASS
tempest_smoke_serial  2018-04-14 06:07:47  huawei-pod2  FAIL      COMPASS-588
rally_sanity          2018-04-14 06:38:46  huawei-pod2  FAIL
refstack_defcore      2018-04-14 06:42:53  huawei-pod2  PASS
patrole               2018-04-14 06:46:46  huawei-pod2  PASS
snaps_smoke           2018-04-14 07:41:13  huawei-pod2  FAIL      SNAPS-283
neutron_trunk         2018-04-14 07:44:51  huawei-pod2  FAIL
cloudify_ims          2018-04-14 08:33:34  huawei-pod2  PASS
vyos_vrouter          2018-04-14 09:06:12  huawei-pod2  PASS
juju_epc              2018-04-14 10:03:04  huawei-pod2  PASS
====================  ===================  ===========  ========  ===========

os-odl_l3-nofeature-ha
----------------------

====================  ===================  ===========  ========  =========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  =========
connection_check      2018-04-13 16:09:09  huawei-pod2  PASS
api_check             2018-04-13 16:18:51  huawei-pod2  PASS
snaps_health_check    2018-04-13 16:19:30  huawei-pod2  PASS
vping_ssh                                  huawei-pod2
vping_userdata        2018-04-13 16:20:41  huawei-pod2  PASS
tempest_smoke_serial  2018-04-13 16:36:07  huawei-pod2  FAIL
rally_sanity          2018-04-13 17:07:48  huawei-pod2  FAIL
refstack_defcore      2018-04-13 17:11:26  huawei-pod2  PASS
patrole               2018-04-13 17:14:42  huawei-pod2  PASS
snaps_smoke           2018-04-13 18:00:18  huawei-pod2  FAIL      SNAPS-283
odl                   2018-04-13 17:15:03  huawei-pod2  PASS
neutron_trunk         2018-04-13 18:03:04  huawei-pod2  FAIL
cloudify_ims          2018-04-13 18:41:38  huawei-pod2  FAIL
vyos_vrouter          2018-04-13 19:14:34  huawei-pod2  PASS
juju_epc              2018-04-13 20:12:55  huawei-pod2  PASS
====================  ===================  ===========  ========  =========

k8-nosdn-nofeature-ha
---------------------

===============  ======  ===========  ========  ======
testcase         date    pod_name     result    jira
===============  ======  ===========  ========  ======
k8s_smoke                huawei-pod2
k8s_conformance          huawei-pod2
===============  ======  ===========  ========  ======
