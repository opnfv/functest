FROM opnfv/functest-tempest

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/queens
ARG ODL_TAG=85448c9d97b89989488e675b29b38ac42d8674e4
ARG REFSTACK_TARGET=2017.09
ARG PATROLE_TAG=0.3.0

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ \
        > upper-constraints.txt && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH | \
        sed -E /#egg=functest/d > upper-constraints.opnfv.txt && \
    git clone https://github.com/openstack/patrole.git /src/patrole && \
    (cd /src/patrole && git checkout $PATROLE_TAG) && \
    update-requirements -s --source /src/openstack-requirements /src/patrole/ && \
    git clone --depth 1 https://github.com/openstack/neutron-tempest-plugin.git /src/neutron-tempest-plugin && \
    update-requirements -s --source /src/openstack-requirements /src/neutron-tempest-plugin && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/patrole /src/neutron-tempest-plugin -rthirdparty-requirements.txt && \
    git clone https://git.opendaylight.org/gerrit/p/integration/test.git /src/odl_test && \
    (cd /src/odl_test && git checkout $ODL_TAG) && \
    virtualenv --system-site-packages /src/tempest/.venv && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt thirdparty-requirements.txt /src/odl_test/.git \
        /src/patrole /src/neutron-tempest-plugin && \
    mkdir -p /home/opnfv/functest/data/refstack && \
    wget "https://refstack.openstack.org/api/v1/guidelines/${REFSTACK_TARGET}/tests?target=compute&type=required&alias=true&flag=false" \
        -O /home/opnfv/functest/data/refstack/defcore.txt && \
    mkdir -p /etc/neutron /etc/glance && \
    wget -q -O /etc/neutron/policy.json https://raw.githubusercontent.com/openstack/neutron/$OPENSTACK_TAG/etc/policy.json && \
    wget -q -O /etc/glance/policy.json https://raw.githubusercontent.com/openstack/glance/$OPENSTACK_TAG/etc/policy.json && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
