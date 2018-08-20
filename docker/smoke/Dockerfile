FROM opnfv/functest-tempest

ARG BRANCH=master
ARG OPENSTACK_TAG=master
ARG REFSTACK_TARGET=2018.02
ARG PATROLE_TAG=0.4.0
ARG NEUTRON_TAG=master
ARG BARBICAN_TAG=0.1.0
ARG NEUTRON_RALLY_TAG=master
ARG INTEL_TAG=refs/changes/04/571004/4

RUN apk --no-cache add --update libvirt-dev && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+.*$/-e\ git+https:\\/\\/git.openstack.org\\/openstack\\/tempest#egg=tempest/ \
        > upper-constraints.txt && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH | \
        sed -E /#egg=functest/d > upper-constraints.opnfv.txt && \
    git init /src/patrole && \
    (cd /src/patrole && \
        git fetch --tags https://git.openstack.org/openstack/patrole.git $PATROLE_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/patrole/ && \
    git init /src/neutron-tempest-plugin && \
    (cd /src/neutron-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/neutron-tempest-plugin.git $NEUTRON_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/neutron-tempest-plugin && \
    git init /src/intel-nfv-ci-tests && \
    (cd /src/intel-nfv-ci-tests && \
        git fetch --tags https://git.openstack.org/openstack/intel-nfv-ci-tests $INTEL_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/intel-nfv-ci-tests && \
    git init /src/barbican-tempest-plugin && \
    (cd /src/barbican-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/barbican-tempest-plugin.git $BARBICAN_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/barbican-tempest-plugin/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin /src/intel-nfv-ci-tests \
        networking-bgpvpn networking-sfc && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt \
        /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin /src/intel-nfv-ci-tests && \
    mkdir -p /home/opnfv/functest/data/refstack && \
    wget "https://refstack.openstack.org/api/v1/guidelines/${REFSTACK_TARGET}/tests?target=compute&type=required&alias=true&flag=false" \
        -O /home/opnfv/functest/data/refstack/defcore.txt && \
    mkdir -p /etc/neutron /etc/glance && \
    wget -q -O /etc/neutron/policy.json https://git.openstack.org/cgit/openstack/neutron/plain/etc/policy.json?h=$OPENSTACK_TAG && \
    wget -q -O /etc/glance/policy.json https://git.openstack.org/cgit/openstack/glance/plain/etc/policy.json?h=$OPENSTACK_TAG && \
    git clone --depth 1 -b $NEUTRON_RALLY_TAG https://git.openstack.org/openstack/neutron.git /src/neutron && \
    (cd /src/neutron && git fetch --tags origin $NEUTRON_RALLY_TAG && git checkout FETCH_HEAD) && \
    mkdir -p /home/opnfv/functest/data/rally/neutron && \
    cp -r /src/neutron/rally-jobs /home/opnfv/functest/data/rally/neutron/rally-jobs && \
    rm -r /src/neutron && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
