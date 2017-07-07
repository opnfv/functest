FROM ollivier/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/ocata

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev git && \
    pip install --src /src \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -rthirdparty-requirements.txt && \
    ln -s /src/tempest /src/refstack-client/.tempest && \
    virtualenv --system-site-packages /src/tempest/.venv && \
    rm thirdparty-requirements.txt && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
