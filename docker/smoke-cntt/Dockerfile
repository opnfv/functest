FROM opnfv/functest-smoke:iruya

COPY testcases.yaml /usr/lib/python3.6/site-packages/xtesting/ci/testcases.yaml
COPY tempest_conf.yaml /usr/lib/python3.6/site-packages/functest/opnfv_tests/openstack/tempest/custom_tests/tempest_conf.yaml
CMD ["run_tests", "-t", "all"]
