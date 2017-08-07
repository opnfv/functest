FROM opnfv/functest-core

ARG VIMS_TAG=stable

RUN apk --no-cache add --update \
        ruby ruby-dev ruby-bundler ruby-irb ruby-rdoc \
        procps git g++ make libxslt-dev libxml2-dev zlib-dev libffi-dev && \
    git clone --depth 1 -b $VIMS_TAG https://github.com/boucherv-orange/clearwater-live-test /src/vims-test && \
    rm -r /src/vims-test/.git && \
    cd /src/vims-test && bundle config build.nokogiri --use-system-libraries && bundle install --system
COPY testcases.yaml /usr/lib/python2.7/site-packages/functest/ci/testcases.yaml
CMD ["bash","-c","prepare_env start && run_tests -t all"]
