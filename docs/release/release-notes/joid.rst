joid
====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ============  ========  =========
testcase              date                 pod_name      result    jira
====================  ===================  ============  ========  =========
connection_check      2018-03-27 21:43:25  huawei-pod12  PASS
api_check             2018-03-27 21:51:36  huawei-pod12  PASS
snaps_health_check    2018-03-27 21:52:05  huawei-pod12  PASS
vping_ssh             2018-03-27 21:53:37  huawei-pod12  PASS
vping_userdata        2018-03-27 21:55:08  huawei-pod12  PASS
tempest_smoke_serial  2018-03-27 22:10:05  huawei-pod12  FAIL
rally_sanity          2018-03-27 22:13:28  huawei-pod12  FAIL
refstack_defcore      2018-03-27 22:17:14  huawei-pod12  FAIL
patrole               2018-03-27 22:20:18  huawei-pod12  FAIL
snaps_smoke           2018-03-27 23:03:54  huawei-pod12  FAIL      SNAPS-283
neutron_trunk                              huawei-pod12
cloudify_ims          2018-03-27 23:06:48  huawei-pod12  FAIL
vyos_vrouter          2018-03-27 23:15:54  huawei-pod12  FAIL
juju_epc              2018-03-27 23:16:20  huawei-pod12  FAIL
====================  ===================  ============  ========  =========
