FROM alpine:3.5

RUN apk --no-cache add --update \
        python libffi libssl1.0 libjpeg-turbo py-pip bash && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev git && \
    pip install \
        -chttps://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=stable/ocata \
        git+https://gerrit.opnfv.org/gerrit/releng#egg=opnfv\&subdirectory=modules \
        git+https://gerrit.opnfv.org/gerrit/snaps#egg=snaps \
        git+https://gerrit.opnfv.org/gerrit/functest#egg=functest && \
    bash -c "mkdir -p /home/opnfv/functest{/conf,/data,/images,/results} /home/opnfv/repos/vnfs" && \
    apk del .build-deps
