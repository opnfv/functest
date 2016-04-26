==============================================
OPNFV Brahmaputra3.0 release note for Functest
==============================================

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
| 2016-04-27 | 3.0.0    | Morgan Richomme  | Add scenarios          |
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
 * bgpvpn

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

 - support new scenarios

New features
------------

 - minor bug fixes (formating)

 - Modification of the configuration to support vPing_userdata on ONOS scenario

 - Use serial option in Tempest to improve success rate

Scenario Matrix
===============

For Brahmaputra 3.0, Functest was succesfully tested on the following scenarios:

+----------------+---------+---------+---------+---------+
|    Scenario    |  Apex   | Compass |  Fuel   |   Joid  |
+================+=========+=========+=========+=========+
|   odl_l2       |    X    |    X    |    X    |    X    |
+----------------+---------+---------+---------+---------+
|   onos         |         |    X    |    X    |         |
+----------------+---------+---------+---------+---------+
|   nosdn        |         |    X    |    X    |         |
+----------------+---------+---------+---------+---------+
|   ovs (dpdk)   |         |         |    X    |         |
+----------------+---------+---------+---------+---------+
|   kvm          |         |         |    X    |         |
+----------------+---------+---------+---------+---------+
|   bgpvpn       |    X    |         |    X    |         |
+----------------+---------+---------+---------+---------+
|   sfc          |         |         |    X    |         |
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
 * Bgpvpn success rate = 100%
 * vIMS: deployement of the orchestrator and the vIMS VNF successful

Other scenarios are currently available but did not meet success criteria for
the release but might be added in the incremental scenario update of the
release.

Brahmaputra limitations
-----------------------

- Fuel and Apex Tempest success rate was below 90% but above 80% on some
scenarios. Some of the error causes were identified (workers, lack of IP)

- vIMS failed in CI for joid/odl_l2 scenario

- vPing userdata and vIMS excluded from onos scenario

- vPing_ssh and vIMS excluded from bgpvpn and kvm scenario

- None of the odl_l3 scenarios has been successful due to vPing ssh issue (ODL
bug reported https://bugs.opendaylight.org/show_bug.cgi?id=5582)

- apex/nosdn never run (not a target scenario) but probably succesful

- vPing SSH and vPing userdata no more run on CI since modification of bgpvpn
configuration regex.

See known issues section for details

Test and installer/scenario dependencies
========================================

It is not always possible to run all the test cases on all the scenarios. The
following table details the dependencies of the test cases per scenario.

+----------------+-------------+-------------+-------------+-------------+
|  Test cases    |    Apex     |   Compass   |    Fuel     |     Joid    |
+================+=============+=============+=============+=============+
| vPing SSH      | all         | all         | all         | all         |
+----------------+-------------+-------------+-------------+-------------+
| vPing userdata | all         | all         | all         | all         |
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
| Bgpvpn         | all         | no          | all         | no          |
+----------------+-------------+-------------+-------------+-------------+

Test results
============

Test results are available in:

 - test results document: http://artifacts.opnfv.org/functest/docs/results/index.html

 - jenkins logs on CI: https://build.opnfv.org/ci/view/functest/

 - Test dashboards: http://testresults.opnfv.org/dashboard

Known issues
------------

 - IPv6 issues in tempest suite:

    - tempest.api.network.test_ports.PortsIpV6TestJSON.test_create_port_in_allowed_allocation_pools

    - Tempest code which doesn't reserve big enough allocation

    - https://bugs.launchpad.net/tempest/+bug/1514457

 - Lack of IP addresses available lead to several errors in different test cases

 - vIMS (http://testresults.opnfv.org/reporting/vims/):

    - the VM needs to have access to OpenStack API.

    - Technical architecture may not allow this access (for security reasons)

    - Orchestrator can be deployed but the vIMS VNF cannot

    - That is the reason why it fails on joid/odl_l2 scenario on Orange POD 2

    - case needs to be consolidated on new scenaios (bgpvpn, sfc, ovs)

Open JIRA tickets
=================

+------------------+-----------------------------------------+
|   JIRA           |         Description                     |
+==================+=========================================+
| FUNCTEST-231     | vPing SSH no more run systematically    |
|                  | in CI                                   |
+------------------+-----------------------------------------+
| FUNCTEST-230     | Heat issues in Rally scenarios          |
+------------------+-----------------------------------------+
| FUNCTEST-229     | Extend reporting to brahmaputra         |
+------------------+-----------------------------------------+
| FUNCTEST-139     | prepare_env failed due to               |
|                  | https://pypi.python.org/samples is not  |
|                  | accessible                              |
+------------------+-----------------------------------------+
| FUNCTEST-135     | vPing scenario failed in odl_l3 scenario|
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
