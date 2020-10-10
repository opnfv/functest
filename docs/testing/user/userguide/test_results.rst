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
  |      tenantnetwork1      |     functest     |     healthcheck     |      00:04       |      PASS      |
  |      tenantnetwork2      |     functest     |     healthcheck     |      00:06       |      PASS      |
  |         vmready1         |     functest     |     healthcheck     |      00:05       |      PASS      |
  |         vmready2         |     functest     |     healthcheck     |      00:06       |      PASS      |
  |        singlevm1         |     functest     |     healthcheck     |      00:31       |      PASS      |
  |        singlevm2         |     functest     |     healthcheck     |      00:35       |      PASS      |
  |        vping_ssh         |     functest     |     healthcheck     |      00:47       |      PASS      |
  |      vping_userdata      |     functest     |     healthcheck     |      00:42       |      PASS      |
  |       cinder_test        |     functest     |     healthcheck     |      01:09       |      PASS      |
  |      tempest_smoke       |     functest     |     healthcheck     |      04:50       |      PASS      |
  |     tempest_horizon      |     functest     |     healthcheck     |      01:00       |      PASS      |
  |           odl            |     functest     |     healthcheck     |      00:00       |      SKIP      |
  +--------------------------+------------------+---------------------+------------------+----------------+

Smoke suite::

  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |      tempest_neutron      |     functest     |     smoke     |      11:58       |      PASS      |
  |       tempest_cinder      |     functest     |     smoke     |      02:13       |      PASS      |
  |      tempest_keystone     |     functest     |     smoke     |      01:18       |      PASS      |
  |        tempest_heat       |     functest     |     smoke     |      23:24       |      PASS      |
  |     tempest_telemetry     |     functest     |     smoke     |      01:54       |      PASS      |
  |        rally_sanity       |     functest     |     smoke     |      20:29       |      PASS      |
  |      refstack_compute     |     functest     |     smoke     |      05:16       |      PASS      |
  |      refstack_object      |     functest     |     smoke     |      01:59       |      PASS      |
  |     refstack_platform     |     functest     |     smoke     |      06:42       |      PASS      |
  |        tempest_full       |     functest     |     smoke     |      31:30       |      PASS      |
  |      tempest_scenario     |     functest     |     smoke     |      09:57       |      PASS      |
  |        tempest_slow       |     functest     |     smoke     |      57:15       |      PASS      |
  |       patrole_admin       |     functest     |     smoke     |      22:15       |      PASS      |
  |       patrole_member      |     functest     |     smoke     |      23:58       |      PASS      |
  |       patrole_reader      |     functest     |     smoke     |      22:15       |      PASS      |
  |      tempest_barbican     |     functest     |     smoke     |      03:37       |      PASS      |
  |      tempest_octavia      |     functest     |     smoke     |      00:00       |      SKIP      |
  |       tempest_cyborg      |     functest     |     smoke     |      00:00       |      SKIP      |
  +---------------------------+------------------+---------------+------------------+----------------+

Smoke CNTT suite::

  +-------------------------------+------------------+---------------+------------------+----------------+
  |           TEST CASE           |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +-------------------------------+------------------+---------------+------------------+----------------+
  |      tempest_neutron_cntt     |     functest     |     smoke     |      10:03       |      PASS      |
  |      tempest_cinder_cntt      |     functest     |     smoke     |      02:10       |      PASS      |
  |     tempest_keystone_cntt     |     functest     |     smoke     |      01:17       |      PASS      |
  |       tempest_heat_cntt       |     functest     |     smoke     |      22:44       |      PASS      |
  |       rally_sanity_cntt       |     functest     |     smoke     |      17:37       |      PASS      |
  |       tempest_full_cntt       |     functest     |     smoke     |      29:48       |      PASS      |
  |     tempest_scenario_cntt     |     functest     |     smoke     |      09:59       |      PASS      |
  |       tempest_slow_cntt       |     functest     |     smoke     |      41:57       |      PASS      |
  +-------------------------------+------------------+---------------+------------------+----------------+

Benchmarking suite::

  +--------------------+------------------+----------------------+------------------+----------------+
  |     TEST CASE      |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------+------------------+----------------------+------------------+----------------+
  |     rally_full     |     functest     |     benchmarking     |      104:28      |      PASS      |
  |     rally_jobs     |     functest     |     benchmarking     |      30:00       |      PASS      |
  |        vmtp        |     functest     |     benchmarking     |      23:43       |      PASS      |
  |       shaker       |     functest     |     benchmarking     |      28:49       |      PASS      |
  +--------------------+------------------+----------------------+------------------+----------------+

Benchmarking CNTT suite::

  +-------------------------+------------------+----------------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +-------------------------+------------------+----------------------+------------------+----------------+
  |     rally_full_cntt     |     functest     |     benchmarking     |      90:27       |      PASS      |
  |     rally_jobs_cntt     |     functest     |     benchmarking     |      22:58       |      PASS      |
  |           vmtp          |     functest     |     benchmarking     |      23:43       |      PASS      |
  |          shaker         |     functest     |     benchmarking     |      28:49       |      PASS      |
  +-------------------------+------------------+----------------------+------------------+----------------+

Vnf suite::

  +----------------------+------------------+--------------+------------------+----------------+
  |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +----------------------+------------------+--------------+------------------+----------------+
  |       cloudify       |     functest     |     vnf      |      04:23       |      PASS      |
  |     cloudify_ims     |     functest     |     vnf      |      24:42       |      PASS      |
  |       heat_ims       |     functest     |     vnf      |      30:33       |      PASS      |
  |     vyos_vrouter     |     functest     |     vnf      |      17:31       |      PASS      |
  |       juju_epc       |     functest     |     vnf      |      37:21       |      PASS      |
  +----------------------+------------------+--------------+------------------+----------------+

Kubernetes healthcheck suite::

  +-------------------+------------------+---------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +-------------------+------------------+---------------------+------------------+----------------+
  |     k8s_quick     |     functest     |     healthcheck     |      00:13       |      PASS      |
  |     k8s_smoke     |     functest     |     healthcheck     |      00:26       |      PASS      |
  +-------------------+------------------+---------------------+------------------+----------------+

Kubernetes smoke suite::

  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |      k8s_conformance      |     functest     |     smoke     |      103:05      |      PASS      |
  |     xrally_kubernetes     |     functest     |     smoke     |      14:17       |      PASS      |
  +---------------------------+------------------+---------------+------------------+----------------+

Kubernetes security suite::

  +---------------------------+------------------+------------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |       TIER       |     DURATION     |     RESULT     |
  +---------------------------+------------------+------------------+------------------+----------------+
  |        kube_hunter        |     functest     |     security     |      00:18       |      PASS      |
  |     kube_bench_master     |     functest     |     security     |      00:07       |      PASS      |
  |      kube_bench_node      |     functest     |     security     |      00:06       |      PASS      |
  +---------------------------+------------------+------------------+------------------+----------------+

Kubernetes benchmarking suite::

  +--------------------------------+------------------+----------------------+------------------+----------------+
  |           TEST CASE            |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------------------+------------------+----------------------+------------------+----------------+
  |     xrally_kubernetes_full     |     functest     |     benchmarking     |      39:15       |      PASS      |
  +--------------------------------+------------------+----------------------+------------------+----------------+

Kubernetes cnf suite::

  +-------------------------+------------------+--------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +-------------------------+------------------+--------------+------------------+----------------+
  |         k8s_vims        |     functest     |     cnf      |      09:27       |      PASS      |
  |        helm_vims        |     functest     |     cnf      |      09:12       |      PASS      |
  |     cnf_conformance     |     functest     |     cnf      |      02:55       |      PASS      |
  +-------------------------+------------------+--------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html
