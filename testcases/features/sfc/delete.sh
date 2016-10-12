tacker sfc-classifier-delete red_http
tacker sfc-classifier-delete blue_ssh
tacker sfc-classifier-delete red_ssh
tacker sfc-classifier-delete blue_http
tacker sfc-delete red
tacker sfc-delete blue
tacker vnf-delete testVNF1
tacker vnf-delete testVNF2
tacker vnfd-delete test-vnfd1
tacker vnfd-delete test-vnfd2
openstack stack delete sfc --y
openstack stack delete sfc_test1 --y
openstack stack delete sfc_test2 --y
nova delete client
nova delete server
