FROM opnfv/functest-benchmarking

COPY testcases.yaml /usr/lib/python3.9/site-packages/xtesting/ci/testcases.yaml
COPY blacklist.yaml /src/functest/functest/opnfv_tests/openstack/rally/blacklist.yaml
CMD ["run_tests", "-t", "all"]
