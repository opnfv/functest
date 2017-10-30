FROM alpine:3.6

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/pike
ARG RALLY_TAG=stable/0.10
ARG OS_FAULTS_TAG=0.1.16
ARG TEMPEST_TAG=17.0.0

RUN apk --no-cache add --update \
        python libffi libssl1.0 libjpeg-turbo py-pip bash \
        grep sed wget ca-certificates git openssh-client && \
    apk --no-cache add --virtual .build-deps --update \
        python-dev build-base linux-headers libffi-dev \
        openssl-dev libjpeg-turbo-dev && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed /^heat-translator=/d | sed /^tosca-parser=/d | \
        sed -E s/^tempest===.*$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@$TEMPEST_TAG#egg=tempest/ | \
        sed s/^requests===.*$/requests===2.13.0/ \
        > upper-constraints.txt && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        -e git+https://github.com/openstack/requirements@$OPENSTACK_TAG#egg=openstack_requirements && \
    git clone --depth 1 https://github.com/openstack/os-faults.git -b $OS_FAULTS_TAG /src/os-faults && \
    update-requirements -s --source /src/openstack-requirements /src/os-faults/ && \
    git clone --depth 1 https://github.com/openstack/rally.git -b $RALLY_TAG /src/rally && \
    update-requirements -s --source /src/openstack-requirements /src/rally/ && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        /src/os-faults /src/rally && \
    pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        git+https://gerrit.opnfv.org/gerrit/functest@$BRANCH#egg=functest \
        git+https://gerrit.opnfv.org/gerrit/parser#egg=nfv-heattranslator\&subdirectory=tosca2heat/heat-translator \
        git+https://gerrit.opnfv.org/gerrit/parser#egg=nfv-toscaparser\&subdirectory=tosca2heat/tosca-parser \
        -e git+https://gerrit.opnfv.org/gerrit/parser#egg=nfv-parser && \
    rm -r upper-constraints.txt /src/os-faults/.git /src/rally/.git && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'" > /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally-manage db create && \
    bash -c "mkdir -p /home/opnfv/functest{/conf,/data,/images,/results} /home/opnfv/repos/vnfs" && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["bash","-c","prepare_env start && run_tests -t all"]
