#!/usr/bin/python

from optparse import OptionParser
import os
import fileinput
import re


BASEDIR='.'
RESULTS_DIR='/home/opnfv/functest/results/odl/'
REPO_DIR='/home/opnfv/repos/odl_integration'

# Colors
class colors:
    green='\033[0;32m'
    light_green='\033[1;32m'
    red='\033[1;31m'
    nc='\033[0m' # No Color

def replace_string(str,replace_str,input_file):
    with open(input_file, 'r') as fd:
        read_lines=fd.readlines()
        fd.close()
        with open(input_file, 'w') as fd:
            for line in read_lines:
                fd.write(re.sub(str, replace, line))

def copy_testfiles(src,dst):
    for item in os.listdir(src):
	s=os.path.join(src,item)
	d=os.path.join(dst,item)
	if os.path.isdir(s):
	    shutil.copytree(s,d,False)
	else:
	    shutil.copy2(s,d)

if __name__ == "__main__":
    parser = OptionParser(usage=colors.red+"usage: %prog --odl_port $odl_port --odl_ip $odl_ip --neutron_ip $neutron_ip --usr_name $usr_name --pass $pass"+colors.nc,version="%prog 1.0")
    parser.add_option('--odl_ip', dest='odlip',help='opendaylight ip address',default='192.168.1.5')
    parser.add_option('--odl_port',dest='odlport', help='opendaylight port ',default='8081')
    parser.add_option('--usr_name', dest='odluser',help='opendayligt username',default='neutron')
    parser.add_option('----pass', dest='odlpasswd',help='opendaylight password',default='octopus')
    parser.add_option('--neutron_ip',dest='neutronip', help='neutron service ip address',default='192.168.0.68')
    (options, args) = parser.parse_args()
    print colors.green+'Current environment parameters for ODL suite.'+colors.nc
    odl_passwd=options.odlpasswd
    odl_ip=options.odlip
    odl_port=options.oplport
    odl_user=options.odluser
    odl_neutronip=options.neutronip

    input_file = REPO_DIR+'/test/csit/suites/openstack/neutron/__init__.robot'
    search_string='"password": ".*"'
    replaceble_string='"password": "'+odl_passwd+'"'
    replace_string(search_string,replaceble_string,input_file)

    search_string='^Documentation.*'
    replaceble_string='a Suite Teardown     Stop Suite'
    replace_string(search_string,replaceble_string,input_file)

    search_string='^Documentation.*'
    replaceble_string='a Suite Setup        Start Suite'
    replace_string(search_string,replaceble_string,input_file)

    print colors.green+'Copy custom tests to suite.'+colors.nc
    copy_testfiles(BASEDIR+'/custom_tests/neutron/',REPO_DIR+'/test/csit/suites/openstack/neutron/')

    test_num=1
    rebot_params=""
    test_file=BASEDIR+'/test_list.txt'
    print colors.green+'Executing chosen tests.'+colors.nc
    with open(test_file,'r') as fd:
	test_dir=fd.read()
	test_dir_list=test_dir.split('\n')
    for test_suite in test_dir:
	if test_suite[0] != '#' and len(test_suite)!=0:
	    print colors.light_green+'Starting test: '+test_suite+colors.line
	    cmd='pybot -v OPENSTACK:'+odl_neutronip+' -v PORT:'+odl_port+' -v CONTROLLER:'+odl_ip+' '+REPO_DIR+test_suite
	    os.system(cmd)
	    res_dir=RESULTS_DIR+'/logs/'+test_num
	    os.mkdir(res_dir)
	    shutil.move('log.html',res_dir+'/log.html')
	    shutil.move('report.html',res_dir+'/report.html')
	    shutil.move('output.xml',res_dir+'/output.xml')
	    test_num=test_num+1
    for i in range(1,test_num+1):
        robot_params+=RESULTS_DIR+'/logs/'+i+'/output.xml'
    print colors.green+"Final Output is located in "+colors.nc
    os.system('rebot '+robot_params)