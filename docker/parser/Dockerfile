FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/pike
ARG RALLY_TAG=stable/0.10
ARG OS_FAULTS_TAG=0.1.16

RUN apk --no-cache add --update \
        python libffi libssl1.0 libjpeg-turbo py-pip bash \
        grep sed wget ca-certificates git openssh-client && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ | \
        > upper-constraints.txt && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        git+https://gerrit.opnfv.org/gerrit/parser#egg=nfv-heattranslator\&subdirectory=tosca2heat/heat-translator \
        git+https://gerrit.opnfv.org/gerrit/parser#egg=nfv-toscaparser\&subdirectory=tosca2heat/tosca-parser \
        -e git+https://gerrit.opnfv.org/gerrit/parser#egg=nfv-parser && \
    rm upper-constraints.txt && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["bash","-c","prepare_env start && run_tests -t all"]
