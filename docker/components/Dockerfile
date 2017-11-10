FROM opnfv/functest-core

# useless build arg forced by releng/jjb/releng/opnfv-docker.sh
ARG BRANCH=master

COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["bash","-c","prepare_env start && run_tests -t all"]
