FROM opnfv/functest-core:euphrates

ARG BRANCH=stable/euphrates
ARG OPENSTACK_TAG=stable/ocata
ARG ODL_TAG=e12ba90cd27577c4c6c70ee54f7d599b5f6777ba
ARG FDS_TAG=stable/euphrates
ARG REFSTACK_TAG=4e187b07672dd1c41cb7c94658f1c91edebf53a2
ARG VIMS_TAG=stable

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --update nodejs nodejs-npm python3 sshpass \
        ruby ruby-bundler ruby-irb ruby-rdoc dnsmasq \
        procps libxslt libxml2 zlib libffi && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev \
        ruby-dev g++ make libxslt-dev libxml2-dev zlib-dev libffi-dev && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ | \
        sed s/^requests===.*$/requests===2.13.0/ \
        > upper-constraints.txt && \
    git clone https://github.com/openstack/refstack-client.git /src/refstack-client && \
    (cd /src/refstack-client && git checkout $REFSTACK_TAG) && \
    update-requirements -s --source /src/openstack-requirements /src/refstack-client/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -e/src/refstack-client -rthirdparty-requirements.txt && \
    python3 -m pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        doctor-tests && \
    git clone https://git.opendaylight.org/gerrit/p/integration/test.git /src/odl_test && \
    (cd /src/odl_test && git checkout $ODL_TAG) && \
    git clone --depth 1 -b $FDS_TAG https://gerrit.opnfv.org/gerrit/fds /src/fds && \
    git clone --depth 1 -b $VIMS_TAG https://github.com/boucherv-orange/clearwater-live-test /src/vims-test && \
    ln -s /src/tempest /src/refstack-client/.tempest && \
    virtualenv --system-site-packages /src/tempest/.venv --python=python2.7 && \
    (cd /src/promise/source && npm install) && \
    (cd /src/vims-test && bundle config build.nokogiri --use-system-libraries && bundle install --system) && \
    npm -g install npm@latest && \
    rm -r upper-constraints.txt thirdparty-requirements.txt /src/refstack-client/.git /src/odl_test/.git \
        /src/fds/.git /src/vims-test/.git && \
    apk del .build-deps
EXPOSE 5000
CMD ["functest_restapi"]
