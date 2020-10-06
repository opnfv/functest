FROM alpine:3.12

ARG BRANCH=stable/leguer
ARG OPENSTACK_TAG=stable/victoria

COPY Switch-to-threading.Thread-for-Rally-tasks.patch /tmp/Switch-to-threading.Thread-for-Rally-tasks.patch
COPY Create-new-server-in-test_create_backup.patch /tmp/Create-new-server-in-test_create_backup.patch
RUN apk --no-cache add --update \
        python3 py3-wheel libffi openssl libjpeg-turbo py3-pip bash \
        grep sed wget ca-certificates git openssh-client qemu-img iputils coreutils mailcap libstdc++ && \
    apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    apk --no-cache add --update py3-distlib\>=0.3.1 \
        --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main && \
    git init /src/requirements && \
    (cd /src/requirements && \
        git fetch --tags https://review.opendev.org/openstack/requirements $OPENSTACK_TAG && \
        git checkout FETCH_HEAD) && \
    git init /src/functest && \
    (cd /src/functest && \
        git fetch --tags https://gerrit.opnfv.org/gerrit/functest $BRANCH && \
        git checkout FETCH_HEAD) && \
    sed -i -E /^tempest==+.*$/d /src/requirements/upper-constraints.txt && \
    case $(uname -m) in aarch*|arm*) sed -i -E /^PyNaCl=/d /src/requirements/upper-constraints.txt && apk add --no-cache py3-pynacl ;; esac && \
    sed -i -E /#egg=functest/d /src/functest/upper-constraints.txt && \
    pip3 install --no-cache-dir --src /src -c/src/functest/upper-constraints.txt -c/src/requirements/upper-constraints.txt \
        -e /src/requirements && \
    update-requirements -s --source /src/requirements /src/functest && \
    pip3 install --no-cache-dir --src /src -c/src/functest/upper-constraints.txt -c/src/requirements/upper-constraints.txt \
        -e /src/functest && \
    (cd /src/rally && patch -p1 < /tmp/Switch-to-threading.Thread-for-Rally-tasks.patch) && \
    sed -i -E /#egg=rally/d /src/functest/upper-constraints.txt && \
    sed -i -E /#egg=tempest/d /src/functest/upper-constraints.txt && \
    (cd /src/tempest && \
        git config --global user.email "opnfv-tech-discuss@lists.opnfv.org" && \
        git config --global user.name "Functest" && \
        patch -p1 < /tmp/Create-new-server-in-test_create_backup.patch && \
        git commit -a -m "Backport critical bugfixes" && \
        rm ~/.gitconfig) && \
    rm -r /src/requirements/.git /src/functest/.git \
        /tmp/Switch-to-threading.Thread-for-Rally-tasks.patch \
        /tmp/Create-new-server-in-test_create_backup.patch && \
    cp /src/functest/functest/ci/logging.ini /usr/lib/python3.8/site-packages/xtesting/ci/ && \
    cp /src/functest/functest/ci/logging.debug.ini /usr/lib/python3.8/site-packages/xtesting/ci/ && \
    bash -c "mkdir -p /var/lib/xtesting /home/opnfv" && \
    ln -s /var/lib/xtesting /home/opnfv/functest && \
    bash -c "mkdir -p /home/opnfv/functest{/conf,/data,/images,/results} /home/opnfv/repos/vnfs" && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'\n" > /etc/rally/rally.conf && \
    printf "\n[openstack]\nneutron_bind_l2_agent_types = Open vSwitch agent,Linux bridge agent,OVN Controller Gateway agent\n" >> /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally db create && \
    apk del .build-deps
