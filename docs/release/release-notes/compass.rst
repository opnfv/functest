compass
=======

os-nosdn-nofeature-ha
---------------------

====================  ===================  ===========  ========  ===========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  ===========
connection_check      2018-04-16 10:32:00  huawei-pod2  PASS
api_check             2018-04-16 10:42:10  huawei-pod2  PASS
snaps_health_check    2018-04-16 10:43:41  huawei-pod2  PASS
vping_ssh             2018-04-16 10:54:53  huawei-pod2  PASS
vping_userdata        2018-04-16 10:56:46  huawei-pod2  PASS
tempest_smoke_serial  2018-04-16 11:11:36  huawei-pod2  FAIL      COMPASS-588
rally_sanity          2018-04-16 11:42:15  huawei-pod2  FAIL
refstack_defcore      2018-04-16 11:45:51  huawei-pod2  PASS
patrole               2018-04-16 11:49:03  huawei-pod2  PASS
snaps_smoke           2018-04-16 12:43:49  huawei-pod2  FAIL      SNAPS-283
neutron_trunk         2018-04-16 12:47:05  huawei-pod2  FAIL
cloudify_ims          2018-04-16 13:41:07  huawei-pod2  PASS
vyos_vrouter          2018-04-16 14:17:44  huawei-pod2  PASS
juju_epc              2018-04-16 15:15:36  huawei-pod2  PASS
====================  ===================  ===========  ========  ===========

os-odl_l3-nofeature-ha
----------------------

====================  ===================  ===========  ========  =========
testcase              date                 pod_name     result    jira
====================  ===================  ===========  ========  =========
connection_check      2018-04-20 06:39:50  huawei-pod2  PASS
api_check             2018-04-20 06:49:03  huawei-pod2  PASS
snaps_health_check    2018-04-20 06:49:39  huawei-pod2  PASS
vping_ssh             2018-04-20 06:50:34  huawei-pod2  PASS
vping_userdata        2018-04-20 06:51:21  huawei-pod2  PASS
tempest_smoke_serial  2018-04-20 07:07:10  huawei-pod2  FAIL
rally_sanity          2018-04-20 07:47:15  huawei-pod2  FAIL
refstack_defcore      2018-04-20 07:50:58  huawei-pod2  FAIL
patrole               2018-04-20 07:54:17  huawei-pod2  PASS
snaps_smoke           2018-04-20 08:40:44  huawei-pod2  FAIL      SNAPS-283
odl                   2018-04-20 07:54:37  huawei-pod2  PASS
neutron_trunk         2018-04-20 08:43:31  huawei-pod2  FAIL
cloudify_ims          2018-04-18 05:38:50  huawei-pod2  PASS
vyos_vrouter          2018-04-18 06:13:30  huawei-pod2  PASS
juju_epc              2018-04-18 07:57:25  huawei-pod2  FAIL
====================  ===================  ===========  ========  =========

k8-nosdn-nofeature-ha
---------------------

===============  ======  ===========  ========  ======
testcase         date    pod_name     result    jira
===============  ======  ===========  ========  ======
k8s_smoke                huawei-pod2
k8s_conformance          huawei-pod2
===============  ======  ===========  ========  ======
