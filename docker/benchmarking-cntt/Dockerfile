FROM opnfv/functest-benchmarking

COPY testcases.yaml /etc/xtesting/testcases.yaml
COPY blacklist.yaml /src/functest/functest/opnfv_tests/openstack/rally/blacklist.yaml
CMD ["run_tests", "-t", "all"]
