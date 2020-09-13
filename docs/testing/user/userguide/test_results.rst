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

  +--------------------------+------------------+---------------------+------------------+----------------+
  |        TEST CASE         |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +--------------------------+------------------+---------------------+------------------+----------------+
  |     connection_check     |     functest     |     healthcheck     |      00:03       |      PASS      |
  |      tenantnetwork1      |     functest     |     healthcheck     |      00:08       |      PASS      |
  |      tenantnetwork2      |     functest     |     healthcheck     |      00:16       |      PASS      |
  |         vmready1         |     functest     |     healthcheck     |      00:09       |      PASS      |
  |         vmready2         |     functest     |     healthcheck     |      00:10       |      PASS      |
  |        singlevm1         |     functest     |     healthcheck     |      00:51       |      PASS      |
  |        singlevm2         |     functest     |     healthcheck     |      00:41       |      PASS      |
  |        vping_ssh         |     functest     |     healthcheck     |      00:56       |      PASS      |
  |      vping_userdata      |     functest     |     healthcheck     |      00:42       |      PASS      |
  |       cinder_test        |     functest     |     healthcheck     |      02:19       |      PASS      |
  |      tempest_smoke       |     functest     |     healthcheck     |      07:02       |      PASS      |
  |     tempest_horizon      |     functest     |     healthcheck     |      00:52       |      PASS      |
  |           odl            |     functest     |     healthcheck     |      00:00       |      SKIP      |
  +--------------------------+------------------+---------------------+------------------+----------------+

Smoke suite::


  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |      tempest_neutron      |     functest     |     smoke     |      16:49       |      PASS      |
  |       tempest_cinder      |     functest     |     smoke     |      01:39       |      PASS      |
  |      tempest_keystone     |     functest     |     smoke     |      00:57       |      PASS      |
  |        tempest_heat       |     functest     |     smoke     |      24:33       |      PASS      |
  |        rally_sanity       |     functest     |     smoke     |      18:41       |      PASS      |
  |      refstack_defcore     |     functest     |     smoke     |      10:38       |      PASS      |
  |        tempest_full       |     functest     |     smoke     |      55:19       |      PASS      |
  |      tempest_scenario     |     functest     |     smoke     |      11:06       |      PASS      |
  |        tempest_slow       |     functest     |     smoke     |      61:39       |      PASS      |
  |          patrole          |     functest     |     smoke     |      02:46       |      PASS      |
  |     networking-bgpvpn     |     functest     |     smoke     |      00:00       |      SKIP      |
  |       networking-sfc      |     functest     |     smoke     |      00:00       |      SKIP      |
  |      tempest_barbican     |     functest     |     smoke     |      02:30       |      PASS      |
  +---------------------------+------------------+---------------+------------------+----------------+

Smoke CNTT suite::

  +-------------------------------+------------------+---------------+------------------+----------------+
  |           TEST CASE           |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +-------------------------------+------------------+---------------+------------------+----------------+
  |      tempest_neutron_cntt     |     functest     |     smoke     |      13:54       |      PASS      |
  |      tempest_cinder_cntt      |     functest     |     smoke     |      01:46       |      PASS      |
  |     tempest_keystone_cntt     |     functest     |     smoke     |      00:58       |      PASS      |
  |       tempest_heat_cntt       |     functest     |     smoke     |      25:31       |      PASS      |
  |       rally_sanity_cntt       |     functest     |     smoke     |      18:50       |      PASS      |
  |       tempest_full_cntt       |     functest     |     smoke     |      44:32       |      PASS      |
  |     tempest_scenario_cntt     |     functest     |     smoke     |      11:14       |      PASS      |
  |       tempest_slow_cntt       |     functest     |     smoke     |      43:55       |      PASS      |
  +-------------------------------+------------------+---------------+------------------+----------------+

Benchmarking suite::

 +--------------------+------------------+----------------------+------------------+----------------+
  |     TEST CASE      |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------+------------------+----------------------+------------------+----------------+
  |     rally_full     |     functest     |     benchmarking     |      108:34      |      PASS      |
  |     rally_jobs     |     functest     |     benchmarking     |      22:07       |      PASS      |
  |        vmtp        |     functest     |     benchmarking     |      15:38       |      PASS      |
  |       shaker       |     functest     |     benchmarking     |      25:12       |      PASS      |
  +--------------------+------------------+----------------------+------------------+----------------+

Benchmarking CNTT suite::

  +-------------------------+------------------+----------------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +-------------------------+------------------+----------------------+------------------+----------------+
  |     rally_full_cntt     |     functest     |     benchmarking     |      106:60      |      PASS      |
  |     rally_jobs_cntt     |     functest     |     benchmarking     |      21:16       |      PASS      |
  |           vmtp          |     functest     |     benchmarking     |      16:15       |      PASS      |
  |          shaker         |     functest     |     benchmarking     |      25:09       |      PASS      |
  +-------------------------+------------------+----------------------+------------------+----------------+

Vnf suite::

  +----------------------+------------------+--------------+------------------+----------------+
  |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +----------------------+------------------+--------------+------------------+----------------+
  |       cloudify       |     functest     |     vnf      |      04:35       |      PASS      |
  |     cloudify_ims     |     functest     |     vnf      |      24:16       |      PASS      |
  |       heat_ims       |     functest     |     vnf      |      30:36       |      PASS      |
  |     vyos_vrouter     |     functest     |     vnf      |      15:37       |      PASS      |
  |       juju_epc       |     functest     |     vnf      |      34:39       |      PASS      |
  +----------------------+------------------+--------------+------------------+----------------+

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

Functest Kubernetes test result::

 +--------------------------------------+------------------------------------------------------------+
 |               ENV VAR                |                           VALUE                            |
 +--------------------------------------+------------------------------------------------------------+
 |            INSTALLER_TYPE            |                          compass                           |
 |           DEPLOY_SCENARIO            |                   k8-nosdn-nofeature-ha                    |
 |              BUILD_TAG               |     jenkins-functest-compass-baremetal-daily-master-75     |
 |               CI_LOOP                |                           daily                            |
 +--------------------------------------+------------------------------------------------------------+

Kubernetes healthcheck suite::

  +-------------------+------------------+---------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +-------------------+------------------+---------------------+------------------+----------------+
  |     k8s_quick     |     functest     |     healthcheck     |      00:20       |      PASS      |
  |     k8s_smoke     |     functest     |     healthcheck     |      00:45       |      PASS      |
  +-------------------+------------------+---------------------+------------------+----------------+

Kubernetes smoke suite::

  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |      k8s_conformance      |     functest     |     smoke     |      100:50      |      PASS      |
  |     xrally_kubernetes     |     functest     |     smoke     |      13:19       |      PASS      |
  +---------------------------+------------------+---------------+------------------+----------------+

Kubernetes security suite::

  +---------------------------+------------------+------------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |       TIER       |     DURATION     |     RESULT     |
  +---------------------------+------------------+------------------+------------------+----------------+
  |        kube_hunter        |     functest     |     security     |      00:19       |      PASS      |
  |     kube_bench_master     |     functest     |     security     |      00:01       |      PASS      |
  |      kube_bench_node      |     functest     |     security     |      00:01       |      PASS      |
  +---------------------------+------------------+------------------+------------------+----------------+

Kubernetes benchmarking suite::

  +--------------------------------+------------------+----------------------+------------------+----------------+
  |           TEST CASE            |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------------------+------------------+----------------------+------------------+----------------+
  |     xrally_kubernetes_full     |     functest     |     benchmarking     |      37:48       |      PASS      |
  +--------------------------------+------------------+----------------------+------------------+----------------+

Kubernetes cnf suite::

  +-------------------------+------------------+--------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +-------------------------+------------------+--------------+------------------+----------------+
  |     cnf_conformance     |     functest     |     cnf      |      02:59       |      PASS      |
  |         k8s_vims        |     functest     |     cnf      |      21:39       |      PASS      |
  +-------------------------+------------------+--------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html
