.. _functest-userguide:

.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

=========================
OPNFV FUNCTEST user guide
=========================

.. toctree::
   :maxdepth: 2

Version history
===============
+------------+----------+------------------+----------------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**                      |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+
| 2016-08-17 | 1.0.0    | Juha Haapavirta  | Colorado release                 |
|            |          | Column Gaynor    |                                  |
+------------+----------+------------------+----------------------------------+
| 2017-01-23 | 1.0.1    | Morgan Richomme  | Adaptations for Danube           |
|            |          |                  |                                  |
|            |          |                  |                                  |
+------------+----------+------------------+----------------------------------+


Introduction
============

The goal of this document is to describe the OPNFV Functest test cases and to
provide a procedure to execute them. In the OPNFV Danube system release,
a Functest CLI utility is introduced for an easier execution of test procedures.

**IMPORTANT**: It is assumed here that the Functest Docker container is already
properly deployed and that all instructions described in this guide are to be
performed from *inside* the deployed Functest Docker container.

.. include:: ./introduction.rst

The different test cases are described in the remaining sections of this document.

VIM (Virtualized Infrastructure Manager)
----------------------------------------

Healthcheck tests
^^^^^^^^^^^^^^^^^
In Danube, healthcheck tests have been refactored and rely on SNAPS, a
OPNFV middleware project.

SNAPS stands for "SDN/NFV Application development Platform and Stack".
SNAPS is an object-oriented OpenStack library packaged with tests that exercise
OpenStack.
More information on SNAPS can be found in  `[13]`_

Three tests are declared as healthcheck tests and can be used for gating by the
installer, they cover functionally the tests previously done by healthcheck
test case.

The tests are:


 * *connection_check*
 * *api_check*
 * *snaps_health_check*

Connection_check consists in 9 test cases (test duration < 5s) checking the
connectivity with Glance, Keystone, Neutron, Nova and the external network.

Api_check verifies the retrieval of OpenStack clients: Keystone, Glance,
Neutron and Nova and may perform some simple queries. When the config value of
snaps.use_keystone is True, functest must have access to the cloud's private
network. This suite consists in 49 tests (test duration < 2 minutes).

snaps_health_check creates instance, allocate floating IP, connect to the VM.
This test replaced the previous Colorado healthcheck test.

Self-obviously, successful completion of the 'healthcheck' testcase is a
necessary pre-requisite for the execution of all other test Tiers.


vPing_ssh
^^^^^^^^^

Given the script **ping.sh**::

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


The goal of this test is to establish an SSH connection using a floating IP
on the Public/External network and verify that 2 instances can talk over a Private
Tenant network::

 vPing_ssh test case
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
 |             | Establish SSH      |             |
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
 |             |    else (timeout): |             |
 |             |      exit Failed   |             |
 |             |                    |             |
 +-------------+                    +-------------+

This test can be considered as an "Hello World" example.
It is the first basic use case which **must** work on any deployment.

vPing_userdata
^^^^^^^^^^^^^^

This test case is similar to vPing_ssh but without the use of Floating IPs
and the Public/External network to transfer the ping script.
Instead, it uses Nova metadata service to pass it to the instance at booting time.
As vPing_ssh, it checks that 2 instances can talk to
each other on a Private Tenant network::

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

When the second VM boots it will execute the script passed as userdata
automatically. The ping will be detected by periodically capturing the output
in the console-log of the second VM.


Tempest
^^^^^^^

Tempest `[2]`_ is the reference OpenStack Integration test suite.
It is a set of integration tests to be run against a live OpenStack cluster.
Tempest has suites of tests for:

  * OpenStack API validation
  * Scenarios
  * Other specific tests useful in validating an OpenStack deployment

Functest uses Rally `[3]`_ to run the Tempest suite.
Rally generates automatically the Tempest configuration file **tempest.conf**.
Before running the actual test cases,
Functest creates the needed resources (user, tenant) and
updates the appropriate parameters into the configuration file.

When the Tempest suite is executed, each test duration is measured and the full
console output is stored to a *log* file for further analysis.

The Tempest testcases are distributed accross two
Tiers:

  * Smoke Tier - Test Case 'tempest_smoke_serial'
  * Components Tier - Test case 'tempest_full_parallel'

NOTE: Test case 'tempest_smoke_serial' executes a defined set of tempest smoke
tests with a single thread (i.e. serial mode). Test case 'tempest_full_parallel'
executes all defined Tempest tests using several concurrent threads
(i.e. parallel mode). The number of threads activated corresponds to the number
of available logical CPUs.

The goal of the Tempest test suite is to check the basic functionalities of the
different OpenStack components on an OPNFV fresh installation, using the
corresponding REST API interfaces.


Rally bench test suites
^^^^^^^^^^^^^^^^^^^^^^^

Rally `[3]`_ is a benchmarking tool that answers the question:

*How does OpenStack work at scale?*

The goal of this test suite is to benchmark all the different OpenStack modules and
get significant figures that could help to define Telco Cloud KPIs.

The OPNFV Rally scenarios are based on the collection of the actual Rally scenarios:

 * authenticate
 * cinder
 * glance
 * heat
 * keystone
 * neutron
 * nova
 * quotas
 * requests

A basic SLA (stop test on errors) has been implemented.

The Rally testcases are distributed accross two Tiers:

  * Smoke Tier - Test Case 'rally_sanity'
  * Components Tier - Test case 'rally_full'

NOTE: Test case 'rally_sanity' executes a limited number of Rally smoke test
cases. Test case 'rally_full' executes the full defined set of Rally tests.


Refstack-client to run Defcore testcases
-----------------------------------------

Refstack-client `[8]`_ is a command line utility that allows you to
execute Tempest test runs based on configurations you specify.
It is the official tool to run Defcore `[9]`_ testcases,
which focuses on testing interoperability between OpenStack clouds.

Refstack-client is integrated in functest, consumed by dovetail, which
intends to define and provide a set of OPNFV related validation criteria
that will provide input for the evaluation of the use of OPNFV trademarks.
This progress is under the guideline of Compliance Verification Program(CVP).

Running methods
^^^^^^^^^^^^^^^

Two running methods are provided after refstack-client integrated into
functest, functest command line and manually, respectively.

By default, for Defcore test cases run by functest command line,
are run followed with automatically generated
configuration file, i.e., refstack_tempest.conf. In some circumstances,
the automatic configuration file may not quite satisfied with the SUT,
Functest also inherits the Refstack-client command line and provides a way
for users to set its configuration file according to its own SUT manually.

*command line*

Inside the functest container, first to prepare functest environment:

::

  cd /home/opnfv/repos/functest
  pip install -e .
  functest env prepare

then to run default defcore testcases by using refstack-client:

::

  functest testcase run refstack_defcore

In OPNFV Continuous Integration(CI) system, the command line method is used.

*manually*

Inside the functest container, first to prepare the refstack virtualenv:

::

  cd /home/opnfv/repos/refstack-client
  source .venv/bin/activate

then prepare the tempest configuration file and the testcases want to run with the SUT,
run the testcases with:

::

  ./refstack-client test -c <Path of the tempest configuration file to use> -v --test-list <Path or URL of test list>

using help for more information:

::

  ./refstack-client --help
  ./refstack-client test --help

Reference tempest configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*command line method*

When command line method is used, the default tempest configuration file
is generated by Rally.

*manually*

When running manually is used, recommended way to generate tempest configuration
file is:

::

  cd /home/opnfv/repos/functest/functest/opnfv_tests/openstack/refstack_client
  python tempest_conf.py

a file called tempest.conf is stored in the current path by default, users can do
some adjustment according to the SUT:

::

  vim refstack_tempest.conf

a reference article can be used `[10]`_.

Defcore testcases
^^^^^^^^^^^^^^^^^^

*Danube Release*

Set of DefCore tempest test cases not flagged and required.
It only contains OpenStack core (no object storage)
The approved guidelines (2016.08) are valid for Kilo, Liberty, Mitaka
and Newton releases of OpenStack
The list can be generated using the Rest API from RefStack project:
https://refstack.openstack.org/api/v1/guidelines/2016.08/tests?target=compute&type=required&alias=true&flag=false


snaps_smoke
------------

This test case contains tests that setup and destroy environments with VMs with
and without Floating IPs with a newly created user and project. Set the config
value snaps.use_floating_ips (True|False) to toggle this functionality. When
the config value of snaps.use_keystone is True, functest must have access
the cloud's private network.
This suite consists in 38 tests (test duration < 10 minutes)


SDN Controllers
---------------

There are currently 3 available controllers:

 * OpenDaylight (ODL)
 * ONOS
 * OpenContrail (OCL)

OpenDaylight
^^^^^^^^^^^^

The OpenDaylight (ODL) test suite consists of a set of basic tests inherited
from the ODL project using the Robot `[11]`_ framework.
The suite verifies creation and deletion of networks, subnets and ports with
OpenDaylight and Neutron.

The list of tests can be described as follows:

 * Basic Restconf test cases
   * Connect to Restconf URL
   * Check the HTTP code status

 * Neutron Reachability test cases
   * Get the complete list of neutron resources (networks, subnets, ports)

 * Neutron Network test cases
   * Check OpenStack networks
   * Check OpenDaylight networks
   * Create a new network via OpenStack and check the HTTP status code returned by Neutron
   * Check that the network has also been successfully created in OpenDaylight

 * Neutron Subnet test cases
   * Check OpenStack subnets
   * Check OpenDaylight subnets
   * Create a new subnet via OpenStack and check the HTTP status code returned by Neutron
   * Check that the subnet has also been successfully created in OpenDaylight

 * Neutron Port test cases
   * Check OpenStack Neutron for known ports
   * Check OpenDaylight ports
   * Create a new port via OpenStack and check the HTTP status code returned by Neutron
   * Check that the new port has also been successfully created in OpenDaylight

 * Delete operations
   * Delete the port previously created via OpenStack
   * Check that the port has been also succesfully deleted in OpenDaylight
   * Delete previously subnet created via OpenStack
   * Check that the subnet has also been successfully deleted in OpenDaylight
   * Delete the network created via OpenStack
   * Check that the network has also been succesfully deleted in OpenDaylight

Note: the checks in OpenDaylight are based on the returned HTTP status
code returned by OpenDaylight.


ONOS
^^^^

TestON Framework is used to test the ONOS SDN controller functions.
The test cases deal with L2 and L3 functions.
The ONOS test suite can be run on any ONOS compliant scenario.

The test cases are described as follows:

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

   * Create Router: Post data for create Router and check it in ONOS
   * Update Router: Update the Router and compare it in ONOS
   * Delete Router: Delete the Router data and check it in ONOS
   * Create RouterInterface: Post Router Interface data to an existing Router
     and check it in ONOS
   * Delete RouterInterface: Delete the RouterInterface and check the Router
   * Create FloatingIp: Post data for create FloatingIp and check it in ONOS
   * Update FloatingIp: Update the FloatingIp and compare it in ONOS
   * Delete FloatingIp: Delete the FloatingIp and check that it is 'NULL' in
     ONOS
   * Create External Gateway: Post data to create an External Gateway for an
     existing Router and check it in ONOS
   * Update External Gateway: Update the External Gateway and compare the change
   * Delete External Gateway: Delete the External Gateway and check that it is
     'NULL' in ONOS


Features
--------

In Danube, functest supports the integration of:

 * barometer
 * bgpvpn
 * doctor
 * domino
 * fds
 * multisite
 * netready
 * odl-sfc
 * promise
 * security_scan

Note: copper is not supported in Danube.

Please refer to the dedicated feature user guides for details.


VNF
---


cloudify_ims
^^^^^^^^^^^^
The IP Multimedia Subsystem or IP Multimedia Core Network Subsystem (IMS) is an
architectural framework for delivering IP multimedia services.

vIMS has been integrated in Functest to demonstrate the capability to deploy a
relatively complex NFV scenario on the OPNFV platform. The deployment of a complete
functional VNF allows the test of most of the essential functions needed for a
NFV platform.

The goal of this test suite consists of:

 * deploy a VNF orchestrator (Cloudify)
 * deploy a Clearwater vIMS (IP Multimedia Subsystem) VNF from this
   orchestrator based on a TOSCA blueprint defined in `[5]`_
 * run suite of signaling tests on top of this VNF

The Clearwater architecture is described as follows:

.. figure:: ../../../images/clearwater-architecture.png
   :align: center
   :alt: vIMS architecture

orchestra_ims
^^^^^^^^^^^^^
Orchestra test case deals with the deployment of OpenIMS with OpenBaton
orchestrator.

parser
^^^^^^

See parser user guide for details: `[12]`_


vyos-vrouter
^^^^^^^^^^^^

This test case deals with the deployment and the test of vyos vrouter with
Cloudify orchestrator. The test case can do testing for interchangeability of
BGP Protocol using vyos.

The Workflow is as follows:
 * Deploy
    Deploy VNF Testing topology by Cloudify using blueprint.
 * Configuration
    Setting configuration to Target VNF and reference VNF using ssh
 * Run
    Execution of test command for test item written YAML format  file.
    Check VNF status and behavior.
 * Reporting
    Output of report based on result using JSON format.

The vyos-vrouter architecture is described in `[14]`_



.. include:: ./runfunctest.rst


Test results
============

Manual testing
--------------

In manual mode test results are displayed in the console and result files
are put in /home/opnfv/functest/results.

Automated testing
--------------

In automated mode, test results are displayed in jenkins logs, a summary is provided
at the end of the job and can be described as follow::

 +==================================================================================================================================================+
 |                                                                FUNCTEST REPORT                                                                   |
 +==================================================================================================================================================+
 |                                                                                                                                                  |
 |  Deployment description:                                                                                                                         |
 |    INSTALLER: fuel                                                                                                                               |
 |    SCENARIO:  os-odl_l2-nofeature-ha                                                                                                             |
 |    BUILD TAG: jenkins-functest-fuel-baremetal-daily-master-324                                                                                   |
 |    CI LOOP:   daily                                                                                                                              |
 |                                                                                                                                                  |
 +=========================+===============+============+===============+===========================================================================+
 | TEST CASE               | TIER          | DURATION   | RESULT        | URL                                                                       |
 +=========================+===============+============+===============+===========================================================================+
 | connection_check        | healthcheck   | 00:02      | PASS          | http://testresults.opnfv.org/test/api/v1/results/58cb62b34079ac000a42e3fe |
 +-------------------------+---------------+------------+---------------+---------------------------------------------------------------------------+
 | api_check               | healthcheck   | 01:15      | PASS          | http://testresults.opnfv.org/test/api/v1/results/58cb62fe4079ac000a42e3ff |
 +-------------------------+---------------+------------+---------------+---------------------------------------------------------------------------+
 | snaps_health_check      | healthcheck   | 00:50      | PASS          | http://testresults.opnfv.org/test/api/v1/results/58cb63314079ac000a42e400 |
 +-------------------------+---------------+------------+---------------+---------------------------------------------------------------------------+
 | vping_ssh               | smoke         | 01:10      | PASS          | http://testresults.opnfv.org/test/api/v1/results/58cb63654079ac000a42e401 |
 +-------------------------+---------------+------------+---------------+---------------------------------------------------------------------------+
 | vping_userdata          | smoke         | 00:59      | PASS          | http://testresults.opnfv.org/test/api/v1/results/58cb63a14079ac000a42e403 |
 +-------------------------+---------------+------------+---------------+---------------------------------------------------------------------------+
 | tempest_smoke_serial    | smoke         | 12:57      | PASS          | http://testresults.opnfv.org/test/api/v1/results/58cb66bd4079ac000a42e408 |
 +-------------------------+---------------+------------+---------------+---------------------------------------------------------------------------+
 | rally_sanity            | smoke         | 10:22      | PASS          | http://testresults.opnfv.org/test/api/v1/results/58cb692b4079ac000a42e40a |
 +-------------------------+---------------+------------+---------------+---------------------------------------------------------------------------+
 | refstack_defcore        | smoke         | 12:28      | PASS          | http://testresults.opnfv.org/test/api/v1/results/58cb6c184079ac000a42e40c |
 +-------------------------+---------------+------------+---------------+---------------------------------------------------------------------------+
 | snaps_smoke             | smoke         | 12:04      | PASS          | http://testresults.opnfv.org/test/api/v1/results/58cb6eec4079ac000a42e40e |
 +-------------------------+---------------+------------+---------------+---------------------------------------------------------------------------+
 | domino                  | features      | 00:29      | PASS          | http://testresults.opnfv.org/test/api/v1/results/58cb6f044079ac000a42e40f |
 +-------------------------+---------------+------------+---------------+---------------------------------------------------------------------------+


Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on:

 * The overall status per scenario and per installer
 * Tempest: Tempest test case including reported errors per scenario and installer
 * vIMS: vIMS details per scenario and installer

.. figure:: ../../../images/functest-reporting-status.png
   :align: center
   :alt: Functest reporting portal Fuel status page

.. include:: ./troubleshooting.rst


References
==========

.. _`[1]`: http://artifacts.opnfv.org/functest/colorado/docs/configguide/#
.. _`[2]`: http://docs.openstack.org/developer/tempest/overview.html
.. _`[3]`: https://rally.readthedocs.org/en/latest/index.html
.. _`[4]`: http://events.linuxfoundation.org/sites/events/files/slides/Functest%20in%20Depth_0.pdf
.. _`[5]`: https://github.com/Orange-OpenSource/opnfv-cloudify-clearwater/blob/master/openstack-blueprint.yaml
.. _`[6]`: https://scap.nist.gov/
.. _`[7]`: https://github.com/OpenSCAP/openscap
.. _`[8]`: https://github.com/openstack/refstack-client
.. _`[9]`: https://github.com/openstack/defcore
.. _`[10]`: https://aptira.com/testing-openstack-tempest-part-1/
.. _`[11]`: http://robotframework.org/
.. _`[12]`: http://artifacts.opnfv.org/parser/colorado/docs/userguide/index.html
.. _`[13]`: https://wiki.opnfv.org/display/PROJ/SNAPS-OO
.. _`[14]`: https://github.com/oolorg/opnfv-functest-vrouter

`OPNFV main site`_

`Functest page`_

IRC support chan: #opnfv-testperf

.. _`OPNFV main site`: http://www.opnfv.org
.. _`Functest page`: https://wiki.opnfv.org/functest
.. _`OpenRC`: http://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html
.. _`Rally installation procedure`: https://rally.readthedocs.org/en/latest/tutorial/step_0_installation.html
.. _`config_functest.yaml` : https://git.opnfv.org/cgit/functest/tree/functest/ci/config_functest.yaml
.. _`Functest reporting`: http://testresults.opnfv.org/reporting/functest/release/danube/index-status-fuel.html
