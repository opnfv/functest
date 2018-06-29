joid
====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ============  ========  ======
testcase              date                 pod_name      result    jira
====================  ===================  ============  ========  ======
connection_check      2018-06-07 04:28:49  huawei-pod12  PASS
api_check             2018-06-07 04:36:58  huawei-pod12  FAIL
snaps_health_check    2018-05-31 05:15:29  huawei-pod12  PASS
vping_ssh             2018-05-31 05:16:39  huawei-pod12  PASS
vping_userdata        2018-05-31 05:17:44  huawei-pod12  PASS
tempest_smoke_serial  2018-05-31 05:32:11  huawei-pod12  FAIL
rally_sanity          2018-05-31 05:35:31  huawei-pod12  FAIL
refstack_defcore      2018-05-31 05:44:03  huawei-pod12  FAIL
patrole               2018-05-31 05:47:21  huawei-pod12  FAIL
snaps_smoke           2018-05-31 06:28:48  huawei-pod12  FAIL
neutron_trunk                              huawei-pod12
cloudify_ims          2018-05-31 06:29:11  huawei-pod12  FAIL
vyos_vrouter          2018-05-31 06:29:19  huawei-pod12  FAIL
juju_epc              2018-05-31 06:29:27  huawei-pod12  FAIL
====================  ===================  ============  ========  ======
