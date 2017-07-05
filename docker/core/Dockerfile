FROM alpine:3.5

RUN apk --no-cache add --update \
        python libffi libssl1.0 libjpeg-turbo py-pip bash \
        grep sed wget ca-certificates && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev git && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/ocata | \
        sed s/^tempest===.*$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@14.0.0#egg=tempest/ \
        > upper-constraints.txt && \
    pip install --src /src -cupper-constraints.txt \
        git+https://gerrit.opnfv.org/gerrit/releng#egg=opnfv\&subdirectory=modules \
        git+https://gerrit.opnfv.org/gerrit/snaps#egg=snaps \
        git+https://gerrit.opnfv.org/gerrit/functest#egg=functest && \
    rm upper-constraints.txt && \
    bash -c "mkdir -p /home/opnfv/functest{/conf,/data,/images,/results} /home/opnfv/repos/vnfs" && \
    apk del .build-deps
