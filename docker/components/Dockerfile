FROM opnfv/functest-core:euphrates

# useless build arg forced by releng/jjb/releng/opnfv-docker.sh
ARG BRANCH=stable/euphrates

COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["bash","-c","prepare_env start && run_tests -t all"]
