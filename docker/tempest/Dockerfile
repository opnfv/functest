FROM opnfv/functest-core:gambia

ARG BRANCH=stable/gambia
ARG OPENSTACK_TAG=stable/queens
ARG TEMPEST_TAG=3588bb3f5ef546a0ef4d4ad621fd1be381b5fdaf
ARG OSLO_CONCURRENCY=3.27.0
ARG RALLY_TAG=1.3.0
ARG RALLY_OPENSTACK_TAG=1.2.0

RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E s/^tempest==+.*$/-e\ git+https:\\/\\/opendev.org\\/openstack\\/tempest@$TEMPEST_TAG#egg=tempest/ upper-constraints.txt && \
    sed -i -E s/^oslo.concurrency==+.*$/oslo.concurrency===$OSLO_CONCURRENCY/ upper-constraints.txt && \
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
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        tempest /src/rally-openstack && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/rally && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/rally /src/rally-openstack && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'" > /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally db create && \
    apk del .build-deps
