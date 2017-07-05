FROM ollivier/functest-core

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev git && \
    pip install --src /src \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/ocata \
        -rthirdparty-requirements.txt && \
    ln -s /src/tempest /src/refstack-client/.tempest && \
    virtualenv --system-site-packages /src/tempest/.venv && \
    rm thirdparty-requirements.txt && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
