.. This work is licensed under a Creative Commons Attribution 4.0 International Licence.
.. http://creativecommons.org/licenses/by/4.0

FuncTest test result document overview
======================================

Functest project is described in `Functest user guide`_.
The user guide details the different test cases as well as the possible errors.
A `developer guide`_ and a `configuration guide`_ are also available.

Functest is run systematically at the end of an OPNFV fresh installation.
All the runnable tests are run sequentially. The installer and the scenario are
considered to evaluate whether the test case can be run or not. That is why all
the number of test cases may vary from 1 installer to another and from 1
scenario to another.

The list of scenario supported by installer can be described as follows:

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

The matrix below details the Functest runnable tests versus the installer and
the scenario:

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

all means that the test case is run on all the scenarios related to the
installer.

Functest results from continuous integration can be found in:
 * jenkins logs: https://build.opnfv.org/ci/view/functest/
 * artifacts http://artifacts.opnfv.org/, it includes the tempest logs and the
 Rally html pages

Additional test result assests and information
==============================================

The Functest deals with 2 dashboards:
 * The `Test Dashboard`_ provides an overview of all the projects
 * The  `Functest Dashboard`_ dedicated to Functest real-time test results

    * is used to provide a quick overview of the different testcases according to installer and scenario.

.. _`Test Dashboard`: https://www.opnfv.org/opnfvtestgraphs/per-test-projects/default
.. _`Functest Dashboard`: https://testresults.opnfv.org/dashboard/
.. _`Functest user guide`: artifacts.opnfv.org/functest/docs/userguide/index.html
.. _`developer guide`: artifacts.opnfv.org/functest/docs/devguide/index.html
.. _`configuration guide`: artifacts.opnfv.org/functest/docs/configguide/index.html
