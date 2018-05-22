joid
====

os-nosdn-nofeature-ha
---------------------

====================  ===================  ============  ========  ======
testcase              date                 pod_name      result    jira
====================  ===================  ============  ========  ======
connection_check      2018-05-22 04:57:59  huawei-pod12  PASS
api_check             2018-05-22 05:06:12  huawei-pod12  FAIL
snaps_health_check    2018-05-15 07:19:15  huawei-pod12  PASS
vping_ssh             2018-05-15 07:21:35  huawei-pod12  PASS
vping_userdata        2018-05-15 07:22:42  huawei-pod12  PASS
tempest_smoke_serial  2018-05-15 07:39:10  huawei-pod12  FAIL
rally_sanity          2018-05-15 07:42:31  huawei-pod12  FAIL
refstack_defcore      2018-05-15 07:46:01  huawei-pod12  FAIL
patrole               2018-05-15 07:48:54  huawei-pod12  FAIL
snaps_smoke           2018-05-15 09:11:53  huawei-pod12  FAIL
neutron_trunk                              huawei-pod12
cloudify_ims          2018-05-15 09:30:34  huawei-pod12  FAIL
vyos_vrouter          2018-05-15 09:59:30  huawei-pod12  FAIL
juju_epc              2018-05-15 10:02:02  huawei-pod12  FAIL
====================  ===================  ============  ========  ======
