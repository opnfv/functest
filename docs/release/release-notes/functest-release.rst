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
OPNFV Danube2.0 release note for Functest
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
| 2016-08-17 | 1.0.0    | Morgan Richomme  | Functest for           |
|            |          | (Orange)         | Colorado.1.0 release   |
+------------+----------+------------------+------------------------+
| 2016-10-24 | 2.0.0    | Morgan Richomme  | Functest for           |
|            |          | (Orange)         | Colorado.2.0 release   |
+------------+----------+------------------+------------------------+
| 2016-08-17 | 3.0.0    | Morgan Richomme  | Functest for           |
|            |          | (Orange)         | Colorado.3.0 release   |
+------------+----------+------------------+------------------------+
| 2017-03-29 | 4.0.0    | Jose Lausuch     | Functest for           |
|            |          | (Ericsson)       | Danube.1.0 release     |
+------------+----------+------------------+------------------------+
| 2017-05-04 | 5.0.0    | Jose Lausuch     | Functest for           |
|            |          | (Ericsson)       | Danube.2.0 release     |
+------------+----------+------------------+------------------------+
| 2017-07-12 | 6.0.0    | Jose Lausuch     | Functest for           |
|            |          | (Ericsson)       | Danube.3.0 release     |
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
| **Repo/tag**                         | danube.3.0                           |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release designation**              | Danube service release               |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Release date**                     | July 14th 2017                       |
|                                      |                                      |
+--------------------------------------+--------------------------------------+
| **Purpose of the delivery**          | Danube third release                 |
|                                      |                                      |
+--------------------------------------+--------------------------------------+

Deliverables
============

Software
--------

 - The Functest Docker image: https://hub.docker.com/r/opnfv/functest (tag: danube.3.0)

 - The TestAPI Docker image: https://hub.docker.com/r/opnfv/testapi (tag:danube.3.0)


Documents
---------

 - Installation/configuration guide: http://docs.opnfv.org/en/stable-danube/submodules/functest/docs/testing/user/configguide/index.html

 - User Guide: http://docs.opnfv.org/en/stable-danube/submodules/functest/docs/testing/user/userguide/index.html

 - Developer Guide: http://docs.opnfv.org/en/stable-danube/submodules/functest/docs/testing/developer/devguide/index.html


Version change
==============


- Bugfixes in refstack client

- Fixed vIMS onboarding and ims deployment

- Increased timeout of OpenBaton installation

- Switched to mitaka-eol in openstack repositories, as stable/mitake is not longer existing

- Minor fixes in logging and test cases

- 3 scenarios have been successfully executed on aarch64 architectures on Fuel deployments (nosdn, odl_l2 and odl_l3)


Scenario Matrix
===============

For Danube 3.0, Functest was tested on the following HA scenarios (new
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
 tests = vping_ssh+vping_userdata+tempest+rally+odl+doctor
 Scoring = 18/18 = 6 * 3

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

+------------------+---------+---------+-----------------+
|  Scenario        | Scoring | Success |    Results      |
|                  |         | rate    |                 |
+==================+=========+=========+=================+
| nosdn            |  20/30  |    67%  | `apex-res-1`_   |
+------------------+---------+---------+-----------------+
| odl_l3           |  16/30  |    53%  | `apex-res-2`_   |
+------------------+---------+---------+-----------------+
| odl-bgpvpn       |  18/33  |    56%  | `apex-res-3`_   |
+------------------+---------+---------+-----------------+
| odl-gluon        |  20/33  |    61%  | `apex-res-4`_   |
+------------------+---------+---------+-----------------+
| kvm              |  20/30  |    67%  | `apex-res-5`_   |
+------------------+---------+---------+-----------------+
| odl_l2-fdio      |  25/33  |    76%  | `apex-res-6`_   |
+------------------+---------+---------+-----------------+
| odl_l2-fdio-noha |  24/33  |    73%  |   local push    |
+------------------+---------+---------+-----------------+
| odl_l3-fdio-noha |  18/30  |    60%  |   local push    |
+------------------+---------+---------+-----------------+
| fdio             |  25/27  |    93%  |   local push    |
+------------------+---------+---------+-----------------+

Compass
-------

+------------------+---------+---------+------------------+
|  Scenario        | Scoring | Success |  Results         |
|                  |         | rate    |                  |
+==================+=========+=========+==================+
| nosdn            |  29/30  |    97%  | `compass-res-1`_ |
+------------------+---------+---------+------------------+
| odl_l2           |  29/33  |    88%  | `compass-res-2`_ |
+------------------+---------+---------+------------------+
| odl_l3           |  23/30  |    77%  | `compass-res-3`_ |
+------------------+---------+---------+------------------+
| onos             |  29/30  |    97%  | `compass-res-4`_ |
+------------------+---------+---------+------------------+
| onos-sfc         |  20/36  |    56%  | `compass-res-5`_ |
+------------------+---------+---------+------------------+

Note: all the Compass tests for Danube have been executed on virtual
environment. Bare metal resources were used for Master branch.


Fuel
----

+----------------------+---------+---------+----------------+
|  Scenario            | Scoring | Success |  Results       |
|                      |         | rate    |                |
+======================+=========+=========+================+
| nosdn                |  39/39  |  100%   | `fuel-res-1`_  |
+----------------------+---------+---------+----------------+
| nosdn-noha           |  36/36  |  100%   | `fuel-res-2`_  |
+----------------------+---------+---------+----------------+
| nosdn-kvm            |  39/39  |  100%   | `fuel-res-3`_  |
+----------------------+---------+---------+----------------+
| nosdn-kvm-noha       |  36/36  |  100%   | `fuel-res-4`_  |
+----------------------+---------+---------+----------------+
| nosdn-ovs            |  39/39  |  100%   | `fuel-res-5`_  |
+----------------------+---------+---------+----------------+
| nosdn-ovs-noha       |  36/36  |  100%   | `fuel-res-6`_  |
+----------------------+---------+---------+----------------+
| odl_l2               |  42/42  |  100%   | `fuel-res-7`_  |
+----------------------+---------+---------+----------------+
| odl_l2-noha          |  39/39  |  100%   | `fuel-res-8`_  |
+----------------------+---------+---------+----------------+
| odl_l2-sfc           |  45/45  |  100%   | `fuel-res-9`_  |
+----------------------+---------+---------+----------------+
| odl_l2-sfc-noha      |  35/42  |   83%   | `fuel-res-10`_ |
+----------------------+---------+---------+----------------+
| odl_l3               |  36/39  |   92%   | `fuel-res-11`_ |
+----------------------+---------+---------+----------------+
| odl_l3-noha          |  36/36  |  100%   | `fuel-res-12`_ |
+----------------------+---------+---------+----------------+
| kvm_ovs_dpdk         |  39/39  |  100%   | `fuel-res-13`_ |
+----------------------+---------+---------+----------------+
| kvm_ovs_dpdk_noha    |  35/36  |   97%   | `fuel-res-14`_ |
+----------------------+---------+---------+----------------+
| kvm_ovs_dpdk_bar     |  42/42  |  100%   | `fuel-res-15`_ |
+----------------------+---------+---------+----------------+
| kvm_ovs_dpdk_bar_noha|  36/39  |   92%   | `fuel-res-16`_ |
+----------------------+---------+---------+----------------+




Joid
----

+---------------------+---------+---------+---------------+
|  Scenario           | Scoring | Success |  Results      |
|                     |         | rate    |               |
+=====================+=========+=========+===============+
| nosdn               |  30/30  |  100%   | `joid-res-1`_ |
+---------------------+---------+---------+---------------+
| nosdn-noha          |  10/30  |   33%   | `joid-res-2`_ |
+---------------------+---------+---------+---------------+
| nosdn-lxd           |  19/21  |   90%   | `joid-res-3`_ |
+---------------------+---------+---------+---------------+
| nosdn-lxd-noha      |  15/21  |   71%   | `joid-res-4`_ |
+---------------------+---------+---------+---------------+
| odl_l2              |   6/33  |   18%   | `joid-res-5`_ |
+---------------------+---------+---------+---------------+

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
| fuel      | odl_-*    | Tempest test case "TestServerBasicOps"       |
|           |           | disabled due to bug `tempest-bug`_           |
+-----------+-----------+----------------------------------------------+
| apex/fuel | *-bgpvpn  | Due to some instabilities in the bgpvpn      |
|           |           | test case, the scenario has been postponed   |
|           |           | to Danube 2.0                                |
+-----------+-----------+----------------------------------------------+
| apex      | *-gluon   | vPing_ssh disabled due to floating ips       |
|           |           | not working 100% of the times.               |
|           |           | Tempest test "test_reboot_server_hard"       |
|           |           | disabled due to bug `gluon-bug`_             |
+-----------+-----------+----------------------------------------------+
| joid      | any       | Tempest cases related to object storage      |
|           |           | excluded                                     |
+-----------+-----------+----------------------------------------------+
| any       | any       | The VNF tier has not been fully tested       |
|           |           | since it has not been run in daily loops     |
|           |           | in CI. Weekly jobs have been activated       |
|           |           | a bit late in the process and have not been  |
|           |           | used to validate the scenarios.              |
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
|                  |                                               |
|                  |                                               |
+------------------+-----------------------------------------------+

All the tickets that are not blocking have been fixed or postponed
the next release.

Functest Danube 2.0 is released without known bugs.



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

.. _`tempest-bug`: https://bugs.launchpad.net/tempest/+bug/1577632

.. _`gluon-bug`: https://bugs.opendaylight.org/show_bug.cgi?id=5586


.. _`apex-res-1`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-baremetal-daily-danube-455

.. _`apex-res-2`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-baremetal-daily-danube-466

.. _`apex-res-3`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-baremetal-daily-danube-449

.. _`apex-res-4`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-baremetal-daily-danube-450

.. _`apex-res-5`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-baremetal-daily-danube-461

.. _`apex-res-6`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-apex-baremetal-daily-danube-485


.. _`compass-res-1`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-virtual-daily-danube-484

.. _`compass-res-2`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-virtual-daily-danube-454

.. _`compass-res-3`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-baremetal-daily-danube-482

.. _`compass-res-4`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-virtual-daily-danube-481

.. _`compass-res-5`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-compass-baremetal-daily-danube-453


.. _`fuel-res-1`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-danube-54

.. _`fuel-res-2`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-danube-937

.. _`fuel-res-3`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-danube-873

.. _`fuel-res-4`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-danube-935

.. _`fuel-res-5`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-danube-875

.. _`fuel-res-6`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-danube-936

.. _`fuel-res-7`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-danube-867

.. _`fuel-res-8`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-danube-939

.. _`fuel-res-9`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-danube-870

.. _`fuel-res-10`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-danube-933

.. _`fuel-res-11`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-danube-868

.. _`fuel-res-12`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-danube-940

.. _`fuel-res-13`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-danube-871

.. _`fuel-res-14`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-danube-938

.. _`fuel-res-15`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-baremetal-daily-danube-869

.. _`fuel-res-16`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-fuel-virtual-daily-danube-941


.. _`joid-res-1`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-danube-298

.. _`joid-res-2`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-danube-260

.. _`joid-res-3`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-danube-281

.. _`joid-res-4`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-danube-301

.. _`joid-res-5`: http://testresults.opnfv.org/test/api/v1/results?build_tag=jenkins-functest-joid-baremetal-daily-danube-291
