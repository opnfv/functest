FROM opnfv/functest-core:euphrates

ARG BRANCH=stable/euphrates
ARG OPENSTACK_TAG=stable/ocata

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --update nodejs nodejs-npm python3 sshpass && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    pip install --no-cache-dir --src /src \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -rthirdparty-requirements.txt && \
    python3 -m pip install --no-cache-dir --src /src \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        doctor-tests && \
    npm -g install npm@latest && \
    (cd /src/promise/source && npm install) && \
    rm -r thirdparty-requirements.txt && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["bash","-c","prepare_env start && run_tests -t all"]
