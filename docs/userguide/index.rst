.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

=========================
OPNFV FUNCTEST user guide
=========================

.. toctree::
   :maxdepth: 2


Introduction
============

The goal of this documents is to describe the Functest test cases as well as
provide a procedure about how to execute them.

A presentation has been created for the first OPNFV Summit `[4]`_.

It is assumed that Functest container has been properly installed `[1]`_.

.. include:: ./introduction.rst

The different scenarios are described in the section hereafter.

VIM (Virtualized Infrastructure Manager)
---

vPing_SSH
^^^^^^^^^

Given the script 'ping.sh'::

    #!/bin/sh
    while true; do
        ping -c 1 $1 2>&1 >/dev/null
        RES=$?
        if [ "Z$RES" = "Z0" ] ; then
            echo 'vPing OK'
            break
        else
            echo 'vPing KO'
        fi
    sleep 1
    done

The goal of this test is described as follows::

 vPing test case
 +-------------+                    +-------------+
 |             |                    |             |
 |             | Boot VM1 with IP1  |             |
 |             +------------------->|             |
 |   Tester    |                    |   System    |
 |             | Boot VM2           |    Under    |
 |             +------------------->|     Test    |
 |             |                    |             |
 |             | Create floating IP |             |
 |             +------------------->|             |
 |             |                    |             |
 |             | Assign floating IP |             |
 |             | to VM2             |             |
 |             +------------------->|             |
 |             |                    |             |
 |             | Stablish SSH       |             |
 |             | connection to VM2  |             |
 |             | through floating IP|             |
 |             +------------------->|             |
 |             |                    |             |
 |             | SCP ping.sh to VM2 |             |
 |             +------------------->|             |
 |             |                    |             |
 |             | VM2 executes       |             |
 |             | ping.sh to VM1     |             |
 |             +------------------->|             |
 |             |                    |             |
 |             |    If ping:        |             |
 |             |      exit OK       |             |
 |             |    else (timeout)  |             |
 |             |      exit Failed   |             |
 |             |                    |             |
 +-------------+                    +-------------+

This test can be considered as an "Hello World" example.
It is the first basic use case which shall work on any deployment.

vPing_userdata
^^^^^^^^^^^^^^

The goal of this test can be described as follows::

 vPing_userdata test case
 +-------------+                    +-------------+
 |             |                    |             |
 |             | Boot VM1 with IP1  |             |
 |             +------------------->|             |
 |             |                    |             |
 |             | Boot VM2 with      |             |
 |             | ping.sh as userdata|             |
 |             | with IP1 as $1.    |             |
 |             +------------------->|             |
 |   Tester    |                    |   System    |
 |             | VM2 exeutes ping.sh|    Under    |
 |             | (ping IP1)         |     Test    |
 |             +------------------->|             |
 |             |                    |             |
 |             | Monitor nova       |             |
 |             |  console-log VM 2  |             |
 |             |    If ping:        |             |
 |             |      exit OK       |             |
 |             |    else (timeout)  |             |
 |             |      exit Failed   |             |
 |             |                    |             |
 +-------------+                    +-------------+

This scenario is similar to the previous one but it uses cloud-init (nova
metadata service) instead of floating IPs and SSH connection. When the second VM
boots it will execute the script automatically and the ping will be detected
capturing periodically the output in the console-log of the second VM.


Tempest
^^^^^^^

Tempest `[2]`_ is the reference OpenStack Integration test suite.
It is a set of integration tests to be run against a live OpenStack cluster.
Tempest has batteries of tests for:

  * OpenStack API validation
  * Scenarios
  * Other specific tests useful in validating an OpenStack deployment

Functest uses Rally `[3]`_ to run the Tempest suite.
Rally generates automatically the Tempest configuration file (tempest.conf).
Before running the actual test cases, Functest creates the needed resources and
updates the appropriate parameters to the configuration file.
When the Tempest suite is executed, each test duration is measured and the full
console output is stored in the tempest.log file for further analysis.

As an addition of Arno, Brahmaputra runs a customized set of Tempest test cases.
The list is specificed through *--tests-file* when running Rally.
This option has been introduced in Rally in version 0.1.2.

The customized test list is available in the Functest repo `[4]`_.
This list contains more than 200 Tempest test cases and can be divided
into two main sections:

  1) Set of tempest smoke test cases
  2) Set of test cases from DefCore list `[8]`_

The goal of the Tempest test suite is to check the basic functionalities of
different OpenStack components on an OPNFV fresh installation using
the corresponding REST API interfaces.


Rally bench test suites
^^^^^^^^^^^^^^^^^^^^^^^

Rally `[3]`_ is a benchmarking tool that answers the question::

 “How does OpenStack work at scale?”.

The goal of this test suite is to benchmark the different OpenStack modules and
get significant figures that could help to define Telco Cloud KPIs.

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

A basic SLA (stop test on errors) have been implemented.


SDN Controllers
---------------

Brahmaputra introduces new SDN controllers.
There are currently 2 possible controllers:

 * OpenDaylight (ODL)
 * ONOS

OpenDaylight
^^^^^^^^^^^^

The OpenDaylight (ODL) test suite consists of a set of basic tests inherited
from the ODL project using the Robot `[11]`_ framework.
The suite verifies creation and deletion of networks, subnets and ports with
OpenDaylight and Neutron.

The list of tests can be described as follows:

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

TestON Framework is used to test the ONOS SDN controller functions.
The test cases deal with L2 and L3 functions.
The ONOS test suite can be run on any ONOS compliant scenario.

The test cases may be described as follows:

 * onosfunctest: The main executable file contains the initialization of
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


Features
--------

vIMS
^^^^
The goal of this test suite consists of:

 * deploy a VNF orchestrator (Cloudify)
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
essential functions needed for a NFV platform.

Promise
^^^^^^^

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

However, these parameters must not be changed, as they are the values expected
by the Promise test suite.

Promise
^^^^^^^
Two test cases have been defined:

  #. Doctor-notification: immediate notification for fault management.

  #. Doctor-mark-down: resource state correction for fault management.

See http://artifacts.opnfv.org/doctor/brahmaputra/docs/userguide/userguide.html
for details.

.. include:: ./runfunctest.rst

Test results
============

For Brahmaputra test results, see the functest results document at:
http://artifacts.opnfv.org/functest/brahmaputra/docs/results/index.html


Test Dashboard
==============

Based on results collected in CI, a test dashboard is dynamically generated:
https://www.opnfv.org/opnfvtestgraphs/per-test-projects/default

A specific dashboard has been created for functest:
http://testresults.opnfv.org/dashboard/

.. include:: ./troubleshooting.rst


References
==========

.. _`[1]`: http://artifacts.opnfv.org/functest/docs/configguide/#functional-testing-installation
.. _`[2]`: http://docs.openstack.org/developer/tempest/overview.html
.. _`[3]`: https://rally.readthedocs.org/en/latest/index.html
.. _`[4]`: http://events.linuxfoundation.org/sites/events/files/slides/Functest%20in%20Depth_0.pdf
.. _`[5]`: https://github.com/Orange-OpenSource/opnfv-cloudify-clearwater/blob/master/openstack-blueprint.yaml
.. _`[6]`: https://wiki.opnfv.org/opnfv_test_dashboard
.. _`[7]`: http://testresults.opnfv.org/testapi/test_projects/functest/cases
.. _`[8]`: https://wiki.openstack.org/wiki/Governance/DefCoreCommittee
.. _`[9]`: https://git.opnfv.org/cgit/functest/tree/testcases/VIM/OpenStack/CI/libraries/os_defaults.yaml
.. _`[10]`: https://git.opnfv.org/cgit/functest/tree/testcases/VIM/OpenStack/CI/rally_cert/task.yaml
.. _`[11]`: http://robotframework.org/

OPNFV main site: opnfvmain_.

OPNFV functional test page: opnfvfunctest_.

IRC support chan: #opnfv-testperf

.. _opnfvmain: http://www.opnfv.org
.. _opnfvfunctest: https://wiki.opnfv.org/opnfv_functional_testing
.. _`OpenRC`: http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html
.. _`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html
.. _`config_test.py` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.py
.. _`config_functest.yaml` : https://git.opnfv.org/cgit/functest/tree/testcases/config_functest.yaml
