FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=master
ARG RALLY_TAG=master
ARG RALLY_OPENSTACK_TAG=master
ARG UJSON_TAG=d25e024f481c5571d15f3c0c406a498ca0467cfd

RUN apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E s/^tempest==+.*$/-e\ git+https:\\/\\/opendev.org\\/openstack\\/tempest#egg=tempest/ upper-constraints.txt && \
    sed -i -E s/^ujson==+.*$/-e\ git+https:\\/\\/github.com\\/esnme\\/ultrajson@$UJSON_TAG#egg=ujson/ upper-constraints.txt && \
    case $(uname -m) in aarch*|arm*) sed -i -E /^PyNaCl=/d upper-constraints.txt ;; esac && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH > upper-constraints.opnfv.txt && \
    sed -i -E /#egg=functest/d upper-constraints.opnfv.txt && \
    git init /src/rally && \
    (cd /src/rally && \
        git fetch --tags https://opendev.org/openstack/rally.git $RALLY_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/rally/ && \
    git init /src/rally-openstack && \
    (cd /src/rally-openstack && \
        git fetch --tags https://opendev.org/openstack/rally-openstack.git $RALLY_OPENSTACK_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/rally-openstack && \
    pip3 install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        tempest /src/rally-openstack && \
    pip3 install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/rally && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/rally /src/rally-openstack && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'" > /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally db create && \
    apk del .build-deps
