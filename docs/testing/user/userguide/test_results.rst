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
  |      tenantnetwork2      |     functest     |     healthcheck     |      00:07       |      PASS      |
  |         vmready1         |     functest     |     healthcheck     |      00:09       |      PASS      |
  |         vmready2         |     functest     |     healthcheck     |      00:09       |      PASS      |
  |        singlevm1         |     functest     |     healthcheck     |      00:30       |      PASS      |
  |        singlevm2         |     functest     |     healthcheck     |      00:33       |      PASS      |
  |        vping_ssh         |     functest     |     healthcheck     |      00:42       |      PASS      |
  |      vping_userdata      |     functest     |     healthcheck     |      00:38       |      PASS      |
  |       cinder_test        |     functest     |     healthcheck     |      01:06       |      PASS      |
  |      tempest_smoke       |     functest     |     healthcheck     |      04:03       |      PASS      |
  |           odl            |     functest     |     healthcheck     |      00:00       |      SKIP      |
  +--------------------------+------------------+---------------------+------------------+----------------+

Smoke suite::

  +------------------------------------+------------------+---------------+------------------+----------------+
  |             TEST CASE              |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +------------------------------------+------------------+---------------+------------------+----------------+
  |     neutron-tempest-plugin-api     |     functest     |     smoke     |      09:26       |      PASS      |
  |            rally_sanity            |     functest     |     smoke     |      16:43       |      PASS      |
  |          refstack_compute          |     functest     |     smoke     |      06:48       |      PASS      |
  |          refstack_object           |     functest     |     smoke     |      02:04       |      PASS      |
  |         refstack_platform          |     functest     |     smoke     |      07:53       |      PASS      |
  |            tempest_full            |     functest     |     smoke     |      31:51       |      PASS      |
  |          tempest_scenario          |     functest     |     smoke     |      09:38       |      PASS      |
  |            tempest_slow            |     functest     |     smoke     |      22:21       |      PASS      |
  |              patrole               |     functest     |     smoke     |      02:32       |      PASS      |
  |              barbican              |     functest     |     smoke     |      02:16       |      PASS      |
  |           neutron_trunk            |     functest     |     smoke     |      00:00       |      SKIP      |
  |         networking-bgpvpn          |     functest     |     smoke     |      00:00       |      SKIP      |
  |           networking-sfc           |     functest     |     smoke     |      00:00       |      SKIP      |
  +------------------------------------+------------------+---------------+------------------+----------------+

Benchmarking suite::

  +--------------------+------------------+----------------------+------------------+----------------+
  |     TEST CASE      |     PROJECT      |         TIER         |     DURATION     |     RESULT     |
  +--------------------+------------------+----------------------+------------------+----------------+
  |     rally_full     |     functest     |     benchmarking     |      92:16       |      PASS      |
  |     rally_jobs     |     functest     |     benchmarking     |      17:31       |      PASS      |
  |        vmtp        |     functest     |     benchmarking     |      15:20       |      PASS      |
  |       shaker       |     functest     |     benchmarking     |      22:44       |      PASS      |
  +--------------------+------------------+----------------------+------------------+----------------+

Vnf suite::

  +----------------------+------------------+--------------+------------------+----------------+
  |      TEST CASE       |     PROJECT      |     TIER     |     DURATION     |     RESULT     |
  +----------------------+------------------+--------------+------------------+----------------+
  |       cloudify       |     functest     |     vnf      |      03:35       |      PASS      |
  |     cloudify_ims     |     functest     |     vnf      |      23:26       |      PASS      |
  |       heat_ims       |     functest     |     vnf      |      34:22       |      PASS      |
  |     vyos_vrouter     |     functest     |     vnf      |      13:49       |      PASS      |
  |       juju_epc       |     functest     |     vnf      |      41:49       |      PASS      |
  +----------------------+------------------+--------------+------------------+----------------+

Kubernetes healthcheck suite::

  +-------------------+------------------+---------------------+------------------+----------------+
  |     TEST CASE     |     PROJECT      |         TIER        |     DURATION     |     RESULT     |
  +-------------------+------------------+---------------------+------------------+----------------+
  |     k8s_smoke     |     functest     |     healthcheck     |      01:15       |      PASS      |
  +-------------------+------------------+---------------------+------------------+----------------+

Kubernetes smoke suite::

  +-------------------------+------------------+---------------+------------------+----------------+
  |        TEST CASE        |     PROJECT      |      TIER     |     DURATION     |     RESULT     |
  +-------------------------+------------------+---------------+------------------+----------------+
  |     k8s_conformance     |     functest     |     smoke     |      135:54      |      PASS      |
  +-------------------------+------------------+---------------+------------------+----------------+

Results are automatically pushed to the test results database, some additional
result files are pushed to OPNFV artifact web sites.

Based on the results stored in the result database, a `Functest reporting`_
portal is also automatically updated. This portal provides information on the
overall status per scenario and per installer

.. _`Functest reporting`: http://testresults.opnfv.org/reporting/master/functest/status-apex.html