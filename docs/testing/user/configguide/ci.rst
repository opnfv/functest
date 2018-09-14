.. SPDX-License-Identifier: CC-BY-4.0

Integration in CI
=================
In CI we use the Docker images and execute the appropriate commands within the
container from Jenkins.

4 steps have been defined::
  * functest-cleanup: clean existing functest dockers on the jumphost
  * functest-daily: run dockers opnfv/functest-* (healthcheck, smoke, features,
    vnf)
  * functest-store-results: push logs to artifacts

See `[2]`_ for details.

.. _`[2]`: https://git.opnfv.org/releng/tree/jjb/functest/functest-daily-jobs.yaml
