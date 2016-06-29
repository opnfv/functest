.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

Executing the functest suites
=============================

Manual testing
--------------

This section assumes the following:
 * The Functest Docker container is running
 * The docker prompt is shown
 * The Functest environment is ready (Functest CLI command 'functest env prepare'
   has been executed)

If any of the above steps are missing please refer to the Functest Config Guide
as they are a prerequisite and all the commands explained in this section **must** be
performed **inside the container**.

In Colorado release, the scripts **run_tests.sh** is now replaced with the new 
Functest CLI. 

**TODO** Figure out how the different options below are passed to the 
Functest CLI and then fix this document in patch #2 !!! Sorry for this approach 
Jose/Morgan. Time is running out

** End of TODO**

** WARNING - Next sections are not yet ready. will be fixed in patch #2 **
    usage:
        bash run_tests.sh [-h|--help] [-r|--report] [-n|--no-clean] [-t|--test <test_name>]

    where:
        -h|--help         show this help text
        -r|--report       push results to database (false by default)
        -n|--no-clean     do not clean up OpenStack resources after test run
        -s|--serial       run tests in one thread
        -t|--test         run specific set of tests
          <test_name>     one or more of the following separated by comma:
                             vping_ssh,vping_userdata,odl,onos,tempest,rally,vims,promise,doctor,bgpvpn

    examples:
        run_tests.sh
        run_tests.sh --test vping_ssh,odl
        run_tests.sh -t tempest,rally --no-clean

The *-r* option is used by the OPNFV Continuous Integration automation mechanisms
in order to push the test results into the NoSQL results collection database.
This database is read only for a regular user given that it needs special rights
and special conditions to push data.

The *-t* option can be used to specify the list of a desired test to be launched,
by default Functest will launch all the test suites in the following order:

  1) vPing test cases
  2) Tempest suite
  3) SDN controller suites
  4) Feature project tests cases (Promise, Doctor, SDNVPN)
  5) vIMS suite
  6) Rally suite

Please note that for some scenarios some test cases might not be launched.
Functest calculates automatically which test can be executed and which cannot given
the environment variable **DEPLOY_SCENARIO** to the docker container.

A single or set of test may be launched at once using *-t <test_name>* specifying
the test name or names separated by commas in the following list:
*[vping_ssh,vping_userdata,odl,onos,rally,tempest,vims,promise,doctor]*.

Functest includes cleaning mechanism in order to remove
all the OpenStack resources except what was present before running any test. The script
*$repos_dir/functest/utils/generate_defaults.py*
is called once by *prepare_env.sh* when setting up the Functest environment
to snapshot all the OpenStack resources (images, networks, volumes, security groups,
tenants, users) so that an eventual cleanup does not remove any of this defaults.

The *-n* option is used for preserving all the possible OpenStack resources created
by the tests after their execution.

The *-s* option forces execution of test cases in a single thread. Currently this
option affects Tempest test cases only and can be used e.g. for troubleshooting
concurrency problems.

The script **clean_openstack.py** which is located in
*$repos_dir/functest/testcases/VIM/OpenStack/CI/libraries/*
is normally called after a test execution if the *-n* is not specified. It
is in charge of cleaning the OpenStack resources that are not specified
in the defaults file generated previously which is stored in
*/home/opnfv/functest/conf/os_defaults.yaml* in the docker
container.

It is important to mention that if there are new OpenStack resources created
manually after preparing the Functest environment, they will be removed if this
flag is not specified in the *run_tests.sh* command.
The reason to include this cleanup meachanism in Functest is because some
test suites such as Tempest or Rally create a lot of resources (users,
tenants, networks, volumes etc.) that are not always properly cleaned, so this
function has been set to keep the system as clean as it was before a
full Functest execution.

Although **run_tests.sh** provides an easy way to run any test, it is possible to
do a direct call to the desired test script. For example:

    python $repos_dir/functest/testcases/vPing/vPing_ssh.py -d

Automated testing
-----------------

As mentioned previously, the **prepare-env.sh** and **run_test.sh** can be called within
the container from Jenkins. There are 2 jobs that automate all the manual steps
explained in the previous section. One job runs all the tests and the other one allows testing
test suite by test suite specifying the test name. The user might use one or
the other job to execute the desired test suites.

One of the most challenging task in the Brahmaputra release consists
in dealing with lots of scenarios and installers. Thus, when the tests are
automatically started from CI, a basic algorithm has been created in order to
detect whether a given test is runnable or not on the given scenario.
Some Functest test suites cannot be systematically run (e.g. ODL suite can not
be run on an ONOS scenario).

CI provides some useful information passed to the container as environment
variables:

 * Installer (apex|compass|fuel|joid), stored in INSTALLER_TYPE
 * Installer IP of the engine or VM running the actual deployment, stored in INSTALLER_IP
 * The scenario [controller]-[feature]-[mode], stored in DEPLOY_SCENARIO with

   * controller = (odl|onos|ocl|nosdn)
   * feature = (ovs(dpdk)|kvm|sfc|bgpvpn)
   * mode = (ha|noha)

The constraints per test case are defined in the Functest configuration file
*/home/opnfv/functest/config/config_functest.yaml*::

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

At the end of the Functest environment creation, a file
*/home/opnfv/functest/conf/testcase-list.txt* is created with the list of
all the runnable tests.
Functest considers the static constraints as regular expressions and compare them
with the given scenario name.
For instance, ODL suite can be run only on an scenario including 'odl' in its name.

The order of execution is also described in the Functest configuration file::

 test_exec_priority:

    1: vping_ssh
    2: vping_userdata
    3: tempest
    4: odl
    5: onos
    6: ovno
    7: doctor
    8: promise
    9: odl-vpnservice
    10: bgpvpn
    #11: openstack-neutron-bgpvpn-api-extension-tests
    12: vims
    13: rally

The tests are executed in the following order:

  1) vPing test cases
  2) Tempest suite
  3) SDN controller suites
  4) Feature project tests cases (Promise, Doctor, BGPVPN...)
  5) vIMS suite
  6) Rally suite

As explained before, at the end of an automated execution, the OpenStack resources
might be eventually removed.
