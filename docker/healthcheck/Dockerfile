FROM opnfv/functest-core:xena

COPY testcases.yaml /usr/lib/python3.9/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
