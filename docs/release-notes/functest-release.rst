==============================================
OPNFV Brahmaputra3.0 release note for Functest
==============================================

Abstract
========

This document describes the release note of Functest project.

License
=======

OPNFV Colorado release note for Functest Docs
(c) by Morgan Richomme (Orange)

OPNFV Colorado release note for Functest Docs
are licensed under a Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this.
If not, see <http://creativecommons.org/licenses/by/4.0/>.

Version history
===============

+------------+----------+------------------+------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**            |
|            |          |                  |                        |
+------------+----------+------------------+------------------------+
| 2016-08-17 | 1.0.0    | Morgan Richomme  | Functest for C release |
|            |          | (Orange)         |                        |
+------------+----------+------------------+------------------------+

OPNFV Colorado Release
=========================

Functest deals with functional testing of the OPNFV solution.
It includes test cases developed within the project and test cases developed in
other OPNFV projects and other upstream communities.

The internal test cases are:

 * healthcheck
 * vPing ssh
 * vPing userdata
 * Tempest Smoke Serial
 * Rally Sanity
 * ODL
 * Tempest full parallel
 * Rally full
 * vIMS

The OPNFV projects integrated into Functest framework for automation are:

 * bgpvpn
 * Copper
 * Doctor
 * Domino
 * Moon
 * Multisite
 * ONOSFW
 * ONOS-sfc
 * ODL-sfc
 * Parser
 * Promise
 * Security scan

The validation of a scenario requires a subset of these tests depending
on the installer and the scenario.

The 3 last internal test cases (tempest full parallel, Rally full and
vIMS) are not considered for scenario validation.

Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | functest                             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/tag**                         | colorado.1.0                         |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | Colorado base release                |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | September 22 2016                    |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | Colorado base release                |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Deliverables
============

Software
--------

 - The Functest Docker image: * TODO link *

 - The testapi Docker image: * TODO link *


Documents
---------

 - Installation/configuration guide: * TODO link *

 - User Guide: * TODO link *

 - Developer Guide: * TODO link *


Version change
==============

Feature evolution
-----------------

 - refactoring of ODL functional tests (with upstream modifications)

 - refactoring of testapi (update, swagger documentation, dockerization)

 - jenkins logs improvement

 - update integration of Doctor, Promise and SDNVPN  projects

 - split Tempest and rally into 2 different tests: smoke and full

 - vIMS test suite integration

 - adoption of Kibana for dashboarding


New features
------------

 - Functest CLI to prepare and run the tests

 - creation of the healthcheck test case

 - support new scenarios (ocl, odl_l2-sfc, onos-sfc, lxd, moon, multisite)

 - integration of new OPNFV feature projects (copper, domino, multisite,
 moon, parser, onos-sfc, odl-sfc, security scan)

 - introduction of test tiers in functest framework

 - automatic reporting

 - introduction of a jenkins summary table

 - support of ARM architecture


Scenario Matrix
===============

For Colorado 1.0, Functest was tested on the following scenarios (if not
precised, the scenario is a na scenario):

+---------------------+---------+---------+---------+---------+
|    Scenario         |  Apex   | Compass |  Fuel   |   Joid  |
+=====================+=========+=========+=========+=========+
|   nosdn             |    X    |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   odl_l2            |    X    |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   odl_l3            |    X    |    X    |    X    |         |
+---------------------+---------+---------+---------+---------+
|   onos              |    X    |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   ocl               |         |    X    |         |         |
+---------------------+---------+---------+---------+---------+
|   ovs-noha (dpdk)   |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   kvm-noha          |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-bgpvpn     |    X    |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-sfc        |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   onos-sfc          |    X    |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   odl_l2-moon       |         |    X    |         |         |
+---------------------+---------+---------+---------+---------+
|   multisite         |         |         |         |         |
+---------------------+---------+---------+---------+---------+
|   lxd               |         |         |         |    X    |
+---------------------+---------+---------+---------+---------+

Functest defines a scenario scoring based on the sum of the unitary test
cases run in CI.
The scoring method is described in https://wiki.opnfv.org/pages/viewpage.action?pageId=6828617

In Colorado, the functional tests have been sliced in different
categories:

+----------------+-----------------------------------------------+
| Category       |  Description                                  |
+================+===============================================+
| healthcheck    | Basic OpenStack commands                      |
+----------------+-----------------------------------------------+
| smoke          | vPings, Tempest and rally smoke tests         |
+----------------+-----------------------------------------------+
| sdn_suites     | Specific SDN feature tests                    |
+----------------+-----------------------------------------------+
| features       | OPNFV feature project functional test suites  |
+----------------+-----------------------------------------------+
| openstack      | Advanced, long duration OpenStack tests       |
|                | (Tempest and Rally full suite). Each test may |
|                | last several hours                            |
+----------------+-----------------------------------------------+
| vnf            | Complex scenarios dealing with orchestration, |
|                | VNF deployment and tests (e.g. vIMS)          |
+----------------+-----------------------------------------------+

For the scenario validation, we consider only the categories healthcheck,
smoke, sdn_suites and features. These tests are run systematically in
the CI daily loops.

Success criteria have been defined for these test cases, they can be
PASS/FAIl or a success rate may be declared (100%, > 90%)
All the criteria, as well as the test dependencies are declared in the
ci/testcases.yaml file.

* TODO scoring table *

The reporting pages can be found at:

 * apex: http://testresults.opnfv.org/reporting/functest/release/colorado/index-status-apex.html
 * compass: http://testresults.opnfv.org/reporting/functest/release/colorado/index-status-compass.html
 * fuel: http://testresults.opnfv.org/reporting/functest/release/colorado/index-status-fuel.html
 * joid: http://testresults.opnfv.org/reporting/functest/release/colorado/index-status-joid.html

Colorado known issues
---------------------

- onos scenarios: vPing userdata and Tempest cases related to metadata
service excluded from onos scenarios https://gerrit.opnfv.org/gerrit/#/c/18729/

- joid scenarios: Tempest cases related to storage excluded
https://gerrit.opnfv.org/gerrit/#/c/17871/

- fuel scenarios: TestServerBasicOps test case skipped
https://gerrit.opnfv.org/gerrit/#/c/19635/

- bgpvpn and kvm scenarios: vPing_ssh and vIMS excluded (metadata
related scenarios)

- multisite: random errors running multisite. A known bug in keystone
mitaka, due to which memcache raises exception and keystone becomes
unresponsive(memcache error in keystone.log)
https://bugs.launchpad.net/keystone/+bug/1600394: workaround consists in
restarting memcache on server


Test and installer/scenario dependencies
========================================

It is not always possible to run all the test cases on all the scenarios.
The following table details the dependencies of the test cases per
scenario. The scenario dependencies (installer or scenario) are detailed
in https://git.opnfv.org/cgit/functest/tree/ci/testcases.yaml

Test results
============

Test results are available in:

 - test results document: http://artifacts.opnfv.org/functest

 - jenkins logs on CI: https://build.opnfv.org/ci/view/functest/



Open JIRA tickets
=================

+------------------+-----------------------------------------------+
|   JIRA           |         Description                           |
+==================+===============================================+
+------------------+-----------------------------------------------+
+------------------+-----------------------------------------------+
+------------------+-----------------------------------------------+
+------------------+-----------------------------------------------+
+------------------+-----------------------------------------------+

Useful links
============

 - wiki project page: https://wiki.opnfv.org/opnfv_functional_testing

 - wiki Functest Colorado page: https://wiki.opnfv.org/display/functest/Functest+Colorado

 - Functest repo: https://git.opnfv.org/cgit/functest

 - Functest CI dashboard: https://build.opnfv.org/ci/view/functest/

 - JIRA dashboard: https://jira.opnfv.org/secure/Dashboard.jspa?selectPageId=10611

 - Functest IRC chan: #opnfv-functest

 - Functest reporting: http://testresults.opnfv.org/reporting

 - Functest test configuration: https://git.opnfv.org/cgit/functest/tree/ci/testcases.yaml

 - Functest Colorado user guide: * TODO *

 - Functest installation/configuration guide: * TODO *

 - Functest developer guide: * TODO *


