FROM opnfv/functest-benchmarking:iruya

COPY testcases.yaml /usr/lib/python3.6/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
