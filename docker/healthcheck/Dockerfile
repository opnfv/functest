FROM opnfv/functest-core

ARG ODL_TAG=85448c9d97b89989488e675b29b38ac42d8674e4

RUN git clone https://git.opendaylight.org/gerrit/p/integration/test.git /src/odl_test && \
    (cd /src/odl_test && git checkout $ODL_TAG) && \
    rm -r /src/odl_test/.git

COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
