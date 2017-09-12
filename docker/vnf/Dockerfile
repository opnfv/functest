FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/pike
ARG VIMS_TAG=stable

RUN apk --no-cache add --update \
        ruby ruby-bundler ruby-irb ruby-rdoc dnsmasq \
        procps libxslt libxml2 zlib libffi python3 go musl-dev && \
    apk --no-cache add --virtual .build-deps --update \
        ruby-dev g++ make libxslt-dev libxml2-dev zlib-dev libffi-dev && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ | \
        > upper-constraints.txt && \
    git clone --depth 1 -b $VIMS_TAG https://github.com/boucherv-orange/clearwater-live-test /src/vims-test && \
    git clone https://github.com/RebacaInc/abot_charm.git /src/epc-requirements/abot_charm && \
    python3 -m pip install --no-cache-dir --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        juju-wait && \
    go get github.com/rogpeppe/godeps && \
    (cd /src/vims-test && bundle config build.nokogiri --use-system-libraries && bundle install --system) && \
    rm -r upper-constraints.txt /src/vims-test/.git /src/epc-requirements/abot_charm/.git && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
