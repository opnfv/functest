.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0

=======
License
=======

OPNFV Danube release note for Functest Docs
(c) by Jose Lausuch (Ericsson)

OPNFV Danube release note for Functest Docs
are licensed under a Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this.
If not, see <http://creativecommons.org/licenses/by/4.0/>.

===========================================
OPNFV Danube1.0 release note for Functest
===========================================

Abstract
========

This document describes the release note of Functest project.


Version history
===============

+------------+----------+------------------+------------------------+
| **Date**   | **Ver.** | **Author**       | **Comment**            |
|            |          |                  |                        |
+------------+----------+------------------+------------------------+
| 2016-08-17 | 1.0.0    | Morgan Richomme  | Functest for Colorado  |
|            |          | (Orange)         | release                |
+------------+----------+------------------+------------------------+
| 2017-03-29 | 4.0.0    | Jose Lausuch     | Functest for Danube    |
|            |          | (Ericsson)       | release                |
+------------+----------+------------------+------------------------+


OPNFV Danube Release
======================

Functest deals with functional testing of the OPNFV solution.
It includes test cases developed within the project and test cases developed in
other OPNFV projects and other upstream communities.

The internal test cases are:

 * connection_check
 * api_check
 * snaps_health_check
 * vping_ssh
 * vping_userdata
 * tempest_smoke_serial
 * refstack_defcore
 * snaps_smoke
 * rally_sanity
 * odl
 * tempest_full_parallel
 * rally_full
 * cloudify_ims

The OPNFV projects integrated into Functest framework for automation are:

 * barometer
 * bgpvpn
 * doctor
 * domino
 * fds
 * multisite
 * netready
 * onos
 * odl-sfc
 * odl-netvirt
 * parser
 * promise
 * security scan
 * orchestra_ims
 * vyos_vrouter

The validation of a scenario requires a subset of these tests depending
on the installer and the scenario.

The test cases from vnf (cloudify_ims, orchestra_ims, vyos_vrouter) and
component categories (tempest full parallel, Rally full) are not considered for
scenario validation.

Release Data
============

+--------------------------------------+--------------------------------------+
| **Project**                          | functest                             |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Repo/tag**                         | danube.1.0                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | Danube base release                  |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | Marcn 31st 2017                      |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | Danube base release                  |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Deliverables
============

Software
--------

 - The Functest Docker image: https://hub.docker.com/r/opnfv/functest (tag: danube.1.0)

 - The TestAPI Docker image: https://hub.docker.com/r/opnfv/testapi (tag:danube.1.0)


Documents
---------

 - Installation/configuration guide: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/user/configguide/index.html

 - User Guide: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/user/userguide/index.html

 - Developer Guide: http://docs.opnfv.org/en/latest/submodules/functest/docs/testing/developer/devguide/index.html


Version change
==============

Feature evolution
-----------------

- Adoption of SNAPS as middleware in 4 new test cases (connection_check, api_check,
   snaps_health_check and snaps_smoke)

- Introduction of refstack suite

- Support new odl suites (odl-netvirt, fds)

- Introduction of VNF onboarding capabilities

- Support of new feature projects (fds, netready, barometer, orchestra, vyos_vrouter)



Framework
---------

 - Harmonization of the naming, better adoption of OpenStack coding conventions

 - Enhanced code to be more Object Oriented, removed bash scripts

 - Introduction of abstraction classes to ease and harmonize the integration of
    test cases (internal or from feature projects)

 - New management of logger, env variables and configuration files

 - Creation of unit tests on the whole framework to ensure stability

 - Creation or ARM Functest docker


Test API
---------

- Automatic documentation (html & pdf)

- Full dockerization and automation of the deployment on testresults.opnfv.org

- Automation of test database backup on artifact


New internal tests cases
------------------------

- connection_check

- api_check

- snaps_health_check (replacing shell script healtcheck)

- refstack_defcore

- snaps_smoke

- vyos_vrouter


Scenario Matrix
===============

For Danube 1.0, Functest was tested on the following HA scenarios (new
dabube scenarios in bold):

+---------------------+---------+---------+---------+---------+
|    Scenario         |  Apex   | Compass |  Fuel   |   Joid  |
+=====================+=========+=========+=========+=========+
|   nosdn             |    X    |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
| **fdio**            |    X    |         |         |         |
+---------------------+---------+---------+---------+---------+
|   kvm               |    X    |         |    X    |         |
+---------------------+---------+---------+---------+---------+
| **kvm_ovs_dpdk**    |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
| **kvm_ovs_dpdk-bar**|         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   lxd               |         |         |         |    X    |
+---------------------+---------+---------+---------+---------+
| **ovs**             |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
| **openo**           |         |    X    |         |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2            |         |    X    |   X     |    X    |
+---------------------+---------+---------+---------+---------+
|   odl-bgpvpn        |   X     |         |         |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-bgpvpn     |         |         |   X     |         |
+---------------------+---------+---------+---------+---------+
| **odl_l2-fdio**     |    X    |         |         |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-sfc        |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l3            |    X    |    X    |    X    |         |
+---------------------+---------+---------+---------+---------+
| **ocl**             |         |   X     |         |         |
+---------------------+---------+---------+---------+---------+
|   onos              |         |   X     |         |         |
+---------------------+---------+---------+---------+---------+
|   multisite         |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+

Non HA scenarios:

+---------------------+---------+---------+---------+---------+
|    Scenario         |  Apex   | Compass |  Fuel   |   Joid  |
+=====================+=========+=========+=========+=========+
|   nosdn             |         |         |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   kvm               |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
| **kvm_ovs_dpdk**    |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
| **kvm_ovs_dpdk-bar**|         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   lxd               |         |         |         |    X    |
+---------------------+---------+---------+---------+---------+
|   ovs               |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2            |         |         |   X     |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-bgpvpn     |         |         |   X     |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-fdio       |    X    |         |         |         |
+---------------------+---------+---------+---------+---------+
| **odl_l3-fdio**     |    X    |         |         |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-sfc        |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l3            |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
| **odl_gluon**       |    X    |         |         |         |
+---------------------+---------+---------+---------+---------+

Colorado deprecated scenarios:

 * odl_l2-moon
 * onos-sfc
 * onos-noha
 * onos-sfc-noha

For the scenario validation, we consider only the healthcheck, smoke and
features categories. These tests are run systematically in the CI daily loops.

Success criterias have been defined for these test cases, they can be
PASS/FAIL or a success rate may be declared (100%, > 90%).
All the criteria, as well as the test dependencies are declared in the
testcases.yaml file located in the ci directory of the repository.

The scoring for the Danube release per installer can be described as
follows.

The scoring is an indicator showing how many feature project test suites
have been integrated in the scenario.

The scoring equals the number of tests * successful iteration of each
test [0-3]. The scoring method is described in https://wiki.opnfv.org/pages/viewpage.action?pageId=6828617

 e.g.
 apex/odl_l2-nofeature-ha
 tests = vping_ssh+vping_userdata+tempest+rally+odl+doctor+copper
 Scoring = 21/21 = 7 * 3

By default, if not specified, the scenarios are HA.
HA means OpenStack High Availability (main services). Note that not
all VIM (e.g. OpenStack) services are deployed in HA mode, as that
depends upon support of the specific service for HA deployment.
For example, in the Danube release, the Congress service
is deployed in non-HA mode even for HA OPNFV scenarios, as explicit
support for HA operation has not yet been verified.
See the release notes of the installers for more details.


Apex
----

+------------------+---------+---------+-------------------+
|  Scenario        | Scoring | Success |    Results        |
|                  |         | rate    |                   |
+==================+=========+=========+===================+
| nosdn            |  33/33  |   100%  | `apex-res-174`_   |
+------------------+---------+---------+-------------------+
| odl_l3           |  27/33  |    82%  | `apex-res-176`_   |
+------------------+---------+---------+-------------------+
| odl-bgpvpn       |  26/30  |    87%  | `apex-res-235`_   |
+------------------+---------+---------+-------------------+
| odl-gluon        |  30/36  |    83%  | `apex-res-235`_   |
+------------------+---------+---------+-------------------+
| kvm              |  32/33  |    97%  | `apex-res-6`_     |
+------------------+---------+---------+-------------------+
| odl_l2-fdio      |  28/36  |    78%  | `apex-res-6`_     |
+------------------+---------+---------+-------------------+
| odl_l2-fdio-noha |  30/36  |    83%  | `apex-res-6`_     |
+------------------+---------+---------+-------------------+
| odl_l3-fdio-noha |  26/30  |    87%  | `apex-res-6`_     |
+------------------+---------+---------+-------------------+
| fdio             |   6/30  |    20%  | `apex-res-6`_     |
+------------------+---------+---------+-------------------+

Compass
-------

+------------------+---------+---------+-------------------+
|  Scenario        | Scoring | Success |  Results          |
|                  |         | rate    |                   |
+==================+=========+=========+===================+
| nosdn            |  12/12  |   100%  | `compass-res-55`_ |
+------------------+---------+---------+-------------------+
| odl_l2           |  15/15  |   100%  | `compass-res-59`_ |
+------------------+---------+---------+-------------------+
| odl_l3           |  9/12   |    75%  | `compass-res-73`_ |
+------------------+---------+---------+-------------------+
| odl_l2-moon      |  15/18  |    83%  | `compass-res-567`_|
+------------------+---------+---------+-------------------+
| onos-ha          |  15/15  |   100%  | `compass-res-285`_|
+------------------+---------+---------+-------------------+
| onos-sfc-ha      |  17/18  |    95%  | `compass-res-76`_ |
+------------------+---------+---------+-------------------+

Note: all the Compass tests for Danube have been executed on virtual
environment. Bare metal resources were used for Master branch.


Fuel
----

+---------------------+---------+---------+-------------------+
|  Scenario           | Scoring | Success |  Results          |
|                     |         | rate    |                   |
+=====================+=========+=========+===================+
************* TODO *****************************************
| nosdn               |  18/18  |  100%   | `fuel-res-129`_   |
+---------------------+---------+---------+-------------------+
| nosdn-noha          |  15/15  |  100%   | `fuel-res-154`_   |
+---------------------+---------+---------+-------------------+
| nosdn-kvm           |  18/18  |  100%   | `fuel-res-128`_   |
+---------------------+---------+---------+-------------------+
| nosdn-kvm-noha      |  15/15  |  100%   | `fuel-res-161`_   |
+---------------------+---------+---------+-------------------+
| nosdn-ovs           |  12/18  |   67%*  |  `fuel-res-213`_  |
+---------------------+---------+---------+-------------------+
| nosdn-ovs-noha      |  15/15  |  100%   | `fuel-res-162`_   |
+---------------------+---------+---------+-------------------+
| odl_l2              |  21/21  |  100%   |  `fuel-res-123`_  |
+---------------------+---------+---------+-------------------+
| odl_l2-noha         |  17/18  |   94%   | `fuel-res-155`_   |
+---------------------+---------+---------+-------------------+
| odl_l2-bgpvpn       |  14/18  |   78%   | `fuel-res-119`_   |
+---------------------+---------+---------+-------------------+
| odl_l2-bgpvpn-noha  |  14/15  |   93%   | `fuel-res-160`_   |
+---------------------+---------+---------+-------------------+
| odl_l2-sfc-noha     |   6/21  |   29%   | `fuel-res-219`_   |
+---------------------+---------+---------+-------------------+
| odl_l2-sfc-ha       |  16/21  |   76%   | `fuel-res-376`_   |
+---------------------+---------+---------+-------------------+
| odl_l3              |  15/18  |   83%   | `fuel-res-115`_   |
+---------------------+---------+---------+-------------------+
| odl_l3-noha         |  12/15  |   80%   | `fuel-res-164`_   |
+---------------------+---------+---------+-------------------+
| onos                |  20/21  |   95%   | `fuel-res-492`_   |
+---------------------+---------+---------+-------------------+
| onos-noha           |  18/18  |  100%   | `fuel-res-166`_   |
+---------------------+---------+---------+-------------------+
| onos-sfc            |  24/24  |  100%   | `fuel-res-124`_   |
+---------------------+---------+---------+-------------------+
| onos-sfc-noha       |  21/21  |  100%   | `fuel-res-129`_   |
+---------------------+---------+---------+-------------------+
| multisite           |  N.R    |  100%   | `fuel-res-8`_     |
+---------------------+---------+---------+-------------------+

*: all results passed, lacking iterations to reach the full score

Results of Functest on AArch64 Danube 3.0

+---------------------+---------+---------+----------------------+
|  Scenario           | Scoring | Success |  Results             |
|                     |         | rate    |                      |
+=====================+=========+=========+======================+
************* TODO *****************************************
| nosdn               |  18/18  |  100%   | `fuel-arm-res-128`_  |
+---------------------+---------+---------+----------------------+
| odl_l2              |  21/21  |  100%   | `fuel-arm-res-122`_  |
+---------------------+---------+---------+----------------------+
| odl_l2-noha         |  18/18  |  100%   | `fuel-arm-res-129`_  |
+---------------------+---------+---------+----------------------+
| odl_l3              |  17/18  |   95%   | `fuel-arm-res-135`_  |
+---------------------+---------+---------+----------------------+


Joid
----

+---------------------+---------+---------+-----------------+
|  Scenario           | Scoring | Success |  Results        |
|                     |         | rate    |                 |
+=====================+=========+=========+=================+
************* TODO *****************************************
| nosdn               |  18/18  |  100%   | `joid-res-102`_ |
+---------------------+---------+---------+-----------------+
| nosdn-noha          |  17/18  |   95%   | `joid-res-93`_  |
+---------------------+---------+---------+-----------------+
| nosdn-lxd           |  12/12  |  100%   | `joid-res-104`_ |
+---------------------+---------+---------+-----------------+
| nosdn-lxd-noha      |  12/12  |  100%   | `joid-res-91`_  |
+---------------------+---------+---------+-----------------+
| odl_l2              |  21/21  |  100%   | `joid-res-103`_ |
+---------------------+---------+---------+-----------------+
| onos                |  21/21  |  100%   | `joid-res-345`_ |
+---------------------+---------+---------+-----------------+
| onos-sfc            |  24/24  |  100%   | `joid-res-97`_  |
+---------------------+---------+---------+-----------------+

It is highly recommended to install a json viewer in your browser
(e.g. https://addons.mozilla.org/fr/firefox/addon/jsonview/)

You can get additional details through test logs on http://artifacts.opnfv.org/.
As no search engine is available on the OPNFV artifact web site you must
retrieve the pod identifier on which the tests have been executed (see
field pod in any of the results) then click on the selected POD and look
for the date of the test you are interested in.

The reporting pages can be found at:

 * apex: http://testresults.opnfv.org/reporting/functest/release/danube/index-status-apex.html
 * compass: http://testresults.opnfv.org/reporting/functest/release/danube/index-status-compass.html
 * fuel: http://testresults.opnfv.org/reporting/functest/release/danube/index-status-fuel.html
 * joid: http://testresults.opnfv.org/reporting/functest/release/danube/index-status-joid.html

Danube known restrictions/issues
==================================

************* TODO *****************************************

+-----------+-----------+----------------------------------------------+
| Installer | Scenario  |  Issue                                       |
+===========+===========+==============================================+
| any       | odl_l3-*  | Tempest cases related to using floating IP   |
|           |           | addresses fail because of a known ODL bug.   |
|           |           | vPing_ssh test case is excluded for the same |
|           |           | reason.                                      |
|           |           | https://jira.opnfv.org/browse/APEX-112       |
|           |           | https://jira.opnfv.org/browse/FUNCTEST-445   |
+-----------+-----------+----------------------------------------------+
| apex/fuel | *-bgpvpn  | vPing_ssh (floating ips not supported) and   |
|           |           | vIMS excluded. Some Tempest cases related to |
|           |           | floating ips also excluded. Some performance |
|           |           | issues have been detected in this scenario   |
|           |           | (i.e. BGPVPN extension enabled) when running |
|           |           | commands against the OpenStack APIs, thus    |
|           |           | Rally sanity test case has been disabled.    |
|           |           | Performance issues seem to be connected to   |
|           |           | the ODL version. It is planned to reintroduce|
|           |           | Rally sanity in Danube 2.0 with the          |
|           |           | adoption of ODL Boron release.               |
+-----------+-----------+----------------------------------------------+
| fuel      | odl       | TestServerBasicOps test case skipped         |
|           |           | Tempest ssh client is hanging on opendaylight|
|           |           | enabled envs (getting deadlock in paramiko   |
|           |           | recv_exit_status method) while trying to     |
|           |           | execute a command on a vm.                   |
+-----------+-----------+----------------------------------------------+
| joid      | any       | Tempest cases related to object storage      |
|           |           | excluded                                     |
|           |           | https://gerrit.opnfv.org/gerrit/#/c/17871/   |
+-----------+-----------+----------------------------------------------+


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

 - jenkins logs on ARM CI: https://build.opnfv.org/ci/view/armband/



Open JIRA tickets
=================

+------------------+-----------------------------------------------+
|   JIRA           |         Description                           |
+==================+===============================================+
************* TODO *****************************************
|                  |                                               |
|                  |                                               |
+------------------+-----------------------------------------------+

Useful links
============

 - wiki project page: https://wiki.opnfv.org/opnfv_functional_testing

 - wiki Functest Danube page: https://wiki.opnfv.org/display/functest/Functest+Danube

 - Functest repo: https://git.opnfv.org/cgit/functest

 - Functest CI dashboard: https://build.opnfv.org/ci/view/functest/

 - JIRA dashboard: https://jira.opnfv.org/secure/Dashboard.jspa?selectPageId=10611

 - Functest IRC chan: #opnfv-functest

 - Reporting page: http://testresults.opnfv.org/reporting/danube.html

 - Functest test configuration: https://git.opnfv.org/cgit/functest/tree/functest/ci/testcases.yaml

