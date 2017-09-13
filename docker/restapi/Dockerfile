FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/ocata
ARG ODL_TAG=35e415b6873b39d72775c88a337e92dac26012e2
ARG FDS_TAG=master
ARG REFSTACK_TAG=4e187b07672dd1c41cb7c94658f1c91edebf53a2
ARG VIMS_TAG=stable

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --update nodejs nodejs-npm python3 \
        ruby ruby-bundler ruby-irb ruby-rdoc dnsmasq \
        procps libxslt libxml2 zlib libffi && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev \
        ruby-dev g++ make libxslt-dev libxml2-dev zlib-dev libffi-dev && \
    git clone --depth 1 https://github.com/openstack/refstack-client.git /src/refstack-client && \
    (cd src/refstack-client && git checkout -b $REFSTACK_TAG) && \
    update-requirements -s --source /src/openstack-requirements /src/refstack-client/ && \
    pip install --no-cache-dir --src /src \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -e/src/refstack-client -rthirdparty-requirements.txt && \
    git clone --depth 1 https://git.opendaylight.org/gerrit/p/integration/test.git /src/odl_test && \
    (cd src/odl_test && git checkout -b $ODL_TAG) && \
    git clone --depth 1 -b $FDS_TAG https://gerrit.opnfv.org/gerrit/fds /src/fds && \
    git clone --depth 1 -b $VIMS_TAG https://github.com/boucherv-orange/clearwater-live-test /src/vims-test && \
    ln -s /src/tempest /src/refstack-client/.tempest && \
    virtualenv --system-site-packages /src/tempest/.venv && \
    (cd /src/promise/source && npm install) && \
    (cd /src/vims-test && bundle config build.nokogiri --use-system-libraries && bundle install --system) && \
    npm -g install npm@latest && \
    rm -r thirdparty-requirements.txt /src/refstack-client/.git /src/odl_test/.git \
        /src/fds/.git /src/vims-test/.git && \
    apk del .build-deps
EXPOSE 5000
CMD ["functest_restapi"]
