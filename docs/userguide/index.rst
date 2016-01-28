*************************
OPNFV FUNCTEST user guide
*************************

.. toctree::
   :numbered:
   :maxdepth: 2


============
Introduction
============

The goal of this document is describing the Functest test cases for Brahmaputra.
A presentation has been created for the first OPNFV Summit: `[4]`

This guide will detail how to launch the different tests assuming that Functest container has been properly installed `[1]`_.


=============================
Description of the test cases
=============================

Functest is an OPNFV project dedicated to functional testing.
In the continuous integration, it is launched after a fresh installation of an OPNFV solution to verify the basic functions.

Functest includes several test suites that usually include several test cases.
Some are developped within the Functest project, some in dedicated feature projects.

The current list of test suites can be distributed in 3 main domains:

+----------------+----------------+---------------------------------------------------------+
| Component      | Test suite     | Comments                                                |
+----------------+----------------+---------------------------------------------------------+
|                | vPing          | NFV "Hello World"                                       |
|    VIM         +----------------+---------------------------------------------------------+
|(Virtualised    | Tempest        | OpenStack reference test suite `[2]`_                   |
| Infrastructure +----------------+---------------------------------------------------------+
| Manager)       | Rally scenario | OpenStack testing tool testing OpenStack modules `[3]`_ |
+----------------+----------------+---------------------------------------------------------+
|                | odl            |                                                         |
|                +----------------+---------------------------------------------------------+
| Controllers    | onos           |                                                         |
|                +----------------+---------------------------------------------------------+
|                | opencontrail   |                                                         |
+----------------+----------------+---------------------------------------------------------+
| Features       | vIMS           | Show the capability to deploy a real NFV testcase       |
|                +----------------+---------------------------------------------------------+
|                | X              |                                                         |
+----------------+----------------+---------------------------------------------------------+


Most of the test suites are developed upstream. For example, Tempest `[2]`_ is the OpenStack integration test suite.
Functest is in charge of the integration of different functional test suites in OPNFV.

In Functest we customized the list of tests within Tempest but do not created our own test cases.
Some OPNFV feature projects (.e.g. SDNVPN) may create tempest scenario upstream that are integrated in our Tempest through our configuration.

The test results are pushed into a test result database (when possible) in order to build a test dashboard.

There is no real notion of Test domain or Test coverage yet, we tried to cover basic components such as VIM and controllers and integrate the tests of the feature projects.

The vIMS test case was also integrated to demonstrate the capability to deploy a relatively complex NFV scenario on top of the OPNFV infrastructure.

Functest considers OPNFV as a black box. OPNFV, since Brahmaputra, offers lots of possible combination (3 controllers, 4 installers).

However most of the tests (except obviously those dedicated to a specific controller) shall be runnable on any configuration.

The different scenarios are described in the section hereafter.

VIM
===

vPing
-----

The goal of this test can be described as follow::

 vPing test case
 +-------------+                   +-------------+
 |             |                   |             |
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
 |             |                   |             |
 |             | Check console log |             |
 |             |    If ping:       |             |
 |             |      exit OK      |             |
 |             |    else (timeout) |             |
 |             |      exit KO      |             |
 |             |                   |             |
 |             |                   |             |
 +-------------+                   +-------------+


This example, using OpenStack Python clients can be considered as an "Hello World" example and may be modified for future use.
It is the first basic example, it must work on any configuration.

Tempest
-------

Tempest `[2]`_ is the reference OpenStack Integration test suite. It is a set of integration tests to be run against a live OpenStack cluster. 
Tempest has batteries of tests for OpenStack API validation, Scenarios, and other specific tests useful in validating an OpenStack deployment.

We use Rally `[3]`_ to run Tempest suite.
Rally generates automatically tempest.conf configuration file.
Before running actual test cases Functest creates needed resources and updates needed parameters into the configuration file.
When the Tempest suite is run, each test duration is measured and full console output is stored into tempest.log file.

We considered the smoke test suite for Arno. For Brahmaputra, we decided to customize the list of test cases using the --tests-file option introduced in Rally in version 0.1.2.

The customized test list is available on the Functest repo `[4]`_ and contains more than 200 tempest test cases chosen for Functest deployment.
The list consists of two main parts:

  1) Set of tempest smoke test cases
  2) Set of test cases from DefCore list (https://wiki.openstack.org/wiki/Governance/DefCoreCommittee)

The goal of Tempest test suite is to check the basic functionality of different OpenStack components on an OPNFV fresh installation using corresponding REST API interfaces.


Rally bench test suites
-----------------------

Rally `[3]`_ is a benchmarking tool that answers the question: “How does OpenStack work at scale?”.

The goal of this test suite is to test the different modules of OpenStack and get significant figures that could help us to define telco Cloud KPI.

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

For Brahmaputra, we integrated the rally certification feature introduced in Rally 0.1.1.

SLA


SDN Controllers
===============

Brahmaputra introduces new SDN controllers in addition of odl already integrated in Arno.
There are currently 3 possible controllers:

 * odl
 * onos
 * opencontrail

OpenDaylight
------------

The ODL test suite consists of a set of basic tests inherited from ODL project.
The suite verifies creation and deletion of networks, subnets and ports with OpenDaylight and Neutron.

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
----

For ONOS function test,TestON Framework is being used.
The test cases contains L2 and L3 function.We config the function by OpenStack,and then check it in ONOS.
Following describe the test cases:

 * onosfunctest: The mainly executable file,contains init the docker environment for test and function call of FUNCvirNetNB and FUNCvirNetNBL3
 * FUNCvirNetNB

   * Create Network :: Post Network data and check it in ONOS
   * Update Network :: Update the Network and compare it in ONOS
   * Delete Network :: Delete the Network and check if it's NULL in ONOS or not
   * Create Subnet :: Post Subnet data and check it in ONOS
   * Update Subnet :: Update the Subnet and compare it in ONOS
   * Delete Subnet :: Delete the Subnet and check if it's NULL in ONOS or not
   * Create Port :: Post Port data and check it in ONOS
   * Update Port :: Update the Port and compare it in ONOS
   * Delete Port :: Delete the Port and check if it's NULL in ONOS or not

 * FUNCvirNetNBL3

   * Create Router :: Post dataes for create Router and check it in ONOS
   * Update Router :: Update the Router and compare it in ONOS
   * Delete Router :: Delete the Router dataes and check it in ONOS
   * Create RouterInterface :: Post RouterInterface data to an exist Router and check it in ONOS
   * Delete RouterInterface :: Delete the RouterInterface and check the Router
   * Create FloatingIp :: Post dataes for create FloatingIp and check it in ONOS
   * Update FloatingIp :: Update the FloatingIp and compare it in ONOS
   * Delete FloatingIp :: Delete the FloatingIp and check if it's NULL in ONOS or not
   * Create External Gateway :: Post dataes for create External Gateway to an exit Router and check it
   * Update External Gateway :: Update the External Gateway and compare it
   * Delete External Gateway :: Delete the External Gateway and check if it's NULL in ONOS or not


OpenContrail
------------
TODO



Features
========

vIMS
----
The goal of this test suite consists in:
 * deploying a VNF orchestrator (cloudify)
 * deploy a Clearwater vIMS (IP Multimedia Subsystem) VNF from this orchestrator based on a TOSCA blueprint defined in `[5]`_
 * run suite of signaling tests on top of this VNF

The Clearwater architecture may be described as follow:

.. figure:: ../images/clearwater-architecture.png
   :align: center
   :alt: vIMS architecture

The duration of each step (orchestion deployment, VNF deployment and test), as well as test results, are stored and, in CI, pushed into the test collection database.

Promise
-------

Promise provides a basic set of test cases as part of Brahmaputra.

The available 33 test cases can be grouped into 7 test suites:

    #. Add a new OpenStack provider into resource pool: Registers   
       OpenStack into a new resource pool and adds more capacity associated
       with this pool.

    #. Allocation without reservation: Creates a new server in OpenStack
       and adds a new allocation record in Promise shim-layer.

    #. Allocation using reservation for immediate use: Creates a resource
       reservation record with no start/end time and immediately creates a new
       server in OpenStack and add a new allocation record in Promise
       shim-layer.

    #. Reservation for future use: Creates a resource reservation record
       for a future start time, queries, modifies and cancels the newly created
       reservation.

    #. Capacity planning: Decreases and increases the available capacity
       from a provider in the future and queries the available collections and
       utilizations.

    #. Reservation with conflict: Tries to create reservations for
       immediate and future use with conflict.

    #. Cleanup test allocations: Destroys all allocations in OpenStack.

The test results are pushed into the LF test DB:
  * Duration of the Promise test case 
  * Number of tests / failures

The specific parameters for Promise can be found in config_functest.yaml and
include::

   promise:
     general:
         tenant_name: Name of the OpenStack tenant/project (e.g. promise)
         tenant_description: Description of the OpenStack tenant (e.g. promise Functionality Testing)
         user_name: Name of the user tenant (e.g. promiser)
         user_pwd: Password of the user tenant (e.g. test)
         image_name: Name of the software image (e.g. promise-img)
         flavor_name: Name of the flavor (e.g. promise-flavor with 1 vCPU and 512 MB RAM)
         flavor_vcpus: 1
         flavor_ram: 512
         flavor_disk: 0


==============
Manual testing
==============

Once you have installed Functest docker file `[1]`_, and configured the system (though /home/opnfv/repos/functest/docker/prepare_env.sh script), you are ready to run the tests.

The script run_tests.sh has several options::

    ./run_tests.sh -h
    Script to trigger the tests automatically.

    usage:
        bash run_tests.sh [--offline] [-h|--help] [-t <test_name>]

    where:
        -h|--help         show this help text
        -r|--report       push results to database (false by default)
        -n|--no-clean     do not clean up OpenStack resources after test run
        -t|--test         run specific set of tests
          <test_name>     one or more of the following: vping,odl,rally,tempest,vims. Separated by comma.

    examples:
        run_tests.sh
        run_tests.sh --test vping,odl
        run_tests.sh -t tempest,rally --no-clean

The -o option can be used to run the container offline (in case you are in a summit where there is no Internet connection...). It is an experimental option.

The -r option is used by the Continuous Integration in order to push the test results into a test collection database, see in next section for details. In manual mode, you must not use it, your try will be anyway probably rejected as your POD must be declared in the database to collect the data.

The -n option is used for preserving all the existing OpenStack resources after execution test cases. 

The -t option can be used to specify the list of test you want to launch, by default Functest will try to launch all its test suites in the following order vPing, odl, Tempest, vIMS, Rally. You may launch only one single test by using -t <the test you want to launch>

Within Tempest test suite you can define which test cases you want to execute in your environment by editing test_list.txt file before executing run_tests.sh script.

Please note that Functest includes cleaning mechanism in order to remove everything except what was present after a fresh install. If you create your own VMs, tenants, networks etc. and then launch Functest, they all will be deleted after executing the tests. Use --no-clean option with run_test.sh in order to preserve all the existing resources. However, be aware that Tempest and Rally create of lot of resources (users, tenants, networks, volumes etc.) that are not always properly cleaned, so this cleaning function has been set to keep the system as clean as possible after a full Functest run.

You may also add you own test by adding a section into the function run_test()


=================
Automated testing
=================

As mentioned in `[1]`, the prepare-env.sh and run_test.sh can be executed within the container from jenkins. 2 jobs have been created, one to run all the test and one that allows testing test suite by test suite. You thus just have to launch the acurate jenkins job on the target lab, all the tests shall be automatically run.


============
Test results
============

VIM
===

vPing
-----

vPing result is displayed in the console::

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
-------

The Tempest results are displayed in the console::

    FUNCTEST.info: Running Tempest tests...
    2016-01-06 16:07:32,271 - run_tempest - INFO - Creating tenant and user for Tempest suite
    2016-01-06 16:07:38,864 - run_tempest - INFO - Starting Tempest test suite: '--tests-file /home/opnfv/repos/functest/testcases/VIM/OpenStack/CI/custom_tests/test_list.txt'.

    {23} tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_get_flavor [0.131741s] ... ok
    {13} tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_get_image [0.367465s] ... ok
    {23} tempest.api.compute.flavors.test_flavors.FlavorsV2TestJSON.test_list_flavors [0.089323s] ... ok
    {13} tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images [0.245090s] ... ok
    {13} tempest.api.compute.images.test_list_images.ListImagesTestJSON.test_list_images_with_detail [0.434553s] ... ok
    {7} setUpClass (tempest.api.identity.admin.v3.test_services.ServicesTestJSON) [0.000000s] ... FAILED
    {5} setUpClass (tempest.api.identity.admin.v3.test_groups.GroupsV3TestJSON) [0.000000s] ... FAILED
    {4} setUpClass (tempest.api.network.test_floating_ips.FloatingIPTestJSON) [0.000000s] ... FAILED
    {10} setUpClass (tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON) [0.000000s] ... FAILED
    {3} tempest.api.compute.servers.test_servers.ServersTestJSON.test_create_server_with_admin_password [3.107954s] ... ok
    {9} tempest.api.compute.security_groups.test_security_groups.SecurityGroupsTestJSON.test_security_groups_create_list_delete [2.933169s] ... ok
    .......
    {1} tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_network [1.002445s] ... ok
    {1} tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_port [1.553398s] ... ok
    {1} tempest.api.network.test_networks.BulkNetworkOpsIpV6TestJSON.test_bulk_create_delete_subnet [3.082247s] ... ok
    {3} tempest.scenario.test_network_basic_ops.TestNetworkBasicOps.test_network_basic_ops [48.295630s] ... ok
    {6} tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_rebuild_server [78.782038s] ... ok
    {6} tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_confirm [15.597440s] ... ok
    {6} tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_resize_server_revert [19.248253s] ... ok
    {6} tempest.api.compute.servers.test_server_actions.ServerActionsTestJSON.test_stop_start_server [7.078850s] ... ok
    {6} tempest.api.compute.volumes.test_attach_volume.AttachVolumeTestJSON.test_attach_detach_volume [40.311720s] ... ok
    {6} tempest.api.volume.test_volumes_actions.VolumesV1ActionsTest.test_attach_detach_volume_to_instance [1.159194s] ... ok
    .......
    ======
    Totals
    ======
    Ran: 199 tests in 241.0000 sec.
     - Passed: 182
     - Skipped: 3
     - Expected Fail: 0
     - Unexpected Success: 0
     - Failed: 14
    Sum of execute time for each test: 481.0934 sec.

In order to check all the available test case related debug information, please inspect tempest.log file stored into related Rally deployment folder.

Rally
-----
 TODO

Controllers
===========

odl
---

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

 Neutron.Delete Networks :: Checking Network deleted in OpenStack a... | FAIL |
 2 critical tests, 1 passed, 1 failed
 2 tests total, 1 passed, 1 failed
 ==============================================================================
 Neutron :: Test suite for Neutron Plugin                              | FAIL |
 18 critical tests, 15 passed, 3 failed
 18 tests total, 15 passed, 3 failed
 ==============================================================================
 Output:  /home/jenkins-ci/workspace/functest-opnfv-jump-2/output.xml
 Log:     /home/jenkins-ci/workspace/functest-opnfv-jump-2/log.html
 Report:  /home/jenkins-ci/workspace/functest-opnfv-jump-2/report.html

3 result files are generated:
 * output.xml
 * log.html
 * report.html

 ODL result page

.. figure:: ./images/functestODL.png
   :width: 170mm
   :align: center
   :alt: ODL suite result page


Known issues
------------

Tests are expected to fail now:
 * Check port deleted in OpenDaylight
 * Check subnet deleted in OpenDaylight
 * Check Network deleted in OpenDaylight

These failures to delete objects in OpenDaylight (when removed via OpenStack Neutron) are due to the following bug: https://bugs.opendaylight.org/show_bug.cgi?id=3052.

onos
----

The ONOS test logs output to OnosSystemTest/TestON/logs with ONOSCI_PATH added,and also can be seen in the console::

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

There's a Result summary for each testcase,and a total summary for the whole test file,if any problem occured,ERROR can be seen in the testcase summary and total summary::

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

opencontrail
------------

TODO


Feature
=======

vIMS
----

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


==========================
Functest in test Dashboard
==========================

The OPNFV testing group created a test collection database to collect the test results from CI.
Any lab integrated in CI can push the results to this database.

The idea is to centralize the resultes and create a dashboard to give a high level overview of the test activities.
You can find more information about the dashboard from Testing Dashboard wiki page `[6]`_.


===============
Troubleshooting
===============

VIM
===

vPing
-----


Tempest
-------

In the upstream OpenStack CI all the Tempest test cases are supposed to pass. If some test cases fail in an OPNFV deployment, the reason is very probably one of the following:

 * Some resources required for execution test cases are missing. Such resources could be e.g. an external network and access to the management subnet (adminURL) from the Functest docker container.
 * Some OpenStack components or services are missing or not configured properly. You can check running services in the controller and compute nodes e.g. with "systemctl" or "service" commands. Configuration parameters can be verified from related .conf files located under /etc/<component> directories. 
 * Used tempest.conf file doesn't contain all the needed parameters or some parameters are not set properly. When using Functest, tempest.conf file is generated by Rally and updated with needed parameters automatically before executing Tempest cases. You can find the used configuration file e.g. with "find / -name tempest.conf" command. Use "rally deployment list" command in order to check UUID of current deployment.

When some Tempest test case fails, captured traceback and possibly also related REST API requests/responses are output to the console.
More detailed debug information can be found from tempest.log file stored into related Rally deployment folder.


Rally
-----


Controllers
===========

odl
---


onos
----


opencontrail
------------


Feature
=======

vIMS
----


==========
References
==========

.. _`[1]`: Functest configuration guide URL
.. _`[2]`: http://docs.openstack.org/developer/tempest/overview.html
.. _`[3]`: https://rally.readthedocs.org/en/latest/index.html
.. _`[4]`: http://events.linuxfoundation.org/sites/events/files/slides/Functest%20in%20Depth_0.pdf
.. _`[5]`: https://github.com/Orange-OpenSource/opnfv-cloudify-clearwater/blob/master/openstack-blueprint.yaml
.. _`[6]`: https://wiki.opnfv.org/opnfv_test_dashboard


OPNFV main site: opnfvmain_.

OPNFV functional test page: opnfvfunctest_.

IRC support chan: #opnfv-testperf

.. _opnfvmain: http://www.opnfv.org
.. _opnfvfunctest: https://wiki.opnfv.org/opnfv_functional_testing
.. _`OpenRC`: http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html
.. _`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html
.. _`config_test.py` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.py
.. _`config_functest.yaml` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.yaml

