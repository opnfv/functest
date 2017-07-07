FROM alpine:3.5

COPY upper-constraints.txt upper-constraints.txt
RUN apk --no-cache add --update \
        python libffi libssl1.0 libjpeg-turbo py-pip bash shadow \
        grep sed wget ca-certificates && \
    chsh -s /bin/bash root && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev git && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/ocata | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ \
        > o-upper-constraints.txt && \
    pip install --src /src -cupper-constraints.txt -co-upper-constraints.txt \
        git+https://gerrit.opnfv.org/gerrit/functest#egg=functest && \
    rm upper-constraints.txt o-upper-constraints.txt && \
    bash -c "mkdir -p /home/opnfv/functest{/conf,/data,/images,/results} /home/opnfv/repos/vnfs" && \
    apk del .build-deps
