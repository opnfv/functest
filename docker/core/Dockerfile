FROM alpine:3.7

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/queens
ARG PIP_TAG=18.0

RUN apk --no-cache add --update \
        python libffi libssl1.0 libjpeg-turbo py-pip bash \
        grep sed wget ca-certificates git openssh-client qemu-img && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH | \
        sed -E /#egg=functest/d > upper-constraints.txt && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG \
        pip==$PIP_TAG && \
    git clone --depth 1 https://gerrit.opnfv.org/gerrit/functest /src/functest && \
    (cd /src/functest && git fetch --tags origin $BRANCH && git checkout FETCH_HEAD) && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG \
        /src/functest && \
    rm -r upper-constraints.txt /src/functest && \
    cp /usr/lib/python2.7/site-packages/functest/ci/logging.ini /usr/lib/python2.7/site-packages/xtesting/ci/ && \
    bash -c "mkdir -p /var/lib/xtesting /home/opnfv" && \
    ln -s /var/lib/xtesting /home/opnfv/functest && \
    bash -c "mkdir -p /home/opnfv/functest{/conf,/data,/images,/results} /home/opnfv/repos/vnfs" && \
    apk del .build-deps
