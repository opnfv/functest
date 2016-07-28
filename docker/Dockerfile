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

ENV HOME /home/opnfv
ENV repos_dir /home/opnfv/repos
ENV creds /home/opnfv/functest/conf/openstack.creds
ENV TERM xterm
ENV COLORTERM gnome-terminal
ENV PYTHONPATH $PYTHONPATH:/home/opnfv/repos/
ENV CONFIG_FUNCTEST_YAML /home/opnfv/repos/functest/ci/config_functest.yaml
WORKDIR /home/opnfv

# Packaged dependencies
RUN apt-get update && apt-get install -y \
ssh \
sshpass \
curl \
git \
gcc \
wget \
python-dev \
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


RUN mkdir -p ${repos_dir}
RUN mkdir -p /home/opnfv/functest/results
RUN mkdir -p /root/.ssh
RUN chmod 700 /root/.ssh

RUN git config --global http.sslVerify false
RUN git clone https://gerrit.opnfv.org/gerrit/functest ${repos_dir}/functest
RUN git clone https://gerrit.opnfv.org/gerrit/releng ${repos_dir}/releng
RUN git clone https://gerrit.opnfv.org/gerrit/doctor ${repos_dir}/doctor
RUN git clone -b 0.5.0 https://github.com/openstack/rally.git ${repos_dir}/rally
RUN git clone https://github.com/openstack/tempest.git ${repos_dir}/tempest
RUN git clone https://git.opendaylight.org/gerrit/p/integration/test.git ${repos_dir}/odl_test
RUN git clone -b stable https://github.com/boucherv-orange/clearwater-live-test ${repos_dir}/vims-test
RUN git clone https://github.com/openstack/networking-bgpvpn ${repos_dir}/bgpvpn
RUN git clone https://github.com/wuwenbin2/OnosSystemTest.git ${repos_dir}/onos
RUN git clone https://github.com/opnfv/promise ${repos_dir}/promise
RUN git clone https://gerrit.opnfv.org/gerrit/ovno ${repos_dir}/ovno
RUN git clone https://gerrit.opnfv.org/gerrit/copper ${repos_dir}/copper
RUN git clone https://gerrit.opnfv.org/gerrit/moon ${repos_dir}/moon
RUN git clone https://gerrit.opnfv.org/gerrit/sdnvpn ${repos_dir}/sdnvpn
RUN git clone https://github.com/openstack/kingbird.git ${repos_dir}/kingbird
RUN git clone https://gerrit.opnfv.org/gerrit/domino ${repos_dir}/domino
RUN git clone https://gerrit.opnfv.org/gerrit/parser ${repos_dir}/parser

RUN pip install -r ${repos_dir}/functest/docker/requirements.pip
RUN pip install -r ${repos_dir}/rally/requirements.txt
RUN pip install -r ${repos_dir}/tempest/requirements.txt
RUN pip install -r ${repos_dir}/parser/tosca2heat/tosca-parser/requirements.txt
RUN pip install -r ${repos_dir}/parser/tosca2heat/heat-translator/requirements.txt
RUN cd ${repos_dir}/parser/tosca2heat/tosca-parser && python setup.py install
RUN cd ${repos_dir}/parser/tosca2heat/heat-translator && python setup.py install


RUN ${repos_dir}/rally/install_rally.sh --yes

ADD http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img /home/opnfv/functest/data/
ADD http://205.177.226.237:9999/onosfw/firewall_block_image.img /home/opnfv/functest/data/

RUN gpg --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
RUN curl -L https://get.rvm.io | bash -s stable

RUN /bin/bash -c ". /home/opnfv/repos/functest/testcases/features/sfc/tacker_client_install.sh"
RUN cd ${repos_dir}/bgpvpn && pip install .
RUN cd ${repos_dir}/kingbird && pip install -e .

RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd /home/opnfv/repos/vims-test \
    && rvm autolibs enable"
RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd /home/opnfv/repos/vims-test \
    && rvm install 1.9.3"
RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd /home/opnfv/repos/vims-test \
    && rvm use 1.9.3"
RUN /bin/bash -c ". /etc/profile.d/rvm.sh \
    && cd /home/opnfv/repos/vims-test \
    && bundle install"

RUN sh -c 'curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -'
RUN sudo apt-get install -y nodejs
RUN cd ${repos_dir}/promise && sudo npm -g install npm@latest
RUN cd ${repos_dir}/promise && npm install

RUN echo "set nocompatible \n\
set backspace=2" \
>> /home/opnfv/.vimrc
RUN echo set nocompatible >> /home/opnfv/.exrc
RUN echo "alias ll='ls -lh' \n\
. /home/opnfv/repos/functest/cli/functest-complete.sh" \
>> /home/opnfv/.bashrc
RUN cd ${repos_dir}/functest/cli && pip install .
