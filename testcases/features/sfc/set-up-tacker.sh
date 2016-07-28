curl "https://gerrit.opnfv.org/gerrit/gitweb?p=fuel.git;a=blob_plain;f=prototypes/sfc_tacker/poc.tacker-up.sh;hb=794427a06b46fddecb76b60c8392e37ae504ab60" > poc.tacker-up.sh
bash poc.tacker-up.sh

touch delete.sh

cat <<EOF > delete.sh
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
#openstack stack delete sfc --y
heat stack-delete sfc
#openstack stack delete sfc_test1 --y
heat stack-delete sfc_test1
#openstack stack delete sfc_test2 --y
heat stack-delete sfc_test2
EOF

chmod +x delete.sh

source tackerc
openstack flavor create custom --ram 1500 --disk 10 --public
