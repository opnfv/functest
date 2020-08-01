FROM opnfv/functest-core:hunter

ARG BRANCH=stable/hunter
ARG OPENSTACK_TAG=stable/rocky
ARG TEMPEST_TAG=21.0.0
ARG RALLY_TAG=1.5.1
ARG RALLY_OPENSTACK_TAG=1.5.0

COPY Accept-custom-registered-endpoints.patch /tmp/Accept-custom-registered-endpoints.patch
COPY Fixes-race-condition-in-test_add_remove_fixed_ip.patch /tmp/Fixes-race-condition-in-test_add_remove_fixed_ip.patch
COPY object-storage-fix-and-cleanup-header-checks.patch /tmp/object-storage-fix-and-cleanup-header-checks.patch
COPY Create-new-server-in-test_create_backup.patch /tmp/Create-new-server-in-test_create_backup.patch
COPY Switch-to-threading.Thread-for-Rally-tasks.patch /tmp/Switch-to-threading.Thread-for-Rally-tasks.patch
RUN apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E s/^tempest==+.*$/-e\ git+https:\\/\\/opendev.org\\/openstack\\/tempest@$TEMPEST_TAG#egg=tempest/ upper-constraints.txt && \
    sed -i -E /^ujson==+.*$/d upper-constraints.txt && \
    sed -i -E /^kubernetes==+.*$/d upper-constraints.txt && \
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
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        tempest /src/rally-openstack && \
    (cd /src/rally && patch -p1 < /tmp/Switch-to-threading.Thread-for-Rally-tasks.patch) && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/rally && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/rally /src/rally-openstack \
        /tmp/Switch-to-threading.Thread-for-Rally-tasks.patch && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'" > /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally db create && \
    (cd /src/tempest && \
        git config --global user.email "opnfv-tech-discuss@lists.opnfv.org" && \
        git config --global user.name "Functest" && \
        patch -p1 < /tmp/Accept-custom-registered-endpoints.patch && \
        patch -p1 < /tmp/object-storage-fix-and-cleanup-header-checks.patch && \
        patch -p1 < /tmp/Fixes-race-condition-in-test_add_remove_fixed_ip.patch && \
        patch -p1 < /tmp/Create-new-server-in-test_create_backup.patch && \
        git commit -a -m "Backport critical bugfixes" && \
        rm ~/.gitconfig) && \
    rm /tmp/Accept-custom-registered-endpoints.patch \
        /tmp/object-storage-fix-and-cleanup-header-checks.patch \
        /tmp/Fixes-race-condition-in-test_add_remove_fixed_ip.patch \
        /tmp/Create-new-server-in-test_create_backup.patch && \
    apk del .build-deps
