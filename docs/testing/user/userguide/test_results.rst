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
results are displayed in jenkins logs. The tests to be executed and a result
summary is provided at the front and end of each tier and can be described as
follow::

 +--------------------------------------+------------------------------------------------------------+
 |               ENV VAR                |                           VALUE                            |
 +--------------------------------------+------------------------------------------------------------+
 |              BUILD_TAG               |     jenkins-functest-compass-baremetal-daily-fraser-18     |
 |       ENERGY_RECORDER_API_URL        |              http://energy.opnfv.fr/resources              |
 |     ENERGY_RECORDER_API_PASSWORD     |                                                            |
 |               CI_LOOP                |                           daily                            |
 |             TEST_DB_URL              |      http://testresults.opnfv.org/test/api/v1/results      |
 |            INSTALLER_TYPE            |                          compass                           |
 |           DEPLOY_SCENARIO            |                   os-nosdn-nofeature-ha                    |
 |       ENERGY_RECORDER_API_USER       |                                                            |
 |              NODE_NAME               |                        huawei-pod2                         |
 +--------------------------------------+------------------------------------------------------------+

For opnfv/functest-healthcheck container::

 +----------------------------+------------------+---------------------+------------------+----------------+
 |         TEST CASE          |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
 +----------------------------+------------------+---------------------+------------------+----------------+
 |      connection_check      |     functest     |     healthcheck     |      00:13       |      PASS      |
 |         api_check          |     functest     |     healthcheck     |      10:07       |      PASS      |
 |     snaps_health_check     |     functest     |     healthcheck     |      01:29       |      PASS      |
 +----------------------------+------------------+---------------------+------------------+----------------+

For opnfv/functest-smoke container::

 +------------------------------+------------------+---------------+------------------+----------------+
 |          TEST CASE           |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
 +------------------------------+------------------+---------------+------------------+----------------+
 |          vping_ssh           |     functest     |     smoke     |      01:44       |      PASS      |
 |        vping_userdata        |     functest     |     smoke     |      01:32       |      PASS      |
 |     tempest_smoke_serial     |     functest     |     smoke     |      14:11       |      FAIL      |
 |         rally_sanity         |     functest     |     smoke     |      30:37       |      FAIL      |
 |       refstack_defcore       |     functest     |     smoke     |      03:13       |      PASS      |
 |           patrole            |     functest     |     smoke     |      02:51       |      PASS      |
 |         snaps_smoke          |     functest     |     smoke     |      54:44       |      FAIL      |
 |        neutron_trunk         |     functest     |     smoke     |      02:55       |      FAIL      |
 |             odl              |     functest     |     smoke     |      00:00       |      SKIP      |
 +------------------------------+------------------+---------------+------------------+----------------+

For opnfv/functest-features container::

 +-----------------------------+------------------------+------------------+------------------+----------------+
 |          TEST CASE          |        PROJECT         |       TIER       |     DURATION     |     RESULT     |
 +-----------------------------+------------------------+------------------+------------------+----------------+
 |     doctor-notification     |         doctor         |     features     |      00:00       |      SKIP      |
 |            bgpvpn           |         sdnvpn         |     features     |      00:00       |      SKIP      |
 |       functest-odl-sfc      |          sfc           |     features     |      00:00       |      SKIP      |
 |      barometercollectd      |       barometer        |     features     |      00:00       |      SKIP      |
 |             fds             |     fastdatastacks     |     features     |      00:00       |      SKIP      |
 +-----------------------------+------------------------+------------------+------------------+----------------+

For opnfv/functest-vnf container::

 +----------------------+------------------+--------------+------------------+----------------+
 |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
 +----------------------+------------------+--------------+------------------+----------------+
 |     cloudify_ims     |     functest     |     vnf      |      38:18       |      PASS      |
 |     vyos_vrouter     |     functest     |     vnf      |      31:12       |      PASS      |
 |       juju_epc       |     functest     |     vnf      |      57:31       |      PASS      |
 +----------------------+------------------+--------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html
