#!/usr/bin/python

from optparse import OptionParser
import os

BASEDIR='.'
RESULTS_DIR='/home/opnfv/functest/results/odl/'
REPO_DIR='/home/opnfv/repos/odl_integration'

# Colors
class colors:
    green='\033[0;32m'
    light_green='\033[1;32m'
    red='\033[1;31m'
    nc='\033[0m' # No Color

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog --odl_port $odl_port --odl_ip $odl_ip --neutron_ip $neutron_ip --usr_name $usr_name --pass $pass",version="%prog 1.0")
    parser.add_option('--odl_ip', dest='odlip',help='opendaylight ip address',default='192.168.1.5')
    parser.add_option('--odl_port',dest='odlport', help='opendaylight port ',default='8081')
    parser.add_option('--usr_name', dest='odluser',help='opendayligt username',default='neutron')
    parser.add_option('----pass', dest='odlpasswd',help='opendaylight password',default='octopus')
    parser.add_option('--neutron_ip',dest='neutronip', help='neutron service ip address',default='192.168.0.68')
    (options, args) = parser.parse_args()

    odl_passwd=options.odlpasswd
    odl_ip=options.odlip
    odl_port=options.oplport
    odl_user=options.odluser
    odl_neutronip=options.neutronip

    cmd='sed -i "s/\"password\": \".*\"/\"password\": \"${'+odl_passwd+'}\"/" ${'+REPO_DIR+'}/test/csit/suites/openstack/neutron/__init__.robot'
    os.system(cmd)
    cmd='sed -i "/^Documentation.*/a Suite Teardown     Stop Suite" ${'+REPO_DIR+'}/test/csit/suites/openstack/neutron/__init__.robot'
    os.system(cmd)
    os.system(cmd)
    cmd='sed -i "/^Documentation.*/a Suite Setup        Start Suite" ${'+REPO_DIR+'}/test/csit/suites/openstack/neutron/__init__.robot'
    os.system(cmd)
    cmd='cp -vf ${'+BASEDIR+'}/custom_tests/neutron/* ${'+REPO_DIR+'}/test/csit/suites/openstack/neutron/'
    os.system(cmd)

    test_num=0
    rebot_params=""
    test_file=BASEDIR+'/test_list.txt'
    fd=open(test_file,"r")
    testcases = [line.rstrip('\n') for line in open(test_file)]
    for each_test in testcases:
        if each_test[0] == "#" :
            pass
        elif each_test == "":
            pass
        else :
            print 'Starting test case :'+ each_test
            cmd='pybot -v OPENSTACK:${'+odl_neutronip+'} -v PORT:${'+odl_port+'} -v CONTROLLER:${'+odl_ip+'} ${'+REPO_DIR+'}/$'+each_test
            os.system(cmd)
            test_num=test_num+1
            res_dir=RESULTS_DIR+'/logs/'+test_num
            cmd='mkdir -p '+res_dir
            os.system(cmd)
            cmd='mv log.html '+res_dir
            os.system(cmd)
            cmd='mv report.html  '+res_dir
            os.system(cmd)
            cmd='mv output.xml '+res_dir
            os.system(cmd)
    for i in range(0,test_num):
        rebot_params=rebot_params+RESULTS_DIR+'/logs/'+i+'/output.xml'

    cmd='rebot '+rebot_params
    os.system(cmd)
