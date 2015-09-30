FROM ubuntu:14.04
MAINTAINER Jose Lausuch <jose.lausuch@ericsson.com>

ENV repo_dir /home/repos
ENV rally_commit 9a17d8490e7fb4afee2f5629e6db41eabe4bc4d4

# Packaged dependencies
RUN apt-get update && apt-get install -y \
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
RUN git clone https://gerrit.opnfv.org/gerrit/functest ${repo_dir}/functest
RUN git clone https://gerrit.opnfv.org/gerrit/releng ${repo_dir}/releng
RUN git clone https://github.com/openstack/rally.git ${repo_dir}/rally
RUN cd ${repo_dir}/rally/ && git reset --hard ${rally_commit}

