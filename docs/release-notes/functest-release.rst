=======
License
=======

OPNFV Colorado release note for Functest Docs
(c) by Morgan Richomme (Orange)

OPNFV Colorado release note for Functest Docs
are licensed under a Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this.
If not, see <http://creativecommons.org/licenses/by/4.0/>.

===========================================
OPNFV Colorado1.0 release note for Functest
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

 - The Functest Docker image: https://hub.docker.com/r/opnfv/functest (tag: colorado.1.0)

 - The testapi Docker image: https://hub.docker.com/r/opnfv/testapi (tag:colorado.1.0)


Documents
---------

 - Installation/configuration guide: http://artifacts.opnfv.org/functest/colorado/docs/configguide/index.html

 - User Guide: http://artifacts.opnfv.org/functest/colorado/docs/userguide/index.html

 - Developer Guide: http://artifacts.opnfv.org/functest/colorado/docs/devguide/index.html


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

 - support new scenarios (ocl, odl_l2-sfc, onos-sfc, lxd, moon, fdio, multisite)

 - integration of new OPNFV feature projects (copper, domino, multisite,
 moon, parser, onos-sfc, odl-sfc, security scan)

 - introduction of test tiers in functest framework

 - automatic reporting

 - introduction of a jenkins summary table

 - support of ARM architecture


Scenario Matrix
===============

For Colorado 1.0, Functest was tested on the following scenarios (if not
precised, the scenario is a HA scenario):

+---------------------+---------+---------+---------+---------+
|    Scenario         |  Apex   | Compass |  Fuel   |   Joid  |
+=====================+=========+=========+=========+=========+
|   nosdn             |    X    |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   nosdn-noha        |         |         |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   kvm               |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   kvm-noha          |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   lxd               |         |         |         |    X    |
+---------------------+---------+---------+---------+---------+
|   lxd-noha          |         |         |         |    X    |
+---------------------+---------+---------+---------+---------+
|   ovs-noha (dpdk)   |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2            |    X    |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   odl_l2-noha       |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-bgpvpn     |    X    |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-bgpvpn-noha|         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-fdio-noha  |    X    |         |         |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-moon       |         |    X    |         |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-sfc-noha   |    X    |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l3            |    X    |    X    |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l3-noha       |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   onos              |         |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   onos-noha         |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   onos-sfc          |         |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   onos-sfc-noha     |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   multisite         |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+

For Colorado 2.0, the following scenarios have been re-released:

+---------------------+---------+---------+---------+---------+
|    Scenario         |  Apex   | Compass |  Fuel   |   Joid  |
+=====================+=========+=========+=========+=========+
|   onos              |    X    |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   odl_l2-sfc-ha     |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+


In Colorado, the functional tests have been sliced in 6 different
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

For the scenario validation, we consider only the healthcheck, smoke,
sdn_suites and features categories. These tests are run systematically
in the CI daily loops.

Success criteria have been defined for these test cases, they can be
PASS/FAIL or a success rate may be declared (100%, > 90%)
All the criteria, as well as the test dependencies are declared in the
ci/testcases.yaml file.

The scoring for the Colorado release per installer can be described as
follows.

The scoring is an indicator showing how many feature project test suites
have been integrated on the scenario.

The scoring equals the number of tests * succesful iteration of each
test [0-3]. The scoring method is described in https://wiki.opnfv.org/pages/viewpage.action?pageId=6828617

 e.g.
 apex/odl_l2-nofeature-ha
 tests = vping_ssh+vping_userdata+tempest+rally+odl+doctor+copper
 Scoring = 21/21 = 7 * 3

By default, if not specified, the scenarios are HA.
HA means OpenStack High Availability (main services). Note that not
all VIM (e.g. OpenStack) services are deployed in HA mode, as that
depends upon support of the specific service for HA deployment.
For example, in the Colorado release, the Congress service
is deployed in non-HA mode even for HA OPNFV scenarios, as explicit
support for HA operation has not yet been verified.
See the release notes of the installers for more details.


Apex
----

+------------------+---------+---------+-------------------+
|  Scenario        | Scoring | Success |    Results        |
|                  |         | rate    |                   |
+==================+=========+=========+===================+
| nosdn            |  17/18  |   95%   | `apex-res-174`_   |
+------------------+---------+---------+-------------------+
| odl_l2           |  21/21  |   100%  | `apex-res-175`_   |
+------------------+---------+---------+-------------------+
| odl_l3           |  15/18  |    83%  | `apex-res-176`_   |
+------------------+---------+---------+-------------------+
| odl_l2-bgpvpn    |  14/18  |    78%  | `apex-res-235`_   |
+------------------+---------+---------+-------------------+
| odl_l2-fdio-noha |  12/15  |    80%  | `apex-res-6`_     |
+------------------+---------+---------+-------------------+
| odl_l2-sfc-noha  |  18/24  |    75%  | `apex-res-217`_   |
+------------------+---------+---------+-------------------+
| onos-nofeature-ha|  20/21  |    95%  | `apex-res-423`_   |
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

Note: all the Compass tests for Colorado have been executed on virtual
environment. Bare metal resources were used for Master branch.


Fuel
----

+---------------------+---------+---------+-------------------+
|  Scenario           | Scoring | Success |  Results          |
|                     |         | rate    |                   |
+=====================+=========+=========+===================+
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

Results of Functest on AArch64 Colorado 1.0

+---------------------+---------+---------+----------------------+
|  Scenario           | Scoring | Success |  Results             |
|                     |         | rate    |                      |
+=====================+=========+=========+======================+
| nosdn               |  18/18  |  100%   | `fuel-arm-res-29`_   |
+---------------------+---------+---------+----------------------+
| odl_l2              |  21/21  |  100%   | `fuel-arm-res-24`_   |
+---------------------+---------+---------+----------------------+
| odl_l2-noha         |  17/18  |   94%   | `fuel-arm-res-30`_   |
+---------------------+---------+---------+----------------------+
| odl_l3              |  14/18  |   78%   | `fuel-arm-res-28`_   |
+---------------------+---------+---------+----------------------+


Joid
----

+---------------------+---------+---------+-----------------+
|  Scenario           | Scoring | Success |  Results        |
|                     |         | rate    |                 |
+=====================+=========+=========+=================+
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

 * apex: http://testresults.opnfv.org/reporting/functest/release/colorado/index-status-apex.html
 * compass: http://testresults.opnfv.org/reporting/functest/release/colorado/index-status-compass.html
 * fuel: http://testresults.opnfv.org/reporting/functest/release/colorado/index-status-fuel.html
 * joid: http://testresults.opnfv.org/reporting/functest/release/colorado/index-status-joid.html

Colorado known restrictions/issues
==================================

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
|           |           | Rally sanity in Colorado 2.0 with the        |
|           |           | adoption of ODL Boron release.               |
+-----------+-----------+----------------------------------------------+
| apex      | *-fdio    | Due to late integration, fdio decided to     |
|           |           | focus on mandatory tests and exclude feature |
|           |           | tests (copper, doctor, security_scan) from   |
|           |           | its scenarios                                |
+-----------+-----------+----------------------------------------------+
| compass   | moon      | First ODL test FAILS because ODL/Openstack   |
|           |           | federation done in moon is partial. Only     |
|           |           | MD-SAL is federated (not AD-SAL)             |
+-----------+-----------+----------------------------------------------+
| fuel      | any       | TestServerBasicOps test case skipped         |
|           |           | https://gerrit.opnfv.org/gerrit/#/c/19635/   |
+-----------+-----------+----------------------------------------------+
| fuel      | kvm       | vPing_ssh and vIMS excluded (metadata related|
|           |           | scenarios)                                   |
+-----------+-----------+----------------------------------------------+
| fuel      | multisite | random errors running multisite. A known bug |
|           |           | in keystone mitaka, due to which memcache    |
|           |           | raises exception and keystone becomes        |
|           |           | unresponsive                                 |
|           |           | bugs.launchpad.net/keystone/+bug/1600394     |
|           |           | workaround consists in restarting memcache on|
|           |           | server                                       |
+-----------+-----------+----------------------------------------------+
| joid      | any       | Tempest cases related to object storage      |
|           |           | excluded                                     |
|           |           | https://gerrit.opnfv.org/gerrit/#/c/17871/   |
+-----------+-----------+----------------------------------------------+
| joid      | domino    | Domino tests are skipped in CI. However the  |
|           |           | test case can be run by manually setting     |
|           |           | IS_IPandKEY_CONFIGURED=true after manually   |
|           |           | setting properly the IP addresses of the 3   |
|           |           | Controller nodes in the configuration file   |
|           |           | /repos/domino/tests/run_multinode.sh         |
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
| `FUNCTEST-446`_  |  Cleanup ODL-SFC output in Functest execution |
|                  |  Impact on odl_l2-sfc scenarios               |
+------------------+-----------------------------------------------+
| `FUNCTEST-454`_  |  Cleanup failures when using HA networks in   |
|                  |  Neutron                                      |
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

 - Functest Colorado user guide: http://artifacts.opnfv.org/functest/colorado/docs/userguide/index.html

 - Functest installation/configuration guide: http://artifacts.opnfv.org/functest/colorado/docs/configguide/index.html

 - Functest developer guide: http://artifacts.opnfv.org/functest/colorado/docs/devguide/index.html

.. _`FUNCTEST-446` : https://jira.opnfv.org/browse/FUNCTEST-446

.. _`FUNCTEST-454` : https://jira.opnfv.org/browse/FUNCTEST-454

.. _`apex-res-6` : http://testresults.opnfv.org/test/api/v1/results?build_tag=bd-push-daily-colorado-6

.. _`apex-res-174` : http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-apex-daily-colorado-daily-colorado-174

.. _`apex-res-175`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-apex-daily-colorado-daily-colorado-175

.. _`apex-res-176`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-apex-daily-colorado-daily-colorado-176

.. _`apex-res-217`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-apex-daily-colorado-daily-colorado-217

.. _`apex-res-235`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-apex-daily-colorado-daily-colorado-235

.. _`apex-res-423`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-apex-daily-colorado-daily-colorado-423

.. _`compass-res-55`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-virtual-daily-colorado-55

.. _`compass-res-59`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-virtual-daily-colorado-59

.. _`compass-res-73`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-virtual-daily-colorado-73

.. _`compass-res-76`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-virtual-daily-colorado-76

.. _`compass-res-77`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-virtual-daily-colorado-77

.. _`compass-res-567`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-virtual-daily-master-567

.. _`compass-res-285`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-virtual-daily-master-285

.. _`fuel-res-8`: https://build.opnfv.org/ci/view/functest/job/functest-fuel-virtual-suite-colorado/lastSuccessfulBuild/console

.. _`fuel-res-115`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-colorado-115

.. _`fuel-res-117`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-colorado-117

.. _`fuel-res-119`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-colorado-119

.. _`fuel-res-123`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-colorado-123

.. _`fuel-res-124`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-colorado-124

.. _`fuel-res-128`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-colorado-128

.. _`fuel-res-129`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-colorado-129

.. _`fuel-res-154`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-154

.. _`fuel-res-155`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-155

.. _`fuel-res-160`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-160

.. _`fuel-res-161`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-161

.. _`fuel-res-162`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-162

.. _`fuel-res-164`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-164

.. _`fuel-res-166`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-166

.. _`fuel-res-213`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-213

.. _`fuel-res-219`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-219

.. _`fuel-res-376`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-376

.. _`fuel-res-492`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-colorado-492

.. _`fuel-arm-res-29`: https://build.opnfv.org/ci/view/armband/job/functest-fuel-armband-baremetal-daily-colorado/29/console

.. _`fuel-arm-res-24`: https://build.opnfv.org/ci/view/armband/job/functest-fuel-armband-baremetal-daily-colorado/24/console

.. _`fuel-arm-res-30`: https://build.opnfv.org/ci/view/armband/job/functest-fuel-armband-baremetal-daily-colorado/30/console

.. _`fuel-arm-res-28`: https://build.opnfv.org/ci/view/armband/job/functest-fuel-armband-baremetal-daily-colorado/28/console

.. _`joid-res-93`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-colorado-93

.. _`joid-res-91`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-colorado-91

.. _`joid-res-99`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-colorado-99

.. _`joid-res-97`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-colorado-97

.. _`joid-res-102`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-colorado-102

.. _`joid-res-103`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-colorado-103

.. _`joid-res-104`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-colorado-104

.. _`joid-res-345`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-colorado-345

