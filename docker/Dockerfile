########################################
#   Docker container for FUNCTEST
########################################
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

FROM ubuntu:14.04
MAINTAINER Jose Lausuch <jose.lausuch@ericsson.com>
LABEL version="0.1" description="OPNFV Functest Docker container"

# Environment variables
ARG BRANCH=master
ARG RALLY_TAG=0.8.1
ARG ODL_TAG=release/carbon
ARG OPENSTACK_TAG=stable/ocata
ARG VIMS_TAG=stable
ARG REPOS_DIR=/home/opnfv/repos
ARG FUNCTEST_BASE_DIR=/home/opnfv/functest
ARG FUNCTEST_CONF_DIR=${FUNCTEST_BASE_DIR}/conf
ARG FUNCTEST_DATA_DIR=${FUNCTEST_BASE_DIR}/data
ARG FUNCTEST_IMAGES_DIR=${FUNCTEST_BASE_DIR}/images
ARG FUNCTEST_RESULTS_DIR=${FUNCTEST_BASE_DIR}/results
ARG FUNCTEST_DIR=/usr/local/lib/python2.7/dist-packages/functest/
ARG REPOS_VNFS_DIR=${REPOS_DIR}/vnfs

# Environment variables
ENV CONFIG_FUNCTEST_YAML ${FUNCTEST_DIR}/ci/config_functest.yaml
ENV REPOS_DIR ${REPOS_DIR}
ENV creds ${FUNCTEST_CONF_DIR}/openstack.creds

# Packaged dependencies
RUN apt-get update && apt-get install -y \
build-essential \
bundler \
crudini \
curl \
dnsmasq \
gcc \
git \
libffi-dev \
libgmp3-dev \
libpq-dev \
libssl-dev \
libxml2-dev \
libxslt-dev \
libzmq3-dev \
python-dev \
python-mock \
python-pip \
postgresql \
ruby \
ruby-dev \
ruby-bundler \
ssh \
sshpass \
wget \
--no-install-recommends

RUN pip install --upgrade pip && easy_install -U setuptools==30.0.0

RUN mkdir -p ${REPOS_VNFS_DIR} \
    && mkdir -p ${FUNCTEST_BASE_DIR}/results \
    && mkdir -p ${FUNCTEST_CONF_DIR} \
    && mkdir -p ${FUNCTEST_DATA_DIR} \
    && mkdir -p ${FUNCTEST_IMAGES_DIR} \
    && mkdir -p /root/.ssh \
    && chmod 700 /root/.ssh

RUN git config --global http.sslVerify false

COPY thirdparty-requirements.txt thirdparty-requirements.txt
RUN wget -q -O- https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt?h=$OPENSTACK_TAG | \
        sed -E s/^tempest==+\(.*\)$/-e\ git+https:\\/\\/github.com\\/openstack\\/tempest@\\1#egg=tempest/ \
        > upper-constraints.txt && \
    pip install --src /src -cupper-constraints.txt \
        -chttps://git.opnfv.org/functest/plain/upper-constraints.txt?h=$BRANCH \
        git+https://gerrit.opnfv.org/gerrit/functest@$BRANCH#egg=functest \
        -rthirdparty-requirements.txt && \
    mkdir -p /etc/rally && \
    printf "[database]\nconnection = 'sqlite:////var/lib/rally/database/rally.sqlite'" > /etc/rally/rally.conf && \
    mkdir -p /var/lib/rally/database && rally-manage db create && \
    rm thirdparty-requirements.txt upper-constraints.txt

# OPNFV repositories
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/domino /src/domino
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/doctor ${REPOS_DIR}/doctor
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/fds /src/fds

# other repositories
RUN git clone --depth 1 -b $ODL_TAG https://git.opendaylight.org/gerrit/p/integration/test.git /src/odl_test
RUN git clone --depth 1 -b $VIMS_TAG https://github.com/boucherv-orange/clearwater-live-test /src/vims-test
RUN git clone --depth 1 https://github.com/wuwenbin2/OnosSystemTest.git ${REPOS_DIR}/onos

# SFC integration
RUN /bin/bash -c ". /usr/local/lib/python2.7/dist-packages/sfc/tests/functest/setup_scripts/tacker_client_install.sh"

# Install tempest venv and create symlink for running refstack-client
RUN ln -s /src/tempest /src/refstack-client/.tempest \
    && virtualenv --system-site-packages /src/tempest/.venv

RUN cd /src/vims-test && bundle install

RUN sh -c 'curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -' \
    && sudo apt-get install -y nodejs \
    && cd /src/promise && sudo npm -g install npm@latest \
    && cd /src/promise/source && npm install

RUN echo ". ${FUNCTEST_DIR}/cli/functest-complete.sh" >> /root/.bashrc
