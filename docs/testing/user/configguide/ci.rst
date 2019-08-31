.. SPDX-License-Identifier: CC-BY-4.0

Integration in CI
=================
In CI we use the Docker images and execute the appropriate commands within the
container from Jenkins.

4 steps have been defined::
  * functest-cleanup: clean existing functest dockers on the jumphost
  * functest-daily: run dockers opnfv/functest-* (healthcheck, smoke,
    benchmarking, vnf)
  * functest-store-results: push logs to artifacts

See `[1]`_ for details.

.. _`[1]`: https://github.com/opnfv/releng/blob/master/jjb/functest/functest-daily-jobs.yaml
