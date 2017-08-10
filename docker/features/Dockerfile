FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/ocata

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev git && \
    pip install --no-cache-dir --src /src \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -rthirdparty-requirements.txt && \
    git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/domino /src/domino && \
    git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/copper /src/copper && \
    rm -r thirdparty-requirements.txt /src/domino/.git /src/copper/.git && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["bash","-c","prepare_env start && run_tests -t all"]
