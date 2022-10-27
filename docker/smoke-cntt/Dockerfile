FROM opnfv/functest-smoke:zed

COPY testcases.yaml /etc/xtesting/testcases.yaml
COPY tempest_conf.yaml /src/functest/functest/opnfv_tests/openstack/tempest/custom_tests/tempest_conf.yaml
CMD ["run_tests", "-t", "all"]
