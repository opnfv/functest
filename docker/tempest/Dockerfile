FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/queens
ARG RALLY_TAG=0.11.2
ARG OS_FAULTS_TAG=0.1.17

RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    case $OPENSTACK_TAG in \
    master) \
        wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
            sed -E s/^tempest==+.*$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest#egg=tempest/ \
            > upper-constraints.txt ;; \
    *) \
        wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
            sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ \
            > upper-constraints.txt ;; \
    esac && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH | \
        sed -E /#egg=functest/d > upper-constraints.opnfv.txt && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        -e git+https://github.com/openstack/requirements@$OPENSTACK_TAG#egg=openstack_requirements && \
    git clone https://github.com/openstack/os-faults.git /src/os-faults && \
    (cd /src/os-faults && git checkout $OS_FAULTS_TAG) && \
    update-requirements -s --source /src/openstack-requirements /src/os-faults/ && \
    git clone https://github.com/openstack/rally.git /src/rally && \
    (cd /src/rally && git checkout $RALLY_TAG) && \
    update-requirements -s --source /src/openstack-requirements /src/rally/ && \
    git clone --depth 1 https://github.com/openstack/rally-openstack.git /src/rally-openstack && \
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
