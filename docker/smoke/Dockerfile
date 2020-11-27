FROM opnfv/functest-core:jerma

ARG REFSTACK_TARGET=2018.11
ARG PATROLE_TAG=0.7.0
ARG NEUTRON_TEMPEST_TAG=0.6.0
ARG CINDER_TEMPEST_TAG=0.3.0
ARG KEYSTONE_TEMPEST_TAG=0.3.0
ARG GLANCE_TAG=stable/train
ARG BARBICAN_TAG=0.3.0
ARG OCTAVIA_TAG=1.2.0
ARG HEAT_TEMPEST_TAG=1.0.0
ARG TELEMETRY_TEMPEST_TAG=1.0.0

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
        git fetch --tags https://opendev.org/openstack/neutron-tempest-plugin.git $NEUTRON_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/neutron-tempest-plugin && \
    git init /src/cinder-tempest-plugin && \
    (cd /src/cinder-tempest-plugin && \
        git fetch --tags https://opendev.org/openstack/cinder-tempest-plugin.git $CINDER_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/cinder-tempest-plugin && \
    git init /src/keystone-tempest-plugin && \
    (cd /src/keystone-tempest-plugin && \
        git fetch --tags https://opendev.org/openstack/keystone-tempest-plugin.git $KEYSTONE_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/keystone-tempest-plugin && \
    git init /src/barbican-tempest-plugin && \
    (cd /src/barbican-tempest-plugin && \
        git fetch --tags https://opendev.org/openstack/barbican-tempest-plugin.git $BARBICAN_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/barbican-tempest-plugin/ && \
    git init /src/octavia-tempest-plugin && \
    (cd /src/octavia-tempest-plugin && \
        git fetch --tags https://opendev.org/openstack/octavia-tempest-plugin.git $OCTAVIA_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/octavia-tempest-plugin && \
    git init /src/heat-tempest-plugin && \
    (cd /src/heat-tempest-plugin && \
        git fetch --tags https://opendev.org/openstack/heat-tempest-plugin.git $HEAT_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/heat-tempest-plugin && \
    git init /src/telemetry-tempest-plugin && \
    (cd /src/telemetry-tempest-plugin && \
        git fetch --tags https://opendev.org/openstack/telemetry-tempest-plugin.git $TELEMETRY_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/requirements /src/telemetry-tempest-plugin && \
    pip3 install --no-cache-dir --src /src -c/src/requirements/upper-constraints.txt \
        -c/src/functest/upper-constraints.txt \
        /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin \
        /src/cinder-tempest-plugin /src/keystone-tempest-plugin \
        /src/octavia-tempest-plugin /src/heat-tempest-plugin /src/telemetry-tempest-plugin && \
    mkdir -p /home/opnfv/functest/data/refstack && \
    mkdir -p /etc/neutron /etc/glance && \
    wget -q -O /etc/glance/policy.json https://opendev.org/openstack/glance/raw/branch/$GLANCE_TAG/etc/policy.json && \
    virtualenv --no-pip --no-setuptools --no-wheel oslo && . oslo/bin/activate && \
    pip3 install --no-cache-dir --src /src -c/src/requirements/upper-constraints.txt \
        -c/src/functest/upper-constraints.txt \
        oslo.policy neutron && \
    oslopolicy-sample-generator  --format json --output-file /etc/neutron/policy.json --namespace neutron && \
    deactivate && \
    rm -r oslo /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin \
        /src/cinder-tempest-plugin /src/keystone-tempest-plugin \
        /src/octavia-tempest-plugin /src/heat-tempest-plugin \
        /src/telemetry-tempest-plugin && \
    apk del .build-deps
COPY compute.txt /home/opnfv/functest/data/refstack/compute.txt
COPY object.txt /home/opnfv/functest/data/refstack/object.txt
COPY platform.txt /home/opnfv/functest/data/refstack/platform.txt
COPY testcases.yaml /usr/lib/python3.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
