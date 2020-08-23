.. SPDX-License-Identifier: CC-BY-4.0

Test results
============

Manual testing
--------------

In manual mode test results are displayed in the console and result files
are put in /home/opnfv/functest/results.

If you want additional logs, you may configure the logging.ini under
/usr/lib/python3.8/site-packages/xtesting/ci.

Automated testing
-----------------

In automated mode, tests are run within split Alpine containers, and test
results are displayed in jenkins logs. The result summary is provided at the
end of each suite and can be described as follow.

Healthcheck suite::

  +--------------------------+------------------+---------------------+------------------+----------------+
  |        TEST CASE         |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +--------------------------+------------------+---------------------+------------------+----------------+
  |     connection_check     |     functest     |     healthcheck     |      00:02       |      PASS      |
  |      tenantnetwork1      |     functest     |     healthcheck     |      00:06       |      PASS      |
  |      tenantnetwork2      |     functest     |     healthcheck     |      00:07       |      PASS      |
  |         vmready1         |     functest     |     healthcheck     |      00:08       |      PASS      |
  |         vmready2         |     functest     |     healthcheck     |      00:08       |      PASS      |
  |        singlevm1         |     functest     |     healthcheck     |      00:41       |      PASS      |
  |        singlevm2         |     functest     |     healthcheck     |      00:41       |      PASS      |
  |        vping_ssh         |     functest     |     healthcheck     |      01:03       |      PASS      |
  |      vping_userdata      |     functest     |     healthcheck     |      00:35       |      PASS      |
  |       cinder_test        |     functest     |     healthcheck     |      01:08       |      PASS      |
  |      tempest_smoke       |     functest     |     healthcheck     |      05:26       |      PASS      |
  |     tempest_horizon      |     functest     |     healthcheck     |      01:09       |      PASS      |
  |           odl            |     functest     |     healthcheck     |      00:00       |      SKIP      |
  +--------------------------+------------------+---------------------+------------------+----------------+

Smoke suite::

  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |      tempest_neutron      |     functest     |     smoke     |      14:27       |      PASS      |
  |       tempest_cinder      |     functest     |     smoke     |      01:53       |      PASS      |
  |      tempest_keystone     |     functest     |     smoke     |      01:19       |      PASS      |
  |        tempest_heat       |     functest     |     smoke     |      23:16       |      PASS      |
  |     tempest_telemetry     |     functest     |     smoke     |      05:03       |      PASS      |
  |        rally_sanity       |     functest     |     smoke     |      19:40       |      PASS      |
  |      refstack_compute     |     functest     |     smoke     |      08:07       |      PASS      |
  |      refstack_object      |     functest     |     smoke     |      02:23       |      PASS      |
  |     refstack_platform     |     functest     |     smoke     |      10:05       |      PASS      |
  |        tempest_full       |     functest     |     smoke     |      41:00       |      PASS      |
  |      tempest_scenario     |     functest     |     smoke     |      09:34       |      PASS      |
  |        tempest_slow       |     functest     |     smoke     |      45:05       |      PASS      |
  |          patrole          |     functest     |     smoke     |      02:30       |      PASS      |
  |      tempest_barbican     |     functest     |     smoke     |      02:16       |      PASS      |
  |      tempest_octavia      |     functest     |     smoke     |      14:01       |      PASS      |
  +---------------------------+------------------+---------------+------------------+----------------+

Smoke CNTT suite::

  +-------------------------------+------------------+---------------+------------------+----------------+
  |           TEST CASE           |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +-------------------------------+------------------+---------------+------------------+----------------+
  |      tempest_neutron_cntt     |     functest     |     smoke     |      12:53       |      PASS      |
  |      tempest_cinder_cntt      |     functest     |     smoke     |      01:57       |      PASS      |
  |     tempest_keystone_cntt     |     functest     |     smoke     |      01:15       |      PASS      |
  |       tempest_heat_cntt       |     functest     |     smoke     |      22:23       |      PASS      |
  |       rally_sanity_cntt       |     functest     |     smoke     |      16:11       |      PASS      |
  |       tempest_full_cntt       |     functest     |     smoke     |      34:57       |      PASS      |
  |     tempest_scenario_cntt     |     functest     |     smoke     |      08:51       |      PASS      |
  |       tempest_slow_cntt       |     functest     |     smoke     |      32:09       |      PASS      |
  +-------------------------------+------------------+---------------+------------------+----------------+

Benchmarking suite::

  +--------------------+------------------+----------------------+------------------+----------------+
  |     TEST CASE      |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------+------------------+----------------------+------------------+----------------+
  |     rally_full     |     functest     |     benchmarking     |      100:35      |      PASS      |
  |     rally_jobs     |     functest     |     benchmarking     |      30:18       |      PASS      |
  |        vmtp        |     functest     |     benchmarking     |      17:18       |      PASS      |
  |       shaker       |     functest     |     benchmarking     |      23:35       |      PASS      |
  +--------------------+------------------+----------------------+------------------+----------------+

Benchmarking CNTT suite::

  +-------------------------+------------------+----------------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +-------------------------+------------------+----------------------+------------------+----------------+
  |     rally_full_cntt     |     functest     |     benchmarking     |      85:26       |      PASS      |
  |     rally_jobs_cntt     |     functest     |     benchmarking     |      17:46       |      PASS      |
  |           vmtp          |     functest     |     benchmarking     |      17:11       |      PASS      |
  |          shaker         |     functest     |     benchmarking     |      23:59       |      PASS      |
  +-------------------------+------------------+----------------------+------------------+----------------+

Vnf suite::

  +----------------------+------------------+--------------+------------------+----------------+
  |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +----------------------+------------------+--------------+------------------+----------------+
  |       cloudify       |     functest     |     vnf      |      06:04       |      PASS      |
  |     cloudify_ims     |     functest     |     vnf      |      24:53       |      PASS      |
  |       heat_ims       |     functest     |     vnf      |      29:29       |      PASS      |
  |     vyos_vrouter     |     functest     |     vnf      |      17:19       |      PASS      |
  |       juju_epc       |     functest     |     vnf      |      28:53       |      PASS      |
  +----------------------+------------------+--------------+------------------+----------------+

Kubernetes healthcheck suite::

  +-------------------+------------------+---------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +-------------------+------------------+---------------------+------------------+----------------+
  |     k8s_smoke     |     functest     |     healthcheck     |      01:09       |      PASS      |
  +-------------------+------------------+---------------------+------------------+----------------+

Kubernetes smoke suite::

  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |      k8s_conformance      |     functest     |     smoke     |      76:12       |      PASS      |
  |     xrally_kubernetes     |     functest     |     smoke     |      12:22       |      PASS      |
  +---------------------------+------------------+---------------+------------------+----------------+

Kubernetes security suite::

  +---------------------+------------------+------------------+------------------+----------------+
  |      TEST CASE      |     PROJECT      |       TIER       |     DURATION     |     RESULT     |
  +---------------------+------------------+------------------+------------------+----------------+
  |     kube_hunter     |     functest     |     security     |      00:18       |      PASS      |
  |      kube_bench     |     functest     |     security     |      00:01       |      PASS      |
  +---------------------+------------------+------------------+------------------+----------------+

Kubernetes benchmarking suite::

  +--------------------------------+------------------+----------------------+------------------+----------------+
  |           TEST CASE            |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------------------+------------------+----------------------+------------------+----------------+
  |     xrally_kubernetes_full     |     functest     |     benchmarking     |      33:07       |      PASS      |
  +--------------------------------+------------------+----------------------+------------------+----------------+

Kubernetes cnf suite::

  +-------------------+------------------+--------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +-------------------+------------------+--------------+------------------+----------------+
  |      k8s_vims     |     functest     |     cnf      |      20:28       |      PASS      |
  +-------------------+------------------+--------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html
