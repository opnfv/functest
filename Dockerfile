########################################
#   Docker container for FUNCTEST
########################################
# Purpose: run all the tests against the POD
#          from a pre-installed docker image
#
# Maintained by Jose Lausuch
# Build:
#    $ docker build -t opnfv/functest:tag .
#
# Execution:
#    $ docker run -t -i \
#      -e "INSTALLER_TYPE=fuel|apex|compass|joid \
#      -e "INSTALLER_IP=10.20.0.2" \
#      -v $(pwd)/config_functest.yaml:/home/opnfv/repos/functest/ci/config_functest.yaml
#      opnfv/functest /bin/bash
#
# NOTE: providing config_functest.yaml is optional. If not provided, it will
#       use the default one located in the repo
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
#

FROM ubuntu:14.04
MAINTAINER Jose Lausuch <jose.lausuch@ericsson.com>
LABEL version="0.1" description="OPNFV Functest Docker container"

ARG BRANCH=master
ARG TEMPEST_TAG=12.2.0
ARG RALLY_TAG=0.7.0
ARG ODL_TAG=release/beryllium-sr3
ARG OPENSTACK_TAG=stable/mitaka
ARG KINGBIRD_TAG=0.2.2
ARG VIMS_TAG=stable
ENV HOME /home/opnfv
ENV repos_dir /home/opnfv/repos
ENV creds /home/opnfv/functest/conf/openstack.creds
ENV TERM xterm
ENV COLORTERM gnome-terminal
ENV PYTHONPATH $PYTHONPATH:/home/opnfv/repos/
ENV CONFIG_FUNCTEST_YAML /home/opnfv/repos/functest/functest/ci/config_functest.yaml
ENV PYTHONPATH $PYTHONPATH:/home/opnfv/repos/:/home/opnfv/repos/functest
ENV VIRTUAL_ENVS_DIR /home/opnfv/functest/virtual_envs

WORKDIR /home/opnfv
COPY . ${repos_dir}/functest

# Packaged dependencies
RUN apt-get update && apt-get install -y \
ssh \
sshpass \
curl \
git \
gcc \
wget \
python-dev \
python-mock \
python-pip \
bundler \
postgresql \
build-essential \
libpq-dev \
libxslt-dev \
libssl-dev \
libgmp3-dev \
libxml2-dev \
libffi-dev \
crudini \
ruby1.9.1-dev \
--no-install-recommends


RUN mkdir -p ${repos_dir} \
    && mkdir -p /home/opnfv/functest/results \
    && mkdir -p /home/opnfv/functest/conf \
    && mkdir -p /root/.ssh \
    && chmod 700 /root/.ssh \
    && mkdir -p ${VIRTUAL_ENVS_DIR}

RUN pip install --upgrade pip \
    && pip install virtualenv

RUN git config --global http.sslVerify false

# OPNFV repositories
#RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/functest ${repos_dir}/functest
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/copper ${repos_dir}/copper
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/moon ${repos_dir}/moon
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/sdnvpn ${repos_dir}/sdnvpn
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/domino ${repos_dir}/domino
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/parser ${repos_dir}/parser
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/doctor ${repos_dir}/doctor
RUN git clone --depth 1 -b $BRANCH https://gerrit.opnfv.org/gerrit/ovno ${repos_dir}/ovno
RUN git clone --depth 1 https://github.com/opnfv/promise ${repos_dir}/promise
RUN git clone --depth 1 https://gerrit.opnfv.org/gerrit/securityscanning ${repos_dir}/securityscanning
RUN git clone --depth 1 https://gerrit.opnfv.org/gerrit/releng ${repos_dir}/releng


# OpenStack repositories
RUN git clone --depth 1 -b $OPENSTACK_TAG https://github.com/openstack/networking-bgpvpn ${repos_dir}/bgpvpn
RUN git clone --depth 1 -b $KINGBIRD_TAG https://github.com/openstack/kingbird.git ${repos_dir}/kingbird
RUN git clone --depth 1 -b $RALLY_TAG https://github.com/openstack/rally.git ${repos_dir}/rally
RUN git clone --depth 1 -b $TEMPEST_TAG https://github.com/openstack/tempest.git ${repos_dir}/tempest

# other repositories
RUN git clone --depth 1 -b $ODL_TAG https://git.opendaylight.org/gerrit/p/integration/test.git ${repos_dir}/odl_test
RUN git clone --depth 1 -b $VIMS_TAG https://github.com/boucherv-orange/clearwater-live-test ${repos_dir}/vims-test
RUN git clone --depth 1 https://github.com/wuwenbin2/OnosSystemTest.git ${repos_dir}/onos

# configure functest
RUN pip install -r ${repos_dir}/functest/docker/requirements.pip
RUN find ${repos_dir}/functest -name "*.py" \
    -not -path *unit_tests* |xargs grep __main__ |cut -d\: -f 1 |xargs chmod -c 755
RUN find ${repos_dir}/functest -name "*.sh" |xargs grep \#\! |cut -d\:  -f 1 |xargs chmod -c 755

# config rally
# comment now as rally is using venv itself
#RUN pip install -r ${repos_dir}/rally/requirements.txt
RUN ${repos_dir}/rally/install_rally.sh --yes

# config tempest
ENV TEMPEST_VENV_DIR=${VIRTUAL_ENVS_DIR}/tempest
RUN virtualenv ${TEMPEST_VENV_DIR} \
    && cd ${TEMPEST_VENV_DIR} \
    && . bin/activate \
    && pip install --upgrade pip \ 
    && pip install -r ${repos_dir}/tempest/requirements.txt \
    && deactivate

# config parser
ENV PARSER_VENV_DIR=${VIRTUAL_ENVS_DIR}/parser
RUN virtualenv ${PARSER_VENV_DIR} \
    && cd ${PARSER_VENV_DIR} \
    && . bin/activate \
    && /bin/bash ${repos_dir}/parser/tests/parser_install.sh ${repos_dir} \
    && deactivate

ADD http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img /home/opnfv/functest/data/
ADD http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-lxc.tar.gz /home/opnfv/functest/data/
ADD http://205.177.226.237:9999/onosfw/firewall_block_image.img /home/opnfv/functest/data/

RUN gpg --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
RUN curl -L https://get.rvm.io | bash -s stable

# configure tacker client
ENV TACKER_CLIENT_VENV_DIR=${VIRTUAL_ENVS_DIR}/tacker
RUN virtualenv ${TACKER_CLIENT_VENV_DIR} \
    && cd ${TACKER_CLIENT_VENV_DIR} \
    && . bin/activate \
    && pip install --upgrade pip \
#    && /bin/bash -c ". /home/opnfv/repos/functest/functest/opnfv_tests/features/sfc/tacker_client_install.sh" \
    && deactivate

# configure bgpvpn
ENV BGPVPN_VENV_DIR=${VIRTUAL_ENVS_DIR}/bgpvpn
RUN virtualenv ${BGPVPN_VENV_DIR} \
    && cd ${BGPVPN_VENV_DIR} \
    && . bin/activate \
    && pip install --upgrade pip \
#    && cd ${repos_dir}/bgpvpn && pip install . \
    && deactivate

# configure kingbird
ENV KINGBIRD_VENV_DIR=${VIRTUAL_ENVS_DIR}/kingbird
RUN virtualenv ${KINGBIRD_VENV_DIR} \
    && cd ${KINGBIRD_VENV_DIR} \
    && . bin/activate \
    && pip install --upgrade pip \
    && cd ${repos_dir}/kingbird && pip install -e . \
    && deactivate

# configure moonclient
ENV MOONCLIENT_VENV_DIR=${VIRTUAL_ENVS_DIR}/moonclient
RUN virtualenv ${MOONCLIENT_VENV_DIR} \
    && cd ${MOONCLIENT_VENV_DIR} \
    && . bin/activate \
    && pip install --upgrade pip \
#    && cd ${repos_dir}/moon/moonclient/ && python setup.py install \
    && deactivate

# config promise 
RUN sh -c 'curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -' \
    && sudo apt-get install -y nodejs \
    && cd ${repos_dir}/promise \
    && sudo npm -g install npm@latest \
    && npm install

RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd /home/opnfv/repos/vims-test \
    && rvm autolibs enable"
RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd /home/opnfv/repos/vims-test \
    && rvm install 1.9.3"
RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd /home/opnfv/repos/vims-test \
    && rvm use 1.9.3"
#RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
#    && cd /home/opnfv/repos/vims-test \
#    && bundle install"


RUN echo "set nocompatible \n\
set backspace=2" \
>> /home/opnfv/.vimrc
RUN echo set nocompatible >> /home/opnfv/.exrc
RUN echo "alias ll='ls -lh' \n\
. /home/opnfv/repos/functest/functest/cli/functest-complete.sh" \
>> /home/opnfv/.bashrc
RUN cd ${repos_dir}/functest/functest/cli && pip install .
