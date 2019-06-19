FROM opnfv/functest-tempest:hunter

ARG BRANCH=stable/hunter
ARG OPENSTACK_TAG=stable/rocky
ARG TEMPEST_TAG=e8088d1218eba0b8e4ed59fa5ca30ac9b664b7fb
ARG REFSTACK_TARGET=2018.11
ARG PATROLE_TAG=0.4.0
ARG NEUTRON_TEMPEST_TAG=0.3.0
ARG BARBICAN_TAG=0.1.0

RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E s/^tempest==+.*$/-e\ git+https:\\/\\/opendev.org\\/openstack\\/tempest@$TEMPEST_TAG#egg=tempest/ upper-constraints.txt && \
    case $(uname -m) in aarch*|arm*) sed -i -E /^PyNaCl=/d upper-constraints.txt ;; esac && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH > upper-constraints.opnfv.txt && \
    sed -i -E /#egg=functest/d upper-constraints.opnfv.txt && \
    git init /src/patrole && \
    (cd /src/patrole && \
        git fetch --tags https://opendev.org/openstack/patrole.git $PATROLE_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/patrole/ && \
    git init /src/neutron-tempest-plugin && \
    (cd /src/neutron-tempest-plugin && \
        git fetch --tags https://opendev.org/openstack/neutron-tempest-plugin.git $NEUTRON_TEMPEST_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/neutron-tempest-plugin && \
    git init /src/barbican-tempest-plugin && \
    (cd /src/barbican-tempest-plugin && \
        git fetch --tags https://opendev.org/openstack/barbican-tempest-plugin.git $BARBICAN_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/barbican-tempest-plugin/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin \
        networking-bgpvpn networking-sfc && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt \
        /src/patrole /src/barbican-tempest-plugin /src/neutron-tempest-plugin && \
    mkdir -p /home/opnfv/functest/data/refstack && \
    mkdir -p /etc/neutron /etc/glance && \
    wget -q -O /etc/neutron/policy.json https://opendev.org/openstack/neutron/raw/branch/$OPENSTACK_TAG/etc/policy.json && \
    wget -q -O /etc/glance/policy.json https://opendev.org/openstack/glance/raw/branch/$OPENSTACK_TAG/etc/policy.json && \
    apk del .build-deps
COPY defcore.txt /home/opnfv/functest/data/refstack/defcore.txt
COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
