FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/pike
ARG ODL_TAG=85448c9d97b89989488e675b29b38ac42d8674e4
ARG RALLY_TAG=stable/0.10
ARG OS_FAULTS_TAG=0.1.16
ARG REFSTACK_TAG=a59189eaacda24b787ecb65e6634257beba361ec
ARG REFSTACK_TARGET=2017.09
ARG FDS_TAG=master
ARG VIMS_TAG=stable

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --update python3 sshpass \
        ruby ruby-bundler ruby-irb ruby-rdoc dnsmasq \
        procps libxslt libxml2 zlib libffi go musl-dev && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev \
        ruby-dev g++ make libxslt-dev libxml2-dev zlib-dev libffi-dev && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ \
        > upper-constraints.txt && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -e git+https://github.com/openstack/requirements@$OPENSTACK_TAG#egg=openstack_requirements && \
    git clone --depth 1 https://github.com/openstack/os-faults.git -b $OS_FAULTS_TAG /src/os-faults && \
    update-requirements -s --source /src/openstack-requirements /src/os-faults/ && \
    git clone --depth 1 https://github.com/openstack/rally.git -b $RALLY_TAG /src/rally && \
    update-requirements -s --source /src/openstack-requirements /src/rally/ && \
    git clone https://github.com/openstack/refstack-client.git /src/refstack-client && \
    (cd /src/refstack-client && git checkout $REFSTACK_TAG) && \
    update-requirements -s --source /src/openstack-requirements /src/refstack-client/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        tempest /src/os-faults && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -e/src/refstack-client /src/rally -rthirdparty-requirements.txt && \
    python3 -m pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        doctor-tests && \
    git clone https://git.opendaylight.org/gerrit/p/integration/test.git /src/odl_test && \
    (cd /src/odl_test && git checkout $ODL_TAG) && \
    git clone --depth 1 -b $FDS_TAG https://gerrit.opnfv.org/gerrit/fds /src/fds && \
    git clone --depth 1 -b $VIMS_TAG https://github.com/boucherv-orange/clearwater-live-test /src/vims-test && \
    ln -s /src/tempest /src/refstack-client/.tempest && \
    virtualenv --system-site-packages /src/tempest/.venv --python=python2.7 && \
    git clone https://github.com/RebacaInc/abot_charm.git /src/epc-requirements/abot_charm && \
    python3 -m pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        juju-wait && \
    go get github.com/rogpeppe/godeps && \
    (cd /src/vims-test && bundle config build.nokogiri --use-system-libraries && bundle install --system) && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -e git+https://github.com/openstack/neutron.git@$OPENSTACK_TAG#egg=neutron && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -r /src/neutron/test-requirements.txt && \
    rm -r upper-constraints.txt thirdparty-requirements.txt /src/refstack-client/.git /src/odl_test/.git \
        /src/os-faults /src/rally /src/fds/.git /src/vims-test/.git /src/epc-requirements/abot_charm/.git && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'" > /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally db create && \
    mkdir -p /home/opnfv/functest/data/refstack && \
    wget "https://refstack.openstack.org/api/v1/guidelines/${REFSTACK_TARGET}/tests?target=compute&type=required&alias=true&flag=false" \
        -O /home/opnfv/functest/data/refstack/defcore.txt && \
    cp /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci && \
    apk del .build-deps
EXPOSE 5000
CMD ["functest_restapi"]
