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
  |     connection_check     |     functest     |     healthcheck     |      00:03       |      PASS      |
  |      tenantnetwork1      |     functest     |     healthcheck     |      00:05       |      PASS      |
  |      tenantnetwork2      |     functest     |     healthcheck     |      00:06       |      PASS      |
  |         vmready1         |     functest     |     healthcheck     |      00:06       |      PASS      |
  |         vmready2         |     functest     |     healthcheck     |      00:08       |      PASS      |
  |        singlevm1         |     functest     |     healthcheck     |      00:32       |      PASS      |
  |        singlevm2         |     functest     |     healthcheck     |      00:37       |      PASS      |
  |        vping_ssh         |     functest     |     healthcheck     |      00:46       |      PASS      |
  |      vping_userdata      |     functest     |     healthcheck     |      00:39       |      PASS      |
  |       cinder_test        |     functest     |     healthcheck     |      01:05       |      PASS      |
  |      tempest_smoke       |     functest     |     healthcheck     |      05:39       |      PASS      |
  |     tempest_horizon      |     functest     |     healthcheck     |      01:05       |      PASS      |
  |           odl            |     functest     |     healthcheck     |      00:00       |      SKIP      |
  +--------------------------+------------------+---------------------+------------------+----------------+

Smoke suite::

  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |      tempest_neutron      |     functest     |     smoke     |      15:30       |      PASS      |
  |       tempest_cinder      |     functest     |     smoke     |      02:01       |      PASS      |
  |      tempest_keystone     |     functest     |     smoke     |      01:17       |      PASS      |
  |        tempest_heat       |     functest     |     smoke     |      22:14       |      PASS      |
  |     tempest_telemetry     |     functest     |     smoke     |      00:00       |      SKIP      |
  |        rally_sanity       |     functest     |     smoke     |      17:24       |      PASS      |
  |      refstack_compute     |     functest     |     smoke     |      07:03       |      PASS      |
  |      refstack_object      |     functest     |     smoke     |      02:09       |      PASS      |
  |     refstack_platform     |     functest     |     smoke     |      07:31       |      PASS      |
  |        tempest_full       |     functest     |     smoke     |      41:52       |      PASS      |
  |      tempest_scenario     |     functest     |     smoke     |      08:42       |      PASS      |
  |        tempest_slow       |     functest     |     smoke     |      43:42       |      PASS      |
  |          patrole          |     functest     |     smoke     |      02:42       |      PASS      |
  |      tempest_barbican     |     functest     |     smoke     |      02:30       |      PASS      |
  |      tempest_octavia      |     functest     |     smoke     |      00:00       |      SKIP      |
  +---------------------------+------------------+---------------+------------------+----------------+

Smoke CNTT suite::

  +-------------------------------+------------------+---------------+------------------+----------------+
  |           TEST CASE           |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +-------------------------------+------------------+---------------+------------------+----------------+
  |      tempest_neutron_cntt     |     functest     |     smoke     |      11:35       |      PASS      |
  |      tempest_cinder_cntt      |     functest     |     smoke     |      01:58       |      PASS      |
  |     tempest_keystone_cntt     |     functest     |     smoke     |      01:13       |      PASS      |
  |       tempest_heat_cntt       |     functest     |     smoke     |      22:32       |      PASS      |
  |       rally_sanity_cntt       |     functest     |     smoke     |      17:16       |      PASS      |
  |       tempest_full_cntt       |     functest     |     smoke     |      41:13       |      PASS      |
  |     tempest_scenario_cntt     |     functest     |     smoke     |      08:57       |      PASS      |
  |       tempest_slow_cntt       |     functest     |     smoke     |      35:58       |      PASS      |
  +-------------------------------+------------------+---------------+------------------+----------------+

Benchmarking suite::

  +--------------------+------------------+----------------------+------------------+----------------+
  |     TEST CASE      |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------+------------------+----------------------+------------------+----------------+
  |     rally_full     |     functest     |     benchmarking     |      93:03       |      PASS      |
  |     rally_jobs     |     functest     |     benchmarking     |      27:05       |      PASS      |
  |        vmtp        |     functest     |     benchmarking     |      17:56       |      PASS      |
  |       shaker       |     functest     |     benchmarking     |      24:02       |      PASS      |
  +--------------------+------------------+----------------------+------------------+----------------+

Benchmarking CNTT suite::

  +-------------------------+------------------+----------------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +-------------------------+------------------+----------------------+------------------+----------------+
  |     rally_full_cntt     |     functest     |     benchmarking     |      89:52       |      PASS      |
  |     rally_jobs_cntt     |     functest     |     benchmarking     |      19:39       |      PASS      |
  |           vmtp          |     functest     |     benchmarking     |      16:59       |      PASS      |
  |          shaker         |     functest     |     benchmarking     |      23:43       |      PASS      |
  +-------------------------+------------------+----------------------+------------------+----------------+

Vnf suite::

  +----------------------+------------------+--------------+------------------+----------------+
  |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +----------------------+------------------+--------------+------------------+----------------+
  |       cloudify       |     functest     |     vnf      |      05:08       |      PASS      |
  |     cloudify_ims     |     functest     |     vnf      |      24:46       |      PASS      |
  |       heat_ims       |     functest     |     vnf      |      33:12       |      PASS      |
  |     vyos_vrouter     |     functest     |     vnf      |      15:53       |      PASS      |
  |       juju_epc       |     functest     |     vnf      |      27:52       |      PASS      |
  +----------------------+------------------+--------------+------------------+----------------+

Kubernetes healthcheck suite::

  +-------------------+------------------+---------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +-------------------+------------------+---------------------+------------------+----------------+
  |     k8s_quick     |     functest     |     healthcheck     |      00:18       |      PASS      |
  |     k8s_smoke     |     functest     |     healthcheck     |      01:14       |      PASS      |
  +-------------------+------------------+---------------------+------------------+----------------+

Kubernetes smoke suite::

  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |      k8s_conformance      |     functest     |     smoke     |      94:26       |      PASS      |
  |     xrally_kubernetes     |     functest     |     smoke     |      13:05       |      PASS      |
  +---------------------------+------------------+---------------+------------------+----------------+

Kubernetes security suite::

  +---------------------+------------------+------------------+------------------+----------------+
  |      TEST CASE      |     PROJECT      |       TIER       |     DURATION     |     RESULT     |
  +---------------------+------------------+------------------+------------------+----------------+
  |     kube_hunter     |     functest     |     security     |      00:24       |      PASS      |
  |      kube_bench     |     functest     |     security     |      00:18       |      PASS      |
  +---------------------+------------------+------------------+------------------+----------------+

Kubernetes benchmarking suite::

  +--------------------------------+------------------+----------------------+------------------+----------------+
  |           TEST CASE            |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------------------+------------------+----------------------+------------------+----------------+
  |     xrally_kubernetes_full     |     functest     |     benchmarking     |      34:16       |      PASS      |
  +--------------------------------+------------------+----------------------+------------------+----------------+

Kubernetes cnf suite::

  +-------------------------+------------------+--------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +-------------------------+------------------+--------------+------------------+----------------+
  |     cnf_conformance     |     functest     |     cnf      |      05:30       |      PASS      |
  |         k8s_vims        |     functest     |     cnf      |      20:28       |      PASS      |
  +-------------------------+------------------+--------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html
