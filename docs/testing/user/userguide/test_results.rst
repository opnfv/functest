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
  |      tenantnetwork2      |     functest     |     healthcheck     |      00:06       |      PASS      |
  |         vmready1         |     functest     |     healthcheck     |      00:06       |      PASS      |
  |         vmready2         |     functest     |     healthcheck     |      00:08       |      PASS      |
  |        singlevm1         |     functest     |     healthcheck     |      00:28       |      PASS      |
  |        singlevm2         |     functest     |     healthcheck     |      00:25       |      PASS      |
  |        vping_ssh         |     functest     |     healthcheck     |      00:36       |      PASS      |
  |      vping_userdata      |     functest     |     healthcheck     |      00:34       |      PASS      |
  |       cinder_test        |     functest     |     healthcheck     |      01:03       |      PASS      |
  |      tempest_smoke       |     functest     |     healthcheck     |      05:13       |      PASS      |
  |           odl            |     functest     |     healthcheck     |      00:00       |      SKIP      |
  +--------------------------+------------------+---------------------+------------------+----------------+

Smoke suite::

  +------------------------------------+------------------+---------------+------------------+----------------+
  |             TEST CASE              |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +------------------------------------+------------------+---------------+------------------+----------------+
  |     neutron-tempest-plugin-api     |     functest     |     smoke     |      09:12       |      PASS      |
  |            rally_sanity            |     functest     |     smoke     |      16:29       |      PASS      |
  |          refstack_compute          |     functest     |     smoke     |      06:25       |      PASS      |
  |          refstack_object           |     functest     |     smoke     |      01:54       |      PASS      |
  |         refstack_platform          |     functest     |     smoke     |      06:52       |      PASS      |
  |            tempest_full            |     functest     |     smoke     |      30:26       |      PASS      |
  |          tempest_scenario          |     functest     |     smoke     |      09:23       |      PASS      |
  |            tempest_slow            |     functest     |     smoke     |      24:42       |      PASS      |
  |              patrole               |     functest     |     smoke     |      02:36       |      PASS      |
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
  |     rally_full     |     functest     |     benchmarking     |      92:16       |      PASS      |
  |     rally_jobs     |     functest     |     benchmarking     |      18:49       |      PASS      |
  |        vmtp        |     functest     |     benchmarking     |      15:28       |      PASS      |
  |       shaker       |     functest     |     benchmarking     |      24:04       |      PASS      |
  +--------------------+------------------+----------------------+------------------+----------------+

Vnf suite::

  +----------------------+------------------+--------------+------------------+----------------+
  |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +----------------------+------------------+--------------+------------------+----------------+
  |       cloudify       |     functest     |     vnf      |      03:49       |      PASS      |
  |     cloudify_ims     |     functest     |     vnf      |      24:20       |      PASS      |
  |       heat_ims       |     functest     |     vnf      |      32:13       |      PASS      |
  |     vyos_vrouter     |     functest     |     vnf      |      14:55       |      PASS      |
  |       juju_epc       |     functest     |     vnf      |      41:24       |      PASS      |
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
  |     xrally_kubernetes     |     functest     |     smoke     |      22:04       |      PASS      |
  |      k8s_conformance      |     functest     |     smoke     |      173:48      |      PASS      |
  +---------------------------+------------------+---------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html
