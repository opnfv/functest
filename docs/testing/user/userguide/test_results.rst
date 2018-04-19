.. SPDX-License-Identifier: CC-BY-4.0

Test results
============

Manual testing
--------------

In manual mode test results are displayed in the console and result files
are put in /home/opnfv/functest/results.

If you want additional logs, you may configure the logging.ini under
/usr/lib/python2.7/site-packages/xtesting/ci.

Automated testing
-----------------

In automated mode, tests are run within split Alpine containers, and test
results are displayed in jenkins logs. The result summary is provided at the
end of each suite and can be described as follow.

Healthcheck suite::

 +----------------------------+------------------+---------------------+------------------+----------------+
 |         TEST CASE          |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
 +----------------------------+------------------+---------------------+------------------+----------------+
 |      connection_check      |     functest     |     healthcheck     |      00:07       |      PASS      |
 |         api_check          |     functest     |     healthcheck     |      07:46       |      PASS      |
 |     snaps_health_check     |     functest     |     healthcheck     |      00:36       |      PASS      |
 +----------------------------+------------------+---------------------+------------------+----------------+

Smoke suite::

 +------------------------------+------------------+---------------+------------------+----------------+
 |          TEST CASE           |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
 +------------------------------+------------------+---------------+------------------+----------------+
 |          vping_ssh           |     functest     |     smoke     |      00:57       |      PASS      |
 |        vping_userdata        |     functest     |     smoke     |      00:33       |      PASS      |
 |     tempest_smoke_serial     |     functest     |     smoke     |      13:22       |      PASS      |
 |         rally_sanity         |     functest     |     smoke     |      24:07       |      PASS      |
 |       refstack_defcore       |     functest     |     smoke     |      05:21       |      PASS      |
 |           patrole            |     functest     |     smoke     |      04:29       |      PASS      |
 |         snaps_smoke          |     functest     |     smoke     |      46:54       |      PASS      |
 |             odl              |     functest     |     smoke     |      00:00       |      SKIP      |
 |        neutron_trunk         |     functest     |     smoke     |      00:00       |      SKIP      |
 +------------------------------+------------------+---------------+------------------+----------------+

Features suite::

 +-----------------------------+------------------------+------------------+------------------+----------------+
 |          TEST CASE          |        PROJECT         |       TIER       |     DURATION     |     RESULT     |
 +-----------------------------+------------------------+------------------+------------------+----------------+
 |     doctor-notification     |         doctor         |     features     |      00:00       |      SKIP      |
 |            bgpvpn           |         sdnvpn         |     features     |      00:00       |      SKIP      |
 |       functest-odl-sfc      |          sfc           |     features     |      00:00       |      SKIP      |
 |      barometercollectd      |       barometer        |     features     |      00:00       |      SKIP      |
 |             fds             |     fastdatastacks     |     features     |      00:00       |      SKIP      |
 +-----------------------------+------------------------+------------------+------------------+----------------+

Components suite::

 +-------------------------------+------------------+--------------------+------------------+----------------+
 |           TEST CASE           |     PROJECT      |        TIER        |     DURATION     |     RESULT     |
 +-------------------------------+------------------+--------------------+------------------+----------------+
 |     tempest_full_parallel     |     functest     |     components     |      48:28       |      PASS      |
 |           rally_full          |     functest     |     components     |      126:02      |      PASS      |
 +-------------------------------+------------------+--------------------+------------------+----------------+

Vnf suite::

 +----------------------+------------------+--------------+------------------+----------------+
 |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
 +----------------------+------------------+--------------+------------------+----------------+
 |     cloudify_ims     |     functest     |     vnf      |      28:15       |      PASS      |
 |     vyos_vrouter     |     functest     |     vnf      |      17:59       |      PASS      |
 |       juju_epc       |     functest     |     vnf      |      46:44       |      PASS      |
 +----------------------+------------------+--------------+------------------+----------------+

Parser testcase::

 +-----------------------+-----------------+------------------+------------------+----------------+
 |       TEST CASE       |     PROJECT     |       TIER       |     DURATION     |     RESULT     |
 +-----------------------+-----------------+------------------+------------------+----------------+
 |     parser-basics     |      parser     |     features     |      00:00       |      SKIP      |
 +-----------------------+-----------------+------------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html
