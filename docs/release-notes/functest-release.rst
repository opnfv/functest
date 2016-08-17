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
 * Rally full parallel
 * vIMS

The OPNFV projects integrated into Functest framework for automation are:

 * bgpvpn
 * Copper
 * Doctor
 * Parser
 * Domino
 * Moon
 * Multisite
 * ONOSFW
 * ONOS-sfc
 * ODL-sfc
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

 - support new scenarios

New features
------------

 - minor bug fixes (formating)

 - Modification of the configuration to support vPing_userdata on ONOS scenario

 - Use serial option in Tempest to improve success rate

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

The success criteria have been defined as follows:

 * vPing SSH 100% OK
 * vPing userdata 100% OK
 * Tempest smoke serial success rate 100%
 * Rally sanity success rate 100%
 * ODL success rate = 100%
 * ONOS success rate = 100%
 * Feature project success rate = 100%

The reporting pages can be found at:

 * apex: * TODO / check branch *
 * compass: * TODO / check branch *
 * fuel: * TODO / check branch *
 * joid: * TODO / check branch *

Colorado limitations
-----------------------

- vPing userdata and Tempest cases related to metada service excluded
from onos scenarios https://gerrit.opnfv.org/gerrit/#/c/18729/

- Tempest cases related to storage for joid scenarios https://gerrit.opnfv.org/gerrit/#/c/17871/

- vPing_ssh and vIMS excluded from bgpvpn and kvm scenario


See known issues section for details


Test and installer/scenario dependencies
========================================

It is not always possible to run all the test cases on all the scenarios. The
following table details the dependencies of the test cases per scenario.
The scenario dependencies (installer or scenario) are detailed in https://git.opnfv.org/cgit/functest/tree/ci/testcases.yaml

Test results
============

Test results are available in:

 - test results document: http://artifacts.opnfv.org/functest

 - jenkins logs on CI: https://build.opnfv.org/ci/view/functest/


Known issues
------------


Open JIRA tickets
=================

+------------------+-----------------------------------------+
|   JIRA           |         Description                     |
+==================+=========================================+
+------------------+-----------------------------------------+
+------------------+-----------------------------------------+
+------------------+-----------------------------------------+
+------------------+-----------------------------------------+
+------------------+-----------------------------------------+

Useful links
============

 - wiki project page: https://wiki.opnfv.org/opnfv_functional_testing

 - wiki Functest Colorado page: https://wiki.opnfv.org/display/functest/Functest+Colorado

 - Functest repo: https://git.opnfv.org/cgit/functest

 - Functest CI dashboard: https://build.opnfv.org/ci/view/functest/

 - JIRA dashboard: https://jira.opnfv.org/secure/Dashboard.jspa?selectPageId=10611

 - Functest IRC chan: #opnfv-functest

 - Functest reporting: http://testresults.opnfv.org/reporting
