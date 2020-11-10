FROM opnfv/functest-tempest:iruya

ARG BRANCH=stable/iruya
ARG OPENSTACK_TAG=stable/stein
ARG TEMPEST_TAG=21.0.0
ARG REFSTACK_TARGET=2018.11
ARG PATROLE_TAG=0.5.0
ARG NEUTRON_TEMPEST_TAG=0.3.0
ARG CINDER_TEMPEST_TAG=0.2.0
ARG KEYSTONE_TEMPEST_TAG=0.2.0
ARG BARBICAN_TAG=0.1.0
ARG OCTAVIA_TAG=1.0.0
ARG HEAT_TEMPEST_TAG=1.0.0
ARG TELEMETRY_TEMPEST_TAG=1.0.0

RUN apk --no-cache add --update libxml2 libxslt && \
    apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev libxml2-dev libxslt-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E /^tempest==+.*$/d upper-constraints.txt && \
    sed -i -E /^ujson==+.*$/d upper-constraints.txt && \
    case $(uname -m) in aarch*|arm*) sed -i -E /^PyNaCl=/d upper-constraints.txt ;; esac && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH > upper-constraints.opnfv.txt && \
    sed -i -E /#egg=functest/d upper-constraints.opnfv.txt && \
    sed -i -E /#egg=rally/d upper-constraints.opnfv.txt && \
    sed -i -E /#egg=xrally-kubernetes/d upper-constraints.opnfv.txt && \
    case $(uname -m) in aarch*|arm*) CFLAGS="-O0" pip3 install --no-cache-dir -cupper-constraints.txt -cupper-constraints.opnfv.txt lxml ;; esac && \
    git init /src/patrole && \
    (cd /src/patrole && \
        git fetch --tags https://opendev.org/openstack/patrole.git $PATROLE_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/patrole/ && \
    git init /src/neutron-tempest-plugin && \
    (cd /src/neutron-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/neutron-tempest-plugin.git $NEUTRON_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/neutron-tempest-plugin && \
    git init /src/cinder-tempest-plugin && \
    (cd /src/cinder-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/cinder-tempest-plugin.git $CINDER_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/cinder-tempest-plugin && \
    git init /src/keystone-tempest-plugin && \
    (cd /src/keystone-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/keystone-tempest-plugin.git $KEYSTONE_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/keystone-tempest-plugin && \
    git init /src/barbican-tempest-plugin && \
    (cd /src/barbican-tempest-plugin && \
        git fetch --tags https://opendev.org/openstack/barbican-tempest-plugin.git $BARBICAN_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/barbican-tempest-plugin/ && \
    git init /src/octavia-tempest-plugin && \
    (cd /src/octavia-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/octavia-tempest-plugin.git $OCTAVIA_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/octavia-tempest-plugin && \
    git init /src/heat-tempest-plugin && \
    (cd /src/heat-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/heat-tempest-plugin.git $HEAT_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/heat-tempest-plugin && \
    git init /src/telemetry-tempest-plugin && \
    (cd /src/telemetry-tempest-plugin && \
        git fetch --tags https://git.openstack.org/openstack/telemetry-tempest-plugin.git $TELEMETRY_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/telemetry-tempest-plugin && \
    pip3 install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin \
        networking-bgpvpn networking-sfc /src/cinder-tempest-plugin \
        /src/keystone-tempest-plugin /src/octavia-tempest-plugin \
        /src/heat-tempest-plugin /src/telemetry-tempest-plugin && \
    mkdir -p /home/opnfv/functest/data/refstack && \
    mkdir -p /etc/neutron /etc/glance && \
    wget -q -O /etc/glance/policy.json https://opendev.org/openstack/glance/raw/branch/$OPENSTACK_TAG/etc/policy.json && \
    virtualenv --no-pip --no-setuptools --no-wheel oslo && . oslo/bin/activate && \
    pip3 install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        oslo.policy neutron && \
    oslopolicy-sample-generator  --format json --output-file /etc/neutron/policy.json --namespace neutron && \
    deactivate && \
    rm -r oslo upper-constraints.txt upper-constraints.opnfv.txt \
        /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin \
        /src/cinder-tempest-plugin /src/keystone-tempest-plugin \
        /src/octavia-tempest-plugin /src/heat-tempest-plugin /src/telemetry-tempest-plugin && \
    apk del .build-deps
COPY compute.txt /home/opnfv/functest/data/refstack/compute.txt
COPY object.txt /home/opnfv/functest/data/refstack/object.txt
COPY platform.txt /home/opnfv/functest/data/refstack/platform.txt
COPY testcases.yaml /usr/lib/python3.6/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
