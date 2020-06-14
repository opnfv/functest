FROM opnfv/functest-smoke:jerma

COPY testcases.yaml /usr/lib/python3.7/site-packages/xtesting/ci/testcases.yaml
COPY tempest_conf.yaml /src/functest/functest/opnfv_tests/openstack/tempest/custom_tests/tempest_conf.yaml
CMD ["run_tests", "-t", "all"]
