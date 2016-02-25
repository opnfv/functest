===========================================
OPNFV Brahmaputra release note for Functest
===========================================

.. contents:: Table of Contents
   :backlinks: none

Abstract
========

This document describes the release note of Functest project.

License
=======

OPNFV Brahmaputra release note for Functest Docs
(c) by Morgan Richomme (Orange)

OPNFV Brahmaputra release note for onosfw Docs
are licensed under a Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this.
If not, see <http://creativecommons.org/licenses/by/4.0/>.

Version history
===============

+------------+----------+------------------+------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**            |
|            |          |                  |                        |
+------------+----------+------------------+------------------------+
| 2016-02-25 | 1.0.0    | Morgan Richomme  | Functest for B release |
|            |          | (Orange)         |                        |
+------------+----------+------------------+------------------------+

OPNFV Brahmaputra Release
=========================

Functest deals with functional testing of the OPNFV solution.
It includes test cases developed within the project and test cases developped in
other OPNFV projects.

The internal test cases are:

 * vPing ssh
 * vPing userdata
 * Tempest
 * Rally
 * vIMS
 * OLD

The OPNFV projects integrated into Functest framework for automation are:

 * Promise
 * Doctor
 * ONOSFW

Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | functest                             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/tag**                         | brahmaputra.1.0                      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | Brahmaputra base release             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | February 26 2016                     |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | Brahmaputra base release             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Deliverables
============

Software
--------

 - The Functest docker container

Documents
---------

 - Installation/configuration guide

 - User Guide

 - Developer Guide

 - Test results per scenario

Version change
==============

Feature evolution
-----------------

 - dockerization of Functest

 - renaming of vPing into vPing userdata

 - Tempest update, use custom list of test cases

 - Rally update, use global scenario

 - Update jenkins logs

 - support of the different scenario

New features
------------

 - introduction of a new vPing scenario vPing ssh

 - introduction of vIMS test case

 - support of Promise

 - support of Doctor

 - support of ONOSFW

 - scenario management system

 - creation of a Test collection API

 - creation of the Test dashboard: https://www.opnfv.org/opnfvtestgraphs/summary

 - creation of Functest dashboard: http://testresults.opnfv.org/dashboard/

Scenario Matrix
===============

For Brahmaputra, Functest was successul with the following scenarios:

+----------------+---------+---------+---------+---------+
|    Scenario    |  Apex   | Compass |  Fuel   |   Joid  |
+================+=========+=========+=========+=========+
|   odl_l2       |    X    |    X    |    X    |    X    |
+----------------+---------+---------+---------+---------+
|   onos         |         |    X    |         |         |
+----------------+---------+---------+---------+---------+
|   nosdn        |         |    X    |    X    |         |
+----------------+---------+---------+---------+---------+
|   ovs (dpdk)   |         |         |    X    |         |
+----------------+---------+---------+---------+---------+

The success criteria was considered as sucessful when we could have at least 4
consecutive succesful runs of the critical test suites in the Continuous
Integration.

The critical test cases were defined as follows:

 * vPing SSH 100% OK
 * vPing userdata 100% OK
 * Tempest success rate > 90%
 * Rally success rate > 90%
 * ODL success rate = 100%
 * ONOSFW success rate = 100%

Other scenarios are currently available but did not match success criteria for
the release but would be added in the incremental scenario update of the
release.

Complete status is provided in https://wiki.opnfv.org/functest_release_2

Brahmaputra restrictions
------------------------

- Fuel and Apex Tempest success rate was below 90% but above 80%. Some of the
error causes were identified (workers, lack of IP)

- vIMS failed in CI for joid/odl_l2 scenario

- vPing userdata and vIMS excluded from onos scenario

- No odl_l3 has been successful due to vPing ssh issue.

- joid/nosdn successful but the complete scenario (including yardstick) not run
4 times in a raw

- apex/nosdn never run (not a target scenario) but probably succesful (pure
OpenStack)

See known issues section for details

Test and installer/scenario dependencies
========================================

It is not always possible to run all the test cases on all the scenario. The
table hereafter details the dependencies of the test cases per scenario.

+----------------+-------------+-------------+-------------+-------------+
|  Test cases    |    Apex     |   Compass   |    Fuel     |     Joid    |
+================+=============+=============+=============+=============+
|   vPing SSH    | all         | all         | all         | all         |
+----------------+-------------+-------------+-------------+-------------+
| vPing userdata | all except  | all except  | all except  | all except  |
|                | ONOS        | ONOS        | ONOS        | ONOS        |
+----------------+-------------+-------------+-------------+-------------+
| Tempest        | all         | all         | all         | all         |
+----------------+-------------+-------------+-------------+-------------+
| Rally          | all         | all         | all         | all         |
+----------------+-------------+-------------+-------------+-------------+
| ODL            | all ODL     | all ODL     | all ODL     | all ODL     |
+----------------+-------------+-------------+-------------+-------------+
| ONOS           | ONOS        | ONOS        | ONOS        | ONOS        |
+----------------+-------------+-------------+-------------+-------------+
| Promise        | no          | no          | all         | all         |
+----------------+-------------+-------------+-------------+-------------+
| vIMS           | all except  | all except  | all except  | all except  |
|                | ONOS        | ONOS        | ONOS        | ONOS        |
+----------------+-------------+-------------+-------------+-------------+
| Doctor         | all         | no          | no          | no          |
+----------------+-------------+-------------+-------------+-------------+

Test results
============

Test results are available in:

 - test results document

 - jenkins logs on CI

 - Test dashboards

known issues
------------

 - metadata not supported in ONOS, which excludes vPing userdata and vIMS test
cases

 - Rally worker issues. A workaround has been implemented to run some Tempest
test cases sequentially to minimize the errors on workers. However this issue
may explain why some Tempest scenarios (especially on apex) do not trigger the
default 210 test cases as expected and lead to a success rate below the success
criteria. https://bugs.launchpad.net/testrepository/+bug/1538941

 - in this tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools 
case the problem is in tempest code which doesn't reserve big enough allocation
pool. https://bugs.launchpad.net/tempest/+bug/1514457

 - Lack of IP addresses available may lead to several errors in different test
cases

 - vIMS, the VM needs to have access to OpenStack API. If technical architecture
does not allow this access (for security reasons), the orchestrator will be
deployed but the VNF will not be deployed. That is the reason why it fails on
joid/odl_l2 scenario on Orange POD 2 in Continous Integration.

Open JIRA tickets
=================

+------------------+-----------------------------------------+
|   JIRA           |         Description                     |
+==================+=========================================+
| FUNCTEST-139     | prepare_env failed due to               |
|                  | https://pypi.python.org/samples is not  |
|                  | accessible                              |
+------------------+-----------------------------------------+
| FUNCTEST-137     | Tempest success rate below 90 on apex   |
+------------------+-----------------------------------------+
| FUNCTEST-136     | Tempest success rate below 90 on fuel   |
+------------------+-----------------------------------------+
| FUNCTEST-135     | vPing scenario failed in odl_l3 scenario|
+------------------+-----------------------------------------+
| FUNCTEST-124     | odl test suite troubleshooting          |
+------------------+-----------------------------------------+

Useful links
============

 - wiki project page: https://wiki.opnfv.org/opnfv_functional_testing

 - Functest repo: https://git.opnfv.org/cgit/functest

 - Functest CI dashboard: https://build.opnfv.org/ci/view/functest/

 - JIRA dashboard: https://jira.opnfv.org/secure/Dashboard.jspa?selectPageId=10611

 - Wiki page for B Release: https://wiki.opnfv.org/functest_release_2

 - Functest IRC chan: #opnfv-testperf

 - Test dashboard: https://www.opnfv.org/opnfvtestgraphs/summary

 - Functest dashboard: http://testresults.opnfv.org/dashboard
