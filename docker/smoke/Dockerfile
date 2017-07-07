FROM ollivier/functest-core

COPY thirdparty-requirements.txt thirdparty-requirements.txt
COPY upper-constraints.txt upper-constraints.txt
RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev git && \
    pip install --src /src -cupper-constraints.txt \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/ocata \
        -rthirdparty-requirements.txt && \
    ln -s /src/tempest /src/refstack-client/.tempest && \
    virtualenv --system-site-packages /src/tempest/.venv && \
    rm thirdparty-requirements.txt upper-constraints.txt && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
