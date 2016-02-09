Overview of the test suites
=============================

Functest is the OPNFV project targeting the functional testing.
In the Continuous Integration pipeline, it is launched after an OPNFV fresh
installation to validate and verify the basic functions of the infrastructure.

The current list of test suites can be distributed in 3 main domains::

 +----------------+----------------+-------------------------------------------+
 | Domain         | Test suite     | Comments                                  |
 +================+================+===========================================+
 |                | vPing          | NFV "Hello World" using SSH connection    |
 |                |                | and floatting IP                          |
 |                +----------------+-------------------------------------------+
 |    VIM         | vPing_userdata | Ping using userdata and cloud-init        |
 |                |                | mechanism                                 |
 |                +----------------+-------------------------------------------+
 |(Virtualised    | Tempest        | OpenStack reference test suite `[2]`_     |
 | Infrastructure +----------------+-------------------------------------------+
 | Manager)       | Rally bench    | OpenStack testing tool benchmarking       |
 |                |                | OpenStackmodules `[3]`_                   |
 +----------------+----------------+-------------------------------------------+
 |                | OpenDaylight   | Opendaylight Test suite                   |
 |                +----------------+-------------------------------------------+
 | Controllers    | ONOS           | Test suite for ONOS L2 and L3 functions   |
 |                +----------------+-------------------------------------------+
 |                | OpenContrail   |                                           |
 +----------------+----------------+-------------------------------------------+
 | Features       | vIMS           | Example of a real VNF deployment to show  |
 |                |                | the NFV capabilities of the platform.     |
 |                |                | The IP Multimedia Subsytem is a typical   |
 |                |                | Telco test case, referenced by ETSI.      |
 |                |                | It provides a fully functional VoIP System|
 |                +----------------+-------------------------------------------+
 |                | Promise        | Resource reservation and management       |
 |                |                | project to identify NFV related           |
 |                |                | requirements and realize resource         |
 |                |                | reservation for future usage by capacity  |
 |                |                | management of resource pools regarding    |
 |                |                | compute, network and storage.             |
 |                +----------------+-------------------------------------------+
 |                | SDNVPN         |                                           |
 +----------------+----------------+-------------------------------------------+

Functest includes different test suites which several test cases within. Some
of the tests are developed by Functest team members whereas others are integrated
from upstream communities or other OPNFV projects. For example,
`Tempest <http://docs.openstack.org/developer/tempest/overview.html>`_ is the
OpenStack integration test suite and Functest is in charge of the selection,
integration and automation of the tests that fit in OPNFV.

The Tempest suite has been customized but no new test cases have been created.
Some OPNFV feature projects (e.g. SDNVPN) have written some Tempest tests cases
and pushed upstream to be used by Functest.

The results produced by the tests run from CI are pushed and collected in a NoSQL
database. The goal is to populate the database with results from different sources
and scenarios and to show them on a Dashboard.

There is no real notion of Test domain or Test coverage. Basic components
(VIM, controllers) are tested through their own suites. Feature projects also
provide their own test suites with differnt ways of running their tests.

vIMS test case was integrated to demonstrate the capability to deploy a
relatively complex NFV scenario on top of the OPNFV infrastructure.

Functest considers OPNFV as a black box.
OPNFV, since the Brahmaputra release, offers lots of potential combinations:

  * 3 controllers (OpenDayligh, ONOS, OpenContrail)
  * 4 installers (Apex, Compass, Fuel, Joid)

Most of the tests are runnable on any combination, but some others might have
restrictions imposed by the installers or the available deployed features.
