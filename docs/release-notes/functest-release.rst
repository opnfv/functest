===========================================
OPNFV Colorado1.0 release note for Functest
===========================================

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

 - The Functest Docker image: * TODO link *

 - The testapi Docker image: * TODO link *


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
|   odl_l2            |    X    |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   odl_l2-noha       |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l3            |    X    |    X    |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l3-noha       |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-bgpvpn     |    X    |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-bgpvpn-noha|         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-fdio-noha  |    X    |         |         |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-moon       |         |    X    |         |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-sfc        |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   odl_l2-sfc-noha   |    X    |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   onos              |         |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   onos-noha         |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   onos-sfc          |         |    X    |    X    |    X    |
+---------------------+---------+---------+---------+---------+
|   onos-sfc-noha     |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   ovs-noha (dpdk)   |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   kvm               |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   kvm-noha          |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   multisite         |         |         |    X    |         |
+---------------------+---------+---------+---------+---------+
|   lxd               |         |         |         |    X    |
+---------------------+---------+---------+---------+---------+
|   lxd-noha          |         |         |         |    X    |
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

By default, if not precised, the scenarios are HA.
HA means OpenStack High Availability (main services). For copper test,
the OpenStack congress module is not HA. See the release notes of the
installers for details.


apex
----

+------------------+---------+---------+---------------+
|  Scenario        | Scoring | Success |  build_tag id |
|                  |         | rate    |               |
+==================+=========+=========+===============+
| nosdn            |  17/18  |   95%   |    174        |
+------------------+---------+---------+---------------+
| odl_l2           |  21/21  |   100%  |    175        |
+------------------+---------+---------+---------------+
| odl_l3           |  15/18  |    83%  |    176        |
+------------------+---------+---------+---------------+
| odl_l2-bgpvpn    |  14/18  |   100%  |    160        |
+------------------+---------+---------+---------------+
| odl_l2-fdio-noha |  11/15  |      %  |     ??        |
+------------------+---------+---------+---------------+
| odl_l2-sfc-noha  |  18/21  |      %  |     ??        |
+------------------+---------+---------+---------------+

compass
-------

+------------------+---------+---------+---------------+
|  Scenario        | Scoring | Success |  build_tag id |
|                  |         | rate    |               |
+==================+=========+=========+===============+
| nosdn            |  12/12  |   100%  |     77        |
+------------------+---------+---------+---------------+
| odl_l2           |  15/15  |   100%  |    175        |
+------------------+---------+---------+---------------+
| odl_l3           |  9/12   |    75%  |     73        |
+------------------+---------+---------+---------------+
| odl_l2-moon      |  9/18   |      %  |    ??         |
+------------------+---------+---------+---------------+
| onos-ha          |  15/15  |   100%  |     72        |
+------------------+---------+---------+---------------+
| onos-sfc-ha      |  16/18  |   100%  |     67        |
+------------------+---------+---------+---------------+

Note: all the Compass tests for Colorado have been executed on virtual
environment. Bare metal resources were used for Master branch.


fuel
----

+---------------------+---------+---------+---------------+
|  Scenario           | Scoring | Success |  build_tag id |
|                     |         | rate    |               |
+=====================+=========+=========+===============+
| nosdn               |  18/18  |  100%   |     129       |
+---------------------+---------+---------+---------------+
| nosdn-noha          |  15/15  |  100%   |     154       |
+---------------------+---------+---------+---------------+
| nosdn-kvm           |  18/18  |  100%   |     128       |
+---------------------+---------+---------+---------------+
| nosdn-kvm-noha      |  15/15  |  100%   |     161       |
+---------------------+---------+---------+---------------+
| nosdn-ovs-noha      |  15/15  |  100%   |     162       |
+---------------------+---------+---------+---------------+
| odl_l2-sfc          |  21/21  |  100%   |               |
+---------------------+---------+---------+---------------+
| odl_l2-sfc-noha     | 16/18   |   88%   |               |
+---------------------+---------+---------+---------------+
| odl_l2              |  21/21  |  100%   |               |
+---------------------+---------+---------+---------------+
| odl_l2-noha         |  17/18  |   94%   |               |
+---------------------+---------+---------+---------------+
| odl_l2-bgpvpn       |  17/18  |   94%   |     119       |
+---------------------+---------+---------+---------------+
| odl_l2-bgpvpn-noha  |  15/15  |  100%   |     160       |
+---------------------+---------+---------+---------------+
| odl_l3              |  15/18  |   67%   |               |
+---------------------+---------+---------+---------------+
| odl_l3-noha         |  12/15  |   80%   |      117      |
+---------------------+---------+---------+---------------+
| onos                |  20/21  |   95%   |      124      |
+---------------------+---------+---------+---------------+
| onos-noha           |  18/18  |  100%   |               |
+---------------------+---------+---------+---------------+
| onos-sfc            |  24/24  |  100%   |               |
+---------------------+---------+---------+---------------+
| onos-sfc-noha       |  21/21  |  100%   |      157      |
+---------------------+---------+---------+---------------+
| multisite           |  N.R    |  100%   |        8      |
+---------------------+---------+---------+---------------+

Note: Multisite build tag is different due to the specificity of the POD
The build_tag is jenkins-functest-fuel-virtual-suite-colorado-8.

joid
----

+---------------------+---------+---------+---------------+
|  Scenario           | Scoring | Success |  build_tag id |
|                     |         | rate    |               |
+=====================+=========+=========+===============+
| nosdn               |  18/18  |  100%   |      102      |
+---------------------+---------+---------+---------------+
| nosdn-noha          |  17/18  |   95%   |       93      |
+---------------------+---------+---------+---------------+
| nosdn-lxd           |  12/12  |  100%   |      104      |
+---------------------+---------+---------+---------------+
| nosdn-lxd-noha      |  12/12  |  100%   |       91      |
+---------------------+---------+---------+---------------+
| odl_l2              |  19/21  |         |               |
+---------------------+---------+---------+---------------+
| onos                |  21/21  |  100%   |       99      |
+---------------------+---------+---------+---------------+
| onos-sfc            |  24/24  |  100%   |       97      |
+---------------------+---------+---------+---------------+

All the results can be found through their build_tag defined as follows:

+---------+---------------------------------------------------------------+
|         |  Build tag                                                    |
+=========+===============================================================+
| apex    | jenkins-functest-apex-apex-daily-colorado-daily-colorado-<id> |
+---------+---------------------------------------------------------------+
| compass | jenkins-functest-compass-virtual-daily-colorado-<id>          |
+---------+---------------------------------------------------------------+
| fuel    | ha: jenkins-functest-fuel-baremetal-daily-colorado-<id>       |
|         | noha: jenkins-functest-fuel-virtual-daily-colorado-<id>       |
+---------+---------------------------------------------------------------+
| joid    | jenkins-functest-joid-baremetal-daily-colorado-<id>           |
+---------+---------------------------------------------------------------+

You can get the results for each scenario using the build_tag by typing:

 http://testresults.opnfv.org/test/api/v1/results?build_tag=<the scenario build_tag>

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
| `FUNCTEST-419`_  |  do not try to Remove docker                  |
|                  |  image opnfv/functest:<none>                  |
|                  |  reported by joid on Intel POD                |
|                  |  may impact CI                                |
|                  |  not reproducible                             |
+------------------+-----------------------------------------------+
| `FUNCTEST-446`_  |  Cleanup ODL-SFC output in Functest execution |
|                  |  Impact on odl_l2-sfc scenarios               |
+------------------+-----------------------------------------------+
| `FUNCTEST-450`_  |  Functest is Failing to get the token using   |
|                  |  keystone client                              |
+------------------+-----------------------------------------------+
| `FUNCTEST-454`_  |  Cleanup failures when using HA networks in   |
|                  |  Neutron                                      |
+------------------+-----------------------------------------------+
| `FUNCTEST-460`_  |  Wrong image format used in rally cases       |
+------------------+-----------------------------------------------+
| `FUNCTEST-462`_  |  OLD test fails after forcing the clone       |
|                  |  release/beryllium-sr3 branch                 |
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
 
_`FUNCTEST-419` : https://jira.opnfv.org/browse/FUNCTEST-419

_`FUNCTEST-446` : https://jira.opnfv.org/browse/FUNCTEST-446

_`FUNCTEST-450` : https://jira.opnfv.org/browse/FUNCTEST-450

_`FUNCTEST-454` : https://jira.opnfv.org/browse/FUNCTEST-454

_`FUNCTEST-460` : https://jira.opnfv.org/browse/FUNCTEST-460

_`FUNCTEST-462` : https://jira.opnfv.org/browse/FUNCTEST-462
