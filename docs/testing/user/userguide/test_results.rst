.. SPDX-License-Identifier: CC-BY-4.0

Test results
============

Manual testing
--------------

In manual mode test results are displayed in the console and result files
are put in /home/opnfv/functest/results.

If you want additional logs, you may configure the logging.ini under
/usr/lib/python3.7/site-packages/xtesting/ci.

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
  |      tenantnetwork2      |     functest     |     healthcheck     |      00:05       |      PASS      |
  |         vmready1         |     functest     |     healthcheck     |      00:05       |      PASS      |
  |         vmready2         |     functest     |     healthcheck     |      00:08       |      PASS      |
  |        singlevm1         |     functest     |     healthcheck     |      00:35       |      PASS      |
  |        singlevm2         |     functest     |     healthcheck     |      00:34       |      PASS      |
  |        vping_ssh         |     functest     |     healthcheck     |      00:44       |      PASS      |
  |      vping_userdata      |     functest     |     healthcheck     |      00:30       |      PASS      |
  |       cinder_test        |     functest     |     healthcheck     |      01:10       |      PASS      |
  |      tempest_smoke       |     functest     |     healthcheck     |      11:18       |      PASS      |
  |     tempest_horizon      |     functest     |     healthcheck     |      01:15       |      PASS      |
  |           odl            |     functest     |     healthcheck     |      00:00       |      SKIP      |
  +--------------------------+------------------+---------------------+------------------+----------------+

Smoke suite::

  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |      tempest_neutron      |     functest     |     smoke     |      14:49       |      PASS      |
  |       tempest_cinder      |     functest     |     smoke     |      01:40       |      PASS      |
  |      tempest_keystone     |     functest     |     smoke     |      01:12       |      PASS      |
  |        tempest_heat       |     functest     |     smoke     |      21:53       |      PASS      |
  |        rally_sanity       |     functest     |     smoke     |      17:10       |      PASS      |
  |      refstack_compute     |     functest     |     smoke     |      07:53       |      PASS      |
  |      refstack_object      |     functest     |     smoke     |      01:59       |      PASS      |
  |     refstack_platform     |     functest     |     smoke     |      07:52       |      PASS      |
  |        tempest_full       |     functest     |     smoke     |      34:39       |      PASS      |
  |      tempest_scenario     |     functest     |     smoke     |      08:30       |      PASS      |
  |        tempest_slow       |     functest     |     smoke     |      44:40       |      PASS      |
  |          patrole          |     functest     |     smoke     |      02:43       |      PASS      |
  |      tempest_barbican     |     functest     |     smoke     |      02:26       |      PASS      |
  |      tempest_octavia      |     functest     |     smoke     |      00:00       |      SKIP      |
  +---------------------------+------------------+---------------+------------------+----------------+

Smoke CNTT suite::

  +-------------------------------+------------------+---------------+------------------+----------------+
  |           TEST CASE           |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +-------------------------------+------------------+---------------+------------------+----------------+
  |      tempest_neutron_cntt     |     functest     |     smoke     |      12:21       |      PASS      |
  |      tempest_cinder_cntt      |     functest     |     smoke     |      01:31       |      PASS      |
  |     tempest_keystone_cntt     |     functest     |     smoke     |      01:08       |      PASS      |
  |       tempest_heat_cntt       |     functest     |     smoke     |      21:47       |      PASS      |
  |       rally_sanity_cntt       |     functest     |     smoke     |      16:09       |      PASS      |
  |       tempest_full_cntt       |     functest     |     smoke     |      39:11       |      PASS      |
  |     tempest_scenario_cntt     |     functest     |     smoke     |      08:32       |      PASS      |
  |       tempest_slow_cntt       |     functest     |     smoke     |      32:22       |      PASS      |
  +-------------------------------+------------------+---------------+------------------+----------------+

Benchmarking suite::

  +--------------------+------------------+----------------------+------------------+----------------+
  |     TEST CASE      |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------+------------------+----------------------+------------------+----------------+
  |     rally_full     |     functest     |     benchmarking     |      91:42       |      PASS      |
  |     rally_jobs     |     functest     |     benchmarking     |      25:24       |      PASS      |
  |        vmtp        |     functest     |     benchmarking     |      16:47       |      PASS      |
  |       shaker       |     functest     |     benchmarking     |      23:43       |      PASS      |
  +--------------------+------------------+----------------------+------------------+----------------+

Benchmarking CNTT suite::

  +-------------------------+------------------+----------------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +-------------------------+------------------+----------------------+------------------+----------------+
  |     rally_full_cntt     |     functest     |     benchmarking     |      86:41       |      PASS      |
  |     rally_jobs_cntt     |     functest     |     benchmarking     |      19:16       |      PASS      |
  |           vmtp          |     functest     |     benchmarking     |      17:05       |      PASS      |
  |          shaker         |     functest     |     benchmarking     |      23:33       |      PASS      |
  +-------------------------+------------------+----------------------+------------------+----------------+

Vnf suite::

  +----------------------+------------------+--------------+------------------+----------------+
  |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +----------------------+------------------+--------------+------------------+----------------+
  |       cloudify       |     functest     |     vnf      |      04:41       |      PASS      |
  |     cloudify_ims     |     functest     |     vnf      |      21:03       |      PASS      |
  |       heat_ims       |     functest     |     vnf      |      30:04       |      PASS      |
  |     vyos_vrouter     |     functest     |     vnf      |      16:21       |      PASS      |
  |       juju_epc       |     functest     |     vnf      |      28:33       |      PASS      |
  +----------------------+------------------+--------------+------------------+----------------+

Kubernetes healthcheck suite::

  +-------------------+------------------+---------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +-------------------+------------------+---------------------+------------------+----------------+
  |     k8s_quick     |     functest     |     healthcheck     |      00:33       |      PASS      |
  |     k8s_smoke     |     functest     |     healthcheck     |      00:49       |      PASS      |
  +-------------------+------------------+---------------------+------------------+----------------+

Kubernetes smoke suite::

  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |      k8s_conformance      |     functest     |     smoke     |      68:21       |      PASS      |
  |     xrally_kubernetes     |     functest     |     smoke     |      13:40       |      PASS      |
  +---------------------------+------------------+---------------+------------------+----------------+

Kubernetes security suite::

  +---------------------------+------------------+------------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |       TIER       |     DURATION     |     RESULT     |
  +---------------------------+------------------+------------------+------------------+----------------+
  |        kube_hunter        |     functest     |     security     |      03:32       |      PASS      |
  |     kube_bench_master     |     functest     |     security     |      00:01       |      PASS      |
  |      kube_bench_node      |     functest     |     security     |      00:20       |      PASS      |
  +---------------------------+------------------+------------------+------------------+----------------+

Kubernetes benchmarking suite::

  +--------------------------------+------------------+----------------------+------------------+----------------+
  |           TEST CASE            |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------------------+------------------+----------------------+------------------+----------------+
  |     xrally_kubernetes_full     |     functest     |     benchmarking     |      34:58       |      PASS      |
  +--------------------------------+------------------+----------------------+------------------+----------------+

Kubernetes cnf suite::

  +-------------------------+------------------+--------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +-------------------------+------------------+--------------+------------------+----------------+
  |         k8s_vims        |     functest     |     cnf      |      09:30       |      PASS      |
  |        helm_vims        |     functest     |     cnf      |      08:20       |      PASS      |
  |     cnf_conformance     |     functest     |     cnf      |      02:16       |      PASS      |
  +-------------------------+------------------+--------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html
