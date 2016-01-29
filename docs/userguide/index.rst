=========================
OPNFV FUNCTEST user guide
=========================

.. toctree::
   :numbered:
   :maxdepth: 2


Introduction
============

The goal of this documents is to describe the Functest test cases as well as
provide a procedure about how to execute (or launch) them.

A presentation has been created for the first OPNFV Summit `[4]`_.

It is assumed that Functest container has been properly installed `[1]`_.


Description of the test cases
=============================

Functest is an OPNFV project dedicated to functional testing.
In the continuous integration, it is launched after an OPNFV fresh installation.
The Functest target is to verify the basic functions of the infrastructure.

Functest includes different test suites which several test cases within.
Test cases are developed in Functest and in feature projects.

The current list of test suites can be distributed in 3 main domains:

+----------------+----------------+--------------------------------------------+
| Method         | Test suite     | Comments                                   |
+================+================+============================================+
|                | vPing          | NFV "Hello World"                          |
|                +----------------+--------------------------------------------+
|    VIM         | vPing_userdata | Ping using userdata and cloud-init         |
|                |                | mechanism                                  |
|                +----------------+--------------------------------------------+
|(Virtualised    | Tempest        | OpenStack reference test suite `[2]`_      |
| Infrastructure +----------------+--------------------------------------------+
| Manager)       | Rally scenario | OpenStack testing tool testing OpenStack   |
|                |                | modules `[3]`_                             |
+----------------+----------------+--------------------------------------------+
|                | OpenDaylight   | Opendaylight Test suite                    |
|                +----------------+--------------------------------------------+
| Controllers    | ONOS           | Test suite of ONOS L2 and L3 functions     |
|                +----------------+--------------------------------------------+
|                | OpenContrail   |                                            |
+----------------+----------------+--------------------------------------------+
| Features       | vIMS           | Show the capability to deploy a real NFV   |
|                |                | test cases.                                |
|                |                | The IP Multimedia Subsytem is a typical    |
|                |                | Telco test case, referenced by ETSI.       |
|                |                | It provides a fully functional VoIP System.|
|                +----------------+--------------------------------------------+
|                | Promise        | Resource reservation and management project|
|                |                | to identify NFV related requirements and   |
|                |                | realize resource reservation for future    |
|                |                | usage by capacity management of resource   |
|                |                | pools regarding compute, network and       |
|                |                | storage.                                   |
|                +----------------+--------------------------------------------+
|                | SDNVPN         |                                            |
+----------------+----------------+--------------------------------------------+


Most of the test suites are developed upstream.
For example, Tempest `[2]`_ is the OpenStack integration test suite.
Functest is in charge of the integration of different functional test suites.

The Tempest suite has been customized but no new test cases have been created.
Some OPNFV feature projects (.e.g. SDNVPN) have created Tempest tests cases and
pushed to upstream.

The tests run from CI are pushed into a database.
The goal is to populate the database with results and to show them on a Test
Dashboard.

There is no real notion of Test domain or Test coverage yet.
Basic components (VIM, controllers) are tested through their own suites.
Feature projects also provide their own test suites.

vIMS test case was integrated to demonstrate the capability to deploy a
relatively complex NFV scenario on top of the OPNFV infrastructure.

Functest considers OPNFV as a black box.
OPNFV, since Brahmaputra, offers lots of possible combinations:

  * 3 controllers (OpenDayligh, ONOS, OpenContrail)
  * 4 installers (Apex, Compass, Fuel, Joid)

However most of the tests shall be runnable on any configuration.

The different scenarios are described in the section hereafter.

VIM
---

vPing
^^^^^

The goal of this test can be described as follows::

 vPing test case
 +-------------+                   +-------------+
 |             |                   |             |
 |             |     Boot VM1      |             |
 |             +------------------>|             |
 |             |                   |             |
 |             |     Get IP VM1    |             |
 |             +------------------>|             |
 |   Tester    |                   |   System    |
 |             |     Boot VM2      |    Under    |
 |             +------------------>|     Test    |
 |             |                   |             |
 |             |   Create (VM2)    |             |
 |             |   floating IP     |             |
 |             +------------------>|             |
 |             |                   |             |
 |             | SCP vPing script  |             |
 |             |      to VM2       |             |
 |             +------------------>|             |
 |             |                   |             |
 |             |   SSH to VM2      |             |
 |             +------------------>|             |
 |             |                   |             |
 |             |    Ping VM1       |             |
 |             |    private IP     |             |
 |             +------------------>|             |
 |             |                   |             |
 |             |    If ping:       |             |
 |             |      exit OK      |             |
 |             |    else (timeout) |             |
 |             |      exit KO      |             |
 |             |                   |             |
 +-------------+                   +-------------+


vPing_userdata
^^^^^^^^^^^^^^

The goal of this test can be described as follow::

 vPing_userdata test case
 +-------------+                   +-------------+
 |             |                   |             |
 |             |     Boot VM1      |             |
 |             +------------------>|             |
 |             |                   |             |
 |             |     Get IP VM1    |             |
 |             +------------------>|             |
 |   Tester    |                   |   System    |
 |             |     Boot VM2      |    Under    |
 |             +------------------>|     Test    |
 |             | VM2 pings VM1     |             |
 |             |   (cloud-init)    |             |
 |             | Check console log |             |
 |             |    If ping:       |             |
 |             |      exit OK      |             |
 |             |    else (timeout) |             |
 |             |      exit KO      |             |
 |             |                   |             |
 +-------------+                   +-------------+


This example can be considered as an "Hello World" example.
It is the first basic example, it must work on any configuration.

Tempest
^^^^^^^

Tempest `[2]`_ is the reference OpenStack Integration test suite.
It is a set of integration tests to be run against a live OpenStack cluster.
Tempest has batteries of tests for:

  * OpenStack API validation
  * Scenarios
  * other specific tests useful in validating an OpenStack deployment

We use Rally `[3]`_ to run Tempest suite.
Rally generates automatically tempest.conf configuration file.
Before running actual test cases Functest creates needed resources.
Needed parameters are updated in the configuration file.
When the Tempest suite is run, each test duration is measured.
The full console output is stored in the tempest.log file.

As an addition of Arno, Brahmaputra runs a customized set of Tempest test cases.
The list is specificed through --tests-file when running Rally.
This option has been introduced in Rally in version 0.1.2.

The customized test list is available in the Functest repo `[4]`_
This list contains more than 200 Tempest test cases.
The list can be divied into two main parts:

  1) Set of tempest smoke test cases
  2) Set of test cases from DefCore list `[8]`_

The goal of Tempest test suite is to check the basic functionalities of
different OpenStack components on an OPNFV fresh installation using
corresponding REST API interfaces.


Rally bench test suites
^^^^^^^^^^^^^^^^^^^^^^^

Rally `[3]`_ is a benchmarking tool that answers the question::

 “How does OpenStack work at scale?”.

The goal of this test suite is to test the different modules of OpenStack and
get significant figures that could help us to define telco Cloud KPI.

The OPNFV scenarios are based on the collection of the existing Rally scenarios:

 * authenticate
 * cinder
 * glance
 * heat
 * keystone
 * neutron
 * nova
 * quotas
 * requests
 * vm

Basic SLA (stop test on errors) have been implemented.


SDN Controllers
---------------

Brahmaputra introduces new SDN controllers.
There are currently 3 possible controllers:

 * OpenDaylight (ODL)
 * ONOS
 * OpenContrail (OCL)

OpenDaylight
^^^^^^^^^^^^

The OpenDaylight (ODL) test suite consists of a set of basic tests inherited
from ODL project.
The suite verifies creation and deletion of networks, subnets and ports with
OpenDaylight and Neutron.

The list of tests can be described as follow:

 * Restconf.basic: Get the controller modules via Restconf
 * Neutron.Networks

   * Check OpenStack Networks :: Checking OpenStack Neutron for known networks
   * Check OpenDaylight Networks :: Checking OpenDaylight Neutron API
   * Create Network :: Create new network in OpenStack
   * Check Network :: Check Network created in OpenDaylight
   * Neutron.Networks :: Checking Network created in OpenStack are pushed

 * Neutron.Subnets

   * Check OpenStack Subnets :: Checking OpenStack Neutron for known Subnets
   * Check OpenDaylight subnets :: Checking OpenDaylight Neutron API
   * Create New subnet :: Create new subnet in OpenStack
   * Check New subnet :: Check new subnet created in OpenDaylight
   * Neutron.Subnets :: Checking Subnets created in OpenStack are pushed

 * Neutron.Ports

   * Check OpenStack ports :: Checking OpenStack Neutron for known ports
   * Check OpenDaylight ports :: Checking OpenDaylight Neutron API
   * Create New Port :: Create new port in OpenStack
   * Check New Port :: Check new subnet created in OpenDaylight
   * Neutron.Ports :: Checking Port created in OpenStack are pushed

 * Delete Ports

   * Delete previously created subnet in OpenStack
   * Check subnet deleted in OpenDaylight
   * Check subnet deleted in OpenStack

 * Delete network

   * Delete previously created network in OpenStack
   * Check network deleted in OpenDaylight
   * Check network deleted in OpenStack


ONOS
^^^^

TestON Framework is used to test ONOS function.
The test cases deal with L2 and L3 functions.
ONOS is configured through OPNFV scenario.
The ONOS test suite can be run on any ONOS compliant scenario.

The test cases may be described as follow:

 * onosfunctest: The mainly executable file contains the initialization of
   the docker environment and functions called by FUNCvirNetNB and
   FUNCvirNetNBL3

 * FUNCvirNetNB

   * Create Network: Post Network data and check it in ONOS
   * Update Network: Update the Network and compare it in ONOS
   * Delete Network: Delete the Network and check if it's NULL in ONOS or
     not
   * Create Subnet: Post Subnet data and check it in ONOS
   * Update Subnet: Update the Subnet and compare it in ONOS
   * Delete Subnet: Delete the Subnet and check if it's NULL in ONOS or not
   * Create Port: Post Port data and check it in ONOS
   * Update Port: Update the Port and compare it in ONOS
   * Delete Port: Delete the Port and check if it's NULL in ONOS or not

 * FUNCvirNetNBL3

   * Create Router: Post dataes for create Router and check it in ONOS
   * Update Router: Update the Router and compare it in ONOS
   * Delete Router: Delete the Router dataes and check it in ONOS
   * Create RouterInterface: Post RouterInterface data to an exist Router
     and check it in ONOS
   * Delete RouterInterface: Delete the RouterInterface and check the Router
   * Create FloatingIp: Post dataes for create FloatingIp and check it in
     ONOS
   * Update FloatingIp: Update the FloatingIp and compare it in ONOS
   * Delete FloatingIp: Delete the FloatingIp and check if it's NULL in
     ONOS  or not
   * Create External Gateway: Post dataes for create External Gateway to an
     exit Router and check it
   * Update External Gateway: Update the External Gateway and compare it
   * Delete External Gateway: Delete the External Gateway and check if it's
     NULL in ONOS or not


OpenContrail
^^^^^^^^^^^^
TODO OVNO



Features
--------

vIMS
^^^^
The goal of this test suite consists of:

 * deploying a VNF orchestrator (cloudify)
 * deploy a Clearwater vIMS (IP Multimedia Subsystem) VNF from this
   orchestrator based on a TOSCA blueprint defined in `[5]`_
 * run suite of signaling tests on top of this VNF

The Clearwater architecture is described as follows:

.. figure:: ../images/clearwater-architecture.png
   :align: center
   :alt: vIMS architecture

Two types of information are stored in the Test Database:

 * the duration of each step (orchestion deployment, VNF deployment and test)
 * the test results

The deployment of a complete functional VNF allows the test of most of the
essential functions needed for a NFV system.

Promise
^^^^^^^

TODO promise


Manual testing
==============

Once the Functest docker container is running and Functest environment ready
(through /home/opnfv/repos/functest/docker/prepare_env.sh script), the system is
ready to run the tests.

The script run_tests.sh is located in $repos_dir/functest/docker and it has
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

The -r option is used by the Continuous Integration in order to push the test
results into a test collection database, see in next section for details.
In manual mode, you must not use it, your try will be anyway probably rejected
as your POD must be declared in the database to collect the data.

The -n option is used for preserving all the existing OpenStack resources after
execution test cases.

The -t option can be used to specify the list of test you want to launch, by
default Functest will try to launch all its test suites in the following order
vPing, odl, Tempest, vIMS, Rally.
You may launch only one single test by using -t <the test you want to launch>

Within Tempest test suite you can define which test cases you want to execute in
your environment by editing test_list.txt file before executing run_tests.sh
script.

Please note that Functest includes cleaning mechanism in order to remove
everything except what was present after a fresh install.
If you create your own VMs, tenants, networks etc. and then launch Functest,
they all will be deleted after executing the tests. Use --no-clean option with
run_test.sh in order to preserve all the existing resources.
However, be aware that Tempest and Rally create of lot of resources (users,
tenants, networks, volumes etc.) that are not always properly cleaned, so this
cleaning function has been set to keep the system as clean as possible after a
full Functest run.

You may also add you own test by adding a section into the function run_test()


Automated testing
=================

As mentioned in `[1]`, the prepare-env.sh and run_test.sh can be executed within
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
    #7: doctor
    8: promise
    9: odl-vpnservice
    10: bgpvpn
    #11: openstack-neutron-bgpvpn-api-extension-tests
    12: vims
    13: rally

The tests are executed as follow:

 * Basic scenario (vPing, vPing_userdata, Tempest)
 * Controller suites: ODL or ONOS or OpenContrail
 * Feature projects
 * vIMS
 * Rally (benchmark scenario)

At the end of an automated execution, everything is cleaned.
We keep only the users/networks that have been statically declared in '[9]'_


Test results
============

VIM
---

vPing
^^^^^

vPing results are displayed in the console::

  FUNCTEST.info: Running vPing test...
  2016-01-23 03:18:20,153 - vPing- INFO - Creating neutron network vping-net...
  2016-01-23 03:18:35,476 - vPing- INFO - Flavor found 'm1.small'
  2016-01-23 03:18:36,350 - vPing- INFO - vPing Start Time:'2016-01-23 03:18:36'
  2016-01-23 03:18:38,571 - vPing- INFO - Creating instance 'opnfv-vping-1' with IP 192.168.130.30...
  2016-01-23 03:18:53,716 - vPing- INFO - Instance 'opnfv-vping-1' is ACTIVE.
  2016-01-23 03:18:55,239 - vPing- INFO - Creating instance 'opnfv-vping-2' with IP 192.168.130.40...
  2016-01-23 03:19:15,593 - vPing- INFO - Instance 'opnfv-vping-2' is ACTIVE.
  2016-01-23 03:19:15,593 - vPing- INFO - Creating floating IP for the second VM...
  2016-01-23 03:19:18,017 - vPing- INFO - Floating IP created: '10.2.65.6'
  2016-01-23 03:19:18,017 - vPing- INFO - Associating floating ip: '10.2.65.6' to VM2
  2016-01-23 03:19:37,839 - vPing- INFO - SCP ping script to VM2...
  2016-01-23 03:19:37,839 - vPing- INFO - Waiting for ping...
  2016-01-23 03:19:40,130 - vPing- INFO - vPing detected!
  2016-01-23 03:19:40,130 - vPing- INFO - vPing duration:'63.8'
  2016-01-23 03:19:40,130 - vPing- INFO - Cleaning up...
  2016-01-23 03:20:06,574 - vPing- INFO - Deleting network 'vping-net'...
  2016-01-23 03:20:13,587 - vPing- INFO - vPing OK




vPing_userdata
^^^^^^^^^^^^^^

vPing_userdata results are displayed in the console::

    2016-01-06 16:06:20,550 - vPing- INFO - Creating neutron network vping-net...
    2016-01-06 16:06:23,867 - vPing- INFO - Flavor found 'm1.small'
    2016-01-06 16:06:24,457 - vPing- INFO - vPing Start Time:'2016-01-06 16:06:24'
    2016-01-06 16:06:24,626 - vPing- INFO - Creating instance 'opnfv-vping-1' with IP 192.168.130.30...
    2016-01-06 16:06:39,351 - vPing- INFO - Instance 'opnfv-vping-1' is ACTIVE.
    2016-01-06 16:06:39,650 - vPing- INFO - Creating instance 'opnfv-vping-2' with IP 192.168.130.40...
    2016-01-06 16:06:53,330 - vPing- INFO - Instance 'opnfv-vping-2' is ACTIVE.
    2016-01-06 16:06:53,330 - vPing- INFO - Waiting for ping...
    2016-01-06 16:06:58,669 - vPing- INFO - vPing detected!
    2016-01-06 16:06:58,669 - vPing- INFO - vPing duration:'34.2'
    2016-01-06 16:06:58,670 - vPing- INFO - Cleaning up...
    2016-01-06 16:07:12,661 - vPing- INFO - Deleting network 'vping-net'...
    2016-01-06 16:07:14,748 - vPing- INFO - vPing OK

A json file is produced and pushed into the test result database.


Tempest
^^^^^^^

The Tempest results are displayed in the console::

  FUNCTEST.info: Running Tempest tests...
  2016-01-28 07:56:55,380 - run_tempest - INFO - Creating tenant and user for Tempest suite
  2016-01-28 07:56:56.127 23795 INFO rally.verification.tempest.tempest [-] Starting: Creating configuration file for Tempest.
  2016-01-28 07:56:59.512 23795 INFO rally.verification.tempest.tempest [-] Completed: Creating configuration file for Tempest.
  16-01-28 07:57:00,597 - run_tempest - INFO - Starting Tempest test suite: '--tests-file /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/custom_tests/test_list.txt'.
  Total results of verification:

  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | UUID                                 | Deployment UUID                      | Set name | Tests | Failures | Created at                 | Status   |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+
  | e0bf7770-2c0f-4c63-913c-cd51a6edd96d | 16582e1e-7b01-4d5d-9c13-a26db8567b7b |          | 144   | 30       | 2016-01-28 07:57:01.044856 | finished |
  +--------------------------------------+--------------------------------------+----------+-------+----------+----------------------------+----------+

  Tests:

  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | name                                                                                                                                     | time      | status  |
  +------------------------------------------------------------------------------------------------------------------------------------------+-----------+---------+
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor                                                               | 0.29804   | success |
  | tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors                                                             | 0.06289   | success |
  | tempest.api.compute.images.test_images.ImagesTestJSON.test_delete_saving_image                                                           | 9.21756   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_delete_image                                        | 8.65376   | success |
  | tempest.api.compute.images.test_images_oneserver.ImagesOneServerTestJSON.test_create_image_specify_multibyte_character_image_name        | 9.10993   | success |
  | tempest.api.compute.images.test_list_image_filters.ListImageFiltersTestJSON.test_list_images_filter_by_changes_since                     | 0.19585   | success |
  ...........................................
  2016-01-28 08:19:32,132 - run_tempest - INFO - Results: {'timestart': '2016-01-2807:57:01.044856', 'duration': 1350, 'tests': 144, 'failures': 30}
  2016-01-28 08:19:32,133 - run_tempest - INFO - Pushing results to DB: 'http://testresults.opnfv.org/testapi/results'.
  2016-01-28 08:19:32,278 - run_tempest - INFO - Deleting tenant and user for Tempest suite)

In order to check all the available test case related debug information, please
inspect tempest.log file stored into related Rally deployment folder.

The Tempest results are pushed to the Test Database.

Rally
^^^^^

The Rally results are displayed in the console, each module is run one after the
other. Tables are displayed::

  +-------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action               | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | keystone.create_role | 0.358 | 0.572  | 0.772  | 0.811  | 1.106 | 0.603 | 100.0%  | 20    |
  | keystone.add_role    | 0.32  | 0.436  | 0.846  | 0.903  | 1.018 | 0.51  | 100.0%  | 20    |
  | keystone.list_roles  | 0.102 | 0.185  | 0.253  | 0.275  | 0.347 | 0.188 | 100.0%  | 20    |
  | total                | 0.845 | 1.223  | 1.821  | 1.822  | 1.823 | 1.302 | 100.0%  | 20    |
  +----------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 7.13633608818
  Full duration: 36.7863121033
  ..............
  +------------------------------------------------------------------------------------------+
  |                                   Response Times (sec)                                   |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | action              | min   | median | 90%ile | 95%ile | max   | avg   | success | count |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  | nova.create_keypair | 1.005 | 1.784  | 3.025  | 3.636  | 4.373 | 2.004 | 100.0%  | 20    |
  | nova.delete_keypair | 0.199 | 0.699  | 1.007  | 1.244  | 3.014 | 0.79  | 100.0%  | 20    |
  | total               | 1.249 | 2.625  | 4.259  | 4.845  | 5.131 | 2.794 | 100.0%  | 20    |
  +---------------------+-------+--------+--------+--------+-------+-------+---------+-------+
  Load duration: 14.9231169224
  Full duration: 71.4614388943


At the end of the module test, a message is displayed to provide a global
summary (Test OK or test failed). The raw results are pushed into the Test
Database.


Controllers
-----------

OpenDaylight
^^^^^^^^^^^^

The results of ODL tests can be seen in the console::

 ==============================================================================
 Basic
 ==============================================================================
 Basic.010 Restconf OK :: Test suite to verify Restconf is OK
 ==============================================================================
 Get Controller Modules :: Get the controller modules via Restconf     | PASS |
 ------------------------------------------------------------------------------
 Basic.010 Restconf OK :: Test suite to verify Restconf is OK          | PASS |
 1 critical test, 1 passed, 0 failed
 1 test total, 1 passed, 0 failed
 ==============================================================================
 Basic                                                                 | PASS |
 1 critical test, 1 passed, 0 failed
 1 test total, 1 passed, 0 failed
 ==============================================================================
 Output:  /home/jenkins-ci/workspace/functest-opnfv-jump-2/output.xml
 Log:     /home/jenkins-ci/workspace/functest-opnfv-jump-2/log.html
 Report:  /home/jenkins-ci/workspace/functest-opnfv-jump-2/report.html

 ..............................................................................

 Neutron.Delete Networks :: Checking Network deleted in OpenStack a... | PASS |
 2 critical tests, 2 passed, 0 failed
 2 tests total, 2 passed, 0 failed
 ==============================================================================
 Neutron :: Test suite for Neutron Plugin                              | PASS |
 18 critical tests, 18 passed, 0 failed
 18 tests total, 18 passed, 0 failed
 ==============================================================================
 Output:  /home/jenkins-ci/workspace/functest-opnfv-jump-2/output.xml
 Log:     /home/jenkins-ci/workspace/functest-opnfv-jump-2/log.html
 Report:  /home/jenkins-ci/workspace/functest-opnfv-jump-2/report.html

3 result files are generated:
 * output.xml
 * log.html
 * report.html

 ODL result page

.. figure:: ../images/functestODL.png
   :width: 170mm
   :align: center
   :alt: ODL suite result page


ONOS
^^^^

The ONOS test logs can be found in OnosSystemTest/TestON/logs
(ONOSCI_PATH to be added),and also can be seen in the console::

 ******************************
 Result summary for Testcase4
 ******************************

 2016-01-14 05:25:40,529 - FUNCvirNetNBL3 - INFO - ONOS Router Delete test Start

 [2016-01-14 05:25:40.529644] [FUNCvirNetNBL3] [CASE]  Virtual Network NBI Test - Router
 2016-01-14 05:25:40,530 - FUNCvirNetNBL3 - INFO - Generate Post Data

 [2016-01-14 05:25:40.530825] [FUNCvirNetNBL3] [STEP]  4.1: Post Network Data via HTTP(Post Router need post network)
 2016-01-14 05:25:40,531 - FUNCvirNetNBL3 - INFO - Sending request http://192.168.122.56:8181/onos/vtn/networks/ using POST method.
 2016-01-14 05:25:40,539 - FUNCvirNetNBL3 - INFO - Verifying the Expected is equal to the actual or not using assert_equal
 2016-01-14 05:25:40,539 - FUNCvirNetNBL3 - INFO - Post Network Success
 2016-01-14 05:25:40,539 - FUNCvirNetNBL3 - INFO - Assertion Passed

 [2016-01-14 05:25:40.539687] [FUNCvirNetNBL3] [STEP]  4.2: Post Router Data via HTTP
 2016-01-14 05:25:40,540 - FUNCvirNetNBL3 - INFO - Sending request http://192.168.122.56:8181/onos/vtn/routers/ using POST method.
 2016-01-14 05:25:40,543 - FUNCvirNetNBL3 - INFO - Verifying the Expected is equal to the actual or not using assert_equal
 2016-01-14 05:25:40,543 - FUNCvirNetNBL3 - INFO - Post Router Success
 2016-01-14 05:25:40,543 - FUNCvirNetNBL3 - INFO - Assertion Passed

 [2016-01-14 05:25:40.543489] [FUNCvirNetNBL3] [STEP]  4.3: Delete Router Data via HTTP
 2016-01-14 05:25:40,543 - FUNCvirNetNBL3 - INFO - Sending request http://192.168.122.56:8181/onos/vtn/routers/e44bd655-e22c-4aeb-b1e9-ea1606875178 using DELETE method.
 2016-01-14 05:25:40,546 - FUNCvirNetNBL3 - INFO - Verifying the Expected is equal to the actual or not using assert_equal
 2016-01-14 05:25:40,546 - FUNCvirNetNBL3 - INFO - Delete Router Success
 2016-01-14 05:25:40,546 - FUNCvirNetNBL3 - INFO - Assertion Passed

 [2016-01-14 05:25:40.546774] [FUNCvirNetNBL3] [STEP]  4.4: Get Router Data is NULL
 2016-01-14 05:25:40,547 - FUNCvirNetNBL3 - INFO - Sending request http://192.168.122.56:8181/onos/vtn/routers/e44bd655-e22c-4aeb-b1e9-ea1606875178 using GET method.
 2016-01-14 05:25:40,550 - FUNCvirNetNBL3 - INFO - Verifying the Expected is equal to the actual or not using assert_equal
 2016-01-14 05:25:40,550 - FUNCvirNetNBL3 - INFO - Get Router Success
 2016-01-14 05:25:40,550 - FUNCvirNetNBL3 - INFO - Assertion Passed


 *****************************
  Result: Pass
 *****************************

 .......................................................................................

 ******************************
  Result summary for Testcase9
 ******************************
 .......................................................................................


 [2016-01-14 05:26:42.543489] [FUNCvirNetNBL3] [STEP]  9.6: FloatingIp Clean Data via HTTP
 2016-01-14 05:26:42,543 - FUNCvirNetNBL3 - INFO - Sending request http://192.168.122.56:8181/onos/vtn/floatingips/e44bd655-e22c-4aeb-b1e9-ea1606875178 using DELETE method.
 2016-01-14 05:26:42,546 - FUNCvirNetNBL3 - INFO - Verifying the Expected is equal to the actual or not using assert_equal
 2016-01-14 05:26:42,546 - FUNCvirNetNBL3 - ERROR - Delete Floatingip failed

 .......................................................................................

 *****************************
  Result: Failed
 *****************************

There is a result summary for each testcase, and a global summary for the whole test.
If any problem occurs during the test, a ERROR message will be provided in the test and the the global summary::

 *************************************
         Test Execution Summary
 *************************************

  Test Start           : 14 Jan 2016 05:25:37
  Test End             : 14 Jan 2016 05:25:41
  Execution Time       : 0:00:03.349087
  Total tests planned  : 11
  Total tests RUN      : 11
  Total Pass           : 8
  Total Fail           : 3
  Total No Result      : 0
  Success Percentage   : 72%
  Execution Result     : 100%


OpenContrail
^^^^^^^^^^^^

TODO OVNO


Feature
-------

vIMS
^^^^

The results in the console are very verbose::

    FUNCTEST.info: Running vIMS test...
    2016-01-07 12:30:24,107 - vIMS - INFO - Prepare OpenStack plateform (create tenant and user)
    2016-01-07 12:30:24,484 - vIMS - INFO - Update OpenStack creds informations
    2016-01-07 12:30:24,484 - vIMS - INFO - Upload some OS images if it doesn't exist
    2016-01-07 12:30:24,917 - vIMS - INFO - centos_7 image doesn't exist on glance repository.
                                Try downloading this image and upload on glance !
    2016-01-07 12:31:01,268 - vIMS - INFO - ubuntu_14.04 image doesn't exist on glance repository.
                                Try downloading this image and upload on glance !
    2016-01-07 12:31:28,670 - vIMS - INFO - Update security group quota for this tenant
    2016-01-07 12:31:28,903 - vIMS - INFO - Update cinder quota for this tenant
    2016-01-07 12:31:29,355 - vIMS - INFO - Collect flavor id for cloudify manager server
    2016-01-07 12:31:30,453 - vIMS - INFO - Prepare virtualenv for cloudify-cli
    2016-01-07 12:31:30,453 - vIMS - DEBUG - Executing command : chmod +x /home/opnfv/repos/functest/testcases/vIMS/CI/create_venv.sh
    2016-01-07 12:31:30,460 - vIMS - DEBUG - Executing command : /home/opnfv/repos/functest/testcases/vIMS/CI/create_venv.sh /home/opnfv/functest/data/vIMS/
    2016-01-07 12:31:30,469 - vIMS - INFO - Downloading the cloudify manager server blueprint
    2016-01-07 12:31:46,028 - vIMS - INFO - Cloudify deployment Start Time:'2016-01-07 12:31:46'
    2016-01-07 12:31:46,029 - vIMS - INFO - Writing the inputs file
    2016-01-07 12:31:46,032 - vIMS - INFO - Launching the cloudify-manager deployment
    .........................................
    2016-01-07 12:36:51 LOG <manager> [rabbitmq_3c04e.create] INFO: preparing fabric environment...
    2016-01-07 12:36:51 LOG <manager> [rabbitmq_3c04e.create] INFO: environment prepared successfully
    .........................................
    2016-01-07 12:42:51,982 - vIMS - INFO - Cloudify-manager server is UP !
    2016-01-07 12:42:51,983 - vIMS - INFO - Cloudify deployment duration:'666.0'
    2016-01-07 12:42:51,983 - vIMS - INFO - Collect flavor id for all clearwater vm
    2016-01-07 12:42:53,330 - vIMS - INFO - vIMS VNF deployment Start Time:'2016-01-07 12:42:53'
    2016-01-07 12:42:53,330 - vIMS - INFO - Downloading the openstack-blueprint.yaml blueprint
    2016-01-07 12:43:05,798 - vIMS - INFO - Writing the inputs file
    2016-01-07 12:43:05,801 - vIMS - INFO - Launching the clearwater deployment
    2016-01-07 12:43:05,801 - vIMS - DEBUG - Executing command : /bin/bash -c 'source /home/opnfv/functest/data/vIMS/venv_cloudify/bin/activate; cd /home/opnfv/functest/data/vIMS/opnfv-cloudify-clearwater; cfy blueprints upload -b clearwater -p openstack-blueprint.yaml; cfy deployments create -b clearwater -d clearwater-opnfv --inputs inputs.yaml; cfy executions start -w install -d clearwater-opnfv --timeout 1800; '
    2016-01-07 13:01:50,577 - vIMS - DEBUG - Validating openstack-blueprint.yaml
    Blueprint validated successfully
    Uploading blueprint openstack-blueprint.yaml to management server 172.30.10.165
    Uploaded blueprint, blueprint's id is: clearwater
    Creating new deployment from blueprint clearwater at management server 172.30.10.165
    Deployment created, deployment's id is: clearwater-opnfv
    .........................................
    2016-01-07 13:01:50,578 - vIMS - INFO - The deployment of clearwater-opnfv is ended
    2016-01-07 13:01:50,578 - vIMS - INFO - vIMS VNF deployment duration:'1137.2'
    2016-01-07 13:04:50,591 - vIMS - DEBUG - Trying to get clearwater nameserver IP ...
    2016-01-07 13:04:55,176 - vIMS - INFO - vIMS functional test Start Time:'2016-01-07 13:04:55'
    2016-01-07 13:14:20,694 - vIMS - INFO - vIMS functional test duration:'565.5'
    .........................................
    Basic Call - Rejected by remote endpoint (TCP) - (6505550603, 6505550969) Passed
    Basic Call - Rejected by remote endpoint (UDP) - (6505550095, 6505550084) Passed
    Basic Call - Messages - Pager model (TCP) - (6505550000, 6505550520) Passed
    Basic Call - Messages - Pager model (UDP) - (6505550742, 6505550077) Passed
    Basic Call - Pracks (TCP) - (6505550670, 6505550304) Passed
    Basic Call - Pracks (UDP) - (6505550990, 6505550391) Passed
    Basic Registration (TCP) - (6505550744) Passed
    Basic Registration (UDP) - (6505550616) Passed
    Multiple Identities (TCP) - (6505550957, 6505550949) Passed
    Multiple Identities (UDP) - (6505550771, 6505550675) Passed
    .........................................
    2016-01-07 13:14:20,695 - vIMS - DEBUG - Trying to load test results
    2016-01-07 13:14:20,702 - vIMS - DEBUG - Push result into DB
    2016-01-07 13:14:20,702 - vIMS - DEBUG - Pushing results to DB....
    2016-01-07 13:14:21,396 - vIMS - DEBUG - <Response [200]>
    2016-01-07 13:14:21,396 - vIMS - INFO - Launching the clearwater-opnfv undeployment

Please note that vIMS traces are very verbose but can bee summarized in several
steps:

 * INFO: environment prepared successfully => environment OK
 * INFO - Cloudify-manager server is UP ! => orchestrator deployed
 * INFO The deployment of clearwater-opnfv is ended => VNF deployed
 * Multiple Identities (UDP) - (6505550771, 6505550675) Passed => tests run
 * DEBUG - Pushing results to DB.... => tests saved


Promise
^^^^^^^

TODO Promise


Functest in test Dashboard
==========================

The OPNFV testing group created a test collection database to collect the test
results from CI.
Any test project running on any lab integrated in CI can push the results to
this database.
This databse can be used afterwards to see the evolution of the tests and
compare the results versus the installers, the scenario or the labs.

You can find more information about the dashboard from Testing Dashboard wiki
page `[6]`_.


Overall Architecture
--------------------

The Test result management in Brahmaputra can be summarized as follow::

  +-------------+    +-------------+    +-------------+
  |             |    |             |    |             |
  |   Test      |    |   Test      |    |   Test      |
  | Project #1  |    | Project #2  |    | Project #N  |
  |             |    |             |    |             |
  +-------------+    +-------------+    +-------------+
           |               |               |
           ▼               ▼               ▼
       +-----------------------------------------+
       |                                         |
       |         Test Rest API front end         |
       |  http://testresults.opnfv.org/testapi   |
       |                                         |
       +-----------------------------------------+
           ▲                |
           |                ▼
           |     +-------------------------+
           |     |                         |
           |     |    Test Results DB      |
           |     |         Mongo DB        |
           |     |                         |
           |     +-------------------------+
           |
           |
     +----------------------+
     |                      |
     |    test Dashboard    |
     |                      |
     +----------------------+

The Test dashboard URL is: TODO LF
A proto Test dashboard has been realized: http://testresults.opnfv.org/proto/

Test API description
--------------------

The Test API is used to declare pods, projects, test cases and test results. An
additional method dashboard has been added to post-process the raw results. The
data model is very basic, 4 objects are created:

  * Pods
  * Test projects
  * Test cases
  * Test results

Pods::

  {
    "id": <ID>,
    "details": <URL description of the POD>,
    "creation_date": YYYY-MM-DD HH:MM:SS ,
    "name": <The POD Name>,
    "mode": <metal or virtual>
  },

Test project::

  {
    "id": <ID>,
    "name": <Name of the Project>,
    "creation_date": "YYYY-MM-DD HH:MM:SS",
    "description": <Short description>
  },

Test case::

  {
    "id": <ID>,
    "name":<Name of the test case>,
    "creation_date": "YYYY-MM-DD HH:MM:SS",
    "description": <short description>,
    "url":<URL for longer description>
  },

Test results::

  {
    "_id": <ID,
    "project_name": <Reference to project>,
    "pod_name": <Reference to POD where the test was executed>,
    "version": <Scenario on which the test was executed>,
    "installer": <Installer Apex or Compass or Fuel or Joid>,
    "description": <Short description>,
    "creation_date": "YYYY-MM-DD HH:MM:SS",
    "case_name": <Reference to the test case>
    "details":{
       <- the results to be put here ->
    }


For Brahmaputra, we got:

 * 16 pods
 * 18 projects
 * 101 test cases

The projects and the test cases have been frozen in December.
But all were not ready for Brahmaputra.



The API can described as follow:

**Version:**::

 +--------+--------------------------+------------------------------------------+
 | Method | Path                     | Description                              |
 +========+==========================+==========================================+
 | GET    | /version                 | Get API version                          |
 +--------+--------------------------+------------------------------------------+


**Pods:**::

 +--------+--------------------------+------------------------------------------+
 | Method | Path                     | Description                              |
 +========+==========================+==========================================+
 | GET    | /pods                    | Get the list of declared Labs (PODs)     |
 +--------+--------------------------+------------------------------------------+
 | POST   | /pods                    | Declare a new POD                        |
 |        |                          | Content-Type: application/json           |
 |        |                          | {                                        |
 |        |                          |    "name": "pod_foo",                    |
 |        |                          |    "creation_date": "YYYY-MM-DD HH:MM:SS"|
 |        |                          | }                                        |
 +--------+--------------------------+------------------------------------------+

**Projects:**::

 +--------+--------------------------+------------------------------------------+
 | Method | Path                     | Description                              |
 +========+==========================+==========================================+
 | GET    | /test_projects           | Get the list of test projects            |
 +--------+--------------------------+------------------------------------------+
 | GET    |/test_projects/{project}  | Get details on {project}                 |
 |        |                          |                                          |
 +--------+--------------------------+------------------------------------------+
 | POST   | /test_projects           | Add a new test project                   |
 |        |                          | Content-Type: application/json           |
 |        |                          | {                                        |
 |        |                          |    "name": "project_foo",                |
 |        |                          |    "description": "whatever you want"    |
 |        |                          | }                                        |
 +--------+--------------------------+------------------------------------------+
 | PUT    | /test_projects/{project} | Update a test project                    |
 |        |                          |                                          |
 |        |                          | Content-Type: application/json           |
 |        |                          | {                                        |
 |        |                          |    <the field(s) you want to modify>     |
 |        |                          | }                                        |
 +--------+--------------------------+------------------------------------------+
 | DELETE | /test_projects/{project} | Delete a test project                    |
 +--------+--------------------------+------------------------------------------+


**Test cases:**::

 +--------+--------------------------+------------------------------------------+
 | Method | Path                     | Description                              |
 +========+==========================+==========================================+
 | GET    | /test_projects/{project}/| Get the list of test cases of {project}  |
 |        | cases                    |                                          |
 +--------+--------------------------+------------------------------------------+
 | POST   | /test_projects/{project}/| Add a new test case to {project}         |
 |        | cases                    | Content-Type: application/json           |
 |        |                          | {                                        |
 |        |                          |    "name": "case_foo",                   |
 |        |                          |    "description": "whatever you want"    |
 |        |                          |    "creation_date": "YYYY-MM-DD HH:MM:SS"|
 |        |                          |    "url": "whatever you want"            |
 |        |                          | }                                        |
 +--------+--------------------------+------------------------------------------+
 | PUT    | /test_projects/{project}?| Modify a test case of {project}          |
 |        | case_name={case}          |                                         |
 |        |                          | Content-Type: application/json           |
 |        |                          | {                                        |
 |        |                          |    <the field(s) you want to modify>     |
 |        |                          | }                                        |
 +--------+--------------------------+------------------------------------------+
 | DELETE | /test_projects/{project}/| Delete a test case                       |
 |        | case_name={case}         |                                          |
 +----------------+----------------+--------------------------------------------+

**Test Results:**::

 +--------+--------------------------+------------------------------------------+
 | Method | Path                     | Description                              |
 +========+==========================+==========================================+
 | GET    |/results/project={project}| Get the test results of {project}        |
 +--------+--------------------------+------------------------------------------+
 | GET    |/results/case={case}      | Get the test results of {case}           |
 +--------+--------------------------+------------------------------------------+
 | GET    |/results?pod={pod}        | get the results on pod {pod}             |
 +--------+--------------------------+------------------------------------------+
 | GET    |/results?installer={inst} | Get the test results of installer {inst} |
 +--------+--------------------------+------------------------------------------+
 | GET    |/results?version={version}| Get the test results of scenario         |
 |        |                          | {version}. Initially the version param   |
 |        |                          | was reflecting git version, in Functest  |
 |        |                          | it was decided to move to scenario       |
 +--------+--------------------------+------------------------------------------+
 | GET    |/results?project={project}| Get all the results of the test case     |
 |        |&case={case}              | {case} of the project {project} with     |
 |        |&version={scenario}       | version {scenario} installed by installer|
 |        |&installer={installer}    | {installer} on POD {pod} stored since    |
 |        |&pod={pod}                | {days} days                              |
 |        |                          | {project_name} and {case_name} are       |
 |        |&period={days}            | mandatory, the other parameters are      |
 |        |                          | optional.                                |
 +--------+--------------------------+------------------------------------------+
 | POST   | /results                 | Add a new test results                   |
 |        |                          | Content-Type: application/json           |
 |        |                          | {                                        |
 |        |                          |    "project_name": "project_foo",        |
 |        |                          |    "case_name": "case_foo",              |
 |        |                          |    "pod_name": "pod_foo",                |
 |        |                          |    "installer": "installer_foo",         |
 |        |                          |    "version": "scenario_foo",            |
 |        |                          |    "details": <your results>             |
 |        |                          | }                                        |
 +--------+--------------------------+------------------------------------------+


**Dashboard:**::

 +--------+--------------------------+------------------------------------------+
 | Method | Path                     | Description                              |
 +========+==========================+==========================================+
 | GET    |/dashboard?               | Get all the dashboard ready results of   |
 |        |&project={project}        | {case} of the project {project}          |
 |        |&case={case}              | version {scenario} installed by installer|
 |        |&version={scenario}       | {installer} on POD {pod} stored since    |
 |        |&installer={installer}    | {days} days                              |
 |        |&pod={pod}                |                                          |
 |        |&period={days}            | {project_name} and {case_name} are       |
 |        |                          | mandatory, the other parameters are      |
 |        |                          | optional.                                |
 +--------+--------------------------+------------------------------------------+


The results with dashboard method are post-processed from raw results.
Please note that dashboard results are not stored. Only raw results are stored.



Test Dashboard
--------------

Based on dashboard post-porcessed results, a Test dashboard is automatically
generated.

TODO LF
or http://testresults.opnfv.org/proto/


Troubleshooting
===============

VIM
---

vPing
^^^^^


vPing_userdata
^^^^^^^^^^^^^^


Tempest
^^^^^^^

In the upstream OpenStack CI all the Tempest test cases are supposed to pass.
If some test cases fail in an OPNFV deployment, the reason is very probably one
of the following:

+-----------------------------+------------------------------------------------+
| Error                       | Details                                        |
+=============================+================================================+
| Resources required for test | Such resources could be e.g. an external       |
| case execution are missing  | network and access to the management subnet    |
|                             | (adminURL) from the Functest docker container. |
+-----------------------------+------------------------------------------------+
| OpenStack components or     | Check running services in the controller and   |
| services are missing or not | compute nodes (e.g. with "systemctl" or        |
| configured properly         | "service" commands). Configuration parameters  |
|                             | can be verified from related .conf files       |
|                             | located under /etc/<component> directories.    |
+--------------------------------+---------------------------------------------+
| Some resources required for | The tempest.conf file, automatically generated |
| execution test cases are    | by Rally in Functest, does not contain all the |
| missing                     | needed parameters or some parameters are not   |
|                             | set properly.                                  |
|                             | The tempest.conf file is located in /home/opnfv|
|                             | /.rally/tempest/for-deployment-<UUID> in       |
|                             | Functest container                             |
|                             | Use "rally deployment list" command in order to|
|                             | check UUID of current deployment.              |
+-----------------------------+------------------------------------------------+


When some Tempest test case fails, captured traceback and possibly also related
REST API requests/responses are output to the console.
More detailed debug information can be found from tempest.log file stored into
related Rally deployment folder.


Rally
^^^^^

Same error causes than for Tempest mentioned above may lead to error in Rally.

Controllers
-----------

ODL
^^^


ONOS
^^^^


OpenContrail
^^^^^^^^^^^^


Feature
-------

vIMS
^^^^


References
==========

.. _`[1]`: Functest configuration guide URL
.. _`[2]`: http://docs.openstack.org/developer/tempest/overview.html
.. _`[3]`: https://rally.readthedocs.org/en/latest/index.html
.. _`[4]`: http://events.linuxfoundation.org/sites/events/files/slides/Functest%20in%20Depth_0.pdf
.. _`[5]`: https://github.com/Orange-OpenSource/opnfv-cloudify-clearwater/blob/master/openstack-blueprint.yaml
.. _`[6]`: https://wiki.opnfv.org/opnfv_test_dashboard
.. _`[7]`: http://testresults.opnfv.org/testapi/test_projects/functest/cases
.. _`[8]`: https://wiki.openstack.org/wiki/Governance/DefCoreCommittee
.. _`[9]`: https://git.opnfv.org/cgit/functest/tree/testcases/VIM/OpenStack/CI/libraries/os_defaults.yaml
.. _`[10]`:https://git.opnfv.org/cgit/functest/tree/testcases/VIM/OpenStack/CI/rally_cert/task.yaml

OPNFV main site: opnfvmain_.

OPNFV functional test page: opnfvfunctest_.

IRC support chan: #opnfv-testperf

.. _opnfvmain: http://www.opnfv.org
.. _opnfvfunctest: https://wiki.opnfv.org/opnfv_functional_testing
.. _`OpenRC`: http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html
.. _`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html
.. _`config_test.py` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.py
.. _`config_functest.yaml` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.yaml

