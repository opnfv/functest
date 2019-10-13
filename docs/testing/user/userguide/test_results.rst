.. SPDX-License-Identifier: CC-BY-4.0

Test results
============

Manual testing
--------------

In manual mode test results are displayed in the console and result files
are put in /home/opnfv/functest/results.

If you want additional logs, you may configure the logging.ini under
/usr/lib/python3.6/site-packages/xtesting/ci.

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
  |      tenantnetwork1      |     functest     |     healthcheck     |      00:06       |      PASS      |
  |      tenantnetwork2      |     functest     |     healthcheck     |      00:08       |      PASS      |
  |         vmready1         |     functest     |     healthcheck     |      00:08       |      PASS      |
  |         vmready2         |     functest     |     healthcheck     |      00:10       |      PASS      |
  |        singlevm1         |     functest     |     healthcheck     |      00:31       |      PASS      |
  |        singlevm2         |     functest     |     healthcheck     |      00:29       |      PASS      |
  |        vping_ssh         |     functest     |     healthcheck     |      00:37       |      PASS      |
  |      vping_userdata      |     functest     |     healthcheck     |      00:36       |      PASS      |
  |       cinder_test        |     functest     |     healthcheck     |      01:05       |      PASS      |
  |      tempest_smoke       |     functest     |     healthcheck     |      04:58       |      PASS      |
  |           odl            |     functest     |     healthcheck     |      00:00       |      SKIP      |
  +--------------------------+------------------+---------------------+------------------+----------------+

Smoke suite::

  +------------------------------------+------------------+---------------+------------------+----------------+
  |             TEST CASE              |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +------------------------------------+------------------+---------------+------------------+----------------+
  |     neutron-tempest-plugin-api     |     functest     |     smoke     |      10:35       |      PASS      |
  |            rally_sanity            |     functest     |     smoke     |      17:11       |      PASS      |
  |          refstack_compute          |     functest     |     smoke     |      06:09       |      PASS      |
  |          refstack_object           |     functest     |     smoke     |      01:48       |      PASS      |
  |         refstack_platform          |     functest     |     smoke     |      05:53       |      PASS      |
  |            tempest_full            |     functest     |     smoke     |      30:02       |      PASS      |
  |          tempest_scenario          |     functest     |     smoke     |      09:26       |      PASS      |
  |            tempest_slow            |     functest     |     smoke     |      18:53       |      PASS      |
  |              patrole               |     functest     |     smoke     |      02:28       |      PASS      |
  |              barbican              |     functest     |     smoke     |      02:13       |      PASS      |
  |           neutron_trunk            |     functest     |     smoke     |      00:00       |      SKIP      |
  |         networking-bgpvpn          |     functest     |     smoke     |      00:00       |      SKIP      |
  |           networking-sfc           |     functest     |     smoke     |      00:00       |      SKIP      |
  |              octavia               |     functest     |     smoke     |      00:00       |      SKIP      |
  +------------------------------------+------------------+---------------+------------------+----------------+

Benchmarking suite::

  +--------------------+------------------+----------------------+------------------+----------------+
  |     TEST CASE      |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------+------------------+----------------------+------------------+----------------+
  |     rally_full     |     functest     |     benchmarking     |      92:42       |      PASS      |
  |     rally_jobs     |     functest     |     benchmarking     |      18:44       |      PASS      |
  |        vmtp        |     functest     |     benchmarking     |      15:20       |      PASS      |
  |       shaker       |     functest     |     benchmarking     |      23:54       |      PASS      |
  +--------------------+------------------+----------------------+------------------+----------------+

Vnf suite::

  +----------------------+------------------+--------------+------------------+----------------+
  |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +----------------------+------------------+--------------+------------------+----------------+
  |       cloudify       |     functest     |     vnf      |      03:50       |      PASS      |
  |     cloudify_ims     |     functest     |     vnf      |      22:34       |      PASS      |
  |       heat_ims       |     functest     |     vnf      |      32:39       |      PASS      |
  |     vyos_vrouter     |     functest     |     vnf      |      15:10       |      PASS      |
  |       juju_epc       |     functest     |     vnf      |      37:03       |      PASS      |
  +----------------------+------------------+--------------+------------------+----------------+

Kubernetes healthcheck suite::

  +-------------------+------------------+---------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +-------------------+------------------+---------------------+------------------+----------------+
  |     k8s_smoke     |     functest     |     healthcheck     |      01:44       |      PASS      |
  +-------------------+------------------+---------------------+------------------+----------------+

Kubernetes smoke suite::

  +---------------------------+------------------+---------------+------------------+----------------+
  |         TEST CASE         |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +---------------------------+------------------+---------------+------------------+----------------+
  |     xrally_kubernetes     |     functest     |     smoke     |      16:12       |      PASS      |
  |      k8s_conformance      |     functest     |     smoke     |      149:59      |      PASS      |
  +---------------------------+------------------+---------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html
