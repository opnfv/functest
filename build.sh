#!/bin/bash

set -e

repo=${repo:-opnfv}
amd64_dirs=${amd64_dirs-"\
docker/core \
docker/healthcheck \
docker/smoke \
docker/features \
docker/components \
docker/vnf \
docker/parser \
docker/restapi"}
arm64_dirs=${arm64_dirs-$(echo "${amd64_dirs}" | sed -e "s|docker/vnf||" \
    -e "s|docker/restapi||")}

find . -name Dockerfile -exec sed -i -e "s|opnfv/functest-core:euphrates|${repo}/functest-core:amd64-euphrates|g" {} +
if [[ ${amd64_dirs} != *"docker/core"* ]]; then
    docker pull "${repo}/functest-core:amd64-euphrates"
fi
for dir in ${amd64_dirs}; do
    (cd "${dir}" && docker build --no-cache -t "${repo}/functest-${dir##**/}:amd64-euphrates" .)
    docker push "${repo}/functest-${dir##**/}:amd64-euphrates"
done
find . -name Dockerfile -exec git checkout {} +

find . -name Dockerfile -exec sed -i -e "s|alpine:3.6|multiarch/alpine:arm64-v3.6|g" {} +
find . -name Dockerfile -exec sed -i -e "s|opnfv/functest-core:euphrates|${repo}/functest-core:arm64-euphrates|g" {} +
if [[ ${arm64_dirs} != *"docker/core"* ]]; then
    docker pull "${repo}/functest-core:arm64-euphrates"
fi
for dir in ${arm64_dirs}; do
    (cd "${dir}" && docker build --no-cache -t "${repo}/functest-${dir##**/}:arm64-euphrates" .)
    docker push "${repo}/functest-${dir##**/}:arm64-euphrates"
done
find . -name Dockerfile -exec git checkout {} +

exit $?
