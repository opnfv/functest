joid
====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ============  ========  =========
testcase              date                 pod_name      result    jira
====================  ===================  ============  ========  =========
connection_check      2018-04-18 05:46:23  huawei-pod12  PASS
api_check             2018-04-18 05:54:49  huawei-pod12  PASS
snaps_health_check    2018-04-18 05:55:19  huawei-pod12  PASS
vping_ssh             2018-04-18 05:59:46  huawei-pod12  PASS
vping_userdata        2018-04-18 06:01:02  huawei-pod12  PASS
tempest_smoke_serial  2018-04-18 06:15:48  huawei-pod12  FAIL
rally_sanity          2018-04-18 06:19:19  huawei-pod12  FAIL
refstack_defcore      2018-04-18 06:23:35  huawei-pod12  FAIL
patrole               2018-04-18 06:26:57  huawei-pod12  FAIL
snaps_smoke           2018-04-18 07:10:31  huawei-pod12  FAIL      SNAPS-283
neutron_trunk                              huawei-pod12
cloudify_ims          2018-04-18 07:34:50  huawei-pod12  FAIL
vyos_vrouter          2018-04-18 07:41:21  huawei-pod12  FAIL
juju_epc              2018-04-18 07:41:47  huawei-pod12  FAIL
====================  ===================  ============  ========  =========
