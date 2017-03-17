.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

Overview of the Functest suites
===============================

Functest is the OPNFV project primarily targeting function testing.
In the Continuous Integration pipeline, it is launched after an OPNFV fresh
installation to validate and verify the basic functions of the
infrastructure.

The current list of test suites can be distributed over 5 main domains: VIM
(Virtualised Infrastructure Manager), Controllers (i.e. SDN Controllers),
Features, VNF (Virtual Network Functions) and MANO stacks.

Functest test suites are also distributed in the OPNFV testing categories:
healthcheck, smoke, features, components, performance, VNF, Stress tests.

All the Healthcheck and smoke tests of a given scenario must be succesful to
validate the scenario for the release.

+-------------+---------------+----------------+----------------------------------+
| Domain      | Tier          | Test case      | Comments                         |
+=============+===============+================+==================================+
| VIM         | healthcheck   | connection     | Check OpenStack connectivity     |
|             |               | _check         | through SNAPS framework          |
|             |               +----------------+----------------------------------+
|             |               | api_check      | Check OpenStack API through      |
|             |               |                | SNAPS framework                  |
|             |               +----------------+----------------------------------+
|             |               | snaps_health   |  basic instance creation, check  |
|             |               | \_check        |  DHCP                            |
|             +---------------+----------------+----------------------------------+
|             | smoke         | vping_ssh      | NFV "Hello World" using an SSH   |
|             |               |                | connection to a destination VM   |
|             |               |                | over a created floating IP       |
|             |               |                | address on the SUT Public /      |
|             |               |                | External network. Using the SSH  |
|             |               |                | connection a test script is then |
|             |               |                | copied to the destination        |
|             |               |                | VM and then executed via SSH.    |
|             |               |                | The script will ping another     |
|             |               |                | VM on a specified IP address over|
|             |               |                | the SUT Private Tenant network.  |
|             |               +----------------+----------------------------------+
|             |               | vping_userdata | Uses Ping with given userdata    |
|             |               |                | to test intra-VM connectivity    |
|             |               |                | over the SUT Private Tenant      |
|             |               |                | network. The correct operation   |
|             |               |                | of the NOVA Metadata service is  |
|             |               |                | also verified in this test.      |
|             |               +----------------+----------------------------------+
|             |               | tempest_smoke  | Generate and run a relevant      |
|             |               | \_serial       | Tempest Test Suite in smoke mode.|
|             |               |                | The generated test set is        |
|             |               |                | dependent on the OpenStack       |
|             |               |                | deployment environment.          |
|             |               +----------------+----------------------------------+
|             |               | rally_sanity   | Run a subset of the OpenStack    |
|             |               |                | Rally Test Suite in smoke mode   |
|             |               +----------------+----------------------------------+
|             |               | snaps_smoke    | Run a subset of the OpenStack    |
|             |               |                | Rally Test Suite in smoke mode   |
|             |               +----------------+----------------------------------+
|             |               | refstack       | Reference RefStack suite         |
|             |               |   \_defcore    | tempest selection for NFV        |
|             +---------------+----------------+----------------------------------+
|             | components    | tempest_full   | Generate and run a full set of   |
|             |               | \_parallel     | the OpenStack Tempest Test Suite.|
|             |               |                | See the OpenStack reference test |
|             |               |                | suite `[2]`_. The generated      |
|             |               |                | test set is dependent on the     |
|             |               |                | OpenStack deployment environment.|
|             |               +----------------+----------------------------------+
|             |               | rally_full     | Run the OpenStack testing tool   |
|             |               |                | benchmarking OpenStack modules   |
|             |               |                | See the Rally documents `[3]`_.  |
|             |               +----------------+----------------------------------+
|             |               | tempest_custom | Allow to run a customized list   |
|             |               |                | of Tempest cases                 |
+-------------+---------------+----------------+----------------------------------+
| Controllers | smoke         | odl            | Opendaylight Test suite          |
|             |               |                | Limited test suite to check the  |
|             |               |                | basic neutron (Layer 2)          |
|             |               |                | operations mainly based on       |
|             |               |                | upstream testcases. See below    |
|             |               |                | for details                      |
|             |               +----------------+----------------------------------+
|             |               | onos           | Test suite of ONOS L2 and L3     |
|             |               |                | functions.                       |
|             |               |                | See `ONOSFW User Guide`_  for    |
|             |               |                | details.                         |
|             |               +----------------+----------------------------------+
|             |               | odl_netvirt    | Test Suite for the OpenDaylight  |
|             |               |                | SDN Controller when the NetVirt  |
|             |               |                | features are installed. It       |
|             |               |                | integrates some test suites from |
|             |               |                | upstream using Robot as the test |
|             |               |                | framework                        |
|             |               +----------------+----------------------------------+
|             |               | fds            | Test Suite for the OpenDaylight  |
|             |               |                | SDN Controller when the GBP      |
|             |               |                | features are installed. It       |
|             |               |                | integrates some test suites from |
|             |               |                | upstream using Robot as the test |
|             |               |                | framework                        |
+-------------+---------------+----------------+----------------------------------+
| Features    | features      | bgpvpn         | Implementation of the OpenStack  |
|             |               |                | bgpvpn API from the SDNVPN       |
|             |               |                | feature project. It allows for   |
|             |               |                | the creation of BGP VPNs.        |
|             |               |                | See `SDNVPN User Guide`_ for     |
|             |               |                | details                          |
|             |               +----------------+----------------------------------+
|             |               | doctor         | Doctor platform, as of Colorado  |
|             |               |                | release, provides the three      |
|             |               |                | features:                        |
|             |               |                | * Immediate Notification         |
|             |               |                | * Consistent resource state      |
|             |               |                | awareness for compute host down  |
|             |               |                | * Valid compute host status      |
|             |               |                | given to VM owner                |
|             |               |                | See `Doctor User Guide`_ for     |
|             |               |                | details                          |
|             |               +----------------+----------------------------------+
|             |               | domino         | Domino provides TOSCA template   |
|             |               |                | distribution service for network |
|             |               |                | service and VNF descriptors      |
|             |               |                | among MANO components e.g.,      |
|             |               |                | NFVO, VNFM, VIM, SDN-C, etc.,    |
|             |               |                | as well as OSS/BSS functions.    |
|             |               |                | See `Domino User Guide`_ for     |
|             |               |                | details                          |
|             |               +----------------+----------------------------------+
|             |               | multisites     | Multisites                       |
|             |               |                | See `Multisite User Guide`_ for  |
|             |               |                | details                          |
|             |               +----------------+----------------------------------+
|             |               | netready       | Testing from netready project    |
|             |               |                | ping using gluon                 |
|             |               +----------------+----------------------------------+
|             |               | odl-sfc        | SFC testing for odl scenarios    |
|             |               |                | See `SFC User Guide`_ for details|
|             |               +----------------+----------------------------------+
|             |               | parser         | Parser is an integration project |
|             |               |                | which aims to provide            |
|             |               |                | placement/deployment templates   |
|             |               |                | translation for OPNFV platform,  |
|             |               |                | including TOSCA -> HOT, POLICY ->|
|             |               |                | TOSCA and YANG -> TOSCA. it      |
|             |               |                | deals with a fake vRNC.          |
|             |               |                | See `Parser User Guide`_ for     |
|             |               |                | details                          |
|             |               +----------------+----------------------------------+
|             |               | promise        | Resource reservation and         |
|             |               |                | management project to identify   |
|             |               |                | NFV related requirements and     |
|             |               |                | realize resource reservation for |
|             |               |                | future usage by capacity         |
|             |               |                | management of resource pools     |
|             |               |                | regarding compute, network and   |
|             |               |                | storage.                         |
|             |               |                | See `Promise User Guide`_ for    |
|             |               |                | details.                         |
|             |               +----------------+----------------------------------+
|             |               | security_scan  | Implementation of a simple       |
|             |               |                | security scan. (Currently        |
|             |               |                | available only for the Apex      |
|             |               |                | installer environment)           |
+-------------+---------------+----------------+----------------------------------+
| VNF         | vnf           | cloudify_ims   | Example of a real VNF deployment |
|             |               |                | to show the NFV capabilities of  |
|             |               |                | the platform. The IP Multimedia  |
|             |               |                | Subsytem is a typical Telco test |
|             |               |                | case, referenced by ETSI.        |
|             |               |                | It provides a fully functional   |
|             |               |                | VoIP System                      |
|             |               +----------------+----------------------------------+
|             |               | orchestra_ims  | OpenIMS deployment using         |
|             |               |                | Openbaton orchestrator           |
|             |               +----------------+----------------------------------+
|             |               | vyos_vrouter   | vRouter testing                  |
+-------------+---------------+----------------+----------------------------------+


As shown in the above table, Functest is structured into different 'domains',
'tiers' and 'test cases'. Each 'test case' usually represents an actual
'Test Suite' comprised -in turn- of several test cases internally.

Test cases also have an implicit execution order. For example, if the early
'healthcheck' Tier testcase fails, or if there are any failures in the 'smoke'
Tier testcases, there is little point to launch a full testcase execution round.

In Danube, we merged smoke and sdn controller tiers in smoke tier.

An overview of the Functest Structural Concept is depicted graphically below:

.. figure:: ../images/concepts_mapping_final.png
   :align: center
   :alt: Functest Concepts Structure

Some of the test cases are developed by Functest team members, whereas others
are integrated from upstream communities or other OPNFV projects. For example,
`Tempest <http://docs.openstack.org/developer/tempest/overview.html>`_ is the
OpenStack integration test suite and Functest is in charge of the selection,
integration and automation of those tests that fit suitably to OPNFV.

The Tempest test suite is the default OpenStack smoke test suite but no new test
cases have been created in OPNFV Functest.

The results produced by the tests run from CI are pushed and collected into a
NoSQL database. The goal is to populate the database with results from different
sources and scenarios and to show them on a `Functest Dashboard`_. A screenshot
of a live Functest Dashboard is shown below:

.. figure:: ../images/FunctestDashboardDanube.png
   :align: center
   :alt: Functest Dashboard


Basic components (VIM, SDN controllers) are tested through their own suites.
Feature projects also provide their own test suites with different ways of
running their tests.

The notion of domain has been introduced in the description of the test cases
stored in the Database.
This parameters as well as possible tags can be used for the Test case catalog.

vIMS test case was integrated to demonstrate the capability to deploy a
relatively complex NFV scenario on top of the OPNFV infrastructure.

Functest considers OPNFV as a black box. As of Danube release the OPNFV
offers a lot of potential combinations:

  * 3 controllers (OpenDaylight, ONOS, OpenContrail)
  * 4 installers (Apex, Compass, Fuel, Joid)

Most of the tests are runnable by any combination, but some tests might have
restrictions imposed by the utilized installers or due to the available
deployed features. The system uses the environment variables (INSTALLER_IP and
DEPLOY_SCENARIO) to automatically determine the valid test cases, for each given
environment.

A convenience Functest CLI utility is also available to simplify setting up the
Functest evironment, management of the OpenStack environment (e.g. resource
clean-up) and for executing tests.
The Functest CLI organised the testcase into logical Tiers, which contain in
turn one or more testcases. The CLI allows execution of a single specified
testcase, all test cases in a specified Tier, or the special case of execution
of **ALL** testcases. The Functest CLI is introduced in more detail in the
section `Executing the functest suites`_ of this document.

.. _`[2]`: http://docs.openstack.org/developer/tempest/overview.html
.. _`[3]`: https://rally.readthedocs.org/en/latest/index.html
.. _`Copper User Guide`: http://artifacts.opnfv.org/copper/colorado/docs/userguide/index.html
.. _`Doctor User Guide`: http://artifacts.opnfv.org/doctor/colorado/userguide/index.html
.. _`Promise User Guide`: http://artifacts.opnfv.org/promise/colorado/docs/userguide/index.html
.. _`ONOSFW User Guide`: http://artifacts.opnfv.org/onosfw/colorado/userguide/index.html
.. _`SDNVPN User Guide`: http://artifacts.opnfv.org/sdnvpn/colorado/docs/userguide/index.html
.. _`Domino User Guide`: http://artifacts.opnfv.org/domino/docs/userguide-single/index.html
.. _`Parser User Guide`: http://artifacts.opnfv.org/parser/colorado/docs/userguide/index.html
.. _`Functest Dashboard`: http://testresults.opnfv.org/kibana_dashboards/
.. _`SFC User Guide`: http://artifacts.opnfv.org/sfc/colorado/userguide/index.html
.. _`Multisite User Guide`: http://artifacts.opnfv.org/multisite/docs/userguide/index.html
