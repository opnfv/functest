FROM opnfv/functest-smoke:hunter

COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
COPY tempest_conf.yaml /usr/lib/python2.7/site-packages/functest/opnfv_tests/openstack/tempest/custom_tests/tempest_conf.yaml
CMD ["run_tests", "-t", "all"]
