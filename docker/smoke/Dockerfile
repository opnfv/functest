FROM opnfv/functest-core

ARG PATROLE_TAG=master
ARG NEUTRON_TEMPEST_TAG=master
ARG CINDER_TEMPEST_TAG=master
ARG KEYSTONE_TEMPEST_TAG=master
ARG NEUTRON_TAG=master
ARG GLANCE_TAG=master
ARG NOVA_TAG=master
ARG KEYSTONE_TAG=master
ARG CINDER_TAG=master
ARG BARBICAN_TAG=master
ARG OCTAVIA_TAG=master
ARG HEAT_TEMPEST_TAG=master
ARG TELEMETRY_TEMPEST_TAG=master

RUN apk --no-cache add --update libxml2 libxslt && \
    apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev libxml2-dev libxslt-dev && \
    case $(uname -m) in aarch*|arm*) CFLAGS="-O0" \
        pip3 install --no-cache-dir -c/src/requirements/upper-constraints.txt \
        -c/src/functest/upper-constraints.txt lxml ;; esac && \
    git init /src/patrole && \
    (cd /src/patrole && \
        git fetch --tags https://opendev.org/openstack/patrole.git $PATROLE_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/patrole/ && \
    git init /src/neutron-tempest-plugin && \
    (cd /src/neutron-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/neutron-tempest-plugin.git $NEUTRON_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/neutron-tempest-plugin && \
    git init /src/cinder-tempest-plugin && \
    (cd /src/cinder-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/cinder-tempest-plugin.git $CINDER_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/cinder-tempest-plugin && \
    git init /src/keystone-tempest-plugin && \
    (cd /src/keystone-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/keystone-tempest-plugin.git $KEYSTONE_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/keystone-tempest-plugin && \
    git init /src/barbican-tempest-plugin && \
    (cd /src/barbican-tempest-plugin && \
        git fetch --tags https://opendev.org/openstack/barbican-tempest-plugin.git $BARBICAN_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/barbican-tempest-plugin/ && \
    git init /src/octavia-tempest-plugin && \
    (cd /src/octavia-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/octavia-tempest-plugin.git $OCTAVIA_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/octavia-tempest-plugin && \
    git init /src/heat-tempest-plugin && \
    (cd /src/heat-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/heat-tempest-plugin.git $HEAT_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/heat-tempest-plugin && \
    git init /src/telemetry-tempest-plugin && \
    (cd /src/telemetry-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/telemetry-tempest-plugin.git $TELEMETRY_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/telemetry-tempest-plugin && \
    pip3 install --no-cache-dir --src /src -c/src/requirements/upper-constraints.txt \
        -c/src/functest/upper-constraints.txt \
        /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin \
        /src/cinder-tempest-plugin /src/keystone-tempest-plugin \
        /src/octavia-tempest-plugin /src/heat-tempest-plugin /src/telemetry-tempest-plugin && \
    mkdir -p /home/opnfv/functest/data/refstack && \
    mkdir -p /etc/neutron /etc/glance && \
    virtualenv --no-pip --no-setuptools --no-wheel oslo && . oslo/bin/activate && \
    pip3 install --no-cache-dir --src /src -c/src/requirements/upper-constraints.txt \
        -c/src/functest/upper-constraints.txt \
        oslo.policy -e git+https://opendev.org/openstack/neutron.git@$NEUTRON_TAG#egg=neutron \
        -e git+https://opendev.org/openstack/glance.git@$GLANCE_TAG#egg=glance \
        -e git+https://opendev.org/openstack/nova.git@$NOVA_TAG#egg=nova \
        -e git+https://opendev.org/openstack/keystone.git@$KEYSTONE_TAG#egg=keystone \
        -e git+https://opendev.org/openstack/cinder.git@$CINDER_TAG#egg=cinder && \
    oslopolicy-sample-generator  --format json --output-file /etc/neutron/policy.json --namespace neutron && \
    oslopolicy-sample-generator  --format json --output-file /etc/glance/policy.json --namespace glance && \
    oslopolicy-sample-generator  --format json --output-file /etc/nova/policy.json --namespace nova && \
    oslopolicy-sample-generator  --format json --output-file /etc/keystone/policy.json --namespace keystone && \
    oslopolicy-sample-generator  --format json --output-file /etc/cinder/policy.json --namespace cinder && \
    deactivate && \
    rm -r oslo /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin \
        /src/cinder-tempest-plugin /src/keystone-tempest-plugin \
        /src/octavia-tempest-plugin /src/heat-tempest-plugin \
        /src/telemetry-tempest-plugin /src/neutron /src/glance /src/nova \
        /src/keystone /src/cinder && \
    apk del .build-deps
COPY compute.txt /home/opnfv/functest/data/refstack/compute.txt
COPY object.txt /home/opnfv/functest/data/refstack/object.txt
COPY platform.txt /home/opnfv/functest/data/refstack/platform.txt
COPY testcases.yaml /usr/lib/python3.8/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
