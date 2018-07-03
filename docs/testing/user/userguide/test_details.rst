.. SPDX-License-Identifier: CC-BY-4.0

The different test cases are described in the remaining sections of this
document.

VIM (Virtualized Infrastructure Manager)
----------------------------------------

Healthcheck tests
^^^^^^^^^^^^^^^^^
Since Danube, healthcheck tests have been refactored and rely on SNAPS, an
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

Snaps_health_check creates a VM with a single port with an IPv4 address that
is assigned by DHCP and then validates the expected IP with the actual.

The flavors for the SNAPS test cases are able to be configured giving new
metadata values as well as new values for the basic elements of flavor (i.e.
ram, vcpu, disk, ephemeral, swap etc). The snaps.flavor_extra_specs dict in the
config_functest.yaml file could be used for this purpose.

Self-obviously, successful completion of the 'healthcheck' testcase is a
necessary pre-requisite for the execution of all other test Tiers.


vPing_ssh
^^^^^^^^^

Given the script **ping.sh**::

    #!/bin/sh
    ping -c 1 $1 2>&1 >/dev/null
    RES=$?
    if [ "Z$RES" = "Z0" ] ; then
        echo 'vPing OK'
    else
        echo 'vPing KO'
    fi


The goal of this test is to establish an SSH connection using a floating IP
on the Public/External network and verify that 2 instances can talk over a
Private Tenant network::

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
Instead, it uses Nova metadata service to pass it to the instance at booting
time.
As vPing_ssh, it checks that 2 instances can talk to
each other on a Private Tenant network::

 vPing_userdata test case
 +-------------+                     +-------------+
 |             |                     |             |
 |             | Boot VM1 with IP1   |             |
 |             +-------------------->|             |
 |             |                     |             |
 |             | Boot VM2 with       |             |
 |             | ping.sh as userdata |             |
 |             | with IP1 as $1.     |             |
 |             +-------------------->|             |
 |   Tester    |                     |   System    |
 |             | VM2 executes ping.sh|    Under    |
 |             | (ping IP1)          |     Test    |
 |             +-------------------->|             |
 |             |                     |             |
 |             | Monitor nova        |             |
 |             |  console-log VM 2   |             |
 |             |    If ping:         |             |
 |             |      exit OK        |             |
 |             |    else (timeout)   |             |
 |             |      exit Failed    |             |
 |             |                     |             |
 +-------------+                     +-------------+

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

The Tempest testcases are distributed across three
Tiers:

  * Smoke Tier - Test Case 'tempest_smoke'
  * Components Tier - Test case 'tempest_full'
  * Neutron Trunk Port - Test case 'neutron_trunk'
  * OpenStack interop testcases - Test case 'refstack_defcore'
  * Testing and verifying RBAC policy enforcement - Test case 'patrole'

NOTE: Test case 'tempest_smoke' executes a defined set of tempest smoke
tests. Test case 'tempest_full' executes all defined Tempest tests.

NOTE: The 'neutron_trunk' test set allows to connect a VM to multiple VLAN
separated networks using a single NIC. The feature neutron trunk ports have
been supported by Apex, Fuel and Compass, so the tempest testcases have been
integrated normally.

NOTE: Rally is also used to run Openstack Interop testcases `[9]`_, which focus
on testing interoperability between OpenStack clouds.

NOTE: Patrole is a tempest plugin for testing and verifying RBAC policy
enforcement. It runs Tempest-based API tests using specified RBAC roles, thus
allowing deployments to verify that only intended roles have access to those
APIs. Patrole currently offers testing for the following OpenStack services:
Nova, Neutron, Glance, Cinder and Keystone. Currently in functest, only neutron
and glance are tested.

The goal of the Tempest test suite is to check the basic functionalities of the
different OpenStack components on an OPNFV fresh installation, using the
corresponding REST API interfaces.


Rally bench test suites
^^^^^^^^^^^^^^^^^^^^^^^

Rally `[3]`_ is a benchmarking tool that answers the question:

*How does OpenStack work at scale?*

The goal of this test suite is to benchmark all the different OpenStack modules
and get significant figures that could help to define Telco Cloud KPIs.

The OPNFV Rally scenarios are based on the collection of the actual Rally
scenarios:

 * authenticate
 * cinder
 * glance
 * heat
 * keystone
 * neutron
 * nova
 * quotas

A basic SLA (stop test on errors) has been implemented.

The Rally testcases are distributed across two Tiers:

  * Smoke Tier - Test Case 'rally_sanity'
  * Components Tier - Test case 'rally_full'

NOTE: Test case 'rally_sanity' executes a limited number of Rally smoke test
cases. Test case 'rally_full' executes the full defined set of Rally tests.


snaps_smoke
------------

This test case contains tests that setup and destroy environments with VMs with
and without Floating IPs with a newly created user and project. Set the config
value snaps.use_floating_ips (True|False) to toggle this functionality.
Please note that When the configuration value of snaps.use_keystone is True,
Functest must have access the cloud's private network.
This suite consists in 120 tests (test duration ~= 50 minutes)

The flavors for the SNAPS test cases are able to be configured giving new
metadata values as well as new values for the basic elements of flavor (i.e.
ram, vcpu, disk, ephemeral, swap etc). The snaps.flavor_extra_specs dict in
the config_functest.yaml file could be used for this purpose.

SDN Controllers
---------------

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
   * Create a new network via OpenStack and check the HTTP status code returned
     by Neutron
   * Check that the network has also been successfully created in OpenDaylight

 * Neutron Subnet test cases

   * Check OpenStack subnets
   * Check OpenDaylight subnets
   * Create a new subnet via OpenStack and check the HTTP status code returned
     by Neutron
   * Check that the subnet has also been successfully created in OpenDaylight

 * Neutron Port test cases

   * Check OpenStack Neutron for known ports
   * Check OpenDaylight ports
   * Create a new port via OpenStack and check the HTTP status code returned by
     Neutron
   * Check that the new port has also been successfully created in OpenDaylight

 * Delete operations

   * Delete the port previously created via OpenStack
   * Check that the port has been also successfully deleted in OpenDaylight
   * Delete previously subnet created via OpenStack
   * Check that the subnet has also been successfully deleted in OpenDaylight
   * Delete the network created via OpenStack
   * Check that the network has also been successfully deleted in OpenDaylight

Note: the checks in OpenDaylight are based on the returned HTTP status
code returned by OpenDaylight.


Features
--------

Functest has been supporting several feature projects since Brahmaputra:


+-----------------+---------+----------+--------+-----------+-----------+
| Test            | Brahma  | Colorado | Danube | Euphrates |  Fraser   |
+=================+=========+==========+========+===========+===========+
| barometer       |         |          |    X   |     X     |     X     |
+-----------------+---------+----------+--------+-----------+-----------+
| bgpvpn          |         |    X     |    X   |     X     |     X     |
+-----------------+---------+----------+--------+-----------+-----------+
| copper          |         |    X     |        |           |           |
+-----------------+---------+----------+--------+-----------+-----------+
| doctor          |    X    |    X     |    X   |     X     |     X     |
+-----------------+---------+----------+--------+-----------+-----------+
| domino          |         |    X     |    X   |     X     |           |
+-----------------+---------+----------+--------+-----------+-----------+
| fds             |         |          |    X   |     X     |     X     |
+-----------------+---------+----------+--------+-----------+-----------+
| moon            |         |    X     |        |           |           |
+-----------------+---------+----------+--------+-----------+-----------+
| multisite       |         |    X     |    X   |           |           |
+-----------------+---------+----------+--------+-----------+-----------+
| netready        |         |          |    X   |           |           |
+-----------------+---------+----------+--------+-----------+-----------+
| odl_sfc         |         |    X     |    X   |     X     |     X     |
+-----------------+---------+----------+--------+-----------+-----------+
| opera           |         |          |    X   |           |           |
+-----------------+---------+----------+--------+-----------+-----------+
| orchestra       |         |          |    X   |     X     |     X     |
+-----------------+---------+----------+--------+-----------+-----------+
| parser          |         |          |    X   |     X     |     X     |
+-----------------+---------+----------+--------+-----------+-----------+
| promise         |    X    |    X     |    X   |     X     |     X     |
+-----------------+---------+----------+--------+-----------+-----------+
| security_scan   |         |    X     |    X   |           |           |
+-----------------+---------+----------+--------+-----------+-----------+
| clover          |         |          |        |           |     X     |
+-----------------+---------+----------+--------+-----------+-----------+
| stor4nfv        |         |          |        |           |     X     |
+-----------------+---------+----------+--------+-----------+-----------+

Please refer to the dedicated feature user guides for details.


VNF
---


cloudify_ims
^^^^^^^^^^^^
The IP Multimedia Subsystem or IP Multimedia Core Network Subsystem (IMS) is an
architectural framework for delivering IP multimedia services.

vIMS has been integrated in Functest to demonstrate the capability to deploy a
relatively complex NFV scenario on the OPNFV platform. The deployment of a
complete functional VNF allows the test of most of the essential functions
needed for a NFV platform.

The goal of this test suite consists of:

 * deploy a VNF orchestrator (Cloudify)
 * deploy a Clearwater vIMS (IP Multimedia Subsystem) VNF from this
   orchestrator based on a TOSCA blueprint defined in `[5]`_
 * run suite of signaling tests on top of this VNF

The Clearwater architecture is described as follows:

.. figure:: ../../../images/clearwater-architecture-v2.png
   :align: center
   :alt: vIMS architecture


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

juju_epc
^^^^^^^^
The Evolved Packet Core (EPC) is the main component of the System Architecture
Evolution (SAE) which forms the core of the 3GPP LTE specification.

vEPC has been integrated in Functest to demonstrate the capability to deploy a
complex mobility-specific NFV scenario on the OPNFV platform. The OAI EPC
supports most of the essential functions defined by the 3GPP Technical Specs;
hence the successful execution of functional tests on the OAI EPC provides a
good endorsement of the underlying NFV platform.

This integration also includes ABot, a Test Orchestration system that enables
test scenarios to be defined in high-level DSL. ABot is also deployed as a
VM on the OPNFV platform; and this provides an example of the automation
driver and the Test VNF being both deployed as separate VNFs on the underlying
OPNFV platform.

The Workflow is as follows:
 * Deploy Orchestrator
    Deploy Juju controller using Bootstrap command.
 * Deploy VNF
    Deploy ABot orchestrator and OAI EPC as Juju charms.
    Configuration of ABot and OAI EPC components is handled through
    built-in Juju relations.
 * Test VNF
    Execution of ABot feature files triggered by Juju actions.
    This executes a suite of LTE signalling tests on the OAI EPC.
 * Reporting
    ABot test results are parsed accordingly and pushed to Functest Db.

Details of the ABot test orchestration tool may be found in `[15]`_

Kubernetes (K8s)
----------------

Kubernetes testing relies on sets of tests, which are part of the  Kubernetes
source tree, such as the Kubernetes End-to-End (e2e) tests `[16]`_.

The kubernetes testcases are distributed across various Tiers:

 * Healthcheck Tier

   * k8s_smoke Test Case: Creates a Guestbook application that contains redis
     server, 2 instances of redis slave, frontend application, frontend service
     and redis master service and redis slave service. Using frontend service,
     the test will write an entry into the guestbook application which will
     store the entry into the backend redis database. Application flow MUST
     work as expected and the data written MUST be available to read.

 * Smoke Tier

   * k8s_conformance Test Case: Runs a series of k8s e2e tests expected to
     pass on any Kubernetes cluster. It is a subset of tests necessary to
     demonstrate conformance grows with each release. Conformance is thus
     considered versioned, with backwards compatibility guarantees and are
     designed to be run with no cloud provider configured.


.. _`[2]`: http://docs.openstack.org/developer/tempest/overview.html
.. _`[3]`: https://rally.readthedocs.org/en/latest/index.html
.. _`[5]`: https://github.com/Orange-OpenSource/opnfv-cloudify-clearwater/blob/master/openstack-blueprint.yaml
.. _`[8]`: https://github.com/openstack/refstack-client
.. _`[9]`: https://github.com/openstack/defcore
.. _`[10]`: https://github.com/openstack/interop/blob/master/2016.08/procedure.rst
.. _`[11]`: http://robotframework.org/
.. _`[12]`: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/user/userguide/index.html
.. _`[13]`: https://wiki.opnfv.org/display/PROJ/SNAPS-OO
.. _`[14]`: https://github.com/oolorg/opnfv-functest-vrouter
.. _`[15]`: https://www.rebaca.com/abot-test-orchestration-tool/
.. _`[16]`: https://github.com/kubernetes/community/blob/master/contributors/devel/e2e-tests.md
