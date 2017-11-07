FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/pike
ARG ODL_TAG=master
ARG FDS_TAG=master
ARG REFSTACK_TAG=master
ARG VIMS_TAG=stable
ARG TEMPEST_TAG=17.0.0

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --update nodejs nodejs-npm python3 sshpass \
        ruby ruby-bundler ruby-irb ruby-rdoc dnsmasq \
        procps libxslt libxml2 zlib libffi && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev \
        ruby-dev g++ make libxslt-dev libxml2-dev zlib-dev libffi-dev && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest===.*$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@$TEMPEST_RAG#egg=tempest/ \
        > upper-constraints.txt && \
    git clone https://github.com/openstack/refstack-client.git /src/refstack-client && \
    (cd src/refstack-client && git checkout $REFSTACK_TAG) && \
    update-requirements -s --source /src/openstack-requirements /src/refstack-client/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -e/src/refstack-client -rthirdparty-requirements.txt && \
    python3 -m pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        doctor-tests && \
    git clone https://git.opendaylight.org/gerrit/p/integration/test.git /src/odl_test && \
    (cd src/odl_test && git checkout $ODL_TAG) && \
    git clone --depth 1 -b $FDS_TAG https://gerrit.opnfv.org/gerrit/fds /src/fds && \
    git clone --depth 1 -b $VIMS_TAG https://github.com/boucherv-orange/clearwater-live-test /src/vims-test && \
    ln -s /src/tempest /src/refstack-client/.tempest && \
    virtualenv --system-site-packages /src/tempest/.venv && \
    # the next line must be uncommented as soon as promise is synced with pike
    # (cd /src/promise/source && npm install) && \
    (cd /src/vims-test && bundle config build.nokogiri --use-system-libraries && bundle install --system) && \
    npm -g install npm@latest && \
    rm -r upper-constraints.txt thirdparty-requirements.txt /src/refstack-client/.git /src/odl_test/.git \
        /src/fds/.git /src/vims-test/.git && \
    apk del .build-deps
EXPOSE 5000
CMD ["functest_restapi"]
