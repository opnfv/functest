Description of functest test cases
==================================

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
  |    VIM         | vPing_userdata | Ping using user data and cloud-init         |
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
  |                |                | The IP Multimedia Subsystem is a typical    |
  |                |                | Telco test case, referenced by ETSI.       |
  |                |                | It provides a fully functional VoIP System.|
  |                +----------------+--------------------------------------------+
  |                | Promise        | Resource reservation and management project|
  |                |                | to identify NFV related requirements and   |
  |                |                | realise resource reservation for future    |
  |                |                | usage by capacity management of resource   |
  |                |                | pools regarding compute, network and       |
  |                |                | storage.                                   |
  |                +----------------+--------------------------------------------+
  |                | SDNVPN         |                                            |
  +----------------+----------------+--------------------------------------------+


Most of the test suites are developed upstream.
For example, `Tempest <http://docs.openstack.org/developer/tempest/overview.html>`_ is the
OpenStack integration test suite.
Functest is in charge of the integration of different functional test suites.

The Tempest suite has been customised but no new test cases have been created.
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

  * 3 controllers (Opendaylight, ONOS, OpenContrail)
  * 4 installers (Apex, Compass, Fuel, Joid)

However most of the tests shall be runnable on any configuration.

