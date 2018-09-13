FROM opnfv/functest-core:hunter

ARG BRANCH=stable/hunter
ARG OPENSTACK_TAG=stable/queens
ARG RALLY_TAG=1.1.0
ARG RALLY_OPENSTACK_TAG=1.2.0
ARG OS_FAULTS_TAG=0.1.17

RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    case $OPENSTACK_TAG in \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/git.openstack.org\\/openstack\\/tempest@\\1#egg=tempest/ \
        > upper-constraints.txt && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH | \
        sed -E /#egg=functest/d > upper-constraints.opnfv.txt && \
    git init /src/os-faults && \
    (cd /src/os-faults && \
        git fetch --tags https://git.openstack.org/openstack/os-faults.git $OS_FAULTS_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/os-faults/ && \
    git init /src/rally && \
    (cd /src/rally && \
        git fetch --tags https://git.openstack.org/openstack/rally.git $RALLY_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/rally/ && \
    git init /src/rally-openstack && \
    (cd /src/rally-openstack && \
        git fetch --tags https://git.openstack.org/openstack/rally-openstack.git $RALLY_OPENSTACK_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/rally-openstack && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        tempest /src/rally-openstack /src/os-faults && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/rally && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/os-faults /src/rally /src/rally-openstack && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'" > /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally db create && \
    apk del .build-deps
