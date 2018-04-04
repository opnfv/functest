.. SPDX-License-Identifier: CC-BY-4.0

Test results
============

Manual testing
--------------

In manual mode test results are displayed in the console and result files
are put in /home/opnfv/functest/results.

If you want additional logs, you may configure the logging.ini under
/usr/lib/python2.7/site-packages/functest/ci.

Automated testing
-----------------

In automated mode, test results are displayed in jenkins logs, a summary is
provided at the end of the job and can be described as follow::

 +-------------------------+----------------------------------------------------------+
 |         ENV VAR         |                          VALUE                           |
 +-------------------------+----------------------------------------------------------+
 |      INSTALLER_TYPE     |                          daisy                           |
 |     DEPLOY_SCENARIO     |                  os-nosdn-nofeature-ha                   |
 |        BUILD_TAG        |     jenkins-functest-daisy-baremetal-daily-master-67     |
 |         CI_LOOP         |                          daily                           |
 +-------------------------+----------------------------------------------------------+

::

 +------------------------------+------------------+---------------------+------------------+----------------+
 |          TEST CASE           |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
 +------------------------------+------------------+---------------------+------------------+----------------+
 |       connection_check       |     functest     |     healthcheck     |      00:08       |      PASS      |
 |          api_check           |     functest     |     healthcheck     |      04:22       |      PASS      |
 |      snaps_health_check      |     functest     |     healthcheck     |      00:35       |      PASS      |
 |          vping_ssh           |     functest     |        smoke        |      00:54       |      PASS      |
 |        vping_userdata        |     functest     |        smoke        |      00:27       |      PASS      |
 |     tempest_smoke_serial     |     functest     |        smoke        |      19:39       |      FAIL      |
 |         rally_sanity         |     functest     |        smoke        |      15:16       |      PASS      |
 |       refstack_defcore       |     functest     |        smoke        |      15:55       |      PASS      |
 |         snaps_smoke          |     functest     |        smoke        |      26:45       |      FAIL      |
 |           cloudify_ims       |     functest     |         vnf         |      23:56       |      PASS      |
 |        orchestra_openims     |     orchestra    |         vnf         |      15:07       |      PASS      |
 |     orchestra_clearwaterims  |     orchestra    |         vnf         |      19:10       |      PASS      |
 |           vyos_vrouter       |     functest     |         vnf         |      00:00       |      SKIP      |
 +------------------------------+------------------+---------------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html
