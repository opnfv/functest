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

OPNFV Brahmaputra release note for Functest Docs
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
It includes test cases developed within the project and test cases developed in
other OPNFV projects and other upstream communities.

The internal test cases are:

 * vPing ssh
 * vPing userdata
 * Tempest
 * Rally
 * vIMS
 * ODL

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

 - The Functest Docker image

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

 - support of the different scenarios

New features
------------

 - introduction of a new vPing test case vPing ssh

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

For Brahmaputra, Functest supports the following scenarios:

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

Functest defines the success criteria when having at least 4 consecutive
successful runs of a given scenario from the Continuous Integration.

The success criteria is defined as follows:

 * vPing SSH 100% OK
 * vPing userdata 100% OK
 * Tempest success rate > 90%
 * Rally success rate > 90%
 * ODL success rate = 100%
 * ONOSFW success rate = 100%
 * Promise success rate = 100%
 * vIMS: deployement of the orchestrator and the vIMS VNF successful

Other scenarios are currently available but did not meet success criteria for
the release but might be added in the incremental scenario update of the
release.

Brahmaputra limitations
-----------------------

- Fuel and Apex Tempest success rate was below 90% but above 80%. Some of the
error causes were identified (workers, lack of IP)

- vIMS failed in CI for joid/odl_l2 scenario

- vPing userdata and vIMS excluded from onos scenario

- None of the odl_l3 scenarios has been successful due to vPing ssh issue.

- joid/nosdn successful but the complete scenario not run 4 times in a raw

- apex/nosdn never run (not a target scenario) but probably succesful

See known issues section for details

Test and installer/scenario dependencies
========================================

It is not always possible to run all the test cases on all the scenarios. The
following table details the dependencies of the test cases per scenario.

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

 - test results document: http://artifacts.opnfv.org/functest/docs/results/index.html

 - jenkins logs on CI: https://build.opnfv.org/ci/view/functest/

 - Test dashboards: http://testresults.opnfv.org/dashboard

Known issues
------------

 - nova metadata service not supported in ONOS:

    - it excludes vPing userdata and vIMS test cases

 - Rally worker issues: 

    - A workaround has been implemented to run Tempest test cases sequentially
   
    - It may explain why Tempest scenarios (mainly on apex) do not run the 210 tests
   
    - https://bugs.launchpad.net/testrepository/+bug/1538941

 - IPv6 issues in tempest suite:

    - tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools

    - Tempest code which doesn't reserve big enough allocation

    - https://bugs.launchpad.net/tempest/+bug/1514457

 - Lack of IP addresses available lead to several errors in different test cases

 - vIMS:

    - the VM needs to have access to OpenStack API. 

    - Technical architecture may not allow this access (for security reasons)

    - Orchestrator can be deployed but the vIMS VNF cannot

    - That is the reason why it fails on joid/odl_l2 scenario on Orange POD 2

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
