FROM alpine:3.9

ARG BRANCH=stable/hunter
ARG OPENSTACK_TAG=stable/rocky

RUN apk -U upgrade && \
    apk --no-cache add --update libcurl --repository=http://dl-cdn.alpinelinux.org/alpine/v3.11/main && \
    apk --no-cache add --update \
        python libffi openssl libjpeg-turbo py-pip bash \
        grep sed wget ca-certificates git openssh-client qemu-img iputils coreutils mailcap \
        libstdc++ && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E /^ujson==+.*$/d upper-constraints.txt && \
    sed -i -E /^kubernetes==+.*$/d upper-constraints.txt && \
    case $(uname -m) in aarch*|arm*) sed -i -E /^PyNaCl=/d upper-constraints.txt && apk add --no-cache py-pynacl ;; esac && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH > upper-constraints.opnfv.txt  && \
    sed -i -E /#egg=functest/d upper-constraints.opnfv.txt && \
    sed -i -E /#egg=rally/d upper-constraints.opnfv.txt && \
    sed -i -E /#egg=xrally-kubernetes/d upper-constraints.opnfv.txt && \
    pip install --no-cache-dir --src /src -cupper-constraints.opnfv.txt -cupper-constraints.txt \
        -e git+https://opendev.org/openstack/requirements@$OPENSTACK_TAG#egg=openstack_requirements && \
    git init /src/functest && \
    (cd /src/functest && \
        git fetch --tags https://gerrit.opnfv.org/gerrit/functest $BRANCH && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/functest && \
    pip install --no-cache-dir --src /src -cupper-constraints.opnfv.txt -cupper-constraints.txt \
        /src/functest && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/functest && \
    cp /usr/lib/python2.7/site-packages/functest/ci/logging.ini /usr/lib/python2.7/site-packages/xtesting/ci/ && \
    cp /usr/lib/python2.7/site-packages/functest/ci/logging.debug.ini /usr/lib/python2.7/site-packages/xtesting/ci/ && \
    bash -c "mkdir -p /var/lib/xtesting /home/opnfv" && \
    ln -s /var/lib/xtesting /home/opnfv/functest && \
    bash -c "mkdir -p /home/opnfv/functest{/conf,/data,/images,/results} /home/opnfv/repos/vnfs" && \
    apk del .build-deps
