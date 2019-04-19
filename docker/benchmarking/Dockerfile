FROM opnfv/functest-core:gambia

ARG BRANCH=stable/gambia
ARG OPENSTACK_TAG=stable/queens
ARG TEMPEST_TAG=3588bb3f5ef546a0ef4d4ad621fd1be381b5fdaf
ARG OSLO_CONCURRENCY=3.27.0
ARG VMTP_TAG=2.4.8

RUN apk --no-cache add --update libxml2 libxslt && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev libxml2-dev libxslt-dev && \
    wget -q -O- https://opendev.org/openstack/requirements/raw/branch/$OPENSTACK_TAG/upper-constraints.txt > upper-constraints.txt && \
    sed -i -E s/^tempest==+.*$/-e\ git+https:\\/\\/opendev.org\\/openstack\\/tempest@$TEMPEST_TAG#egg=tempest/ upper-constraints.txt && \
    sed -i -E s/^oslo.concurrency==+.*$/oslo.concurrency===$OSLO_CONCURRENCY/ upper-constraints.txt && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH > upper-constraints.opnfv.txt && \
    sed -i -E /#egg=functest/d upper-constraints.opnfv.txt && \
    git init /src/vmtp && \
    (cd /src/vmtp && \
        git fetch --tags https://opendev.org/x/vmtp.git $VMTP_TAG && \
        git checkout FETCH_HEAD) && \
    update-requirements -s --source /src/openstack-requirements /src/vmtp/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        /src/vmtp && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/vmtp && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
