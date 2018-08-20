FROM opnfv/functest-tempest

ARG BRANCH=master
ARG OPENSTACK_TAG=master
ARG REFSTACK_TARGET=2018.02
ARG PATROLE_TAG=master
ARG NEUTRON_TAG=master
ARG BARBICAN_TAG=master
ARG INTEL_TAG=refs/changes/04/571004/12

RUN apk --no-cache add --update libvirt-dev && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev libxml2-dev libxslt-dev && \
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
    mkdir -p /home/opnfv/functest/data/refstack && \
    wget "https://refstack.openstack.org/api/v1/guidelines/${REFSTACK_TARGET}/tests?target=compute&type=required&alias=true&flag=false" \
        -O /home/opnfv/functest/data/refstack/defcore.txt && \
    mkdir -p /etc/neutron /etc/cinder /etc/glance /etc/keystone /etc/nova && \
    wget -q -O /etc/glance/policy.json https://git.openstack.org/cgit/openstack/glance/plain/etc/policy.json?h=$OPENSTACK_TAG && \
    virtualenv --no-pip --no-setuptools --no-wheel oslo && . oslo/bin/activate && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        oslo.policy -e git+https://git.openstack.org/openstack/neutron.git@$OPENSTACK_TAG#egg=neutron \
        -e git+https://git.openstack.org/openstack/cinder.git@$OPENSTACK_TAG#egg=cinder \
        -e git+https://git.openstack.org/openstack/keystone.git@$OPENSTACK_TAG#egg=keystone \
        -e git+https://git.openstack.org/openstack/nova.git@$OPENSTACK_TAG#egg=nova && \
    oslopolicy-sample-generator  --format json --output-file /etc/cinder/policy.json --namespace cinder && \
    oslopolicy-sample-generator  --format json --output-file /etc/keystone/policy.json --namespace keystone && \
    oslopolicy-sample-generator  --format json --output-file /etc/neutron/policy.json --namespace neutron && \
    oslopolicy-sample-generator  --format json --output-file /etc/nova/policy.json --namespace nova && \
    deactivate && \
    mkdir -p /home/opnfv/functest/data/rally/neutron && \
    cp -r /src/neutron/rally-jobs /home/opnfv/functest/data/rally/neutron/rally-jobs && \
    rm -r oslo upper-constraints.txt upper-constraints.opnfv.txt \
        /src/neutron /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin \
        /src/intel-nfv-ci-tests && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
