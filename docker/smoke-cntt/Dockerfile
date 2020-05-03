FROM opnfv/functest-smoke:kali

COPY testcases.yaml /usr/lib/python3.8/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
