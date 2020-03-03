FROM alpine:3.11

ARG BRANCH=master
ARG OPENSTACK_TAG=master

RUN apk --no-cache add --update \
        python3 libffi openssl libjpeg-turbo py3-pip bash \
        grep sed wget ca-certificates git openssh-client qemu-img iputils mailcap && \
    apk --no-cache add --virtual .build-deps --update \
        python3-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    case $(uname -m) in aarch*|arm*) sed -i -E /^PyNaCl=/d upper-constraints.txt && apk add --no-cache py3-pynacl ;; esac && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH > upper-constraints.opnfv.txt  && \
    sed -i -E /#egg=functest/d upper-constraints.opnfv.txt && \
    sed -i -E /^tempest==+.*$/d upper-constraints.txt && \
    sed -i -E s/^ujson==+.*$/-e\ git+https:\\/\\/github.com\\/esnme\\/ultrajson@$UJSON_TAG#egg=ujson/ upper-constraints.txt && \
    pip3 install --no-cache-dir --src /src -cupper-constraints.opnfv.txt -cupper-constraints.txt \
        -e git+https://opendev.org/openstack/requirements@$OPENSTACK_TAG#egg=openstack_requirements && \
    git init /src/functest && \
    (cd /src/functest && \
        git fetch --tags https://gerrit.opnfv.org/gerrit/functest $BRANCH && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/functest && \
    pip3 install --no-cache-dir --src /src -cupper-constraints.opnfv.txt -cupper-constraints.txt \
        /src/functest && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/functest && \
    cp /usr/lib/python3.8/site-packages/functest/ci/logging.ini /usr/lib/python3.8/site-packages/xtesting/ci/ && \
    cp /usr/lib/python3.8/site-packages/functest/ci/logging.debug.ini /usr/lib/python3.8/site-packages/xtesting/ci/ && \
    bash -c "mkdir -p /var/lib/xtesting /home/opnfv" && \
    ln -s /var/lib/xtesting /home/opnfv/functest && \
    bash -c "mkdir -p /home/opnfv/functest{/conf,/data,/images,/results} /home/opnfv/repos/vnfs" && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'\n" > /etc/rally/rally.conf && \
    printf "\n[openstack]\nneutron_bind_l2_agent_types = Open vSwitch agent,Linux bridge agent,OVN Controller Gateway agent\n" >> /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally db create && \
    apk del .build-deps
