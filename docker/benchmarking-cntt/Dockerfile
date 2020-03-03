FROM opnfv/functest-benchmarking:jerma

COPY testcases.yaml /usr/lib/python3.7/site-packages/xtesting/ci/testcases.yaml
COPY blacklist.yaml /usr/lib/python3.7/site-packages/functest/opnfv_tests/openstack/rally/blacklist.yaml
CMD ["run_tests", "-t", "all"]
