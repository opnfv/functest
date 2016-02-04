Executing the functest suites
=============================

Manual testing
--------------

Once the Functest docker container is running and Functest environment ready
(through /home/opnfv/repos/functest/docker/prepare_env.sh script), the system is
ready to run the tests.

The script *run_tests.sh* is located in $repos_dir/functest/docker and it has
several options::

    ./run_tests.sh -h
    Script to trigger the tests automatically.

    usage:
        bash run_tests.sh [--offline] [-h|--help] [-t <test_name>]

    where:
        -h|--help         show this help text
        -r|--report       push results to database (false by default)
        -n|--no-clean     do not clean up OpenStack resources after test run
        -t|--test         run specific set of tests
          <test_name>     one or more of the following: vping,vping_userdata,odl,rally,tempest,vims,onos,promise. Separated by comma.

    examples:
        run_tests.sh
        run_tests.sh --test vping,odl
        run_tests.sh -t tempest,rally --no-clean

The *-r* option is used by the Continuous Integration in order to push the test
results into a test collection database, see in next section for details.
In manual mode, you must not use it, your try will be anyway probably rejected
as your POD must be declared in the database to collect the data.

The *-n* option is used for preserving all the existing OpenStack resources after
execution test cases.

The *-t* option can be used to specify the list of test you want to launch, by
default Functest will try to launch all its test suites in the following order
vPing, odl, Tempest, vIMS, Rally.
You may launch only one single test by using *-t <the test you want to launch>*.

Within Tempest test suite you can define which test cases you want to execute in
your environment by editing test_list.txt file before executing *run_tests.sh*
script.

Please note that Functest includes cleaning mechanism in order to remove
everything except what was present after a fresh install.
If you create your own VMs, tenants, networks etc. and then launch Functest,
they all will be deleted after executing the tests. Use the *--no-clean* option with
run_test.sh in order to preserve all the existing resources.
However, be aware that Tempest and Rally create of lot of resources (users,
tenants, networks, volumes etc.) that are not always properly cleaned, so this
cleaning function has been set to keep the system as clean as possible after a
full Functest run.

You may also add you own test by adding a section into the function run_test().


Automated testing
-----------------

As mentioned in `[1]`, the *prepare-env.sh* and *run_test.sh* can be executed within
the container from jenkins.
2 jobs have been created, one to run all the test and one that allows testing
test suite by test suite.
You thus just have to launch the acurate jenkins job on the target lab, all the
tests shall be automatically run.

When the tests are automatically started from CI, a basic algorithm has been
created in order to detect whether the test is runnable or not on the given
scenario.
In fact, one of the most challenging task in Brahmaputra consists in dealing
with lots of scenario and installers.
Functest test suites cannot be systematically run (e.g. run the ODL suite on an
ONOS scenario).

CI provides several information:

 * The installer (apex|compass|fuel|joid)
 * The scenario [controller]-[feature]-[mode] with

   * controller = (odl|onos|ocl|nosdn)
   * feature = (ovs(dpdk)|kvm)
   * mode = (ha|noha)

Constraints per test case are defined in the Functest configuration file
/home/opnfv/functest/config/config_functest.yaml::

 test-dependencies:
    functest:
        vims:
            scenario: '(ocl)|(odl)|(nosdn)'
        vping:
        vping_userdata:
            scenario: '(ocl)|(odl)|(nosdn)'
        tempest:
        rally:
        odl:
            scenario: 'odl'
        onos:
            scenario: 'onos'
        ....

At the end of the Functest environment creation (prepare_env.sh see `[1]`_), a
file (/home/opnfv/functest/conf/testcase-list.txt) is created with the list of
all the runnable tests.
We consider the static constraints as regex and compare them with the scenario.
For instance, odl can be run only on scenario including odl in its name.

The order of execution is also described in the Functest configuration file::

 test_exec_priority:

    1: vping
    2: vping_userdata
    3: tempest
    4: odl
    5: onos
    6: ovno
    7: doctor
    8: promise
    9: odl-vpnservice
    10: bgpvpn
    11: openstack-neutron-bgpvpn-api-extension-tests
    12: vims
    13: rally

The tests are executed as follow:

 * Basic scenario (vPing, vPing_userdata, Tempest)
 * Controller suites: ODL or ONOS or OpenContrail
 * Feature projects (promise, vIMS)
 * Rally (benchmark scenario)

At the end of an automated execution, everything is cleaned.
Before running Functest, we take a snapshot of the OpenStack configuration
(users, tenants, networks, ....) and after Functest we removed everything
created by Functest to restitute the system as it was prior to the tests.
