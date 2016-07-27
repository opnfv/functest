apt-get install git -y
git clone https://gerrit.opnfv.org/gerrit/fuel
pushd fuel
git fetch https://gerrit.opnfv.org/gerrit/fuel refs/changes/65/15065/5 && git checkout FETCH_HEAD
popd
mv fuel/prototypes/sfc_tacker/poc.tacker-up.sh .
sleep 3
bash poc.tacker-up.sh

touch delete.sh

echo "
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
" >> delete.sh

chmod +x delete.sh

source tackerc
openstack flavor create custom --ram 1500 --disk 10 --public
