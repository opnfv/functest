#!/bin/bash

#This scripts correct the current ODL bug which does not detect
#when SFF and classifier are in the same swtich

nsp=`ovs-ofctl -O Openflow13 dump-flows br-int table=11 | \
grep "NXM_NX_NSP" | head -1 | cut -d',' -f13 | cut -d':' -f2 \
| cut -d'-' -f11`

ip=`ovs-ofctl -O Openflow13 dump-flows br-int table=11 | \
grep NXM_NX_NSH_C1 | head -1 | cut -d':' -f5 | cut -d'-' -f1`

output_port=`ovs-ofctl -O Openflow13 show br-int | \
grep vxgpe | cut -d'(' -f1`

output_port2=`echo $output_port`

echo "This is the nsp =$(($nsp))"
echo "This is the ip=$ip"
echo "This is the vxlan-gpe port=$output_port2"

ovs-ofctl -O Openflow13 del-flows br-int "table=11,tcp,reg0=0x1,tp_dst=80"
ovs-ofctl -O Openflow13 del-flows br-int "table=11,tcp,reg0=0x1,tp_dst=22"

ovs-ofctl -O Openflow13 add-flow br-int "table=11,tcp,reg0=0x1,tp_dst=80 \
actions=move:NXM_NX_TUN_ID[0..31]->NXM_NX_NSH_C2[],push_nsh,\
load:0x1->NXM_NX_NSH_MDTYPE[],load:0x3->NXM_NX_NSH_NP[],\
load:$ip->NXM_NX_NSH_C1[],load:$nsp->NXM_NX_NSP[0..23],\
load:0xff->NXM_NX_NSI[],load:$ip->NXM_NX_TUN_IPV4_DST[],\
load:$nsp->NXM_NX_TUN_ID[0..31],resubmit($output_port,0)"

ovs-ofctl -O Openflow13 add-flow br-int "table=11,tcp,reg0=0x1,tp_dst=22\
 actions=move:NXM_NX_TUN_ID[0..31]->NXM_NX_NSH_C2[],push_nsh,\
load:0x1->NXM_NX_NSH_MDTYPE[],load:0x3->NXM_NX_NSH_NP[],\
load:$ip->NXM_NX_NSH_C1[],load:$nsp->NXM_NX_NSP[0..23],\
load:0xff->NXM_NX_NSI[],load:$ip->NXM_NX_TUN_IPV4_DST[],\
load:$nsp->NXM_NX_TUN_ID[0..31],resubmit($output_port,0)"
