FROM opnfv/functest-core

ARG BRANCH=master
ARG OPENSTACK_TAG=stable/queens
ARG VIMS_TEST_TAG=release-129
ARG QUAFF_TAG=59213d6d8ee29433552bb75f505cdc96b0b18909
ARG CLOUDIFY_VIMS_TAG=fraser
ARG HEAT_VIMS_TAG=release-129
ARG VROUTER_TAG=fraser
ARG JUJU_TAG=tags/juju-2.2.5
ARG JUJU_WAIT_TAG=2.6.4
ARG ABOT_CHARM=opnfv-fraser

ENV GOPATH /src/epc-requirements/go
ENV GOBIN /src/epc-requirements/go/bin
ENV PATH $GOBIN:$PATH

RUN apk --no-cache add --update \
        ruby ruby-bundler ruby-irb ruby-rdoc dnsmasq \
        procps libxslt libxml2 zlib libffi python3 go musl-dev && \
    apk --no-cache add --virtual .build-deps --update \
        ruby-dev g++ make libxslt-dev libxml2-dev zlib-dev libffi-dev g++ make && \
    wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/git.openstack.org\\/openstack\\/tempest@\\1#egg=tempest/ \
        > upper-constraints.txt && \
    wget -q -O- https://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH | \
        sed -E /#egg=functest/d > upper-constraints.opnfv.txt && \
    git clone --depth 1 -b $VIMS_TEST_TAG https://github.com/Metaswitch/clearwater-live-test /src/vims-test && \
    sed -i s/unf_ext\ \(.*\)/unf_ext\ \(0.0.7.4\)/g /src/vims-test/Gemfile.lock && \
    git init /src/vims-test/quaff && \
    (cd /src/vims-test/quaff && \
        git fetch --tags https://github.com/Metaswitch/quaff $QUAFF_TAG && \
        git checkout FETCH_HEAD) && \
    git init /src/vims-test/build-infra && \
    (cd /src/vims-test/build-infra && \
        git fetch --tags https://github.com/Metaswitch/clearwater-build-infra $VIMS_TEST_TAG && \
        git checkout FETCH_HEAD) && \
    git init /src/cloudify_vims && \
    (cd /src/cloudify_vims && \
        git fetch --tags https://github.com/Orange-OpenSource/opnfv-cloudify-clearwater.git $CLOUDIFY_VIMS_TAG && \
        git checkout FETCH_HEAD) && \
    git init  /src/heat_vims && \
    (cd /src/heat_vims && \
        git fetch --tags https://github.com/Metaswitch/clearwater-heat.git $HEAT_VIMS_TAG && \
        git checkout FETCH_HEAD) && \
    git init /src/opnfv-vnf-vyos-blueprint && \
    (cd /src/opnfv-vnf-vyos-blueprint && \
        git fetch --tags https://github.com/oolorg/opnfv-vnf-vyos-blueprint.git $VROUTER_TAG && \
        git checkout FETCH_HEAD) && \
    mkdir -p /home/opnfv/functest/data/router && \
    git init /home/opnfv/functest/data/router/opnfv-vnf-data && \
    (cd /home/opnfv/functest/data/router/opnfv-vnf-data && \
        git fetch --tags https://github.com/oolorg/opnfv-vnf-data.git $VROUTER_TAG && \
        git checkout FETCH_HEAD) && \
    git init /src/epc-requirements/abot_charm && \
    (cd /src/epc-requirements/abot_charm && \
        git fetch --tags https://github.com/RebacaInc/abot_charm.git $ABOT_CHARM && \
        git checkout FETCH_HEAD) && \
    python3 -m pip install --no-cache-dir --src /src -cupper-constraints.txt -cupper-constraints.opnfv.txt \
        juju-wait==$JUJU_WAIT_TAG && \
    go get github.com/rogpeppe/godeps && \
    go get -d -v github.com/juju/juju/... || true && \
    (cd $GOPATH/src/github.com/juju/juju && git checkout $JUJU_TAG && godeps -u dependencies.tsv) && \
    go install -v github.com/juju/juju/... && \
    rm -r $GOPATH/src/ $GOPATH/pkg && \
    (cd /src/vims-test && bundle config build.nokogiri --use-system-libraries && bundle install --system) && \
    rm -r upper-constraints.txt upper-constraints.opnfv.txt /src/vims-test/.git /src/cloudify_vims/.git /src/heat_vims/.git /src/vims-test/quaff/.git \
        /src/vims-test/build-infra/.git /src/opnfv-vnf-vyos-blueprint/.git \
        /src/epc-requirements/abot_charm/.git && \
    apk del .build-deps
COPY testcases.yaml /usr/lib/python2.7/site-packages/xtesting/ci/testcases.yaml
CMD ["run_tests", "-t", "all"]
