joid
====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ============  ========  =========
testcase              date                 pod_name      result    jira
====================  ===================  ============  ========  =========
connection_check      2018-04-19 08:34:42  huawei-pod12  PASS
api_check             2018-04-19 08:43:15  huawei-pod12  PASS
snaps_health_check    2018-04-19 08:43:44  huawei-pod12  PASS
vping_ssh             2018-04-19 08:45:12  huawei-pod12  PASS
vping_userdata        2018-04-19 08:46:31  huawei-pod12  PASS
tempest_smoke_serial  2018-04-19 09:01:29  huawei-pod12  FAIL
rally_sanity          2018-04-19 09:05:00  huawei-pod12  FAIL
refstack_defcore      2018-04-12 23:47:59  huawei-pod12  FAIL
patrole               2018-04-19 09:08:12  huawei-pod12  FAIL
snaps_smoke           2018-04-19 09:54:29  huawei-pod12  FAIL      SNAPS-283
neutron_trunk                              huawei-pod12
cloudify_ims          2018-04-19 09:57:23  huawei-pod12  FAIL
vyos_vrouter          2018-04-19 10:03:12  huawei-pod12  FAIL
juju_epc              2018-04-19 10:03:38  huawei-pod12  FAIL
====================  ===================  ============  ========  =========
