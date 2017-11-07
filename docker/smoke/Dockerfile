FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/pike
ARG ODL_TAG=master
ARG FDS_TAG=master
ARG REFSTACK_TAG=master

RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev git && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ \
        > upper-constraints.txt && \
    git clone https://github.com/openstack/refstack-client.git /src/refstack-client && \
    (cd src/refstack-client && git checkout $REFSTACK_TAG) && \
    update-requirements -s --source /src/openstack-requirements /src/refstack-client/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -e/src/refstack-client && \
    git clone https://git.opendaylight.org/gerrit/p/integration/test.git /src/odl_test && \
    (cd src/odl_test && git checkout $ODL_TAG) && \
    git clone --depth 1 -b $FDS_TAG https://gerrit.opnfv.org/gerrit/fds /src/fds && \
    ln -s /src/tempest /src/refstack-client/.tempest && \
    virtualenv --system-site-packages /src/tempest/.venv && \
    rm -r upper-constraints.txt /src/refstack-client/.git /src/odl_test/.git /src/fds/.git && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["bash","-c","prepare_env start && run_tests -t all"]
