FROM opnfv/functest-core

COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["bash","-c","run_tests -t all"]
