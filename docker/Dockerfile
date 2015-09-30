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
#    $ docker run -t -i -e "INSTALLER_TYPE=fuel/foreman" -e "INSTALLER_IP=10.20.0.2/172.30.10.73"
#


FROM ubuntu:14.04
MAINTAINER Jose Lausuch <jose.lausuch@ericsson.com>
LABEL version="0.1" description="OPNFV Functest Docker container"

ENV repo_dir /home/repos
ENV rally_commit 9a17d8490e7fb4afee2f5629e6db41eabe4bc4d4

# Packaged dependencies
RUN apt-get update && apt-get install -y \
    ssh \
    sshpass \
	git \
	gcc \
	wget \
	python-dev \
	postgresql \
	libxslt-dev \
	libssl-dev \
	libgmp3-dev \
	libxml2-dev \
	libffi-dev \
	--no-install-recommends


RUN mkdir ${repo_dir}
RUN mkdir /home/functest
RUN git clone https://gerrit.opnfv.org/gerrit/functest ${repo_dir}/functest
RUN git clone https://gerrit.opnfv.org/gerrit/releng ${repo_dir}/releng
RUN git clone https://github.com/openstack/rally.git ${repo_dir}/rally
RUN cd ${repo_dir}/rally/ && git reset --hard ${rally_commit}

RUN pip install -r ${repo_dir}/functest/docker/requirements.pip